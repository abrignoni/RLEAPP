"""Cross-core regression coverage for ALEAPP #1646. Author: @AlexisBrignoni, Codex.

Exercise console fallback under real descriptor exhaustion in a child process.
"""
import errno
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from scripts import ilapfuncs  # pylint: disable=wrong-import-position




















class LoggingLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.old_path = ilapfuncs.OutputParameters.screen_output_file_path
        self.addCleanup(setattr, ilapfuncs.OutputParameters, 'screen_output_file_path', self.old_path)
        self.log_temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.log_temp.cleanup)
        self.addCleanup(ilapfuncs.close_screen_log)
        ilapfuncs.OutputParameters.screen_output_file_path = str(pathlib.Path(self.log_temp.name) / 'log.html')

    def test_descriptor_errors_fall_back_to_console(self):
        for code in (errno.EMFILE, errno.ENFILE):
            output = io.StringIO()
            with patch('builtins.open', side_effect=OSError(code, 'descriptor exhaustion')), patch('sys.stdout', output):
                ilapfuncs.logfunc('original parser failure')
            self.assertIn('HTML log unavailable', output.getvalue())
            self.assertIn('original parser failure', output.getvalue())
            ilapfuncs.close_screen_log()

    def test_unrelated_logging_errors_remain_visible(self):
        with patch('builtins.open', side_effect=PermissionError(errno.EACCES, 'permission denied')):
            with self.assertRaises(PermissionError):
                ilapfuncs.logfunc('message')

    def test_normal_html_and_console_logging(self):
        with tempfile.TemporaryDirectory() as temp:
            path = pathlib.Path(temp) / 'log.html'
            ilapfuncs.OutputParameters.screen_output_file_path = str(path)
            with patch('sys.stdout', new_callable=io.StringIO) as output:
                ilapfuncs.logfunc('normal message')
            self.assertEqual(path.read_text(), 'normal message<br>' + ilapfuncs.OutputParameters.nl)
            self.assertEqual(output.getvalue(), 'normal message\n')

    @unittest.skipIf(sys.platform == 'win32', 'RLIMIT_NOFILE is Unix-only')
    def test_real_descriptor_exhaustion_in_child_process(self):
        result = subprocess.run([sys.executable, '-B', __file__, '--descriptor-stress'],
                                cwd=REPO_ROOT, capture_output=True, text=True, check=False, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('exhausted-descriptor logging: PASS', result.stdout)


def descriptor_stress():
    """Lower limits in this child only; fail if large stores still need N handles."""
    import resource  # pylint: disable=import-outside-toplevel
    with tempfile.TemporaryDirectory() as temp:
        root = pathlib.Path(temp)
        original = resource.getrlimit(resource.RLIMIT_NOFILE)
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, original[1]))
        handles = []
        try:
            # Exhaust descriptors for real, then exercise the actual logger.
            while True:
                try:
                    handles.append(open(root / 'held', 'ab'))  # pylint: disable=consider-using-with
                except OSError as exc:
                    assert exc.errno == errno.EMFILE
                    break
            ilapfuncs.OutputParameters.screen_output_file_path = str(root / 'log.html')
            ilapfuncs.logfunc('descriptor exhaustion remains recoverable')
        finally:
            for handle in handles:
                handle.close()
            resource.setrlimit(resource.RLIMIT_NOFILE, original)
            ilapfuncs.close_screen_log()
    print('exhausted-descriptor logging: PASS')


if __name__ == '__main__':
    if sys.argv[1:] == ['--descriptor-stress']:
        descriptor_stress()
    else:
        unittest.main()

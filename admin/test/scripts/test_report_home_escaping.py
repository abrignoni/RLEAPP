"""Values read from the evidence are escaped on the report home page tabs."""
import contextlib
import io
import pathlib
import shutil
import tempfile
import unittest

from scripts import ilapfuncs

PAYLOAD = '<svg onload=document.title=1>'
MAIN_SCRIPT = pathlib.Path(__file__).resolve().parents[3] / 'rleapp.py'


class ReportHomeEscapingTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.log = pathlib.Path(self.tmp) / 'Screen_Output.html'
        saved_path = getattr(ilapfuncs.OutputParameters, 'screen_output_file_path', '')
        saved_nl = getattr(ilapfuncs.OutputParameters, 'nl', None)
        def restore():
            ilapfuncs.close_screen_log()
            ilapfuncs.OutputParameters.screen_output_file_path = saved_path
            ilapfuncs.OutputParameters.nl = saved_nl
        self.addCleanup(restore)
        ilapfuncs.OutputParameters.screen_output_file_path = str(self.log)
        ilapfuncs.OutputParameters.nl = '\n'

    def _logged(self, message):
        console = io.StringIO()
        with contextlib.redirect_stdout(console):
            ilapfuncs.logfunc(message)
        ilapfuncs.close_screen_log()
        return self.log.read_text(encoding='utf8'), console.getvalue()

    def test_run_log_file_is_escaped_and_console_stays_raw(self):
        text, console = self._logged(PAYLOAD)
        self.assertNotIn('<svg', text)
        self.assertIn('&lt;svg', text)
        self.assertIn(PAYLOAD, console)

    def test_ordinary_run_log_line_is_unchanged(self):
        text, _ = self._logged('Parsed "a" from b\'s file')
        self.assertIn('Parsed "a" from b\'s file<br>', text)

    def test_processed_files_log_escapes_its_values(self):
        source = MAIN_SCRIPT.read_text(encoding='utf8')
        for expected in ('{esc(input_path)}', '{esc(plugin.name)}', '{esc(artifact_search_regex)}',
                         '{esc(Context.get_relative_path(display_path))}'):
            self.assertIn(expected, source)


if __name__ == '__main__':
    unittest.main()

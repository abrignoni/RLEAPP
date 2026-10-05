"""Complete liked-tweet strings and invalid-record isolation."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.artifacts import twitterReturnsTip as artifact


EXPECTED = [
    ('100', 'He said "yes", then: café ☕\n<sample & text>',
     'https://example.test/a?q="x",y: z'),
    ('101', 'Plain text', 'https://example.test/101'),
    ('102', '', ''),
]


def create_fixture(root):
    """Construct legacy-style signed text wrapping indented JSON field lines."""
    path = Path(root) / 'CONSTRUCTED' / 'account-like.txt'
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ['-----BEGIN PGP SIGNED MESSAGE-----', 'Hash: SHA256', '', '[']
    for values in EXPECTED:
        lines.extend(['  {', '    "like": {'])
        for field, value in zip(('tweetId', 'fullText', 'expandedUrl'), values):
            lines.append(f'      "{field}": {json.dumps(value, ensure_ascii=True)},')
        lines.extend(['    }', '  },'])
    lines.extend([']', '-----BEGIN PGP SIGNATURE-----', 'CONSTRUCTED ONLY'])
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return path


class Context:
    def __init__(self, root, path):
        self.root, self.path = Path(root), path

    def get_files_found(self):
        return [self.path]

    def get_relative_path(self, path):
        return str(Path(path).relative_to(self.root))


class TestTwitterLikeText(unittest.TestCase):
    def test_complete_strings_and_existing_helper(self):
        with tempfile.TemporaryDirectory() as directory:
            path = create_fixture(directory)
            headers, rows, source = artifact.twitterLike.__wrapped__(Context(directory, path))
        self.assertEqual(headers, ('Tweet ID', 'Full Text', 'Expanded URL'))
        self.assertEqual(rows, EXPECTED)
        self.assertEqual(source, 'CONSTRUCTED/account-like.txt')
        # Other return artifacts retain their previously documented interpretation.
        self.assertEqual(getattr(artifact, '_value')('"text": "a,b: c",'), 'ab')

    def test_invalid_records_do_not_reuse_prior_text(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid-like.txt'
            blocks = []
            for number, invalid in enumerate(('null', '42', '"unterminated', '"text" trailing')):
                blocks.extend([f'"tweetId": "bad{number}",',
                               f'"fullText": {invalid},', '"expandedUrl": "bad-url",'])
            blocks.extend(['"tweetId": "bad-id" junk,', '"fullText": "bad text",',
                           '"expandedUrl": "bad-url",', '"tweetId": "bad-url",',
                           '"fullText": "bad text",', '"expandedUrl": false,',
                           '"tweetId": "good",', '"fullText": "fresh, intact: text",',
                           '"expandedUrl": "good-url",', '"expandedUrl": "standalone",'])
            path.write_text('\n'.join(blocks), encoding='utf-8')
            with patch.object(artifact, 'logfunc') as log:
                _, rows, _ = artifact.twitterLike.__wrapped__(Context(directory, path))
        self.assertEqual(rows, [('good', 'fresh, intact: text', 'good-url'),
                                ('', '', 'standalone')])
        self.assertEqual(log.call_count, 6)
        self.assertTrue(all('invalid-like.txt:' in call.args[0] for call in log.call_args_list))


if __name__ == '__main__':
    unittest.main()

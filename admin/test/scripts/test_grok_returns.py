"""xAI (Grok) return helpers and the Twitter account artifact's xAI guard. Constructed values only."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.artifacts import grokReturns as grok
from scripts.artifacts import twitterReturnsTip as twitter

USER = '00000000-0000-4000-8000-000000000001'
ASSET = '00000000-0000-4000-8000-0000000000aa'


def signed(body):
    return ('-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA512\n\n' + body +
            '\n-----BEGIN PGP SIGNATURE-----\nCONSTRUCTED ONLY\n-----END PGP SIGNATURE-----\n')


class Context:
    def __init__(self, root, paths):
        self.root, self.paths = Path(root), paths

    def get_files_found(self):
        return [str(p) for p in self.paths]

    def get_relative_path(self, path):
        return str(Path(path).relative_to(self.root)) if path else ''


class TestGrokHelpers(unittest.TestCase):
    def test_timestamps(self):
        for text in ('2026-01-02T03:04:05.1234+00:00', '2026-01-02T03:04:05.12345+00:00',
                     '2026-01-02T03:04:05.123400Z', '2026-01-02T03:04:05.1234+00:00'):
            dt = getattr(grok, '_ts')(text)
            self.assertEqual((dt.year, dt.second, dt.microsecond, dt.utcoffset().seconds),
                             (2026, 5, 123400 if '1234' in text and '12345' not in text else 123450, 0))
        self.assertEqual(getattr(grok, '_ts')('2026-01-02T05:04:05+02:00').hour, 3)
        dt = getattr(grok, '_ts')({'date': {'numberLong': '1767323045000'}})
        self.assertEqual(dt.isoformat(), '2026-01-02T03:04:05+00:00')
        self.assertEqual(getattr(grok, '_ts')({'$date': {'$numberLong': '1767323045000'}}), dt)
        self.assertEqual(getattr(grok, '_ts')(None), '')
        self.assertEqual(getattr(grok, '_ts')('not a time'), 'not a time')

    def test_unwrap_undoes_dash_escaping(self):
        body = getattr(grok, '_unwrap')(signed('[\n- -1\n]'))
        self.assertEqual(json.loads(body), [-1])
        self.assertEqual(getattr(grok, '_unwrap')('[1]'), '[1]')

    def test_key_filenames(self):
        key_filename = getattr(grok, '_key_filename')
        self.assertEqual(key_filename(f'users/{USER}/generated/{ASSET}/image.jpg'),
                         (f'{ASSET}_image.jpg', None))
        self.assertEqual(key_filename(f'https://assets.example/users/{USER}/{ASSET}/content'),
                         (None, ASSET))
        self.assertEqual(key_filename(f'imagine-public/images/{ASSET}.jpg'), (f'{ASSET}.jpg', None))
        self.assertEqual(key_filename('something/else'), (None, None))

    def test_primary_file_order(self):
        entries = [('_preview_image.jpg', 'p', 'p'), ('_image.jpg', 'i', 'i'), ('.jpeg', 'c', 'c')]
        self.assertEqual(getattr(grok, '_primary')(entries)[1], 'c')
        self.assertEqual(getattr(grok, '_primary')(entries[:2])[1], 'i')

    def test_only_xai_records_are_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            good = root / f'{USER}-ip-logs.txt'
            good.write_text(signed(json.dumps([{'xaiIpLog': {
                'userId': USER, 'ipAddress': '192.0.2.10',
                'createTime': '2026-01-02T03:04:05.123456+00:00',
                'lastLoginTime': '2026-01-03T03:04:05.123456+00:00'}}])), encoding='utf-8')
            wrong_wrapper = root / f'{USER.replace("1", "2")}-ip-logs.txt'
            wrong_wrapper.write_text(json.dumps([{'ipAudit': {'loginIp': '192.0.2.11'}}]))
            numeric = root / '123456789-ip-logs.txt'
            numeric.write_text(json.dumps([{'xaiIpLog': {'ipAddress': '192.0.2.12'}}]))
            ctx = Context(root, [good, wrong_wrapper, numeric, root])
            with patch.object(grok, 'logfunc'):
                headers, rows, source = grok.grokIpLogs.__wrapped__(ctx)
        self.assertEqual(headers[2], 'IP Address')
        self.assertEqual([r[2] for r in rows], ['192.0.2.10'])
        self.assertEqual(source, str(good))


class TestTwitterAccountSkipsXai(unittest.TestCase):
    def test_twitter_account_kept_and_xai_account_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tw = root / '123456789-account.txt'
            tw.write_text(signed('[\n  {\n    "account" : {\n      "email" : "a@example.test",\n'
                                 '      "createdVia" : "web",\n      "username" : "constructed",\n'
                                 '      "accountId" : "123456789",\n'
                                 '      "createdAt" : "2020-01-02T03:04:05.000Z"\n    }\n  }\n]'),
                          encoding='utf-8')
            xai = root / f'{USER}-account.txt'
            xai.write_text(signed('[\n  {\n    "xaiAccount" : {\n      "account" : {\n'
                                  f'        "userId" : "{USER}",\n'
                                  '        "email" : "b@example.test"\n      }\n    }\n  }\n]'),
                           encoding='utf-8')
            with patch.object(twitter, 'logfunc') as log:
                _, rows, source = twitter.twitterAccount.__wrapped__(Context(root, [tw, xai]))
                _, xai_rows, xai_source = twitter.twitterAccount.__wrapped__(Context(root, [xai]))
        self.assertEqual([(r[1], r[2], r[4]) for r in rows], [('123456789', 'a@example.test', 'constructed')])
        self.assertEqual(source, '123456789-account.txt')
        self.assertEqual((xai_rows, xai_source), ([], ''))
        self.assertTrue(any('xAI account file' in c.args[0] for c in log.call_args_list))


if __name__ == '__main__':
    unittest.main()

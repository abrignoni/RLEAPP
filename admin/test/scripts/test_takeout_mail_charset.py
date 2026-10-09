"""Synthetic MIME charset and first-plain selection controls. @AlexisBrignoni, Codex."""
import base64
import codecs
import quopri
import unittest
from email import policy
from email.message import Message
from email.parser import BytesParser
from unittest.mock import patch

from scripts.artifacts import takeoutGoogleMail as artifact

get_body = artifact._get_body  # pylint: disable=protected-access
decode_body = artifact._decode_body_payload  # pylint: disable=protected-access


def leaf(payload, charset=None, content_type='text/plain', transfer='base64', disposition=None):
    content_type += '' if charset is None else '; charset="' + charset + '"'
    headers = ['Content-Type: ' + content_type, 'Content-Transfer-Encoding: ' + transfer]
    if disposition is not None:
        headers.append('Content-Disposition: ' + disposition)
    if transfer == 'base64':
        encoded = base64.b64encode(payload)
    elif transfer == 'quoted-printable':
        encoded = quopri.encodestring(payload)
    else:
        encoded = payload
    return BytesParser(policy=policy.compat32).parsebytes(
        ('\r\n'.join(headers) + '\r\n\r\n').encode('ascii') + encoded)


def multipart(parts, content_type='multipart/mixed'):
    message = Message()
    message['Content-Type'] = content_type
    message.set_payload(parts)
    return message


class CharsetPolicyTests(unittest.TestCase):
    def test_supported_aliases(self):
        cases = [
            ('UTF-8', b'caf\xc3\xa9', 'café'),
            ('utf8', b'caf\xc3\xa9', 'café'),
            ('utf_8', b'caf\xc3\xa9', 'café'),
            ('latin1', b'caf\xe9', 'café'),
            ('ISO-8859-1', b'caf\xe9', 'café'),
            ('ASCII', b'plain ASCII', 'plain ASCII'),
            ('us-ascii', b'plain ASCII', 'plain ASCII'),
            ('CP1252', b'price \x80', 'price €'),
            ('windows-1252', b'price \x80', 'price €'),
            ('utf-16', b'\xff\xfeA\x00', 'A'),
            ('utf-16-le', b'A\x00', 'A'),
            ('utf-16-be', b'\x00A', 'A'),
        ]
        for charset, payload, expected in cases:
            with self.subTest(charset=charset):
                self.assertEqual(get_body(leaf(payload, charset)), expected)

    def test_missing_empty_unknown_and_malformed_fallback(self):
        for charset in (None, '', 'x-unknown-charset', 'utf 8', 'x' * 129):
            with self.subTest(charset=charset):
                self.assertEqual(get_body(leaf(b'caf\xc3\xa9', charset)), 'cafÃ©')

    def test_known_but_unsupported_character_encoding_falls_back(self):
        # ISO-8859-7 maps this byte to Greek alpha; finite support deliberately excludes it.
        self.assertEqual(get_body(leaf(b'\xe1', 'iso-8859-7')), 'á')

    def test_non_mime_transform_names_never_transform_payload(self):
        for charset in ('unicode_escape', 'raw_unicode_escape', 'idna', 'punycode',
                        'base64_codec', 'hex_codec', 'rot_13', 'undefined'):
            with self.subTest(charset=charset):
                self.assertEqual(get_body(leaf(b'\\u00e9', charset)), r'\u00e9')

    def test_invalid_declared_bytes_use_whole_payload_latin1(self):
        cases = [('utf-8', b'A\xc3\xa9\xff', 'AÃ©ÿ'),
                 ('ascii', b'A\xff', 'Aÿ'), ('utf-16', b'\xff', 'ÿ')]
        for charset, payload, expected in cases:
            with self.subTest(charset=charset):
                self.assertEqual(get_body(leaf(payload, charset)), expected)

    def test_transfer_decoding_precedes_character_decoding(self):
        for transfer in ('base64', 'quoted-printable', '8bit'):
            with self.subTest(transfer=transfer):
                self.assertEqual(get_body(leaf(b'caf\xc3\xa9', 'utf-8', transfer=transfer)), 'café')

    def test_first_plain_part_and_its_own_charset_win(self):
        message = multipart([leaf(b'<p>html</p>', 'utf-8', 'text/html'),
                             leaf(b'price \x80', 'cp1252'), leaf(b'later', 'utf-8')])
        message.set_param('charset', 'ascii')
        self.assertEqual(get_body(message), 'price €')

    def test_empty_first_plain_stops_before_later_plain(self):
        self.assertEqual(get_body(multipart([leaf(b'', 'utf-8'), leaf(b'later', 'utf-8')])), '')

    def test_first_plain_fallback_still_stops_before_later_plain(self):
        self.assertEqual(get_body(multipart([leaf(b'\xff', 'utf-8'), leaf(b'later', 'utf-8')])), 'ÿ')

    def test_none_payload_continues_to_next_plain(self):
        empty = Message()
        empty['Content-Type'] = 'text/plain; charset=utf-8'
        self.assertIsNone(empty.get_payload(decode=True))
        self.assertEqual(get_body(multipart([empty, leaf(b'next', 'ascii')])), 'next')

    def test_html_only_and_non_plain_are_blank(self):
        self.assertEqual(get_body(leaf(b'<p>html</p>', 'utf-8', 'text/html')), '')
        self.assertEqual(get_body(multipart([leaf(b'<p>html</p>', 'utf-8', 'text/html')])), '')

    def test_plain_attachment_and_nested_message_keep_selection(self):
        self.assertEqual(get_body(multipart([
            leaf(b'first', 'ascii', disposition='attachment'), leaf(b'later', 'ascii')])), 'first')
        nested = multipart([leaf(b'caf\xc3\xa9', 'utf-8')], 'message/rfc822')
        self.assertEqual(get_body(multipart([nested, leaf(b'later', 'ascii')])), 'café')

    def test_unrelated_lookup_failure_is_not_hidden(self):
        with patch.object(codecs, 'lookup', side_effect=RuntimeError('synthetic unexpected failure')):
            with self.assertRaisesRegex(RuntimeError, 'synthetic unexpected failure'):
                decode_body(leaf(b'A', 'utf-8'), b'A')


if __name__ == '__main__':
    unittest.main()

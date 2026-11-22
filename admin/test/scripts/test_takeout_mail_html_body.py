"""A Takeout message with no usable plain part is read from its HTML part."""
import unittest
from email.message import EmailMessage

from scripts.artifacts import takeoutGoogleMail as artifact

columns = artifact._body_columns  # pylint: disable=protected-access
PAGE = '<style>p{}</style><p>Hello&nbsp;<b>wor</b>ld</p><p><a href="https://example.test/x">link</a></p>'


def alternative(plain):
    message = EmailMessage()
    message.set_content(plain)
    message.add_alternative(PAGE, subtype='html')
    return message


class TakeoutHtmlBodyTests(unittest.TestCase):
    def test_plain_text_wins_when_it_has_text(self):
        self.assertEqual(columns(alternative('plain words\n')), ('plain words\n', 'text/plain', ''))

    def test_blank_plain_part_uses_html(self):
        self.assertEqual(columns(alternative('  \n')), ('Hello world\nlink [1]', 'text/html', '[1] https://example.test/x'))

    def test_html_only_message(self):
        message = EmailMessage()
        message.set_content(PAGE, subtype='html')
        self.assertEqual(columns(message)[:2], ('Hello world\nlink [1]', 'text/html'))

    def test_an_html_attachment_is_not_the_body(self):
        message = EmailMessage()
        message.set_content('  \n')
        message.add_attachment(PAGE, subtype='html', filename='page.html')
        self.assertEqual(columns(message)[1:], ('', ''))

    def test_an_attached_message_is_not_the_body(self):
        inner = EmailMessage()
        inner.set_content(PAGE, subtype='html')
        message = EmailMessage()
        message.set_content('  \n')
        message.add_attachment(inner)
        self.assertEqual(columns(message)[1:], ('', ''))

    def test_an_attached_multipart_is_not_the_body(self):
        inner = EmailMessage()
        inner.set_content(PAGE, subtype='html')
        inner.make_related()
        inner['Content-Disposition'] = 'attachment; filename="page.mht"'
        message = EmailMessage()
        message.set_content('  \n')
        message.make_mixed()
        message.attach(inner)
        self.assertEqual(columns(message)[1:], ('', ''))

    def test_unclosed_style_and_script_keep_their_text(self):
        for name in ('style', 'script'):
            message = EmailMessage()
            message.set_content(f'<{name}>a{{}}</{name}><p>Kept</p><{name}>open', subtype='html')
            self.assertEqual(columns(message)[0].splitlines()[0], 'Kept')
            self.assertIn('open', columns(message)[0])

    def test_markup_the_parser_refuses_does_not_stop_the_artifact(self):
        message = EmailMessage()
        message.set_content('<p>Hello</p><![bogus]>', subtype='html')
        self.assertIn('Hello', columns(message)[0])

    def test_no_text_parts(self):
        message = EmailMessage()
        message.set_content(b'x', maintype='application', subtype='octet-stream')
        self.assertEqual(columns(message), ('', '', ''))


if __name__ == '__main__':
    unittest.main()

"""Readable text and link targets of an HTML email body."""
import re
from html.parser import HTMLParser

from bs4 import BeautifulSoup, CData, NavigableString
from bs4.element import PreformattedString, Tag

# whitespace plus the invisible padding characters observed in marketing preheaders
_WHITESPACE_RUN = re.compile(r'[\s\u00ad\u034f\u200b\u200c\u200d\ufeff]+')
_LINE_END = re.compile(r'\r\n|\r|\n')
_NON_DISPLAY_TAGS = ('script', 'style')
_CELL_TAGS = ('td', 'th')
_BLOCK_TAGS = ('address', 'article', 'aside', 'blockquote', 'center', 'dd', 'details', 'div', 'dl',
               'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4',
               'h5', 'h6', 'header', 'hr', 'li', 'main', 'nav', 'ol', 'p', 'pre', 'section',
               'table', 'title', 'tr', 'ul')


class _LineBreak(NavigableString):
    """A marker placed in the parsed tree. It is not evidence text and is never emitted."""


def body_text_and_links(html_body):
    """The readable text of an HTML body plus the link targets it carries.

    Tags and the contents of closed style and script elements are dropped. A br or block element
    ends a line, table cells are separated by a space and text inside pre keeps its
    lines. Within a line, whitespace runs (including the zero-width padding marketing
    mail hides its preheader behind) collapse to one space. Each link's place in the
    text is marked [n], and the second value lists the targets by those numbers, as
    the parser returns them. A repeated target keeps its first number. A link with no words of its own,
    such as a linked image, still gets a marker, so the words just before a marker are
    not always the link's text."""
    if not html_body:
        return '', ''
    source = html_body.decode('utf-8', 'replace') if isinstance(html_body, bytes) else str(html_body)
    scan = HTMLParser()
    scan.feed(source)
    # A style or script left open holds the rest of the body. Closing it for the parse keeps
    # that text on Python versions that would otherwise drop it at the end of the input.
    open_element = scan.cdata_elem if scan.cdata_elem in _NON_DISPLAY_TAGS else None
    closer = f'</{open_element}>' if open_element else ''
    soup = BeautifulSoup(html_body + (closer.encode() if isinstance(html_body, bytes) else closer),
                         'html.parser')
    for name in _NON_DISPLAY_TAGS:
        found = soup.find_all(name)
        # The scan and the tree can disagree on malformed input, so the element may be absent.
        if name == open_element and found:
            found.pop()
        for hidden in found:
            hidden.extract()
    targets = []
    numbers = {}
    for anchor in soup.find_all('a', href=True):
        href = anchor.get('href')
        if not href:
            continue
        if href not in numbers:
            targets.append(href)
            numbers[href] = len(targets)
        anchor.append(NavigableString(f' [{numbers[href]}]'))
    for tag in soup.find_all(_BLOCK_TAGS):
        tag.insert(0, _LineBreak(''))
        tag.append(_LineBreak(''))
    for tag in soup.find_all(_CELL_TAGS):
        tag.append(NavigableString(' '))
    has_pre = soup.find('pre') is not None
    lines = [[]]
    for node in soup.descendants:
        if isinstance(node, _LineBreak):
            # A block edge ends a line that has text. It never makes a blank line by itself.
            if _WHITESPACE_RUN.sub('', ''.join(lines[-1])):
                lines.append([])
            else:
                lines[-1] = []
        elif isinstance(node, Tag) and node.name == 'br':
            lines.append([])
        elif isinstance(node, NavigableString) and (
                isinstance(node, CData) or not isinstance(node, PreformattedString)):
            if has_pre and node.find_parent('pre') is not None:
                first, *rest = _LINE_END.split(str(node))
                lines[-1].append(first)
                lines.extend([line] for line in rest)
            else:
                lines[-1].append(str(node))
    kept = []
    for line in lines:
        line = _WHITESPACE_RUN.sub(' ', ''.join(line)).strip()
        if line or (kept and kept[-1]):  # one blank line at most, none at the start
            kept.append(line)
    text = '\n'.join(kept).rstrip('\n')
    links = '\n'.join(f'[{number}] {target}' for number, target in enumerate(targets, 1))
    return text, links

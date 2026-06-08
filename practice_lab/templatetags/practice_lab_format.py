import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()


def _inline_format(text):
    safe_text = escape(text)
    safe_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe_text)
    safe_text = re.sub(r'`(.+?)`', r'<code>\1</code>', safe_text)
    return safe_text


@register.filter
def practice_markdown(value):
    """Render the small, safe Markdown subset used by Practice Lab."""
    lines = str(value or '').splitlines()
    output = []
    paragraph = []
    list_type = None

    def close_paragraph():
        if paragraph:
            output.append(f'<p>{"<br>".join(paragraph)}</p>')
            paragraph.clear()

    def close_list():
        nonlocal list_type
        if list_type:
            output.append(f'</{list_type}>')
            list_type = None

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            close_paragraph()
            close_list()
            continue

        heading = re.match(r'^(#{1,3})\s+(.+)$', line)
        bullet = re.match(r'^[-*]\s+(.+)$', line)
        numbered = re.match(r'^\d+[.)]\s+(.+)$', line)
        quote = re.match(r'^>\s?(.+)$', line)
        legacy_heading = line.endswith(':') and len(line) <= 100

        if heading:
            close_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(f'<h{level}>{_inline_format(heading.group(2))}</h{level}>')
        elif bullet or numbered:
            close_paragraph()
            wanted_type = 'ul' if bullet else 'ol'
            if list_type != wanted_type:
                close_list()
                output.append(f'<{wanted_type}>')
                list_type = wanted_type
            item = bullet.group(1) if bullet else numbered.group(1)
            output.append(f'<li>{_inline_format(item)}</li>')
        elif quote:
            close_paragraph()
            close_list()
            output.append(f'<blockquote>{_inline_format(quote.group(1))}</blockquote>')
        elif legacy_heading:
            close_paragraph()
            close_list()
            output.append(f'<h3>{_inline_format(line)}</h3>')
        else:
            close_list()
            paragraph.append(_inline_format(line))

    close_paragraph()
    close_list()
    return mark_safe(''.join(output))

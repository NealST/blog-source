#!/usr/bin/env python3
"""
md2wechat_formatter.py — Markdown → WeChat HTML 排版工具

产出 _preview.html，浏览器打开 → 全选复制 → 粘贴到公众号编辑器。

用法：
  python3 md2wechat_formatter.py article.md
  python3 md2wechat_formatter.py article.md --font-size medium
  python3 md2wechat_formatter.py article.md --indent
  python3 md2wechat_formatter.py article.md -o output.html
"""

import argparse
import html as html_module
import os
import re
import sys

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from pygments import highlight as pyg_highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False

try:
    from premailer import transform as premailer_transform
    HAS_PREMAILER = True
except ImportError:
    HAS_PREMAILER = False

# ─── Theme ───
# 墨筝（mozheng）统一主题 — 融合 mozheng 品牌色 + medium 排版精华
# 墨（近黑微暖 #1C1C1E）+ 筝（古筝丝弦哑光金 #C4956A）+ 宣纸底 #F2EDE3

THEME = {
    'bg':               '#F2EDE3',
    'text':             '#333333',
    'heading':          '#1C1C1E',
    'accent':           '#C4956A',
    'link':             '#C4956A',
    'mark_bg':          'rgba(196,149,106,0.28)',
    'code_bg':          '#f0ece4',
    'code_border':      '#ddd8ce',
    'code_text':        '#1C1C1E',
    'pre_bg':           '#1C1C1E',
    'pre_border':       'rgba(196,149,106,0.15)',
    'pre_text':         '#F2EDE3',
    'syntax': {
        'keyword':  '#C4956A',   # 筝弦金 — 关键字
        'string':   '#A8C97F',   # 苔绿 — 字符串
        'comment':  '#7A7876',   # 淡墨 — 注释
        'number':   '#D4A76A',   # 暖金 — 数字
        'func':     '#8FBCBB',   # 青瓷 — 函数名
        'type':     '#B48EAD',   # 藤紫 — 类型
        'operator': '#9A8A7B',   # 淡棕 — 操作符
    },
    'blockquote_border':'#C4956A',     # 已弃用：金色左竖线与 H2 装饰冲突，保留供向后兼容
    'blockquote_border_soft':'#e8dfd0', # 方案 B：浅米色四面边框，让卡片做"安静的信息容器"
    'strong':           '#1C1C1E',
    'blockquote_bg':    '#f5efe4',
    'table_header_bg':  '#1C1C1E',
    'table_header_text':'#F2EDE3',
    'table_stripe':     '#f0ece4',
    'table_border':     '#d5d0c6',
    'hr_color':         '#C4956A',
}

FONT_SIZES = {
    'small':  '14px',
    'medium': '15px',
    'large':  '16px',
}

# ─── CSS Builder ───

def _hex_tint(hex_color, factor=0.7):
    """Blend a hex color toward white by `factor` (0=original, 1=white)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r2 = int(r + (255 - r) * factor)
    g2 = int(g + (255 - g) * factor)
    b2 = int(b + (255 - b) * factor)
    return f'#{r2:02x}{g2:02x}{b2:02x}'


def build_css(font_size_name='large', indent=False):
    t = THEME
    fs = FONT_SIZES[font_size_name]
    lh = '1.8' if font_size_name == 'large' else '1.75'
    body_font = "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'PingFang HK', 'Noto Sans SC', 'Microsoft YaHei', 'Helvetica Neue', 'Apple Color Emoji', 'Segoe UI Emoji', sans-serif"
    heading_font = body_font

    css = f"""
/* md2wechat_formatter — mozheng unified theme */
* {{ margin: 0; padding: 0; }}
body {{
  background: {t['bg']};
  padding: 0;
  margin: 0;
}}
.tip {{
  background: #eee;
  padding: 10px;
  text-align: center;
  font-size: 13px;
  color: #999;
  margin-bottom: 0;
  font-family: -apple-system, 'PingFang SC', sans-serif;
}}
.content {{
  max-width: 680px;
  margin: 0 auto;
  padding: 24px 16px 40px;
  background-color: {t['bg']};
  font-family: {body_font};
  font-size: {fs};
  line-height: {lh};
  color: {t['text']};
  word-wrap: break-word;
  overflow-wrap: break-word;
  letter-spacing: 0.3px;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}}
.content h1 {{
  font-size: 24px;
  font-weight: 800;
  color: {t['heading']};
  font-family: {heading_font};
  margin: 40px 0 16px;
  padding: 10px 0;
  border-top: 2px solid {t['heading']};
  border-bottom: 2px solid {t['heading']};
  text-align: center;
  letter-spacing: 1px;
  line-height: 1.3;
}}
.content h2 {{
  font-size: 20px;
  font-weight: 700;
  color: {t['heading']};
  font-family: {heading_font};
  margin: 38px 0 14px;
  padding-bottom: 0;
  border-bottom: none;
  border-left: 4px solid {t['accent']};
  padding-left: 12px;
  letter-spacing: 0.3px;
  line-height: 1.35;
}}
.content h3 {{
  font-size: 17px;
  font-weight: 700;
  color: {t['heading']};
  font-family: {heading_font};
  margin: 24px 0 10px;
  line-height: 1.3;
}}
.content h4, .content h5, .content h6 {{
  font-size: {fs};
  font-weight: 700;
  color: {t['heading']};
  font-family: {heading_font};
  margin: 20px 0 8px;
  letter-spacing: 0.5px;
}}
.content p {{
  margin: 0 0 15px;
  text-align: left;
  word-break: break-word;{f"{chr(10)}  text-indent: 2em;" if indent else ""}
}}
.content a {{
  color: {t['link']};
  text-decoration: none;
  border-bottom: 1px solid {t['link']};
  word-break: break-all;
}}
.content mark {{
  background: {t['mark_bg']};
  color: inherit;
  padding: 0 2px;
}}
.content strong {{
  color: {t['strong']};
  font-weight: 700;
}}
.content em {{
  font-style: italic;
}}
.content del {{
  text-decoration: line-through;
  color: #999;
}}
.content code {{
  font-family: 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace;
  font-size: 0.88em;
  background: {t['code_bg']};
  border: 1px solid {t['code_border']};
  border-radius: 3px;
  padding: 2px 5px;
  color: {t['code_text']};
  word-break: break-word;
}}
.code-wrap {{
  margin: 16px 0;
  border-radius: 6px;
  overflow: hidden;
  border: none;
  background: {t['pre_bg']};
}}
.code-badge {{
  display: block;
  background: #2C2A28;
  color: {t['accent']};
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 11px;
  font-weight: 600;
  padding: 6px 14px;
  letter-spacing: 1px;
  text-transform: uppercase;
  border-bottom: 1px solid #3D3632;
}}
.content pre {{
  background: {t['pre_bg']};
  border: 1px solid {t['pre_border']};
  border-radius: 6px;
  padding: 14px 16px;
  overflow-x: auto;
  margin: 16px 0;
  -webkit-overflow-scrolling: touch;
  white-space: pre-wrap;
  word-break: break-word;
}}
.code-wrap pre {{
  background: {t['pre_bg']};
  border: none;
  border-radius: 0;
  padding: 14px 16px;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
}}
.content pre code,
.code-wrap pre code {{
  background: none;
  border: none;
  padding: 0;
  border-radius: 0;
  font-size: 14px;
  line-height: 1.6;
  color: {t['pre_text']};
  word-break: break-word;
}}
.content blockquote {{
  /* 方案 B：四面浅边框 + 圆角卡片，避免与 H2 的金色左竖线视觉冲突 */
  margin: 16px 0 20px;
  padding: 14px 18px;
  border: 1px solid {t['blockquote_border_soft']};
  background: {t['blockquote_bg']};
  color: #666;
  border-radius: 6px;
}}
.content blockquote p {{
  margin: 0;
}}
.content blockquote p + p {{
  margin-top: 8px;
}}
.content blockquote cite {{
  display: block;
  margin-top: 12px;
  font-style: normal;
  font-size: 13px;
  color: #999;
  letter-spacing: 0.3px;
}}
.content ul, .content ol {{
  margin: 0 0 16px;
  padding-left: 24px;
}}
.content li {{
  margin-bottom: 6px;
}}
.content li > ul, .content li > ol {{
  margin: 4px 0 4px;
  padding-left: 20px;
}}
.content ul ul {{
  list-style-type: circle;
}}
.content ul ul ul {{
  list-style-type: square;
}}
.content li p {{
  margin: 0;
}}
.content table {{
  width: 100%;
  border-collapse: collapse;
  margin: 0 0 24px;
  font-size: 15px;
  table-layout: auto;
}}
.content thead th {{
  background: {t['table_header_bg']};
  color: {t['table_header_text']};
  font-weight: 600;
  padding: 10px 12px;
  text-align: left;
  border: 1px solid {t['table_border']};
}}
.content tbody td {{
  padding: 10px 12px;
  border: 1px solid {t['table_border']};
  vertical-align: top;
}}
.content tbody tr:nth-child(even) td {{
  background: {t['table_stripe']};
}}
.content hr {{
  border: none;
  height: auto;
  background: transparent;
  margin: 40px 0;
  text-align: center;
  color: {t['accent']};
  font-size: 16px;
  letter-spacing: 14px;
  line-height: 1;
  opacity: 0.5;
}}
.content h2 + p {{
  margin-top: 4px;
}}
.content h3 + p {{
  margin-top: 2px;
}}
.content figure {{
  margin: 20px 0;
  text-align: center;
}}
.content figure img {{
  margin: 0 auto;
}}
.content figcaption {{
  margin-top: 8px;
  font-size: 14px;
  color: #999;
  line-height: 1.5;
  letter-spacing: 0.2px;
}}
.content img {{
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 8px 0;
}}
.admonition {{
  margin: 16px 0 20px;
  padding: 14px 18px;
  border-radius: 6px;
  font-size: 15px;
  line-height: 1.7;
}}
.admonition .admonition-title {{
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 6px;
}}
.admonition p {{
  margin: 0 0 6px;
}}
.admonition p:last-child {{
  margin-bottom: 0;
}}
.admonition-tip {{
  border-left: 4px solid #A8C97F;
  background: #f4f8ef;
}}
.admonition-tip .admonition-title {{
  color: #5a7a3a;
}}
.admonition-warning {{
  border-left: 4px solid #D4A76A;
  background: #fdf6ee;
}}
.admonition-warning .admonition-title {{
  color: #8a6a30;
}}
.admonition-note {{
  border-left: 4px solid #8FBCBB;
  background: #f0f6f6;
}}
.admonition-note .admonition-title {{
  color: #4a7a7a;
}}
.admonition-info {{
  border-left: 4px solid #B48EAD;
  background: #f6f0f4;
}}
.admonition-info .admonition-title {{
  color: #7a5a72;
}}
"""
    return css

# ─── Syntax Highlighting ───

def build_pygments_style(theme):
    """Build a Pygments-compatible inline-style formatter from theme syntax colors."""
    if not HAS_PYGMENTS or 'syntax' not in theme:
        return None
    s = theme['syntax']
    # Map Pygments token types → inline CSS colors
    # We build a custom style dict for InlineHtmlFormatter
    style_map = {
        'Keyword':            s['keyword'],
        'Keyword.Constant':   s['keyword'],
        'Keyword.Declaration':s['keyword'],
        'Keyword.Namespace':  s['keyword'],
        'Keyword.Type':       s['type'],
        'Name.Builtin':       s['func'],
        'Name.Function':      s['func'],
        'Name.Function.Magic':s['func'],
        'Name.Class':         s['type'],
        'Name.Decorator':     s['func'],
        'Literal.String':     s['string'],
        'Literal.String.Backtick': s['string'],
        'Literal.String.Double': s['string'],
        'Literal.String.Single': s['string'],
        'Literal.String.Escape': s['number'],
        'Literal.Number':     s['number'],
        'Literal.Number.Integer': s['number'],
        'Literal.Number.Float': s['number'],
        'Comment':            s['comment'],
        'Comment.Single':     s['comment'],
        'Comment.Multiline':  s['comment'],
        'Comment.Hashbang':   s['comment'],
        'Operator':           s['operator'],
        'Operator.Word':      s['keyword'],
        'Punctuation':        s.get('operator', '#9A8A7B'),
    }
    return style_map


def highlight_code(code_text, lang, theme):
    """Syntax-highlight code using Pygments, returning inline-styled HTML."""
    if not HAS_PYGMENTS or 'syntax' not in theme:
        return html_module.escape(code_text)

    style_map = build_pygments_style(theme)
    try:
        lexer = get_lexer_by_name(lang) if lang else guess_lexer(code_text)
    except Exception:
        lexer = TextLexer()

    # Use Pygments to tokenize, then manually build inline-styled spans
    from pygments import lex
    result = []
    for token_type, token_value in lex(code_text, lexer):
        escaped = html_module.escape(token_value)
        # Walk up the token type hierarchy to find a matching style
        color = None
        tt = token_type
        while tt:
            key = str(tt)
            if key.startswith('Token.'):
                key = key[6:]  # strip 'Token.' prefix
            if key in style_map:
                color = style_map[key]
                break
            tt = tt.parent
        if color:
            result.append(f'<span style="color:{color}">{escaped}</span>')
        else:
            result.append(escaped)
    return ''.join(result)


# ─── Markdown Conversion ───

def strip_frontmatter(text):
    """Remove YAML frontmatter (--- ... ---)."""
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            return text[end + 3:].lstrip('\n')
    return text


def calculate_reading_time(text):
    """Estimate reading time in minutes from markdown text."""
    clean = re.sub(r'```[\s\S]*?```', '', text)
    chinese_chars = len(re.findall(r'[一-鿿]', clean))
    english_words = len(re.findall(r'[a-zA-Z]+', clean))
    minutes = chinese_chars / 400 + english_words / 200
    return max(1, round(minutes))


def _ensure_blank_line_before_list(text):
    """Insert a blank line before list markers that follow paragraph text.

    Python's markdown library requires a blank line before a list block to
    recognise it as a list. Without the blank line, `* item` after a paragraph
    is treated as continuation text (rendered as raw `*` inside <p>).
    """
    lines = text.split('\n')
    result = []
    in_fenced_code = False
    list_marker_re = re.compile(r'^(\s*)([-*+]|\d+\.)\s+')

    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r'^`{3,}', stripped):
            in_fenced_code = not in_fenced_code
            result.append(line)
            continue
        if in_fenced_code:
            result.append(line)
            continue

        if list_marker_re.match(line) and i > 0:
            # Look back for the nearest non-blank line
            prev_idx = i - 1
            while prev_idx >= 0 and lines[prev_idx].strip() == '':
                prev_idx -= 1
            if prev_idx >= 0:
                prev_line = lines[prev_idx]
                prev_stripped = prev_line.strip()
                # If previous non-blank line is NOT a list marker and NOT a
                # heading, insert blank line so markdown sees a new list block
                if (not list_marker_re.match(prev_line)
                        and not prev_stripped.startswith('#')
                        and not re.match(r'^`{3,}', prev_stripped)
                        and lines[i - 1].strip() != ''):
                    result.append('')
        result.append(line)

    return '\n'.join(result)


def _normalize_list_indent(text):
    """Normalize list indentation so Python markdown lib produces proper nesting.

    The `markdown` library requires 4-space indent per nesting level, but most
    writers use 2- or 3-space indent (GFM style). This preprocessor detects the
    smallest indent unit used in list blocks and re-maps all indentation to
    4-space multiples.
    """
    lines = text.split('\n')
    result = []
    in_fenced_code = False

    for line in lines:
        # Don't touch fenced code blocks
        if re.match(r'^`{3,}', line.strip()):
            in_fenced_code = not in_fenced_code
            result.append(line)
            continue
        if in_fenced_code:
            result.append(line)
            continue

        # Match indented list items: leading spaces + list marker (*, -, +, 1.)
        m = re.match(r'^(\s+)([-*+]|\d+\.)\s+(.*)', line)
        if m:
            indent = len(m.group(1))
            marker = m.group(2)
            content = m.group(3)
            # Detect indent unit: treat 2, 3, or 4 spaces as 1 nesting level
            if indent <= 4:
                level = 1
            else:
                # For deeper nesting, estimate level from smallest plausible unit
                unit = 2 if indent % 2 == 0 else 3
                level = max(1, indent // unit)
            new_indent = '    ' * level  # 4 spaces per level
            result.append(f'{new_indent}{marker} {content}')
        else:
            result.append(line)

    return '\n'.join(result)


ADMONITION_LABELS = {
    'tip': '💡 提示',
    'warning': '⚠️ 注意',
    'note': '📝 备注',
    'info': 'ℹ️ 信息',
}


def _convert_admonitions(md_text):
    """Convert :::type ... ::: blocks to HTML admonition divs before markdown parsing."""
    lines = md_text.split('\n')
    result = []
    i = 0
    in_fenced_code = False

    while i < len(lines):
        stripped = lines[i].strip()
        if re.match(r'^`{3,}', stripped):
            in_fenced_code = not in_fenced_code
            result.append(lines[i])
            i += 1
            continue
        if in_fenced_code:
            result.append(lines[i])
            i += 1
            continue

        adm_match = re.match(r'^:::\s*(tip|warning|note|info)\s*(.*)?$', stripped, re.IGNORECASE)
        if adm_match:
            adm_type = adm_match.group(1).lower()
            custom_title = (adm_match.group(2) or '').strip()
            title = custom_title if custom_title else ADMONITION_LABELS.get(adm_type, adm_type)
            i += 1
            body_lines = []
            while i < len(lines) and lines[i].strip() != ':::':
                body_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip closing :::
            body_text = '\n'.join(body_lines).strip()
            body_html = '<br>'.join(
                inline_format(l) if l.strip() else '' for l in body_text.split('\n')
            )
            result.append(
                f'<div class="admonition admonition-{adm_type}">'
                f'<div class="admonition-title">{title}</div>'
                f'<p>{body_html}</p>'
                f'</div>'
            )
            continue

        result.append(lines[i])
        i += 1

    return '\n'.join(result)


def convert_with_markdown_lib(md_text, theme=None):
    """Convert using the `markdown` Python package."""
    md_text = _convert_admonitions(md_text)
    md_text = _ensure_blank_line_before_list(md_text)
    md_text = _normalize_list_indent(md_text)
    extensions = [
        'tables',
        'fenced_code',
        'sane_lists',
        'smarty',
    ]
    html_out = md_lib.markdown(md_text, extensions=extensions)
    # Post-process: apply Pygments syntax highlighting to <pre><code> blocks
    if theme and HAS_PYGMENTS and 'syntax' in theme:
        def _highlight_block(m):
            cls = m.group(1) or ''
            code_html = m.group(2)
            # Extract language from class="language-xxx"
            lang_match = re.search(r'language-(\w+)', cls)
            lang = lang_match.group(1) if lang_match else ''
            # Decode HTML entities back to raw text for Pygments
            raw = html_module.unescape(code_html)
            highlighted = highlight_code(raw, lang, theme)
            cls_attr = f' class="language-{lang}"' if lang else ''
            return f'<pre><code{cls_attr}>{highlighted}</code></pre>'
        html_out = re.sub(
            r'<pre><code(?:\s+class="([^"]*)")?>(.*?)</code></pre>',
            _highlight_block,
            html_out,
            flags=re.DOTALL,
        )
    return html_out


def inline_format(text):
    """Process inline Markdown: bold, italic, code, links, images, highlight."""
    # Images (before links to avoid conflict)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Bold (** or __)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    # Strikethrough (~~text~~) → <del>
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    # Highlight (==text==) — Markdown extra syntax → <mark>
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)
    # Italic (* or _) — but not inside words with underscores
    text = re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'<em>\1</em>', text)
    # Inline code (must come after bold/italic to avoid conflicts inside code)
    text = re.sub(r'`([^`]+?)`', lambda m: '<code>' + html_module.escape(m.group(1)) + '</code>', text)
    return text


def convert_basic(text, theme=None):
    """Fallback Markdown→HTML using regex. Handles the features used in the article."""
    text = _convert_admonitions(text)
    lines = text.split('\n')
    out = []
    i = 0
    n = len(lines)

    def flush_paragraph(buf):
        if buf:
            out.append('<p>' + inline_format(' '.join(buf)) + '</p>')
        return []

    para_buf = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # ── Fenced code block ──
        code_match = re.match(r'^```(\w*)', stripped)
        if code_match:
            para_buf = flush_paragraph(para_buf)
            lang = code_match.group(1)
            i += 1
            code_lines = []
            while i < n and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1  # skip closing ```
            code_raw = '\n'.join(code_lines)
            highlighted = highlight_code(code_raw, lang, theme) if theme else html_module.escape(code_raw)
            out.append(f'<pre><code>{highlighted}</code></pre>')
            continue

        # ── Table ──
        if '|' in stripped and stripped.startswith('|') and stripped.endswith('|'):
            para_buf = flush_paragraph(para_buf)
            table_lines = []
            while i < n and '|' in lines[i].strip() and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            out.append(parse_table(table_lines))
            continue

        # ── Heading ──
        h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        if h_match:
            para_buf = flush_paragraph(para_buf)
            level = len(h_match.group(1))
            text_content = inline_format(h_match.group(2))
            out.append(f'<h{level}>{text_content}</h{level}>')
            i += 1
            continue

        # ── Horizontal rule ──
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            para_buf = flush_paragraph(para_buf)
            out.append('<hr />')
            i += 1
            continue

        # ── Blockquote ──
        if stripped.startswith('>'):
            para_buf = flush_paragraph(para_buf)
            bq_lines = []
            while i < n and lines[i].strip().startswith('>'):
                bq_lines.append(lines[i].strip()[1:].strip())
                i += 1
            bq_html = '<br/>'.join(inline_format(l) for l in bq_lines if l)
            out.append(f'<blockquote><p>{bq_html}</p></blockquote>')
            continue

        # ── Unordered list ──
        ul_match = re.match(r'^[-*+]\s+(.+)$', stripped)
        if ul_match:
            para_buf = flush_paragraph(para_buf)
            items = []
            while i < n:
                m = re.match(r'^[-*+]\s+(.+)$', lines[i].strip())
                if m:
                    items.append(inline_format(m.group(1)))
                    i += 1
                elif lines[i].strip() == '':
                    # Check if next non-empty line is still a list item
                    j = i + 1
                    while j < n and lines[j].strip() == '':
                        j += 1
                    if j < n and re.match(r'^[-*+]\s+', lines[j].strip()):
                        i = j
                        continue
                    break
                else:
                    break
            items_html = ''.join(f'<li>{item}</li>' for item in items)
            out.append(f'<ul>{items_html}</ul>')
            continue

        # ── Ordered list ──
        ol_match = re.match(r'^\d+\.\s+(.+)$', stripped)
        if ol_match:
            para_buf = flush_paragraph(para_buf)
            items = []
            while i < n:
                m = re.match(r'^\d+\.\s+(.+)$', lines[i].strip())
                if m:
                    items.append(inline_format(m.group(1)))
                    i += 1
                elif lines[i].strip() == '':
                    j = i + 1
                    while j < n and lines[j].strip() == '':
                        j += 1
                    if j < n and re.match(r'^\d+\.', lines[j].strip()):
                        i = j
                        continue
                    break
                else:
                    break
            items_html = ''.join(f'<li>{item}</li>' for item in items)
            out.append(f'<ol>{items_html}</ol>')
            continue

        # ── Empty line ──
        if stripped == '':
            para_buf = flush_paragraph(para_buf)
            i += 1
            continue

        # ── Regular paragraph text ──
        para_buf.append(stripped)
        i += 1

    flush_paragraph(para_buf)
    return '\n'.join(out)


def parse_table(lines):
    """Parse Markdown table lines into HTML."""
    if len(lines) < 2:
        return ''

    def split_cells(row):
        cells = row.split('|')
        if cells and cells[0].strip() == '':
            cells = cells[1:]
        if cells and cells[-1].strip() == '':
            cells = cells[:-1]
        return [c.strip() for c in cells]

    def parse_alignments(sep_line):
        """Extract column alignments from separator row like |:---|:---:|---:|."""
        cols = split_cells(sep_line)
        aligns = []
        for col in cols:
            col = col.strip()
            left = col.startswith(':')
            right = col.endswith(':')
            if left and right:
                aligns.append('center')
            elif right:
                aligns.append('right')
            else:
                aligns.append('left')
        return aligns

    header_cells = split_cells(lines[0])

    sep_idx = 1
    alignments = []
    if sep_idx < len(lines) and re.match(r'^[\s|:-]+$', lines[sep_idx]):
        alignments = parse_alignments(lines[sep_idx])
        data_start = sep_idx + 1
    else:
        data_start = sep_idx

    def align_attr(col_idx):
        if col_idx < len(alignments) and alignments[col_idx] != 'left':
            return f' style="text-align:{alignments[col_idx]}"'
        return ''

    html = '<table><thead><tr>'
    for idx, cell in enumerate(header_cells):
        html += f'<th{align_attr(idx)}>{inline_format(cell)}</th>'
    html += '</tr></thead><tbody>'

    for row_line in lines[data_start:]:
        cells = split_cells(row_line)
        html += '<tr>'
        for idx, cell in enumerate(cells):
            html += f'<td{align_attr(idx)}>{inline_format(cell)}</td>'
        html += '</tr>'

    html += '</tbody></table>'
    return html


def convert_md_to_html(md_text, theme=None):
    """Convert Markdown to HTML using best available method."""
    if HAS_MARKDOWN:
        return convert_with_markdown_lib(md_text, theme)
    return convert_basic(md_text, theme)


# ─── Content Post-processing ───

def _slugify(text):
    """Generate a stable anchor id from heading text."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text).strip()
    text = re.sub(r'\s+', '-', text)
    return text.lower()[:60] or 'section'


def wrap_code_with_badge(html):
    """Wrap <pre><code class="language-X"> with code-wrap + language badge."""
    def _wrap(m):
        full_pre = m.group(0)
        lang_match = re.search(r'class="(?:[^"]*?)language-(\w+)', full_pre)
        if not lang_match:
            return full_pre
        lang = lang_match.group(1)
        return (
            f'<section class="code-wrap">'
            f'<section class="code-badge">{lang}</section>'
            f'{full_pre}'
            f'</section>'
        )
    return re.sub(r'<pre><code\s+class="[^"]+">[\s\S]*?</code></pre>', _wrap, html)


def split_inline_images(html):
    """Split <p>text<img/></p> into <p>text</p><figure><img/></figure>.

    When an image follows text within the same paragraph (no blank line
    separating them in Markdown), the parser merges them. This splitter
    extracts trailing images into standalone <figure> blocks for cleaner
    visual flow on mobile.
    """
    def _split(m):
        full = m.group(0)
        # Match: <p ...>text_before<img ...>optional_tail</p>
        inner_re = re.compile(
            r'^(<p[^>]*>)(.*?)(<img[^>]*/?>)\s*</p>$', re.DOTALL
        )
        im = inner_re.match(full)
        if not im:
            return full
        p_open, text_before, img_tag = im.group(1), im.group(2), im.group(3)
        text_before = text_before.strip()
        if not text_before:
            # Image alone in <p> — leave for wrap_image_caption
            return full
        return f'{p_open}{text_before}</p>\n<figure>{img_tag}</figure>'

    return re.sub(r'<p[^>]*>(?:(?!</p>).)*<img[^>]*/?>(?:(?!</p>).)*</p>', _split, html, flags=re.DOTALL)


def wrap_image_caption(html):
    """Convert <p><img alt="X" /></p> into <figure><img/><figcaption>X</figcaption></figure>.

    Caption only rendered when alt text is non-empty.
    """
    def _wrap(m):
        alt = m.group('alt').strip()
        img = m.group('img')
        if not alt:
            return f'<figure>{img}</figure>'
        return f'<figure>{img}<figcaption>{alt}</figcaption></figure>'
    return re.sub(
        r'<p>\s*(?P<img><img[^>]*alt="(?P<alt>[^"]*)"[^>]*/?>)\s*</p>',
        _wrap,
        html,
    )


def wrap_blockquote_cite(html):
    """If a blockquote ends with a paragraph starting with — or --, wrap as <cite>."""
    def _wrap(m):
        body = m.group(1)
        # Check the trailing <p>...</p> for cite marker
        cite_re = re.compile(r'(.*)<p>\s*([—\-]{1,2}\s+[^<]+)</p>\s*$', re.DOTALL)
        cm = cite_re.match(body)
        if not cm:
            return m.group(0)
        head, cite_text = cm.group(1), cm.group(2)
        return f'<blockquote>{head}<cite>{cite_text}</cite></blockquote>'
    return re.sub(r'<blockquote>([\s\S]*?)</blockquote>', _wrap, html)


def add_heading_decorations(html, theme):
    """No-op: h2 decoration now uses border-left in CSS (inline-block spans get stripped by WeChat)."""
    return html


def add_blockquote_decoration(html, theme):
    """Inject a large decorative quote mark at the top of blockquotes."""
    if not theme:
        return html
    accent = theme['accent']
    quote_span = (
        f'<span style="display:block;font-size:32px;line-height:1;'
        f"font-family:Georgia,'Times New Roman',serif;"
        f'color:{accent};opacity:0.5;margin-bottom:4px;">'
        '\u201c</span>'
    )
    html = re.sub(
        r'<blockquote([^>]*)>\s*<p',
        lambda m: f'<blockquote{m.group(1)}>{quote_span}<p',
        html,
    )
    return html


def convert_strikethrough(html):
    """Convert ~~text~~ to <del> for libraries that don't support strikethrough."""
    return re.sub(r'~~(.+?)~~', r'<del>\1</del>', html)


def convert_mark_to_span(html, theme):
    """Convert <mark> and raw ==text== to <span> with inline styles for WeChat compatibility.

    The python-markdown library doesn't support ==highlight== syntax,
    so raw ==text== may appear as literal text in the HTML output.
    """
    mark_bg = '#e5d4c1'
    if theme:
        raw_bg = theme.get('mark_bg', 'rgba(196,149,106,0.28)')
        if raw_bg.startswith('rgba'):
            mark_bg = _rgba_to_hex(raw_bg)
        else:
            mark_bg = raw_bg
    styled = (
        f'<span style="background:{mark_bg};'
        f'color:inherit;padding:2px 4px;">'
    )
    html = re.sub(
        r'<mark>(.*?)</mark>',
        lambda m: f'{styled}{m.group(1)}</span>',
        html,
    )
    html = re.sub(
        r'(?<!=)==(?!=)(.+?)(?<!=)==(?!=)',
        lambda m: f'{styled}{m.group(1)}</span>',
        html,
    )
    return html


def add_reading_time(html, minutes, theme):
    """Insert a reading time indicator after the first H1 heading."""
    indicator = (
        '<p style="text-align:left;font-size:13px;color:#999;'
        f'margin:4px 0 28px;letter-spacing:1px;line-height:1;">'
        f'\u23f1 \u9884\u8ba1\u9605\u8bfb {minutes} \u5206\u949f</p>'
    )
    if '</h1>' in html:
        return html.replace('</h1>', '</h1>\n' + indicator, 1)
    return indicator + '\n' + html


def add_follow_prompt(html, theme):
    """Append a follow/subscribe prompt at the end of the article."""
    accent = '#C4956A'
    if theme:
        accent = theme.get('accent', accent)
    prompt_html = (
        f'<section style="margin:36px auto 0;max-width:320px;padding:16px 24px;'
        f'text-align:center;border:1px solid #e8dfd0;border-radius:8px;'
        f'background:#f5efe4;">'
        f'<p style="margin:0 0 4px;font-size:14px;color:#1C1C1E;'
        f'font-weight:600;letter-spacing:1px;text-align:center;">'
        f'\u5173\u6ce8\u516c\u4f17\u53f7\u300c<span style="color:{accent};">'
        f'\u58a8\u7b5d</span>\u300d</p>'
        f'<p style="margin:0;font-size:12px;color:#999;'
        f'letter-spacing:0.5px;text-align:center;">'
        f'\u7b2c\u4e00\u65f6\u95f4\u83b7\u53d6\u6df1\u5ea6\u79d1\u6280\u5185\u5bb9</p>'
        f'</section>'
    )
    return html + '\n' + prompt_html


def add_end_mark(html, theme):
    """Append a centered END mark at the bottom of the article."""
    accent = '#C4956A'
    if theme:
        accent = theme.get('accent', accent)
    end_html = (
        f'<p style="text-align:center;color:{accent};font-size:13px;'
        f'margin:40px 0 0;letter-spacing:3px;opacity:0.6;">'
        '\u2014 END \u2014</p>'
    )
    return html + '\n' + end_html


def convert_task_list(html):
    """Convert [ ] and [x] at the start of <li> content to Unicode checkboxes."""
    html = re.sub(
        r'(<li[^>]*>)\s*\[ \]\s*',
        r'\1<span style="margin-right:4px;">☐</span> ',
        html,
    )
    html = re.sub(
        r'(<li[^>]*>)\s*\[x\]\s*',
        r'\1<span style="margin-right:4px;color:#C4956A;">☑</span> ',
        html,
        flags=re.IGNORECASE,
    )
    return html


def postprocess_content(html, theme=None, reading_minutes=None):
    """Run all content-level post-processing steps in the right order."""
    html = wrap_code_with_badge(html)
    html = convert_task_list(html)
    html = split_inline_images(html)
    html = wrap_image_caption(html)
    html = wrap_blockquote_cite(html)
    html = add_blockquote_decoration(html, theme)
    html = convert_strikethrough(html)
    html = convert_mark_to_span(html, theme)
    html = add_heading_decorations(html, theme)
    accent = theme['accent'] if theme else '#C4956A'
    dots_html = (
        f'<p style="text-align:center;color:{accent};'
        f'font-size:18px;letter-spacing:18px;line-height:1;'
        f'margin:24px 0;opacity:0.55;">'
        '\u00b7\u00a0\u00b7\u00a0\u00b7</p>'
    )
    html = re.sub(r'<hr\s*/?\s*>', dots_html, html)
    if reading_minutes is not None:
        html = add_reading_time(html, reading_minutes, theme)
    html = add_follow_prompt(html, theme)
    html = add_end_mark(html, theme)
    return html


# ─── WeChat Sanitizer ───

def _rgba_to_hex(rgba_str, bg_hex='#F2EDE3'):
    """Convert rgba(r,g,b,a) to hex with opacity baked into the given background color."""
    m = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)', rgba_str)
    if not m:
        return rgba_str
    r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
    a = float(m.group(4)) if m.group(4) else 1.0
    bg = bg_hex.lstrip('#')
    bg_r, bg_g, bg_b = int(bg[0:2], 16), int(bg[2:4], 16), int(bg[4:6], 16)
    r2 = int(r * a + bg_r * (1 - a))
    g2 = int(g * a + bg_g * (1 - a))
    b2 = int(b * a + bg_b * (1 - a))
    return f'#{r2:02x}{g2:02x}{b2:02x}'


def sanitize_for_wechat(html_str, theme=None):
    """Post-process inlined HTML to survive WeChat editor re-parsing.

    WeChat editor quirks:
    - Strips <style> blocks entirely
    - Strips styles on <div> (must use <section>)
    - Strips styles on <blockquote> (must use <section>)
    - Removes overflow-x, -webkit-*, word-wrap, overflow-wrap
    - Doesn't understand rgba() — convert to hex
    - :nth-child cannot be inlined — apply stripe bg directly to even <tr> rows
    """
    result = html_str

    # 1. Remove residual <style> blocks (premailer may leave pseudo-selectors)
    result = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', result)

    # 2. Replace <div> with <section> (WeChat preserves styles on <section>)
    result = result.replace('<div ', '<section ')
    result = result.replace('<div>', '<section>')
    result = result.replace('</div>', '</section>')

    # 2.5. Replace <blockquote> with <section> (WeChat strips styles on blockquote)
    result = re.sub(r'<blockquote([^>]*)>', r'<section\1>', result)
    result = result.replace('</blockquote>', '</section>')

    # 3. Strip CSS properties WeChat editor doesn't support
    unsupported_props = [
        r'overflow-x\s*:\s*[^;"\']+;?\s*',
        r'-webkit-overflow-scrolling\s*:\s*[^;"\']+;?\s*',
        r'overflow-wrap\s*:\s*[^;"\']+;?\s*',
        r'word-wrap\s*:\s*[^;"\']+;?\s*',
        r'table-layout\s*:\s*[^;"\']+;?\s*',
        r'border-collapse\s*:\s*[^;"\']+;?\s*',
    ]
    for prop_re in unsupported_props:
        result = re.sub(prop_re, '', result)

    # 4. Convert rgba() values to hex inside style attributes
    def replace_rgba_in_style(m):
        return _rgba_to_hex(m.group(0))
    result = re.sub(r'rgba?\([^)]+\)', replace_rgba_in_style, result)

    # 5. Inline table stripe background to even rows
    # After premailer, even-row <td> may still lack background.
    # Find all <tbody> blocks and add bg to even <tr>'s <td> elements.
    if theme:
        stripe_bg = theme.get('table_stripe', '#f0ece4')

        def add_stripe_to_tbody(tbody_match):
            tbody_html = tbody_match.group(0)
            row_index = [0]

            def process_tr(tr_match):
                row_index[0] += 1
                tr_html = tr_match.group(0)
                if row_index[0] % 2 == 0:
                    # Add background to each <td> in this even row
                    def add_bg_to_td(td_match):
                        tag = td_match.group(0)
                        if 'background' in tag:
                            return tag  # already has bg
                        if 'style="' in tag:
                            return tag.replace('style="', f'style="background:{stripe_bg}; ')
                        return tag.replace('<td', f'<td style="background:{stripe_bg}"', 1)
                    tr_html = re.sub(r'<td[^>]*>', add_bg_to_td, tr_html)
                return tr_html

            return re.sub(r'<tr[\s\S]*?</tr>', process_tr, tbody_html)

        result = re.sub(r'<tbody[\s\S]*?</tbody>', add_stripe_to_tbody, result)

    # 6. Fix strong tag colors — enforce #1C1C1E and font-weight:700
    # Catch ANY non-standard color on <strong>, not just #C4956A
    def fix_strong_style(m):
        tag = m.group(0)
        tag = re.sub(r'color\s*:\s*(?!#1C1C1E)#[0-9a-fA-F]{6}', 'color:#1C1C1E', tag)
        tag = re.sub(r'font-weight\s*:\s*(?!700)\d+', 'font-weight:700', tag)
        return tag
    result = re.sub(r'<strong[^>]*style="[^"]*"[^>]*>', fix_strong_style, result)

    # 7. Clean up empty style attributes
    result = re.sub(r'\s*style="\s*"', '', result)

    return result


# ─── HTML Assembly ───

def build_html(content_html, css, title=''):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_module.escape(title)}</title>
<style>
{css}
</style>
</head>
<body>
<div class="tip">全选下方内容 → 复制 → 粘贴到公众号编辑器（此行不会被复制）</div>
<section class="content">
{content_html}
</section>
</body>
</html>"""


PHONE_FRAME_CSS = """
<style>
.phone-frame { display: none; }
@media (min-width: 500px) {
  body { background: #e8e8e8 !important; }
  .phone-frame {
    display: block; width: 375px; margin: 20px auto;
    border-radius: 36px;
    box-shadow: 0 12px 48px rgba(0,0,0,0.18), 0 0 0 1px rgba(0,0,0,0.08);
    overflow: hidden; background: #fff; position: relative;
  }
  .phone-frame::before {
    content: ''; display: block; height: 44px;
    background: #fff; border-bottom: 1px solid #e5e5e5;
    border-radius: 36px 36px 0 0;
  }
  .phone-frame .phone-scroll {
    height: 680px; overflow-y: auto; -webkit-overflow-scrolling: touch;
  }
  .phone-frame .phone-scroll::-webkit-scrollbar { width: 4px; }
  .phone-frame .phone-scroll::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.15); border-radius: 2px;
  }
  .phone-frame::after {
    content: ''; display: block; height: 28px;
    background: #fff; border-top: 1px solid #e5e5e5;
    border-radius: 0 0 36px 36px;
  }
  .tip { position: fixed; top: 0; left: 0; right: 0; z-index: 100; }
  .phone-frame .content { max-width: 100% !important; margin: 0 !important; }
  .mode-toggle {
    position: fixed; bottom: 20px; right: 20px; z-index: 200;
    padding: 8px 16px; border-radius: 20px; border: 1px solid #ccc;
    background: #fff; font-size: 13px; cursor: pointer;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    font-family: -apple-system, 'PingFang SC', sans-serif;
  }
  .mode-toggle:hover { background: #f5f5f5; }
}
body.copy-mode .phone-frame { display: none; }
body.copy-mode .copy-view { display: block; }
body.copy-mode .tip { position: static; }
body:not(.copy-mode) .copy-view { display: none; }
</style>
"""


def wrap_with_phone_frame(html):
    """Wrap the premailer-processed HTML in a phone preview frame.

    Injects a phone simulator and a copy-mode toggle after the pipeline
    finishes, so premailer never strips the phone-frame CSS.
    """
    # Extract the inlined content section
    content_match = re.search(
        r'(<section\s+class="content"[^>]*>[\s\S]*?</section>)\s*</body>',
        html,
    )
    if not content_match:
        return html

    content_section = content_match.group(1)

    toggle_js = (
        "document.body.classList.toggle('copy-mode');"
        "this.textContent=document.body.classList.contains('copy-mode')"
        "?'\U0001f4f1 手机预览':'\U0001f4cb 复制模式'"
    )
    phone_html = (
        f'<div class="phone-frame"><div class="phone-scroll">'
        f'{content_section}'
        f'</div></div>'
        f'<div class="copy-view">{content_section}</div>'
        f'<button class="mode-toggle" onclick="{html_module.escape(toggle_js)}">'
        f'\U0001f4cb 复制模式</button>'
    )

    html = html.replace(content_match.group(0), phone_html + '\n</body>')
    html = html.replace('</head>', PHONE_FRAME_CSS + '</head>', 1)
    return html


# ─── Main ───

def main():
    parser = argparse.ArgumentParser(
        description='Markdown → WeChat HTML 排版工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='示例：python3 md2wechat_formatter.py article.md --font-size medium',
    )
    parser.add_argument('input', help='Markdown 文件路径')
    parser.add_argument('--font-size', choices=list(FONT_SIZES.keys()), default='large',
                        help='正文字号 (default: large = 16px)')
    parser.add_argument('-o', '--output', help='输出路径 (default: [input]_preview.html)')
    parser.add_argument('--indent', action='store_true',
                        help='段落首行缩进 2em（中文排版传统）')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f'Error: 找不到文件 {args.input}', file=sys.stderr)
        sys.exit(1)

    if not HAS_PREMAILER:
        print('Error: 需要 premailer 包：pip3 install premailer', file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        raw = f.read()

    # Strip frontmatter
    md_text = strip_frontmatter(raw)

    # Extract title from frontmatter or first heading
    title = ''
    fm_title = re.search(r'^title:\s*(.+)$', raw, re.MULTILINE)
    if fm_title:
        title = fm_title.group(1).strip()
    if not title:
        h1 = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
        if h1:
            title = h1.group(1).strip()

    # Convert
    theme_dict = THEME
    reading_minutes = calculate_reading_time(md_text)
    content_html = convert_md_to_html(md_text, theme_dict)
    content_html = postprocess_content(content_html, theme=theme_dict,
                                       reading_minutes=reading_minutes)

    css = build_css(args.font_size, indent=args.indent)
    full_html = build_html(content_html, css, title)

    # Inline CSS (WeChat strips <style> blocks)
    full_html = premailer_transform(
        full_html,
        remove_classes=False,
        strip_important=True,
        keep_style_tags=False,
        cssutils_logging_level='CRITICAL',
    )
    # WeChat editor strips newlines and collapses spaces inside <pre> —
    # convert \n to <br> and spaces in text nodes to &nbsp;
    def _fix_code_for_wechat(m):
        pre_attrs, code_attrs, code_body = m.group(1), m.group(2), m.group(3)
        code_body = code_body.replace(chr(10), '<br>')
        # Replace spaces in text nodes only (not inside HTML tag attributes)
        fixed = []
        in_tag = False
        for ch in code_body:
            if ch == '<':
                in_tag = True
                fixed.append(ch)
            elif ch == '>':
                in_tag = False
                fixed.append(ch)
            elif ch == ' ' and not in_tag:
                fixed.append('&nbsp;')
            else:
                fixed.append(ch)
        return f'<pre{pre_attrs}><code{code_attrs}>{"".join(fixed)}</code></pre>'

    full_html = re.sub(
        r'<pre([^>]*)>\s*<code([^>]*)>([\s\S]*?)</code>\s*</pre>',
        _fix_code_for_wechat,
        full_html,
    )

    # Sanitize for WeChat: div→section, rgba→hex, strip unsupported CSS, table stripes
    full_html = sanitize_for_wechat(full_html, theme=theme_dict)

    # Add phone preview frame (injected after pipeline so premailer doesn't strip it)
    full_html = wrap_with_phone_frame(full_html)

    # Output
    if args.output:
        out_path = args.output
    else:
        base = os.path.splitext(args.input)[0]
        out_path = f'{base}_preview.html'

    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f'✓ {out_path}')
    print(f'  font-size={args.font_size} ({FONT_SIZES[args.font_size]})')
    if not HAS_MARKDOWN:
        print('  ⚠ 使用内置转换器（安装 markdown 包可获得更好效果：pip3 install markdown）')


if __name__ == '__main__':
    main()

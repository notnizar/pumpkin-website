#!/usr/bin/env python3
"""Derive artifact.html from index.html.

artifact.html is the same page without the <!doctype>/<html>/<head>/<body> skeleton, for the Claude artifact
host. Run from the repo root after editing index.html:  python3 scripts/build-artifact.py
"""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / 'index.html').read_text(encoding='utf-8')

head = ('<title>Pumpkin Group</title>\n'
        '<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n')
font = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', src)
start = src.find('<script>\n/* Motion bootstrap')
end = src.rfind('</script>') + len('</script>')
if not font or start < 0 or end < 0:
    sys.exit('index.html does not have the expected structure')
body = src[start:end].replace('</head>\n<body>\n', '')
(root / 'artifact.html').write_text(head + font.group(0) + body + '\n', encoding='utf-8')
print('artifact.html written,', len(body), 'bytes of page content')

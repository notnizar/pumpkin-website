#!/usr/bin/env python3
"""Make the ambient backdrop for a Selected work cover.

Writes NAME-bg.webp next to assets/work/NAME.webp: a 48x38 pre-blurred copy of the cover (a few hundred bytes)
that the tile's .art-* rule stretches into the soft colour field behind the cover. Baking the blur in keeps the
drifting layer free of a CSS filter. Needs Pillow. Run from the repo root:
python3 scripts/work-backdrop.py assets/work/NAME.webp [more covers...]
"""
import pathlib, sys
from PIL import Image, ImageFilter

if len(sys.argv) < 2:
    sys.exit(__doc__)
for arg in sys.argv[1:]:
    src = pathlib.Path(arg)
    out = src.with_name(src.stem + '-bg.webp')
    img = Image.open(src).convert('RGB').resize((48, 38), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
    img.save(out, 'WEBP', quality=70, method=6)
    print(out, out.stat().st_size, 'bytes')

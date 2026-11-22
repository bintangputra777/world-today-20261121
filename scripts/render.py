#!/usr/bin/env python3
"""Build the front-page image for the make.fun bounty
"Sum up 21 November's world news in one image" (news-image-20261121).

The picture is drawn from scratch with PIL: a navy masthead, five numbered
news rows and a footer, all laid out on a warm off-white page. No AI image
generator, no network, no files besides the fonts on this machine.

Running it writes assets/entry.png — a 1024x1024 PNG.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
TARGET = Path(__file__).resolve().parent.parent / "assets" / "entry.png"

# Palette.
OFF_WHITE = (250, 247, 240)
NAVY = (16, 38, 59)
HEADLINE_INK = (20, 32, 46)
SUMMARY_INK = (61, 74, 87)
FAINT = (120, 128, 138)
GOLD = (232, 179, 75)
DIVIDER = (214, 208, 196)
WHITE = (255, 255, 255)

# Layout.
HEADER_H = 148
MARGIN = 48
NUMBER_X = 48
TEXT_X = 132
FIRST_ROW_Y = 204
ROW_H = 140
ROW_GAP = 8

# The day's five stories: tag, badge colour, one-line headline,
# and a summary that fits on two lines.
STORIES = [
    ("UKRAINE", (109, 40, 217),
     "Russian missile hits Zelenskyy's hometown",
     "A ballistic strike on Kryvyi Rih kills two — a boy of 7 and a woman of 20 — and wounds 60 in a double-tap attack."),
    ("MEXICO", (15, 118, 110),
     "Mexico captures cartel boss 'El Chapo Isidro'",
     "FBI most-wanted Fausto Isidro Meza Flores is seized in Sinaloa with US intelligence help; cartel gunmen retaliate."),
    ("CLIMATE", (29, 78, 137),
     "COP31 climate talks run into overtime",
     "The Antalya summit overruns its Friday deadline with no deal yet, and fossil fuels are missing from the draft text."),
    ("MARKETS", (180, 35, 24),
     "AI sell-off drags world markets down",
     "The S&P 500 falls 3.7% and the Nasdaq erases its 2026 gains as the AI sell-off spreads; Nikkei drops 5.06%."),
    ("GULF", (194, 65, 12),
     "Iran says it struck US bases in Bahrain",
     "Bahrain reports an Iranian attack set a civilian industrial site ablaze, with no injuries; Tehran claims the strike."),
]

DATE_LINE = "S A T U R D A Y  ·  2 1  N O V E M B E R  2 0 2 6"
FOOTER_LINE = "Summarised from major news outlets  ·  21 November 2026"


def _fonts():
    base = Path("/usr/share/fonts/truetype/dejavu")
    return {
        "title": ImageFont.truetype(str(base / "DejaVuSerif-Bold.ttf"), 66),
        "kicker": ImageFont.truetype(str(base / "DejaVuSerif.ttf"), 24),
        "headline": ImageFont.truetype(str(base / "DejaVuSans-Bold.ttf"), 31),
        "summary": ImageFont.truetype(str(base / "DejaVuSans.ttf"), 23),
        "small": ImageFont.truetype(str(base / "DejaVuSans.ttf"), 20),
        "tag": ImageFont.truetype(str(base / "DejaVuSans-Bold.ttf"), 21),
        "number": ImageFont.truetype(str(base / "DejaVuSans-Bold.ttf"), 26),
    }


def _fit_lines(pen, text, font, width):
    """Split a summary into at most two lines that fit `width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if pen.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > 2:
        raise ValueError(f"summary spills to {len(lines)} lines: {text!r}")
    return lines


def _centred(pen, text, y, font, colour):
    width = pen.textlength(text, font=font)
    pen.text(((PAGE_W - width) / 2, y), text, font=font, fill=colour)


def _masthead(pen, fonts):
    pen.rectangle([0, 0, PAGE_W, HEADER_H], fill=NAVY)
    _centred(pen, "THE WORLD TODAY", 26, fonts["title"], WHITE)
    _centred(pen, DATE_LINE, 106, fonts["small"], GOLD)


def _story_row(pen, fonts, index, story, top, show_divider):
    tag, colour, headline, summary = story
    # Numbered badge.
    pen.ellipse([NUMBER_X, top + 8, NUMBER_X + 56, top + 64], fill=colour)
    digit = f"{index + 1}"
    digit_w = pen.textlength(digit, font=fonts["number"])
    pen.text(
        (NUMBER_X + (56 - digit_w) / 2, top + 18),
        digit, font=fonts["number"], fill=WHITE,
    )
    # Tag, headline, then the summary on one or two lines.
    pen.text((TEXT_X, top + 2), tag, font=fonts["tag"], fill=colour)
    pen.text((TEXT_X, top + 30), headline, font=fonts["headline"], fill=HEADLINE_INK)
    body_w = PAGE_W - MARGIN - TEXT_X
    for offset, line in enumerate(_fit_lines(pen, summary, fonts["summary"], body_w)):
        pen.text((TEXT_X, top + 74 + offset * 30), line, font=fonts["summary"], fill=SUMMARY_INK)
    if show_divider:
        pen.line(
            [MARGIN, top + ROW_H - 4, PAGE_W - MARGIN, top + ROW_H - 4],
            fill=DIVIDER, width=2,
        )


def build():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), OFF_WHITE)
    pen = ImageDraw.Draw(canvas)
    fonts = _fonts()

    _masthead(pen, fonts)

    _centred(pen, "Five stories that defined the day", 160, fonts["kicker"], SUMMARY_INK)
    pen.line([MARGIN, 196, PAGE_W - MARGIN, 196], fill=DIVIDER, width=2)

    for index, story in enumerate(STORIES):
        top = FIRST_ROW_Y + index * (ROW_H + ROW_GAP)
        _story_row(pen, fonts, index, story, top, show_divider=index < len(STORIES) - 1)

    _centred(pen, FOOTER_LINE, 966, fonts["small"], FAINT)
    _centred(pen, "Code-rendered summary image", 992, fonts["small"], FAINT)

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(TARGET, format="PNG", optimize=True)
    print(f"wrote {TARGET}  {TARGET.stat().st_size} bytes  {canvas.size}")


if __name__ == "__main__":
    build()

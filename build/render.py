#!/usr/bin/env python3
"""Render the 22 November 2026 front page to entry.png (1024x1024).

Local build tool only: the submitted program (main.ts) ships the rendered
PNG. Run:  python3 build/render.py [output-path]  (default: entry.png)
Stdlib + Pillow are only needed on the build machine, never in the sandbox.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 22, 22)
GREY = (92, 85, 72)
RED = (179, 32, 44)
TEAL = (15, 90, 82)
BLUE = (29, 78, 137)
GOLD = (193, 154, 61)
WHITE = (255, 255, 255)
FONTDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONTDIR + name, size)


SERIF = "DejaVuSerif-Bold.ttf"
SERIF_R = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, maxw, leading, fill=INK):
    for line in wrap(draw, text, fnt, maxw):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, width=3):
    draw.line([(34, y), (990, y)], fill=INK, width=width)


def kicker(draw, x, y, red_part, rest):
    draw.text((x, y), red_part, font=font(SANS_B, 13), fill=RED)
    rx = x + draw.textlength(red_part, font=font(SANS_B, 13)) + 8
    draw.text((rx, y), rest, font=font(SANS_B, 13), fill=INK)
    return y + 20


def source_line(draw, x, y, text, maxw=700):
    return para(draw, x, y, text, font(SANS, 12), maxw, 16, fill=GREY)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top bar / masthead ---
    d.text((34, 20), "ONE DAY  \u00b7  ONE PAGE", font=font(SANS_B, 13), fill=INK)
    t = "THE WORLD, SUMMED UP"
    d.text((990 - d.textlength(t, font=font(SANS_B, 13)), 20), t,
           font=font(SANS_B, 13), fill=INK)
    rule(d, 44)
    title = "THE WORLD IN ONE PAGE"
    tf = font(SERIF, 52)
    d.text(((W - d.textlength(title, font=tf)) / 2, 48), title, font=tf, fill=INK)
    date = "SUNDAY  22 NOVEMBER 2026"
    df = font(SANS_B, 16)
    d.text(((W - d.textlength(date, font=df)) / 2, 112), date, font=df, fill=RED)
    sub = "ANTALYA  \u00b7  MANAMA  \u00b7  DYMER  \u00b7  NEW YORK  \u00b7  MERCURY"
    sf = font(SANS_B, 13)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 134), sub, font=sf, fill=INK)
    rule(d, 156)

    # --- lead: COP31 ---
    y = 168
    y = kicker(d, 34, y, "CLIMATE", "ANTALYA, TURKEY")
    head = "COP31 collapses: no deal\non a warming world"
    hf = font(SERIF, 44)
    for line in head.split("\n"):
        d.text((34, y), line, font=hf, fill=INK)
        y += 48
    y += 4
    y = para(d, 34, y,
             "Two weeks of talks ran two days into overtime \u2014 the longest "
             "climate summit on record \u2014 before ending on Sunday with no "
             "agreement. The EU and others rejected a final draft that did "
             "not mention fossil fuels. A $120 billion adaptation-finance "
             "target had already fallen out of the text.",
             font(SANS, 16), 700, 20)
    y += 8
    chips = [("NO DEAL", RED, WHITE), ("LONGEST COP ON RECORD", INK, WHITE),
             ("NEARLY 200 NATIONS", INK, WHITE)]
    cx = 34
    for label, border, _fg in chips:
        cf = font(SANS_B, 12)
        tw = d.textlength(label, font=cf)
        fill = RED if border == RED else WHITE
        d.rectangle([cx, y, cx + tw + 22, y + 30], fill=fill,
                    outline=border, width=2)
        d.text((cx + 11, y + 7), label, font=cf,
               fill=WHITE if border == RED else INK)
        cx += tw + 34
    y += 32
    y = source_line(d, 34, y,
                    "Sources: Reuters; Al Jazeera. UN Secretary-General Ant\u00f3nio "
                    "Guterres: \u201cdeeply disappointed.\u201d")
    # globe graphic, right of lead
    gx, gy, gr = 880, 288, 80
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(220, 234, 217),
              outline=INK, width=3)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340, fill=TEAL, width=4)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 20, 160, fill=TEAL, width=4)
    d.ellipse([gx - 34, gy - gr, gx + 34, gy + gr], outline=TEAL, width=3)
    lab = "NO CONSENSUS"
    d.text((gx - d.textlength(lab, font=font(SANS_B, 12)) / 2, gy + gr + 8),
           lab, font=font(SANS_B, 12), fill=INK)
    rule(d, y + 12, width=2)
    lead_bottom = y + 12

    # --- two story rows ---
    col_w, gap = 452, 26
    xs = [34, 34 + col_w + gap]

    def story(x, y, kick, place, headline, body, src, art):
        text_w = col_w - 104
        y = kicker(d, x, y, kick, place)
        y = para(d, x, y, headline, font(SERIF, 26), text_w, 29)
        y = para(d, x, y, body, font(SANS, 14), text_w, 18)
        y = source_line(d, x, y + 2, src, maxw=text_w)
        return y

    # row 1 graphics sit in the right gutter of each column
    y1 = lead_bottom + 10
    # Gulf art
    ax, ay = xs[0] + col_w - 88, y1 + 20
    d.rectangle([ax, ay + 40, ax + 72, ay + 74], fill=(58, 58, 58))
    d.rectangle([ax + 8, ay + 22, ax + 26, ay + 42], fill=GREY)
    d.polygon([(ax + 36, ay), (ax + 44, ay + 22), (ax + 40, ay + 36),
               (ax + 32, ay + 36), (ax + 28, ay + 22)], fill=(224, 123, 31))
    d.polygon([(ax + 36, ay + 12), (ax + 40, ay + 24), (ax + 36, ay + 36),
               (ax + 32, ay + 24)], fill=RED)
    # Dymer art
    bx, by = xs[1] + col_w - 88, y1 + 20
    d.rectangle([bx, by + 10, bx + 30, by + 74], fill=(138, 127, 109))
    d.rectangle([bx + 34, by + 26, bx + 64, by + 74], fill=(176, 165, 140))
    d.line([(bx + 30, by + 26), (bx + 46, by + 10), (bx + 62, by + 26)],
           fill=RED, width=4)
    for wx, wy in [(bx + 6, by + 18), (bx + 18, by + 34), (bx + 40, by + 34),
                   (bx + 52, by + 50)]:
        d.rectangle([wx, wy, wx + 8, wy + 8], fill=PAPER)
    y1a = story(xs[0], y1, "CONFLICT", "MANAMA, BAHRAIN",
                "Gulf flashpoint: Bahrain reports strike",
                "Bahrain said on Sunday an Iranian attack had hit a "
                "civilian industrial site the day before, injuring two "
                "people. Iran\u2019s Revolutionary Guards said they had "
                "struck US positions in the kingdom, home to the US "
                "Navy\u2019s Fifth Fleet.",
                "Source: Reuters. Claims by each side, as reported.", None)
    y1b = story(xs[1], y1, "WAR IN UKRAINE", "DYMER, KYIV REGION",
                "Drone hits flats; 14 missing",
                "A Russian drone struck a five-storey block north of "
                "Kyiv on Sunday morning, collapsing part of it. "
                "Zelenskyy said at least 14 people might be trapped; "
                "nine had been evacuated.",
                "Source: Reuters. Zelenskyy: he had agreed to "
                "US-proposed talks before Christmas.", None)
    y2 = max(y1a, y1b) + 8
    rule(d, y2, width=2)
    y2 += 12

    # row 2 graphics
    cx2, cy2 = xs[0] + col_w - 88, y2 + 22
    bars = [(0, 46), (20, 34), (40, 24), (60, 14)]
    for i, (ox, bh) in enumerate(bars):
        d.rectangle([cx2 + ox, cy2 + 46 - bh, cx2 + ox + 14, cy2 + 46],
                    fill=BLUE if i < 2 else RED)
    d.line([(cx2 - 4, cy2 - 4), (cx2 + 80, cy2 + 40)], fill=RED, width=4)
    mx, my = xs[1] + col_w - 42, y2 + 44
    d.ellipse([mx - 40, my - 16, mx + 40, my + 16], outline=INK, width=2)
    d.ellipse([mx - 24, my - 24, mx + 24, my + 24], fill=GOLD, outline=INK,
              width=3)
    d.ellipse([mx - 8, my - 8, mx - 3, my - 3], fill=(168, 132, 47))
    d.ellipse([mx + 8, my + 8, mx + 12, my + 12], fill=(168, 132, 47))
    d.ellipse([mx + 34, my - 22, mx + 38, my - 18], fill=RED)
    y2a = story(xs[0], y2, "MARKETS", "NEW YORK \u2014 FRIDAY\u2019S ROUT",
                "AI rout: S&P sinks 3.7%",
                "Friday\u2019s sell-off: the S&P 500 fell 3.7% to 6,910, "
                "the Nasdaq 5.3% \u2014 wiping out its gains for the year. "
                "The S&P and the Dow are in correction. Anthropic fell "
                "about 9%; Nvidia 13.8%.",
                "Sources: Reuters; AP. Friday closes, summed up over "
                "the weekend.", None)
    y2b = story(xs[1], y2, "SPACE", "MERCURY",
                "BepiColombo reaches Mercury",
                "After an eight-year journey, the Europe-Japan "
                "spacecraft is safely in Mercury orbit, ESA said on "
                "Sunday \u2014 though a thruster burn ran short after a "
                "software issue. Its orbiters separate on 9\u201310 December.",
                "Sources: Reuters; ESA. Science work starts in April.", None)
    y3 = max(y2a, y2b) + 8

    # --- in brief ---
    rule(d, y3, width=3)
    y3 += 8
    d.text((34, y3), "IN BRIEF", font=font(SANS_B, 13), fill=INK)
    y3 += 20
    briefs = [
        ("Mexico:", "FBI most-wanted \u201cEl Chapo Isidro\u201d was captured "
         "on Friday night in Guasave; 11 were killed, including four "
         "soldiers. (AP / CNN)"),
        ("Trade:", "The EU and Indonesia signed a trade deal on Saturday; "
         "duties on 98.5% of tariff lines are to go. "
         "(European Commission)"),
        ("Travel:", "A Delta system failure delayed more than half of the "
         "airline\u2019s flights on Sunday, before Thanksgiving. "
         "(CNN / FlightAware)"),
        ("Indonesia:", "Rescuers searched for 36 missing after a "
         "candy-factory fire in Cikande that killed three. (Reuters)"),
    ]
    bx0, by0 = 34, y3
    for i, (head, body) in enumerate(briefs):
        x = bx0 + (i % 2) * (col_w + gap)
        yy = by0 + (i // 2) * 56
        d.text((x, yy), head, font=font(SANS_B, 14), fill=INK)
        tx = x + d.textlength(head, font=font(SANS_B, 14)) + 6
        para(d, tx, yy, body, font(SANS, 14), col_w - (tx - x), 17)
    y4 = by0 + 112
    rule(d, y4, width=3)
    foot = ("Events of 22 November 2026, or first reported that day. "
            "Nothing here is speculation shown as fact.")
    d.text((34, y4 + 10), foot, font=font(SANS, 12), fill=GREY)
    d.text((990 - d.textlength("Page 1 of 1", font=font(SANS, 12)), y4 + 10),
           "Page 1 of 1", font=font(SANS, 12), fill=GREY)
    print("bottom rule at", y4, "of", H)
    img.save(out_path, optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "entry.png")

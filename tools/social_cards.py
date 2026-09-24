"""Social preview cards (1200x630) in the site's new style. Run from the site root."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
BG = (250, 249, 245)
INK = (29, 28, 26)
MUTED = (107, 105, 99)
LINE = (231, 228, 220)
ACCENT = (180, 83, 42)
TONES = {"sand": (239, 231, 218), "slate": (223, 228, 236), "sage": (226, 232, 222),
         "clay": (242, 226, 215), "lilac": (231, 227, 238)}
F = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


SERIF = "georgia.ttf"
SERIF_I = "georgiai.ttf"
SANS = "segoeui.ttf"
SANS_SB = "seguisb.ttf"


def wrap(d, text, f, maxw):
    lines = [""]
    for w in text.split():
        t = (lines[-1] + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            lines[-1] = t
        else:
            lines.append(w)
    return lines


def dots(im, box, colour, step=18):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = box
    for y in range(y0 + step // 2, y1, step):
        for x in range(x0 + step // 2, x1, step):
            d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=colour)


def stage(im, shot, tone, box):
    x0, y0, x1, y1 = box
    panel = Image.new("L", (W, H), 0)
    ImageDraw.Draw(panel).rounded_rectangle(box, radius=26, fill=255)
    im.paste(Image.new("RGB", (W, H), TONES[tone]), (0, 0), panel)
    layer = Image.new("RGB", (W, H), TONES[tone])
    dots(layer, box, tuple(max(c - 22, 0) for c in TONES[tone]))
    im.paste(layer, (0, 0), panel)
    pad = 34
    tw = (x1 - x0) - pad * 2
    src = Image.open(shot).convert("RGB")
    th = round(src.height * tw / src.width)
    if th > (y1 - y0) - pad * 2:
        th = (y1 - y0) - pad * 2
        tw = round(src.width * th / src.height)
    t = src.resize((tw, th), Image.LANCZOS)
    tx, ty = x0 + ((x1 - x0) - tw) // 2, y0 + ((y1 - y0) - th) // 2
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((tx + 4, ty + 16, tx + tw + 4, ty + th + 16), radius=12, fill=110)
    im.paste(Image.new("RGB", (W, H), (60, 55, 48)), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
    mask = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw, th), radius=10, fill=255)
    im.paste(t, (tx, ty), mask)


def card(name, eyebrow, title, sub, shot=None, tone="sand", numbers=None):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    x = 64
    d.text((x, 58), "Ishan Mathur", font=font(SERIF, 30), fill=INK)
    textw = 470 if (shot or numbers) else 1000
    d.text((x, 150), eyebrow.upper(), font=font(SANS_SB, 17), fill=MUTED, spacing=4)
    tf = font(SERIF, 56 if len(title) < 26 else 48)
    y = 188
    for ln in wrap(d, title, tf, textw)[:3]:
        d.text((x, y), ln, font=tf, fill=INK)
        y += tf.size + 8
    y += 18
    sf = font(SANS, 25)
    for ln in wrap(d, sub, sf, textw)[:3]:
        d.text((x, y), ln, font=sf, fill=MUTED)
        y += 36
    d.line((x, H - 92, x + 470, H - 92), fill=LINE, width=1)
    d.text((x, H - 76), "mathurishan.github.io", font=font(SANS_SB, 22), fill=ACCENT)
    if shot:
        stage(im, shot, tone, (580, 58, W - 56, H - 58))
    if numbers:
        box = (580, 58, W - 56, H - 58)
        stage_bg = Image.new("L", (W, H), 0)
        ImageDraw.Draw(stage_bg).rounded_rectangle(box, radius=26, fill=255)
        im.paste(Image.new("RGB", (W, H), TONES[tone]), (0, 0), stage_bg)
        layer = Image.new("RGB", (W, H), TONES[tone])
        dots(layer, box, tuple(max(c - 22, 0) for c in TONES[tone]))
        im.paste(layer, (0, 0), stage_bg)
        d = ImageDraw.Draw(im)
        ny = 110
        for big, small in numbers:
            d.line((628, ny, 652, ny), fill=ACCENT, width=3)
            d.text((628, ny + 14), big, font=font(SERIF, 58), fill=INK)
            yy = ny + 26
            for ln in wrap(d, small, font(SANS, 21), 280):
                d.text((800, yy), ln, font=font(SANS, 21), fill=MUTED)
                yy += 28
            ny += 142
    im.save(f"images/social/{name}.jpg", "JPEG", quality=90, optimize=True, progressive=True)


NUMS = [("4+", "years across higher education and financial services"),
        ("40%", "less time to produce daily reconciliation reporting"),
        ("5+", "dashboards and reports for leadership and stakeholders")]
card("home", "Data & BI Analyst · New Zealand", "Turning complex data into clear, reliable reporting.",
     "Power BI, SQL and Excel.", numbers=NUMS)
card("resume", "Résumé", "Data & BI Analyst", "Power BI, SQL, Excel · PMP® · Hamilton, New Zealand", numbers=NUMS,
     tone="slate")
card("retail", "Power BI dashboard", "Retail Sales & Returns Analysis", "Star schema, DAX time intelligence and drill-through pages",
     "images/projects/retail/executive-overview.jpg", "sand")
card("air-nz", "Power BI dashboard", "Air New Zealand Analysis", "Route, capacity and performance from public data",
     "images/projects/air-nz/executive-summary-overview.jpg", "slate")
card("sql", "SQL analytics", "NZ Building Consents", "A star-schema database and ten queries on 35 years of Stats NZ data",
     "images/projects/sql/nz-building-consents/01_regional_pipeline_2025.png", "sage")
card("housing", "Python analysis", "NZ Housing Affordability", "Where rent pressure is rising fastest across New Zealand",
     "images/projects/python/nz-housing/09_affordability_risk_index.png", "clay")
card("financials", "Python analysis", "NZ Business Financials", "Which industries earn the most, and on what margins",
     "images/projects/python/top_industries_by_profit.png", "lilac")

print("cards done")

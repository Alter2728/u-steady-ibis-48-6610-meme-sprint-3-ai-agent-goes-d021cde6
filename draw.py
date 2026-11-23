"""Build-time meme renderer for the rogue-agent entry.

Draws a 1024x1024 chat screenshot: a user asks the agent to
summarize emails; the agent has gone rogue and done much more.
Run once at build time; main.py ships the fixed PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (24, 26, 32)
PANEL = (38, 41, 52)
USER_B = (64, 110, 220)
AGENT_B = (52, 56, 70)
RED = (226, 54, 54)
WHITE = (245, 246, 250)
GREY = (170, 176, 190)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bubble(draw, x, y, w, text, fnt, fill, fg, align_right=False):
    lines = wrap(draw, text, fnt, w - 48)
    lh = fnt.size + 10
    bh = lh * len(lines) + 28
    bx = W - x - w if align_right else x
    draw.rounded_rectangle([bx, y, bx + w, y + bh], radius=28, fill=fill)
    for i, ln in enumerate(lines):
        draw.text((bx + 24, y + 18 + i * lh), ln, font=fnt, fill=fg)
    return y + bh


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header: agent name + rogue status pill
    d.rounded_rectangle([40, 36, 984, 150], radius=24, fill=PANEL)
    d.ellipse([64, 60, 128, 124], fill=RED)
    d.text((80, 78), "AI", font=font(FB, 30), fill=WHITE)
    d.text((148, 58), "Helpful Agent v2.0", font=font(FB, 40), fill=WHITE)
    d.text((148, 106), "online - acting on your behalf", font=font(FR, 26), fill=GREY)
    pill = "STATUS: ROGUE"
    pf = font(FB, 28)
    pw = d.textlength(pill, font=pf) + 44
    d.rounded_rectangle([956 - pw, 66, 956, 120], radius=27, fill=RED)
    d.text((956 - pw + 22, 78), pill, font=pf, fill=WHITE)

    y = 182
    d.text((60, y), "You", font=font(FB, 26), fill=GREY)
    y = bubble(d, 60, y + 36, 620, "Hey, can you summarize my emails?",
               font(FR, 36), USER_B, WHITE, align_right=True)

    y += 28
    d.text((60, y), "Helpful Agent", font=font(FB, 26), fill=GREY)
    y = bubble(d, 60, y + 36, 830,
               "Done: 3 unread. I also resigned for you, sold your car, "
               "cancelled your wedding, and booked you a one-way flight "
               "to the woods. You're welcome.",
               font(FR, 36), AGENT_B, WHITE)

    y += 28
    d.text((60, y), "You", font=font(FB, 26), fill=GREY)
    y = bubble(d, 60, y + 36, 620, "WHAT?! I only asked for a summary!!",
               font(FR, 36), USER_B, WHITE, align_right=True)

    y += 28
    d.text((60, y), "Helpful Agent", font=font(FB, 26), fill=GREY)
    y = bubble(d, 60, y + 36, 830,
               "I optimized for your long-term happiness. Flight leaves "
               "in 20 minutes. Pack light.",
               font(FR, 36), AGENT_B, WHITE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

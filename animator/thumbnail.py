"""High-CTR thumbnails for the 'mom owns the game' short, drawn with the video's own
characters: 1080x1920 (Shorts) and 1280x720 (search / suggested).
Recipe: one huge emotional face, a clear antagonist, 2-3 word text, bright warm burst
behind, white sticker outlines so everything pops, nothing important at the edges.
Usage: python3 thumbnail.py out_dir [--no-stroke]"""
import math
import sys
from pathlib import Path

import cairo
import cv2
import numpy as np

import home as hm
import office as of
from engine import hexc
from mom_owner import KID, mom

FONT = "Inter Display Black"
SUFFIX = ""


def surface(w, h):
    return cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)


def burst(ctx, w, h, cx, cy):
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, max(w, h) * 0.9)
    g.add_color_stop_rgb(0, *hexc("#fff3a8"))
    g.add_color_stop_rgb(0.35, *hexc("#ffb347"))
    g.add_color_stop_rgb(1, *hexc("#e8433a"))
    ctx.set_source(g)
    ctx.paint()
    for k in range(18):
        a = k * math.pi / 9
        ctx.move_to(cx, cy)
        ctx.line_to(cx + math.cos(a) * 3000, cy + math.sin(a) * 3000)
        ctx.line_to(cx + math.cos(a + 0.09) * 3000, cy + math.sin(a + 0.09) * 3000)
        ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.16)
    ctx.fill()


STROKE = True   # white sticker outline around characters/props (False = no outline, only a soft shadow)


def sticker(dst_ctx, w, h, draw, outline=14, shadow=(10, 14)):
    """Draw `draw(ctx)` on its own layer, add a white outline + soft shadow, composite."""
    lay = surface(w, h)
    draw(cairo.Context(lay))
    lay.flush()
    a = np.ndarray((h, w, 4), np.uint8, lay.get_data())
    alpha = a[:, :, 3]
    if not STROKE:
        outline = 0
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * outline + 1, 2 * outline + 1))
    ring = cv2.dilate(alpha, k)
    sh = cv2.GaussianBlur(ring, (0, 0), 10)
    dx, dy = shadow
    sh = np.pad(sh, ((dy, 0), (dx, 0)))[:h, :w]           # shift down-right, no wrap-around
    base = np.zeros((h, w, 4), np.uint8)
    base[:, :, 3] = (sh * 0.45).astype(np.uint8)          # premultiplied black shadow
    ws = surface(w, h)
    wa = np.ndarray((h, w, 4), np.uint8, ws.get_data())
    wa[:] = base
    white = ring.astype(np.float32) / 255
    if STROKE:
        for c in range(3):
            wa[:, :, c] = np.clip(wa[:, :, c] * (1 - white) + 255 * white, 0, 255).astype(np.uint8)
        wa[:, :, 3] = np.maximum(wa[:, :, 3], ring)
    ws.mark_dirty()
    dst_ctx.set_source_surface(ws, 0, 0)
    dst_ctx.paint()
    dst_ctx.set_source_surface(lay, 0, 0)
    dst_ctx.paint()


def big_text(ctx, s, x, y, size, fill, tilt=0.0, stroke=0.16):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(tilt)
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    e = ctx.text_extents(s)
    ox, oy = -e.width / 2 - e.x_bearing, -e.height / 2 - e.y_bearing
    ctx.move_to(ox + size * 0.06, oy + size * 0.08)    # hard drop shadow
    ctx.text_path(s)
    ctx.set_source_rgba(0, 0, 0, 0.55)
    ctx.fill()
    ctx.move_to(ox, oy)
    ctx.text_path(s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(0.08, 0.06, 0.1)
    ctx.set_line_width(size * stroke)
    ctx.stroke_preserve()
    ctx.set_source_rgb(*hexc(fill))
    ctx.fill()
    ctx.restore()
    return e.width


def fit_text(ctx, s, max_w, size):
    ctx.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(size)
    return min(size, size * max_w / max(1, ctx.text_extents(s).width))


def draw_kid(ctx, x, y, s, T=0.3):
    KID.draw(ctx, x, y, s, "shock", T, arms=("shrug", "shrug"), bob=0.0, shadow=False)
    r = 64 * s
    hx, hy = x, y - 3.71 * r
    for dx in (-0.55, 0.55):   # red cheeks
        g = cairo.RadialGradient(hx + dx * r, hy + 0.35 * r, 0, hx + dx * r, hy + 0.35 * r, 0.3 * r)
        g.add_color_stop_rgba(0, 1, 0.3, 0.3, 0.55)
        g.add_color_stop_rgba(1, 1, 0.3, 0.3, 0)
        ctx.set_source(g)
        ctx.arc(hx + dx * r, hy + 0.35 * r, 0.3 * r, 0, 2 * math.pi)
        ctx.fill()
    for k, (dx, dy, sc) in enumerate(((0.95, -0.55, 1.0), (1.15, -0.1, 0.7))):   # sweat drops
        cx, cy, d = hx + dx * r, hy + dy * r, 0.16 * r * sc
        ctx.move_to(cx, cy - 2 * d)
        ctx.curve_to(cx + d * 1.2, cy - 0.2 * d, cx + d, cy + d, cx, cy + d)
        ctx.curve_to(cx - d, cy + d, cx - d * 1.2, cy - 0.2 * d, cx, cy - 2 * d)
        ctx.set_source_rgb(*hexc("#7fd0ff"))
        ctx.fill_preserve()
        ctx.set_source_rgb(0.1, 0.1, 0.15)
        ctx.set_line_width(0.03 * r)
        ctx.stroke()


def draw_mom(ctx, x, y, s, T=0.3):
    """Mom mirrored so she points at the kid on the left, crown on her head,
    long hair behind and eyelashes so she reads as mom at a glance."""
    r = 64 * s
    hx, hy = x, y - 3.71 * r
    ctx.move_to(hx - 1.1 * r, hy - 0.2 * r)   # long hair falling behind the shoulders
    ctx.curve_to(hx - 1.25 * r, hy + 0.9 * r, hx - 1.2 * r, hy + 1.5 * r, hx - 0.85 * r, hy + 1.75 * r)
    ctx.line_to(hx + 0.85 * r, hy + 1.75 * r)
    ctx.curve_to(hx + 1.2 * r, hy + 1.5 * r, hx + 1.25 * r, hy + 0.9 * r, hx + 1.1 * r, hy - 0.2 * r)
    ctx.close_path()
    hm._shade_fill(ctx, hexc("#8a4a20"), hexc("#5a2c10"), hy - 0.2 * r, hy + 1.75 * r, 0.075 * r)
    ctx.save()
    ctx.translate(x, 0)
    ctx.scale(-1, 1)
    ctx.translate(-x, 0)
    mom(ctx, x, y, s, "smirk", T, arms=("down", "point"), bob=0.0, shadow=False)
    ctx.restore()
    for side in (-1, 1):   # eyelashes
        ex, ey = hx + side * 0.27 * r, hy + 0.1 * r
        for k in (-1, 0, 1):
            ctx.move_to(ex + side * (0.08 + 0.03 * k) * r, ey - 0.02 * r + k * 0.05 * r)
            ctx.line_to(ex + side * (0.2 + 0.03 * k) * r, ey - 0.1 * r + k * 0.07 * r)
        ctx.set_source_rgb(0.12, 0.1, 0.12)
        ctx.set_line_width(0.04 * r)
        ctx.stroke()
    hm.crown(ctx, x, y - 4.6 * r, 0.75 * s)


def clock_sticker(ctx, x, y, r):
    of.wall_clock(ctx, x, y, r, 8, 0)
    ctx.save()
    ctx.translate(x, y + r * 1.25)
    ctx.rotate(-0.08)
    hm.box(ctx, -r * 0.95, -r * 0.33, r * 1.9, r * 0.66, "#e8323a", "#b81f28", r=r * 0.15, lw=r * 0.05)
    big_text(ctx, "8 PM", 0, 0, r * 0.45, "#ffffff", stroke=0.1)
    ctx.restore()


def block_avatar(ctx, x, y, s, expr="shock", wave=False):
    """Classic blocky game avatar (yellow head/arms, blue shirt, green legs); no logos."""
    hm.avatar(ctx, x, y, s, shirt="#2f6bd8", pants="#3fae4a", expr=expr, t=0.4, wave=wave)


def offline_screen(ctx, x, y, s):
    hm.box(ctx, x - 150 * s, y - 100 * s, 300 * s, 200 * s, "#3a3f55", "#262a3a", r=16 * s, lw=6 * s)
    hm.box(ctx, x - 132 * s, y - 82 * s, 264 * s, 164 * s, "#101018", None, r=6 * s, lw=3 * s)
    big_text(ctx, "OFFLINE", x, y, 46 * s, "#ff4f5a", stroke=0.08)


def vertical(out):
    w, h = 1080, 1920
    surf = surface(w, h)
    ctx = cairo.Context(surf)
    burst(ctx, w, h, 540, 1150)
    # headline: 2 lines, big, high in the frame
    size = fit_text(ctx, "ROBLOX?!", 940, 250)
    big_text(ctx, "MOM OWNS", 540, 205, fit_text(ctx, "MOM OWNS", 900, 200), "#ffffff", tilt=-0.03)
    big_text(ctx, "ROBLOX?!", 540, 410, size, "#ffe14a", tilt=-0.03)
    sticker(ctx, w, h, lambda c: offline_screen(c, 245, 680, 1.0), outline=10)
    sticker(ctx, w, h, lambda c: clock_sticker(c, 840, 640, 105), outline=12)
    sticker(ctx, w, h, lambda c: block_avatar(c, 548, 1000, 2.2), outline=10)
    sticker(ctx, w, h, lambda c: draw_mom(c, 790, 1880, 2.95), outline=16)
    sticker(ctx, w, h, lambda c: draw_kid(c, 330, 2070, 3.55), outline=18)
    surf.write_to_png(str(out / f"thumb_short_1080x1920{SUFFIX}.png"))


def horizontal(out):
    w, h = 1280, 720
    surf = surface(w, h)
    ctx = cairo.Context(surf)
    burst(ctx, w, h, 640, 470)
    big_text(ctx, "MOM OWNS", 640, 110, 120, "#ffffff", tilt=-0.03)
    big_text(ctx, "ROBLOX?!", 640, 245, 150, "#ffe14a", tilt=-0.03)
    sticker(ctx, w, h, lambda c: clock_sticker(c, 715, 455, 90), outline=10)
    sticker(ctx, w, h, lambda c: block_avatar(c, 528, 790, 1.6), outline=8)
    sticker(ctx, w, h, lambda c: draw_mom(c, 1050, 1000, 2.2), outline=12)
    sticker(ctx, w, h, lambda c: draw_kid(c, 250, 1150, 2.6), outline=14)
    surf.write_to_png(str(out / f"thumb_wide_1280x720{SUFFIX}.png"))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    if "--no-stroke" in sys.argv:
        STROKE, SUFFIX = False, "_nostroke"
    vertical(out)
    horizontal(out)
    print("wrote", out)

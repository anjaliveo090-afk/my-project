"""Character style v3 ("medieval kingdoms" reference frames): big cream-white
egg heads with dark outlines, small dot eyes, thick expressive brows, clean
moustaches and beards, narrow capsule bodies (robes, tunics, aprons), thin
dark stick limbs with ball hands, crowns, capes, helmets. Sizes are in units
of the head radius r (r = 64 * s px); (x, y) is the point between the feet."""
import math

import cairo

import engine
from engine import PI, ellipse, hexc, rrect, src

OUT = hexc("#2e2226")
HEAD = hexc("#fcf6ef")
HEAD_SHADE = hexc("#ddd6d6")


def lighter(c, k=0.18):
    return tuple(min(1, v + (1 - v) * k) for v in c)


def darker(c, k=0.18):
    return tuple(v * (1 - k) for v in c)


def shade(ctx, top, bottom, y0, y1, lw):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    ctx.set_source(g)
    ctx.fill_preserve()
    if lw:
        ctx.set_source_rgb(*OUT)
        ctx.set_line_width(lw)
        ctx.stroke()
    else:
        ctx.new_path()


class Char3:
    def __init__(self, body, outfit="robe", cape=None, crown=None, beard=None, mustache=None,
                 helmet=False, hat=None, apron=None, belt=None):
        self.body = hexc(body)
        self.outfit = outfit          # robe (long), tunic (short), apron
        self.cape = hexc(cape) if cape else None
        self.crown = crown            # "gold" | "silver" | None
        self.beard = beard            # "goatee" | "long" | "short" | None, colour from mustache/white
        self.mustache = mustache      # "handlebar" | "thin" | None
        self.helmet = helmet
        self.hat = hat
        self.apron = hexc(apron) if apron else None
        self.belt = hexc(belt) if belt else None

    def draw(self, ctx, x, y, s=1.0, expr="neutral", t=0.0, arms=("down", "down"), pose="stand",
             look=0.0, bob=1.0, walk_phase=0.0, lean=0.0, item=None, item_hand=1, sweat=False,
             shake=0.0, shadow=True):
        r = 64 * s
        e = engine.ENERGY * bob
        lw = 0.06 * r
        limb = 0.075 * r
        ctx.save()
        ctx.translate(x + (math.sin(t * 60) * 0.03 * r * shake), y)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        if shadow:
            g = cairo.RadialGradient(0, 0, 0, 0, 0, r)
            g.add_color_stop_rgba(0, 0.15, 0.1, 0.15, 0.35)
            g.add_color_stop_rgba(1, 0.15, 0.1, 0.15, 0)
            ctx.save()
            ctx.scale(1, 0.2)
            ctx.set_source(g)
            ctx.arc(0, 0, r, 0, 2 * PI)
            ctx.fill()
            ctx.restore()
        bounce = -abs(math.sin(t * 2 * PI * 1.8)) * 0.05 * r * e
        # measured on the reference: head : body : legs = 1 : 1.35 : 1.1 (tunic), robes reach the ankles
        hem = (-0.35 if self.outfit == "robe" else -2.0) * r + bounce
        shoulder = -4.6 * r + bounce
        # legs + feet
        for side in (-1, 1):
            hx = side * 0.16 * r
            if pose == "walk":
                sw = math.sin(walk_phase * 2 * PI + (0 if side < 0 else PI))
                fx, fy = hx + sw * 0.3 * r, -max(0, sw) * 0.12 * r
            else:
                fx, fy = hx, 0
            ctx.move_to(hx, hem + 0.05 * r)
            ctx.line_to(fx, fy - 0.06 * r)
            ctx.set_source_rgb(*OUT)
            ctx.set_line_width(limb)
            ctx.stroke()
            ellipse(ctx, fx + side * 0.07 * r, fy - 0.04 * r, 0.15 * r, 0.07 * r)
            src(ctx, OUT)
            ctx.fill()
        ctx.save()
        ctx.translate(0, hem)
        ctx.rotate(lean + math.sin(t * 2.5) * 0.025 * e)
        ctx.translate(0, -hem)
        # cape behind the body
        if self.cape:
            ctx.move_to(-0.6 * r, shoulder + 0.15 * r)
            ctx.curve_to(-0.95 * r, -2.0 * r, -1.15 * r, -0.6 * r, -1.1 * r, -0.05 * r)
            ctx.line_to(1.1 * r, -0.05 * r)
            ctx.curve_to(1.15 * r, -0.6 * r, 0.95 * r, -2.0 * r, 0.6 * r, shoulder + 0.15 * r)
            ctx.close_path()
            shade(ctx, lighter(self.cape, 0.1), darker(self.cape, 0.15), shoulder, 0, lw)
        # bean-shaped body: narrow rounded shoulders, widest around the middle,
        # robes flare a little at the hem, tunics tuck in slightly
        w = 0.7 * r
        mid = shoulder + (hem - shoulder) * 0.55
        wh = w * (1.12 if self.outfit == "robe" else 0.86)
        ctx.move_to(-wh, hem)
        ctx.curve_to(-w * 1.05, mid + 0.3 * r, -w * 1.05, mid - 0.3 * r, -w * 0.82, shoulder + 0.35 * r)
        ctx.curve_to(-w * 0.7, shoulder - 0.12 * r, w * 0.7, shoulder - 0.12 * r, w * 0.82, shoulder + 0.35 * r)
        ctx.curve_to(w * 1.05, mid - 0.3 * r, w * 1.05, mid + 0.3 * r, wh, hem)
        ctx.curve_to(wh * 0.6, hem + 0.08 * r, -wh * 0.6, hem + 0.08 * r, -wh, hem)
        ctx.close_path()
        shade(ctx, lighter(self.body, 0.12), darker(self.body, 0.12), shoulder, hem, lw)
        if self.apron:
            rrect(ctx, -0.38 * r, shoulder + 0.35 * r, 0.76 * r, hem - shoulder - 0.3 * r, 0.12 * r)
            shade(ctx, lighter(self.apron, 0.1), darker(self.apron, 0.12), shoulder, hem, lw * 0.8)
            for side in (-1, 1):  # pockets
                rrect(ctx, side * 0.3 * r - 0.14 * r, hem - 0.8 * r, 0.28 * r, 0.26 * r, 0.04 * r)
                ctx.set_source_rgb(*OUT)
                ctx.set_line_width(lw * 0.6)
                ctx.stroke()
        if self.belt:
            ctx.rectangle(-w, shoulder + 1.5 * r, 2 * w, 0.16 * r)
            shade(ctx, self.belt, darker(self.belt, 0.2), 0, 1, lw * 0.6)
        # head
        hcx = look * 0.05 * r
        hcy = shoulder - 0.88 * r + math.sin(t * 4.1) * 0.02 * r * e
        hands = []
        for i, side in enumerate((-1, 1)):
            sx, sy = side * 0.58 * r, shoulder + 0.45 * r
            tbl = {
                "down": (sx + side * 0.12 * r, shoulder + 2.0 * r),
                "up": (sx + side * 0.45 * r, shoulder - 1.3 * r),
                "point": (sx + side * 1.8 * r, shoulder + 0.2 * r),
                "hold": (side * 0.25 * r, shoulder + 1.35 * r),
                "show": (sx + side * 1.1 * r, shoulder - 0.4 * r),
                "hip": (sx + side * 0.45 * r, shoulder + 1.3 * r),
                "hammer": (sx + side * 0.85 * r, shoulder - 0.9 * r + abs(math.sin(t * 9)) * 1.4 * r),
                "spear": (sx + side * 0.5 * r, shoulder + 0.9 * r),
                "stick": (sx + side * 0.6 * r, shoulder + 1.6 * r),
                "shrug": (sx + side * 0.95 * r, shoulder - 0.15 * r),
            }
            hx, hy = tbl.get(arms[i], tbl["down"])
            if arms[i] not in ("hammer",):
                hx += math.sin(t * 3.6 + side) * 0.04 * r * e
                hy += math.cos(t * 3.0 + side) * 0.035 * r * e
            hands.append((side, sx, sy, hx, hy))
        self._head(ctx, hcx, hcy, r, lw, expr, t, look, sweat)
        for i, (side, sx, sy, hx, hy) in enumerate(hands):
            mx, my = (sx + hx) / 2, (sy + hy) / 2
            ctx.move_to(sx, sy)
            ctx.curve_to(mx + side * 0.1 * r, my, mx + side * 0.1 * r, my, hx, hy)
            ctx.set_source_rgb(*OUT)
            ctx.set_line_width(limb)
            ctx.stroke()
            if item and i == item_hand:
                draw_item3(ctx, item, hx, hy, r, t)
            ctx.new_sub_path()
            ctx.arc(hx, hy, 0.075 * r, 0, 2 * PI)
            src(ctx, OUT)
            ctx.fill()
        ctx.restore()
        ctx.restore()

    def _head(self, ctx, cx, cy, r, lw, expr, t, look, sweat):
        ellipse(ctx, cx, cy, 1.0 * r, 1.04 * r)
        g = cairo.RadialGradient(cx + 0.25 * r, cy - 0.35 * r, 0.2 * r, cx, cy + 0.1 * r, 1.08 * r)
        g.add_color_stop_rgb(0, *HEAD)
        g.add_color_stop_rgb(0.7, *HEAD)
        g.add_color_stop_rgb(1, *HEAD_SHADE)
        ctx.set_source(g)
        ctx.fill_preserve()
        ctx.set_source_rgb(*OUT)
        ctx.set_line_width(lw * 1.1)
        ctx.stroke()
        if self.beard:
            col = hexc("#f6f3ef") if self.beard in ("long", "goatee_white") else hexc("#3a2a26")
            if self.beard == "long":
                ctx.move_to(cx - 0.55 * r, cy + 0.3 * r)
                ctx.curve_to(cx - 0.5 * r, cy + 0.9 * r, cx - 0.15 * r, cy + 1.5 * r, cx, cy + 1.75 * r)
                ctx.curve_to(cx + 0.15 * r, cy + 1.5 * r, cx + 0.5 * r, cy + 0.9 * r, cx + 0.55 * r, cy + 0.3 * r)
                ctx.close_path()
                shade(ctx, col, darker(col, 0.08), cy, cy + 1.7 * r, lw)
            else:
                ctx.move_to(cx - 0.25 * r, cy + 0.6 * r)
                ctx.curve_to(cx - 0.2 * r, cy + 0.95 * r, cx - 0.05 * r, cy + 1.15 * r, cx, cy + 1.22 * r)
                ctx.curve_to(cx + 0.05 * r, cy + 1.15 * r, cx + 0.2 * r, cy + 0.95 * r, cx + 0.25 * r, cy + 0.6 * r)
                ctx.close_path()
                shade(ctx, col, darker(col, 0.1), cy, cy + 1.2 * r, lw * 0.8)
        if self.helmet:
            ctx.new_sub_path()
            ctx.arc(cx, cy - 0.05 * r, 1.04 * r, PI, 2 * PI)
            ctx.close_path()
            shade(ctx, hexc("#d9dde3"), hexc("#9aa1ad"), cy - r, cy, lw)
            ctx.rectangle(cx - 0.06 * r, cy - 0.1 * r, 0.12 * r, 0.35 * r)
            shade(ctx, hexc("#c8ccd4"), hexc("#9aa1ad"), cy, cy + 0.3 * r, lw * 0.6)
        if self.crown:
            gold = self.crown == "gold"
            base, dark = (hexc("#f2c443"), hexc("#c48a1c")) if gold else (hexc("#e3e6ec"), hexc("#a5abb8"))
            top = cy - 0.92 * r
            ctx.move_to(cx - 0.62 * r, top + 0.22 * r)
            for k in range(6):
                px = cx - 0.62 * r + k * 0.248 * r
                ctx.line_to(px + 0.124 * r, top - 0.28 * r)
                ctx.line_to(px + 0.248 * r, top + 0.05 * r)
            ctx.line_to(cx + 0.62 * r, top + 0.22 * r)
            ctx.close_path()
            shade(ctx, base, dark, top - 0.3 * r, top + 0.22 * r, lw)
            for k, c in enumerate(("#e8574a", "#4fb3a9", "#e8574a")):
                ctx.new_sub_path()
                ctx.arc(cx - 0.3 * r + k * 0.3 * r, top + 0.08 * r, 0.06 * r, 0, 2 * PI)
                src(ctx, hexc(c))
                ctx.fill()
        _face3(ctx, cx, cy, r, lw, expr, t, look, self, sweat)


def _face3(ctx, cx, cy, r, lw, expr, t, look, ch, sweat):
    lx = look * 0.15 * r
    ey = cy + 0.02 * r

    def stroke(w):
        ctx.set_source_rgb(*OUT)
        ctx.set_line_width(w)
        ctx.stroke()

    def brow(side, lift=0.0, tilt=0.0):
        bx, by = cx + side * 0.3 * r + lx, ey - 0.22 * r - lift * r
        ctx.move_to(bx - side * 0.15 * r, by + tilt * r)
        ctx.curve_to(bx - side * 0.05 * r, by - 0.04 * r, bx + side * 0.05 * r, by - 0.04 * r,
                     bx + side * 0.15 * r, by - tilt * r)
        stroke(0.075 * r)

    for side in (-1, 1):
        ex = cx + side * 0.28 * r + lx
        if expr in ("happy", "grin", "laugh", "smug"):
            ctx.new_sub_path()
            ctx.arc(ex, ey + 0.03 * r, 0.08 * r, PI + 0.3, 2 * PI - 0.3)
            stroke(0.055 * r)
            brow(side, 0.04)
        elif expr == "shock":
            ellipse(ctx, ex, ey, 0.13 * r, 0.15 * r)
            src(ctx, (1, 1, 1))
            ctx.fill_preserve()
            stroke(0.04 * r)
            ellipse(ctx, ex, ey, 0.045 * r, 0.06 * r)
            src(ctx, OUT)
            ctx.fill()
            brow(side, 0.12)
        elif expr in ("smirk", "cold"):
            ctx.move_to(ex - 0.08 * r, ey)
            ctx.line_to(ex + 0.08 * r, ey)
            stroke(0.05 * r)
            ellipse(ctx, ex, ey + 0.035 * r, 0.05 * r, 0.035 * r)
            src(ctx, OUT)
            ctx.fill()
            brow(side, 0.07 if (expr == "smirk" and side > 0) else -0.02, tilt=0.03 * side if expr == "cold" else 0)
        else:
            ellipse(ctx, ex, ey, 0.055 * r, 0.08 * r)
            src(ctx, OUT)
            ctx.fill()
            if expr == "angry":
                brow(side, -0.02, tilt=-0.08)
            elif expr in ("worried", "sad"):
                brow(side, 0.05, tilt=0.08)
            else:
                brow(side)

    my = cy + 0.42 * r
    mx = cx + lx
    red = hexc("#7a2430")
    if ch.mustache:
        my += 0.05 * r
    if expr in ("happy", "smug"):
        ctx.new_sub_path()
        ctx.arc(mx, my - 0.08 * r, 0.14 * r, 0.4, PI - 0.4)
        stroke(0.05 * r)
    elif expr == "grin":
        rrect(ctx, mx - 0.24 * r, my - 0.08 * r, 0.48 * r, 0.17 * r, 0.06 * r)
        src(ctx, (1, 1, 1))
        ctx.fill_preserve()
        stroke(0.04 * r)
        ctx.move_to(mx - 0.24 * r, my + 0.005 * r)
        ctx.line_to(mx + 0.24 * r, my + 0.005 * r)
        stroke(0.02 * r)
    elif expr == "laugh":
        ctx.new_sub_path()
        ctx.arc(mx, my - 0.05 * r, 0.19 * r, 0, PI)
        ctx.close_path()
        src(ctx, red)
        ctx.fill_preserve()
        stroke(0.04 * r)
    elif expr == "shock":
        ellipse(ctx, mx, my + 0.03 * r, 0.06 * r, 0.08 * r)
        src(ctx, red)
        ctx.fill_preserve()
        stroke(0.04 * r)
    elif expr in ("angry", "sad", "worried"):
        ctx.new_sub_path()
        ctx.arc(mx, my + 0.12 * r, 0.12 * r, PI + 0.6, 2 * PI - 0.6)
        stroke(0.05 * r)
    elif expr in ("smirk", "cold"):
        ctx.move_to(mx - 0.1 * r, my + 0.01 * r)
        ctx.curve_to(mx, my + 0.03 * r, mx + 0.08 * r, my, mx + 0.14 * r, my - 0.05 * r)
        stroke(0.05 * r)
    else:
        ctx.move_to(mx - 0.1 * r, my)
        ctx.line_to(mx + 0.1 * r, my)
        stroke(0.05 * r)
    if ch.mustache == "handlebar":
        for side in (-1, 1):
            ctx.move_to(mx, cy + 0.33 * r)
            ctx.curve_to(mx + side * 0.18 * r, cy + 0.2 * r, mx + side * 0.4 * r, cy + 0.28 * r,
                         mx + side * 0.48 * r, cy + 0.16 * r)
            ctx.curve_to(mx + side * 0.42 * r, cy + 0.46 * r, mx + side * 0.15 * r, cy + 0.46 * r, mx, cy + 0.38 * r)
            ctx.close_path()
            src(ctx, OUT)
            ctx.fill()
    elif ch.mustache == "thin":
        for side in (-1, 1):
            ctx.move_to(mx, cy + 0.32 * r)
            ctx.curve_to(mx + side * 0.12 * r, cy + 0.27 * r, mx + side * 0.22 * r, cy + 0.3 * r, mx + side * 0.27 * r, cy + 0.38 * r)
            stroke(0.04 * r)
    if sweat:
        k = (t * 1.5) % 1
        sx, sy = cx + 0.55 * r, cy - 0.35 * r + k * 0.25 * r
        ctx.move_to(sx, sy - 0.12 * r)
        ctx.curve_to(sx + 0.09 * r, sy, sx + 0.07 * r, sy + 0.08 * r, sx, sy + 0.08 * r)
        ctx.curve_to(sx - 0.07 * r, sy + 0.08 * r, sx - 0.09 * r, sy, sx, sy - 0.12 * r)
        src(ctx, hexc("#8fd3ff"))
        ctx.fill_preserve()
        stroke(0.025 * r)


def draw_item3(ctx, item, x, y, r, t):
    if item == "spear":
        ctx.move_to(x, y + 2.6 * r)
        ctx.line_to(x, y - 2.4 * r)
        ctx.set_source_rgb(*hexc("#b07a3a"))
        ctx.set_line_width(0.08 * r)
        ctx.stroke()
        ctx.move_to(x, y - 3.1 * r)
        ctx.curve_to(x + 0.18 * r, y - 2.8 * r, x + 0.14 * r, y - 2.5 * r, x, y - 2.38 * r)
        ctx.curve_to(x - 0.14 * r, y - 2.5 * r, x - 0.18 * r, y - 2.8 * r, x, y - 3.1 * r)
        shade(ctx, hexc("#eef1f5"), hexc("#a5abb8"), y - 3.1 * r, y - 2.4 * r, 0.04 * r)
        ctx.move_to(x, y - 2.36 * r)
        ctx.line_to(x - 0.06 * r, y - 2.0 * r)
        ctx.line_to(x + 0.06 * r, y - 2.0 * r)
        ctx.close_path()
        src(ctx, hexc("#d64a3a"))
        ctx.fill()
    elif item == "shield":
        shield(ctx, x + 0.3 * r, y, 1.05 * r)
    elif item == "stick":
        ctx.move_to(x, y - 0.4 * r)
        ctx.line_to(x + 0.12 * r, y + 2.9 * r)
        ctx.set_source_rgb(*hexc("#8a5a33"))
        ctx.set_line_width(0.07 * r)
        ctx.stroke()
    elif item == "hammer":
        ctx.move_to(x, y)
        ctx.line_to(x, y - 0.6 * r)
        ctx.set_source_rgb(*hexc("#8a5a33"))
        ctx.set_line_width(0.07 * r)
        ctx.stroke()
        rrect(ctx, x - 0.2 * r, y - 0.8 * r, 0.4 * r, 0.22 * r, 0.04 * r)
        shade(ctx, hexc("#c8ccd4"), hexc("#80858f"), y - 0.8 * r, y - 0.58 * r, 0.035 * r)
    elif item == "moneybag":
        ellipse(ctx, x, y + 0.22 * r, 0.2 * r, 0.2 * r)
        shade(ctx, hexc("#e8c477"), hexc("#b98a3e"), y, y + 0.42 * r, 0.035 * r)


def shield(ctx, x, y, R, teal="#55c1ba"):
    ctx.new_sub_path()
    ctx.arc(x, y, R, 0, 2 * PI)
    shade(ctx, hexc("#f2c443"), hexc("#c48a1c"), y - R, y + R, 0.06 * R)
    ctx.new_sub_path()
    ctx.arc(x, y, R * 0.86, 0, 2 * PI)
    shade(ctx, lighter(hexc(teal), 0.15), darker(hexc(teal), 0.15), y - R, y + R, 0.04 * R)
    ctx.new_sub_path()
    ctx.arc(x, y, R * 0.62, 0, 2 * PI)
    shade(ctx, hexc("#e9edf2"), hexc("#a5abb8"), y - R, y + R, 0.04 * R)
    for k in range(24):
        a = k * PI / 12
        ctx.move_to(x + math.cos(a) * R * 0.3, y + math.sin(a) * R * 0.3)
        ctx.line_to(x + math.cos(a) * R * 0.6, y + math.sin(a) * R * 0.6)
    ctx.set_source_rgba(0.5, 0.52, 0.58, 0.5)
    ctx.set_line_width(0.015 * R * 4)
    ctx.stroke()
    ctx.new_sub_path()
    ctx.arc(x, y, R * 0.24, 0, 2 * PI)
    shade(ctx, hexc("#ffffff"), hexc("#9aa1ad"), y - R * 0.24, y + R * 0.24, 0.04 * R)

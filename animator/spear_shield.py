"""Story: the blacksmith who sold an unstoppable spear and an unbreakable shield.
Medieval reference style: 2D characters (style3) on a 3D-rendered terrace plate
(render3d/terrace_v2.py, WIDE=1 NOCHARS=1 NOPROPS=1) and painted 2D sets
(medieval.py). Keyframed camera lands on the key word every 2-4 words."""
import math
import sys

import cairo

import medieval as md
from engine import (W, H, clamp, ease, glow, hexc, keyed, label, lerp, lerpc, pop, render, text)
from style3 import Char3, OUT, shield as draw_shield

TOTAL = 52.85
C = (W / 2, H / 2)
PLATE = None


def plate(ctx, path="../output/spear_shield/plates/terrace.png"):
    """Wide 3D render: covers world (-180, -320) .. (900, 1600) at 1 px per world px."""
    global PLATE
    if PLATE is None:
        PLATE = cairo.ImageSurface.create_from_png(path)
    ctx.save()
    ctx.translate(-180, -320)
    ctx.set_source_surface(PLATE, 0, 0)
    ctx.paint()
    ctx.restore()


KR = Char3("#e8452f", cape="#a8424a", crown="gold", beard="goatee", legs=2.75, torso=2.05)
KT = Char3("#2fb3a8", cape="#25807d", crown="silver", beard="bib", legs=2.75, torso=2.05)
SM = Char3("#8d8f97", outfit="tunic", apron="#d8913a", mustache="handlebar", legs=2.0, torso=2.0)
MSG_R = Char3("#d9534a", outfit="tunic", legs=2.1, torso=1.8, belt="#6b4a2a")
MSG_T = Char3("#3aa6a0", outfit="tunic", legs=2.1, torso=1.8, belt="#6b4a2a")


def head_y(feet, s, ch):
    """Screen y of a Char3 head centre (for camera keys)."""
    r = 64 * s
    return feet - (ch.legs + ch.torso + 0.62) * r


def tint(ctx, rgb, a):
    if a > 0:
        ctx.set_source_rgba(*rgb, a)
        ctx.rectangle(-3000, -5000, 7000, 10000)
        ctx.fill()


def spear_h(ctx, x, y, length, s=1.0, ang=0.0, glow_a=0.0):
    """A big spear drawn on its own (pointing right at ang=0)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    if glow_a:
        glow(ctx, length, 0, 120 * s, (1, 0.9, 0.5), glow_a)
    ctx.move_to(0, 0)
    ctx.line_to(length - 60 * s, 0)
    ctx.set_source_rgb(*hexc("#b07a3a"))
    ctx.set_line_width(14 * s)
    ctx.stroke()
    ctx.move_to(length + 30 * s, 0)
    ctx.curve_to(length - 10 * s, -26 * s, length - 50 * s, -20 * s, length - 70 * s, 0)
    ctx.curve_to(length - 50 * s, 20 * s, length - 10 * s, 26 * s, length + 30 * s, 0)
    md.shade(ctx, hexc("#f2f4f8"), hexc("#a5abb8"), -26 * s, 26 * s, 4 * s)
    ctx.restore()


# ---------------------------------------------------------------- terrace (day / night)
def terrace_base(ctx, T, night=0.0):
    plate(ctx)
    if night:
        tint(ctx, (0.05, 0.08, 0.25), 0.62 * night)
        glow(ctx, 600, 150, 160, (0.85, 0.9, 1.0), 0.35 * night)
        ctx.new_sub_path()
        ctx.arc(600, 150, 34, 0, 2 * math.pi)
        ctx.set_source_rgba(0.97, 0.95, 0.85, night)
        ctx.fill()


def shadows(ctx, items, night=0.0):
    for x, y, w in items:
        md.cast_shadow(ctx, x, y, w, 420, dx=0.75, dy=0.45, a=0.3 * (1 - 0.6 * night))


def s_hook(ctx, t, d):
    T = t
    terrace_base(ctx, T)
    shadows(ctx, ((150, 1010, 170), (380, 960, 160), (610, 1010, 170)))
    md.barrel(ctx, 505, 930, 1.25)
    has_spear = T > 1.25
    has_shield = T > 4.6
    SM.draw(ctx, 380, 960, 1.45, keyed(T, [(0, "smirk"), (2.3, "grin"), (5.4, "smug")]), T,
            arms=("show" if 0.6 < T < 1.3 else "down", "show" if 4.0 < T < 4.7 else "down"), bob=0.6, shadow=False)
    KR.draw(ctx, 150, 1010, 1.45, keyed(T, [(0, "neutral"), (1.3, "grin"), (5.6, "angry")]), T,
            arms=("belly", "spear"), item="spear" if has_spear else None, bob=0.5, shadow=False)
    KT.draw(ctx, 610, 1010, 1.45, keyed(T, [(0, "neutral"), (4.7, "smirk"), (5.8, "cold")]), T,
            arms=("hold", "hip"), item="shield" if has_shield else None, item_hand=0, bob=0.5, shadow=False)
    if 2.4 < T < 3.4:  # "break through anything": the spear tip flashes
        glow(ctx, 237, 360, 90, (1, 0.95, 0.6), 0.7 * math.sin((T - 2.4) * math.pi))
    md.anvil(ctx, 300, 1190, 1.25)
    md.round_table(ctx, 380, 1390, 1.0)


def s_years(ctx, t, d):
    T = 7.0 + t
    terrace_base(ctx, T)
    k = ease((T - 7.4) / 1.5)
    n = max(1, int(round(lerp(1, 100, k))))
    md.years_sign(ctx, 40, 1080, 1.05, f"{n:03d}")
    for x, col in ((110, "#e8574a"), (330, "#f2c443"), (560, "#ffffff")):
        md.helmet_flower(ctx, x, 1215, 0.95, col)


def s_proud(ctx, t, d):
    T = 9.4 + t
    terrace_base(ctx, T)
    shadows(ctx, ((190, 1010, 170), (560, 1010, 170)))
    KR.draw(ctx, 190, 1010, 1.45, keyed(T, [(0, "smug"), (11.0, "grin")]), T, arms=("hip", "spear"),
            item="spear", bob=0.7, shadow=False)
    KT.draw(ctx, 560, 1010, 1.45, keyed(T, [(0, "smug"), (11.8, "grin")]), T, arms=("hold", "hip"),
            item="shield", item_hand=0, bob=0.7, shadow=False)
    md.round_table(ctx, 380, 1390, 1.0)


# ---------------------------------------------------------------- battlefield
def s_aerial(ctx, t, d):
    md.river_aerial(ctx, 13.3 + t, bridge_y=900)


def s_field(ctx, t, d):
    """Low ground angle: two armies facing across the field, kings in front.
    Covers 'one king holding the spear' through 'two pieces of metal' (15.9-26.75)."""
    T = 15.9 + t
    cyc = clamp((T - 21.75) / 1.25)  # "an entire week passed": quick day/night cycles
    night = 0.5 - 0.5 * math.cos(cyc * 2 * math.pi * 3) if 0 < cyc < 1 else 0.0
    md.sky(ctx, -900, 640, top="#5f88d0" if not night else "#1d2457", bottom="#a9cdf3")
    tint(ctx, (0.05, 0.08, 0.25), 0.6 * night)
    for x, y, s in ((150, 220, 1.4), (560, 160, 1.2), (900, 300, 1.0)):
        md.cloud(ctx, x, y, s, T)
    md.castle(ctx, 120, 600, 0.35, md.RED)
    md.castle(ctx, 920, 600, 0.35, md.TEAL)
    md.field_ground(ctx, 600, 525, y_bottom=1700)
    md.army_rows(ctx, 330, 615, -150, 900, rows=16, side=md.RED, s_near=0.55, t=T)
    md.army_rows(ctx, 720, 615, 1200, 900, rows=16, side=md.TEAL, s_near=0.55, t=T)
    tired = T > 23.0
    KR.draw(ctx, 260, 1060, 1.3, "tired" if tired else keyed(T, [(0, "smug"), (19.6, "worried")]), T,
            arms=("belly", "spear"), item="spear", bob=0.4)
    KT.draw(ctx, 790, 1060, 1.3, "tired" if tired else keyed(T, [(0, "smug"), (19.8, "worried")]), T,
            arms=("hold", "hip"), item="shield", item_hand=0, bob=0.4)
    tint(ctx, (0.05, 0.08, 0.25), 0.35 * night)
    md.flowers_foreground(ctx, 1350, T, x0=-300, x1=1100)


# ---------------------------------------------------------------- night: messengers
def s_night(ctx, t, d):
    T = 26.75 + t
    terrace_base(ctx, T, night=1.0)
    glow(ctx, 380, 760, 300, (1, 0.7, 0.35), 0.45)  # forge glow
    md.anvil(ctx, 380, 1180, 1.2, spark_t=None)
    expr = keyed(T, [(0, "tired"), (29.5, "shock"), (30.4, "worried"), (33.9, "smirk"), (36.0, "grin")])
    SM.draw(ctx, 380, 960, 1.45, expr, T, arms=("hip", "hip") if T > 33.8 else ("down", "down"), bob=0.6, shadow=False)
    xr = lerp(-120, 200, ease((T - 28.0) / 1.4))
    xt = lerp(880, 560, ease((T - 28.2) / 1.4))
    walking = 28.0 < T < 29.6
    for ch, x, lk in ((MSG_R, xr, 0.6), (MSG_T, xt, -0.6)):
        ch.draw(ctx, x, 1060, 1.15, keyed(T, [(0, "worried"), (36.2, "shock")]), T, pose="walk" if walking else "stand",
                walk_phase=T * 2.2, arms=("hold", "hold"), look=lk, bob=0.5)
    if 30.3 < T < 33.6:  # same question from both sides
        for x in (200, 560):
            label(ctx, "?", x, 640, 70, hexc("#fff4dc"), fg=OUT, scale=pop(T - 30.4), tilt=0.0)
    if 32.4 < T < 33.8:
        label(ctx, "WHICH ONE WORKS?", 380, 330, 40, hexc("#f2c443"), fg=OUT, scale=pop(T - 32.45), tilt=-0.04)
    if T > 36.1:
        label(ctx, "FIGHT AND FIND OUT", 380, 330, 40, hexc("#e8574a"), scale=pop(T - 36.15), tilt=0.04)


# ---------------------------------------------------------------- the paradox
def s_paradox(ctx, t, d):
    T = 37.4 + t
    g = cairo.LinearGradient(0, -400, 0, 1700)
    g.add_color_stop_rgb(0, *hexc("#1c2550"))
    g.add_color_stop_rgb(1, *hexc("#3b2f6b"))
    ctx.set_source(g)
    ctx.paint()
    glow(ctx, 380, 600, 520, (1, 0.8, 0.45), 0.25)
    hit = ease((T - 41.6) / 0.35)
    sx = lerp(-60, 130, ease((T - 38.0) / 1.0)) + 140 * hit
    spear_h(ctx, sx, 640, 380, 1.0, glow_a=0.6 if 38.5 < T < 40.0 else 0.0)
    if 40.3 < T < 41.7:
        glow(ctx, 560, 640, 220, (0.6, 0.95, 1.0), 0.5)
    draw_shield(ctx, 560, 640, 150)
    if T > 41.9:  # they cannot both be real
        k = T - 41.9
        for a in range(10):
            ang = a * math.pi / 5
            ln = 140 * min(1, k * 4)
            ctx.move_to(520 + math.cos(ang) * 20, 640 + math.sin(ang) * 20)
            ctx.line_to(520 + math.cos(ang) * ln, 640 + math.sin(ang) * ln)
        ctx.set_source_rgba(1, 0.9, 0.5, max(0, 1 - k))
        ctx.set_line_width(6)
        ctx.stroke()
        label(ctx, "?!", 380, 380, 110, hexc("#f2c443"), fg=OUT, scale=pop(k - 0.15), tilt=0.06)


# ---------------------------------------------------------------- ordinary iron, nervous kings
def s_iron(ctx, t, d):
    T = 43.1 + t
    terrace_base(ctx, T)
    shadows(ctx, ((380, 960, 160),))
    hammering = T < 46.0
    SM.draw(ctx, 380, 960, 1.45, keyed(T, [(0, "smirk"), (45.4, "smug")]), T,
            arms=("down", "hammer") if hammering else ("hip", "hip"), item="hammer" if hammering else None, bob=0.6, shadow=False)
    md.anvil(ctx, 300, 1190, 1.25, spark_t=((T * 2.2) % 1) if hammering else None)
    for k in range(3):  # plain iron bars on the anvil
        ctx.rectangle(255 + k * 22, 985 - k * 4, 110, 12)
        ctx.set_source_rgb(*hexc("#8a8f99"))
        ctx.fill_preserve()
        ctx.set_source_rgb(*OUT)
        ctx.set_line_width(3)
        ctx.stroke()
    if T > 45.0:
        label(ctx, "ORDINARY IRON", 330, 1080, 40, hexc("#c9ced8"), fg=OUT, scale=pop(T - 45.05), tilt=-0.05)
    if T > 46.1:  # both kings peek in, sweating
        xr = lerp(-160, 60, ease((T - 46.1) / 0.6))
        xt = lerp(880, 680, ease((T - 46.2) / 0.6))
        KR.draw(ctx, xr, 1040, 1.45, "worried", T, arms=("belly", "spear"), item="spear", sweat=True, shake=0.6, shadow=False)
        KT.draw(ctx, xt, 1040, 1.45, "worried", T, arms=("hold", "hip"), item="shield", item_hand=0, sweat=True, shake=0.6, shadow=False)


def s_end(ctx, t, d):
    T = 48.95 + t
    terrace_base(ctx, T)
    md.years_sign(ctx, 40, 1080, 1.05, "100")
    if T > 50.4:
        label(ctx, "PEACE", 255, 700, 70, hexc("#7cc08a"), fg=OUT, scale=pop(T - 50.45), tilt=-0.08)
    SM.draw(ctx, 590, 1120, 1.3, keyed(T, [(0, "smug"), (51.4, "grin")]), T, arms=("bags", "bags"), bob=0.8)
    for x, col in ((110, "#e8574a"), (330, "#f2c443")):
        md.helmet_flower(ctx, x, 1225, 0.95, col)


SHOTS = [
    dict(start=0.0, draw=s_hook, dof=2, keys=[
        (0.13, 2.0, (380, 560)),                          # "A blacksmith"
        (1.70, 1.7, (200, 600), 0.5),                     # "sold one king a spear"
        (2.79, 3.0, (240, 390), 0.4),                     # "break through anything"
        (4.36, 1.7, (560, 600), 0.5),                     # "his greatest enemy"
        (5.30, 2.4, (600, 690), 0.45),                    # "a shield"
        (6.40, 1.0, (380, 700), 0.6)]),                   # "nothing in the world could break"
    dict(start=7.0, draw=s_years, dof=2, keys=[
        (7.0, 1.15, (360, 700)), (8.61, 1.8, (290, 690), 0.5),  # "a hundred years"
        (9.2, 1.4, (330, 1000), 0.35)]),                  # helmets with flowers
    dict(start=9.4, draw=s_proud, dof=2, keys=[
        (9.88, 1.25, (380, 720)), (11.14, 2.0, (200, 560), 0.5),  # "finally"
        (11.93, 2.0, (560, 560), 0.45),                   # "the weapon"
        (12.90, 1.1, (380, 700), 0.45)]),                 # "to win the war"
    dict(start=13.3, draw=s_aerial, keys=[
        (13.38, 0.95, (360, 520)), (15.18, 1.35, (360, 760), 0.9)]),  # "marched onto the same battlefield"
    dict(start=15.9, draw=s_field, dof=2, keys=[
        (15.9, 1.0, (525, 700)), (16.89, 1.6, (280, 640), 0.5),       # "one king holding the spear"
        (18.38, 1.6, (770, 640), 0.5),                    # "the other carrying the shield"
        (20.12, 0.85, (525, 640), 0.6),                   # "something strange happened"
        (21.15, 1.5, (525, 700), 0.4),                    # "Nobody attacked."
        (22.61, 0.85, (525, 560), 0.5),                   # "an entire week passed"
        (23.92, 1.5, (180, 760), 0.5),                    # "10,000 soldiers"
        (24.79, 1.5, (870, 760), 0.5),                    # "standing around"
        (26.37, 1.3, (560, 620), 0.5)]),                  # "two pieces of metal"
    dict(start=26.75, draw=s_night, dof=2, keys=[
        (27.10, 1.0, (380, 700)), (28.73, 1.5, (220, 760), 0.5),     # "secretly sent messengers"
        (29.53, 1.9, (380, 560), 0.45),                   # "to the blacksmith"
        (31.26, 1.2, (380, 700), 0.45),                   # "the same question"
        (33.00, 1.5, (380, 520), 0.45),                   # "which weapon actually works?"
        (34.30, 2.0, (380, 560), 0.4),                    # "the blacksmith gave them"
        (36.14, 1.15, (380, 560), 0.4),                   # "fight and you'll find out"
        (37.10, 1.1, (380, 700), 0.35)]),
    dict(start=37.4, draw=s_paradox, keys=[
        (37.43, 1.0, C), (38.61, 1.5, (330, 640), 0.45),  # "a spear that can pierce"
        (40.41, 1.5, (520, 640), 0.45),                   # "a shield that can never be pierced"
        (42.22, 1.8, (450, 600), 0.4)]),                  # "cannot both be real"
    dict(start=43.1, draw=s_iron, dof=2, keys=[
        (43.43, 1.6, (340, 640)), (45.04, 1.6, (340, 1040), 0.45),   # "ordinary iron"
        (46.55, 1.15, (380, 700), 0.45),                  # "neither king"
        (47.50, 1.9, (90, 560), 0.4),                     # "would risk"
        (48.28, 1.9, (650, 560), 0.4)]),                  # "the first to test them"
    dict(start=48.95, draw=s_end, dof=2, keys=[
        (49.54, 1.2, (360, 760)), (50.43, 1.9, (250, 680), 0.45),    # "a hundred years"
        (51.57, 1.7, (590, 720), 0.45),                   # "without a single battle"
        (52.6, 1.0, (380, 700), 0.6)]),
]
for k, s in enumerate(SHOTS):
    s["end"] = SHOTS[k + 1]["start"] if k + 1 < len(SHOTS) else TOTAL

SFX = [
    (0.2, "bell.wav", 0.3), (1.3, "pop.wav", 0.6), (2.6, "sparkle.wav", 0.7), (4.7, "pop.wav", 0.6),
    (5.5, "thud.wav", 0.6), (6.4, "sting_soft.wav", 0.6),
    *[(7.4 + k * 0.1, "tick.wav", 0.4) for k in range(15)], (8.95, "thud.wav", 0.7),
    (11.2, "sparkle.wav", 0.5), (12.0, "sparkle.wav", 0.5),
    *[(13.5 + k * 0.45, "step.wav", 0.5) for k in range(5)],
    (19.6, "sting_soft.wav", 0.6), (21.2, "murmur.wav", 0.3),
    *[(21.8 + k * 0.42, "tick.wav", 0.5) for k in range(3)],
    (26.3, "pop.wav", 0.5),
    *[(28.0 + k * 0.4, "step.wav", 0.35) for k in range(4)],
    (29.5, "boing.wav", 0.5), (30.4, "pop.wav", 0.6), (32.45, "pop.wav", 0.7),
    (36.15, "sting.wav", 0.7),
    (38.6, "sparkle.wav", 0.6), (40.4, "sparkle.wav", 0.6), (41.85, "thud.wav", 0.9), (41.9, "sting_low.wav", 0.6),
    *[(43.3 + k * 0.45, "coin.wav", 0.4) for k in range(6)],
    (45.05, "pop.wav", 0.6), (46.5, "boing.wav", 0.4),
    (50.45, "bell.wav", 0.6), (50.5, "sparkle.wav", 0.6),
    *[(51.4 + k * 0.3, "coin.wav", 0.5) for k in range(4)],
]

if __name__ == "__main__":
    import json
    import engine
    engine.LIPSYNC = False
    json.dump([{"time": round(t, 3), "file": f, "volume": v} for t, f, v in sorted(SFX)],
              open(sys.argv[2], "w"), indent=1)
    render(SHOTS, TOTAL, sys.argv[1], grain=4)

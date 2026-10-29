"""Story: mom allows only 10 seconds of the block game; you speedrun a whole game in them.
Office/home style (style2 characters, home.py/arcade.py/speed.py sets). One literal visual per
phrase, an on-screen timer that counts down at every spoken 'Second N', ~1 SFX per second,
characters inside the Shorts safe zone (safezone.fit). The last shot returns to the first
scene so the Short loops ("comment loop if you watched this more than once")."""
import math
import sys

import home as hm
import office as of
import speed as sp
from arcade import hand, red_x
from engine import W, H, clamp, ease, glow, hexc, keyed, label, lerp, pop, render, text
from style2 import Char2, OUT

TOTAL = 53.11
C = (W / 2, H / 2)

KID = Char2("#4fb3a9", hair="bowl", hair_col="#8a4a20", outfit="shirt")
KID_SH = Char2("#4fb3a9", hair="bowl", hair_col="#8a4a20", outfit="shirt", shades=True)
MOM = Char2("#9d7fd6", hair="side", hair_col="#6d381c", outfit="apron")
RED, GOLD = "#e8574a", "#f2b84b"


def tint(ctx, rgb, a):
    if a > 0:
        ctx.set_source_rgba(*rgb, a)
        ctx.rectangle(-3000, -5000, 7000, 10000)
        ctx.fill()


def mom(ctx, x, y, s, expr, T, **kw):
    r = 64 * s
    ctx.new_sub_path()
    ctx.arc(x, y - 4.75 * r, 0.4 * r, 0, 2 * math.pi)
    hm._shade_fill(ctx, hexc("#8a4a20"), hexc("#6d381c"), y - 5.2 * r, y - 4.4 * r, 0.075 * r)
    MOM.draw(ctx, x, y, s, expr, T, **kw)


def you(ctx, x, y, s, T, **kw):
    """The blocky game avatar = you."""
    hm.avatar(ctx, x, y, s, shirt=RED, pants="#2b45a6", hair="curly", t=T, **kw)


def kid_pc(ctx, T, expr, night=0.0, screen="game", arms=("down", "down"), pc_on=1.0, s=1.1, ch=None):
    hm.bedroom(ctx, T, night=0.0)
    of.desk(ctx, 520, 960, 340)
    hm.pc(ctx, 520, 940, 0.9, T, screen=screen, on=pc_on)
    of.chair(ctx, 250, 1180, 1.05, col=RED)
    (ch or KID).draw(ctx, 250, 1180, s, expr, T, pose="sit", arms=arms, look=0.5)
    tint(ctx, (0.04, 0.05, 0.18), 0.55 * night)
    if night and pc_on:
        glow(ctx, 520, 800, 380, (0.5, 0.75, 1), 0.35)


def ghosts(ctx, fn, n=4, step=70, a=0.45):
    """Motion-trail copies behind a fast mover; fn(ctx, dx) draws the mover shifted by dx."""
    for i in range(n, 0, -1):
        ctx.push_group()
        fn(ctx, -i * step)
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(a * (1 - i / (n + 1)))
    fn(ctx, 0)


# ---------------------------------------------------------------- 0.0 hook
def s_hook(ctx, t, d, T0=0.0):
    T = T0 + t
    kid_pc(ctx, T, "happy", arms=("hold", "hold"))
    mom(ctx, 580, 1250, 1.1, keyed(T, [(0, "smirk"), (1.0, "cold")]), T, arms=("down", "point"))
    if T0 == 0.0:
        label(ctx, "MOM:", 560, 540, 40, hexc("#9d7fd6"), scale=pop(T - 0.43), tilt=0.06)


def s_ten(ctx, t, d):
    T = 1.51 + t
    sp.burst_bg(ctx, T)
    k = clamp((T - 1.51) / 0.8)
    sc = pop(T - 1.55)
    if sc > 0.02:
        ctx.save()
        ctx.translate(360, 640)
        ctx.scale(sc, sc)
        ctx.translate(-360, -640)
        sp.stopwatch(ctx, 360, 640, 230, 1 - 0.1 * k, "10", T)
        ctx.restore()
    label(ctx, "ONLY 10 SECONDS", 360, 330, 44, hexc("#e8574a"), scale=pop(T - 1.81), tilt=-0.05)


def s_play(ctx, t, d):
    T = 2.32 + t
    hm.bedroom(ctx, T)
    of.desk(ctx, 360, 1160, 700)
    hm.pc(ctx, 360, 1130, 1.9, T)
    label(ctx, "PLAY!", 360, 360, 70, hexc("#4fd16a"), scale=pop(T - 2.52), tilt=-0.05)
    k = ease((T - 2.6) / 0.35)
    hm.cursor(ctx, lerp(560, 400, k), lerp(900, 760, k), 1.5, click=1.0 if 2.95 < T < 3.1 else 0.0)


def s_just(ctx, t, d):
    T = 3.22 + t
    sp.dark_bg(ctx, "#3a0f1f", "#1c1f33")
    frac = 1 - clamp((T - 3.46) / 0.8) * 0.9
    n = max(1, int(math.ceil(10 * frac)))
    sp.stopwatch(ctx, 360, 640, 230, frac, str(n), T, num_col="#d63c3c")
    label(ctx, "JUST 10!", 360, 330, 56, hexc("#ffd84a"), fg=OUT, scale=pop(T - 3.46), tilt=-0.05)


def s_bed(ctx, t, d):
    T = 4.27 + t
    hm.bedroom(ctx, T, night=0.6)
    hm.bed(ctx, 560, 1150, 1.0, blanket="#4f8bff")
    walk = ease((T - 4.27) / 0.8)
    KID.draw(ctx, lerp(260, 470, walk), 1250, 1.15, "sad", T, pose="walk" if walk < 1 else "stand",
             walk_phase=T * 2, look=0.4)
    mom(ctx, 130, 1250, 1.2, "cold", T, arms=("down", "point"))
    if T > 4.91:
        label(ctx, "BED.", 360, 420, 70, hexc("#9d7fd6"), scale=pop(T - 4.91), tilt=0.05)


def s_shock(ctx, t, d):
    T = 5.23 + t
    sp.burst_bg(ctx, T, "#ffd0c0", "#e8433a")
    sp.speed_lines(ctx, T, 360, 700, a=0.5)
    KID.draw(ctx, 360, 1400, 1.9, "shock", T, arms=("up", "up"))
    label(ctx, "10 SECONDS?!", 360, 330, 56, hexc("#ffd84a"), fg=OUT, scale=pop(T - 5.75), tilt=-0.06)


def s_imposs(ctx, t, d):
    T = 6.46 + t
    hm.bedroom(ctx, T)
    of.wall_clock(ctx, 360, 520, 170, 12, 0)
    red_x(ctx, 360, 520, 150, (T - 6.55) / 0.3)
    KID.draw(ctx, 360, 1300, 1.4, keyed(T, [(0, "worried"), (6.9, "sad")]), T, arms=("up", "up"))
    label(ctx, "IMPOSSIBLE!", 360, 800, 56, hexc("#e8323a"), scale=pop(T - 6.68), tilt=0.05)


def s_cool(ctx, t, d):
    T = 7.47 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#ff9b3a")
    KID_SH.draw(ctx, 360, 1380, 1.7, keyed(T, [(0, "smirk"), (8.1, "grin")]), T, arms=("hip", "hip"))
    label(ctx, "NOT IF YOU'RE...", 360, 360, 44, hexc("#4f8bff"), scale=pop(T - 7.85), tilt=-0.05)


def s_speed(ctx, t, d):
    T = 8.88 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 1000)
    sp.speed_lines(ctx, T, 360, 700, a=0.55)
    ghosts(ctx, lambda c, dx: you(c, 420 + dx, 1000, 1.6, T, walk=T * 3.5, expr="grin"), n=5, step=60)
    label(ctx, "SPEEDRUNNER", 360, 330, 54, hexc("#ffd84a"), fg=OUT, scale=pop(T - 8.88), tilt=-0.05)


# ---------------------------------------------------------------- obby
def s_enter(ctx, t, d):
    T = 9.86 + t
    pl = sp.course(ctx, T)
    hm.box(ctx, 40, 360, 440, 120, "#ffffff", "#e8e8f0", r=14)   # OBBY sign
    text(ctx, "OBBY", 260, 420, 80, hexc("#4fd16a"), outline=True)
    you(ctx, 140, pl[0][1], 1.2, T, expr="grin")
    label(ctx, "SECOND 10", 360, 560, 50, hexc("#e8574a"), scale=pop(T - 9.86), tilt=-0.05)


def s_stages(ctx, t, d):
    T = 11.67 + t
    pl = sp.course(ctx, T, n=22)


def stages_overlay(ctx, t, d):
    T = 11.67 + t
    make_hud(11.67)(ctx, t, d)
    n = int(lerp(1, 100, ease((T - 11.67) / 1.0)))
    label(ctx, f"STAGE {n}/100", 360, 560, 52, hexc("#4f8bff"), scale=pop(T - 11.7), tilt=-0.04)


def s_jump(ctx, t, d):
    T = 12.75 + t
    pl = sp.course(ctx, T, n=22, numbers=False)
    p = clamp((T - 12.75) / 1.35)
    x = lerp(150, 2900, ease(p))
    y = lerp(900, 800, p) - math.sin(math.pi * p) * 850
    ctx.save()
    ctx.translate(x, y - 100)
    ctx.rotate(p * 2 * math.pi * 1.0)
    ctx.translate(-x, -(y - 100))
    ghosts(ctx, lambda c, dx: you(c, x + dx, y, 1.3, T, expr="grin", jump=0), n=3, step=80, a=0.4)
    ctx.restore()
    label(ctx, "ONE JUMP!", x, y - 420, 44, hexc("#ffd84a"), fg=OUT, scale=pop(T - 13.78), tilt=-0.05)


def s_finish(ctx, t, d):
    T = 14.20 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 960)
    sp.finish(ctx, 420, 960, 1.15, T, confetti=14.2)
    you(ctx, 260, 960, 1.5, T, expr="happy", wave=True, jump=max(0, math.sin((T - 14.2) * 9)) * 30)
    label(ctx, "FINISH!", 360, 560, 76, hexc("#4fd16a"), fg=OUT, scale=pop(T - 14.25), tilt=-0.05)


# ---------------------------------------------------------------- noob king
def s_arena(ctx, t, d):
    T = 15.05 + t
    sp.arena(ctx, T, crack=clamp((T - 15.05) / 0.8))
    you(ctx, 250, 1050, 1.3, T, expr="shock")
    label(ctx, "SECOND 9", 400, 560, 56, hexc("#e8574a"), scale=pop(T - 15.05), tilt=-0.05)


def king(ctx, x, y, s, T, expr="angry"):
    sp.cape(ctx, x, y, s, T)
    hm.avatar(ctx, x, y, s, shirt="#f2b84b", pants="#8a4a20", expr=expr, t=T)
    hm.crown(ctx, x, y - 218 * s, 0.55 * s)


def s_king(ctx, t, d):
    T = 16.03 + t
    sp.arena(ctx, T, crack=1.0)
    rise = ease((T - 16.03) / 0.9)
    glow(ctx, 450, 900, 420, (1, 0.7, 0.3), 0.5 * rise)
    king(ctx, 450, lerp(1500, 1080, rise), 2.0, T)
    you(ctx, 150, 1080, 1.0, T, expr="shock")
    if T > 16.34:
        label(ctx, "NOOB KING", 360, 560, 60, hexc("#ffd84a"), fg=OUT, scale=pop(T - 16.34), tilt=-0.05)


def s_boom(ctx, t, d):
    T = 17.16 + t
    sp.arena(ctx, T, crack=1.0)
    king(ctx, 520, 1100, 1.9, T, expr="shock")
    k = (T - 17.16) / 0.55
    you(ctx, lerp(40, 190, ease(k * 3)), 1100, 1.9, T, expr="angry")
    sp.shockwave(ctx, 330, 800, k)
    sp.starburst(ctx, 360, 820, 230, k)
    ctx.set_source_rgba(1, 1, 1, max(0.0, 0.7 - k * 3))
    ctx.rectangle(-500, -500, 2000, 2500)
    ctx.fill()
    label(ctx, "BOOM!", 360, 560, 90, hexc("#ff4f5a"), fg=OUT, scale=pop(T - 17.2), tilt=-0.08)


def s_hit(ctx, t, d):
    T = 17.72 + t
    sp.arena(ctx, T, crack=1.0)
    p = clamp((T - 17.72) / 0.6)
    sp.speed_lines(ctx, T, 360, 700, a=0.4)
    ctx.save()
    ctx.translate(lerp(420, 800, ease(p)), 1000 - math.sin(p * math.pi) * 220)
    ctx.rotate(p * 2.2)
    king(ctx, 0, 100, 1.9, T, expr="shock")
    ctx.restore()
    you(ctx, 170, 1080, 1.9, T, expr="angry", wave=False)
    label(ctx, "ONE HIT!", 360, 560, 66, hexc("#ffd84a"), fg=OUT, scale=pop(T - 17.99), tilt=-0.05)


def s_ko(ctx, t, d):
    T = 18.33 + t
    sp.arena(ctx, T, crack=1.0)
    ctx.save()
    ctx.translate(480, 1180)
    ctx.rotate(-math.pi / 2 + 0.05)
    king(ctx, 0, 0, 1.6, T, expr="sad")
    ctx.restore()
    sp.stars_around(ctx, 300, 900, 120, T)
    you(ctx, 170, 1100, 1.5, T, expr="happy", wave=True)
    label(ctx, "K.O.", 360, 560, 110, hexc("#ff4f5a"), fg=OUT, scale=pop(T - 18.76), tilt=-0.08)


def s_drop(ctx, t, d):
    T = 19.42 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#f2a65a")
    hm.coin_rain(ctx, T, n=26, seed=4)
    you(ctx, 360, 1080, 1.7, T, expr="happy", wave=True)
    label(ctx, "SECOND 8", 360, 560, 54, hexc("#e8574a"), scale=pop(T - 19.42), tilt=-0.05)
    if T > 20.27:
        label(ctx, "HE DROPS...", 360, 560, 40, hexc("#4f8bff"), scale=pop(T - 20.27), tilt=0.05)


def s_billion(ctx, t, d):
    T = 20.60 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#e0a93a")
    n = int(lerp(0, 1_000_000_000, ease((T - 20.6) / 0.8)))
    hm.coin_rain(ctx, T, n=30, seed=6)
    hm.robux_coin(ctx, 360, 720, 2.0, spin=T * 2)
    text(ctx, f"{n:,}", 360, 930, 58, hexc("#ffffff"), outline=True)
    label(ctx, "1 BILLION R$", 360, 560, 52, hexc("#e8574a"), scale=pop(T - 21.0), tilt=-0.05)
    you(ctx, 360, 1330, 1.0, T, expr="shock")


# ---------------------------------------------------------------- shop
def s_shop(ctx, t, d):
    T = 22.06 + t
    sp.shop_wall(ctx, T)
    hm.box(ctx, 130, 300, 460, 100, "#ffd84a", "#e0a93a", r=16)
    text(ctx, "SHOP", 360, 352, 70, hexc("#5a3a10"), outline=False)
    you(ctx, 360, 1160, 1.6, T, expr="grin", wave=True)
    label(ctx, "SECOND 7", 360, 560, 46, hexc("#e8574a"), scale=pop(T - 22.06), tilt=-0.05)


def s_buy(ctx, t, d):
    T = 23.09 + t
    sp.shop_wall(ctx, T, bought_at=23.2)
    n = min(24, int((T - 23.09) / 1.98 * 24))
    label(ctx, f"PASSES: {n}", 360, 560, 50, hexc("#4fd16a"), scale=1.0, tilt=0)
    k = (T - 23.09) / 1.98
    hm.cursor(ctx, 120 + 520 * ((k * 3) % 1), 560 + 270 * int(k * 3), 1.2, click=1.0 if (T * 10) % 1 < 0.4 else 0.0)
    you(ctx, 600, 1210, 1.2, T, expr="happy")


def s_toastpass(ctx, t, d):
    T = 25.07 + t
    sp.dark_bg(ctx, "#101018", "#1c1f33")
    glow(ctx, 360, 640, 620, (1, 0.85, 0.4), 0.55)
    hm.box(ctx, 140, 330, 440, 620, "#fff3c0", "#f2c243", r=34, lw=8)
    sp.toaster(ctx, 360, 740, 0.9, T, toast=1.0)
    text(ctx, "GIANT TOASTER", 360, 860, 40, hexc("#8a5a10"), outline=False)
    hm.box(ctx, 220, 880, 280, 60, "#4fd16a", "#2e9c46", r=16)
    text(ctx, "BUY", 360, 912, 42, (1, 1, 1), outline=False)
    sp.sparkles(ctx, T, 360, 640, n=14)
    k = ease((T - 25.3) / 0.4)
    hm.cursor(ctx, lerp(620, 380, k), lerp(1100, 930, k), 1.4, click=1.0 if T > 25.75 else 0.0)


def s_toaster(ctx, t, d):
    T = 25.96 + t
    sp.burst_bg(ctx, T, "#ffe9b0", "#f2a65a")
    if T < 26.58:
        you(ctx, 360, 1000, 1.5, T, expr="shock")
        sp.sparkles(ctx, T, 360, 800, spread=200, n=18, seed=9)
    else:
        k = clamp((T - 26.58) / 0.7)
        glow(ctx, 360, 800, 600 * (1 - k * 0.4), (1, 1, 1), 0.9 * (1 - k))
        sp.toaster(ctx, 360, 1060, 1.5 * ease(k + 0.15), T, toast=1.0, mad=T > 27.37)
        if T > 27.37:
            label(ctx, "GIANT TOASTER", 360, 560, 50, hexc("#e8574a"), scale=pop(T - 27.37), tilt=-0.05)


# ---------------------------------------------------------------- crowd
def crowd(ctx, T, crowns_t=None, rows=3, per=5):
    cols = ["#e8574a", "#4fb3a9", "#f2b84b", "#9d7fd6", "#4f8bff", "#e57373", "#7cc08a"]
    i = 0
    for r in range(rows):
        for c in range(per):
            x = 70 + c * 145 + (r % 2) * 70
            y = 980 + r * 150
            s = 0.8 + r * 0.12
            you_c = cols[(i * 3) % len(cols)]
            hm.avatar(ctx, x, y, s, shirt=you_c, pants="#2b45a6", hair=("curly", None)[i % 2], expr="happy",
                      t=T + i * 0.3, wave=(i % 3 == 0), jump=abs(math.sin(T * 5 + i)) * 14)
            if crowns_t is not None:
                k = ease((T - crowns_t - i * 0.05) / 0.35)
                if k > 0:
                    hm.crown(ctx, x, lerp(-100, y - 216 * s, k), 0.4 * s)
            i += 1


def s_crowd(ctx, t, d):
    T = 28.38 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 940)
    crowd(ctx, T)
    label(ctx, "SECOND 6", 360, 560, 54, hexc("#e8574a"), scale=pop(T - 28.38), tilt=-0.05)
    label(ctx, "EVERYONE", 360, 560, 50, hexc("#4f8bff"), scale=pop(T - 29.29), tilt=0.04)


def s_likesub(ctx, t, d):
    T = 29.76 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 940)
    tint(ctx, (0.1, 0.1, 0.2), 0.3)
    hm.like_button(ctx, 360, 470, 1.4 * pop(T - 29.76), pressed=clamp((T - 30.0) / 0.12))
    hm.subscribe_button(ctx, 360, 720, 1.3 * pop(T - 30.22), pressed=clamp((T - 30.7) / 0.12))
    k = ease((T - 29.9) / 0.3)
    hm.cursor(ctx, lerp(600, 420, k), lerp(1000, 500, k) if T < 30.4 else lerp(500, 760, ease((T - 30.4) / 0.25)),
              1.4, click=1.0 if (30.0 < T < 30.15 or 30.7 < T < 30.85) else 0.0)


def s_crowns(ctx, t, d):
    T = 31.40 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 940)
    crowd(ctx, T, crowns_t=31.4)
    label(ctx, "FREE GOLDEN CROWN", 360, 560, 40, hexc("#ffd84a"), fg=OUT, scale=pop(T - 31.79), tilt=-0.05)
    sp.sparkles(ctx, T, 360, 700, n=14, seed=2)


# ---------------------------------------------------------------- pet
def s_egg(ctx, t, d):
    T = 32.29 + t
    sp.dark_bg(ctx, "#1c1f33", "#3a2a60")
    sp.burst_bg(ctx, T, "#5a4a9a", "#1c1f33", a=0.1)
    crack = clamp((T - 32.7) / 1.2)
    sp.egg(ctx, 360, 1000, 1.25, T, crack=crack, glow_k=crack)
    you(ctx, 120, 1100, 1.0, T, expr="shock")
    label(ctx, "SECOND 5", 360, 560, 54, hexc("#e8574a"), scale=pop(T - 32.29), tilt=-0.05)


def s_pet(ctx, t, d):
    T = 33.93 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#c26bff")
    ctx.set_source_rgba(1, 1, 1, max(0.0, 0.9 - (T - 33.93) * 3))
    ctx.rectangle(-500, -500, 2000, 2500)
    ctx.fill()
    sp.pet(ctx, 360, 1020 - 40 * math.sin(T * 3), 1.15 * pop(T - 33.95), T)
    sp.sparkles(ctx, T, 360, 700, n=18)
    label(ctx, "LEGENDARY!", 360, 560, 62, hexc("#ffd84a"), fg=OUT, scale=pop(T - 33.93), tilt=-0.05)
    you(ctx, 110, 1180, 1.0, T, expr="happy", wave=True)


# ---------------------------------------------------------------- countdown
def s_four(ctx, t, d):
    T = 36.00 + t
    sp.dark_bg(ctx, "#4a0f1f", "#1c1f33")
    ctx.set_source_rgba(1, 0.1, 0.1, 0.12 + 0.1 * math.sin(T * 16))
    ctx.rectangle(-500, -500, 2000, 2500)
    ctx.fill()
    text(ctx, "4", 360, 640, 520 * pop(T - 36.0), hexc("#ffffff"), outline=True)
    you(ctx, 360, 1200, 1.0, T, expr="shock", walk=T * 4)


def s_three(ctx, t, d):
    T = 36.68 + t
    kid_pc(ctx, T, "shock", night=0.3, arms=("up", "up"))
    tint(ctx, (0.8, 0.05, 0.1), 0.18)
    text(ctx, "3", 360, 600, 460 * pop(T - 36.68), hexc("#ff4f5a"), outline=True)


def s_discover(ctx, t, d):
    T = 37.24 + t
    sp.dark_bg(ctx, "#08060f", "#1c1f33")
    k = ease((T - 37.2) / 1.0)
    ax = lerp(120, 330, k)
    you(ctx, ax, 1100, 1.4, T, expr="shock")
    ctx.move_to(ax + 40, 900)   # flashlight beam sweeping right
    ctx.line_to(ax + 900, 700 + 300 * math.sin(T * 2))
    ctx.line_to(ax + 900, 1200 + 300 * math.sin(T * 2))
    ctx.close_path()
    ctx.set_source_rgba(1, 0.95, 0.7, 0.22)
    ctx.fill()
    label(ctx, "SUDDENLY!", 360, 560, 60, hexc("#ffd84a"), fg=OUT, scale=pop(T - 37.24), tilt=-0.05)
    if T > 37.98:
        label(ctx, "!", 520, 620, 90, hexc("#e8574a"), scale=pop(T - 37.98), tilt=0)


def s_button(ctx, t, d):
    T = 38.47 + t
    sp.dark_bg(ctx, "#08060f", "#1c1f33")
    sp.secret_button(ctx, 360, 900, 1.4, T)
    sp.sparkles(ctx, T, 360, 700, n=14, seed=6)
    label(ctx, "SECRET", 360, 560, 70, hexc("#9d7fd6"), fg=OUT, scale=pop(T - 38.47), tilt=-0.06)
    if T > 39.29:
        label(ctx, "EXTRA TIME", 360, 560, 50, hexc("#4fd16a"), fg=OUT, scale=pop(T - 39.29), tilt=0.04)


def s_smash(ctx, t, d):
    T = 40.01 + t
    sp.dark_bg(ctx, "#08060f", "#1c1f33")
    k = (T - 40.01) / 0.7
    sp.secret_button(ctx, 360, 900, 1.4, T, pressed=min(1.0, k * 5))
    sp.shockwave(ctx, 360, 800, k, col=(0.6, 1, 0.7))
    sp.starburst(ctx, 360, 780, 230, k, "#c8ffd0", "#4fd16a")
    ctx.save()
    ctx.translate(360, lerp(-100, 600, ease(k * 4)))
    ctx.rotate(math.pi / 2)
    hand(ctx, 120, 0, 1.6, flip=1, col="#ffdd55")
    ctx.restore()
    label(ctx, "SMASH!", 360, 560, 90, hexc("#4fd16a"), fg=OUT, scale=pop(T - 40.13), tilt=-0.08)


def s_slow(ctx, t, d):
    T = 40.72 + t
    hm.game_sky(ctx)
    hm.baseplate(ctx, 1000)
    tint(ctx, (0.2, 0.35, 0.8), 0.35)
    for i in range(14):   # coins frozen in mid-air, drifting very slowly
        hm.robux_coin(ctx, 60 + i * 48, 300 + (i * 97) % 600 + math.sin(T * 0.6 + i) * 18, 0.6, spin=T * 0.4 + i)
    ph = (T - 40.72) * 0.35
    you(ctx, 360, 900 - math.sin(min(ph, 1) * math.pi) * 260, 1.7, T, expr="happy", wave=True)
    sp.shockwave(ctx, 360, 700, ((T - 40.72) / 1.2) % 1.0, col=(0.7, 0.85, 1), r_max=620)
    label(ctx, "SLOW MOTION", 360, 560, 52, hexc("#4f8bff"), scale=pop(T - 42.08), tilt=-0.05)


def s_momreach(ctx, t, d):
    T = 42.81 + t
    hm.bedroom(ctx, T, night=0.75)
    hm.box(ctx, 360, 760, 360, 30, "#b07a4a", "#8a5a33", r=4)
    hm.router(ctx, 560, 700, 0.9, T, on=1.0)
    of.desk(ctx, 180, 1000, 300)
    of.chair(ctx, 120, 1220, 1.0, col=RED)
    KID_SH.draw(ctx, 110, 1220, 1.0, "grin", T, pose="sit", arms=("hold", "hold"), bob=0.1)
    k = ease((T - 42.81) / 1.2)
    mom(ctx, lerp(150, 430, k), 1330, 1.35, "cold", T, pose="walk" if k < 1 else "stand", walk_phase=T * 0.9,
        arms=("down", "point"), look=0.5, bob=0.4)
    label(ctx, "MOM...", 340, 360, 54, hexc("#9d7fd6"), scale=pop(T - 43.38), tilt=-0.05)


def s_wifi(ctx, t, d):
    T = 44.18 + t
    hm.bedroom(ctx, T, night=0.75)
    hm.box(ctx, 100, 900, 520, 34, "#b07a4a", "#8a5a33", r=4)
    hm.router(ctx, 340, 860, 1.35, T, on=1.0, plug_out=ease((T - 44.7) / 0.5) * 0.0)
    k = ease((T - 44.18) / 0.9)
    hand(ctx, lerp(-200, 330, k), lerp(1060, 1000, k), 1.7, flip=1, col="#e9c9a8")
    label(ctx, "WI-FI!", 360, 560, 72, hexc("#e8323a"), scale=pop(T - 44.73), tilt=0.06)


def s_toolate(ctx, t, d):
    T = 45.43 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#ff7a2a")
    sp.speed_lines(ctx, T, 360, 700, a=0.5)
    KID_SH.draw(ctx, 360, 1400, 1.7, "grin", T, arms=("point", "hip"))
    label(ctx, "TOO LATE!", 360, 560, 82, hexc("#e8323a"), fg=OUT, scale=pop(T - 45.73), tilt=-0.06)


def s_runner(ctx, t, d):
    T = 46.06 + t
    sp.dark_bg(ctx, "#1c1f33", "#4a2a7a")
    sp.burst_bg(ctx, T, "#fff3a8", "#c26bff", a=0.12)
    KID_SH.draw(ctx, 360, 1380, 1.7, "smirk", T, arms=("hip", "hip"))
    sp.sparkles(ctx, T, 360, 700, n=14)
    label(ctx, "SPEEDRUNNER", 360, 560, 56, hexc("#ffd84a"), fg=OUT, scale=pop(T - 46.62), tilt=-0.05)
    hm.crown(ctx, 360, 520, 1.0 * pop(T - 46.7)) if False else None


def s_plus(ctx, t, d):
    T = 47.19 + t
    sp.burst_bg(ctx, T, "#c8ffd0", "#2e9c46")
    k = clamp((T - 47.51) / 0.3)
    txt = "0:03" if k < 0.5 else "0:13"
    sp.digital(ctx, 360, 640, 1.4 * (1 + 0.2 * math.exp(-10 * max(0, T - 47.51))), txt,
               col="#4fd16a" if k > 0.5 else "#ff4f5a", size=100)
    label(ctx, "+10 SECONDS!", 360, 330, 64, hexc("#ffd84a"), fg=OUT, scale=pop(T - 47.51), tilt=-0.05)
    hm.coin_rain(ctx, T, n=14, seed=8)


def s_forceful(ctx, t, d):
    T = 48.38 + t
    hm.bedroom(ctx, T, night=0.0)
    mom(ctx, 360, 1480, 2.0, "shock", T, arms=("up", "up"))
    label(ctx, "?!", 540, 470, 90, hexc("#e8323a"), scale=pop(T - 48.4), tilt=0.1)


def s_what(ctx, t, d):
    T = 49.01 + t
    hm.bedroom(ctx, T)
    mom(ctx, 360, 1700, 2.6, keyed(T, [(0, "shock"), (49.3, "angry")]), T, arms=("hip", "hip"), bob=2.0)
    label(ctx, "WHAT?!", 360, 360, 76, hexc("#e8323a"), fg=OUT, scale=pop(T - 49.05), tilt=-0.05)


def s_again(ctx, t, d):
    T = 49.62 + t
    kid_pc(ctx, T, "grin", arms=("hold", "hold"), ch=KID_SH)
    mom(ctx, 560, 1300, 1.2, "angry", T, arms=("up", "up"), bob=2.0)
    for k in range(3):   # steam
        ph = (T * 1.5 + k / 3) % 1
        text(ctx, "♨", 520 + k * 40, 700 - ph * 150, 50, (1, 1, 1), outline=True)
    label(ctx, "NOT AGAIN!", 360, 360, 64, hexc("#e8323a"), fg=OUT, scale=pop(T - 49.89), tilt=-0.05)


def s_loop(ctx, t, d):
    T = 50.51 + t
    sp.burst_bg(ctx, T, "#fff3a8", "#4f8bff")
    sp.loop_arrow(ctx, 360, 560, 190, T)
    text(ctx, "10", 360, 560, 150, (1, 1, 1), outline=True)
    sp.comment_bubble(ctx, 360, 1000, 0.95 * pop(T - 50.9), ("COMMENT", "LOOP"))
    label(ctx, "WATCHED TWICE?", 360, 300, 40, hexc("#e8574a"), scale=pop(T - 51.46), tilt=-0.05)


def s_end(ctx, t, d):
    s_hook(ctx, t, d, T0=0.0)   # back to the first frame: the Short loops


S = []


def shot(start, draw, keys, **kw):
    S.append(dict(start=start, draw=draw, keys=keys, **kw))


def push(t0, t1, z0, z1, c0, c1):
    return [(t0, z0, c0), (t1, z1, c1, max(0.2, t1 - t0))]


shot(0.0, s_hook, push(0.0, 1.51, 1.0, 1.2, (360, 840), (380, 800)), dof=2)
shot(1.51, s_ten, push(1.51, 2.32, 1.0, 1.2, C, C), shake=(1.55, 8))
shot(2.32, s_play, push(2.32, 3.22, 1.0, 1.3, (360, 800), (400, 760)))
shot(3.22, s_just, push(3.22, 4.27, 1.0, 1.25, C, C), shake=(3.46, 6))
shot(4.27, s_bed, push(4.27, 5.23, 1.0, 1.15, (300, 900), (360, 880)), dof=2)
shot(5.23, s_shock, push(5.23, 6.46, 1.0, 1.3, (360, 820), (360, 760)), shake=(5.75, 10))
shot(6.46, s_imposs, push(6.46, 7.47, 1.0, 1.2, (360, 760), (360, 780)), shake=(6.68, 6))
shot(7.47, s_cool, push(7.47, 8.88, 1.0, 1.2, (360, 880), (360, 800)))
shot(8.88, s_speed, push(8.88, 9.86, 1.0, 1.25, (300, 820), (440, 780)))
shot(9.86, s_enter, push(9.86, 11.67, 1.0, 1.3, (260, 780), (300, 860)), dof=2)
shot(11.67, s_stages, [(11.67, 1.0, (360, 720)), (12.75, 0.85, (1700, 640), 1.0)], blur=False)
shot(12.75, s_jump, [(12.75, 1.0, (260, 800)), (13.4, 0.8, (1500, 520), 0.6), (14.2, 1.0, (2850, 780), 0.5)])
shot(14.20, s_finish, push(14.20, 15.05, 1.0, 1.25, (360, 760), (380, 700)), shake=(14.25, 7))
shot(15.05, s_arena, push(15.05, 16.03, 1.0, 1.15, (360, 800), (360, 780)), shake=(15.05, 10), dof=2)
shot(16.03, s_king, push(16.03, 17.16, 1.0, 1.25, (360, 820), (440, 760)), shake=(16.5, 8))
shot(17.16, s_boom, push(17.16, 17.72, 1.0, 1.15, C, C), shake=(17.16, 18))
shot(17.72, s_hit, push(17.72, 18.33, 1.0, 1.2, (360, 780), (500, 760)), shake=(17.72, 10))
shot(18.33, s_ko, push(18.33, 19.42, 1.0, 1.15, (360, 860), (360, 820)))
shot(19.42, s_drop, push(19.42, 20.60, 1.0, 1.2, (360, 760), (360, 740)))
shot(20.60, s_billion, push(20.60, 22.06, 1.0, 1.25, (360, 760), (360, 700)), shake=(20.7, 5))
shot(22.06, s_shop, push(22.06, 23.09, 1.0, 1.2, (360, 760), (360, 820)))
shot(23.09, s_buy, push(23.09, 25.07, 1.1, 1.0, (260, 640), (460, 880)))
shot(25.07, s_toastpass, push(25.07, 25.96, 1.0, 1.25, (360, 740), (360, 780)))
shot(25.96, s_toaster, [(25.96, 1.0, (360, 860)), (26.69, 1.1, (360, 760), 0.4), (27.37, 0.9, (360, 700), 0.4)],
     shake=(26.58, 14))
shot(28.38, s_crowd, push(28.38, 29.76, 1.0, 1.2, (360, 900), (360, 860)), dof=2)
shot(29.76, s_likesub, push(29.76, 31.40, 1.0, 1.2, C, (360, 640)))
shot(31.40, s_crowns, push(31.40, 32.29, 1.0, 1.25, (360, 860), (360, 820)))
shot(32.29, s_egg, push(32.29, 33.93, 1.0, 1.35, (360, 880), (360, 760)), shake=(33.3, 9))
shot(33.93, s_pet, push(33.93, 36.00, 1.0, 1.3, (360, 840), (360, 700)), dof=2)
shot(36.00, s_four, push(36.00, 36.68, 1.0, 1.2, C, C), shake=(36.0, 9))
shot(36.68, s_three, push(36.68, 37.24, 1.0, 1.25, (360, 700), (360, 640)), shake=(36.68, 10))
shot(37.24, s_discover, push(37.24, 38.47, 1.0, 1.25, (300, 880), (440, 820)))
shot(38.47, s_button, push(38.47, 40.01, 1.0, 1.5, (360, 700), (360, 820)))
shot(40.01, s_smash, push(40.01, 40.72, 1.1, 1.0, (360, 800), (360, 740)), shake=(40.01, 16))
shot(40.72, s_slow, push(40.72, 42.81, 1.0, 1.25, (360, 760), (360, 700)))
shot(42.81, s_momreach, push(42.81, 44.18, 1.0, 1.25, (300, 900), (420, 900)), dof=2)
shot(44.18, s_wifi, push(44.18, 45.43, 1.0, 1.4, (360, 800), (360, 860)), shake=(44.73, 7))
shot(45.43, s_toolate, push(45.43, 46.06, 1.0, 1.2, (360, 860), (360, 800)), shake=(45.73, 9))
shot(46.06, s_runner, push(46.06, 47.19, 1.0, 1.25, (360, 880), (360, 800)))
shot(47.19, s_plus, push(47.19, 48.38, 1.0, 1.3, C, C), shake=(47.51, 9))
shot(48.38, s_forceful, push(48.38, 49.01, 1.0, 1.3, (360, 760), (360, 700)), shake=(48.4, 8))
shot(49.01, s_what, push(49.01, 49.62, 1.1, 1.3, (360, 860), (360, 820)), shake=(49.05, 10))
shot(49.62, s_again, push(49.62, 50.51, 1.0, 1.2, (360, 900), (400, 880)))
shot(50.51, s_loop, push(50.51, 52.2, 1.0, 1.2, C, (360, 700)))
shot(52.2, s_end, push(52.2, TOTAL, 1.2, 1.0, (380, 800), (360, 840)))
SHOTS = S
for k, s in enumerate(SHOTS):
    s["end"] = SHOTS[k + 1]["start"] if k + 1 < len(SHOTS) else TOTAL

# on-screen timer: counts down at every spoken "Second N" (9.86 .. 47.19)
HUD = [(9.86, "0:10", False), (15.05, "0:09", False), (19.42, "0:08", False), (22.06, "0:07", False),
       (28.38, "0:06", False), (32.29, "0:05", False), (36.00, "0:04", True), (36.68, "0:03", True)]


def make_hud(T0):
    def ov(ctx, t, d):
        T = T0 + t
        cur = None
        for ts, txt, urg in HUD:
            if T >= ts:
                cur = (ts, txt, urg)
        if cur and 9.86 <= T < 47.19:
            sp.hud(ctx, cur[1], bump=math.exp(-9 * (T - cur[0])), urgent=cur[2])
    return ov


for s in SHOTS:
    if 9.86 <= s["start"] < 47.19:
        s["top"] = 250   # keep characters and labels below the timer
        s["overlay"] = stages_overlay if s["draw"] is s_stages else make_hud(s["start"])

SFX = [
    (0.45, "pop.wav", 0.7), (1.05, "tick.wav", 0.5), (1.55, "pop.wav", 0.8), (1.8, "tick.wav", 0.5),
    (2.52, "pop.wav", 0.7), (2.95, "tick.wav", 0.8), (3.46, "tick.wav", 0.6), (3.7, "tick.wav", 0.6),
    (3.95, "tick.wav", 0.6), (4.2, "tick.wav", 0.6), (4.91, "pop.wav", 0.7), (5.75, "thud.wav", 0.9),
    (6.2, "boing.wav", 0.5), (6.55, "tick.wav", 0.6), (6.68, "thud.wav", 0.8), (7.85, "pop.wav", 0.7),
    (8.3, "sparkle.wav", 0.5), (8.88, "pop.wav", 0.8), *[(9.0 + k * 0.2, "step.wav", 0.5) for k in range(4)],
    (9.86, "tick.wav", 0.9), (9.9, "pop.wav", 0.6), (11.0, "tick.wav", 0.5),
    *[(11.7 + k * 0.1, "tick.wav", 0.4) for k in range(8)], (12.87, "boing.wav", 0.7), (13.78, "pop.wav", 0.7),
    (14.25, "bell.wav", 0.8), (14.3, "sparkle.wav", 0.7), (15.05, "tick.wav", 0.9), (15.1, "thud.wav", 0.7),
    (15.6, "thud.wav", 0.5), (16.34, "pop.wav", 0.8), (16.6, "sting.wav", 0.7), (17.2, "thud.wav", 1.0),
    (17.25, "pop.wav", 0.8), (17.99, "pop.wav", 0.8), (18.3, "thud.wav", 0.9), (18.76, "pop.wav", 0.8),
    (19.42, "tick.wav", 0.9), (19.6, "coin.wav", 0.6), (19.9, "coin.wav", 0.6), (20.27, "pop.wav", 0.6),
    *[(20.65 + k * 0.1, "coin.wav", 0.45) for k in range(8)], (21.0, "pop.wav", 0.8), (21.5, "sparkle.wav", 0.6),
    (22.06, "tick.wav", 0.9), (22.4, "pop.wav", 0.6), *[(23.2 + k * 0.1, "pop.wav", 0.35) for k in range(12)],
    (24.5, "tick.wav", 0.6), (25.07, "sparkle.wav", 0.6), (25.75, "tick.wav", 0.9), (26.0, "pop.wav", 0.5),
    (26.58, "thud.wav", 0.9), (26.65, "boing.wav", 0.8), (27.37, "pop.wav", 0.8), (28.38, "tick.wav", 0.9),
    (28.5, "pop.wav", 0.6), (29.29, "pop.wav", 0.7), (30.0, "tick.wav", 0.9), (30.7, "tick.wav", 0.9),
    (30.75, "bell.wav", 0.5), *[(31.45 + k * 0.1, "pop.wav", 0.4) for k in range(5)], (31.79, "sparkle.wav", 0.8),
    (32.29, "tick.wav", 0.9), *[(32.8 + k * 0.25, "tick.wav", 0.6) for k in range(4)], (33.3, "thud.wav", 0.6),
    (33.93, "sparkle.wav", 0.9), (33.95, "bell.wav", 0.7), (34.5, "pop.wav", 0.5), (35.2, "sparkle.wav", 0.6),
    (36.0, "tick.wav", 1.0), (36.05, "thud.wav", 0.8), (36.68, "tick.wav", 1.0), (36.72, "thud.wav", 0.9),
    (37.24, "sting.wav", 0.8), (37.98, "pop.wav", 0.7), (38.47, "pop.wav", 0.8), (38.6, "sparkle.wav", 0.6),
    (39.29, "pop.wav", 0.7), (40.13, "thud.wav", 1.0), (40.15, "sparkle.wav", 0.8), (40.7, "sting_low.wav", 0.6),
    (41.5, "tick.wav", 0.3), (42.08, "pop.wav", 0.6), (42.9, "murmur.wav", 0.5), (43.4, "pop.wav", 0.6),
    (44.1, "step.wav", 0.5), (44.73, "sting.wav", 0.8), (45.3, "tick.wav", 0.6), (45.73, "thud.wav", 0.9),
    (45.78, "boing.wav", 0.6), (46.62, "sparkle.wav", 0.8), (47.2, "pop.wav", 0.7), (47.51, "bell.wav", 0.9),
    (47.6, "coin.wav", 0.6), (48.4, "boing.wav", 0.7), (49.05, "thud.wav", 0.8), (49.3, "tick.wav", 0.5),
    (49.89, "pop.wav", 0.8), (50.2, "boing.wav", 0.5), (50.9, "pop.wav", 0.8), (51.46, "pop.wav", 0.7),
    (52.2, "sparkle.wav", 0.5),
]

if __name__ == "__main__":
    import json
    import engine
    engine.LIPSYNC = False
    json.dump([{"time": round(t, 3), "file": f, "volume": v} for t, f, v in sorted(SFX)],
              open(sys.argv[2], "w"), indent=1)
    kw = {}
    if len(sys.argv) > 4:
        kw["frames"] = (int(sys.argv[3]), int(sys.argv[4]))
    import safezone
    safezone.fit(SHOTS, sys.modules[__name__])   # characters inside the Shorts safe zone
    render(SHOTS, TOTAL, sys.argv[1], grain=4, xfade=0.18, fade_out=0.0, **kw)

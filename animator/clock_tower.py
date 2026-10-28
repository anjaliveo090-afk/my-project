"""Story: 'The clock tower that lied' - 19 shots timed to the voiceover."""
import math

from engine import (W, H, Char, clamp, cobbles, disc, ease, glow, hexc, hills, hourglass,
                    houses, keyed, label, lerp, lerpc, mill, moon, pop, render, rrect,
                    shafts, sky, stars, sun, text, tower, bokeh, bricks, clock_face,
                    draw_sandwich, fill_stroke, ellipse, INK, ref_camera, set_voice)

TOTAL = 60.66

CLOCKMAKER = Char("#3f8f6b", hair="bowl", hair_col="#6b4226")
FOREMAN = Char("#8a5a2b", hair="bald", hair_col="#6d6d6d", mustache="#3a2a20")
MAYOR = Char("#24243a", hair="tophat", hair_col="#bdbdbd", mustache="#d8d8d8", tie="#c0392b")
WORKERS = [Char(c, hair="cap", hair_col=h) for c, h in (
    ("#3d6fb6", "#5b5b66"), ("#b8473d", "#6b4a33"), ("#d39b2a", "#4f4f5a"),
    ("#7a4fa0", "#6b4a33"), ("#2f9a9a", "#5b5b66"))]

NIGHT_TOP, NIGHT_BOT = hexc("#0e1638"), hexc("#3b2c66")
DAWN_TOP, DAWN_BOT = hexc("#3a4d8f"), hexc("#f2a37a")
DAY_TOP, DAY_BOT = hexc("#6fb4e8"), hexc("#d9eef7")
GOLD_TOP, GOLD_BOT = hexc("#5c7fc0"), hexc("#f7c27a")
DUSK_TOP, DUSK_BOT = hexc("#2a2350"), hexc("#e8774f")


# 0: establishing aerial of the town at dawn
def s_town(ctx, t, d):
    sky(ctx, NIGHT_TOP, DAWN_BOT)
    stars(ctx, 1, 90, 0.8, t, 500)
    moon(ctx, 560, 230, 34)
    hills(ctx, 820, hexc("#3a3466"), 2, 80)
    houses(ctx, 960, 3, 0.55, hexc("#4a4170"), hexc("#2c2850"), hexc("#2a2440"), lit=0.9)
    mill(ctx, 430, 1000, 0.6, t, lit=0.8)
    tower(ctx, 250, 1060, 0.75, 6, 20 + t * 3, lit=0.8, glow_a=0.9)
    houses(ctx, 1150, 4, 0.9, hexc("#5a4d7a"), hexc("#35305c"), hexc("#2a2440"), lit=1.0)
    ctx.rectangle(-600, 1130, W + 1200, 600)
    ctx.set_source_rgb(*hexc("#241f3f"))
    ctx.fill()
    bokeh(ctx, 5, 14, t, (1, 0.8, 0.5), 0.2)


# 1: the tower clock close up, it smirks (it lies)
def s_clock(ctx, t, d):
    bricks(ctx, -400, -400, W + 800, H + 800, hexc("#9c5b44"), hexc("#5e3226"), 60)
    shafts(ctx, t, (1, 0.85, 0.55), 0.22)
    m = 20 + int(t * 2) * 1
    eyes = keyed(t, [(0, None), (1.55, "smirk")])
    clock_face(ctx, 360, 600, 250, 6, m, glow=0.5, eyes=eyes)


# 2: crowd, nobody owns a watch
def s_crowd(ctx, t, d):
    sky(ctx, DAWN_TOP, DAWN_BOT)
    houses(ctx, 900, 11, 0.9, hexc("#c98f6d"), hexc("#6d3f4a"), hexc("#3a2f45"), lit=0.4)
    tower(ctx, 360, 930, 0.7, 6, 20, lit=0.3)
    cobbles(ctx, 900, hexc("#8a7a8f"), hexc("#4c4058"))
    shafts(ctx, t, (1, 0.8, 0.6), 0.15)
    xs = (100, 235, 370, 505, 640)
    for k, (x, ch) in enumerate(zip(xs, WORKERS)):
        if k == 2:
            expr = keyed(t, [(0, "neutral"), (0.9, "shock"), (1.8, "worried")])
            arms = keyed(t, [(0, ("down", "down")), (0.7, ("down", "hold")), (1.8, ("shrug", "shrug"))])
        else:
            expr = keyed(t, [(0, "neutral"), (1.9 + k * 0.08, "worried")])
            arms = keyed(t, [(0, ("down", "down")), (1.9 + k * 0.08, ("shrug", "shrug"))])
        ch.draw(ctx, x, 1180 + (k % 2) * 25, 0.78, expr, t + k, arms=arms, look=(-0.4 if x > 360 else 0.4))


# 3: the bell tells everyone when to work
def s_bell(ctx, t, d):
    sky(ctx, GOLD_TOP, GOLD_BOT)
    sun(ctx, 140, 380, 40, (1, 0.85, 0.55))
    houses(ctx, 950, 21, 0.8, hexc("#d7a27c"), hexc("#7b4553"), hexc("#3a2f45"))
    tower(ctx, 170, 1000, 0.9, 7, 0, bell=math.sin(t * 5.5) * 0.35 * math.exp(-t * 0.25))
    mill(ctx, 420, 1010, 0.75, t, gate=True)
    cobbles(ctx, 1000, hexc("#9c8a8a"), hexc("#5a4a5a"))
    for k, ch in enumerate(WORKERS):
        x = -120 + k * 95 + t * 85
        ch.draw(ctx, x, 1190 + (k % 2) * 20, 0.62, "determined", t + k, pose="walk",
                walk_phase=t * 1.7 + k * 0.3, arms=("down", "down"), look=0.5, bob=1.4)
    shafts(ctx, t, (1, 0.85, 0.55), 0.18)


# 4: nobody argues with a bell (salute)
def s_salute(ctx, t, d):
    sky(ctx, GOLD_TOP, GOLD_BOT)
    tower(ctx, 360, 1200, 1.2, 7, 0, bell=math.sin(t * 5) * 0.2)
    glow(ctx, 360, 230, 300, (1, 0.85, 0.5), 0.35)
    arms = keyed(t, [(0, ("down", "down")), (0.45, ("down", "salute"))])
    WORKERS[0].draw(ctx, 360, 1330, 1.85, keyed(t, [(0, "neutral"), (0.45, "determined")]), t,
                    arms=arms, bob=0.4)


# 5: a young clockmaker arrives with a perfect pocket watch
def s_arrive(ctx, t, d):
    sky(ctx, GOLD_TOP, GOLD_BOT)
    sun(ctx, 560, 420, 46, (1, 0.8, 0.5))
    houses(ctx, 980, 31, 0.95, hexc("#d9a07a"), hexc("#7b4553"), hexc("#3a2f45"))
    cobbles(ctx, 980, hexc("#a08c86"), hexc("#5a4a5a"))
    shafts(ctx, t, (1, 0.85, 0.55), 0.2, x=200)
    walking = t < 1.6
    x = lerp(-60, 330, ease(t / 1.6))
    if walking:
        CLOCKMAKER.draw(ctx, x, 1190, 1.05, "happy", t, pose="walk", walk_phase=t * 1.8,
                        arms=("down", "down"), item="suitcase", item_hand=0, look=0.6, bob=1.3)
    else:
        arms = ("down", "show")
        CLOCKMAKER.draw(ctx, x, 1190, 1.05, keyed(t, [(0, "happy"), (2.0, "smirk")]), t,
                        arms=arms, item="watch", item_hand=1, bob=0.6)
        k = t - 2.0
        if k > 0:
            sx, sy = x + 30 * 1.05 + 60 * 1.05, 1190 - 85 * 1.05 - 88 * 1.05 - 40 * 1.05 - 22
            for a in range(4):
                ang = a * math.pi / 2 + k * 2
                ln = 30 * pop(k)
                ctx.move_to(sx + math.cos(ang) * 8, sy + math.sin(ang) * 8)
                ctx.line_to(sx + math.cos(ang) * (8 + ln), sy + math.sin(ang) * (8 + ln))
                ctx.set_source_rgba(1, 0.95, 0.6, clamp(1.4 - k))
                ctx.set_line_width(5)
                ctx.stroke()
            glow(ctx, sx, sy, 90, (1, 0.9, 0.5), 0.6 * clamp(1.4 - k * 0.5))


# 6: he sits outside the mill for a week, writing everything down
def s_week(ctx, t, d):
    cyc = (t / d) * 3.0
    night = 0.5 - 0.5 * math.cos(cyc * 2 * math.pi)
    sky(ctx, lerpc(DAY_TOP, NIGHT_TOP, night), lerpc(GOLD_BOT, NIGHT_BOT, night))
    stars(ctx, 9, 60, night, t, 600)
    tower(ctx, 600, 860, 0.55, 6, (t * 400) % 60, lit=night, glow_a=night)
    mill(ctx, -140, 1050, 0.85, t, lit=night)
    cobbles(ctx, 1040, lerpc(hexc("#9c8a8a"), hexc("#3a3456"), night), lerpc(hexc("#5a4a5a"), hexc("#1d1a30"), night))
    rrect(ctx, 210, 1080, 130, 80, 6)
    fill_stroke(ctx, hexc("#9a6a3c"), 4)
    CLOCKMAKER.draw(ctx, 260, 1090, 0.95, keyed(t, [(0, "determined"), (2.3, "worried")]), t,
                    pose="sit", arms=("hold", "write"), item="notebook", item_hand=0, look=0.3, bob=0.3)
    days = min(7, int(t / d * 7.5) + 1)
    for k in range(days):
        x = 470 + (k % 4) * 22 + (k // 4) * 110
        ctx.move_to(x, 1010)
        ctx.line_to(x, 940)
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(6)
        ctx.stroke()
        if k == 4:
            ctx.move_to(460, 990)
            ctx.line_to(550, 955)
            ctx.stroke()
    dark = night * 0.35
    ctx.set_source_rgba(0.05, 0.05, 0.2, dark)
    ctx.rectangle(-600, -800, W + 1200, H + 1600)
    ctx.fill()


def _compare(ctx, t, top, bot, sun_y, th, tm, wh, wm, tag, tag_col):
    sky(ctx, top, bot)
    sun(ctx, 600, sun_y, 50, (1, 0.75, 0.5))
    hills(ctx, 1000, lerpc(top, (0, 0, 0), 0.4), 41, 90)
    tower(ctx, 230, 1250, 1.1, th, tm, glow_a=0.6)
    text(ctx, "TOWER", 230, 650, 40, (1, 1, 1))
    clock_face(ctx, 520, 760, 120, wh, wm, rim="#d9a92e", glow=0.5)
    ctx.move_to(520, 626)
    ctx.curve_to(520, 560, 600, 520, 640, 470)
    ctx.set_source_rgb(*hexc("#e0b84a"))
    ctx.set_line_width(6)
    ctx.stroke()
    text(ctx, "WATCH", 520, 930, 40, (1, 1, 1))
    label(ctx, tag, 360, 1080, 62, tag_col, scale=pop(t - 0.8), tilt=-0.06)


# 7: dawn: tower 20 minutes fast
def s_dawn(ctx, t, d):
    _compare(ctx, t, DAWN_TOP, DAWN_BOT, 980 - t * 40, 6, 20, 6, 0, "+20 MIN", hexc("#d63c3c"))


# 8: dusk: tower 25 minutes slow
def s_dusk(ctx, t, d):
    _compare(ctx, t, DUSK_TOP, DUSK_BOT, 860 + t * 40, 5, 35, 6, 0, "-25 MIN", hexc("#3d6fd6"))


# 9: an hour of free work every day flows to the mill owner
def s_hourglass(ctx, t, d):
    sky(ctx, hexc("#2b1f2a"), hexc("#5a3a32"))
    bricks(ctx, -400, -400, W + 800, H + 800, hexc("#5a3328"), hexc("#2a1712"), 50)
    glow(ctx, 360, 640, 520, (1, 0.7, 0.35), 0.25)
    hourglass(ctx, 360, 640, 1.25, 1 - t / d * 0.9)
    for k, ch in enumerate(WORKERS[:3]):
        ch.draw(ctx, 90 + k * 90, 1170, 0.55, "sad", t + k, arms=("hold", "hold"), bob=0.5, look=0.5)
    MAYOR.draw(ctx, 600, 1180, 0.8, keyed(t, [(0, "smirk"), (1.6, "grin")]), t, arms=("hip", "up"), look=-0.4)
    for k in range(8):
        ph = (t * 0.9 + k / 8) % 1
        x = lerp(250, 600, ph)
        y = 960 - math.sin(ph * math.pi) * 160
        disc(ctx, x, y, 14, (*hexc("#f2c94c"), 1))
        ctx.arc(x, y, 14, 0, 2 * math.pi)
        ctx.set_source_rgb(*INK)
        ctx.set_line_width(3)
        ctx.stroke()
    label(ctx, "1 HOUR FREE / DAY", 360, 210, 46, hexc("#f2c94c"), fg=INK, scale=pop(t - 1.4), tilt=0.04)


# 10: the foreman laughs so hard he drops his sandwich
def s_foreman(ctx, t, d):
    sky(ctx, DAY_TOP, DAY_BOT)
    mill(ctx, 40, 1000, 1.1, t)
    cobbles(ctx, 990, hexc("#9c8a8a"), hexc("#5a4a5a"))
    CLOCKMAKER.draw(ctx, 80, 1250, 1.0, "neutral", t, talk=t < 0.9, arms=("down", "show"),
                    item="notebook", item_hand=1, look=0.7, bob=0.5)
    laughing = t >= 0.9
    expr = "laugh" if laughing else "neutral"
    lean = -0.18 + math.sin(t * 16) * 0.05 if laughing else 0
    has = t < 1.9
    FOREMAN.draw(ctx, 450, 1260, 1.25, expr, t, arms=("hip", "show" if has else "up"),
                 item="sandwich" if has else None, item_hand=1, lean=lean, bob=2.5 if laughing else 0.5,
                 look=-0.3)
    if not has:
        k = t - 1.9
        y = min(1240, 690 + 900 * k * k)
        draw_sandwich(ctx, 600, y, rot=k * 6 if y < 1240 else 1.2)


# 11: "Clocks don't lie, kid."
def s_wag(ctx, t, d):
    sky(ctx, DAY_TOP, DAY_BOT)
    bricks(ctx, -400, -200, W + 800, 1300, hexc("#a2563f"), hexc("#5e3226"), 50)
    FOREMAN.draw(ctx, 360, 1420, 2.4, "smirk", t, arms=("hip", "wag"), bob=0.3, look=0.2)


# 12: the workers look at him like he insulted their mothers
def s_workers(ctx, t, d):
    sky(ctx, hexc("#4a2a3a"), hexc("#c0533f"))
    mill(ctx, 0, 980, 1.2, t, lit=0.3)
    cobbles(ctx, 960, hexc("#7a5a5a"), hexc("#3a2a3a"))
    glow(ctx, 470, 900, 500, (1, 0.3, 0.2), 0.25)
    for k, ch in enumerate(WORKERS[:4]):
        expr = keyed(t, [(0, "neutral"), (0.8 + k * 0.1, "angry")])
        arms = ("hip", "hip") if k == 1 else ("down", "down")
        ch.draw(ctx, 300 + k * 120, 1150 + (k % 2) * 40, 0.95, expr, t + k, arms=arms, look=-0.5)
    CLOCKMAKER.draw(ctx, 70, 1300, 1.2, keyed(t, [(0, "neutral"), (1.4, "worried")]), t,
                    talk=t < 0.8, look=0.7, arms=("down", "show"), item="notebook")


# 13: the mayor... owns the mill
def s_office(ctx, t, d):
    ctx.rectangle(-600, -800, W + 1200, H + 1600)
    ctx.set_source_rgb(*hexc("#4a2e2a"))
    ctx.fill()
    for k in range(-6, 14):
        ctx.rectangle(k * 90, 200, 80, 760)
        fill_stroke(ctx, hexc("#5e3b33"), 3)
    rrect(ctx, 80, 230, 300, 380, 12)
    fill_stroke(ctx, hexc("#2a2440"), 6)
    ctx.save()
    rrect(ctx, 86, 236, 288, 368, 10)
    ctx.clip()
    sky(ctx, GOLD_TOP, GOLD_BOT, 230, 610, depth=1)
    tower(ctx, 230, 760, 0.45, 6, 20, depth=1)
    ctx.restore()
    rrect(ctx, 460, 270, 200, 120, 8)
    fill_stroke(ctx, hexc("#d9c08a"), 5)
    text(ctx, "MILL", 560, 310, 34, INK, outline=False)
    text(ctx, "OWNER", 560, 352, 34, INK, outline=False)
    MAYOR.draw(ctx, 470, 1060, 1.15, keyed(t, [(0, "happy"), (1.9, "grin")]), t, arms=("hip", "hip"), look=-0.3)
    ctx.rectangle(-600, 960, W + 1200, 500)
    fill_stroke(ctx, hexc("#6b3d26"), 5)
    rrect(ctx, 380, 900, 190, 60, 6)
    fill_stroke(ctx, hexc("#e2b23c"), 4)
    text(ctx, "MAYOR", 475, 930, 34, INK, outline=False)
    CLOCKMAKER.draw(ctx, 140, 1330, 1.3, keyed(t, [(0, "neutral"), (1.9, "shock")]), t,
                    talk=t < 1.6, look=0.6, arms=("down", "hold"), item="notebook")


# 14: he smiles, listens to every number, asks one question
def s_listen(ctx, t, d):
    ctx.rectangle(-600, -800, W + 1200, H + 1600)
    ctx.set_source_rgb(*hexc("#4a2e2a"))
    ctx.fill()
    for k in range(-6, 14):
        ctx.rectangle(k * 90, 0, 80, 1100)
        fill_stroke(ctx, hexc("#5e3b33"), 3)
    glow(ctx, 360, 600, 450, (1, 0.8, 0.5), 0.3)
    nod = math.sin(t * 7) * 10 if t < 2.3 else 0
    arms = ("hip", "show") if t < 2.3 else ("hip", "up")
    MAYOR.draw(ctx, 360, 1380, 2.0, "grin", t, arms=arms, item="notebook" if t < 2.3 else None,
               head_nod=nod, bob=0.2)


# 15: "Whose clock is wrong, son? Yours, or mine?"
def s_cold(ctx, t, d):
    ctx.rectangle(-600, -800, W + 1200, H + 1600)
    ctx.set_source_rgb(*hexc("#1b1626"))
    ctx.fill()
    rrect(ctx, 30, 120, 260, 360, 10)
    fill_stroke(ctx, hexc("#0e1638"), 6)
    ctx.save()
    rrect(ctx, 36, 126, 248, 348, 8)
    ctx.clip()
    sky(ctx, NIGHT_TOP, NIGHT_BOT, 120, 480, depth=1)
    tower(ctx, 160, 640, 0.4, 6, 20, glow_a=1.0, depth=1)
    ctx.restore()
    glow(ctx, 600, 300, 600, (1, 0.55, 0.3), 0.35)
    arms = ("down", "down") if t < 1.3 else ("point", "down")
    MAYOR.draw(ctx, 450, 1700, 3.4, keyed(t, [(0, "grin"), (0.25, "cold")]), t, arms=arms, bob=0.1,
               look=-0.2)


# 16: by Friday he left town with the only honest clock
def s_leave(ctx, t, d):
    sky(ctx, NIGHT_TOP, NIGHT_BOT)
    stars(ctx, 16, 120, 0.9, t, 700)
    moon(ctx, 150, 260, 40)
    houses(ctx, 860, 17, 0.6, hexc("#3e3866"), hexc("#26224a"), hexc("#221d38"), lit=1.0)
    tower(ctx, 470, 900, 0.65, 9, 0, lit=1.0, glow_a=0.9)
    hills(ctx, 960, hexc("#1f1c3d"), 18, 40)
    ctx.move_to(260, 960)
    ctx.line_to(460, 960)
    ctx.line_to(820, 1600)
    ctx.line_to(-100, 1600)
    ctx.close_path()
    ctx.set_source_rgb(*hexc("#3a3456"))
    ctx.fill()
    x = lerp(330, 220, t / d)
    s = lerp(1.2, 0.85, t / d)
    CLOCKMAKER.draw(ctx, x, lerp(1260, 1150, t / d), s, "sad", t, pose="walk", walk_phase=t * 1.3,
                    arms=("down", "hold"), item="watch", item_hand=1, look=-0.5, bob=1.0)
    glow(ctx, x + 20 * s, lerp(1260, 1150, t / d) - 170 * s, 70, (1, 0.85, 0.4), 0.55)


# 17: in real life: 1800s England, clocks turned forward in the morning, back at night
def s_history(ctx, t, d):
    ctx.rectangle(-600, -800, W + 1200, H + 1600)
    ctx.set_source_rgb(*hexc("#8a6a4a"))
    ctx.fill()
    bricks(ctx, -400, -200, W + 800, 1300, hexc("#8a6a4a"), hexc("#3a2a1a"), 50)
    for k in range(5):
        x = 30 + k * 150
        rrect(ctx, x, 980, 120, 110, 8)
        fill_stroke(ctx, hexc("#6b4a2a"), 4)
        WORKERS[k].draw(ctx, x + 60, 1240, 0.6, "sad", t + k, arms=("hold", "hold"), bob=0.4)
    if t < 3.2:
        m = 0 + 50 * ease((t - 0.8) / 1.6)
    else:
        m = 50 - 50 * ease((t - 3.6) / 1.6)
    clock_face(ctx, 360, 520, 190, 6, m, glow=0.4)
    arrow = 1 if t < 3.2 else -1
    a0, a1 = -math.pi / 2 - 0.7 * arrow, -math.pi / 2 + 0.7 * arrow
    ctx.new_sub_path()
    if arrow > 0:
        ctx.arc(360, 520, 245, a0, a1)
    else:
        ctx.arc_negative(360, 520, 245, a0, a1)
    ctx.set_source_rgb(*hexc("#e0302a"))
    ctx.set_line_width(16)
    ctx.stroke()
    hx, hy = 360 + math.cos(a1) * 245, 520 + math.sin(a1) * 245
    tang = a1 + arrow * math.pi / 2
    ctx.move_to(hx + math.cos(tang) * 34, hy + math.sin(tang) * 34)
    ctx.line_to(hx + math.cos(tang + 2.4) * 30, hy + math.sin(tang + 2.4) * 30)
    ctx.line_to(hx + math.cos(tang - 2.4) * 30, hy + math.sin(tang - 2.4) * 30)
    ctx.close_path()
    ctx.fill()
    rrect(ctx, 565, 900, 110, 85, 6)
    fill_stroke(ctx, hexc("#6b4a2a"), 4)
    MAYOR.draw(ctx, 620, 900, 0.8, "grin", t, arms=("up", "hip"), look=-0.6)
    label(ctx, "ENGLAND, 1800s", 360, 120, 44, hexc("#f3e2b8"), fg=INK, scale=pop(t - 0.2), tilt=-0.03)
    label(ctx, "FORWARD AT DAWN" if t < 3.2 else "BACK AT NIGHT", 360, 210, 40,
          hexc("#d63c3c"), scale=pop(t - (0.9 if t < 3.2 else 3.5)), tilt=0.04)


# 18: in a city with only one clock, the lie becomes the time
def s_final(ctx, t, d):
    sky(ctx, NIGHT_TOP, NIGHT_BOT)
    stars(ctx, 23, 140, 0.9, t, 800)
    moon(ctx, 580, 220, 36)
    houses(ctx, 1080, 25, 0.7, hexc("#3e3866"), hexc("#26224a"), hexc("#221d38"), lit=1.0)
    tower(ctx, 360, 1150, 0.95, 6, 20, lit=1.0, glow_a=1.2, clock_eyes="cold" if t > 1.3 else None)
    ctx.rectangle(-600, 1140, W + 1200, 600)
    ctx.set_source_rgb(*hexc("#1b1833"))
    ctx.fill()
    bokeh(ctx, 8, 16, t, (1, 0.8, 0.5), 0.18)


C = (W / 2, H / 2)
SHOTS = [
    dict(start=0.00, draw=s_town, cam=(1.0, 1.15, (360, 560), (330, 700)), focus=(270, 620)),
    dict(start=2.60, draw=s_clock, cam=(1.0, 1.12, (360, 640), (360, 600)), focus=(370, 560)),
    dict(start=5.32, draw=s_crowd, cam=(1.0, 1.1, C, (360, 760)), focus=(370, 980)),
    dict(start=8.00, draw=s_bell, cam=(1.06, 1.1, (300, 680), (460, 700)), focus=(380, 960), cap=1.35),
    dict(start=11.53, draw=s_salute, speaker=WORKERS[0], cam=(1.0, 1.08, C, (360, 680))),
    dict(start=13.10, draw=s_arrive, speaker=CLOCKMAKER, cam=(1.0, 1.25, (360, 760), (420, 720)), focus=(390, 860)),
    dict(start=16.99, draw=s_week, speaker=CLOCKMAKER, cam=(1.0, 1.08, C, (330, 760)), focus=(280, 860)),
    dict(start=20.48, draw=s_dawn, cam=(1.0, 1.06, C, C), cap=1.15),
    dict(start=23.05, draw=s_dusk, cam=(1.06, 1.0, C, C)),
    dict(start=25.42, draw=s_hourglass, speaker=MAYOR, cam=(1.0, 1.1, C, (360, 680)), cap=1.12),
    dict(start=29.85, draw=s_foreman, cam=(1.0, 1.1, C, (400, 720)), focus=(440, 900), shake=(0.9, 6)),
    dict(start=33.07, draw=s_wag, speaker=FOREMAN, cam=(1.0, 1.06, C, C)),
    dict(start=34.35, draw=s_workers, cam=(1.0, 1.15, C, (440, 820)), focus=(460, 900)),
    dict(start=37.55, draw=s_office, speaker=MAYOR, cam=(1.18, 1.0, (330, 820), C), shake=(1.9, 5)),
    dict(start=40.90, draw=s_listen, speaker=MAYOR, cam=(1.0, 1.1, C, (360, 600)), focus=(360, 820)),
    dict(start=44.06, draw=s_cold, speaker=MAYOR, cam=(1.0, 1.12, C, (420, 560)), focus=(430, 800), cap=1.3, vignette=0.75),
    dict(start=46.46, draw=s_leave, cam=(1.2, 1.0, (330, 900), C)),
    dict(start=51.05, draw=s_history, speaker=MAYOR, cam=(1.0, 1.06, C, C), cap=1.12, sepia=True),
    dict(start=57.77, draw=s_final, cam=(1.3, 1.0, (360, 420), C)),
]
for k, s in enumerate(SHOTS):
    s["end"] = SHOTS[k + 1]["start"] if k + 1 < len(SHOTS) else TOTAL
ref_camera(SHOTS)

# SFX cue sheet: (time, file, volume)
SFX = [(s["start"] - 0.18, "whoosh.wav", 0.45) for s in SHOTS[1:]]
SFX += [
    (0.2, "bell.wav", 0.35),
    *[(2.7 + k * 0.5, "tick.wav", 0.7) for k in range(5)],
    (4.15, "sting_soft.wav", 0.6),
    (8.3, "bell.wav", 0.7), (9.9, "bell.wav", 0.55),
    (11.98, "pop.wav", 0.7),
    (15.1, "sparkle.wav", 0.7),
    *[(17.3 + k * 0.45, "page.wav", 0.5) for k in range(7)],
    (21.3, "pop.wav", 0.8), (21.3, "thud.wav", 0.6),
    (23.85, "pop.wav", 0.8), (23.85, "thud.wav", 0.6),
    *[(25.6 + k * 0.5, "coin.wav", 0.45) for k in range(8)],
    (26.8, "pop.wav", 0.7),
    (30.75, "boing.wav", 0.7), (31.9, "thud.wav", 0.8),
    (33.2, "pop.wav", 0.5),
    (35.0, "murmur.wav", 0.7),
    (39.45, "sting.wav", 0.8),
    (41.2, "pop.wav", 0.5),
    (44.2, "sting_low.wav", 0.9),
    *[(46.7 + k * 0.55, "step.wav", 0.55) for k in range(8)],
    (51.3, "pop.wav", 0.6),
    *[(51.9 + k * 0.1, "tick.wav", 0.45) for k in range(16)],
    *[(54.7 + k * 0.1, "tick.wav", 0.45) for k in range(16)],
    (58.0, "bell.wav", 0.8),
]

if __name__ == "__main__":
    import json
    import sys
    out = sys.argv[1]
    json.dump([{"time": round(t, 3), "file": f, "volume": v} for t, f, v in SFX],
              open(sys.argv[2], "w"), indent=1)
    if len(sys.argv) > 3:
        set_voice(sys.argv[3])
    render(SHOTS, TOTAL, out, grain=5)

"""Clock tower, cinematic cut: the camera reaches a new framing every 2-4 words,
landing on the word it illustrates, and moves (crane, pan, tilt, push, pull)
between framings like the reference videos. Word times come from the
voiceover alignment (output/clock_tower/aligned.json)."""
import math
import sys

import clock_tower as ct
from clock_tower import (CLOCKMAKER, MAYOR, WORKERS, DAWN_TOP, DAWN_BOT, DAY_TOP, GOLD_TOP,
                         GOLD_BOT, NIGHT_TOP, NIGHT_BOT, DUSK_TOP, DUSK_BOT)
from engine import (W, H, clamp, cobbles, ease, glow, hexc, hills, houses, keyed, lerp, lerpc,
                    mill, moon, pop, render, set_voice, sky, stars, sun, tower, bokeh, shafts)
from style2 import Char2

TOTAL = 60.66
C = (W / 2, H / 2)
INSPECTOR = Char2("#6f7d8c", hair="bowl", hair_col="#4a3a30", outfit="suit", tie="#2b45a6", glasses=True)


def walk_x(T, t0, t1, x0, x1):
    return lerp(x0, x1, ease((T - t0) / (t1 - t0)))


# A (0-5.3): mill owner under the tower -> crane up -> clock lies -> drone over the city -> street
def s_open(ctx, t, d):
    T = t
    night = clamp(0.5 - 0.5 * math.cos(clamp((T - 3.2) / 1.0) * 2 * math.pi * 2)) if 3.2 < T < 4.2 else 0.0
    sky(ctx, lerpc(DAWN_TOP, NIGHT_TOP, night), lerpc(DAWN_BOT, NIGHT_BOT, night), -1200, 1300)
    stars(ctx, 3, 140, 0.3 + night, T, 600, depth=0.2)
    sun(ctx, 600, 700, 50, (1, 0.8, 0.55), depth=0.25)
    hills(ctx, 980, hexc("#5a4d86"), 2, 120, depth=0.35)
    houses(ctx, 1040, 3, 0.6, hexc("#b98a8a"), hexc("#6d3f5a"), hexc("#3a2f45"), lit=night, depth=0.6)
    m = 20 + (max(0.0, T - 3.3) * 400 if T < 4.2 else 360)
    tower(ctx, 360, 1150, 1.6, 6, m % 60 + 0, lit=0.4 + night * 0.6, glow_a=0.5 + night,
          clock_eyes="smirk" if T > 1.85 else None, depth=1)
    mill(ctx, 560, 1150, 0.9, T, lit=night, depth=1)
    houses(ctx, 1200, 5, 0.95, hexc("#d9a07a"), hexc("#7b4553"), hexc("#3a2f45"), x0=-600, x1=150,
           lit=night, depth=1)
    cobbles(ctx, 1150, hexc("#a08c86"), hexc("#5a4a5a"))
    shafts(ctx, T, (1, 0.85, 0.6), 0.16)
    if T < 2.4:
        arms = ("down", "down") if T < 0.55 else ("down", "up")
        MAYOR.draw(ctx, 360, 1330, 1.3, "grin" if T > 0.3 else "smirk", T, arms=arms, look=0.1)
    for k in range(3):
        x = -200 + (T - 3.9) * 300 + k * 190
        if -200 < x < 1000:
            WORKERS[k].draw(ctx, x, 1360 + k * 12, 1.0, "neutral", T + k, pose="walk",
                            walk_phase=T * 1.8 + k * 0.3, look=0.6)


# B (5.3-11.5): nobody owns a watch, the bell tells the city when to work and go home
def s_street(ctx, t, d):
    T = 5.32 + t
    dusk = ease((T - 10.7) / 0.6)
    sky(ctx, lerpc(DAY_TOP, DUSK_TOP, dusk), lerpc(GOLD_BOT, DUSK_BOT, dusk), -900, 1100)
    sun(ctx, 160, lerp(300, 820, dusk), 46, (1, 0.8, 0.5), depth=0.25)
    houses(ctx, 900, 11, 0.9, hexc("#d9a07a"), hexc("#7b4553"), hexc("#3a2f45"), lit=dusk, depth=0.85)
    swing = math.sin((T - 8.3) * 5.5) * 0.4 * math.exp(-(T - 8.3) * 0.5) if T > 8.3 else 0.0
    tower(ctx, 560, 920, 1.0, 7 if T < 10.7 else 6, 0, bell=swing, lit=dusk, glow_a=dusk, depth=1)
    mill(ctx, 760, 940, 0.8, T, lit=dusk, depth=1)
    cobbles(ctx, 900, hexc("#a08c86"), hexc("#5a4a5a"))
    shafts(ctx, T, (1, 0.85, 0.55), 0.15)
    go = walk_x(T, 9.85, 10.55, 0, 300) - walk_x(T, 10.8, 11.45, 0, 300)
    moving = 9.85 < T < 10.55 or 10.8 < T < 11.45
    for k, ch in enumerate(WORKERS):
        x = 120 + k * 125 + go
        if k == 2:
            expr = keyed(T, [(0, "neutral"), (7.2, "shock"), (7.7, "worried"), (9.8, "determined")])
            arms = keyed(T, [(0, ("down", "down")), (6.9, ("down", "hold")), (7.7, ("shrug", "shrug")),
                             (9.8, ("down", "down"))])
        else:
            expr = keyed(T, [(0, "neutral"), (7.6 + k * 0.06, "worried"), (9.8, "determined")])
            arms = keyed(T, [(0, ("down", "down")), (7.6 + k * 0.06, ("shrug", "shrug")), (9.8, ("down", "down"))])
        ch.draw(ctx, x, 1150 + (k % 2) * 20, 0.95, expr, T + k, arms=arms,
                pose="walk" if moving else "stand", walk_phase=T * 1.9 + k * 0.25,
                look=(0.6 if 9.8 < T < 10.7 else (-0.6 if T > 10.7 else 0.0)))


# D (13.1-17.0): the clockmaker walks into town and holds up a perfect watch
def s_arrive2(ctx, t, d):
    T = 13.10 + t
    sky(ctx, GOLD_TOP, GOLD_BOT, -600, 1100)
    sun(ctx, 560, 420, 46, (1, 0.8, 0.5), depth=0.25)
    houses(ctx, 900, 31, 0.95, hexc("#d9a07a"), hexc("#7b4553"), hexc("#3a2f45"), depth=0.85)
    cobbles(ctx, 880, hexc("#a08c86"), hexc("#5a4a5a"))
    shafts(ctx, T, (1, 0.85, 0.55), 0.2, x=200)
    x = walk_x(T, 13.1, 14.5, -80, 330)
    if T < 14.6:
        CLOCKMAKER.draw(ctx, x, 1060, 1.15, "happy", T, pose="walk", walk_phase=T * 1.8,
                        arms=("down", "down"), item="suitcase", item_hand=0, look=0.6, bob=1.0)
    else:
        CLOCKMAKER.draw(ctx, x, 1060, 1.15, keyed(T, [(0, "happy"), (15.9, "smirk")]), T,
                        arms=("down", "show"), item="watch", item_hand=1, bob=0.4)
        wx, wy = 426, 800
        k = T - 16.3
        if k > 0:
            for a in range(4):
                ang = a * math.pi / 2 + k * 2
                ln = 26 * pop(k)
                ctx.move_to(wx + math.cos(ang) * 10, wy + math.sin(ang) * 10)
                ctx.line_to(wx + math.cos(ang) * (10 + ln), wy + math.sin(ang) * (10 + ln))
                ctx.set_source_rgba(1, 0.95, 0.6, clamp(1.4 - k))
                ctx.set_line_width(4)
                ctx.stroke()
            glow(ctx, wx, wy, 60, (1, 0.9, 0.5), 0.6 * clamp(1.4 - k * 0.5))


def s_history2(ctx, t, d):
    ct.s_history(ctx, t, d)
    for k, x in enumerate((90, 190)):
        INSPECTOR.draw(ctx, x, 1000 + k * 10, 0.8, keyed(t, [(0, "neutral"), (2.6, "shock")]), t + k,
                       arms=("hold", "write") if k == 0 else ("hold", "down"), item="notebook", item_hand=0,
                       look=0.5)


SHOTS = [
    dict(start=0.00, draw=s_open, dof=2, keys=[
        (0.00, 1.7, (360, 1000)), (0.45, 1.75, (360, 990)),          # "A mill owner"
        (1.37, 1.45, (360, 140), 0.75),                              # "built the clock tower" crane up
        (1.95, 2.1, (360, 125), 0.45),                               # "that lied"
        (2.90, 0.78, (360, 420), 0.7),                               # "the entire city" drone pull
        (3.80, 0.84, (380, 430)),                                    # "for ten years" time-lapse
        (4.80, 1.25, (360, 1110), 0.7)]),                            # "Nobody noticed" down to the street
    dict(start=5.32, draw=s_street, dof=2, keys=[
        (5.32, 1.05, (360, 830)),                                    # "See, back then"
        (7.00, 2.0, (370, 935), 0.5),                                # "almost nobody owned"
        (7.60, 1.5, (520, 930), 0.4),                                # "a watch"
        (8.45, 1.9, (560, 90), 0.55),                                # "the tower's bell"
        (9.42, 0.85, (560, 430), 0.55),                              # "told the whole city"
        (10.25, 1.15, (820, 900), 0.5),                              # "when to start work"
        (11.18, 1.15, (560, 900), 0.45)]),                           # "and when to go home"
    dict(start=11.53, draw=ct.s_salute, speaker=WORKERS[0], dof=3, keys=[
        (11.53, 1.0, (360, 760)), (12.10, 1.55, (360, 880), 0.45),  # "nobody argues"
        (12.70, 1.7, (360, 190), 0.45)]),                            # "with a bell"
    dict(start=13.10, draw=s_arrive2, speaker=CLOCKMAKER, dof=3, keys=[
        (13.10, 1.25, (60, 860)), (13.93, 1.25, (300, 860), 0.8),   # "a young clockmaker" tracking
        (14.57, 0.9, (360, 640), 0.5),                               # "moved to town" reveal
        (15.42, 3.0, (426, 800), 0.5),                               # "a pocket watch" insert
        (16.50, 3.5, (426, 800), 0.6)]),                             # "never lost a second"
    dict(start=16.99, draw=ct.s_week, speaker=CLOCKMAKER, dof=2, keys=[
        (16.99, 1.15, (300, 860)), (17.80, 1.15, (130, 800), 0.45), # "outside the mill"
        (18.26, 0.95, (360, 700), 0.4),                              # "for a week" time-lapse
        (18.70, 2.8, (245, 975), 0.4),                               # "writing down"
        (19.87, 2.4, (600, 430), 0.5)]),                             # "the bell rang"
    dict(start=20.48, draw=ct.s_dawn, keys=[
        (20.48, 1.0, C), (21.30, 1.9, (230, 560), 0.5),             # "the tower"
        (22.00, 1.9, (520, 760), 0.45),                              # "twenty minutes"
        (22.55, 1.05, (400, 560), 0.4)]),                            # "fast" + label
    dict(start=23.05, draw=ct.s_dusk, keys=[
        (23.05, 1.0, C), (23.80, 1.9, (230, 560), 0.5),
        (24.30, 1.9, (520, 760), 0.45), (25.02, 1.05, (400, 560), 0.4)]),
    dict(start=25.42, draw=ct.s_hourglass, speaker=MAYOR, keys=[
        (25.42, 1.0, C), (26.10, 2.2, (180, 880), 0.5),             # "every worker"
        (27.06, 2.4, (600, 840), 0.45),                              # "the mill owner"
        (27.82, 1.3, (360, 640), 0.45),                              # "an hour of free work"
        (29.13, 1.0, (360, 560), 0.45)]),                            # "every single day"
    dict(start=29.85, draw=ct.s_foreman, dof=3, shake=(0.9, 6), keys=[
        (29.85, 1.0, (300, 900)), (30.50, 1.7, (450, 950), 0.45),   # "the foreman"
        (31.40, 1.5, (450, 930), 0.4),                               # "laughed so hard"
        (32.50, 2.3, (600, 1180), 0.5)]),                            # "dropped his sandwich" follow it down
    dict(start=33.07, draw=ct.s_wag, speaker=ct.FOREMAN, dof=3, keys=[
        (33.07, 1.1, (360, 860)), (33.65, 1.5, (360, 840), 0.4)]),
    dict(start=34.35, draw=ct.s_workers, dof=3, dutch=0.05, keys=[
        (34.35, 1.0, (330, 880)), (34.98, 1.5, (480, 930), 0.45),   # "the workers"
        (36.40, 2.2, (420, 965), 0.5)]),                             # "insulted their mothers"
    dict(start=37.55, draw=ct.s_office, speaker=MAYOR, shake=(1.9, 5), keys=[
        (37.55, 1.0, C), (38.16, 1.9, (470, 790), 0.45),            # "the mayor"
        (38.89, 1.9, (140, 1022), 0.45),                             # "awkward"
        (39.90, 2.2, (560, 320), 0.5),                               # "the mayor owned" -> MILL OWNER sign
        (40.48, 1.8, (230, 420), 0.4)]),                             # "the mill" -> window
    dict(start=40.90, draw=ct.s_listen, speaker=MAYOR, dof=3, keys=[
        (40.90, 1.1, (380, 900)), (41.56, 1.6, (360, 900), 0.4),    # "smiled, listened"
        (42.34, 2.0, (528, 960), 0.45),                              # "every number"
        (43.47, 1.7, (360, 900), 0.45)]),                            # "one question"
    dict(start=44.06, draw=ct.s_cold, speaker=MAYOR, dof=4, dutch=-0.06, vignette=0.75, keys=[
        (44.06, 1.2, (440, 880)), (45.02, 1.6, (440, 870), 0.45),   # "son?"
        (45.60, 2.2, (160, 380), 0.4),                               # "Yours," -> tower in the window
        (46.03, 1.8, (440, 870), 0.35)]),                            # "or mine?"
    dict(start=46.46, draw=ct.s_leave, dof=2, keys=[
        (46.46, 1.0, (360, 700)), (47.22, 1.7, (311, 975), 0.45),   # "the clockmaker"
        (48.80, 3.0, (290, 1065), 0.5),                              # "the only honest clock"
        (50.60, 0.85, (360, 560), 0.6)]),                            # "in his pocket" crane up
    dict(start=51.05, draw=s_history2, sepia=True, keys=[
        (51.05, 1.0, C), (52.30, 2.0, (140, 800), 0.5),             # "factory inspectors"
        (53.75, 1.5, (360, 260), 0.45),                              # "England"
        (54.90, 2.2, (620, 720), 0.45),                              # "mill owners"
        (55.60, 1.6, (360, 520), 0.45),                              # "turning clocks forward"
        (57.00, 1.7, (360, 500), 0.4)]),                             # "back at night"
    dict(start=57.77, draw=ct.s_final, keys=[
        (57.77, 0.85, (360, 560)), (58.88, 1.8, (360, 545), 0.6),   # "only one clock"
        (59.50, 2.6, (360, 535), 0.45),                              # "the lie"
        (60.17, 3.0, (360, 535), 0.4)]),                             # "becomes the time"
]
for k, s in enumerate(SHOTS):
    s["end"] = SHOTS[k + 1]["start"] if k + 1 < len(SHOTS) else TOTAL


def camera_whooshes():
    """A whoosh under every big camera move (long travel or big zoom change)."""
    out = []
    for s in SHOTS:
        keys = s["keys"]
        for a, b in zip(keys, keys[1:]):
            m = b[3] if len(b) > 3 else min(0.55, 0.75 * (b[0] - a[0]))
            dist = math.hypot(b[2][0] - a[2][0], b[2][1] - a[2][1])
            if dist > 250 or max(a[1], b[1]) / min(a[1], b[1]) > 1.6:
                out.append((b[0] - m, "whoosh.wav", 0.35))
    return out


SFX = [(s["start"] - 0.15, "whoosh.wav", 0.4) for s in SHOTS[1:]] + camera_whooshes() + [
    (1.0, "whoosh.wav", 0.5),
    (1.9, "sting_soft.wav", 0.6),
    *[(1.4 + k * 0.5, "tick.wav", 0.6) for k in range(2)],
    *[(3.3 + k * 0.08, "tick.wav", 0.35) for k in range(11)],
    (8.35, "bell.wav", 0.7), (9.9, "bell.wav", 0.5),
    (7.2, "pop.wav", 0.6),
    (12.1, "pop.wav", 0.7), (12.7, "bell.wav", 0.5),
    (15.4, "pop.wav", 0.5), (16.3, "sparkle.wav", 0.7),
    *[(16.4 + k * 0.5, "tick.wav", 0.5) for k in range(2)],
    *[(18.7 + k * 0.3, "page.wav", 0.5) for k in range(4)],
    (19.9, "bell.wav", 0.6),
    (22.6, "pop.wav", 0.8), (22.6, "thud.wav", 0.6),
    (25.05, "pop.wav", 0.8), (25.05, "thud.wav", 0.6),
    *[(27.0 + k * 0.4, "coin.wav", 0.4) for k in range(6)],
    (29.2, "pop.wav", 0.7),
    (30.95, "boing.wav", 0.7), (32.5, "thud.wav", 0.8),
    (33.6, "pop.wav", 0.5),
    (35.0, "murmur.wav", 0.7),
    (39.9, "sting.wav", 0.8),
    (41.1, "pop.wav", 0.5),
    (44.2, "sting_low.wav", 0.9),
    *[(46.7 + k * 0.55, "step.wav", 0.5) for k in range(7)],
    (48.8, "sparkle.wav", 0.6),
    (51.2, "pop.wav", 0.6), (53.75, "pop.wav", 0.6),
    *[(55.3 + k * 0.08, "tick.wav", 0.4) for k in range(12)],
    *[(56.9 + k * 0.08, "tick.wav", 0.4) for k in range(12)],
    (58.0, "bell.wav", 0.8), (59.45, "sting_soft.wav", 0.6),
]

if __name__ == "__main__":
    import json
    json.dump([{"time": round(t, 3), "file": f, "volume": v} for t, f, v in sorted(SFX)],
              open(sys.argv[2], "w"), indent=1)
    if "--no-lipsync" in sys.argv:
        import engine
        engine.LIPSYNC = False
    elif len(sys.argv) > 3:
        set_voice(sys.argv[3])
    render(SHOTS, TOTAL, sys.argv[1], grain=5)

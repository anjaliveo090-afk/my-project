# The Clock Tower That Lied — motion graphics short

A 60.66 s vertical (9:16, 1080×1920, 30 fps) motion-graphics piece built on the uploaded track
`assets/narration.mp3`. Every frame is a function of time, generated from code in `scene.js`.
The same code drives a live preview (`index.html`) and the offline renderer (`render.mjs`).

## 1. What the audio actually is

The upload is **spoken narration, not music**: a single narrator (a Voiceflow voice export) telling a
short story with a twist. The analysis found:

| Measure | Result |
|---|---|
| Duration | 60.66 s, mono, 44.1 kHz |
| Content | One voice; no beat, drums, bass line, drops or music bed |
| Pauses | 0.2–0.3 s between sentences, close to silent (−30 to −40 dB) |
| Energy | Flat (−17 to −22 dB RMS per second), dominated by the speech band |
| Delivery | About 3.8 words per second, conversational storytelling: hook, setup, reveal, comic beats, twist, epilogue |

Because there is no beat, the visuals are synced to the **voice**: sentence onsets, stressed
words ("lied", "bell", "fast", "slow", "nearly an hour", "dropped", "looked", "insulted", "mine", "time")
and the pauses between lines. No music, sound effects or narration were added.

**Transcript.** The text comes from a word-timestamped transcription (Whisper small, run locally).
It is stored in `assets/words.js`. All 229 words were recognised as coherent English, and the
few lower-confidence words fit their context. Only the spoken words are used on screen; nothing was
invented.

## 2. Art direction

*Victorian line art on ink.* The visuals are thin brass line drawings (tower, mill, city, dials) on near-black
ink, with three colours that each carry a meaning:

- **Brass** is the tower: the official, owned version of time.
- **Red** is the lie: stolen minutes, "LIED", the wedges cut out of each dial.
- **Cyan** is the truth: the clock maker and his pocket watch. The watch's second hand ticks once per real second.

The type system has three voices: *Instrument Serif* for narration and character, *Inter Black* for
hard claims, and *JetBrains Mono* for evidence (the log, the offsets, dates). The **circle** is the recurring
shape and is used for match cuts: the dial, the bell rings, the iris wipes, the pocket watch, the sun, the
calendar dials and the final clock. Film grain and a soft vignette sit over everything.

The format follows the repo's `style_bible.md`: 9:16, about 60 s, an early hook, and burned-in word-by-word
captions in the lower part of the frame. Its cartoon-character look is meant for AI video
generation, so this piece swaps it for an original motion-graphics look.

## 3. Structure and sync map

| Time | Narration | Visual |
|---|---|---|
| 0.0–3.3 | "A mill owner built a clock tower that **lied** to the entire city." | The dial draws on, then the tower grows. On "lied" the minute hand jumps 20 min, the rim flashes red, **LIED** slams in and the camera shakes. The city rises on "entire city". |
| 3.4–5.3 | "For 10 years, nobody noticed." | The camera pushes into the dial. The hands spin with an eased speed ramp and an angular smear, then stop. "nobody noticed." appears quietly. |
| 5.4–7.5 | "…almost nobody owned a watch," | The camera pulls back to the city. Small watches pop into the sky, then vanish one by one on "nobody owned a watch", leaving the one clock. |
| 8.3–11.2 | "…the tower **bell** told the whole city when to **start work**… **go home**" | Bell rings spread from the dial and light the windows as each ring passes. A split-flap board flips START WORK → GO HOME on the spoken words. |
| 11.6–13.4 | "and nobody argues with a **bell**." | On "bell", a final ring becomes an **iris wipe** into the cool night palette. |
| 13.2–17.0 | "…young clock maker… a **pocket watch** that never lost a second." | A cyan dot walks into town. The camera zooms in and the dot becomes the pocket watch (match cut). NEVER LOST A SECOND types in word by word. |
| 17.0–20.5 | "…for a week, writing down every time the bell rang." | The watch tucks into a corner and a week of columns appears. 28 tally marks are written in, the last landing on "rang". |
| 20.6–25.3 | "At dawn… **20 minutes fast**. At dusk… **25 minutes slow**" | The watch expands into a two-hand comparison dial (brass tower vs cyan truth) as the sun rises, then sets. Red wedges cut +20 and −25 minutes. FAST. and SLOW. rise on the words. |
| 25.4–29.8 | "…every worker was handing the owner **nearly an hour** of **free work** **every single day**." | The two wedges join into one 45-minute bite. Workers appear and red particles stream up into the wedge. The dial shrinks into a 35-cell calendar where every day loses the same 45 minutes. |
| 29.9–34.3 | "So he told the foreman, who **laughed**… **dropped** his sandwich. Clocks don't **lie**, kid." | Card 01. The title letters bounce on each syllable of the laugh. The sandwich falls apart under gravity on "dropped". The quote appears word by word. |
| 34.4–37.4 | "…the workers, who **looked** at him like he'd **insulted** their mothers." | Card 02. A grid of faces snaps its eyes to camera on "looked" and scowls on "insulted". |
| 37.6–40.8 | "…the mayor… the mayor **owned the mill**." | Card 03. MAYOR = MILL OWNER builds on the spoken words. |
| 40.9–46.4 | "He smiled… every number… one question. Whose clock is wrong, son? **Yours** or **mine**?" | A single smile arc, then the ledger numbers drift in and a large "?". On "Yours" the small cyan watch appears. On "mine" the brass tower dial looms over the frame. |
| 46.5–51.0 | "By Friday… left town with the only honest clock… in his pocket." | The camera pulls back from the dial to the city (match zoom). The cyan dot walks out of frame and the windows dim. |
| 51.1–57.7 | "In real life, factory inspectors in 1800s England… **forward** in the morning and **back** at night." | A paper page slides up for documentary mode, in an engraved ink style. A minute hand is turned forward, then back, with red arrows. |
| 57.8–60.66 | "In a city with only one clock, **the lie becomes the time**." | Ink floods back from the dial (iris). One clock remains. **LIE** morphs into **TIME** (L flips to T, M grows in) and the hands settle on twelve on "time". Fade to black at the end of the audio. |

## 4. Run it

The preview needs a local web server, because fonts don't load over `file://`:

```bash
cd clock-tower-video && python3 -m http.server 8000
```

Then open <http://localhost:8000/index.html>. Space plays and pauses, the arrow keys step one frame, and `?t=22` starts at 22 s.

To render, install Playwright (Chromium) and ffmpeg first:

```bash
node render.mjs
```

```bash
node render.mjs --from 20 --to 30
```

```bash
node render.mjs --stills 1.9,22.5,60.2
```

The first command writes `out/clock-tower.mp4`, the second renders only a time range, and the third renders stills.
Options: `--workers 4` (parallel pages) and `--sub 3` (motion-blur sub-frames averaged over a 180° shutter).

To retime against a different voice take, regenerate `assets/words.js`. Every cue in `scene.js` is
looked up by word (the `Q` table), not hard-coded.

## Files

- `scene.js`: all scenes, camera keyframes and type animation
- `index.html`: preview player and the frame hook used by the renderer
- `render.mjs`: headless frame renderer plus the ffmpeg mux
- `assets/narration.mp3`: the uploaded track; `assets/words.js` holds the word timings
- `fonts/`: Instrument Serif, Inter and JetBrains Mono (SIL Open Font License)
- `clock-tower.mp4`: the rendered result

# Visual grammar: how the reference turns each sentence into a shot

Source: the 3 reference videos. Method:
- `analysis/shots.py`: tracks features at 10 fps and measures every shot's camera move (zoom, pan, tilt) and lighting (brightness, warmth, saturation).
- `analysis/cue_sheets.py`: 3 frames (start, middle, end) for every SRT line, so each sentence can be matched to its picture. Video 3 has no SRT, so it was read from 1 fps frames and burned-in captions.

This is a rulebook, not model training: Claude reads it and applies it to every new voiceover.

## 1. Measured numbers

| What | Value |
|---|---|
| New visual per narration line | about 1 per SRT line, every **~2 s** (shots measured 0.9-2.2 s median per video) |
| Push-in | **55%** of shots. Median **1.3x per shot**, about **0.17x per second** at a near-constant speed; 1.5-3x on a reveal |
| Pull-out | **32%**. Median 0.77x. Used to reveal context or end a scene |
| Slow drift | 6% |
| Static hold | 3%. Only on emotional beats ("gone.") |
| Pans / tilts | ~2%. Rare |
| Push-in direction | 88% drift **upward**: the camera pushes toward a face or object, usually off-centre, not a dead-centre zoom |

Measured with the caption band masked out (`analysis/shots.py`); static captions otherwise hide the camera move. Tracker checked on a synthetic 1.5x zoom: it reads 1.49-1.50.
| Transitions | Soft cross-dissolve 0.3-0.4 s between almost every shot |
| Lighting | Brightness mostly 0.34-0.57 (mid-dark, never flat bright). Saturation 0.34-0.51 |

The camera never sits still. A shot with no move is a deliberate pause.

## 2. Sentence type → shot (rules)

| # | When the sentence... | Show | Camera | Character | Example in reference |
|---|---|---|---|---|---|
| 1 | Opens with a bold claim (the hook) | A **symbol object** for the idea, big and close | Fast push-in | Character appears second, reacting | "impossible to get fired" → giant red **FIRE** button, then boss grinning holding a key |
| 2 | Names a concrete thing (clock, phone, desk, bucket, police) | **That exact object**, close up, as an insert | Push-in on it | None or a hand | "ticking clock" → clock insert; "steel balls" → stacked buckets |
| 3 | Names an abstract idea (law, rule, money, time) | A **physical metaphor** with a label | Push-in | Optional | "law" → padlock labelled LABOR LAW on a fire alarm; "on paper nobody gambles" → clipboard "GAMBLING: NONE ☑" |
| 4 | Says "Imagine..." / "you" | Introduce the **you** character in the place, medium-wide | Track or push with them | Neutral, looking around | "Imagine your boss walks you past your desk" → walk through office |
| 5 | Quotes someone ("your boss says") | **Close-up of the speaker** looking at camera | Push-in on face | Big expression snap on the key word | "is nothing." → boss holds up an empty gift box, toothy grin |
| 6 | Is a punchline or ironic thought | **Close-up face to camera**, often holding the prop | Short push, then hold | Exaggerated reaction (grin, shock) | "wait, I'm getting paid for this?" → grin at camera with a phone showing pay |
| 7 | Contains a list ("cookies, chocolate, shampoo...") | **Same framing**, one item per word | Slight drift | Picks each item, expression changes each beat | prize counter items |
| 8 | Marks time ("every Friday", "one Monday", "a week") | **Calendar page** or time-lapse | Push-in on date | None | "Every Friday" → calendar NOV FRI 25 |
| 9 | Moves to a new place | **Establishing wide**: aerial, street or one-point corridor | Push-in or crane down | Small in frame | "almost every street" → neon city aerial; "inside" → long pachinko aisle |
| 10 | Is a twist or loss ("then... he's gone") | **Empty space** where the thing was | Static hold or very slow push, 2-3 beats | Absent, or small and confused | empty desk, chair pushed in |
| 11 | Explains why ("You see, ...") | **Lighting change** to darker blue with one warm lamp; the "explainer" character in a new set | Pull-out to reveal | Smug or calm, talks to camera | boss in blue corridor with lamp |
| 12 | Shows group reaction | Crowd in one row, all turn **in sync** | Push toward the protagonist | Same expression snap together | co-workers staring |
| 13 | Ends the story | **Return to an earlier location or symbol** | Pull-out or push to a sign | Small, alone | CAREER DEVELOPMENT ROOM door; police with clipboard |

## 3. Composition
- Subject sits in the middle or lower-middle third, leaving the caption zone (about 70% down) readable.
- **Foreground framing** for depth: a shoulder, a head, a cat or a desk edge cut off at the frame edge and slightly blurred.
- Characters break the fourth wall: punchlines are delivered looking straight at the camera.
- Strong depth of field: the background is softer than the subject in close-ups.
- One-point perspective for long spaces (corridors, aisles, streets).

## 4. Character performance
- Expressions **snap on the key word** of the sentence, not at the start of the shot.
- Recurring set: deadpan, smirk (half-lid + one brow), shock (circle eyes), toothy grin (boss), happy arcs, laugh with tears, angry brows, sad brows.
- Bodies mostly hold a pose with a small idle sway. Big actions are short: lean back, point, raise a prop, lie back with sunglasses.
- Props are held up to the camera when they matter (phone, box, tokens).

## 5. Lighting by mood (measured warmth: positive = warm, negative = cool)
| Mood | Look | Reference |
|---|---|---|
| Normal / neutral | Cool white daylight, green or white walls | office (warmth −0.1 to −0.2) |
| Happy, reward, paradise | Warm yellow sun patch or golden glow | corner guy, prize counter (+0.2 to +0.3) |
| Menace, explanation, the system | Deep blue with **one warm lamp** spotlight | boss corridor (−0.3 to −0.45, saturation up to 0.79) |
| Night / city | Blue-purple with pink and cyan neon, wet reflections | v2 streets |
| Loss, emptiness | Cool, desaturated, quiet | empty desk |
| History / legend | Warm golden or sunset palette | v3 ending landscapes |

## 6. Rhythm of a ~60 s video
1. 0-5 s: hook claim + symbol object + main character reaction.
2. 5-20 s: "Imagine / you" setup in the main location, 1 visual per line.
3. 20-40 s: escalation, with time markers (calendar), lists and crowd reactions.
4. 40-50 s: twist (empty space, hold) then "You see," explanation with the lighting change.
5. 50-60 s: closing line on a returning symbol, pull-out, fade.

## 7. How to apply to a new voiceover
1. Transcribe and split into sentences with times.
2. Tag each sentence with a rule number from section 2 (a long sentence gets 2-3 visuals, one per clause, about every 2 s).
3. Pick the camera from the rule, then the lighting from section 5 by mood.
4. Put the expression snap on the key word's timestamp.
5. Join every shot with a 0.3-0.4 s cross-dissolve and a whoosh.

## 8. Checking a render against the reference
Run `python3 analysis/shots.py <video> out.json` on the new video and compare with the reference numbers in section 1.

Clock-tower video (v2), measured the same way:

| | Reference | Clock tower v2 |
|---|---|---|
| Push-in / pull-out | 55% / 32% | 75% / 25% |
| Zoom speed | 0.17x per second | 0.16x per second |
| Push-ins drifting up | 88% | 100% |
| Seconds per visual | ~2 s | ~3.2 s (too long: split long sentences into 2 visuals) |
| Holds on emotional beats | 3% | none |

`animator/engine.py: ref_camera()` applies section 1 to every shot. Give each shot a `focus` (the face or object to push toward) and a `cap` for busy frames.

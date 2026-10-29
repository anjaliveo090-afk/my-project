# Master prompt: new voice → same-style animated short

Copy everything inside the box into a new Claude Code chat on the repository
`anjaliveo090-afk/my-project`, and attach your voiceover (mp3/wav), plus the script if you have it.

```
I am attaching a voiceover. Make a 9:16 animated short from it in exactly the same style
as the clock-tower video in this repository.

SETUP
- Work on branch `claude/dazzling-hypatia-7p55ue` (all the tools live there; fetch and check it out first).
- Read these before doing anything else, and follow them strictly:
  CLAUDE.md, style_bible.md, visual_grammar.md (all sections, especially 2, 3, 8, 10),
  animator/README.md, assembler/README.md. For the kings/medieval look also read
  style_medieval.md and use animator/style3.py + animator/medieval.py.
- Use animator/clock_tower2.py and animator/job_room.py as templates to copy (office sets and props are in animator/office.py). Do not change engine.py or style2.py
  unless something is broken.

STEP 1 - WORDS
- Get word-level timings with `python3 analysis/align_words.py <voice> <script.txt|subs.srt> output/<story_name>`
  (pocketsphinx offline; Hugging Face downloads are blocked here). If I gave a script, align it to
  the voice. If not, transcribe and show me the cleaned script so I can correct words.
- Save script.txt, aligned.json and captions.srt in output/<story_name>/.

STEP 2 - VISUAL PLAN (show it to me before rendering)
- Split the narration into phrases of 2-4 words.
- Tag each sentence with a rule number from visual_grammar.md section 2, and plan a table:
  time | phrase | what is on screen | camera move (crane/drone up, pull back, push in,
  pan/tilt following an object, track with a character, insert close-up) | character +
  expression | lighting/mood.
- The camera must ARRIVE on the word it illustrates (example: "A mill owner" = the owner;
  "built" = camera cranes up the tower; "the clock tower" = the clock).
- Dissolve only when the location changes; the camera keeps moving through it.

STEP 3 - BUILD
- Create animator/<story_name>.py from clock_tower2.py: new worlds (scenes), Char2
  characters in the user's reference style (thick dark limbs, dark ball hands, big dark
  shoes, tall oval eyes, thick brows, smooth fringe with highlights, collared clothes, soft
  shading), keyframed camera `keys` on word times, dof on character shots, over-the-shoulder
  (back_figure) and dutch angles where they fit.
- Composition: the main subject (face or key object) must stay between y 250 and 820 of
  720x1280, never in the bottom area where Shorts captions and the Subscribe button sit.
- Lighting by mood from visual_grammar.md section 5 (warm = happy, deep blue + one lamp =
  menace/explanation, cool desaturated = loss, neon = night city, golden = history).

STEP 4 - DEFAULTS (my settings from the last video)
- NO lip-sync: render with --no-lipsync; characters hold expressions that fit the moment
  and snap on key words.
- NO captions (do not pass --srt to the assembler).
- NO camera whoosh SFX: drop every whoosh.wav cue.
- All other SFX at 10% of their cue volume (≈ -13 dB under the voice, as measured on the reference). Background music: animator/audio.py music_ref() at --music-volume 0.4 (≈ -20 dB under the voice, D minor, no drums). Read sound_design.md.
- Synthesised SFX and music only (animator/audio.py), never copied from the reference channel.

STEP 5 - CHECK BEFORE SENDING
- Render a contact sheet of a frame at every camera key and look at it: subject centred,
  nothing important cut off or outside the scene, no empty/black areas.
- Run analysis/flow.py on the caption-free animation: camera median should be about 6-15
  and mean about 10-24 (% width per second), like the reference.
- Then render, assemble, and send me the final mp4. Commit and push the code
  (output/ is git-ignored).

Tell me honestly what could not match the reference (it is 2D code animation, not a 3D
AI render).
```

## Notes
- The new chat only works on this branch: everything (engine, characters, rules) is on
  `claude/dazzling-hypatia-7p55ue` and not merged into the default branch.
- The reference videos are not needed again: their analysis is saved in `style_bible.md`
  and `visual_grammar.md`.
- A 60 s video takes a while: new scenes have to be drawn for every new story.

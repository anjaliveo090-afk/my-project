# Master prompt: reference videos → a complete repo for that style (any account)

Use this when you want a new style from your own reference videos, from **any** Claude or
GitHub account (yours, a team member's, a student's). Claude builds the whole repo itself, like
`github.com/anjaliveo090-afk/my-project`, and writes the voice + SRT master prompt for it.

## What you do (4 steps, one time)
1. **Make an empty repo.**
   - On **github.com**, click **+** (top right), then **New repository**.
   - Give it a name (for example `ramen-style-shorts`).
   - Tick **Add a README file** and click **Create repository**.
2. **Connect it to Claude.**
   - Open **claude.ai/connect-github**, click **Connect GitHub**, and allow that new repo.
   - In the **Setup script** field of the environment, add `bash setup.sh || true` (optional, it makes later chats start faster).
3. **Open a session.** Open **claude.ai/code** and choose the new repo.
4. **Attach and send.**
   - With 📎, attach 3-8 **reference videos** (mp4).
   - Also attach their **SRTs** if you have them, and 2-5 clear **character / background images**.
   - Copy everything inside the box below, paste it, and send.

Claude takes 1-2 hours. It shows you the character sheet and a sample video, and then opens a
**pull request**. Open it on GitHub and click **Merge**.

After that, every video needs only: choose the repo, attach **voice + SRT**, and send:
```
I am attaching a voiceover and its SRT. Run bash setup.sh, then read MASTER_PROMPT.md
and follow the prompt inside it exactly.
```

---

```
I am attaching reference videos (and maybe SRTs and character/background images) of ONE
visual style. Build this repository into a complete toolkit that turns any voice + SRT into
a 9:16 animated short in EXACTLY this style, the same way the public repo
github.com/anjaliveo090-afk/my-project does for its styles. Work step by step and show me
progress.

STEP 0 - BOOTSTRAP THE TOOLKIT (copy, don't rewrite)
- git clone --depth 1 -b claude/dazzling-hypatia-7p55ue https://github.com/anjaliveo090-afk/my-project /tmp/kit
- Copy into this repo:
  - /tmp/kit/animator/engine.py and /tmp/kit/animator/audio.py → animator/
  - /tmp/kit/analysis/*.py → analysis/
  - /tmp/kit/assembler/ → assembler/
  - /tmp/kit/setup.sh, requirements.txt, .gitignore → repo root
- Copy as worked examples, into reference_examples/: CLAUDE.md, MASTER_PROMPT.md,
  visual_grammar.md, sound_design.md, style_bible.md, style_medieval.md,
  animator/gambling.py, animator/arcade.py, animator/office.py, animator/style2.py,
  animator/job_room.py, animator/spear_shield2.py, animator/style3.py, animator/medieval.py.
  Read them to learn the method: literal visual per phrase, keyframed camera landing on words,
  measured sound targets, contact-sheet checks.
- Run `bash setup.sh` (installs packages, ffmpeg, and the voice/music separation model).

STEP 1 - ANALYSE THE REFERENCES (frame by frame + sound)
For every reference video run:
  - analysis/frame_log.py <video> [srt] <out> 4   (4 fps contact sheets with the spoken line; LOOK at every sheet)
  - analysis/audio_ref.py <video> [srt] <out>     (every SFX: time, kind, loudness vs voice; music key/tempo/level)
  - analysis/new_visuals.py <video>               (how often the visual changes)
  - analysis/flow.py <video>                      (camera speed)
Then write:
  - style_bible.md:
    - format and safe zones
    - characters measured in head-widths: head shape, body, limb thickness, hands, feet, height ratios, outline colour and width, light direction, shading, rim light
    - faces and the expression set
    - palette (hex)
    - sets and backgrounds, depth of field, lighting by mood
  - visual_grammar.md:
    - measured pace and camera numbers
    - a table of "sentence type -> what is shown -> camera -> character reaction", with examples from these references
  - sound_design.md:
    - measured music: level vs voice, key, tempo, drums
    - measured SFX: per 10 s, loudness, kinds, what triggers them, on cuts or not
    - the target numbers to check a render against
  - analysis/ref_data/*.json (the analysis outputs)

STEP 2 - BUILD THE STYLE IN CODE
- animator/style.py: a character class with the SAME draw() signature as
  reference_examples/animator/style2.py Char2 (x, y, s, expr, t, arms, pose, look, bob,
  item, item_hand, walk_phase, lean, shadow), so the story template works unchanged.
- animator/sets.py: the backgrounds and props this style uses.
- If the music differs from audio.music_ref(), add a function to animator/audio.py that
  matches the measured key/tempo/density, and check it with audio_ref.py.
- Render a test sheet: each character × all expressions × main poses, next to my images.
  Compare and fix until proportions, line weight, colours and shading match. Show me the sheet.

STEP 3 - SAMPLE VIDEO
- Write animator/sample.py modelled on reference_examples/animator/gambling.py:
  - a 20-30 s made-up narration in the references' tone
  - a literal visual for every 2-4 words, with the camera arriving on the key word
  - about one SFX per visual event
- Render it, assemble with assembler/assemble.py (music + SFX at the measured levels).
- Measure it with new_visuals.py, flow.py and audio_ref.py. Fix anything outside the
  reference range, then send me the mp4.

STEP 4 - WRITE THE INSTRUCTIONS FOR FUTURE CHATS
- CLAUDE.md: the workflow for this repo. When the user gives voice + SRT:
  1. align words (analysis/align_words.py)
  2. plan the shots with visual_grammar.md
  3. build animator/<story>.py from sample.py
  4. check a contact sheet
  5. render and assemble
  6. measure against sound_design.md / visual_grammar.md
  7. send the mp4
  8. patch only the needed shots on fix requests
  Defaults:
  - no captions
  - no lip-sync unless the references clearly lip-sync
  - no camera whoosh unless the references use them
- MASTER_PROMPT.md: the voice + SRT prompt for this repo, in the same structure as
  reference_examples/MASTER_PROMPT.md but pointing to style.py / sets.py / sample.py and this
  style's measured targets. No branch checkout line: everything will be on main.
- README.md: what this repo is, plus the short message for a new chat:
  "I am attaching a voiceover and its SRT. Run bash setup.sh, then read MASTER_PROMPT.md and follow the prompt inside it exactly."

STEP 5 - PUBLISH
- Commit and push your branch, then open a pull request into main and give me the link so I
  can click Merge.

RULES
- Copy the STYLE only. Never copy the reference channel's characters, logos, text or SFX files.
- Be honest about limits: this is 2D code animation (pycairo, optional Blender plates).
  3D or AI-rendered references are approximated in look; pace, camera, sentence->visual
  logic and sound levels can match closely.
```

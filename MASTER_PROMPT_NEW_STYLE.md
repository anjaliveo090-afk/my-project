# Master prompt: teach this repo a NEW style (one time)

Use this in a NEW repository created from this one (see NEW_STYLE_GUIDE.md).
1. Attach 3-8 reference videos of the new style, their SRTs if you have them, and 2-5 clear character/background images.
2. Paste the text inside the box below.

```
This repository is a copy of my animated-shorts toolkit. I am attaching reference videos
(and images) of a NEW style. Teach the repository this new style so that afterwards I can
send only a voice + SRT and get a video in exactly this new style.

SETUP
- Check out branch `claude/dazzling-hypatia-7p55ue` (all the tools are there), then create
  your own working branch from it. Run `bash setup.sh`.
- Read CLAUDE.md, visual_grammar.md, sound_design.md, style_bible.md, animator/README.md first.
  They describe the PREVIOUS style; keep the method, replace the style.
- Reusable, do not rewrite:
  - animator/engine.py (render, key_camera, dof, grain)
  - animator/audio.py (synth SFX + music_ref)
  - assembler/assemble.py
  - analysis/*.py

STEP 1 - ANALYSE THE REFERENCES (frame by frame + sound)
- For every video:
  - analysis/frame_log.py video [srt] out 4  (4 fps contact sheets; LOOK at every sheet)
  - analysis/audio_ref.py video [srt] out    (SFX times/kinds/loudness, music key/tempo/level)
  - analysis/new_visuals.py video            (how often the visual changes)
  - analysis/flow.py video                   (camera speed)
- Write style_<name>.md (pick a short name for the style):
  - format and framing
  - characters, measured in head-widths: head shape, body, limbs thickness, hands, feet, height ratio, outline colour and width, shading/light direction, rim light
  - faces and the expression set
  - colour palette (hex)
  - sets/backgrounds and depth of field
  - lighting by mood
  - camera moves, transitions, and pace numbers
- Update sound_design.md with the new measured music/SFX numbers. Keep the same table format.
- Add every new "sentence type -> shot" rule you see to visual_grammar.md (new section).
- Save the analysis JSONs to analysis/ref_data/.

STEP 2 - BUILD THE STYLE IN CODE
- animator/style_<name>.py: a character class with the SAME draw() signature as
  style2.Char2 (x, y, s, expr, t, arms, pose, look, bob, item, walk_phase, lean, ...), so all
  templates keep working.
- animator/sets_<name>.py: backgrounds and props of this style.
- Render a test sheet: every character × the expressions × the poses, next to the
  reference images. Compare and fix until proportions, line weight, colours and shading match.
  Show me the sheet.

STEP 3 - PROVE IT WITH A SAMPLE
- Make a 20-30 s sample video (a short made-up narration, or the first lines of one reference
  SRT re-voiced is not needed: silent animation + music + SFX is fine).
- Copy the structure of animator/gambling.py: a literal visual per 2-4 words, the camera
  arriving on key words, ~1 SFX per second.
- Measure the sample with new_visuals.py, flow.py and audio_ref.py, and compare with the
  reference numbers. Fix anything outside the range. Send me the sample mp4.

STEP 4 - MAKE IT THE DEFAULT
- Rewrite CLAUDE.md and MASTER_PROMPT.md so that a new chat with "voice + SRT" uses
  style_<name>.py, sets_<name>.py, style_<name>.md and the sample as the template.
  Keep the old code files, just stop pointing to them.
- Commit and push your branch. Tell me the branch name, and offer a pull request into main
  so later chats need no branch name.

RULES
- Copy the STYLE only, never the reference channel's characters, logos or SFX files.
- Tell me honestly what cannot match: this is 2D code animation, so a 3D/AI-rendered
  reference is only approximated.
```

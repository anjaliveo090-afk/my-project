# Project: reference-style animated shorts

When the user gives a voiceover, SRT or script, follow this workflow without being asked.

1. Read `style_bible.md` (the analysed look of the 3 reference videos: format, characters, face reactions, camera, pacing, STYLE LOCK, CLIP TEMPLATE).
2. If only audio is given, get an SRT first (ask the user for CapCut auto-captions, or transcribe with a speech-to-text tool if installed).
3. Run `python3 assembler/plan_clips.py <srt>` to split the narration into 10 s clips with speed and SFX hints.
4. For each clip write a detailed prompt: STYLE LOCK + characters + 3-4 timed shots (camera move, action, face reaction, soft cross-dissolve). Keep the same character looks across clips. Give Image-mode prompts for each character and location so the user can use them as Flow Ingredients.
5. Give an SFX cue sheet per clip (whoosh on cuts, ticks, stings), as `sfx_cues.example.json` format.
6. After the user generates clips in Flow (9:16, Omni, 10 s) and saves them, assemble with `assembler/assemble.py` (see `assembler/README.md`).
7. If the user shares a generated frame, compare it with the Style Bible and fix the prompt.

Without Flow: `animator/` draws the whole video in code (see `animator/README.md`); use it when the user wants Claude Code to make the video itself.

Limits to state honestly: Claude Code cannot generate the AI video; Flow's Omni does. Face consistency needs Ingredients images. Do not copy the reference channel's characters or SFX files, only the style.

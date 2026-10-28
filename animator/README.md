# Animator

Code-drawn version of the reference style (no AI video model): big-head stick characters, moving camera, cross-dissolves, synthesised SFX and music.

- `engine.py`: characters, expressions, props, backgrounds, camera, render to mp4.
- `audio.py`: synthesised SFX (`whoosh`, `tick`, `bell`, `pop`, `sting`, ...) and a music bed.
- `style2.py`: characters in the user's reference style (measured from their sheets: thick limbs, dark ball hands, big dark shoes, tall oval eyes, smooth fringe with highlights, collared outfits, soft shading) and `back_figure` for over-the-shoulder shots.
- `clock_tower.py`: one story (19 shots timed to the voiceover) + its SFX cue sheet.

## Make the clock-tower video
```bash
O=output/clock_tower
python3 animator/audio.py $O/sfx 60.66
(cd animator && python3 clock_tower.py ../$O/clips/animation.mp4 ../$O/cues.json ../voice.mp3)  # voice drives lip-sync
python3 assembler/assemble.py --clips $O/clips --voice voice.mp3 --srt $O/captions.srt --words 2 \
  --sfx $O/cues.json --sfx-dir $O/sfx --music $O/sfx/music.wav --music-volume 0.2 --crf 23 \
  --out $O/clock_tower_final.mp4
```
Captions come from a word-timed SRT (2 words per cue). For a new voiceover, copy `clock_tower.py`, change the shot `start` times to the new sentence times, and redraw the scenes.

Needs `pycairo`, `numpy`, `ffmpeg`.

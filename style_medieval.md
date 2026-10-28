# Style: medieval kingdoms (second reference)

Source: 5 frames the user shared (kings at a war table, king in a field with an army,
aerial river with two armies and a bridge, "YEARS AT WAR 100" sign, sweating blacksmith).
Code: `animator/style3.py` (characters), `animator/medieval.py` (sets and props).
Use this style when the user asks for the "kings / medieval / war" look.

## Characters (`style3.Char3`)
- **Head:** big cream-white egg (`#fcf6ef`), dark brown outline (`#2e2226`), soft grey shade at the lower edge. No skin colour, no hair on most characters.
- **Proportions (measured):** head : body : legs = 1 : 1.35 : 1.1 for tunics. Robes reach the ankles (body about 2 head-heights). Body width about 0.8 of the head width.
- **Body:** bean shape (narrow rounded shoulders, widest in the middle). Robes flare at the hem; capes hang behind in a darker shade.
- **Limbs:** thin dark sticks, small dark ball hands, small dark oval feet.
- **Face:** small black oval eyes, **thick expressive brows** (they carry the emotion), short line mouth. Clean shapes for facial hair: handlebar moustache (blacksmith), pointed goatee (kings), long white beard (old man).
- **Identity by colour:** two sides, **red** (`#e84a36`, cape `#ac575d`, gold crown) vs **teal** (`#3aa6a0`, silver crown). Soldiers wear grey helmets and teal-gold or red shields.
- **Props in hands:** spear with red tassel, round shield (gold rim, teal ring, silver boss), walking stick, hammer, money bags.
- **Reactions:** sweat drop and shake lines when nervous, smug half-lidded eyes for the confident king, closed arc eyes when happy.

## Sets (`medieval.py`)
- **Painted backdrop, out of focus:** blue sky gradient (`#5f88d0` → `#a9cdf3`), puffy white clouds with lavender undersides, blue mountains with snow caps, castles with red and teal roofs, green hills and trees. Always drawn through `blurred()` with a light haze, so characters pop.
- **Sunlit stone terrace:** warm tiles (`#d6bd9f`) in perspective, long diagonal shadows from every character and prop (`cast_shadow`), stone parapet with scratched tally marks (time passing).
- **Props:** red/teal banners on poles, anvil on a tree stump (sparks), barrel full of spears, round red/teal war table as a foreground frame, "YEARS AT WAR" flip-number sign, rusty helmets with flowers growing out of them.
- **Battlefield:** farmland with crop rows and a dirt track running to the vanishing point, rows of soldiers receding.
- **Aerial:** river running away from camera (narrower far away), patchwork fields, two dense armies with flags on each bank, stone bridge across the lower third, a tiny duck family in the river.

## Camera angles (one per reference frame)
1. **Eye-level group shot on the terrace:** characters fill the frame from the waist up to the crowns, a foreground object at the bottom edge (war table, anvil) for depth, blurred landscape behind.
2. **Low ground angle:** camera almost at grass level, big blurred grass and flowers in front, a character mid-frame, an army line receding into the distance.
3. **High aerial (drone):** looking down the river; the tiny characters on the bridge are the story, the armies give scale. Good for reveals ("finally", "for 100 years").
4. **Prop close-up with story detail:** the sign fills the frame, a character beside it, foreground details that tell time passed (flowers growing in old helmets).
5. **Action medium:** one character reacting (sweat, shaking), others framing him on both sides, motion lines.

Everything in `visual_grammar.md` still applies: a new framing every 2-4 words landing on the key word, crane/drone moves between framings, subject between y 250 and 820, default no lip-sync, no captions, no whoosh, SFX at 10%.

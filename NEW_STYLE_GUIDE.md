# Naya style (naye characters + visual look) ke liye nayi repo kaise banayein

Is repo ka engine, camera, sound aur analysis tools har style mein kaam aate hain.
Naye style ke liye inki copy (nayi repo) banti hai, aur Claude usme sirf naya character, naye sets aur naye rules jodta hai.

## Step 1: Nayi repo banao (5 minute, sirf ek baar)
1. **github.com/anjaliveo090-afk/my-project** kholo.
2. **Settings** mein jaao. **General** ke andar sabse upar **Template repository** ✔ kar do. Yeh sirf pehli baar karna hai.
3. Repo ke main page par hara button **Use this template** dabao, phir **Create a new repository**.
4. Details bharo:
   - **Repository name:** naya naam, jaise `shorts-style-b`
   - **Include all branches:** ✔ zaroor lagao, kyunki saara kaam branch `claude/dazzling-hypatia-7p55ue` par hai.
   - **Public ya Private:** jo chaho.
5. **Create repository** dabao. Ab aapke paas `aapka-naam/shorts-style-b` hai.

## Step 2: Claude se jodo
1. **claude.ai/connect-github** kholo, **Connect GitHub** dabao, aur nayi repo ko **Allow** karo.
2. **claude.ai/code** kholo aur nayi repo `shorts-style-b` chuno.
3. Session ke upar environment ke naam par click karo, phir **Edit**. **Setup script** mein `bash setup.sh` likhkar save karo.

## Step 3: Claude ko naya style sikhao (sirf ek baar, 1-2 ghante)
Nayi session mein yeh cheezein attach karo:
- Us style ki **3 se 8 reference videos** (mp4). Jitni zyada, utna accha.
- Unki **SRT**, agar ho. Na ho to bhi chalega.
- Characters aur background ki **2 se 5 saaf images**, jaise character sheet ya screenshot.

Phir `MASTER_PROMPT_NEW_STYLE.md` file mein box ke andar wala poora text paste karke **Send** karo.

Claude yeh sab khud karega:
- Videos ko frame-by-frame aur sound ke saath analyse karega.
- Naya character aur sets banayega, aur unhe reference images se milayega.
- 20-30 second ki test video banayega.
- Sab memory files mein save karke push karega.

Test video dekhkar jo galat lage, usi chat mein batao. Jaise *"haath patle hain"* ya *"rang zyada dark hai"*. Claude sudhaar dega.

## Step 4: Ab har video ke liye (pehle jaisa hi)
Nayi session mein repo `shorts-style-b` chuno, **voice + SRT** attach karo, aur yeh message bhejo:

```
I am attaching a voiceover and its SRT. Run bash setup.sh, then read MASTER_PROMPT.md
and follow the prompt inside it exactly to make the video in this repo's style.
```

Agar Step 3 ka kaam abhi `main` mein merge nahi hua hai, to message ki shuruaat mein yeh line jodo:
`Checkout the branch where the new style was built.`
Step 3 ke ant mein Claude batayega ki woh branch kaunsi hai.

## Dhyan rakhne wali baatein
- **Har style ki apni repo.** Ek repo mein sudhaar karne se doosri mein khud nahi aata.
- **Reference sirf style ke liye hai.** Characters aur SFX copy nahi hote, sirf style seekha jata hai.
- **3D reference ho to look kitna milega:** agar reference AI ya 3D se bani hai, to Claude ki 2D code animation look mein milti-julti hogi, bilkul same nahi. Speed, camera, sentence se visual ka logic aur sound ke numbers reference jaise hi honge.
- **Students ko dene ke liye:** nayi repo ka link do aur `MASTER_PROMPT.md` wale steps batao. Woh **Use this template** ya **Fork** karke apni copy banayenge.

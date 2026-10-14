# Ma‘at logo — image-generation prompts

For **GPT Image / ChatGPT**. Run one prompt per variant, in a new chat each time. After prompt 1 gives a figure you like, attach that image to prompts 2–4 and add: *"Use the attached figure exactly; do not redesign it."*

**Brief:** Ma‘at, the ancient Egyptian goddess of truth and justice, drawn the way New Kingdom tomb paintings show her (e.g. the tomb of Nefertari): kneeling in profile with winged arms spread, and her ostrich feather on her head. She keeps her original painted colors and feather detail, redrawn as a clean, flat logo.

**Original Egyptian pigment palette:**

| Part | Color |
| --- | --- |
| Skin | yellow ochre `#D9A441` |
| Hair / wig, outlines | carbon black `#1C1C1C` |
| Sheath dress | linen white `#F2EBDD` |
| Wing feather bands, collar | Egyptian blue `#2B5FA8`, malachite green `#3E8E63`, red ochre `#B23A2A` |
| Ostrich feather on her head | white with black outline and a central shaft |
| Jewelry, headband | gold `#C9962B` |

---

## 1. Symbol only (master mark)

```text
Design a flat vector logo mark of Ma'at, the ancient Egyptian goddess of truth and justice, faithful to how she appears in New Kingdom tomb paintings such as the tomb of Nefertari.

Posture: Ma'at kneels in strict Egyptian profile facing right — head, legs and feet in profile, shoulders shown frontally, one knee raised. Both arms are stretched out horizontally to the sides, and each arm carries a long wing hanging from it, the wings spread wide in a symmetric, protective span.

Feather details: each wing has the traditional layered structure — near the arm, two or three rows of small rounded covert feathers like overlapping scales; below them, long straight primary feathers running to the wing tip, separated by thin black lines. The feathers are painted in repeating bands of Egyptian blue, malachite green and red ochre, exactly like the tomb paintings. On her head, held by a gold headband, stands a single tall white ostrich feather with a black outline, a visible central shaft, and its tip curling forward.

Figure colors (original Egyptian pigments): skin yellow ochre #D9A441; straight black wig #1C1C1C; close-fitting white linen sheath dress #F2EBDD; broad collar necklace and armbands in Egyptian blue #2B5FA8, malachite green #3E8E63 and red ochre #B23A2A; gold #C9962B jewelry; thin carbon-black #1C1C1C outlines around every shape, as in Egyptian painting.

Style: clean flat vector logo — solid color fills, crisp black outlines, simplified but historically accurate shapes. No gradients, no shading, no 3D, no texture, no cracked-plaster or aged effect, no photorealism.

Background: flat deep lapis blue #14213D. Figure centered with generous even margin, square 1:1 canvas. No text, no hieroglyphs, no border, no frame, no extra objects; she holds nothing.
```

## 2. Horizontal lockup — on lapis

```text
Create a horizontal logo lockup for an app called "Ma‘at".

Left: the Egyptian goddess Ma'at as in New Kingdom tomb paintings — kneeling in profile facing right, arms stretched out with long wings spread wide in a symmetric span. Traditional feather structure on each wing: rows of small scale-like covert feathers near the arm, then long primary feathers in repeating bands of Egyptian blue #2B5FA8, malachite green #3E8E63 and red ochre #B23A2A, separated by thin black lines. A tall white ostrich feather with black outline and central shaft stands on her head, held by a gold headband. Skin yellow ochre #D9A441, black wig, white linen sheath dress #F2EBDD, colorful broad collar, gold #C9962B jewelry, thin black #1C1C1C outlines. Flat vector, solid fills, no gradients, no texture, no aged effect. She holds nothing.

Right: the wordmark "Ma‘at" — exactly these five characters: capital M, lowercase a, a curly left single quotation mark ‘ (representing the Arabic letter ayn), lowercase a, lowercase t. Set in an elegant high-contrast editorial serif typeface (in the style of Instrument Serif or Didot), regular weight, natural letter spacing, in gold #C9962B. Cap height about 60% of the figure's height, vertically centered on it.

Background: flat deep lapis blue #14213D. Canvas: wide 3:1 rectangle with even padding. No tagline, no other text, no border, no shadows.
```

## 3. Horizontal lockup — on cream

```text
Create the light-background version of the "Ma‘at" logo lockup.

Left: the same Egyptian goddess Ma'at as in New Kingdom tomb paintings — kneeling in profile facing right, arms stretched out with long wings spread wide in a symmetric span. Rows of small scale-like covert feathers near the arm, then long primary feathers in repeating bands of Egyptian blue #2B5FA8, malachite green #3E8E63 and red ochre #B23A2A, separated by thin black lines. A tall white ostrich feather with black outline and central shaft on her head, held by a gold headband. Skin yellow ochre #D9A441, black wig, white linen sheath dress #F2EBDD, colorful broad collar, gold #C9962B jewelry, thin black #1C1C1C outlines. Flat vector, solid fills, no gradients, no texture, no aged effect. She holds nothing.

Right: the wordmark "Ma‘at" — exactly these five characters: capital M, lowercase a, a curly left single quotation mark ‘, lowercase a, lowercase t — in an elegant high-contrast editorial serif typeface, regular weight, in deep lapis blue #14213D. Cap height about 60% of the figure's height, vertically centered on it.

Background: flat papyrus cream #F3EAD7. Canvas: wide 3:1 rectangle with even padding. No tagline, no other text, no border, no shadows, no paper texture.
```

## 4. App icon / favicon — simplified emblem

```text
Design an app icon of the Egyptian goddess Ma'at, simplified for very small sizes but keeping her original tomb-painting colors.

Subject: Ma'at's head in Egyptian profile facing right — yellow ochre #D9A441 skin, black #1C1C1C wig, gold #C9962B headband — with her tall white ostrich feather standing on her head (black outline, central shaft, tip curling forward). Below and around the head, one wide wing sweeps in a smooth crescent, made of four or five thick feather bands in Egyptian blue #2B5FA8, malachite green #3E8E63 and red ochre #B23A2A. No body, no arms, no fine facial detail.

Style: flat vector, solid fills, bold black outlines, large clear gaps between shapes so it still reads at 16 pixels. No gradients, no shading, no texture.

Tile: the emblem centered on a deep lapis blue #14213D rounded-square tile (corner radius about 22% of the tile width), filling about 70% of the tile. Square 1:1 canvas. No text, no letters, no border, no shadow, no glossy effect.
```

---

## After generating

- Check the wordmark's spelling **letter by letter**. If the ‘ comes out wrong, generate the symbol alone and set "Ma‘at" in Instrument Serif yourself (the poster's font).
- Compare the wings with a reference photo of Ma'at in the tomb of Nefertari (QV66): scale-like rows near the arm, long banded primaries below.
- For the favicon, export at 512×512 and check it still reads at 32 px and 16 px.
- To use it in the app, replace `page_icon="⚖️"` in `app.py` with the icon file's path.

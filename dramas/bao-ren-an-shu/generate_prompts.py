import os

style_anchor = "Dark cinematic historical drama, Han Dynasty Chinese setting, high contrast chiaroscuro lighting, deep shadows and warm firelight, rough textures, grimy and realistic aesthetics, incredibly detailed, highly dramatic and epic mood, 16.9 aspect ratio, 8k resolution"

base_char = "a gaunt middle-aged Chinese male character with messy grayish-white hair unbound without a crown, extremely hollow and deep eyes with bloodshot details, prominent cheekbones, wearing a torn and rough hemp grey Hanfu robe stained with dried dark blood"
clean_char = "a gaunt middle-aged Chinese male character with neat grayish-white hair, extremely hollow but proud eyes, wearing a clean pure dark green Han Dynasty official court robe"

scenarios = {
    "A": "inside an ancient cold stone prison cell, dimly lit by a flickering bronze oil lamp casting long shadows, rows of hanging bamboo slips inscribed with ancient Chinese characters in the background",
    "B": "inside a brutal medieval dungeon, thick iron bars, a heavy blood-stained wooden torture pillar in the center, dusty floor",
    "C": "in an absolute pitch-black void, floating ancient spectral ash and faint floating embers",
    "C2": "inside an ancient stone prison cell, a heavy wooden door pushed open, blinding bright morning sunlight flooding into the room",
    "D": "inside a massive and oppressive Han Dynasty imperial court, towering black pillars, ancient Chinese architecture, extremely intimidating atmosphere",
    "E": "outside in an ancient Chinese palace stone corridor during a heavy cold rainstorm, gloomy and desolate atmosphere"
}

shots = [
    {
        "id": "01", "bg": "A", "char": base_char,
        "action": "extreme close up of rough scarred hands holding a small bronze carving knife, writing on bamboo slips, a drop of blood falling from finger",
        "camera": "extreme close up, focus moving with the knife",
        "light": "deep shadows, high contrast, warm orange firelight against cold dark grey stone"
    },
    {
        "id": "02", "bg": "A", "char": base_char,
        "action": "close up of the man's tired face, dropping the bronze knife, looking up slowly towards a high window with incredibly hollow and deep eyes",
        "camera": "very slow push in towards his eyes",
        "light": "flickering directional firelight, deep cinematic shadows on half his face"
    },
    {
        "id": "03", "bg": "D", "char": clean_char,
        "action": "the single proud figure standing straight and alone in the massive court, while hundreds of other officials kneel down in fear in the dark background",
        "camera": "extreme wide shot, showing his tiny figure against the massive oppressive architecture",
        "light": "oppressive cold shadows, dramatic lighting from above, making the setting look like a giant cage"
    },
    {
        "id": "04", "bg": "D", "char": clean_char,
        "action": "imperial guards roughly tackling the man to the dark floor, dragging him away, his green robe getting chaotic. he looks hopelessly at the other ignoring officials",
        "camera": "high angle looking down, guards casting dark shadows over his helpless face",
        "light": "cold sharp dramatic lighting, oppressive"
    },
    {
        "id": "05", "bg": "B", "char": base_char,
        "action": "the man is brutally tied to the bloody wooden pillar, half his body covered in blood, struggling in extreme pain, biting his lips, leaning his head back in agony",
        "camera": "low angle medium shot looking up at the tragic figure",
        "light": "harsh cold pale sunlight piercing through a high window, strong contrast"
    },
    {
        "id": "06", "bg": "B", "char": base_char,
        "action": "high-angle close up of the man's extremely shaky, bloody hand slowly reaching across the dirty floor towards a rusted short sword, desperate",
        "camera": "high angle looking down, slow track following the hand",
        "light": "dusty and grim, cold shadow"
    },
    {
        "id": "07", "bg": "B", "char": base_char,
        "action": "close up of the man's other bloody hand violently grabbing his own reaching hand, struggling intensely, fingers gripping until knuckles turn white",
        "camera": "static close up capturing the aggressive friction of his hands",
        "light": "harsh contrast, highlighting muscle tension"
    },
    {
        "id": "08", "bg": "B", "char": base_char,
        "action": "the man is lying on the dirty floor, burying his head against the cold stone, facial muscles twitching in extreme sorrow, crying silently",
        "camera": "extreme slow pull out zooming back to show his lone figure in the dark cell",
        "light": "very low key lighting, mostly enveloped in cold darkness"
    },
    {
        "id": "09", "bg": "E", "char": base_char + " completely soaked with rain",
        "action": "the miserable man limping in the heavy rain. other walking officials see him and aggressively cover their faces with wide sleeves to avoid him like a monster",
        "camera": "handheld tracking shot following him, people in foreground blurred out",
        "light": "cold blue moody lighting, cinematic rain rainstorms, wet ground reflecting cold grey light"
    },
    {
        "id": "10", "bg": "E", "char": base_char + " completely soaked with rain",
        "action": "the man stands alone in the pouring rain, looking utterly abandoned, slowly hanging down his proud head in total devastating despair",
        "camera": "close up focusing deeply on his soaked miserable face",
        "light": "cold blue cinematic lighting, water dripping off his lonely silhouette"
    },
    {
        "id": "11", "bg": "A", "char": base_char,
        "action": "the man looks down at a mud-stained ancient silk letter on the ground, then abruptly throws back his head in a miserable, tragic bitter laugh, tears falling",
        "camera": "medium shot, slight handshake tracking his violent laughter",
        "light": "warm solitary oil lamp, highlighting the tears on his grimy face"
    },
    {
        "id": "12", "bg": "C", "char": base_char,
        "action": "the man's side profile experiencing a sudden harsh realization, staring forward in awe. ghostly reflections of ancient scholars flash over his face",
        "camera": "very fast cinematic arc shot spinning around his face",
        "light": "sudden bursts of ethereal bright amber light glowing in the pitch black void"
    },
    {
        "id": "13", "bg": "A", "char": base_char,
        "action": "the man suddenly turns his head towards the camera like a madman, eyes completely bloodshot and bursting with furious determination",
        "camera": "violent crash zoom punching right onto his fierce eyes",
        "light": "aggressive flickering orange light from below, deep intimidating shadows"
    },
    {
        "id": "14", "bg": "A", "char": base_char,
        "action": "the man lunges desperately towards a pile of bamboo slips, grabbing the carving knife and carving characters furiously, as bamboo splinters fly in the air, his face twisted in obsessive passion",
        "camera": "medium close up, following the chaotic and violent motion of the knife hand",
        "light": "high contrast chiaroscuro, intense warm light focusing on the bamboo and his face"
    },
    {
        "id": "15", "bg": "A", "char": base_char,
        "action": "close up profile view of the man's face, veins bulging, tears and sweat dripping, his mouth wide open roaring out his ultimate regret to the heavens",
        "camera": "handheld tracking, intense shaky camera movement matching his emotional outburst",
        "light": "low key lighting, sharp highlight outlining his facial structure"
    },
    {
        "id": "16", "bg": "C", "char": base_char,
        "action": "the man stands perfectly still in the dark void, his expression solemn and utterly fearless. He takes a deep breath, staring directly at the viewer like a towering mountain",
        "camera": "extremely slow and elegant push in towards him, cinematic holy focus",
        "light": "single dramatic spotlight in absolute darkness, highly spiritual"
    },
    {
        "id": "17", "bg": "C", "char": base_char,
        "action": "extreme close up of the man's unwavering, immortal face, illuminated by massive violent lightning strikes. His eyes convey absolute majesty and triumph over death",
        "camera": "extreme face close up, static locked angle",
        "light": "strobe lightning flashes, brilliant chaotic white light against pitch black"
    },
    {
        "id": "18", "bg": "C2", "char": base_char,
        "action": "top down close up of the man's calm, aged hands carefully tying a thick hemp string around a rolled-up bundle of ancient bamboo slips on a wooden desk",
        "camera": "top down flat lay shot, static and perfectly stable",
        "light": "blinding beautiful morning sunlight, cinematic god rays washing over the slips"
    },
    {
        "id": "19", "bg": "C2", "char": base_char,
        "action": "the man lifts the bamboo scrolls, his back facing the camera, silhouetted against the intensely bright and holy sunlight entering the door. his posture is aged but unyielding",
        "camera": "slow dolly out, capturing his majestic silhouette",
        "light": "extreme backlighting, blinding white and golden sun rays silhouetting the figure"
    },
    {
        "id": "20", "bg": "C2", "char": base_char,
        "action": "the man slowly turns his side profile towards the camera over his shoulder, closing his eyes with a faint, peaceful smile of ultimate relief, before turning to walk out into the blinding white light",
        "camera": "static shot watching him leave",
        "light": "the background dissolves into pure overexposed blinding white light"
    }
]

for shot in shots:
    prompt = f"{style_anchor}, {scenarios[shot['bg']]}, {shot['char']}, {shot['action']}, {shot['camera']}, {shot['light']}."
    filepath = f"dramas/bao-ren-an-shu/prompts/shot-{shot['id']}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(prompt)

print("✅ Regenerated all 20 video prompts into the prompts/ folder.")

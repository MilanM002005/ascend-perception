import cv2, os

arena_dir = "data/arena_images"
seed_dir  = "data/seeds"

# Clear old seeds first
for f in os.listdir(seed_dir):
    os.remove(os.path.join(seed_dir, f))

crops = [
    ("DJI_0145.JPG", 400, 200),
    ("DJI_0160.JPG", 600, 300),
    ("DJI_0175.JPG", 300, 400),
    ("DSC05986.JPG", 500, 250),
    ("DSC05990.JPG", 350, 350),
    ("DSC05984.JPG", 200, 150),
]

for idx, (fname, x, y) in enumerate(crops, 1):
    path = os.path.join(arena_dir, fname)
    img  = cv2.imread(path)
    if img is None:
        print(f"Could not load {fname}")
        continue

    # ← resize FIRST, exactly like detector does
    img = cv2.resize(img, (1280, 720))

    seed = img[y:y+128, x:x+128]
    out  = os.path.join(seed_dir, f"seed_{idx}.jpg")
    cv2.imwrite(out, seed)
    print(f"seed_{idx}.jpg  ←  {fname} resized to 1280x720, cropped at ({x},{y})")
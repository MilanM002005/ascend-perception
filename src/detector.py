import cv2
import os

from matcher import compare_images


PATCH_SIZE  = 128
STEP_SIZE   = 32
ARENA_W     = 1280
ARENA_H     = 720


def scan_arena(seed_img, arena_img):
    arena_resized = cv2.resize(arena_img, (ARENA_W, ARENA_H))

    best_score = -1.0
    best_x     = 0
    best_y     = 0

    for y in range(0, ARENA_H - PATCH_SIZE, STEP_SIZE):
        for x in range(0, ARENA_W - PATCH_SIZE, STEP_SIZE):

            patch = arena_resized[y : y + PATCH_SIZE,
                                  x : x + PATCH_SIZE]

            score = compare_images(seed_img, patch)

            if score > best_score:
                best_score = score
                best_x     = x
                best_y     = y

    return best_x, best_y, round(best_score, 2)


def find_best_arena(seed_path, arena_folder):
    seed_img = cv2.imread(seed_path)
    if seed_img is None:
        raise FileNotFoundError(f"Cannot load seed: {seed_path}")

    best_score = -1.0
    best_image = None
    best_x     = 0
    best_y     = 0

    for filename in sorted(os.listdir(arena_folder)):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        arena_path = os.path.join(arena_folder, filename)
        arena_img  = cv2.imread(arena_path)
        if arena_img is None:
            print(f"  [WARN] Could not load {filename}, skipping.")
            continue

        x, y, score = scan_arena(seed_img, arena_img)

        print(f"  Checked {filename:<20} score={score:.2f}  loc=({x},{y})")

        if score > best_score:
            best_score = score
            best_image = filename
            best_x     = x
            best_y     = y

    if best_image is None:
        raise FileNotFoundError(f"No valid arena images found in: {arena_folder}")

    return best_image, best_x, best_y, best_score
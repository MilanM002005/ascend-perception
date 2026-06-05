import cv2
import os

from matcher import compare_images


def find_best_arena(seed_path, arena_folder):

    seed = cv2.imread(seed_path)

    best_score = -1
    best_image = None

    for filename in os.listdir(arena_folder):

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        arena_path = os.path.join(
            arena_folder,
            filename
        )

        arena = cv2.imread(arena_path)

        h, w = arena.shape[:2]

        arena_small = cv2.resize(
            arena,
            (1280, 720)
        )

        patch_size = 128
        step = 64

        image_best = 0

        for y in range(
            0,
            arena_small.shape[0] - patch_size,
            step
        ):
            for x in range(
                0,
                arena_small.shape[1] - patch_size,
                step
            ):

                patch = arena_small[
                    y:y+patch_size,
                    x:x+patch_size
                ]

                score = compare_images(
                    seed,
                    patch
                )

                image_best = max(
                    image_best,
                    score
                )

        

        if image_best > best_score:
            best_score = image_best
            best_image = filename

    return best_image, best_score 
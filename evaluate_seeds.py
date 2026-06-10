#To check for all the available seed images

import os
import sys
import cv2

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from detector import find_best_arena, ARENA_W, ARENA_H, PATCH_SIZE

SEEDS_DIR  = os.path.join("data", "seeds")
ARENA_DIR  = os.path.join("data", "arena_images")
OUTPUT_DIR = os.path.join("outputs", "detections")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def draw_and_save(seed_name, arena_filename, best_x, best_y, score):
    arena_path    = os.path.join(ARENA_DIR, arena_filename)
    arena_img     = cv2.imread(arena_path)
    arena_display = cv2.resize(arena_img, (ARENA_W, ARENA_H))

    top_left     = (best_x, best_y)
    bottom_right = (best_x + PATCH_SIZE, best_y + PATCH_SIZE)
    cv2.rectangle(arena_display, top_left, bottom_right,
                  color=(0, 255, 0), thickness=3)

    label = f"{seed_name}  score={score:.1f}  ({best_x},{best_y})"
    cv2.putText(arena_display, label,
                (best_x, max(best_y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 255, 0), 2, cv2.LINE_AA)

    out_name = f"{os.path.splitext(seed_name)[0]}_in_{os.path.splitext(arena_filename)[0]}.jpg"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    cv2.imwrite(out_path, arena_display)
    return out_path


def main():
    seed_files = sorted([
        f for f in os.listdir(SEEDS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if not seed_files:
        print(f"No seed images found in {SEEDS_DIR}")
        sys.exit(1)

    arena_files = [
        f for f in os.listdir(ARENA_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    if not arena_files:
        print(f"No arena images found in {ARENA_DIR}")
        sys.exit(1)

    print(f"\nFound {len(seed_files)} seed(s) and {len(arena_files)} arena image(s).\n")
    print("=" * 60)

    all_results = []

    for seed_name in seed_files:
        seed_path = os.path.join(SEEDS_DIR, seed_name)

        print(f"\nSeed: {seed_name}")
        print("-" * 40)

        best_arena, best_x, best_y, best_score = find_best_arena(
            seed_path, ARENA_DIR
        )

        print()
        print(f"  Best arena : {best_arena}")
        print(f"  Score      : {best_score}")
        print(f"  Location   : x={best_x}, y={best_y}")

        out_path = draw_and_save(seed_name, best_arena,
                                 best_x, best_y, best_score)
        print(f"  Saved      : {out_path}")
        print("=" * 60)

        all_results.append({
            "seed":  seed_name,
            "arena": best_arena,
            "score": best_score,
            "x":     best_x,
            "y":     best_y,
        })

    print("\nSUMMARY")
    print(f"{'Seed':<15} {'Best Arena':<25} {'Score':>7}  {'Location'}")
    print("-" * 65)
    for r in all_results:
        print(f"{r['seed']:<15} {r['arena']:<25} {r['score']:>7.2f}  x={r['x']}, y={r['y']}")

    print(f"\nOutput images saved to: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
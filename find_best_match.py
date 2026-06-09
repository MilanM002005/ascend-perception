import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from detector import find_best_arena

SEEDS_DIR = os.path.join("data", "seeds")
ARENA_DIR = os.path.join("data", "arena_images")


def main():
    if len(sys.argv) > 1:
        seed_path = sys.argv[1]
    else:
        seed_path = os.path.join(SEEDS_DIR, "seed_1.jpg")

    if not os.path.exists(seed_path):
        print(f"Seed not found: {seed_path}")
        sys.exit(1)

    seed_name = os.path.basename(seed_path)
    print(f"\nSeed: {seed_name}")
    print("-" * 40)

    best_arena, best_x, best_y, best_score = find_best_arena(
        seed_path, ARENA_DIR
    )

    print()
    print(f"Best arena : {best_arena}")
    print(f"Score      : {best_score}")
    print(f"Location   : x={best_x}, y={best_y}")


if __name__ == "__main__":
    main()
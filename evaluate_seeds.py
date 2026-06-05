import sys
from pathlib import Path

sys.path.append("src")

from detector import find_best_arena


SEEDS_DIR = "data/seeds"
ARENA_DIR = "data/arena_images"

NUM_RUNS = 3  # repeat stability test


seed_files = sorted(Path(SEEDS_DIR).glob("seed_*.jpg"))

for seed_path in seed_files:

    print("\n" + "=" * 60)
    print(f"SEED: {seed_path.name}")
    print("=" * 60)

    results = []

    for i in range(NUM_RUNS):

        best_image, score = find_best_arena(
            str(seed_path),
            ARENA_DIR
        )

        results.append((best_image, score))

        print(f"Run {i+1}: {best_image} | score: {score:.2f}")

    # Stability summary
    print("\nSummary:")

    if len(set([r[0] for r in results])) == 1:
        print("CONSISTENT MATCH ✔")
    else:
        print("INCONSISTENT MATCH ⚠️")

    # Best overall (average-like intuition)
    from collections import defaultdict

    score_map = defaultdict(list)

    for img, sc in results:
        score_map[img].append(sc)

    print("\nTop candidates:")

    sorted_candidates = sorted(
        score_map.items(),
        key=lambda x: sum(x[1]) / len(x[1]),
        reverse=True
    )

    for img, scores in sorted_candidates[:2]:
        avg_score = sum(scores) / len(scores)
        print(f"{img} -> avg score: {avg_score:.2f} (runs: {scores})")
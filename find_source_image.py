import sys
import os

sys.path.append("src")

from detector import find_best_arena

best_image, score = find_best_arena(
    "data/seeds/seed_6.jpg",
    "data/arena_images"
)

print()
print("BEST MATCH")
print(best_image)
print(score) 
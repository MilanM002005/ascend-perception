import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from matcher import compare

seed_path = "data/seeds/seed_1.jpg"

best_score = -1
best_image = None

arena_folder = "data/arena_images"

for image_name in os.listdir(arena_folder):

    if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(arena_folder, image_name)

    try:
        score, _ = compare(seed_path, image_path)

        print(f"{image_name}: {score}")

        if score > best_score:
            best_score = score
            best_image = image_name

    except Exception as e:
        print(f"Error with {image_name}: {e}")

print("\n" + "=" * 60)
print("BEST MATCH")
print("=" * 60)
print(f"Image: {best_image}")
print(f"Score: {best_score}")
# ASCEND Perception

## Goal

Identify locations of seed features within arena imagery.

---

## Current Scope

* Image preprocessing
* Feature extraction using ORB
* Feature matching
* Retrieval of the most likely source arena image for a given seed image

---

## Future Scope

* Localization of seed within arena image
* Coordinate estimation
* Image stitching
* Global mapping

---

## Folder Structure

* `data/seeds/` — seed images (cropped reference images)
* `data/arena_images/` — full arena images to search through
* `src/preprocess.py` — image cleaning and preparation
* `src/matcher.py` — ORB feature matching
* `src/detector.py` — arena image retrieval logic
* `find_source_image.py` — run retrieval for a single seed
* `evaluate_seeds.py` — evaluate all seeds and test stability
* `outputs/` — saved results
* `docs/` — architecture notes

---

## How It Works

1. Load a seed image.
2. Load each arena image.
3. Generate overlapping patches using a sliding-window approach.
4. Compare the seed against each patch using ORB feature matching.
5. Record the highest similarity score for each arena image.
6. Return the arena image with the highest score.

---

## Usage

Run a single retrieval:

```bash
python find_source_image.py
```

Run evaluation on all seeds:

```bash
python evaluate_seeds.py
```

---

## Current Output

Input:

* Seed image
* Arena image dataset

Output:

* Best matching arena image
* Similarity score

---

## Evaluation Status

Current testing demonstrates:

* Stable results across repeated runs
* Deterministic retrieval behavior
* Successful retrieval for multiple seed images

---

## Handoff to Localization Module

Current module:

Seed Image → Best Matching Arena Image

Next module (Person 2):

Seed Image → Best Matching Arena Image → Estimated (x, y) Location

Your new README already covers everything. Just replace the entire contents of `README.md` with this:

```markdown
# ASCEND Perception

A computer vision pipeline that locates seed features within drone-captured arena imagery using ORB feature matching and sliding window search.

---

## Goal

Identify the location of seed features within arena imagery, returning the best matching arena image and the exact pixel coordinates of the match.

---

## Current Scope

- Image preprocessing (grayscale, CLAHE, resize)
- Feature extraction using ORB
- Feature matching with Lowe's Ratio Test
- Sliding window search across arena images
- Best match retrieval (arena image + x,y coordinates)
- Output images with bounding box drawn at detected location

---

## Future Scope

- Image stitching
- Global arena mapping
- GPS/real-world coordinate estimation
- Distance calculation from docking station

---

## Pipeline

```
Drone Flight
      ↓
Capture Images
      ↓
Image Stitching (future)
      ↓
Global Arena Map (future)
      ↓
Seed Feature Search  ← current scope
      ↓
Feature Coordinates
      ↓
Distance from Docking Station (future)
```

---

## Folder Structure

```
ascend-perception/
│
├── data/
│   ├── seeds/              # 128x128 seed images to search for
│   └── arena_images/       # drone-captured arena images to search within
│
├── src/
│   ├── preprocess.py       # image loading, grayscale, CLAHE, resize
│   ├── matcher.py          # ORB feature extraction and matching
│   └── detector.py         # sliding window search, returns x,y,score
│
├── docs/
│   ├── architecture.md     # pipeline architecture diagrams
│   └── person2_handover.md # Person 2 handover notes
│
├── outputs/
│   └── detections/         # output images with bounding boxes drawn
│
├── evaluate_seeds.py       # main benchmark — runs all seeds vs all arenas
├── find_best_match.py      # quick single-seed test utility
├── find_source_image.py    # original single-seed retrieval (Person 1)
├── make_seeds.py           # crops test seeds from arena images at correct scale
├── requirements.txt
└── README.md
```

---

## How It Works

### Step 1 — Preprocessing
Every image goes through the same pipeline before comparison:
- Convert to grayscale
- Apply CLAHE to enhance local contrast
- Resize to a standard dimension

### Step 2 — Feature Extraction (ORB)
ORB finds up to 500 distinctive keypoints in each image and generates a binary descriptor for each one.

### Step 3 — Feature Matching
Descriptors from the seed are matched against each arena patch using Brute Force matching with Hamming distance. Lowe's Ratio Test (0.85) filters weak matches.

### Step 4 — Similarity Score

```
score = (good matches / seed keypoints) x 100
```

### Step 5 — Sliding Window Search
The arena image is resized to 1280x720. A 128x128 window slides across it in steps of 32 pixels. The window with the highest score is returned as the detected location.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Usage

### Create seeds (first time only)
```bash
python make_seeds.py
```

### Run full benchmark
```bash
python evaluate_seeds.py
```

### Quick single seed test
```bash
python find_best_match.py
python find_best_match.py data/seeds/seed_2.jpg
```

### Original single retrieval (Person 1)
```bash
python find_source_image.py
```

---

## Current Output

Input:
- Seed image (128x128)
- Arena image dataset

Output:
- Best matching arena image
- Similarity score (0-100)
- Pixel coordinates (x, y) of match location
- Detection image with green bounding box saved to `outputs/detections/`

Example:
```
Seed: seed_1.jpg
  Best arena : DJI_0145.JPG
  Score      : 28.57
  Location   : x=416, y=192
  Saved      : outputs/detections/seed_1_in_DJI_0145.jpg
```

---

## Understanding Scores

| Score Range | Meaning |
|---|---|
| 70 - 100 | Very strong match |
| 40 - 70 | Good match, reliable for drone imagery |
| 20 - 40 | Weak, verify visually |
| Below 20 | No real match |

---

## Evaluation Results

| Seed | Best Arena | Score | Location |
|---|---|---|---|
| seed_1.jpg | DJI_0145.JPG | 28.57 | x=416, y=192 |
| seed_2.jpg | DJI_0161.JPG | 43.37 | x=608, y=416 |
| seed_3.jpg | DJI_0175.JPG | 28.23 | x=288, y=416 |
| seed_4.jpg | DSC05986.JPG | 41.48 | x=512, y=256 |
| seed_5.jpg | DSC05990.JPG | 46.10 | x=352, y=352 |
| seed_6.jpg | DSC05984.JPG | 36.65 | x=192, y=160 |

---

OUTPUT

The pipeline outputs pixel coordinates (x, y) in 1280x720 space for every detected seed. Next steps:

1. Map pixel coordinates to real-world metre or GPS coordinates using known arena dimensions and drone altitude
2. Calculate distance from each detected feature to the docking station
3. Replace images in `data/arena_images/` with real drone footage and run:

TO RUN
```bash
python evaluate_seeds.py
```

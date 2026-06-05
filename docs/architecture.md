# ASCEND Perception — Architecture

## Current Pipeline (Person 1 Scope)
Seed Image
↓
Preprocess (grayscale + CLAHE)
↓
Feature Extraction (ORB)
↓
Feature Matching (Brute Force)
↓
Similarity Score

## What each step means
- **Seed Image** — a small cropped image of the thing we want to find (e.g. a rock, a patch of soil)
- **Preprocess** — clean the image (grayscale, enhance contrast)
- **Feature Extraction** — find unique "keypoints" in the image (corners, edges, blobs)
- **Feature Matching** — compare keypoints between seed and arena image
- **Similarity Score** — a number telling us how well they matched

## Future Pipeline (Person 2, 3 scope)
Drone Frames
↓
Image Stitching
↓
Global Arena Map
↓
Feature Search
↓
X,Y Coordinates
↓
Distance From Docking Station
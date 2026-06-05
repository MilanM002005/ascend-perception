
import cv2
import numpy as np


def extract_features(image):
    """
    ORB = Oriented FAST and Rotated BRIEF.
    Finds interesting points (keypoints) and creates descriptors.
    """

    orb = cv2.ORB_create(nfeatures=500)

    keypoints, descriptors = orb.detectAndCompute(
        image,
        None
    )

    return keypoints, descriptors


def match_features(desc1, desc2):
    """
    Match ORB descriptors using KNN matching
    and Lowe's Ratio Test.
    """

    if desc1 is None or desc2 is None:
        return []

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)

    matches = bf.knnMatch(
        desc1,
        desc2,
        k=2
    )

    good_matches = []

    for pair in matches:

        if len(pair) < 2:
            continue

        m, n = pair

        if m.distance < 0.85 * n.distance:
            good_matches.append(m)

    good_matches = sorted(
        good_matches,
        key=lambda x: x.distance
    )

    return good_matches


def compute_similarity_score(matches, kp1):
    """
    Score based on percentage of seed keypoints
    that found a good match.
    """

    if len(kp1) == 0:
        return 0

    score = (len(matches) / len(kp1)) * 100

    return round(score, 2)


def compare(seed_path, arena_path):
    """
    Compare a seed image against an arena image.
    """

    from preprocess import (
        convert_to_grayscale,
        apply_clahe,
        load_image
    )

    seed_img = load_image(seed_path)
    seed_img = cv2.resize(seed_img, (128, 128))
    seed_img = convert_to_grayscale(seed_img)
    seed_img = apply_clahe(seed_img)

    arena_img = load_image(arena_path)
    arena_img = cv2.resize(arena_img, (640, 480))
    arena_img = convert_to_grayscale(arena_img)
    arena_img = apply_clahe(arena_img)

    kp1, desc1 = extract_features(seed_img)
    kp2, desc2 = extract_features(arena_img)

    matches = match_features(desc1, desc2)

    score = compute_similarity_score(
        matches,
        kp1
    )

    print(f"Seed: {seed_path}")
    print(f"Arena: {arena_path}")
    print(f"Keypoints in seed: {len(kp1)}")
    print(f"Keypoints in arena: {len(kp2)}")
    print(f"Good Matches: {len(matches)}")
    print(f"Similarity Score: {score}")

    return score, matches


def compare_images(seed_img, arena_patch):
    """
    Compare two already-loaded images.

    Used by detector.py when scanning
    patches inside arena images.
    """

    from preprocess import (
        convert_to_grayscale,
        apply_clahe
    )

    seed_img = cv2.resize(
        seed_img,
        (128, 128)
    )

    arena_patch = cv2.resize(
        arena_patch,
        (128, 128)
    )

    seed_img = convert_to_grayscale(
        seed_img
    )

    arena_patch = convert_to_grayscale(
        arena_patch
    )

    seed_img = apply_clahe(
        seed_img
    )

    arena_patch = apply_clahe(
        arena_patch
    )

    kp1, desc1 = extract_features(
        seed_img
    )

    kp2, desc2 = extract_features(
        arena_patch
    )

    matches = match_features(
        desc1,
        desc2
    )

    score = compute_similarity_score(
        matches,
        kp1
    )

    return score
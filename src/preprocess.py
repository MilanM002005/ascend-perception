import cv2
import numpy as np

def load_image(path):
    """
    Loads an image from the given file path.
    Returns the image in BGR color format (default for OpenCV).
    """
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at: {path}")
    return image


def convert_to_grayscale(image):
    """
    Converts a BGR image to grayscale.
    Grayscale is simpler — just brightness values, no color.
    Feature matching works on grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_clahe(gray_image):
    """
    CLAHE = Contrast Limited Adaptive Histogram Equalization.
    In plain English: makes dark areas brighter and bright areas more visible.
    This helps find features in images taken in bad lighting (like a drone outdoors).
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(gray_image)


def resize_image(image, width=640, height=480):
    """
    Resizes image to a standard size.
    Keeps processing consistent regardless of original image size.
    """
    return cv2.resize(image, (width, height))


def preprocess(path):
    """
    Full pipeline: load → grayscale → CLAHE → resize.
    This is the function you'll call from matcher.py.
    Just pass it an image path and it returns a clean image ready for matching.
    """
    image = load_image(path)
    gray = convert_to_grayscale(image)
    enhanced = apply_clahe(gray)
    resized = resize_image(enhanced)
    return resized
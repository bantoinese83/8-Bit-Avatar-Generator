import cv2
import numpy as np


def load_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise FileNotFoundError(f"No image found at {image_path}")
    return image


def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_threshold(image, threshold_value=0, max_value=255):
    _, thresh = cv2.threshold(image, threshold_value, max_value, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.bitwise_not(thresh)


def find_contours(image, retrieval_mode=cv2.RETR_EXTERNAL):
    contours, _ = cv2.findContours(image, retrieval_mode, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(image, contours):
    mask = np.zeros_like(image)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)
    return mask


def apply_mask(image, mask):
    b, g, r = cv2.split(image)
    alpha = mask
    rgba = [b, g, r, alpha]
    result = cv2.merge(rgba, 4)
    return result


def save_image(image, output_path):
    cv2.imwrite(output_path, image)


def remove_background(image_path, output_path):
    image = load_image(image_path)
    gray = convert_to_grayscale(image)
    thresh = apply_threshold(gray)
    contours = find_contours(thresh)
    mask = draw_contours(thresh, contours)  # Use the threshold image for drawing contours
    result = apply_mask(image, mask)
    save_image(result, output_path)
    return output_path




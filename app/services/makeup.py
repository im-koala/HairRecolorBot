import cv2
import numpy as np
from skimage.filters import gaussian
from app.services.test import evaluate

def sharpen(img):
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, multichannel=True)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255
    return np.array(img_out, dtype=np.uint8)


def hair(image, parsing, color):
    part = 17
    b, g, r = color
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    image_hsv[:, :, 0:1] = tar_hsv[:, :, 0:1]

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
    changed = sharpen(changed)

    if (changed.shape[0] != parsing.shape[0]) or (changed.shape[1] != parsing.shape[1]):
        parsing = cv2.resize(
            parsing,
            (changed.shape[1], changed.shape[0]),
            interpolation=cv2.INTER_NEAREST,
        )

    changed[parsing != part] = image[parsing != part]

    return changed

def recolor_hair(image_path: str, output_image_path: str, color: str):
    image = cv2.imread(image_path)
    parsing = evaluate(image_path)
    parsing = cv2.resize(parsing, image.shape[0:2], interpolation=cv2.INTER_NEAREST)

    image = hair(image, parsing, color)

    cv2.imwrite(output_image_path, image)
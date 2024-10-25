import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import read_png


def threshold(image, threshold_value):
    """
    Apply a binary threshold to a grayscale image.

    Parameters:
        image (numpy.ndarray): A 2D array representing the grayscale image.
        threshold_value (int): The threshold value to binarize the image.

    Returns:
        numpy.ndarray: A binary image where pixels are set to 255 if the corresponding
                   pixel in the input image is greater than the threshold value,
                   otherwise set to 0.
    """
    height, width = image.shape
    binary_image = np.zeros((height, width), np.uint8)

    for i in range(height):
        for j in range(width):
            if image[i, j] > threshold_value:
                binary_image[i, j] = 255
            else:
                binary_image[i, j] = 0

    return binary_image


image = read_png('denoised_5x5/9504i5c9jde103011350.png')
threshold_value = 161

binary_image = threshold(image, threshold_value)

plt.subplot(1, 2, 1)
plt.title('Eredeti kép')
plt.imshow(image, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Bináris kép')
plt.imshow(binary_image, cmap='gray')
plt.axis('off')

plt.show()
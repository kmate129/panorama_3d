import os
import numpy as np
from utils import read_png, save_png


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


threshold_value = 168
input_folder = "sharpened_m0dot5"
output_folder = "thresholded_163"

os.makedirs(output_folder, exist_ok=True)

for sub_folder, subdirs, files in os.walk(input_folder):
    for file in files:
        file_path = os.path.join(sub_folder, file)

        if os.path.isfile(file_path):
            rel_path = os.path.relpath(sub_folder, input_folder)
            output_folder_path = os.path.join(output_folder, rel_path)
            
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)
                
            if not file.lower().endswith('.png'):
                output_file = f'{file}.png'
            else:
                output_file = file

            output_file_path = os.path.join(output_folder_path, output_file)

            try:
                im = read_png(file_path)
                filtered_im = threshold(im, threshold_value)

                save_png(filtered_im, output_file_path)

                print('SUCCESS>', file_path, '-->', output_file_path)
            except Exception as e:
                print('FAIL>', file_path, '-->', output_file_path, ':', e)
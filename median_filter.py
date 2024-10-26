import os
import numpy as np

from utils import read_png, save_png

def cross_median_filter(image):
    """
    Apply a cross-shaped median filter to the input image.
    The filter considers a cross-shaped neighborhood around each pixel, 
    specifically the following coordinates relative to the center pixel:
    (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (4, 2).
    Parameters:
        image (numpy.ndarray): The input 2D image array.
    Returns:
        numpy.ndarray: The output image array with the cross-shaped median filter applied.
    """
    output_image = np.zeros_like(image)
    filter_coords = [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]
    
    rows, cols = image.shape

    for i in range(2, rows - 2):
        for j in range(2, cols - 2):
            pixel_values = []
            for coord in filter_coords:
                x_offset, y_offset = coord
                pixel_values.append(image[i - 2 + x_offset, j - 2 + y_offset])
            
            median_value = np.median(pixel_values)
            output_image[i, j] = median_value

    return output_image

input_folder = "thresholded_168"
output_folder = "median_filtered_final"

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
                filtered_im = cross_median_filter(im)

                save_png(filtered_im, output_file_path)

                print('SUCCESS>', file_path, '-->', output_file_path)
            except Exception as e:
                print('FAIL>', file_path, '-->', output_file_path, ':', e)
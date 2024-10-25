import os
import numpy as np
from utils import read_png, save_png, scale_to_0_255

def laplace_filter(image):
    """
    Applies a Laplace filter to the input image to enhance edges.
    Parameters:
        image (numpy.ndarray): A 2D array representing the grayscale image to be filtered.
    Returns:
        numpy.ndarray: A 2D array representing the filtered image with enhanced edges.
    """
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]])
    
    height, width = image.shape
    filtered_image = np.zeros((height, width))

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            filtered_value = np.sum(kernel * image[i-1:i+2, j-1:j+2])
            filtered_image[i, j] = filtered_value

    return filtered_image

def enhance_image(original_image, A):
    """
    Enhance the given image by applying a Laplacian filter and scaling the result.
    Parameters:
        original_image (numpy.ndarray): The original image to be enhanced.
        A (float): The scaling factor for the Laplacian image.
    Returns:
        numpy.ndarray: The enhanced image scaled to the range [0, 255] and converted to uint8.
    """
    laplacian_image = laplace_filter(original_image)
    enhanced_image = original_image - A * laplacian_image
    enhanced_image = scale_to_0_255(enhanced_image)
    enhanced_image = enhanced_image.astype(np.uint8)
    
    return enhanced_image


A_value = -0.5
input_folder = "denoised_7x7"
output_folder = "sharpened_m0dot5"

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
                filtered_im = enhance_image(im, A_value)

                save_png(filtered_im, output_file_path)

                print('SUCCESS>', file_path, '-->', output_file_path)
            except Exception as e:
                print('FAIL>', file_path, '-->', output_file_path, ':', e)
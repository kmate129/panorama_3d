import os
import numpy as np
from utils import read_png, save_png


def apply_convolution(image, kernel, padding_mode='constant'):
    """
    Applies a convolution operation to a given image using the specified kernel and padding mode.
    Parameters:
    image (numpy.ndarray): The input image to be filtered. It should be a 2D array.
    kernel (numpy.ndarray): The convolution kernel to be applied. It should be a 2D square array.
    padding_mode (str, optional): The mode of padding to be used. It can be 'constant' or 'edge'. 
                                  Default is 'constant'.
    Returns:
        numpy.ndarray: The filtered image after applying the convolution operation.
    Raises:
        ValueError: If the padding_mode is not 'constant' or 'edge'.
    """
    image_height, image_width = image.shape
    kernel_size = kernel.shape[0]
    pad_size = kernel_size // 2
    
    if padding_mode == 'constant':
        padded_image = np.pad(image, pad_size, mode='constant', constant_values=0)
    elif padding_mode == 'edge':
        padded_image = np.pad(image, pad_size, mode='edge')
    else:
        raise ValueError("A padding_mode értéke 'constant' vagy 'edge' lehet.")
    
    filtered_image = np.zeros_like(image)
    
    for i in range(image_height):
        for j in range(image_width):
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            filtered_image[i, j] = np.sum(region * kernel)
    
    return filtered_image


def gaussian_kernel(size):
    """
    Generates a Gaussian kernel matrix.
    Parameters:
    size (int): The size of the kernel. Must be an odd integer.
    Returns:
        numpy.ndarray: A 2D array representing the Gaussian kernel.
    Raises:
        ValueError: If the size is an even integer.
    Example:
    >>> gaussian_kernel(3)
    array([[0.07511361, 0.1238414 , 0.07511361],
           [0.1238414 , 0.20417996, 0.1238414 ],
           [0.07511361, 0.1238414 , 0.07511361]], dtype=float32)
    """
    if size % 2 == 0:
        raise ValueError("Kernel size can not be even")
        
    center = size // 2
    kernel = np.zeros((size, size), dtype=np.float32)

    for x in range(-center, center + 1):
        for y in range(-center, center + 1):
            kernel[x + center, y + center] = np.exp(-(x**2 + y**2) / (2 * (1**2)))
     
    kernel /= np.sum(kernel)
    return kernel


input_folder = "original_png_8bit"

output_folder = "denoised_7x7"
kernel_3x3 = gaussian_kernel(7)

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
                filtered_im = apply_convolution(im, kernel_3x3, padding_mode="edge")

                save_png(filtered_im, output_file_path)

                print('SUCCESS>', file_path, '-->', output_file_path)
            except Exception as e:
                print('FAIL>', file_path, '-->', output_file_path, ':', e)
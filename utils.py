import os
import numpy as np
import png
import pydicom as dicom
import cv2

def _dicom_to_png(dicom_file, png_file):
    """
    Converts a DICOM file to a PNG file.

    Parameters:
    dicom_file (str): The path to the input DICOM file.
    png_file (str): The path to the output PNG file.

    Returns:
    None

    This function reads a DICOM file, extracts the pixel data, and writes it to a PNG file.
    The pixel values are scaled to fit within the PNG format's bit depth.
    """
    plan = dicom.dcmread(dicom_file)
    shape = plan.pixel_array.shape

    image_2d = []
    max_val = 0
    min_val = 100000
    for row in plan.pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
            if col > max_val: 
                max_val = col
            if col < min_val:
                min_val = col
        image_2d.append(pixels)

    print(max_val)
    print(min_val)
    w = png.Writer(shape[0], shape[1], greyscale=True, bitdepth=8)
    w.write(png_file, image_2d)


def convert_file(dicom_file_path, png_file_path):
    """
    Converts a DICOM file to a PNG file.

    Args:
        dicom_file_path (str): The file path to the DICOM file.
        png_file_path (str): The file path where the PNG file will be saved.

    Raises:
        Exception: If the DICOM file does not exist.

    """
    if not os.path.exists(dicom_file_path):
        raise Exception('File "%s" does not exists' % dicom_file_path)

    dicom_file = open(dicom_file_path, 'rb')
    png_file = open(png_file_path, 'wb')

    _dicom_to_png(dicom_file, png_file)

    png_file.close()


def convert_folder(dicom_folder, png_folder):
    os.makedirs(png_folder)

    for sub_folder, subdirs, files in os.walk(dicom_folder):
        for dicom_file in os.listdir(sub_folder):
            dicom_file_path = os.path.join(sub_folder, dicom_file)

            if os.path.isfile(dicom_file_path):

                rel_path = os.path.relpath(sub_folder, dicom_folder)
                png_folder_path = os.path.join(png_folder, rel_path)
                if not os.path.exists(png_folder_path):
                    os.makedirs(png_folder_path)
                png_file_path = os.path.join(png_folder_path, '%s.png' % dicom_file)

                try:
                    convert_file(dicom_file_path, png_file_path)
                    print('SUCCESS>', dicom_file_path, '-->', png_file_path)
                except Exception as e:
                    print('FAIL>', dicom_file_path, '-->', png_file_path, ':', e)


def read_png(filename, log=True):
    """
    Reads a PNG image using OpenCV and converts it to a numpy array.
    """
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    if log:
        print("Beolvasott kép mérete:", image.shape)

    return image


def save_png(image, filename):
    """
    Saves a numpy array as a PNG file using OpenCV.
    """
    cv2.imwrite(filename, image)


def scale_to_0_255(image):
    """
    Scales the pixel values of an image to the range [0, 255].
    This function takes an image with arbitrary pixel values and scales them
    linearly so that the minimum pixel value becomes 0 and the maximum pixel
    value becomes 255. The resulting image is returned as an array of type
    uint8.
    Parameters:
        image (numpy.ndarray): The input image to be scaled.
    Returns:
        numpy.ndarray: The scaled image with pixel values in the range [0, 255].
    """
    min_pixel = np.min(image)
    max_pixel = np.max(image)
    scaled_image = 255 * (image - min_pixel) / (max_pixel - min_pixel)
    
    return scaled_image.astype(np.uint8)


def from_folder_to_3d_grid(folder, number_of_images):
    """
    Reads all PNG images from a folder and stacks them along the z-axis to create a 3D matrix.
    This function reads all PNG images from a folder, sorts them by filename, and stacks them
    along the z-axis to create a 3D matrix. The resulting matrix has dimensions (height, width, depth),
    where the depth corresponds to the number of images in the folder.
    Parameters:
        folder (str): The path to the folder containing the PNG images.
    Returns:
        numpy.ndarray: A 3D matrix containing the pixel values of the PNG images.
    """
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    files.remove('.DS_Store')
    files.sort()

    files2 = []
    for i in range(number_of_images):
        files2.append(files[i])

    if not files:
        raise ValueError("Nincs fájl a megadott mappában.")
    
    first_image = read_png(os.path.join(folder, files2[0]), log=False)
    
    height, width = first_image.shape
    
    num_images = len(files2)
    image_stack = np.zeros((num_images, height, width), dtype=np.uint8)

    for i, filename in enumerate(files2):
        img_path = os.path.join(folder, filename)
        img = read_png(img_path)
        image_stack[i] = img

    return image_stack


def save_to_obj(verts, faces, normals, filename):
    """
    Saves vertices and faces to an .obj file.
    
    verts: np.ndarray of shape (n_verts, 3), where each row is a vertex [x, y, z]
    faces: np.ndarray of shape (n_faces, 3), where each row contains the indices of vertices forming a triangle
    filename: str, the name of the output file
    """
    with open(filename, 'w') as file:
        for vert in verts:
            file.write(f"v {vert[0]} {vert[1]} {vert[2]}\n")

        for item in normals:
            file.write("vn {0} {1} {2}\n".format(item[0],item[1],item[2]))
        
        for face in faces:
            file.write(f"f {face[0] + 1} {face[1] + 1} {face[2] + 1}\n")

import os
import png
import pydicom as dicom

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
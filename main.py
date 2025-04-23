
from utils import from_folder_to_3d_grid, save_to_obj
from parallel import split_and_process
import time
import numpy as np
import pyvista as pv
import vtk

def convert_faces_to_pyvista_format(faces):
    face_list = []
    for face in faces:
        face_list.append([len(face)] + list(face))
    
    return np.array(face_list)

if __name__ == "__main__":
    ct = from_folder_to_3d_grid('median_filtered_final', 688)
    print(ct.shape)
    print(type(ct), ct.dtype)

    iso_val=255
    overall_start = time.perf_counter()
    verts, faces = split_and_process(ct, iso_val)
    overall_end = time.perf_counter()
    print(f"\nOverall Time taken by algorithm\n{'-'*40}\n{overall_end - overall_start} s")

    faces = convert_faces_to_pyvista_format(faces)
    celltypes = np.empty(faces.shape[0], dtype=np.uint8)
    grid = pv.UnstructuredGrid(faces.ravel(), celltypes, verts)
    cleaned_grid = grid.clean()

    polydata = cleaned_grid.extract_surface()

    polydata.save('original_skull.stl')
    save_to_obj(verts, faces, "original_skull.obj")
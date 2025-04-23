import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from marching_cubes import get_contour_segments

def worker(thres, cube_slice, offset, base_index):
    verts, faces = get_contour_segments(thres, cube_slice)

    verts = np.array(verts)
    faces = np.array(faces)

    if verts.size == 0 or faces.size == 0:
        return np.empty((0, 3)), np.empty((0, 3), dtype=int)

    if verts.ndim == 1:
        verts = verts.reshape((1, -1))
    elif verts.shape[1] != 3:
        raise ValueError(f"Verts shape is invalid: {verts.shape}")

    offset = np.array(offset)
    if offset.shape != (3,):
        raise ValueError(f"Offset must be (3,), but got {offset.shape}")

    verts += offset
    faces += base_index
    return verts, faces


def split_and_process(cube_matrix, thres, divisions=8):
    size = cube_matrix.shape[0]
    chunk_size = size // divisions
    tasks = []

    with ProcessPoolExecutor() as executor:
        futures = []
        
        for x in range(divisions):
            for y in range(divisions):
                for z in range(divisions):
                    x0, x1 = x * chunk_size, (x + 1) * chunk_size
                    y0, y1 = y * chunk_size, (y + 1) * chunk_size
                    z0, z1 = z * chunk_size, (z + 1) * chunk_size

                    cube_chunk = cube_matrix[x0:x1+1, y0:y1+1, z0:z1+1]  
                    offset = (x0, y0, z0)
                    futures.append(executor.submit(worker, thres, cube_chunk, offset, len(futures)))

        all_vertices = []
        all_faces = []
        vertex_offset = 0

        for future in as_completed(futures):
            verts, faces = future.result()

            if verts.size == 0 or faces.size == 0:
                continue

            faces[:, 1:] += vertex_offset
            vertex_offset += len(verts)

            all_vertices.append(verts)
            all_faces.append(faces)

        all_vertices = np.vstack(all_vertices)
        all_faces = np.vstack(all_faces)

    return all_vertices, all_faces
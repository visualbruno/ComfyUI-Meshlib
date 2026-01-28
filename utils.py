"""
Utility functions for ComfyUI-Meshlib nodes
"""

import numpy as np


def trimesh_to_meshlib(tm):
    """
    Convert a trimesh.Trimesh object to a MeshLib Mesh.
    
    Args:
        tm: trimesh.Trimesh object
        
    Returns:
        meshlib.mrmeshpy.Mesh object
    """
    import meshlib.mrmeshnumpy as mrmeshnumpy
    
    vertices = np.asarray(tm.vertices, dtype=np.float32)
    faces = np.asarray(tm.faces, dtype=np.int32)
    
    return mrmeshnumpy.meshFromFacesVerts(faces, vertices)


def meshlib_to_trimesh(mesh):
    """
    Convert a MeshLib Mesh to a trimesh.Trimesh object.
    
    Args:
        mesh: meshlib.mrmeshpy.Mesh object
        
    Returns:
        trimesh.Trimesh object
    """
    import trimesh
    import meshlib.mrmeshnumpy as mrmeshnumpy
    
    vertices = mrmeshnumpy.getNumpyVerts(mesh)
    faces = mrmeshnumpy.getNumpyFaces(mesh.topology)
    
    return trimesh.Trimesh(vertices=vertices, faces=faces)


def get_output_path(filename_prefix: str, file_format: str) -> str:
    """
    Generate an output path for saving files.
    
    Args:
        filename_prefix: Prefix for the filename
        file_format: File extension (without dot)
        
    Returns:
        Full path to the output file
    """
    import folder_paths
    from pathlib import Path
    
    full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, folder_paths.get_output_directory())
    
    output_path = Path(full_output_folder) / f'{filename}_{counter:05}.{file_format}'
    output_path.parent.mkdir(exist_ok=True, parents=True) 
    
    return str(output_path)


def resolve_input_path(file_path: str) -> str:
    """
    Resolve a file path, checking the input directory if the path doesn't exist.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Resolved absolute path
    """
    import os
    import folder_paths
    
    if os.path.exists(file_path):
        return file_path
    
    # Try input directory
    input_path = os.path.join(folder_paths.get_input_directory(), file_path)
    if os.path.exists(input_path):
        return input_path
    
    raise FileNotFoundError(f"File not found: {file_path}")

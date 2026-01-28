"""
I/O Nodes for ComfyUI-Meshlib
Handles loading and saving meshes and point clouds
"""

import os
from pathlib import Path

import folder_paths

from ..utils import trimesh_to_meshlib, meshlib_to_trimesh, get_output_path, resolve_input_path


class MeshlibLoadMesh:
    """Load a mesh from file using MeshLib"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "", 
                    "tooltip": "Path to mesh file (STL, OBJ, PLY, CTM, GLB, OFF, etc.)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    OUTPUT_TOOLTIPS = ("Loaded MeshLib mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Load a mesh from file. Supports STL, OBJ, PLY, CTM, GLB, OFF, and many other formats."

    def process(self, file_path):
        import meshlib.mrmeshpy as mrmeshpy
        
        resolved_path = resolve_input_path(file_path)
        mesh = mrmeshpy.loadMesh(resolved_path)
        
        return (mesh,)


class MeshlibSaveMesh:
    """Save a mesh to file using MeshLib"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "filename_prefix": ("STRING", {"default": "3D/meshlib"}),
                "file_format": (["stl", "obj", "ply", "ctm", "glb", "off"],),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    OUTPUT_NODE = True
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Save a mesh to file. Supports STL, OBJ, PLY, CTM, GLB, and OFF formats."

    def process(self, mesh, filename_prefix, file_format):
        import meshlib.mrmeshpy as mrmeshpy
        
        output_path = get_output_path(filename_prefix, file_format)
        mrmeshpy.saveMesh(mesh, output_path)
        
        return (output_path,)


class MeshlibLoadPoints:
    """Load a point cloud from file using MeshLib"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "",
                    "tooltip": "Path to point cloud file (PLY, OBJ, PTS, etc.)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_POINTCLOUD",)
    RETURN_NAMES = ("points",)
    OUTPUT_TOOLTIPS = ("Loaded MeshLib point cloud",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Load a point cloud from file."

    def process(self, file_path):
        import meshlib.mrmeshpy as mrmeshpy
        
        resolved_path = resolve_input_path(file_path)
        points = mrmeshpy.loadPoints(resolved_path)
        
        return (points,)


class MeshlibSavePoints:
    """Save a point cloud to file using MeshLib"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "points": ("MESHLIB_POINTCLOUD",),
                "filename_prefix": ("STRING", {"default": "3D/points"}),
                "file_format": (["ply", "obj", "pts"],),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_path",)
    OUTPUT_NODE = True
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Save a point cloud to file."

    def process(self, points, filename_prefix, file_format):
        import meshlib.mrmeshpy as mrmeshpy
        
        output_path = get_output_path(filename_prefix, file_format)
        mrmeshpy.savePoints(points, output_path)
        
        return (output_path,)


class MeshlibFromTrimesh:
    """Convert a Trimesh object to MeshLib Mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "trimesh": ("TRIMESH",),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Convert a Trimesh object to MeshLib Mesh format."

    def process(self, trimesh):
        mesh = trimesh_to_meshlib(trimesh)
        return (mesh,)


class MeshlibToTrimesh:
    """Convert a MeshLib Mesh to Trimesh object"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            }
        }
    
    RETURN_TYPES = ("TRIMESH",)
    RETURN_NAMES = ("trimesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Convert a MeshLib Mesh to Trimesh format."

    def process(self, mesh):
        tm = meshlib_to_trimesh(mesh)
        return (tm,)


class MeshlibCopyMesh:
    """Create a copy of a MeshLib mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh_copy",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/IO"
    DESCRIPTION = "Create a deep copy of a MeshLib mesh."

    def process(self, mesh):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh_copy = mrmeshpy.copyMesh(mesh)
        return (mesh_copy,)

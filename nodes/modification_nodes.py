"""
Modification Nodes for ComfyUI-Meshlib
Mesh modification operations: decimation, subdivision, offset, relax, transform
"""

import math


class MeshlibDecimate:
    """Decimate (simplify) a mesh by reducing triangle count"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "target_faces": ("INT", {
                    "default": 10000, 
                    "min": 4,
                    "max": 10000000,
                    "tooltip": "Target number of faces after decimation"
                }),
                "max_error": ("FLOAT", {
                    "default": 0.001, 
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.0001,
                    "tooltip": "Maximum geometric error allowed (relative to mesh size)"
                }),
                "subdivide_parts": ("INT", {
                    "default": 64, 
                    "min": 1,
                    "max": 256,
                    "tooltip": "Number of parallel processing parts (higher = faster but slightly lower quality)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "INT", "INT")
    RETURN_NAMES = ("mesh", "verts_deleted", "faces_deleted")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Modification"
    DESCRIPTION = "Decimate a mesh by reducing the number of triangles while preserving shape."

    def process(self, mesh, target_faces, max_error, subdivide_parts):
        import meshlib.mrmeshpy as mrmeshpy
        
        # Work on a copy to avoid modifying original
        mesh = mrmeshpy.copyMesh(mesh)
        mesh.packOptimally()
        
        current_faces = mesh.topology.numValidFaces()
        faces_to_delete = max(0, current_faces - target_faces)
        
        settings = mrmeshpy.DecimateSettings()
        settings.maxDeletedFaces = faces_to_delete
        settings.maxError = max_error
        settings.subdivideParts = subdivide_parts
        
        result = mrmeshpy.decimateMesh(mesh, settings)
        
        return (mesh, result.vertsDeleted, result.facesDeleted)


class MeshlibSubdivide:
    """Subdivide a mesh by splitting edges and faces"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "max_edge_length": ("FLOAT", {
                    "default": 0.1, 
                    "min": 0.0001,
                    "max": 100.0,
                    "step": 0.01,
                    "tooltip": "Maximum edge length after subdivision"
                }),
                "max_deviation_after_flip": ("FLOAT", {
                    "default": 0.5, 
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                    "tooltip": "Maximum deviation allowed when flipping edges"
                }),
                "max_splits": ("INT", {
                    "default": 10000000,
                    "min": 1,
                    "max": 100000000,
                    "tooltip": "Maximum number of edge splits to perform"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "INT")
    RETURN_NAMES = ("mesh", "splits_done")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Modification"
    DESCRIPTION = "Subdivide a mesh by splitting edges longer than the specified length."

    def process(self, mesh, max_edge_length, max_deviation_after_flip, max_splits):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        settings = mrmeshpy.SubdivideSettings()
        settings.maxEdgeLen = max_edge_length
        settings.maxDeviationAfterFlip = max_deviation_after_flip
        settings.maxEdgeSplits = max_splits
        
        splits = mrmeshpy.subdivideMesh(mesh, settings)
        
        return (mesh, splits)


class MeshlibOffset:
    """Create an offset (shell) of a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "offset": ("FLOAT", {
                    "default": 0.1,
                    "min": -100.0,
                    "max": 100.0,
                    "step": 0.01,
                    "tooltip": "Offset distance (positive = expand, negative = shrink)"
                }),
                "voxel_count": ("INT", {
                    "default": 5000000, 
                    "min": 100000,
                    "max": 50000000,
                    "tooltip": "Approximate number of voxels for the operation (higher = more detail)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Modification"
    DESCRIPTION = "Create an offset surface from a mesh. Positive offset expands, negative shrinks."

    def process(self, mesh, offset, voxel_count):
        import meshlib.mrmeshpy as mrmeshpy
        
        params = mrmeshpy.OffsetParameters()
        params.voxelSize = mrmeshpy.suggestVoxelSize(mesh, voxel_count)
        
        # Check if mesh has holes and adjust sign detection
        if not mrmeshpy.findRightBoundary(mesh.topology).empty():
            params.signDetectionMode = mrmeshpy.SignDetectionMode.HoleWindingRule
        
        result = mrmeshpy.offsetMesh(mesh, offset, params)
        
        return (result,)


class MeshlibRelax:
    """Relax/smooth a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "iterations": ("INT", {
                    "default": 5, 
                    "min": 1, 
                    "max": 100,
                    "tooltip": "Number of relaxation iterations"
                }),
                "force": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1,
                    "tooltip": "Relaxation strength (0-1)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Modification"
    DESCRIPTION = "Smooth a mesh by relaxing vertex positions."

    def process(self, mesh, iterations, force):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        params = mrmeshpy.MeshRelaxParams()
        params.iterations = iterations
        params.force = force
        
        mrmeshpy.relax(mesh, params)
        
        return (mesh,)


class MeshlibTransform:
    """Transform a mesh (translate, rotate, scale)"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "translate_x": ("FLOAT", {"default": 0.0, "step": 0.1}),
                "translate_y": ("FLOAT", {"default": 0.0, "step": 0.1}),
                "translate_z": ("FLOAT", {"default": 0.0, "step": 0.1}),
                "rotate_x": ("FLOAT", {
                    "default": 0.0, 
                    "min": -180, 
                    "max": 180,
                    "step": 1.0,
                    "tooltip": "Rotation around X axis in degrees"
                }),
                "rotate_y": ("FLOAT", {
                    "default": 0.0, 
                    "min": -180, 
                    "max": 180,
                    "step": 1.0,
                    "tooltip": "Rotation around Y axis in degrees"
                }),
                "rotate_z": ("FLOAT", {
                    "default": 0.0, 
                    "min": -180, 
                    "max": 180,
                    "step": 1.0,
                    "tooltip": "Rotation around Z axis in degrees"
                }),
                "scale_uniform": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001,
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Uniform scale factor"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Modification"
    DESCRIPTION = "Apply translation, rotation, and scaling to a mesh."

    def process(self, mesh, translate_x, translate_y, translate_z, 
                rotate_x, rotate_y, rotate_z, scale_uniform):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        # Apply scale first (around origin)
        if scale_uniform != 1.0:
            scale_mat = mrmeshpy.Matrix3f.scale(scale_uniform)
            mesh.transform(mrmeshpy.AffineXf3f.linear(scale_mat))
        
        # Apply rotations (X, Y, Z order)
        if rotate_x != 0:
            axis = mrmeshpy.Vector3f(1, 0, 0)
            rot = mrmeshpy.Matrix3f.rotation(axis, math.radians(rotate_x))
            mesh.transform(mrmeshpy.AffineXf3f.linear(rot))
        
        if rotate_y != 0:
            axis = mrmeshpy.Vector3f(0, 1, 0)
            rot = mrmeshpy.Matrix3f.rotation(axis, math.radians(rotate_y))
            mesh.transform(mrmeshpy.AffineXf3f.linear(rot))
        
        if rotate_z != 0:
            axis = mrmeshpy.Vector3f(0, 0, 1)
            rot = mrmeshpy.Matrix3f.rotation(axis, math.radians(rotate_z))
            mesh.transform(mrmeshpy.AffineXf3f.linear(rot))
        
        # Apply translation last
        if translate_x != 0 or translate_y != 0 or translate_z != 0:
            trans = mrmeshpy.Vector3f(translate_x, translate_y, translate_z)
            mesh.transform(mrmeshpy.AffineXf3f.translation(trans))
        
        return (mesh,)

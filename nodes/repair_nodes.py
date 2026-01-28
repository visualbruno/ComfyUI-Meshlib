"""
Repair Nodes for ComfyUI-Meshlib
Mesh repair operations: fill holes, stitch holes, fix degeneracies, find self-intersections
"""

from tqdm import tqdm
from comfy.utils import ProgressBar


class MeshlibFillHoles:
    """Fill all holes in a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            },
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "INT")
    RETURN_NAMES = ("mesh", "holes_filled")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Repair"
    DESCRIPTION = "Fill all holes in a mesh using optimal triangulation."

    def process(self, mesh):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        hole_edges = mesh.topology.findHoleRepresentiveEdges()
        holes_filled = 0
        
        nb_holes = len(hole_edges)
        print(f"{nb_holes} holes found")
        
        if nb_holes>0:
            progress_bar = tqdm(total=nb_holes,desc="Filling holes")
            pbar = ProgressBar(nb_holes)
            
            for e in hole_edges:
                params = mrmeshpy.FillHoleParams()
                params.metric = mrmeshpy.getUniversalMetric(mesh)
                mrmeshpy.fillHole(mesh, e, params)
                holes_filled += 1
                progress_bar.update(1)
                pbar.update(1)
        
        return (mesh, holes_filled)


class MeshlibStitchHoles:
    """Stitch two holes together with a tunnel"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "hole_index_a": ("INT", {
                    "default": 0,
                    "min": 0,
                    "tooltip": "Index of first hole to stitch"
                }),
                "hole_index_b": ("INT", {
                    "default": 1,
                    "min": 0,
                    "tooltip": "Index of second hole to stitch"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Repair"
    DESCRIPTION = "Stitch two holes together creating a tunnel between them."

    def process(self, mesh, hole_index_a, hole_index_b):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        hole_edges = mesh.topology.findHoleRepresentiveEdges()
        
        if hole_index_a >= len(hole_edges) or hole_index_b >= len(hole_edges):
            raise ValueError(f"Hole index out of range. Mesh has {len(hole_edges)} holes.")
        
        if hole_index_a == hole_index_b:
            raise ValueError("Cannot stitch a hole to itself.")
        
        edge_a = hole_edges[hole_index_a]
        edge_b = hole_edges[hole_index_b]
        
        params = mrmeshpy.StitchHolesParams()
        mrmeshpy.stitchHoles(mesh, edge_a, edge_b, params)
        
        return (mesh,)


class MeshlibFixDegeneracies:
    """Fix mesh degeneracies (degenerate triangles, duplicate vertices, etc.)"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "max_deviation_factor": ("FLOAT", {
                    "default": 1e-5, 
                    "min": 0.0,
                    "max": 0.1,
                    "step": 1e-6,
                    "tooltip": "Maximum deviation as a factor of mesh diagonal"
                }),
                "tiny_edge_length": ("FLOAT", {
                    "default": 1e-3, 
                    "min": 0.0,
                    "max": 1.0,
                    "step": 1e-4,
                    "tooltip": "Edges shorter than this will be collapsed"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Repair"
    DESCRIPTION = "Fix mesh degeneracies including degenerate triangles, tiny edges, and duplicate vertices."

    def process(self, mesh, max_deviation_factor, tiny_edge_length):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        params = mrmeshpy.FixMeshDegeneraciesParams()
        params.maxDeviation = max_deviation_factor * mesh.computeBoundingBox().diagonal()
        params.tinyEdgeLength = tiny_edge_length
        
        mrmeshpy.fixMeshDegeneracies(mesh, params)
        
        return (mesh,)


class MeshlibFindSelfIntersections:
    """Find self-intersecting triangles in a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "INT", "BOOLEAN")
    RETURN_NAMES = ("mesh", "self_intersecting_faces", "has_intersections")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Repair"
    DESCRIPTION = "Find self-intersecting triangles in a mesh. Returns the count of intersecting faces."

    def process(self, mesh):
        import meshlib.mrmeshpy as mrmeshpy
        
        # Find self-intersecting faces
        # Returns a vector of FaceFace pairs
        intersecting_faces = mrmeshpy.findSelfCollidingTriangles(mesh)
        count = len(intersecting_faces)
        has_intersections = count > 0
        
        return (mesh, count, has_intersections)

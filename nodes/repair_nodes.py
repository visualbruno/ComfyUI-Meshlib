"""
Repair Nodes for ComfyUI-Meshlib
Mesh repair operations: fill holes, stitch holes, fix degeneracies, find self-intersections
"""


class MeshlibFillHoles:
    """Fill all holes in a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            },
            "optional": {
                "max_hole_edges": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "tooltip": "Maximum number of edges in holes to fill (0 = fill all holes)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "INT")
    RETURN_NAMES = ("mesh", "holes_filled")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Repair"
    DESCRIPTION = "Fill all holes in a mesh using optimal triangulation."

    def process(self, mesh, max_hole_edges=0):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        hole_edges = mesh.topology.findHoleRepresentiveEdges()
        holes_filled = 0
        
        for e in hole_edges:
            # Skip holes that are too large if max_hole_edges is set
            if max_hole_edges > 0:
                # Count edges in this hole
                hole_loop = mesh.topology.trackLeftBoundaryLoop(e)
                if len(hole_loop) > max_hole_edges:
                    continue
            
            params = mrmeshpy.FillHoleParams()
            params.metric = mrmeshpy.getUniversalMetric(mesh)
            mrmeshpy.fillHole(mesh, e, params)
            holes_filled += 1
        
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
        intersecting_faces = mrmeshpy.findSelfCollidingTriangles(mesh)
        count = intersecting_faces.count()
        has_intersections = count > 0
        
        return (mesh, count, has_intersections)

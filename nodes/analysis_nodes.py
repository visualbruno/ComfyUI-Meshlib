"""
Analysis Nodes for ComfyUI-Meshlib
Mesh analysis: signed distance, collision detection, mesh info
"""


class MeshlibSignedDistance:
    """Calculate signed distance between two meshes"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh_a": ("MESHLIB_MESH", {"tooltip": "First mesh"}),
                "mesh_b": ("MESHLIB_MESH", {"tooltip": "Second mesh"}),
            }
        }
    
    RETURN_TYPES = ("FLOAT", "STRING")
    RETURN_NAMES = ("signed_distance", "info")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Analysis"
    DESCRIPTION = """Calculate the minimum signed distance between two meshes.
Positive distance means meshes are separated, negative means they overlap."""

    def process(self, mesh_a, mesh_b):
        import meshlib.mrmeshpy as mrmeshpy
        
        result = mrmeshpy.findSignedDistance(mesh_a, mesh_b)
        
        info = f"Signed distance: {result.signedDist:.6f}"
        
        return (result.signedDist, info)


class MeshlibCollisionDetection:
    """Detect collisions between two meshes"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh_a": ("MESHLIB_MESH", {"tooltip": "First mesh"}),
                "mesh_b": ("MESHLIB_MESH", {"tooltip": "Second mesh"}),
                "detailed": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "If True, count all colliding faces. If False, just check if any collision exists (faster)."
                }),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN", "INT", "INT")
    RETURN_NAMES = ("is_colliding", "colliding_faces_a", "colliding_faces_b")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Analysis"
    DESCRIPTION = "Detect if two meshes collide and count the number of colliding faces."

    def process(self, mesh_a, mesh_b, detailed):
        import meshlib.mrmeshpy as mrmeshpy
        
        if not detailed:
            # Fast collision check
            is_colliding = not mrmeshpy.findCollidingTriangles(
                mesh_a, mesh_b, firstIntersectionOnly=True).empty()
            return (is_colliding, 0, 0)
        
        # Detailed collision detection
        bitset_a, bitset_b = mrmeshpy.findCollidingTriangleBitsets(mesh_a, mesh_b)
        count_a = bitset_a.count()
        count_b = bitset_b.count()
        is_colliding = count_a > 0
        
        return (is_colliding, count_a, count_b)


class MeshlibGetMeshInfo:
    """Get information about a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "INT", "FLOAT", "FLOAT", "FLOAT", "STRING")
    RETURN_NAMES = ("num_vertices", "num_faces", "num_holes", "surface_area", "volume", "bbox_diagonal", "info_string")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Analysis"
    DESCRIPTION = "Get detailed information about a mesh including vertex/face counts, surface area, volume, and bounding box."

    def process(self, mesh):
        import meshlib.mrmeshpy as mrmeshpy
        
        num_verts = mesh.topology.numValidVerts()
        num_faces = mesh.topology.numValidFaces()
        
        # Count holes
        hole_edges = mesh.topology.findHoleRepresentiveEdges()
        num_holes = len(hole_edges)
        
        # Compute bounding box
        bbox = mesh.computeBoundingBox()
        diagonal = bbox.diagonal()
        
        # Compute surface area
        surface_area = mesh.area()
        
        # Compute volume (only valid for closed meshes)
        try:
            volume = mesh.volume()
        except:
            volume = 0.0
        
        # Build info string
        info_lines = [
            f"Vertices: {num_verts}",
            f"Faces: {num_faces}",
            f"Holes: {num_holes}",
            f"Surface Area: {surface_area:.4f}",
            f"Volume: {volume:.4f}",
            f"BBox Diagonal: {diagonal:.4f}",
            f"BBox Min: ({bbox.min.x:.4f}, {bbox.min.y:.4f}, {bbox.min.z:.4f})",
            f"BBox Max: ({bbox.max.x:.4f}, {bbox.max.y:.4f}, {bbox.max.z:.4f})",
        ]
        info_string = "\n".join(info_lines)
        
        return (num_verts, num_faces, num_holes, surface_area, volume, diagonal, info_string)

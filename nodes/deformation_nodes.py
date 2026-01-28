"""
Deformation Nodes for ComfyUI-Meshlib
Free-form and Laplacian mesh deformation
"""


class MeshlibFreeFormDeform:
    """Apply free-form deformation to a mesh using a control grid"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "grid_resolution": ("INT", {
                    "default": 3,
                    "min": 2,
                    "max": 10,
                    "tooltip": "Resolution of the control grid (NxNxN)"
                }),
                "deform_center_x": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                    "tooltip": "X offset for center control points"
                }),
                "deform_center_y": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                    "tooltip": "Y offset for center control points"
                }),
                "deform_center_z": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                    "tooltip": "Z offset for center control points"
                }),
                "deform_strength": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "Strength of the deformation"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Deformation"
    DESCRIPTION = """Apply free-form deformation using a control grid. 
The center control points are moved according to the deform offsets."""

    def process(self, mesh, grid_resolution, deform_center_x, deform_center_y, 
                deform_center_z, deform_strength):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        # Construct deformer on mesh vertices
        ffDeformer = mrmeshpy.FreeFormDeformer(mesh.points, mesh.topology.getValidVerts())
        
        # Compute mesh bounding box
        box = mesh.computeBoundingBox()
        
        # Init deformer with NxNxN grid on mesh box
        ffDeformer.init(mrmeshpy.Vector3i.diagonal(grid_resolution), box)
        
        # Calculate center index
        center = grid_resolution // 2
        
        # Calculate target position (center of box + offset)
        box_center = box.center()
        offset = mrmeshpy.Vector3f(
            deform_center_x * deform_strength,
            deform_center_y * deform_strength,
            deform_center_z * deform_strength
        )
        target = mrmeshpy.Vector3f(
            box_center.x + offset.x,
            box_center.y + offset.y,
            box_center.z + offset.z
        )
        
        # Move center control points toward the target
        # This creates a "pinch" or "bulge" effect
        for i in range(grid_resolution):
            for j in range(grid_resolution):
                for k in range(grid_resolution):
                    # Calculate distance from center
                    di = abs(i - center)
                    dj = abs(j - center)
                    dk = abs(k - center)
                    
                    # Only move points near the center
                    if di <= 1 and dj <= 1 and dk <= 1:
                        weight = 1.0 - (di + dj + dk) / 3.0
                        if weight > 0:
                            grid_pos = mrmeshpy.Vector3i(i, j, k)
                            current_pos = ffDeformer.getRefGridPointPosition(grid_pos)
                            new_pos = mrmeshpy.Vector3f(
                                current_pos.x + offset.x * weight,
                                current_pos.y + offset.y * weight,
                                current_pos.z + offset.z * weight
                            )
                            ffDeformer.setRefGridPointPosition(grid_pos, new_pos)
        
        # Apply deformation to mesh vertices
        ffDeformer.apply()
        
        # Invalidate mesh caches
        mesh.invalidateCaches()
        
        return (mesh,)


class MeshlibLaplacianDeform:
    """Apply Laplacian deformation to a mesh"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "anchor_vertex_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "tooltip": "Index of the anchor vertex to move"
                }),
                "move_x": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                    "tooltip": "Movement in X direction"
                }),
                "move_y": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.1,
                    "tooltip": "Movement in Y direction"
                }),
                "move_z": ("FLOAT", {
                    "default": 0.1,
                    "step": 0.1,
                    "tooltip": "Movement in Z direction"
                }),
                "influence_radius": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 50,
                    "tooltip": "Number of expansion iterations for the deformation region"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Deformation"
    DESCRIPTION = """Apply Laplacian deformation which smoothly deforms a region 
of the mesh while preserving local shape details."""

    def process(self, mesh, anchor_vertex_index, move_x, move_y, move_z, influence_radius):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        # Construct Laplacian deformer
        lDeformer = mrmeshpy.Laplacian(mesh)
        
        # Get valid vertices
        valid_verts = mesh.topology.getValidVerts()
        num_verts = valid_verts.count()
        
        if anchor_vertex_index >= num_verts:
            raise ValueError(f"Anchor vertex index {anchor_vertex_index} out of range. Mesh has {num_verts} vertices.")
        
        # Find the actual vertex ID at the given index
        anchor_v = mrmeshpy.VertId(anchor_vertex_index)
        
        # Mark anchor point in free area
        freeVerts = mrmeshpy.VertBitSet()
        freeVerts.resize(valid_verts.size())
        freeVerts.set(anchor_v, True)
        
        # Expand free area
        mrmeshpy.expand(mesh.topology, freeVerts, influence_radius)
        
        # Initialize Laplacian
        lDeformer.init(freeVerts, mrmeshpy.EdgeWeights.Cotan, mrmeshpy.VertexMass.NeiArea)
        
        # Get current position and compute new position
        current_pos = mesh.points.vec[anchor_vertex_index]
        new_pos = mrmeshpy.Vector3f(
            current_pos.x + move_x,
            current_pos.y + move_y,
            current_pos.z + move_z
        )
        
        # Fix anchor vertex at new position
        lDeformer.fixVertex(anchor_v, new_pos)
        
        # Apply deformation
        lDeformer.apply()
        
        # Invalidate mesh caches
        mesh.invalidateCaches()
        
        return (mesh,)

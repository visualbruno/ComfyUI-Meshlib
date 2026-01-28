"""
Alignment Nodes for ComfyUI-Meshlib
Mesh alignment using ICP (Iterative Closest Point)
"""


class MeshlibICP:
    """Align two meshes using Iterative Closest Point algorithm"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh_floating": ("MESHLIB_MESH", {
                    "tooltip": "The mesh that will be transformed to align with the fixed mesh"
                }),
                "mesh_fixed": ("MESHLIB_MESH", {
                    "tooltip": "The reference mesh that stays in place"
                }),
                "sampling_factor": ("FLOAT", {
                    "default": 0.01, 
                    "min": 0.001, 
                    "max": 0.1,
                    "step": 0.001,
                    "tooltip": "Sampling density as a factor of mesh diagonal"
                }),
                "distance_threshold_factor": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.01,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Maximum distance for point pairs as a factor of mesh diagonal"
                }),
                "exit_distance_factor": ("FLOAT", {
                    "default": 0.003,
                    "min": 0.0001,
                    "max": 0.1,
                    "step": 0.0001,
                    "tooltip": "Stop when mean distance reaches this factor of mesh diagonal"
                }),
                "max_iterations": ("INT", {
                    "default": 100,
                    "min": 1,
                    "max": 1000,
                    "tooltip": "Maximum number of ICP iterations"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH", "STRING")
    RETURN_NAMES = ("aligned_mesh", "info")
    FUNCTION = "process"
    CATEGORY = "Meshlib/Alignment"
    DESCRIPTION = """Align a floating mesh to a fixed reference mesh using ICP.
The floating mesh is transformed to best match the fixed mesh."""

    def process(self, mesh_floating, mesh_fixed, sampling_factor, 
                distance_threshold_factor, exit_distance_factor, max_iterations):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh_floating = mrmeshpy.copyMesh(mesh_floating)
        
        diagonal = mesh_fixed.getBoundingBox().diagonal()
        icp_sampling_voxel_size = diagonal * sampling_factor
        
        icp_params = mrmeshpy.ICPProperties()
        icp_params.distThresholdSq = (diagonal * distance_threshold_factor) ** 2
        icp_params.exitVal = diagonal * exit_distance_factor
        icp_params.iterLimit = max_iterations
        
        icp = mrmeshpy.ICP(
            mesh_floating, mesh_fixed,
            mrmeshpy.AffineXf3f(), mrmeshpy.AffineXf3f(),
            icp_sampling_voxel_size
        )
        icp.setParams(icp_params)
        xf = icp.calculateTransformation()
        
        mesh_floating.transform(xf)
        
        # Get alignment info
        try:
            info = str(icp.getLastICPInfo())
        except:
            info = "ICP completed"
        
        return (mesh_floating, info)

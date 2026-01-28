"""
Noise Nodes for ComfyUI-Meshlib
Add noise and denoise meshes
"""


class MeshlibAddNoise:
    """Add random noise to mesh vertices"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "sigma_factor": ("FLOAT", {
                    "default": 0.001, 
                    "min": 0.0,
                    "max": 0.1,
                    "step": 0.0001,
                    "tooltip": "Noise intensity as a factor of mesh bounding box diagonal"
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "tooltip": "Random seed for reproducible noise"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Noise"
    DESCRIPTION = "Add random Gaussian noise to mesh vertex positions."

    def process(self, mesh, sigma_factor, seed):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        settings = mrmeshpy.NoiseSettings()
        settings.sigma = mesh.computeBoundingBox().diagonal() * sigma_factor
        settings.seed = seed
        
        mrmeshpy.addNoise(mesh.points, mesh.topology.getValidVerts(), settings)
        mesh.invalidateCaches()
        
        return (mesh,)


class MeshlibDenoise:
    """Denoise a mesh using Mumford-Shah framework"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            },
            "optional": {
                "iterations": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "tooltip": "Number of denoising iterations"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Noise"
    DESCRIPTION = """Denoise a mesh using the Mumford-Shah framework.
This method preserves sharp edges while smoothing noisy areas."""

    def process(self, mesh, iterations=1):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.copyMesh(mesh)
        
        for _ in range(iterations):
            mrmeshpy.meshDenoiseViaNormals(mesh)
        
        return (mesh,)

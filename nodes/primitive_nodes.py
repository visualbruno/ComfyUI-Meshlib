"""
Primitive Nodes for ComfyUI-Meshlib
Creates basic mesh primitives
"""


class MeshlibMakeSphere:
    """Create a UV sphere primitive"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "radius": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Radius of the sphere"
                }),
                "horizontal_resolution": ("INT", {
                    "default": 64, 
                    "min": 4, 
                    "max": 512,
                    "tooltip": "Number of horizontal segments"
                }),
                "vertical_resolution": ("INT", {
                    "default": 64, 
                    "min": 4, 
                    "max": 512,
                    "tooltip": "Number of vertical segments"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Primitives"
    DESCRIPTION = "Create a UV sphere mesh primitive."

    def process(self, radius, horizontal_resolution, vertical_resolution):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.makeUVSphere(radius, horizontal_resolution, vertical_resolution)
        return (mesh,)


class MeshlibMakeCube:
    """Create a cube primitive"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "size_x": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Size in X direction"
                }),
                "size_y": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Size in Y direction"
                }),
                "size_z": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Size in Z direction"
                }),
                "center": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Center the cube at origin"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Primitives"
    DESCRIPTION = "Create a cube/box mesh primitive."

    def process(self, size_x, size_y, size_z, center):
        import meshlib.mrmeshpy as mrmeshpy
        
        size = mrmeshpy.Vector3f(size_x, size_y, size_z)
        
        if center:
            base = mrmeshpy.Vector3f(-size_x / 2, -size_y / 2, -size_z / 2)
        else:
            base = mrmeshpy.Vector3f(0, 0, 0)
        
        mesh = mrmeshpy.makeCube(size, base)
        return (mesh,)


class MeshlibMakeTorus:
    """Create a torus primitive"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "primary_radius": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Distance from center of torus to center of tube"
                }),
                "secondary_radius": ("FLOAT", {
                    "default": 0.2, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Radius of the tube"
                }),
                "primary_resolution": ("INT", {
                    "default": 64, 
                    "min": 4, 
                    "max": 512,
                    "tooltip": "Number of segments around the main ring"
                }),
                "secondary_resolution": ("INT", {
                    "default": 32, 
                    "min": 4, 
                    "max": 512,
                    "tooltip": "Number of segments around the tube"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Primitives"
    DESCRIPTION = "Create a torus mesh primitive."

    def process(self, primary_radius, secondary_radius, primary_resolution, secondary_resolution):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.makeTorus(primary_radius, secondary_radius, primary_resolution, secondary_resolution)
        return (mesh,)


class MeshlibMakeCylinder:
    """Create a cylinder primitive"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "radius": ("FLOAT", {
                    "default": 0.5, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Radius of the cylinder"
                }),
                "length": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.001, 
                    "max": 1000.0,
                    "step": 0.1,
                    "tooltip": "Length/height of the cylinder"
                }),
                "resolution": ("INT", {
                    "default": 64, 
                    "min": 4, 
                    "max": 512,
                    "tooltip": "Number of segments around the circumference"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Primitives"
    DESCRIPTION = "Create a cylinder mesh primitive."

    def process(self, radius, length, resolution):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.makeCylinder(radius, length, resolution)
        return (mesh,)

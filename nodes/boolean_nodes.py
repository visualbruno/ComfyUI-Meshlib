"""
Boolean Nodes for ComfyUI-Meshlib
Boolean operations on meshes
"""


class MeshlibBoolean:
    """Perform boolean operations on two meshes"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh_a": ("MESHLIB_MESH", {"tooltip": "First mesh (A)"}),
                "mesh_b": ("MESHLIB_MESH", {"tooltip": "Second mesh (B)"}),
                "operation": ([
                    "Union", 
                    "Intersection", 
                    "DifferenceAB",  # A - B
                    "DifferenceBA",  # B - A
                ], {
                    "default": "Union",
                    "tooltip": "Boolean operation to perform"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/Boolean"
    DESCRIPTION = """Perform boolean operations on two meshes.
    
- Union: Combine both meshes
- Intersection: Keep only overlapping parts
- DifferenceAB: Subtract B from A
- DifferenceBA: Subtract A from B"""

    def process(self, mesh_a, mesh_b, operation):
        import meshlib.mrmeshpy as mrmeshpy
        
        op_map = {
            "Union": mrmeshpy.BooleanOperation.Union,
            "Intersection": mrmeshpy.BooleanOperation.Intersection,
            "DifferenceAB": mrmeshpy.BooleanOperation.DifferenceAMinusB,
            "DifferenceBA": mrmeshpy.BooleanOperation.DifferenceBMinusA,
        }
        
        result = mrmeshpy.boolean(mesh_a, mesh_b, op_map[operation])
        
        if not result.valid():
            raise ValueError(f"Boolean operation failed: {result.errorString}")
        
        return (result.mesh,)

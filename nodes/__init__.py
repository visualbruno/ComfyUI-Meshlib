# ComfyUI-Meshlib Nodes
# This module exports all node classes for ComfyUI registration

from .io_nodes import (
    MeshlibLoadMesh,
    MeshlibSaveMesh,
    MeshlibLoadPoints,
    MeshlibSavePoints,
    MeshlibFromTrimesh,
    MeshlibToTrimesh,
    MeshlibCopyMesh,
)

from .primitive_nodes import (
    MeshlibMakeSphere,
    MeshlibMakeCube,
    MeshlibMakeTorus,
    MeshlibMakeCylinder,
)

from .boolean_nodes import (
    MeshlibBoolean,
)

from .modification_nodes import (
    MeshlibDecimate,
    MeshlibSubdivide,
    MeshlibOffset,
    MeshlibRelax,
    MeshlibTransform,
)

from .repair_nodes import (
    MeshlibFillHoles,
    MeshlibStitchHoles,
    MeshlibFixDegeneracies,
    MeshlibFindSelfIntersections,
)

from .deformation_nodes import (
    MeshlibFreeFormDeform,
    MeshlibLaplacianDeform,
)

from .analysis_nodes import (
    MeshlibSignedDistance,
    MeshlibCollisionDetection,
    MeshlibGetMeshInfo,
)

from .alignment_nodes import (
    MeshlibICP,
)

from .pointcloud_nodes import (
    MeshlibTriangulatePointCloud,
    MeshlibPointSampling,
    MeshlibPointCloudFromMesh,
)

from .noise_nodes import (
    MeshlibAddNoise,
    MeshlibDenoise,
)

# Export all node classes
NODE_CLASS_MAPPINGS = {
    # I/O Nodes
    "MeshlibLoadMesh": MeshlibLoadMesh,
    "MeshlibSaveMesh": MeshlibSaveMesh,
    "MeshlibLoadPoints": MeshlibLoadPoints,
    "MeshlibSavePoints": MeshlibSavePoints,
    "MeshlibFromTrimesh": MeshlibFromTrimesh,
    "MeshlibToTrimesh": MeshlibToTrimesh,
    "MeshlibCopyMesh": MeshlibCopyMesh,
    
    # Primitive Nodes
    "MeshlibMakeSphere": MeshlibMakeSphere,
    "MeshlibMakeCube": MeshlibMakeCube,
    "MeshlibMakeTorus": MeshlibMakeTorus,
    "MeshlibMakeCylinder": MeshlibMakeCylinder,
    
    # Boolean Nodes
    "MeshlibBoolean": MeshlibBoolean,
    
    # Modification Nodes
    "MeshlibDecimate": MeshlibDecimate,
    "MeshlibSubdivide": MeshlibSubdivide,
    "MeshlibOffset": MeshlibOffset,
    "MeshlibRelax": MeshlibRelax,
    "MeshlibTransform": MeshlibTransform,
    
    # Repair Nodes
    "MeshlibFillHoles": MeshlibFillHoles,
    "MeshlibStitchHoles": MeshlibStitchHoles,
    "MeshlibFixDegeneracies": MeshlibFixDegeneracies,
    "MeshlibFindSelfIntersections": MeshlibFindSelfIntersections,
    
    # Deformation Nodes
    "MeshlibFreeFormDeform": MeshlibFreeFormDeform,
    "MeshlibLaplacianDeform": MeshlibLaplacianDeform,
    
    # Analysis Nodes
    "MeshlibSignedDistance": MeshlibSignedDistance,
    "MeshlibCollisionDetection": MeshlibCollisionDetection,
    "MeshlibGetMeshInfo": MeshlibGetMeshInfo,
    
    # Alignment Nodes
    "MeshlibICP": MeshlibICP,
    
    # Point Cloud Nodes
    "MeshlibTriangulatePointCloud": MeshlibTriangulatePointCloud,
    "MeshlibPointSampling": MeshlibPointSampling,
    "MeshlibPointCloudFromMesh": MeshlibPointCloudFromMesh,
    
    # Noise Nodes
    "MeshlibAddNoise": MeshlibAddNoise,
    "MeshlibDenoise": MeshlibDenoise,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # I/O Nodes
    "MeshlibLoadMesh": "Meshlib - Load Mesh",
    "MeshlibSaveMesh": "Meshlib - Save Mesh",
    "MeshlibLoadPoints": "Meshlib - Load Points",
    "MeshlibSavePoints": "Meshlib - Save Points",
    "MeshlibFromTrimesh": "Meshlib - From Trimesh",
    "MeshlibToTrimesh": "Meshlib - To Trimesh",
    "MeshlibCopyMesh": "Meshlib - Copy Mesh",
    
    # Primitive Nodes
    "MeshlibMakeSphere": "Meshlib - Make Sphere",
    "MeshlibMakeCube": "Meshlib - Make Cube",
    "MeshlibMakeTorus": "Meshlib - Make Torus",
    "MeshlibMakeCylinder": "Meshlib - Make Cylinder",
    
    # Boolean Nodes
    "MeshlibBoolean": "Meshlib - Boolean",
    
    # Modification Nodes
    "MeshlibDecimate": "Meshlib - Decimate",
    "MeshlibSubdivide": "Meshlib - Subdivide",
    "MeshlibOffset": "Meshlib - Offset",
    "MeshlibRelax": "Meshlib - Relax",
    "MeshlibTransform": "Meshlib - Transform",
    
    # Repair Nodes
    "MeshlibFillHoles": "Meshlib - Fill Holes",
    "MeshlibStitchHoles": "Meshlib - Stitch Holes",
    "MeshlibFixDegeneracies": "Meshlib - Fix Degeneracies",
    "MeshlibFindSelfIntersections": "Meshlib - Find Self Intersections",
    
    # Deformation Nodes
    "MeshlibFreeFormDeform": "Meshlib - Free Form Deform",
    "MeshlibLaplacianDeform": "Meshlib - Laplacian Deform",
    
    # Analysis Nodes
    "MeshlibSignedDistance": "Meshlib - Signed Distance",
    "MeshlibCollisionDetection": "Meshlib - Collision Detection",
    "MeshlibGetMeshInfo": "Meshlib - Get Mesh Info",
    
    # Alignment Nodes
    "MeshlibICP": "Meshlib - ICP Alignment",
    
    # Point Cloud Nodes
    "MeshlibTriangulatePointCloud": "Meshlib - Triangulate Point Cloud",
    "MeshlibPointSampling": "Meshlib - Point Sampling",
    "MeshlibPointCloudFromMesh": "Meshlib - Point Cloud From Mesh",
    
    # Noise Nodes
    "MeshlibAddNoise": "Meshlib - Add Noise",
    "MeshlibDenoise": "Meshlib - Denoise",
}

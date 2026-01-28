"""
Point Cloud Nodes for ComfyUI-Meshlib
Point cloud triangulation and sampling
"""


class MeshlibTriangulatePointCloud:
    """Convert a point cloud to a mesh via triangulation"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "points": ("MESHLIB_POINTCLOUD",),
            },
            "optional": {
                "fix_mesh": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Apply offset with 0 distance to fix mesh issues after triangulation"
                }),
                "voxel_count": ("INT", {
                    "default": 5000000,
                    "min": 100000,
                    "max": 50000000,
                    "tooltip": "Voxel count for mesh fixing (if enabled)"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_MESH",)
    RETURN_NAMES = ("mesh",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/PointCloud"
    DESCRIPTION = "Triangulate a point cloud to create a mesh surface."

    def process(self, points, fix_mesh=True, voxel_count=5000000):
        import meshlib.mrmeshpy as mrmeshpy
        
        mesh = mrmeshpy.triangulatePointCloud(points)
        
        if fix_mesh and mesh is not None:
            # Fix possible issues with offset of 0
            params = mrmeshpy.OffsetParameters()
            params.voxelSize = mrmeshpy.suggestVoxelSize(mesh, voxel_count)
            mesh = mrmeshpy.offsetMesh(mesh, 0.0, params)
        
        return (mesh,)


class MeshlibPointSampling:
    """Sample points uniformly from a mesh surface"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
                "num_samples": ("INT", {
                    "default": 10000,
                    "min": 100,
                    "max": 10000000,
                    "tooltip": "Approximate number of points to sample"
                }),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_POINTCLOUD",)
    RETURN_NAMES = ("points",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/PointCloud"
    DESCRIPTION = "Sample points uniformly from a mesh surface."

    def process(self, mesh, num_samples):
        import meshlib.mrmeshpy as mrmeshpy
        
        # Calculate approximate sampling distance based on surface area
        area = mesh.area()
        if area > 0:
            # Approximate distance needed for num_samples points
            # Area per point = total_area / num_samples
            # For uniform distribution, distance ~ sqrt(area_per_point)
            import math
            distance = math.sqrt(area / num_samples)
        else:
            distance = 0.01
        
        # Create point cloud from mesh
        settings = mrmeshpy.UniformSamplingSettings()
        settings.distance = distance
        
        point_cloud = mrmeshpy.pointCloudFromMesh(mesh)
        
        # Uniformly sample
        valid_points = mrmeshpy.pointUniformSampling(point_cloud, settings)
        if valid_points:
            point_cloud.validPoints = valid_points
            point_cloud.invalidateCaches()
        
        return (point_cloud,)


class MeshlibPointCloudFromMesh:
    """Convert a mesh to a point cloud"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mesh": ("MESHLIB_MESH",),
            }
        }
    
    RETURN_TYPES = ("MESHLIB_POINTCLOUD",)
    RETURN_NAMES = ("points",)
    FUNCTION = "process"
    CATEGORY = "Meshlib/PointCloud"
    DESCRIPTION = "Convert a mesh to a point cloud (extracts all vertices)."

    def process(self, mesh):
        import meshlib.mrmeshpy as mrmeshpy
        
        point_cloud = mrmeshpy.pointCloudFromMesh(mesh)
        
        return (point_cloud,)

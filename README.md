# 🌀 ComfyUI Wrapper for https://github.com/MeshInspector/MeshLib


## ⚙️ Nodes

---

### 1. IO Nodes

<img width="765" height="239" alt="{0ACE9ED0-67E9-4490-99BE-B05251B2BC8C}" src="https://github.com/user-attachments/assets/a008e3e1-1488-4e95-87c0-ffff1c526f9e" />

| Node | Description |
| --- | --- |
| Meshlib - Load Mesh	| Load mesh from file (STL, OBJ, PLY, CTM, GLB, OFF) |
| Meshlib - Save Mesh	| Save mesh to file |
| Meshlib - Load Points	| Load point cloud from file |
| Meshlib - Save Points	| Save point cloud to file |
| Meshlib - From Trimesh | Convert Trimesh object to MeshLib Mesh |
| Meshlib - To Trimesh | Convert MeshLib Mesh to Trimesh object |
| Meshlib - Copy Mesh | Create a deep copy of a mesh |

---

### 2. Primitive Nodes

<img width="474" height="298" alt="{3321009F-CFFB-4D0C-9A59-20CFF5EA93D3}" src="https://github.com/user-attachments/assets/5c047c4b-914a-4aa9-9673-617da7c3b599" />

| Node | Description |
| --- | --- |
| Meshlib - Make Sphere	| Create a UV sphere with configurable radius and resolution |
| Meshlib - Make Cube	| Create a box with configurable dimensions |
| Meshlib - Make Torus | Create a torus with primary/secondary radius |
| Meshlib - Make Cylinder | Create a cylinder with configurable radius and length |

---

### 3. Boolean Operations

<img width="232" height="132" alt="image" src="https://github.com/user-attachments/assets/aafc68ac-ca0b-45de-b514-06557de36cb5" />

| Node | Description |
| --- | --- |
| Meshlib - Boolean |	Perform Union, Intersection, or Difference operations on two meshes |

---

### 4. Modification Nodes

<img width="632" height="423" alt="{A47D6A16-6C9B-4BD1-9904-D38B13A07BA1}" src="https://github.com/user-attachments/assets/07efa203-ed25-4fb8-855c-a670099a3984" />

| Node | Description |
| --- | --- |
| Meshlib - Decimate | Reduce triangle count while preserving shape |
| Meshlib - Subdivide | Increase mesh resolution by splitting edges |
| Meshlib - Offset | Create offset surface (shell) - positive expands, negative shrinks |
| Meshlib - Relax | Smooth mesh by relaxing vertex positions |
| Meshlib - Transform | Apply translation, rotation, and uniform scaling |

---

### 5. Repair Nodes

<img width="597" height="253" alt="image" src="https://github.com/user-attachments/assets/e3a4dda1-64c4-4032-b35b-36e6d5af04c9" />

| Node | Description |
| --- | --- |
| Meshlib - Fill Holes | Automatically fill all holes in a mesh |
| Meshlib - Stitch Holes | Connect two holes with a tunnel |
| Meshlib - Fix Degeneracies | Fix degenerate triangles, tiny edges, duplicate vertices |
| Meshlib - Find Self Intersections | Detect self-intersecting triangles |

---

### 6. Deformation Nodes

<img width="548" height="187" alt="{85E60C0A-53D1-459A-8B8C-70731E82AF72}" src="https://github.com/user-attachments/assets/8f73c546-7777-4b1f-b19d-152b8efa43cc" />

| Node | Description |
| --- | --- |
| Meshlib - Free Form Deform | Apply free-form deformation using a control grid |
| Meshlib - Laplacian Deform | Smooth deformation preserving local shape details |

---

### 7. Analysis Nodes

<img width="470" height="265" alt="{A740476E-4ED0-4477-BC7C-8ECBAD648D63}" src="https://github.com/user-attachments/assets/3a564fda-dc84-46a6-90cd-291cd2e675f4" />

| Node | Description |
| --- | --- |
| Meshlib - Signed Distance | Calculate minimum signed distance between two meshes |
| Meshlib - Collision Detection | Detect if two meshes collide and count colliding faces |
| Meshlib - Get Mesh Info | Get vertex/face counts, surface area, volume, bounding box |

---

### 8. Alignment Nodes

<img width="390" height="203" alt="{C885AD16-31E9-4009-AC3A-7A4D617D8C27}" src="https://github.com/user-attachments/assets/e286fa4b-2d40-4126-834f-aef0c0835aa9" />

| Node | Description |
| --- | --- |
| Meshlib - ICP Alignment | Align meshes using Iterative Closest Point algorithm |

---

### 9. Point Cloud Nodes

<img width="469" height="214" alt="{08CE858E-8F46-4F2E-8C67-235571BF632D}" src="https://github.com/user-attachments/assets/51d73a9b-f8b4-43a8-aa13-75f9096f5394" />

| Node | Description |
| --- | --- |
| Meshlib - Triangulate Point Cloud | Convert point cloud to mesh surface |
| Meshlib - Point Sampling | Sample points uniformly from mesh surface |
| Meshlib - Point Cloud From Mesh | Convert mesh vertices to point cloud |

---

### 10. Noise Nodes

<img width="512" height="170" alt="{B6B18D4D-CABA-492E-BE87-00EDA0F8504B}" src="https://github.com/user-attachments/assets/df8510a7-871f-4860-a92d-e1d7fb3fcb2c" />

| Node | Description |
| --- | --- |
| Meshlib - Add Noise | Add Gaussian noise to vertex positions |
| Meshlib - Denoise | Remove noise using Mumford-Shah framework (preserves sharp edges) |



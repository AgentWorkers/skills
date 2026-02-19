---
name: pywayne-visualization-rerun-utils
description: 这些静态3D可视化工具基于Rerun SDK开发，用于添加点云、轨迹、相机、平面以及棋盘等元素。它们适用于在Rerun环境中可视化3D数据，包括SLAM（Simultaneous Localization and Mapping）轨迹、机器人姿态、相机标定目标等。所有这些工具都是静态的（即不需要管理任何视图器实例）。对于SE(3)/SO(3)矩阵运算，建议使用pywayne-vio-se3或pywayne-vio-so3库。
---
# Pywayne Visualization Rerun Utils

`pywaynevisualization.rerun_utils.RerunUtils` 提供了用于向 Rerun 查看器中添加 3D 元素的静态方法。

## 快速入门

```python
import numpy as np
import rerun as rr
from pywayne.visualization.rerun_utils import RerunUtils

# Initialize Rerun (called once globally)
rr.init('my_app', spawn=True)

# Use static methods to add elements
RerunUtils.add_point_cloud(points, colors=[255, 0, 0])
RerunUtils.add_trajectory(trajectory)
RerunUtils.add_camera(pose, image='path/to/image.jpg')
```

## 点云（Point Cloud）

```python
# Single color (default: red)
RerunUtils.add_point_cloud(points)

# Multi-color points
colors = np.random.randint(0, 255, (100, 3))
RerunUtils.add_point_cloud(points, colors=colors, label='colored')

# Data format: points (N, 3)
```

## 轨迹（Trajectory）

```python
# Single-color trajectory (default: green)
RerunUtils.add_trajectory(trajectory)

# Multi-color trajectory
colors = np.array([[0, 255, 0], [255, 0, 0]], dtype=np.float32)
RerunUtils.add_trajectory(trajectory, colors=colors, label='path')

# Data format: traj_endpoints (N, 3)
```

## 相机（Camera）

```python
# Camera only (no image)
RerunUtils.add_camera(pose, label='main_camera')

# Camera with image
RerunUtils.add_camera(pose, image='path/to/image.jpg', label='rgb_camera')

# Data format: camera_pose (4, 4) or (4, 7)
```

## 平面（Plane）

```python
# Plane by center and normal
RerunUtils.add_plane_from_center_and_normal(center, normal, half_size=1.0)

# Plane from SE3 transformation matrix
RerunUtils.add_plane_from_Twp(Twp, half_size=1.0)
```

## 国际象棋棋盘（Chessboard）

```python
# Standard chessboard
RerunUtils.add_chessboard_from_Twp()

# Custom chessboard with colors
RerunUtils.add_chessboard_from_Twp(
    rows=9, cols=6, cell_size=0.025,
    Twp=pose_matrix,
    color1=np.array([255, 0, 0]),  # Red
    color2=np.array([0, 0, 255])   # Blue
    label='calib_board'
)
```

## 内部辅助函数（Internal Helper Functions）

```python
# Get quaternion from v1 to v2 (used internally for plane rotation)
quat = RerunUtils._get_quaternion_from_v1_and_v2(v1, v2)
```

## 重要说明：

- **初始化**：在使用这些方法之前，请先调用 `rr.init('name', spawn=True)`。
- **静态方法**：所有方法都是静态类方法，无需创建实例。
- **依赖项**：需要 Rerun SDK（通过 `gettool` 自动下载）。
- **数据类型**：所有位置输入必须为 `float32` 类型。
- **坐标系**：Rerun 使用 `ViewCoordinates.RDF`（以机器人为中心的坐标系统）。
- **SE3 姿态**：支持 (4, 4) 或 (4, 7) 格式的矩阵。
- **颜色格式**：颜色数据应为形状为 (3,) 的 numpy 数组（RGB 格式）。
---
name: pywayne-visualization-pangolin-utils
description: 这是一个3D可视化工具包，它基于Pangolin视图器实现点云、轨迹、相机位置、平面以及图像的实时显示功能。适用于可视化传感器数据（如IMU、SLAM、跟踪系统产生的数据）、机器人状态，以及包含相机姿态和轨迹的任何3D数据。该工具包支持双图像显示模式、用于调试的步进模式（step mode），以及主相机跟随功能（main camera following）。
---
# Pywayne Visualization Pangolin 工具库

`pywaynevisualization.pangolin_utils.PangolinViewer` 提供了一个 Python 接口，用于操作 Pangolin 3D 可视化库。

## 快速入门

```python
from pywayne.visualization.pangolin_utils import PangolinViewer, Colors
import numpy as np

# Create viewer
viewer = PangolinViewer(800, 600)
viewer.init()

# Run visualization loop
while viewer.should_not_quit():
    # ... add/update visual elements ...
    viewer.show(delay_time_in_s=0.03)

viewer.join()  # Wait for window to close
```

## 颜色

使用 `Colors` 类来设置常用颜色：

```python
Colors.RED      # [1.0, 0.0, 0.0]
Colors.GREEN    # [0.0, 1.0, 0.0]
Colors.BLUE     # [0.0, 0.0, 1.0]
Colors.YELLOW   # [1.0, 1.0, 0.0]
Colors.CYAN     # [0.0, 1.0, 1.0]
Colors.MAGENTA  # [1.0, 0.0, 1.0]
Colors.WHITE    # [1.0, 1.0, 1.0]
Colors.BLACK    # [0.0, 0.0, 0.0]
Colors.ORANGE   # [1.0, 0.5, 0.0]
Colors.PURPLE   # [0.5, 0.5, 0.5]
Colors.GRAY     # [0.5, 0.5, 0.5]
Colors.BROWN    # [0.6, 0.3, 0.1]
Colors.PINK     # [1.0, 0.75, 0.8]
```

## 核心控制功能

```python
viewer.run()          # Start main loop (blocking)
viewer.close()         # Close viewer
viewer.join()         # Wait for process to end
viewer.reset()         # Reset viewer state
viewer.init()          # Initialize view (set initial camera)
viewer.show(0.03)      # Render frame with delay (s)
viewer.should_not_quit()  # Check if viewer should continue
viewer.clear_all_visual_elements()  # Clear all elements
```

## 点云（Point Cloud）

```python
# Clear all points
viewer.clear_all_points()

# Add single-color points (default: red)
viewer.add_points(points, point_size=4.0)

# Add points with custom colors
viewer.add_points_with_colors(points, colors, point_size=4.0)

# Add points with named color
viewer.add_points_with_color_name(points, color_name="red", point_size=4.0)

# Data format: points (N, 3), colors (N, 3)
```

## 轨迹（Trajectory）

```python
# Clear all trajectories
viewer.clear_all_trajectories()

# Add trajectory with quaternions (positions + orientations)
viewer.add_trajectory_quat(
    positions,           # (N, 3)
    orientations,        # (N, 4) or (N, 7) depending on quat_format
    color=Colors.GREEN,
    quat_format="wxyz",   # "wxyz" or "xyzw"
    line_width=2.0,
    show_cameras=True,    # Show camera models along trajectory
    camera_size=0.05
)

# Add trajectory with SE3 poses
viewer.add_trajectory_se3(
    poses_se3,           # (N, 4) or (N, 7)
    color=Colors.GREEN,
    line_width=2.0,
    show_cameras=False
)
```

## 相机（Camera）

```python
# Clear all cameras
viewer.clear_all_cameras()

# Set main camera (view follows this camera)
viewer.set_main_camera(camera_id)

# Add camera with quaternion
cam_id = viewer.add_camera_quat(
    position,           # (3,)
    orientation,         # (4,) or (7) depending on quat_format
    color=Colors.YELLOW,
    quat_format="wxyz",
    scale=0.1,
    line_width=1.0
)

# Add camera with SE3 pose
cam_id = viewer.add_camera_se3(
    pose_se3,            # (4,) or (7)
    color=Colors.YELLOW,
    scale=0.1,
    line_width=1.0
)
```

## 平面（Plane）

```python
# Clear all planes
viewer.clear_all_planes()

# Add plane by vertices
viewer.add_plane(
    vertices,        # (>=3, 3)
    color=Colors.GRAY,
    alpha=0.5,       # Transparency 0-1
    label="plane"
)

# Add plane by normal + center
viewer.add_plane_normal_center(
    normal,          # (3,) - direction of plane normal
    center,          # (3,) - center point
    size,            # half-size (distance from center to edge)
    color=Colors.GRAY,
    alpha=0.5,
    label="plane"
)

# Add plane from SE3 transformation
viewer.add_plane_from_Twp(
    Twp,             # (4, 4) - world pose matrix
    size=1.0,
    color=Colors.GREEN,
    alpha=0.5,
    label="plane"
)
```

## 棋盘（Chessboard）

这些功能适用于相机校准和空间参考：

```python
# Add chessboard on XY plane
viewer.add_chessboard(rows=8, cols=8, cell_size=0.1)

# Add chessboard on custom plane with normal
viewer.add_chessboard(
    rows=9, cols=6, cell_size=0.025,
    origin=np.array([0, 0, 0]),
    normal=np.array([1, 0, 0]),  # YZ plane
    color1=Colors.RED,
    color2=Colors.YELLOW,
    alpha=0.8
)

# Add chessboard from SE3 transformation
viewer.add_chessboard_from_Twp(
    rows=9, cols=6, cell_size=0.025,
    Twp=pose_matrix,
    color1=Colors.BLACK,
    color2=Colors.WHITE,
    alpha=0.8,
    label="calib"
)
```

## 直线（Line）

```python
viewer.clear_all_lines()

viewer.add_line(
    start_point,      # (3,)
    end_point,        # (3,)
    color=Colors.WHITE,
    line_width=1.0
)
```

## 图像显示（Image Display）

```python
# Set image resolution
viewer.set_img_resolution(width, height)

# Add left image
viewer.add_image_1(img_array)           # Use numpy array
viewer.add_image_1(image_path="path.jpg")  # Use file path

# Add right image
viewer.add_image_2(img_array)
viewer.add_image_2(image_path="path.jpg")
```

## 步进模式（调试用，Step Mode, for debugging）

```python
viewer.is_step_mode_active()   # Check if step mode is active
viewer.wait_for_step()         # Wait for step trigger
```

## 重要说明：

- **依赖项**：需要安装 Pangolin 库（通过 `gettool` 自动下载）。
- **数据类型**：所有位置/点的输入值必须为 `float32` 类型。
- **四元数格式**：支持 `wxyz` 和 `xyzw` 格式。
- **SE3 姿势（SE3 Poses）**：支持 (4, 4) 或 (4, 7) 矩阵格式。
- **自动清理功能**：`clear_all_visual_elements()` 可清除所有显示的点、轨迹、相机和平面。
- **相机跟随功能**：使用 `set_main_camera()`，并传入通过 `add_camera_*()` 返回的相机 ID。
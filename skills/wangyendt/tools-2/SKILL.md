---
name: pywayne-vio-tools
description: VIO（视觉惯性测距）数据处理工具，用于SE(3)姿态转换和3D可视化。适用于处理SE(3)矩阵时需要进行姿态表示转换（tx, ty, tz, qw, qx, qy, qz），以及需要带有方向箭头的姿态轨迹3D可视化，或者进行视觉惯性测距数据的转换与分析的场景。
---
# Pywayne VIO 工具

## 概述

提供用于 VIO 数据处理的实用工具：在 SE(3) 变换矩阵和姿态表示之间进行转换，并以 3D 形式可视化姿态轨迹，同时显示方向指示器。

## 快速入门

```python
from pywayne.vio.tools import SE3_to_pose, pose_to_SE3, visualize_pose
import numpy as np

# Convert SE(3) to pose
SE3 = np.eye(4)  # Single 4x4 SE(3) matrix
pose = SE3_to_pose(SE3)  # Returns [tx, ty, tz, qw, qx, qy, qz]

# Batch conversion
SE3_array = np.random.randn(10, 4, 4)  # 10 SE(3) matrices
poses = SE3_to_pose(SE3_array)

# Convert back to SE(3)
SE3_recon = pose_to_SE3(pose)

# Visualize poses
visualize_pose(poses)  # 3D plot with position markers and orientation arrows
```

## 核心功能

### SE3_to_pose

将 SE(3) 变换矩阵转换为姿态表示。

**输入：** `SE3_mat` - 单个 4x4 的 SE(3) 矩阵，或形状为 (N, 4, 4) 的 N 个 SE(3) 矩阵数组

**输出：** `pose` - 形状为 (7,) 或 (N, 7) 的数组，包含 [tx, ty, tz, qw, qx, qy, qz]

**依赖库：** `qmt.quatFromRotMat()`（用于提取四元数）

### pose_to_SE3

将姿态表示转换回 SE(3) 变换矩阵。

**输入：** `pose_mat` - 单个姿态表示（形状为 (7,)），或形状为 (N, 7) 的 N 个姿态表示（每个表示包含 [tx, ty, tz, qw, qx, qy, qz]）

**输出：** `SE3_mat` - 形状为 (4, 4) 或 (N, 4, 4) 的 SE(3) 矩阵数组

**依赖库：** `qmt.quatToRotMat()`, `ahrs.Quaternion`

### visualize_pose

以 3D 形式可视化 SE(3) 姿态，同时显示位置标记和方向箭头。

**参数：**
- `poses`：姿态数组 [tx, ty, tz, qw, qx, qy, qz]
- `arrow_length_ratio`：方向箭头的比例因子（默认值：0.1）

**可视化效果：**
- 黑点：位置（平移）
- 红色箭头：X 轴方向
- 绿色箭头：Y 轴方向
- 蓝色箭头：Z 轴方向

**依赖库：** `matplotlib.pyplot`, `qmt.quatToRotMat()`

## 数据格式

### SE(3) 矩阵
```
[[R00 R01 R02 tx]
 [R10 R11 R12 ty]
 [R20 R21 R22 tz]
 [  0   0   0  1]]
```

### 姿态表示
```
[tx, ty, tz, qw, qx, qy, qz]
```
- 平移：tx, ty, tz（米）
- 四元数：qw, qx, qy, qz（汉密尔顿约定）

## 所需依赖库：
- `numpy` - 数组操作库
- `qmt` - 四元数处理库
- `ahrs` - 四元数类
- `matplotlib` - 3D 可视化库

安装方法：
```bash
pip install numpy qmt ahrs matplotlib
```
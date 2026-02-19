---
name: pywayne-vio-se3
description: SE(3)刚体变换库，用于3D旋转和平移操作。适用于处理机器人姿态、相机变换、SLAM系统或任何3D刚体运动相关任务。支持SE(3)矩阵运算、李群/代数映射（log/Log、exp/Exp）、表示形式转换（四元数、轴角、欧拉角），以及轨迹的批量处理。
---
# SE3刚体变换

## 快速入门

```python
import numpy as np
from pywayne.vio.SE3 import *

# Create SE(3) transformation from rotation and translation
R = np.eye(3)
t = np.array([1, 2, 3])
T = SE3_from_Rt(R, t)

# Lie algebra operations
xi = np.array([0.1, 0.2, 0.3, 0.05, 0.1, 0.15])  # [rho, theta]
T_from_xi = SE3_Exp(xi)  # se(3) vector -> SE(3)
xi_recovered = SE3_Log(T_from_xi)  # SE(3) -> se(3) vector
```

## 核心操作

### 基本矩阵运算

**创建/验证SE(3)矩阵：**
- `check_SE3(T)` - 验证4x4矩阵是否为有效的SE(3)矩阵
- `SE3_from_Rt(R, t)` - 根据旋转矩阵和平移向量构造SE(3)矩阵
- `SE3_to_Rt(T)` - 从SE(3)矩阵中提取旋转矩阵和平移向量

**组合/反转变换：**
- `SE3_mul(T1, T2)` - 矩阵乘法（组合多个变换）
- `SE3_inv(T)` - 矩阵求逆
- `SE3_diff(T1, T2, from_1_to_2=True)` - 计算两个变换之间的相对位移

### 李群/李代数映射

**向量形式（推荐使用）：**
- `SE3_Exp(xi)` - 将6D向量转换为SE(3)矩阵（其中xi = [rho, theta]）
- `SE3_Log(T)` - 将SE(3)矩阵转换为6D向量

**矩阵形式（理论用法）：**
- `SE3_exp(xi_hat)` - 将4x4矩阵转换为SE(3)矩阵
- `SE3_log(T)` - 将SE(3)矩阵转换为4x4矩阵
- `SE3_skew(xi)` - 将6D向量转换为4x4李代数矩阵
- `SE3_unskew(xi_hat)` - 将4x4矩阵转换为6D向量

**命名规则：** 大写表示向量，小写表示矩阵

### 表示形式转换

**四元数 + 平移：**
- `SE3_from_quat_trans(q, t)` - 输入为wxyz形式的四元数
- `SE3_to_quat_trans(T)` - 返回四元数和平移向量

**轴角 + 平移：**
- `SE3_from_axis_angle_trans(axis, angle, t)` - 输入为轴、角度和平移向量
- `SE3_to_axis_angle_trans(T)` - 返回轴、角度和平移向量

**欧拉角 + 平移：**
- `SE3_from_euler_trans(euler_angles, t, axes='zyx', intrinsic=True)` - 输入为欧拉角
- `SE3_to_euler_trans(T, axes='zyx', intrinsic=True)` - 返回欧拉角和平移向量

### 统计运算**

- `SE3_mean(T_batch)` - 计算多个SE(3)矩阵的平均值（输入格式为Nx4x4，输出为4x4矩阵）

## 输入/输出格式

**单个变换：**
- 输入：4x4矩阵或3x3/3x3数组
- 输出：4x4矩阵或标量向量

**批量运算：**
- 输入：Nx4x4或Nx3x3/Nx3数组
- 输出：与输入相同的批量格式
- 所有函数都支持单个输入和批量输入

**6D向量格式：`[rho_1, rho_2, rho_3, theta_1, theta_2, theta_3]`
- 前三个元素表示平移（线性速度）
- 后三个元素表示旋转（角速度）

## 常见应用模式

### 轨迹处理

```python
# Batch process robot trajectory
poses = np.array([...])  # Nx4x4
log_poses = SE3_Log(poses)  # Nx6 Lie algebra space
mean_pose = SE3_Exp(np.mean(log_poses, axis=0))  # Intrinsic mean
```

### 相对运动

```python
# Relative transform between two poses
T_rel = SE3_diff(T_world_keyframe1, T_world_keyframe2)
# T_rel transforms points from frame2 to frame1
```

### 相机姿态估计

```python
# Camera to world transformation
R_cam = np.column_stack([right, up, forward])  # Camera axes
t_cam = camera_position
T_cam2world = SE3_from_Rt(R_cam, t_cam)
T_world2cam = SE3_inv(T_cam2world)
```

## 注意事项：

- 所有角度均以弧度为单位
- 矩阵乘法遵循右乘规则：`P' = T @ P`
- 对于大角度和大的位移，该算法具有数值稳定性
- 批量运算使用向量化NumPy库以提高效率
- 性能参考（处理1000个变换）：`SE3_exp`操作耗时约2.5毫秒，`SE3_Log`操作耗时约0.8毫秒
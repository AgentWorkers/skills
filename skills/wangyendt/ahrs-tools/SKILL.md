---
name: pywayne-ahrs-tools
description: AHRS（Attitude and Heading Reference System，姿态与航向参考系统）的四元数分解工具以及滚转/俯仰补偿功能。这些工具适用于使用 `pywayne.ahrs.tools` 模块进行四元数到欧拉角的转换，或通过滚转-俯仰补偿方法将设备的姿态调整至零俯仰和零滚转状态。
---
# Pywayne AHRS 工具

该模块提供了基于四元数的 AHRS（姿态和航向参考系统）相关工具。

## 快速入门

```python
from pywayne.ahrs.tools import quaternion_decompose, quaternion_roll_pitch_compensate
import numpy as np

# Quaternion decomposition
q = np.array([0.70710678, 0, 0, 0.707962])  # w, x, y, z
angle_all, angle_heading, angle_inclination = quaternion_decompose(q)

# Roll/pitch compensation
q_comp = quaternion_roll_pitch_compensate(q)
```

## 四元数分解

```python
from pywayne.ahrs.tools import quaternion_decompose
import numpy as np

# Input quaternion (w, x, y, z)
q = np.array([w, x, y, z])

# Decompose into angles
angle_all, angle_heading, angle_inclination = quaternion_decompose(q)

# angle_all: Rotation angles around all axes (vertical + horizontal)
# angle_heading: Angle around vertical axis (inclination)
# angle_inclination: Angle around horizontal axis (bank)
```

## 滚转/俯仰补偿

```python
from pywayne.ahrs.tools import quaternion_roll_pitch_compensate
import numpy as np

# Input quaternion (w, x, y, z)
q = np.array([0.989893, -0.099295, 0.024504, -0.098242])

# Compensate pitch and roll to zero
q_comp = quaternion_roll_pitch_compensate(q)
```

## 所需依赖库

- `numpy`：用于数组操作
- `qmt`：OpenCV 提供的四元数转换模块

## 注意事项

- 四元数分解会同时返回两个角度（以弧度为单位）以及航向/倾角
- `angle_all` 的计算公式为 `2 * arccos(abs(quaternion_z))`
- `angle_heading` 的计算公式为 `arctan2(np.abs(quaternion_xy))`
- `angle_inclination` 的计算公式为 `2 * arcsin(np.abs(quaternion_xy))`
- 滚转/俯仰补偿功能通过使用逆旋转操作将 `q_comp` 的俯仰和滚动角度设置为零
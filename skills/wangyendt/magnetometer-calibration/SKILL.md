---
name: pywayne-calibration-magnetometer-calibration
description: 传感器校准工具包，包含使用近似公式（close-form method）进行磁力计校准的功能。适用于校准惯性测量单元（IMU）传感器（加速度计、陀螺仪、磁力计），以计算用于磁力计校正的软铁矩阵（soft-iron matrix）和硬铁偏移量（hard-iron offset）。在校准过程中需要结合视觉质量滤波（VQF）技术进行传感器数据融合，以实现方向估计。
---
# Pywayne 校准

`pywayne.calibration.MagnetometerCalibrator` 提供了使用传感器数据（加速度计、陀螺仪、磁力计）进行磁力计校准的功能。

## 快速入门

```python
from pywayne.calibration import MagnetometerCalibrator
import numpy as np

# Sensor data: ts (N,), acc (N,3), gyro (N,3), mag (N,3)
calibrator = MagnetometerCalibrator(method='close_form')
Sm, h = calibrator.process(ts, acc, gyro, mag)

# Sm: Soft-iron matrix (3x3)
# h: Hard-iron offset vector (3,)
```

## 输入数据格式

传感器数据必须是具有相同采样数量的 NumPy 数组：

```python
ts   # (N,)     - Timestamps (seconds)
acc  # (N, 3)   - Accelerometer [ax, ay, az]
gyro # (N, 3)   - Gyroscope [gx, gy, gz]
mag  # (N, 3)   - Magnetometer [mx, my, mz]
```

**数据要求：**
- 传感器数据应涵盖各种方向，以确保校准效果的有效性
- 所需的最小数据点数量（具体数量取决于校准的稳定性）
- 数组必须是连续存储的（系统会自动进行内部转换）

## 校准参数

`process()` 函数返回以下参数：

| 参数        | 形状       | 描述                                      |
|------------|-----------|-----------------------------------------|
| `Sm`        | (3, 3)     | 软铁矩阵                                      |
| `h`        | (3,)      | 硬铁偏移向量                                    |

## 在应用程序中的使用

将校准结果应用于原始磁力计读数：

```python
# Calibrated reading
m_calibrated = Sm @ (m_raw - h)
```

## 时间校准

虽然时间校准模块已经实现，但暂时仅用于未来的扩展计划，目前尚未提供任何功能。

## 重要说明

- **依赖库**：需要 `vqf`（VQF 四元数滤波器）和 `qmt`（四元数数学运算）模块
- **校准方法**：目前仅支持 `close_form` 方法
- **方向处理**：在校准过程中使用 VQF 进行传感器数据融合和方向估计
- **输出结果**：校准过程中会打印出所有校准参数
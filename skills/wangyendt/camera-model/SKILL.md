---
name: pywayne-cv-camera-model
description: 这是一个用于 `camera_models` C++ 库的相机模型封装层，通过 `pybind11` 实现。当使用 `pywayne.cv.camera_model` 模块从 YAML 配置文件中加载相机模型、访问相机属性（如模型类型、图像尺寸、参数等）、执行投影操作（如 `lift_projective`、`space_to_plane`），以及将相机参数导出为字典时，可以方便地使用该封装层。
---
# Pywayne相机模型

该模块通过pybind11封装了`camera_models` C++库，为相机操作提供了Python接口。

## 快速入门

```python
from pywayne.cv.camera_model import CameraModel
from pywayne.cv.tools import write_cv_yaml
import numpy as np

# Create camera model
camera = CameraModel()

# Load from YAML file
camera.load_from_yaml('camera_config.yaml')

# Access properties
print(f"Model: {camera.model_type}")
print(f"Size: {camera.image_width}x{camera.image_height}")
```

## 从YAML文件加载相机模型

```python
from pathlib import Path

# Sample YAML configuration
yaml_data = {
    "model_type": "PINHOLE",
    "camera_name": "my_camera",
    "image_width": 1280,
    "image_height": 720,
    "distortion_parameters": {"k1": 0.0, "k2": 0.0},
    "projection_parameters": {"fx": 600.0, "fy": 600.0, "cx": 640.0, "cy": 360.0}
}

# Write YAML file
write_cv_yaml('camera_config.yaml', yaml_data)

# Load model
camera.load_from_yaml('camera_config.yaml')
```

## 支持的相机模型

| 模型类型 | 描述 |
|------------|-------------|
| `PINHOLE` | 具有径向畸变的标准针孔相机 |
| `PINHOLE_FULL` | 包含所有畸变参数的完整针孔模型 |
| `CATA` | 折射相机模型 |
| `EQUIDISTANT` | 等距相机模型 |
| `OCAM` | 统一相机模型 |

## 投影操作

### lift_projective()

将一个2D图像点转换为3D投影射线：

```python
# Input can be tuple, list, or numpy array
ray_3d = camera.lift_projective([u, v])  # Returns np.ndarray (x, y, z)
```

### space_to_plane()

将一个3D点投影到2D图像平面上：

```python
# Input can be tuple, list, or numpy array
uv = camera.space_to_plane([x, y, z])  # Returns np.ndarray (u, v)
```

## 属性

| 属性 | 描述 |
|---------|-------------|
| `model_type` | 相机模型类型（枚举） |
| `camera_name` | 加载的相机名称 |
| `image_width` | 图像宽度（以像素为单位） |
| `image_height` | 图像高度（以像素为单位） |

## 参数字典

将所有相机参数导出为字典：

```python
params = camera.get_parameters_as_dict()
print(params)
```

包含模型特定的参数：
- **Pinhole**: `k1`, `k2`, `p1`, `p2`, `fx`, `fy`, `cx`, `cy`
- **Pinhole Full**: `k1-k6`, `p1-p2`, `fx`, `fy`, `cx`, `cy`
- **CATA**: `xi`, `k1-k2`, `p1-p2`, `gamma1-2`, `u0`, `v0`
- **Equidistant**: `k2-k5`, `mu`, `mv`, `u0`, `v0`
- **OCAM**: `C`, `D`, `E`, `center_x`, `center_y`, `poly`, `inv_poly`

## 所需依赖库

- `camera_models` - C++库（如果缺失，将通过`gettool`自动下载）
- `numpy` - 用于数组操作
- `pywayne.cv.tools.write_cv_yaml` - 用于写入YAML文件

## 注意事项

- 如果未找到相关库，系统会自动通过`gettool`进行检测和下载
- 投影方法支持元组/列表以及numpy数组作为输入参数
- 投影方法的输出结果始终为`np.ndarray`类型，数据类型为`np.float64`
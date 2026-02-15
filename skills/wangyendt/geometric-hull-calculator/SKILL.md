---
name: pywayne-cv-geometric-hull-calculator
description: 这是一个用于计算二维点集的几何外壳（Geometric Hull）的工具。它支持计算凸包（Convex Hull）、凹包（Concave Hull，也称为Alphashape）以及最小外接矩形（Minimum Bounding Rectangle）。在使用 `pywayne.cv.geometric_hull_calculator` 模块时，可以利用该工具来计算几何外壳，通过 OpenCV 或 matplotlib 对结果进行可视化处理，并生成随机测试点集。
---
# Pywayne 几何外壳计算器

该模块用于计算二维点集的几何外壳（凸包和凹包）。

## 快速入门

```python
from pywayne.cv.geometric_hull_calculator import GeometricHullCalculator
import numpy as np

# Create calculator with random points
points = GeometricHullCalculator.generate_random_points(num_points=50)
calculator = GeometricHullCalculator(points, algorithm='concave-hull')

# Get results
print(f"MBR: {calculator.get_mbr()}")
print(f"Convex Hull: {calculator.get_convex_hull()}")
print(f"Concave Hull: {calculator.get_concave_hull()}")

# Visualize with matplotlib
calculator.visualize_matplotlib()
```

## 初始化

```python
# algorithm options: 'concave-hull' or 'alphashape'
# use_filtered_pts: Enable point filtering based on radius
calculator = GeometricHullCalculator(
    points=your_points,
    algorithm='alphashape',
    use_filtered_pts=True
)
```

## 支持的算法

| 算法 | 描述 |
|---------|-------------|
| `concave-hull` | 使用 `concave_hull` 库计算凹包 |
| `alphashape` | 使用 `alphashape` 库计算凹包 |

## 外壳类型

| 类型 | 方法 | 描述 |
|------|---------|-------------|
| 凸包 | `get_convex_hull()` | 包含所有点的外层外壳 |
| 凹包 | `get_concave_hull()` | 内部凹边界 |

## 属性

| 属性 | 描述 |
|---------|-------------|
| `points` | 输入的二维点集（N×2 的 numpy 数组） |
| `algorithm` | 用于计算凹包的算法 |
| `useFiltered_pts` | 是否使用了过滤后的点 |
| `box` | 最小外接矩形的四个角 |
| `center` | 输入点的中心点 |
| `filter_radius` | 用于点过滤的半径 |
| `concave_hull_result` | 凹包的点或多边形 |

## 可视化

### OpenCV 可视化

```python
calculator.visualize_opencv()
```

显示内容：所有输入点、最小外接矩形（MBR）、中心点、过滤圆（如果启用）、凹包（绿色）、凸包（红色）。

### Matplotlib 可视化

```python
calculator.visualize_matplotlib()
```

显示内容：所有输入点（红色）、最小外接矩形（蓝色）、中心点、过滤半径圆（如果启用）、凹包（橙色）、凸包（紫色）。

## 所需依赖库

- `numpy` - 用于数组操作 |
- `cv2`（OpenCV） - 用于 OpenCV 可视化和最小外接矩形的计算 |
- `matplotlib` - 用于 matplotlib 可视化 |
- `scipy` - 用于凸包的计算 |
- `concave_hull` - 用于计算凹包的库 |
- `alphashape` - 用于计算凹包的库 |
- `shapely` - 用于多边形操作和面积计算的库 |

## 注意事项

- 点过滤使用的是最小外接矩形边长 30% 的半径 |
- 最小外接矩形使用 OpenCV 的 `minAreaRect` 函数计算 |
- 凸包使用 scipy 的 `ConvexHull` 函数计算 |
- 支持 `alphashape` 返回的单个多边形和多个多边形结果
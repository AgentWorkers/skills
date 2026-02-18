---
name: pywayne-cv-apriltag-detector
description: **AprilTag角点检测功能**：用于相机标定和姿态估计。在使用 `pywayne.cv.apriltag_detector` 模块时，该功能可帮助检测图像中的 AprilTag 标志点。该模块支持通过 `gettool` 自动安装相关库，能够绘制包含角点位置及标识符的检测结果，并兼容文件路径及 NumPy 数组两种数据输入格式。
---
# Pywayne AprilTag 检测器

该模块用于检测用于相机校准和姿态估计的 AprilTag 标志。

## 快速入门

```python
from pywayne.cv.apriltag_detector import ApriltagCornerDetector

# Create detector
detector = ApriltagCornerDetector()

# Detect from file path
detections = detector.detect('test.png', show_result=True)

# Detect from numpy array
import cv2
image = cv2.imread('test.png')
detections = detector.detect(image)
```

## 检测方法

### `detect()`

在图像中检测 AprilTag 标志：

```python
detections = detector.detect(
    image,           # File path, Path object, or numpy array
    show_result=False  # Show visualization window
)
```

返回检测结果列表，包含以下信息：
- `id`：标签 ID
- `hamming_distance`：检测置信度（值越低，置信度越高）
- `center`：标签中心坐标（x, y）
- `corners`：4 个角点的坐标

### `detect_and_draw()`

检测 AprilTag 标志，并在原始图像上绘制结果：

```python
result_image = detector.detect_and_draw(image)
cv2.imshow('Detection Result', result_image)
cv2.waitKey(0)
```

可视化效果包括：
- 绿色多边形轮廓
- 红色角点圆圈
- 标签中心处的红色 ID 标签

## 所需库

- `cv2`（OpenCV）：图像处理库
- `numpy`：数组操作库
- `gettool`：用于自动下载 `apriltag_detection` 库

## 库的安装

如果系统未安装 `apriltag_detection` 库，该检测器会使用 `gettool` 自动进行安装。

## 检测结果格式

每个检测结果包含以下字段：
| 字段 | 描述 |
|--------|-------------|
| `id` | 标签标识符 |
| `hamming_distance` | 哈明距离（值越低，置信度越高） |
| `center` | 标签中心坐标（x, y） |
| `corners` | 4 个角点的坐标（格式为 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] |

## 注意事项

- 支持灰度和 BGR 格式的图像
- 检测前会自动将图像转换为灰度格式
- 可视化效果的大小会随图像尺寸自动调整
- 该检测器使用 AprilTag 36h11 标签格式
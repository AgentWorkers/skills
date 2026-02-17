---
name: pywayne-cv-tools
description: OpenCV YAML 文件读写工具。在使用 `pywayne.cv.tools` 模块时，这些工具可用于读取 OpenCV FileStorage 的 YAML 文件。支持嵌套结构、NumPy 数组、基本数据类型以及列表。能够处理 `cv2.FileNode` 的解析，包括 `Map`、`Seq` 和 `matrix` 节点。
---
# Pywayne CV YAML I/O

该模块提供了用于读写 OpenCV `cv2.FileStorage` YAML 文件的实用工具。

## 快速入门

```python
from pywayne.cv.tools import read_cv_yaml, write_cv_yaml
import numpy as np

# Write to YAML file
data = {
    "camera_name": "test_camera",
    "image_width": 1920,
    "image_height": 1080,
    "calibration_matrix": np.eye(3)
}
write_cv_yaml('config.yaml', data)

# Read from YAML file
data = read_cv_yaml('config.yaml')
print(data)
```

## 支持的数据类型

| 类型 | 处理方式 |
|------|---------|
| `int`、`float`、`str` | 直接写入文件 |
| `np.ndarray` | 使用 `fs.write()` 方法写入文件 |
| `list` | 使用 `FileNode_SEQ` 方法写入文件 |
| `dict` | 使用 `FileNode_MAP` 方法写入文件 |
| `None` | 被忽略 |

## 读取文件

```python
from pywayne.cv.tools import read_cv_yaml

# Read YAML file (returns dict or None on error)
data = read_cv_yaml('camera_config.yaml')
if data:
    print(data['camera_name'])
    print(data['image_width'])
```

**注意事项：**
- 递归处理嵌套结构 |
- 如果文件无法打开，返回 `None` |
- 使用 `wayne_print` 显示错误信息（错误信息以红色/黄色显示） |
- 对于字典和列表，支持 `FileNode_MAP` 和 `FileNode_SEQ` 两种格式 |
- 矩阵节点通过 `.mat()` 方法进行读取

## 写入文件

```python
from pywayne.cv.tools import write_cv_yaml

# Write data to YAML file
data = {
    "matrix": np.eye(3),
    "vector": [1, 2, 3]
}
success = write_cv_yaml('config.yaml', data)

if success:
    print("Write successful")
```

**注意事项：**
- 成功时返回 `True`，失败时返回 `False` |
- 对于 OpenCV 中的列表，如果键为空，则使用空键进行处理 |
- 支持使用空键字符串表示未命名的序列 |
- 在写入过程中会忽略 `None` 值

## 所需依赖库

- `cv2`（OpenCV）：用于文件存储操作 |
- `numpy`：用于处理 numpy 数组 |
- `pywayne.tools`：用于日志记录（使用 `wayne_print`）

## API 参考

| 函数 | 描述 |
|---------|-------------|
| `read_cv_yaml(path)` | 读取 OpenCV YAML 文件，返回字典或 `None` |
| `write_cv_yaml(path, data)` | 将字典写入 OpenCV YAML 文件，返回布尔值 |

## 文件结构处理

该模块支持 OpenCV 的 `cv2.FileNode` 类型：

| 节点类型 | 处理方式 |
|-----------|---------|
| Map | 使用 `.keys()` 方法（需要可调用对象） |
| Seq | 通过元素迭代进行递归解析 |
| Matrix | 使用 `.mat()` 方法 |
| Int/Float/String | 使用 `.real()`、`.int()`、`.string()` 方法 |
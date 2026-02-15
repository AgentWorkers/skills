---
name: pywayne-aliyun-oss
description: 阿里云OSS（对象存储服务）的Python文件管理工具包。适用于与阿里云OSS交互时执行以下操作：上传文件、下载文件、列出对象、删除文件、管理目录、读取文件内容、检查文件是否存在、获取文件元数据以及复制和移动对象。该工具包支持两种访问方式：需要身份验证的访问（通过API密钥/密钥对进行写入操作）和匿名访问（仅支持读取操作）。
---
# Pywayne Aliyun OSS

`pywayne.aliyun_oss.OssManager` 提供了一套全面的工具，用于管理阿里云 OSS（对象存储服务）的 bucket。

## 快速入门

```python
from pywayne.aliyun_oss import OssManager

# Initialize with write permissions
oss = OssManager(
    endpoint="https://oss-cn-xxx.aliyuncs.com",
    bucket_name="my-bucket",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# Initialize with read-only (anonymous) access
oss = OssManager(
    endpoint="https://oss-cn-xxx.aliyuncs.com",
    bucket_name="my-bucket",
    verbose=False  # Disable verbose output
)
```

## 上传操作

### 上传本地文件

```python
oss.upload_file(key="data/sample.txt", file_path="./sample.txt")
```

### 上传文本内容

```python
oss.upload_text(key="config/settings.json", text='{"key": "value"}')
```

### 上传图片（numpy 数组）

```python
import cv2
image = cv2.imread("photo.jpg")
oss.upload_image(key="photos/photo.jpg", image=image)
```

### 上传整个目录

```python
oss.upload_directory(local_path="./local_folder", prefix="remote_folder/")
```

## 下载操作

### 下载单个文件

```python
# Preserve directory structure: downloads/data/sample.txt
oss.download_file(key="data/sample.txt", root_dir="./downloads")

# Use only basename: downloads/sample.txt
oss.download_file(key="data/sample.txt", root_dir="./downloads", use_basename=True)
```

### 下载带有前缀的文件

```python
oss.download_files_with_prefix(prefix="photos/", root_dir="./downloads")
```

### 下载整个目录

```python
oss.download_directory(prefix="photos/", local_path="./downloads")
```

## 列表操作

### 列出 bucket 中的所有键

```python
keys = oss.list_all_keys()  # Returns sorted list
```

### 列出带有前缀的键

```python
keys = oss.list_keys_with_prefix(prefix="data/")
```

### 列出目录内容（仅第一层）

```python
contents = oss.list_directory_contents(prefix="data/")
# Returns: [("file1.txt", False), ("subdir", True), ...]
```

## 读取操作

### 将文件内容作为字符串读取

```python
content = oss.read_file_content(key="config/settings.json")
```

### 检查文件是否存在

```python
if oss.key_exists("data/sample.txt"):
    print("File exists")
```

### 获取文件元数据

```python
metadata = oss.get_file_metadata("data/sample.txt")
# Returns: {'content_length': 1234, 'last_modified': ..., 'etag': ..., 'content_type': ...}
```

## 删除操作

### 删除单个文件

```python
oss.delete_file(key="data/sample.txt")
```

### 删除带有前缀的文件

```python
oss.delete_files_with_prefix(prefix="temp/")
```

## 复制和移动操作

### 在 bucket 内复制对象

```python
oss.copy_object(source_key="data/original.txt", target_key="backup/original.txt")
```

### 在 bucket 内移动对象

```python
oss.move_object(source_key="data/temp.txt", target_key="archive/temp.txt")
```

## 重要说明

- **写入权限**：上传、删除、复制和移动操作需要 `api_key` 和 `api_secret`
- **匿名访问**：仅进行读取操作时可以省略 `api_key` 和 `api_secret`
- **目录处理**：OSS 实际上没有传统的目录结构——使用前缀（以 `/` 结尾的键）来表示目录
- **自然排序**：`list_all_keys()` 和 `list_keys_with_prefix()` 默认会按照自然顺序进行排序
- **详细输出**：当 `verbose=True`（默认值）时，所有方法都会打印状态信息
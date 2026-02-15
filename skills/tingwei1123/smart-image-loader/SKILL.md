---
name: smart-image-loader
description: 这是一个智能的图像加载器，能够处理 URL 和本地文件。它会自动将 URL 下载到临时文件夹中，然后使用相应的读取工具来显示图像。当用户需要查看或展示图像时（无论是来自网络的 URL 还是工作区中的文件），都可以使用这个工具。
---

# 智能图片加载器

## 快速入门

当用户请求显示一张图片时，系统会执行以下步骤：

1. **检查输入是否为 URL 或本地路径**：
   - URL 以 `http://` 或 `https://` 开头。
   - 本地路径是指工作区内的文件路径。

2. **对于 URL**：
   - 使用 Python 脚本将图片下载到临时文件夹中。
   - 使用 `read` 工具显示图片。
   - 下载完成后删除临时文件。

3. **对于本地文件**：
   - 验证文件是否存在（可以是工作区内的相对路径或绝对路径）。
   - 直接使用 `read` 工具显示图片。

## 使用示例

**用户请求：** “显示这张图片：https://example.com/photo.jpg”

1. 运行命令：`python3 scripts/smart_image_loader.py https://example.com/photo.jpg`
2. 脚本将图片下载到临时文件夹 `/tmp/dir/photo.jpg`。
3. 使用 `read` 工具显示图片。
4. 删除临时文件。

**用户请求：** “显示文件：./images/logo.png”

1. 运行命令：`python3 scripts/smart_image_loader.py ./images/logo.png`
2. 脚本验证文件是否存在。
3. 使用 `read` 工具显示图片（文件路径为 `/home/node/clawd/images/logo.png`）。

## 脚本用法

```bash
python3 scripts/smart_image_loader.py <image_path_or_url>
```

### 参数

| 参数 | 说明 |
|---------|---------|
| `image_path_or_url` | 本地文件路径（相对或绝对路径）或 URL |

### 输出格式

脚本返回类似 JSON 的输出，包含以下内容：
- `Status`：成功（SUCCESS）或失败（FAILED）
- `Type`：图片类型（url 或 local）
- `File Path`：用于调用 `read` 工具的文件路径
- `Message`：状态描述
- `Cleanup Needed`：是否需要删除临时文件

### 示例

```bash
# URL example
python3 scripts/smart_image_loader.py https://example.com/image.jpg
# Output: Downloads to /tmp/xyz/image.jpg, use read tool on that path

# Local file example (relative)
python3 scripts/smart_image_loader.py ./photos/vacation.jpg
# Output: File found at /home/node/clawd/photos/vacation.jpg

# Local file example (absolute)
python3 scripts/smart_image_loader.py /home/node/clawd/downloads/graphic.png
# Output: File found at /home/node/clawd/downloads/graphic.png
```

## 工作流程决策树

```
User asks to display an image
         |
         v
    Is it a URL? (http:// or https://)
         |
    +----+---------------------------+
    |                                 |
   YES                               NO
    |                                 |
    v                                 v
Download to temp              Does file exist?
    |                                 |
    v                          +-----+-----+
Use read tool                 |           |
    |                        YES          NO
    v                              |
Cleanup temp file              v
                           Use read tool
                               |
                               v
                          Done (no cleanup)
```

## 清理指南

- **URL 下载**：显示图片后务必删除临时文件。
- **本地文件**：无需清理（文件保留在工作区内）。
- 可使用 `exec` 命令配合 `rm <file_path>` 来删除临时文件。

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

## 错误处理

| 错误情况 | 处理方式 |
|---------|---------|
| URL 下载失败 | 向用户报告错误 |
| 本地文件不存在 | 向用户报告错误 |
| 输入无效 | 显示使用说明 |
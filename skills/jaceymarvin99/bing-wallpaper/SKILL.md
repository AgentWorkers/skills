---
name: bing-wallpaper
description: >
  **使用场景：**  
  当用户需要获取每日更新的Bing壁纸时。
---
# Bing壁纸技能

该技能帮助AI代理从60s API获取每日Bing壁纸，该API提供最新的Bing首页背景图片。

## 何时使用此技能

当用户执行以下操作时，请使用此技能：
- 请求今天的Bing壁纸
- 请求一张美观的每日背景图片

## 使用方法

执行关联的`scripts/wallpaper.sh`脚本来获取Bing壁纸。

```bash
./scripts/wallpaper.sh [encoding]
```

### 选项

- `--encoding, -e <format>`：可选。指定输出响应的格式。有效选项包括`text`、`json`、`image`和`markdown`。

### 返回值

脚本会安全地调用60s Bing壁纸API，并将响应输出到`stdout`。根据`encoding`参数的不同，返回值可能是JSON字符串、纯文本、markdown格式或二进制图像数据。

### 使用示例

```bash
# Get Bing wallpaper using default API encoding
./scripts/wallpaper.sh

# Get Bing wallpaper in JSON format
./scripts/wallpaper.sh --encoding json

# Get Bing wallpaper in plain text format (simplified usage)
./scripts/wallpaper.sh text

# Get Bing wallpaper in markdown format
./scripts/wallpaper.sh -e markdown

# Get Bing wallpaper as an image
./scripts/wallpaper.sh image
```

## 响应格式

返回值会根据`encoding`参数的不同而有所差异：

1. **默认及推荐格式（`--encoding markdown`）**
   - **使用场景：** 默认情况下用于获取壁纸信息。
   - **原因：** 以易于阅读的markdown格式返回壁纸的简要描述及图片链接。

2. **仅返回链接（`--encoding text`）**
   - **使用场景：** 用户仅需要图片链接时。
   - **原因：** 仅返回原始图片链接，不包含其他信息。

3. **结构化数据（`--encoding json`）**
   - **使用场景：** 需要以结构化JSON格式获取壁纸描述和链接时。
   - **原因：** 便于通过编程方式解析响应并提取特定字段。

4. **直接返回图片文件（`--encoding image`）**
   - **使用场景：** 用户明确请求图片文件本身时。
---
name: remarkable
description: 通过 Cloud API (rmapi) 从 reMarkable 数字笔平板电脑中获取手写笔记、草图和绘图。利用 AI 图像生成技术对这些内容进行处理：优化图像质量、提取手写文字并将其保存到内存或日志中，或者将草图作为其他工作流程的输入数据。该功能适用于处理 reMarkable 平板电脑中的内容、同步手写笔记、处理草图，以及将平板上的绘图集成到项目中。
---

# reMarkable平板电脑集成（rmapi）

通过Cloud API从reMarkable平板电脑获取手写笔记、草图和绘图内容。对这些内容进行处理：利用AI图像生成技术优化图片质量，提取文本并保存到内存或日志文件中，或将其作为其他工作流程的输入数据。

## 典型使用场景

1. **日志记录**：用户在reMarkable上写下想法 → 通过rmapi获取内容 → 使用OCR技术识别文本 → 将结果添加到`memory/YYYY-MM-DD.md`文件或专门的日志文件中。
2. **草图优化**：用户绘制草图 → 通过rmapi获取内容 → 使用nano-banana-pro（AI图像编辑工具）进行优化 → 获取处理后的最终版本。
3. **头脑风暴/笔记记录**：用户记录想法、列表或图表 → 通过rmapi获取内容 → 提取关键信息 → 添加到项目文档或内存中。
4. **插图制作**：用户创作手绘插图 → 通过rmapi获取内容 → 可选地对图片进行美化处理 → 用于博客文章或社交媒体等。

## 处理流程

```
reMarkable tablet → Cloud sync → rmapi fetch → PDF/PNG
                                                  ↓
                                    ┌─────────────┴─────────────┐
                                    │                           │
                              Text content?               Visual/sketch?
                                    │                           │
                              OCR / interpret            nano-banana-pro
                                    │                     (AI enhance)
                                    │                           │
                              Add to memory/            Return refined
                              journal/project            image to user
```

## 设置

- **工具**：rmapi（ddvk分支）v0.0.32
- **二进制文件**：`~/bin/rmapi`
- **配置文件**：`~/.rmapi`（登录后生成的设备令牌）
- **同步文件夹**：`~/clawd/remarkable-sync/`

### 认证（一次性操作）

1. 用户访问https://my.remarkable.com/connect/desktop进行登录。
2. 登录后，系统会生成一个8位字符的令牌。
3. 运行`rmapi`并输入该令牌。
4. 令牌会保存在`~/.rmapi`文件中，后续运行将自动完成认证。

## 命令

```bash
# List files/folders
rmapi ls
rmapi ls --json

# Navigate
rmapi cd "folder name"

# Find by tag / starred / regex
rmapi find --tag="share-with-gandalf" /
rmapi find --starred /
rmapi find / ".*sketch.*"

# Download (PDF)
rmapi get "filename"

# Download with annotations rendered (best for sketches)
rmapi geta "filename"

# Bulk download folder
rmapi mget -o ~/clawd/remarkable-sync/ "/Shared with Gandalf"
```

## 工作流程共享方式

### 方案A：专用文件夹
用户在reMarkable上创建一个名为“Shared with Gandalf”的文件夹 → 将需要共享的文件移动到该文件夹中 → 代理程序通过`rmapi mget`命令获取这些文件。

### 方案B：基于标签的共享
用户在文件上添加`share-with-gandalf`标签 → 代理程序通过`rmapi find --tag`命令找到这些文件。

### 方案C：标记文件
用户对文件进行星标标记 → 代理程序通过`rmapi find --starred`命令获取这些文件。

## 数据获取脚本

```bash
# Fetch from shared folder
~/clawd/scripts/remarkable-fetch.sh

# Fetch starred items
~/clawd/scripts/remarkable-fetch.sh --starred

# Fetch by tag
~/clawd/scripts/remarkable-fetch.sh --tag="share-with-gandalf"
```

## 注意事项：
- 在文件可被访问之前，必须先完成平板电脑与云端的同步操作。
- `geta`命令可将注释内容转换为PDF格式（适用于手写内容）。
- 可使用`convert`（ImageMagick工具）将PDF格式转换为PNG格式，以便进行后续的图像处理。
- 对于文本提取，系统采用视觉识别技术而非传统的OCR技术来解析手写内容。
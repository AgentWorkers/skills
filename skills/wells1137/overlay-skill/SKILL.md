---
name: overlay-skill
description: 为视频添加专业的包装效果和动态图形，包括片头/片尾、字幕、过渡效果、水印以及视频底部的标识。支持多种样式和自定义选项。
version: 2.0.0
author: wells1137
tags: [video, editing, motion graphics, ffmpeg, moviepy]
---
# 覆盖效果（Overlay Effects）

该功能可以为视频添加各种专业的包装效果和动态图形，从而提升视频的整体质量。它支持使用 FFmpeg 和 MoviePy 作为后端引擎，并提供丰富的预设模板和灵活的定制参数。

## 核心功能

| 功能          | 描述                                      | 示例用法                |
|---------------|-----------------------------------------|----------------------|
| **开场/结尾动画**   | 为视频添加吸引人的开场动画或专业的结尾动画。            | 显示品牌标志动画、播放结束提示。         |
| **字幕/标题**     | 在视频中叠加静态或动态的文字信息。                | 显示对话字幕、章节标题、行动号召信息。       |
| **过渡效果**     | 创建平滑或动态的片段过渡效果。                | 在场景之间实现淡入淡出效果，或用滑动方式切换下一个镜头。 |
| **水印/边框**     | 添加版权信息或装饰性边框。                        | 在视频角落显示频道标志，或添加电影风格的黑色边框。    |
| **底部信息栏**     | 显示参与者姓名、地点等其他相关信息。                | 显示受访者姓名、职位以及拍摄地点。         |

## 工作流程

代理使用该功能时，需按照以下步骤操作：

1. **选择功能**：根据用户需求从五个核心功能中选择一个。
2. **选择样式/模板**：从 `templates/presets.json` 文件中选择一个预设样式（例如 `modern`、`cyberpunk`、`business`）。
3. **配置参数**：为相应的脚本提供必要的参数（例如文字内容、图片路径、颜色、位置等）。
4. **执行脚本**：运行 `/scripts` 目录下的相应 Python 脚本以生成所需效果。
5. **预览并交付**：生成最终视频后将其呈现给用户。

## 使用指南（针对代理开发者）

本部分详细介绍了每个脚本的命令行接口，帮助代理开发者了解如何执行该功能的各项操作。

### 1. 开场/结尾动画

**脚本**：`add_intro_outro.py`

```bash
python /home/ubuntu/skills/overlay-skill/scripts/add_intro_outro.py --input <video> --output <video> --type <intro|outro> --text "Your Text" --template <name>
```

### 2. 字幕/标题

**脚本**：`add_subtitles.py`

```bash
python /home/ubuntu/skills/overlay-skill/scripts/add_subtitles.py --input <video> --output <video> --text "Your Text" --start HH:MM:SS --end HH:MM:SS --style <name>
```

### 3. 过渡效果

**脚本**：`add_transition.py`

```bash
python /home/ubuntu/skills/overlay-skill/scripts/add_transition.py --input1 <video1> --input2 <video2> --output <video> --type <fade|slide|wipe>
```

### 4. 水印/边框

**脚本**：`add_watermark.py`

```bash
python /home/ubuntu/skills/overlay-skill/scripts/add_watermark.py --input <video> --output <video> --image <image> --position <pos> --border-color <color>
```

### 5. 底部信息栏

**脚本**：`add_lower_third.py`

```bash
python /home/ubuntu/skills/overlay-skill/scripts/add_lower_third.py --input <video> --output <video> --title "Title" --subtitle "Subtitle" --template <name>
```

## 资源

- `/scripts/`：包含所有功能的 Python 实现代码。
- `/templates/presets.json`：包含开场动画、字幕和底部信息栏的预设样式。
- `/references/ffmpeg_moviepy_cheatsheet.md`：包含 FFmpeg 和 MoviePy 的常用命令及技巧的参考手册。
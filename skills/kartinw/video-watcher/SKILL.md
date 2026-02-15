---
name: video-analyzer
description: 通过定期提取视频帧来分析视频内容。当您需要了解视频文件中的内容、审查视频片段、分析视频场景，或者在无法直接播放视频的情况下对其进行描述时，可以使用该方法。支持 MP4、MOV、AVI、MKV 等常见的视频格式。
---

# 视频分析工具

该工具通过使用 `ffmpeg` 每 1 秒提取视频文件中的一个帧，然后对这些帧进行分析以了解视频内容。

## 先决条件

系统上需要安装 `ffmpeg`。如果未安装，请先进行安装：

```bash
# Ubuntu/Debian
sudo apt-get install -y ffmpeg

# macOS
brew install ffmpeg
```

## 使用方法

### 从视频中提取帧

```bash
scripts/extract_frames.sh <video_path> [output_dir] [fps]
```

**参数：**
- `video_path`（必填）：视频文件的路径
- `output_dir`（可选）：提取后的帧文件的存储目录。默认情况下，文件会保存在当前目录下的 `frames_<video_name>` 文件夹中
- `fps`（可选）：每秒提取的帧数。默认值为 1（即每秒提取 1 帧）

**示例：**
```bash
scripts/extract_frames.sh /path/to/video.mp4
scripts/extract_frames.sh /path/to/video.mp4 ./my_frames
scripts/extract_frames.sh /path/to/video.mp4 ./my_frames 2  # 2 frames per second
```

**输出结果：**
- 生成编号为 `frame_001.jpg`、`frame_002.jpg` 等的帧图像文件
- 输出视频的元数据（时长、分辨率、帧数）

## 工作流程**
1. 在视频文件上运行 `extract_frames.sh` 脚本
2. 使用 `read` 工具查看提取出的帧图像
3. 为了进行更全面的分析，可以定期（例如每 5 帧）抽取一些帧进行观察
4. 描述每个帧中的内容，从而理解整个视频的内容

## 提示**
- 对于时长较短的视频（<1 分钟）：查看所有帧
- 对于时长适中的视频（1-5 分钟）：每隔 3-5 帧抽取一部分帧进行观察
- 对于时长较长的视频（>5 分钟）：每隔 10 帧抽取一部分帧，重点关注场景变化
- 注意观察的场景包括：场景切换、文字/标题、用户界面元素、动作以及人物等
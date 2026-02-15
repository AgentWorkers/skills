---
name: ffmpeg-cli
description: 使用 FFmpeg 进行全面的视频/音频处理。功能包括：  
(1) 视频转码和格式转换；  
(2) 剪裁和合并视频片段；  
(3) 音频提取和编辑；  
(4) 生成缩略图和 GIF 图像；  
(5) 分辨率调整和画质优化；  
(6) 添加字幕或水印；  
(7) 调整视频播放速度（慢动作/快动作）；  
(8) 色彩校正和滤镜应用。
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["ffmpeg"]},"install":[{"id":"brew","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (brew)"}]}}
---

# FFmpeg 命令行工具（FFmpeg CLI）

## 快速参考

| 功能 | 命令                |
|------|----------------------|
| 剪裁视频 | `{baseDir}/scripts/cut.sh -i <输入文件> -s <开始时间> -e <结束时间> -o <输出文件>` |
| 合并视频片段 | `{baseDir}/scripts/merge.sh -o <输出文件> <文件1> <文件2> ...` |
| 提取音频 | `{baseDir}/scripts/extract-audio.sh -i <视频文件> -o <输出音频文件.mp3>` |
| 生成缩略图 | `{baseDir}/scripts/thumb.sh -i <视频文件> -t <时间戳> -o <输出图片文件>` |
| 创建 GIF 文件 | `{baseDir}/scripts/gif.sh -i <视频文件> -s <开始时间> -e <结束时间> -o <输出 GIF 文件>` |
| 转换视频格式 | `{baseDir}/scripts/convert.sh -i <输入文件> -o <输出视频文件.mp4>` |
| 调整播放速度 | `{baseDir}/scripts/speed.sh -i <输入文件> -r <0.5-2.0> -o <输出文件>` |
| 添加水印 | `{baseDir}/scripts/watermark.sh -i <视频文件> -w <图片文件> -o <输出视频文件>` |

## 脚本说明

### cut.sh - 剪裁视频片段
```bash
{baseDir}/scripts/cut.sh -i video.mp4 -s 00:01:30 -e 00:02:45 -o clip.mp4
```

### merge.sh - 合并视频片段
```bash
{baseDir}/scripts/merge.sh -o merged.mp4 part1.mp4 part2.mp4 part3.mp4
```

### extract-audio.sh - 提取音频轨道
```bash
{baseDir}/scripts/extract-audio.sh -i video.mp4 -o audio.mp3
```

### thumb.sh - 从视频中提取帧并生成图片
```bash
{baseDir}/scripts/thumb.sh -i video.mp4 -t 00:00:15 -o frame.jpg
```

### gif.sh - 将视频片段转换为 GIF 格式
```bash
{baseDir}/scripts/gif.sh -i video.mp4 -s 00:00:10 -e 00:00:15 -o clip.gif
```

### convert.sh - 将视频转换为新的格式
```bash
{baseDir}/scripts/convert.sh -i input.avi -o output.mp4
```

### speed.sh - 调整视频的播放速度
```bash
{baseDir}/scripts/speed.sh -i video.mp4 -r 2.0 -o fast.mp4  # 2x speed
{baseDir}/scripts/speed.sh -i video.mp4 -r 0.5 -o slow.mp4  # 0.5x speed
```

### watermark.sh - 在视频上添加水印
```bash
{baseDir}/scripts/watermark.sh -i video.mp4 -w logo.png -o output.mp4
```

## 注意事项

- 所有脚本均支持常见的视频格式（mp4、avi、mov、mkv、webm 等）。
- 输出视频的质量经过优化，以在文件大小和清晰度之间取得平衡。
- 使用 `-h` 参数可查看脚本的详细使用说明；不使用该参数时，脚本会显示基本用法。
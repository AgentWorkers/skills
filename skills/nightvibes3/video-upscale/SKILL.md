---
name: video_upscale
description: "基于AI的视频画质提升技术：Real-ESRGAN与Waifu2x的结合应用  
当用户需要提升视频质量、进行视频缩放或转换至高清/4K格式时，可选用该技术。该技术适用于动漫及真实视频素材，并支持处理过程中的进度跟踪功能。"
metadata: {"openclaw":{"emoji":"🎬","triggers":["upscale","enhance","make HD","make 4K","improve quality"]}}
---
# 视频放大功能

基于人工智能的视频放大技术，支持进度跟踪和任务隔离。

## 快速使用方法

```bash
/home/bobby/video-tools/real-video-enhancer/upscale_video.sh "{{filepath}}" "{{output_path}}" "{{mode}}" "{{preset}}" "{{engine}}" "{{job_id}}"
```

## 参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| filepath | 必填 | 输入视频路径 |
| mode | auto | `anime` 或 `real`（自动检测） |
| preset | fast | `fast`（2倍放大）或 `high`（4倍放大） |
| engine | auto | `waifu2x` 或 `realesrgan` |
| job_id | auto | `tg_<chatid>_<messageid>` |

## 模式选择

- **anime** → Waifu2x（更适合带有文字的动漫） |
- **real** → Real-ESRGAN（更适合逼真的图像）

## 预设选择

| 预设 | 放大倍数 | CRF 值 | 处理速度 |
|--------|---------|-----|-------|
| fast | 2倍 | 20 | 速度较快 |
| high | 4倍 | 16 | 速度较慢 |

## 示例命令

- “放大这个视频” |
- “将这个动漫片段放大” |
- “将视频分辨率提升到4K” |
- “以高质量进行优化，并随时通知我处理进度”

## 输出格式

```
JOB_ID: tg_123_456
PHASE: EXTRACTING_FRAMES
FRAMES_TOTAL: 780
PHASE: UPSCALING
PROGRESS: 78/780
...
STATUS: OK
UPSCALED_VIDEO: /path/to/output.mp4
```

## 安装说明

请参阅 [INSTALL.md](references/INSTALL.md) 以获取安装指南。
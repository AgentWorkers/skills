---
name: video-frames
description: 使用 ffmpeg 从视频中提取帧或短片段。
homepage: https://ffmpeg.org
metadata: {"clawdbot":{"emoji":"🎞️","requires":{"bins":["ffmpeg"]},"install":[{"id":"brew","kind":"brew","formula":"ffmpeg","bins":["ffmpeg"],"label":"Install ffmpeg (brew)"}]}}
---

# 视频帧（ffmpeg）

从视频中提取单帧，或生成用于查看的缩略图。

## 快速入门

提取第一帧：

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --out /tmp/frame.jpg
```

在指定时间戳处提取帧：

```bash
{baseDir}/scripts/frame.sh /path/to/video.mp4 --time 00:00:10 --out /tmp/frame-10s.jpg
```

## 注意事项：

- 使用 `--time` 参数可以查看指定时间点附近的视频内容。
- 若需要快速分享视频内容，建议使用 `.jpg` 格式；若需要用于高清晰度的用户界面展示，则使用 `.png` 格式。
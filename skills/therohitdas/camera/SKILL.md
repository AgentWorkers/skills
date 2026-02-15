---
name: camera
description: 从 MacBook 的网络摄像头中捕获照片。当用户请求拍照、截图或查看照片时可以使用此功能。MacBook 提供两个摄像头：Brio（位于显示器正面的前置摄像头）和 FaceTime（位于 MacBook 侧面的摄像头）。
---

# 相机功能

## 可用的相机

| 相机 | 索引 | 位置 | 适用场景 |
|--------|-------|----------|----------|
| **Brio 100** | 0 | 安装在外置显示器上，正对用户 | 正面视角，用于拍摄面部照片 |
| **FaceTime HD** | 1 | 安装在MacBook右侧，朝向用户倾斜 | 侧面/侧面视角 |

## 拍摄命令

使用 `-loglevel error` 来抑制ffmpeg产生的冗余日志信息。拍摄前请务必进行5秒的预热（相机需要调整曝光设置）。

### Brio（正面视角）
```bash
ffmpeg -loglevel error -f avfoundation -framerate 30 -i "0" -t 5 -y /tmp/brio_warmup.mp4 && \
ffmpeg -loglevel error -sseof -0.5 -i /tmp/brio_warmup.mp4 -frames:v 1 -update 1 -y /tmp/brio.jpg
```

### FaceTime（侧面视角）
**必须使用 `-pixel_format nv12`** 以避免缓冲区错误。
```bash
ffmpeg -loglevel error -f avfoundation -pixel_format nv12 -framerate 30 -i "1" -t 5 -y /tmp/facetime_warmup.mp4 && \
ffmpeg -loglevel error -sseof -0.5 -i /tmp/facetime_warmup.mp4 -frames:v 1 -update 1 -y /tmp/facetime.jpg
```

### 两种相机同时使用（多角度拍摄）
同时运行这两个命令以获取多角度的照片。

## 输出结果
- 照片保存在 `/tmp/brio.jpg` 和 `/tmp/facetime.jpg` 文件中
- 预热视频保存在 `/tmp/*_warmup.mp4` 文件中（可删除）
- 每张照片的大小约为80-100KB

## 注意事项
- 请先关闭Photo Booth或其他相机应用程序（否则可能会产生冲突）
- FaceTime相机必须使用 `-pixel_format nv12`，否则会因缓冲区错误而无法正常工作
- 拍摄前进行5秒的预热是确保正确曝光的必要步骤
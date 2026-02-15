---
name: mac-node-snapshot
description: 一种通过 OpenClaw 的 `screen.record` 功能来捕获 macOS 屏幕内容的强大且易于使用的方法。非常适合无头环境（headless environments），同时能够确保捕获过程的可靠性。
---

# mac-node-snapshot

## 概述
该技能使用 `node screen.record` 功能来录制 1 秒钟的屏幕画面，并提取一张高质量的 PNG 图片。此工作流程可以绕过常见的屏幕截图权限问题，确保获取到可靠的图像。

## 快速入门（单个命令，无需脚本）
所有路径均以 `{skill}` 为基准。

```bash
mkdir -p "{skill}/tmp" \
&& openclaw nodes screen record --node "<node>" --duration 1000 --fps 10 --no-audio --out "{skill}/tmp/snap.mp4" \
&& ffmpeg -hide_banner -loglevel error -y -ss 00:00:00 -i "{skill}/tmp/snap.mp4" -frames:v 1 "{skill}/tmp/snap.png"
```

## 适用场景
当用户请求以下操作时，可以使用此技能：
- “截图”
- “我的屏幕上显示的是什么？”
- “捕获屏幕画面”
- “通过 `screen.record` 功能截图”

## 注意事项：
- **系统要求**：需要安装 `ffmpeg`（安装前请先询问用户）。
- 如果提取到的图片为黑色，建议用户唤醒屏幕后再尝试。
- 可以使用 `read` 命令读取 `{skill}/tmp/snap.png` 文件，并将其作为回复内容发送给用户。

## 常见问题及解决方法：
- **`screen_record` 失败（节点断开连接）**：检查节点状态，确保 OpenClaw 应用正在运行且已正确配对。
- **`screenRecording` 选项被禁用**：用户需要在系统设置中允许屏幕录制功能；此问题无法绕过。
- **图片显示为黑色**：可能是屏幕处于休眠或锁定状态，请用户唤醒屏幕后再尝试。
# AOI演示片段制作工具（macOS）

S-DNA: `AOI-2026-0215-SDNA-CLIP01`

## 该工具的功能
这是一个仅适用于终端（且符合公共安全标准的）工具，用于在macOS上制作黑客马拉松的演示片段。该工具基于`ffmpeg/ffprobe`实现以下功能：
- 列出可用的捕获设备（通过`avfoundation`接口）
- 录制屏幕内容（持续N秒）
- 剪裁屏幕顶部的菜单栏或标题栏
- 对视频片段进行裁剪
- 提供简单的预设选项供用户选择

## 该工具不支持的功能
- 无法将视频上传至YouTube
- 不支持任何形式的表单提交
- 不允许将视频发布到外部平台
- 不涉及任何敏感信息的处理（如密码等）

## 使用要求
- 确保系统为macOS
- 已安装`ffmpeg`和`ffprobe`程序
- 终端应用程序必须具有屏幕录制的权限

## 命令说明
### 1) 列出可用捕获设备
```bash
aoi-clip devices
```

### 2) 录制屏幕内容
```bash
# pixel_format auto-fallback is enabled by default
# (tries: uyvy422 → nv12 → yuyv422 → 0rgb → bgr0)
aoi-clip record --out tempo_demo_raw.mp4 --duration 15 --fps 30 --screen "Capture screen 0"

# optionally force a specific pixel format
# aoi-clip record --out tempo_demo_raw.mp4 --duration 15 --fps 30 --screen "Capture screen 0" --pixel uyvy422
```

### 3) 剪裁屏幕顶部的菜单栏
```bash
# explicit crop
aoi-clip crop --in tempo_demo_raw.mp4 --out tempo_demo_crop.mp4 --top 150

# auto-recommend top crop based on video height (still applies crop, but chooses a value)
aoi-clip crop --in tempo_demo_raw.mp4 --out tempo_demo_crop.mp4 --top auto
```

### 4) 对视频片段进行裁剪
```bash
aoi-clip trim --in tempo_demo_crop.mp4 --out tempo_demo_15s.mp4 --from 0 --to 15
```

### 5) 使用预设设置进行视频处理
```bash
aoi-clip preset terminal --out demo.mp4
```

## 安全性与审计要求
该工具仅在本地运行`ffmpeg/ffprobe`，并严格限制可执行的二进制文件及参数。

## 发布管理（公开透明）
我们免费发布这些工具，并持续对其进行优化。每次发布前，工具都必须通过我们的安全审核流程，并附带详细的变更日志。我们绝不会发布任何会削弱安全性的更新或导致许可条款模糊的版本。如多次违反安全规定，我们将逐步采取限制措施（从警告开始，直至暂停发布或最终将工具归档）。

## 技术支持
- 如有疑问、发现漏洞或需要功能请求，请访问：[https://github.com/edmonddantesj/aoi-skills/issues](https://github.com/edmonddantesj/aoi-skills/issues)
- 请在提交问题时注明工具的名称：`aoi-demo-clip-maker`

## 许可协议
本工具采用MIT许可证。
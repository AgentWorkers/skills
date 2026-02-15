---
name: Screenshot
description: 使用合适的工具，在各种平台上捕获屏幕截图、窗口截图以及指定区域的内容。
metadata: {"clawdbot":{"emoji":"📸","os":["linux","darwin","win32"]}}
---

## macOS

- 使用内置的 `screencapture` 命令：
  - `-x` 选项用于静默截图：`screencapture -x output.png`
  - `-i` 选项用于交互式选择要截图的区域。
- 通过进程 ID (PID) 捕获特定窗口：`screencapture -l$(osascript -e 'tell app "AppName" to id of window 1') out.png`
- 对于视网膜显示器，默认输出分辨率为原始分辨率的两倍；若需捕获精确的像素区域，请使用 `-R x,y,w,h` 选项。
- iOS 模拟器：`xcrun simctl io booted screenshot output.png` — 比 `screencapture` 更快速且更可靠。

## Linux

- GNOME 系统使用 `gnome-screenshot`，KDE 系统使用 `spectacle`，极简或无头环境使用 `scrot`。
- 无头 X11 环境：`xvfb-run scrot output.png` — 适用于持续集成 (CI) 环境。
- Wayland 会话可能会影响 X11 工具的正常使用；在 Wayland 环境中推荐使用 `grim`，在需要选择截图区域时使用 `slurp`。

## Windows

- PowerShell 内置命令：`Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | ...` 虽然可行，但代码较为冗长；推荐使用 `nircmd savescreenshot`。
- `nircmd savescreenshot output.png` 可在命令行 (CLI) 中使用，且几乎不受 Windows 版本限制。
- 若需编程方式捕获屏幕截图，`python -m PIL.ImageGrab` 具有跨平台兼容性，但需要先安装 Pillow 库。

## Web 页面

- 使用 Playwright 工具：`npx playwright screenshot URL output.png --full-page` — 可捕获包含 JavaScript 渲染和滚动内容的完整页面。
- 请确保网络请求已完成后再执行截图操作（使用 `--wait-for-timeout=5000` 参数）；否则页面可能无法完全加载动态内容。
- 对于较长的页面，全页截图可能会导致像素失真；建议将其分割成适合视口大小的片段。
- Puppeteer 的等效命令：`page.screenshot({fullPage: true})`，需在 `networkidle0` 后执行。

## 格式与质量

- UI 和文本内容建议使用 PNG 格式（无损压缩），照片使用 JPEG 格式（文件体积更小）。
- JPEG 的质量设置在 85-92% 之间最为合适：低于 85% 会导致文本显示失真，高于 95% 也不会带来明显画质提升。
- WebP 格式相比 JPEG 可节省 25-35% 的文件体积，但除旧版 Safari 外，大多数浏览器都支持该格式。

## 自动化最佳实践

- 为截图文件添加时间戳：`screenshot-$(date +%Y%m%d-%H%M%S).png` — 避免批量操作时文件被覆盖。
- 在进行对比测试时，请确保所有截图的视口大小一致；不同分辨率可能导致错误的差异结果。
- 在上传截图前，使用 `pngquant` 或 `jpegoptim` 工具对图片进行压缩，以节省存储和传输时间。
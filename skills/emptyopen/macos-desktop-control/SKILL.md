# macOS 控制技能

这是一个专为 macOS (Darwin) 设计的高保真自动化工具，能够让代理程序感知桌面状态，并执行精确的鼠标和键盘操作。

## 🛠 包含的脚本
该技能利用位于 `/scripts` 目录中的专用封装脚本与系统级二进制文件进行交互：

### 1. `clicclick_wrapper.sh`
用于处理合成输入事件的 `clicclick` 工具的专用封装脚本。
- **路径**: `scripts/clicclick_wrapper.sh`
- **功能**: 执行 `/opt/homebrew/bin/clicclick` 并传递参数。
- **支持的操作**: 左键/右键点击、鼠标移动以及键盘模拟。

### 2. `vision_wrapper.sh`
该技能的视觉感知引擎。
- **路径**: `scripts/vision_wrapper.sh`
- **功能**: 以静默模式（使用 `-x` 参数）调用 macOS 的原生 `screencapture` 工具。
- **输出**: 生成一个标准的 PNG 图像文件，保存在 `/tmp/claw_view.png` 中。

---

## 🚀 工具规格

### `see`
用于捕获当前屏幕状态以供视觉分析。
- **返回值**: 一个字符串，表示捕获文件的路径。
- **用途**: 用于识别 UI 元素、窗口位置以及应用程序状态。

### `click`
用于向鼠标和键盘发送精确的指令。
- **用法**: `click "c:x,y"`（点击）或 `click "m:x,y"`（移动）。
- **语法**: 支持 `clicclick` 的所有标准语法，包括 `w:`（等待）和 `t:`（输入）。

---

## ⚙️ 需求与设置

1. **二进制依赖项**:
   ```bash
   brew install cliclick
   ```
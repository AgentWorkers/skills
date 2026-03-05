---
name: macpilot-screenshot-ocr
description: 使用 MacPilot 捕获屏幕截图并通过 OCR（光学字符识别）提取文本。您可以截取全屏、指定区域或窗口的截图，并支持多语言识别屏幕上的文本。
---
# MacPilot截图与OCR功能

使用MacPilot可以捕获屏幕、特定区域或应用程序窗口的截图，并利用苹果内置的Vision OCR技术从图像或屏幕区域中提取文本。

## 使用场景

在以下情况下可以使用此功能：
- 需要捕获当前屏幕上的内容
- 需要从图像文件中提取文本
- 需要读取屏幕上某个特定区域的文本
- 需要捕获某个特定应用程序窗口的内容
- 需要验证应用程序的视觉状态
- 需要录制屏幕画面

## 截图命令

### 全屏截图
```bash
macpilot screenshot --json                           # Capture to temp file
macpilot screenshot ~/Desktop/screen.png --json      # Capture to specific path
macpilot screenshot --with-permissions --json        # Use CGWindowListCreateImage directly
```

### 指定区域截图
```bash
macpilot screenshot --region 100,200,800,600 --json
# Region format: x,y,width,height (from top-left corner)
```

### 指定窗口截图
```bash
macpilot screenshot --window "Safari" --json         # Capture Safari window
macpilot screenshot --window "Finder" --json         # Capture Finder window
```

### 所有窗口截图
```bash
macpilot screenshot --all-windows --json             # Each window separately
```

### 指定显示区域截图
```bash
macpilot screenshot --display 1 --json               # Second display (0-indexed)
```

### 格式选项
```bash
macpilot screenshot --format png ~/Desktop/shot.png  # PNG (default, lossless)
macpilot screenshot --format jpg ~/Desktop/shot.jpg  # JPEG (smaller files)
```

## OCR命令

### 从图像文件中提取文本
```bash
macpilot ocr scan /path/to/image.png --json
macpilot ocr scan ~/Desktop/screenshot.png --json
```

### 从屏幕区域中提取文本
```bash
macpilot ocr scan 100 200 800 600 --json
# Arguments: x y width height (captures region then OCRs it)
```

### 多语言OCR支持
```bash
macpilot ocr scan image.png --language en-US --json       # English
macpilot ocr scan image.png --language ja --json           # Japanese
macpilot ocr scan image.png --language zh-Hans --json      # Simplified Chinese
macpilot ocr scan image.png --language de --json           # German
macpilot ocr scan image.png --language fr --json           # French
```

### OCR点击（查找并点击屏幕上的文本）
```bash
macpilot ocr click "Submit" --json                    # Find text on screen and click it
macpilot ocr click "OK" --app Finder --json           # Click text in specific app
macpilot ocr click "Accept" --timeout 10 --json       # Retry until text appears (10s)
```

“OCR点击”功能会先截取屏幕截图，然后运行OCR识别，找到匹配的文本（不区分大小写），并在文本中心坐标处进行点击。可以使用`--timeout`参数设置等待文本出现的超时时间，并在需要时重试。

## 屏幕录制（ScreenCaptureKit）

### 开始录制
```bash
macpilot screen record start --output ~/Desktop/recording.mov --json
macpilot screen record start --output rec.mov --region 0,0,1920,1080 --json  # Region
macpilot screen record start --output rec.mov --window Safari --json          # Window
macpilot screen record start --output rec.mov --display 1 --json              # Display
macpilot screen record start --output rec.mov --audio --json                  # With audio
macpilot screen record start --output rec.mov --quality high --fps 60 --json  # Quality
```

### 控制录制过程
```bash
macpilot screen record stop --json         # Stop and save
macpilot screen record status --json       # Check if recording
macpilot screen record pause --json        # Pause recording
macpilot screen record resume --json       # Resume recording
```

录制质量选项：`low`（1 Mbps）、`medium`（5 Mbps，默认值）、`high`（10 Mbps）。默认帧率为30帧/秒。

## 显示信息
```bash
macpilot display-info --json
# Returns: all displays with resolution, position, scale factor
```

## 工作流程示例

- **一键截图并OCR处理**：将截图与OCR功能结合使用。
- **快速截图并提取文本**：快速截取屏幕区域并提取其中的文本。
- **查找并点击文本**：无需手动计算坐标即可定位并点击屏幕上的文本。
- **验证用户界面状态**：检查应用程序界面的显示效果是否符合预期。
- **录制自动化操作**：将整个自动化流程录制下来。

## 使用技巧

- 请确保在系统设置中为MacPilot.app授予了屏幕录制权限。
- 对于包含文本的截图，PNG格式（无损压缩）是最佳选择；JPEG格式适用于普通图片。
- OCR对高对比度的文本识别效果更好；如果文本较小，请适当扩大截图区域。
- 在截取特定区域之前，可以使用`display-info`命令获取屏幕尺寸。
- 屏幕坐标系以左上角（0,0）为原点，x轴向右增加，y轴向下增加。
- 在Retina显示屏上，坐标值以逻辑像素为单位（而非物理像素）。
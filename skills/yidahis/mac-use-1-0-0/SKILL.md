---
name: mac-use
description: **视觉控制 macOS GUI 应用程序**  
- 可以截取屏幕截图；  
- 可以点击界面元素；  
- 可以滚动页面；  
- 可以在应用程序中输入文本。  
**适用场景**：当用户需要与任何 macOS 桌面应用程序的图形界面进行交互时使用。
metadata: {"openclaw":{"emoji":"🖥️","requires":{"bins":["python3"]},"os":["darwin"],"install":[{"id":"python-brew","kind":"brew","formula":"python","bins":["python3"],"label":"Install Python 3 (brew)"}]}}
---

# 在 macOS 上的使用方法

您可以通过以下步骤来控制任何 macOS 图形用户界面（GUI）应用程序：
1. **截图** → 2. **选择目标元素** → 3. **点击该元素** → 4. **验证操作结果**。

## 准备工作

**适用平台**：仅限 macOS（需要 Apple Vision 框架来支持光学字符识别 OCR 功能）。

**系统预装的二进制文件**：
- `python3` — 通过 Homebrew 安装 (`brew install python`)
- `screencapture` — macOS 内置的截图工具

**Python 包** — 请从技能目录（skill directory）中安装相关包：
```bash
pip3 install --break-system-packages -r {baseDir}/requirements.txt
```

## 工作原理

`screenshot` 命令会捕获当前窗口的图像，然后使用 Apple Vision OCR 技术检测其中的所有文本元素，并在图像上添加编号注释。最终会生成两个文件：
1. 一个带有注释的图像文件 `/tmp/mac_use.png`，其中每个检测到的文本元素都会被标记上绿色的编号框。
2. 一个 JSON 格式的元素列表，例如：`[{num: 1, text: "提交", at: [500, 200]}, {num: 2, text: "取消", at: [600, 200]}, ...}`，其中 `at` 表示元素在 1000x1000 像素画布上的中心坐标（坐标原点位于左上角）。

您可以通过以下两种方式获取这些信息：
- 通过 Bash 命令直接获取 JSON 格式的元素列表。
- 打开 `/tmp/mac_use.png` 文件来查看带有注释的图像。

**注意**：务必同时使用这两种方式，以便将元素编号与实际看到的内容进行对照。

## 快速参考

```bash
# List all visible windows
python3 {baseDir}/scripts/mac_use.py list

# Screenshot + annotate (returns image + numbered element list)
python3 {baseDir}/scripts/mac_use.py screenshot <app> [--id N]

# Click element by number (primary click method)
python3 {baseDir}/scripts/mac_use.py clicknum <N>

# Click at canvas coordinates (fallback for unlabeled icons)
python3 {baseDir}/scripts/mac_use.py click --app <app> [--id N] <x> <y>

# Scroll inside a window
python3 {baseDir}/scripts/mac_use.py scroll --app <app> [--id N] <direction> <amount>

# Type text (uses clipboard paste — supports all languages)
python3 {baseDir}/scripts/mac_use.py type [--app <app>] "text here"

# Press key or combo
python3 {baseDir}/scripts/mac_use.py key [--app <app>] <combo>
```

## 工作流程

1. 使用 `open -a "应用程序名称"` 打开目标应用程序（可选地也可以使用 URL 或文件路径）。
2. 等待应用程序加载完成：`sleep 2`。
3. 使用 `screenshot` 命令截图该应用程序：
   这个命令会返回一个 JSON 文件，其中包含图像路径 (`file`) 和元素列表 (`elements`)。
4. 打开 `/tmp/mac_use.png` 文件，查看带有编号的元素。
5. 决定要与哪个元素进行交互：
   - **推荐使用 `clicknum N`：直接点击编号对应的元素。
   - **备用方法：click --app <应用程序名称> x y`：仅用于那些没有文字标签的图标（如箭头、关闭按钮等）。
6. 根据需要使用 `clicknum`、`type`、`key` 或 `scroll` 命令来执行操作。
7. 再次截图以验证操作结果。
8. 重复步骤 3。

## 常用命令

### `list`  
显示所有可见的应用程序窗口。  
返回的 JSON 数组示例：`[{"app":"Google Chrome","title":"Wikipedia","id":4527,"x":120,"y":80,"w":1200,"h":800}, ...]`

### `screenshot`  
捕获当前窗口的图像，使用 OCR 技术检测文本元素，并添加编号注释。在截图之前，目标窗口会自动移动到屏幕顶部，以便处理窗口重叠的情况。  
- 参数说明：  
  - `<应用程序名称>`：模糊匹配（不区分大小写，例如 "chrome" 会匹配 "Google Chrome"）。
  - `--id N`：指定目标窗口的 ID（当同一应用程序有多个窗口时需要使用）。
  - 返回的 JSON 包含：  
    - `file`：带有注释的截图文件路径（`/tmp/mac_use.png`）。
    - `id`、`app`、`title`、`scale`：窗口的元数据。
    - `elements`：一个包含元素信息的数组（每个元素的形式为 `{num, text, at}`，其中 `at` 表示元素在 1000x1000 像素画布上的坐标）。
  - 如果有多个匹配的窗口，会返回一个窗口列表，此时需要使用 `--id` 参数来指定目标窗口。

### `clicknum`  
点击上一张截图中编号对应的元素。这是主要的交互方式。  
- 参数说明：  
  - `N`：上一张截图中元素的编号。

### `click`  
使用画布坐标来点击屏幕上的某个位置。**仅用于没有文字标签的图标**。  
- 参数说明：  
  - 坐标范围是 0-1000，其中 x=0 表示左侧，y=0 表示顶部。

### `scroll`  
在应用程序窗口内滚动。  
- 可用的方向：`up`（向上）、`down`（向下）、`left`（向左）、`right`（向右）。
- 滚动幅度：3-5 表示中等速度，10+ 表示快速滚动。
- 在滚动前，鼠标会移动到窗口的中心位置。

### `type`  
在当前聚焦的输入框中输入文本。  
- 参数说明：  
  - `--app`：先激活目标应用程序，确保输入内容会发送到正确的窗口。
  - 使用剪贴板（Cmd+V）来确保文本格式正确（支持 Unicode 和中文字符）。
  - 输入前请确保先点击目标输入框。

### `key`  
按下单个键或键组合。  
- 参数说明：  
  - `--app`：先激活目标应用程序。
  - 常用键：`return`、`tab`、`escape`、`space`、`delete`、`backspace`、`up`、`down`、`left`、`right`。
  - 可选修饰符：`cmd`、`ctrl`、`alt`/`opt`、`shift`。

## 重要规则

- 在与应用程序进行任何交互之前，务必先截图。
- 每次操作完成后，务必截图以验证结果。
- 运行 `screenshot` 命令后，务必查看截图文件，因为您需要同时获取元素列表和视觉结果。
- 尽量使用 `clicknum` 而不是 `click`，除非目标元素没有文字标签。
- 在输入内容之前，请确保先点击正确的输入框。
- 如果系统显示 `multiple_windows` 错误，使用 `list` 命令查看所有窗口，然后使用 `--id` 参数来指定目标窗口。
- 对于弹出窗口（如微信小程序面板），它们是独立的窗口，具有自己的 ID，需要使用 `list` 和 `--id` 来定位它们。
- 打开应用程序后，请等待 2-3 秒再截图。
- 在截图或点击之前，请先使用 `osascript -e 'tell application "应用程序名称" to activate' && sleep 1` 来激活目标应用程序（以防应用程序被其他窗口遮挡）。
- 请勿使用此工具输入密码或敏感信息。

## 坐标系统（仅用于 `click` 命令）

截图会被渲染在一个 1000x1000 像素的画布上：
- 坐标原点 (0, 0) 位于左上角。
- x 值从左向右递增（0 表示左侧边界，1000 表示右侧边界）。
- y 值从上向下递增（0 表示顶部边界，1000 表示底部边界）。
- 应用程序窗口会自动调整大小以适应画布，并保持原有的宽高比，周围会有深灰色的边框。

## 示例：在微信中使用该工具在美团上点餐**

```bash
# 1. Open WeChat
open -a "WeChat"
sleep 3

# 2. Screenshot WeChat — find the mini program window
python3 {baseDir}/scripts/mac_use.py list
# → find the mini program window ID

# 3. Screenshot the mini program (annotated + element list)
python3 {baseDir}/scripts/mac_use.py screenshot 微信 --id 41266
# → returns: {"file": "/tmp/mac_use.png", "elements": [{num: 1, text: "搜索", at: [500, 200]}, ...]}
# → Read /tmp/mac_use.png to see annotated image

# 4. Click "搜索" (element #1)
python3 {baseDir}/scripts/mac_use.py clicknum 1

# 5. Type search query
python3 {baseDir}/scripts/mac_use.py type --app 微信 "炸鸡"

# 6. Press Enter
python3 {baseDir}/scripts/mac_use.py key --app 微信 return
sleep 2

# 7. Screenshot to see results
python3 {baseDir}/scripts/mac_use.py screenshot 微信 --id 41266
# → Read /tmp/mac_use.png, pick a restaurant by number

# 8. Click on a restaurant (e.g. element #5)
python3 {baseDir}/scripts/mac_use.py clicknum 5
```
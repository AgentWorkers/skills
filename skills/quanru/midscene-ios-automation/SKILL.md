---
name: iOS Device Automation
description: |
  AI-powered iOS device automation using Midscene CLI. Control iOS devices and simulators
  with natural language commands via WebDriverAgent.
  Triggers: ios, iphone, ipad, ios app, tap on iphone, swipe, ios simulator, mobile app ios,
  ios device, ios testing, iphone automation, ipad automation, ios screen, ios navigate
allowed-tools:
  - Bash
---

# iOS设备自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在任何Bash工具调用中设置`run_in_background: true`**，用于midscene命令。每个`npx @midscene/ios`命令必须使用`run_in_background: false`（或完全省略该参数）。在任务结束后，后台执行会导致通知频繁弹出，从而破坏截图分析-执行循环。
> 2. **每次Bash工具调用只能发送一个midscene CLI命令**。等待其结果，读取截图，然后决定下一步操作。切勿使用`&&`、`;`或`sleep`来链接命令。
> 3. **为每次Bash工具调用设置`timeout: 60000`（60秒）**，以确保midscene命令有足够的时间同步完成。

使用`npx @midscene/ios`自动化iOS设备和模拟器。每个CLI命令都直接对应一个MCP工具——您（AI代理）作为大脑，根据截图来决定采取哪些操作。

## 先决条件

CLI会自动从当前工作目录加载`.env`文件。首次使用前，请确认`.env`文件存在并且包含API密钥：

```bash
cat .env | grep MIDSCENE_MODEL_API_KEY | head -c 30
```

如果不存在`.env`文件或API密钥，请让用户创建一个。有关支持的提供者，请参阅[模型配置](https://midscenejs.com/zh/model-common-config.html)。

**切勿运行`echo $MIDSCENE_MODEL_API_KEY`**——密钥是在运行时从`.env`文件中加载的，而不是从shell环境中加载的。

## 命令

### 连接到设备

```bash
npx @midscene/ios connect
```

### 截取屏幕截图

```bash
npx @midscene/ios take_screenshot
```

截取屏幕截图后，读取保存的图像文件以了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用actionSpace工具与设备进行交互：

```bash
npx @midscene/ios Tap --locate '{"prompt":"the Settings icon"}'
npx @midscene/ios Input --locate '{"prompt":"search field"}' --content 'hello world'
npx @midscene/ios Scroll --direction down
npx @midscene/ios Swipe --locate '{"prompt":"the notification panel"}' --direction down
npx @midscene/ios KeyboardPress --value Enter
npx @midscene/ios LongPress --locate '{"prompt":"the message bubble"}'
npx @midscene/ios Launch --uri 'com.apple.Preferences'
```

### 自然语言操作

使用`act`在一个命令中执行多步骤操作——适用于临时UI交互：

```bash
npx @midscene/ios act --prompt "tap Delete, then confirm in the alert dialog"
```

### 断开连接

```bash
npx @midscene/ios disconnect
```

## 工作流程模式

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **截取屏幕截图**以查看当前状态
3. **分析**屏幕截图以决定下一步操作
4. **执行操作**（点击、输入、滚动等）
5. **再次截取屏幕截图**以验证结果
6. **重复步骤3-5，直到任务完成
7. **完成后断开连接**

## 最佳实践

1. **频繁截取屏幕截图**：在每个操作之前和之后都截取屏幕截图，以验证状态变化。
2. **清晰描述UI元素**：使用可见的文本标签、图标或位置描述（例如，“右上角的设置图标”，而不是模糊的描述）。
3. **使用JSON传递定位参数**：始终以JSON字符串的形式传递`--locate`参数，并在字符串中包含描述目标元素的`prompt`字段。
4. **顺序执行操作**：一次执行一个操作，并在进入下一步之前验证结果。
5. **切勿在后台运行**：在每次Bash工具调用中，要么省略`run_in_background`参数，要么明确将其设置为`false`。切勿设置`run_in_background: true`。

### 处理临时UI

操作表单、警告对话框、弹出菜单和分享表单在命令执行之间会消失。在与临时UI交互时：

- **使用`act`进行多步骤临时交互**——它会在一个进程中执行所有操作。
- **或者快速连续执行命令**——在步骤之间不要截取屏幕截图。
- **不要暂停进行分析**——连续执行与临时交互相关的所有命令。
- 持久性UI（应用屏幕、标签栏、导航栏）可以在不同的命令之间进行交互。

**示例 — 使用`act`处理警告对话框（推荐用于临时UI）：**

```bash
npx @midscene/ios act --prompt "tap the Delete button, then confirm in the alert dialog"
npx @midscene/ios take_screenshot
```

**示例 — 使用单独的命令处理警告对话框（另一种方法）：**

```bash
# Tap the button that triggers the alert, then interact with the alert back-to-back
npx @midscene/ios Tap --locate '{"prompt":"the Delete button"}'
npx @midscene/ios Tap --locate '{"prompt":"Confirm in the alert dialog"}'
# NOW take a screenshot to verify the result
npx @midscene/ios take_screenshot
```

## 故障排除

### WebDriverAgent未运行
**症状：**连接被拒绝或出现超时错误。
**解决方案：**
- 确保WebDriverAgent已安装在设备/模拟器上并正在运行。
- 对于模拟器：检查`http://localhost:8100/status`是否返回有效响应。
- 请参阅https://midscenejs.com/zh/usage-ios.html以获取设置说明。

### 未找到设备
**症状：**未检测到设备或出现连接错误。
**解决方案：**
- 对于物理设备：确保设备已通过USB连接并且被信任。
- 对于模拟器：使用`xcrun simctl list devices booted`验证模拟器是否已启动。

### API密钥问题
**症状：**出现认证或模型错误。
**解决方案：**
- 检查`.env`文件中是否包含`MIDSCENE_MODEL_API_KEY=<your-key>`。
- 详情请参阅https://midscenejs.com/zh/model-common-config.html。
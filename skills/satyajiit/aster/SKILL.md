---
name: aster
version: 0.1.13
description: 您的AI CoPilot移动版——或者干脆为您的AI配备一部独立的手机。通过MCP，您可以拨打电话、发送短信、使用语音播报功能（TTS）进行语音交流、自动化用户界面操作、管理文件、搜索媒体内容，以及使用40多种其他工具。该平台采用开源技术，支持自我托管，并将用户隐私置于首位。
homepage: https://aster.theappstack.in
metadata: {"aster":{"category":"device-control","requires":{"bins":["node"]},"mcp":{"type":"http","url":"http://localhost:5988/mcp"}}}
---

# Aster – 你的移动AI助手

这是一个专为Android设备设计的AI助手，它支持MCP（Model Context Protocol）协议。你也可以为AI配备专属手机，让它自行拨打电话、发送短信并执行各种操作。该项目完全开源，且高度重视用户隐私——你的数据永远不会离开你的网络。

**官方网站**：[aster.theappstack.in](https://aster.theappstack.in) | **GitHub仓库**：[github.com/satyajiit/aster-mcp](https://github.com/satyajiit/aster-mcp)

---

如需查看Android应用程序和Web控制台的截图，请访问[aster.theappstack.in](https://aster.theappstack.in)。

---

## 设置

1. **安装并启动服务器**：
```bash
npm install -g aster-mcp
aster start
```

2. 从[Releases](https://github.com/satyajiit/aster-mcp/releases)下载Aster Android应用程序，并将其安装到你的Android设备上（可以是你的日常使用手机，或者专门用于AI的设备），然后连接到终端中显示的服务器地址。

3. 在你的`.mcp.json`文件中配置MCP设置：
```json
{
  "mcpServers": {
    "aster": {
      "type": "http",
      "url": "http://localhost:5988/mcp"
    }
  }
}
```

---

## 安全性与隐私保护

Aster采用了以安全性和隐私保护为核心的架构：

- **本地运行**：所有功能都在你的本地机器上运行，不依赖云服务器或第三方中继服务。你的数据始终保留在你的网络范围内。
- **零数据收集**：不进行任何分析、跟踪或使用数据收集。你的所有操作都由你自己掌控。
- **设备审批**：每台新设备在连接或执行命令之前，都需要通过控制台进行手动审批。
- **Tailscale集成**：支持通过Tailscale和WireGuard实现加密的远程访问，支持自动TLS（WSS）加密，无需端口转发。
- **无需root权限**：仅使用官方的Android辅助功能API（与屏幕阅读器相同的系统接口），无需root权限、ADB调试或任何漏洞利用。所有操作都受到权限控制，并处于沙箱环境中。
- **前台可见性**：当服务运行时，会在Android设备上显示通知图标，不会在后台悄悄运行。
- **数据存储本地**：所有数据（设备信息、日志等）都存储在本地SQLite数据库中，不会被发送到外部。
- **100%开源**：采用MIT许可证，代码完全公开透明，你可以在[GitHub](https://github.com/satyajiit/aster-mcp)上查看每一行代码。

---

## 可用工具

### 设备与屏幕操作
- `aster_list_devices` – 列出已连接的设备
- `aster_get_device_info` – 获取设备详情（电池电量、存储空间、规格等）
- `aster_take_screenshot` – 截取屏幕截图
- `aster_get_screen_hierarchy` – 获取UI层级结构

### 输入与交互
- `aster_input_gesture` – 点击、滑动、长按等手势操作
- `aster_input_text` – 在指定字段中输入文本
- `aster_click_by_text` – 通过文本点击元素
- `aster_click_by_id` – 通过元素ID点击元素
- `aster_find_element` – 查找UI元素
- `aster_global_action` – 返回主页、最近使用应用等操作

### 应用与系统操作
- `aster_launch(intent` – 启动应用程序或执行系统意图
- `aster_list_packages` – 列出已安装的应用程序
- `aster_read_notifications` – 读取通知信息
- `aster_read_sms` – 读取短信内容
- `aster_send_sms` – 向指定电话号码发送短信
- `aster_get_location` – 获取GPS位置信息
- `aster_execute_shell` – 在Android应用沙箱中运行shell命令（无root权限，仅限于应用数据目录和用户可访问的存储空间，超时30秒，输出限制为1MB）

### 文件与存储操作
- `aster_list_files` – 列出目录内容
- `aster_read_file` – 读取文件内容
- `aster_write_file` – 向文件写入内容
- `aster_delete_file` – 删除文件
- `aster_analyze_storage` – 分析存储空间使用情况
- `aster_find_large_files` – 查找大文件
- `aster_search_media` – 通过自然语言搜索图片/视频

### 设备功能控制
- `aster_get_battery` – 获取电池电量信息
- `aster_get_clipboard` / `aster_set_clipboard` – 访问剪贴板
- `aster_show_toast` – 显示通知提示
- `aster_speak_tts` – 文本转语音
- `aster_vibrate` – 振动设备
- `aster_play_audio` – 播放音频
- `aster_post_notification` – 发送通知
- `aster_make_call` – 拨打电话
- `aster_make_call_with_voice` – 拨打电话后启用免提功能，并通过TTS朗读AI生成的文本
- `aster_show-overlay` – 在设备上显示网页覆盖层

### 媒体处理
- `aster_index_media_metadata` – 提取图片/视频的EXIF元数据
- `aster_search_media` – 通过自然语言查询搜索图片/视频

---

## 主动事件转发（OpenClaw回调）

Aster可以通过Webhook将手机上的实时事件推送到你的AI代理。启用此功能后，事件会以HTTP POST格式发送，代理无需主动请求数据——手机会自动将事件信息发送给你。

你可以通过控制台（路径：/settings/openclaw）或命令行界面（CLI）来配置事件转发功能：`aster set-openclaw-callbacks`。

### Webhook格式

事件通过HTTP POST请求发送到配置的OpenClaw端点（默认为`/hooks/agent`）。AI会读取`message`字段中的数据。所有事件相关信息都使用标准的`[key] value`格式进行封装。

**通知事件的示例HTTP POST请求数据**：
```json
{
  "message": "[skill] aster\n[event] notification\n[device_id] 6241e40fb71c0cf7\n[model] samsung SM-S938B, Android 16\n[data-app] messaging\n[data-package] com.google.android.apps.messaging\n[data-title] John\n[data-text] Hey, are you free tonight?",
  "wakeMode": "now",
  "deliver": true,
  "channel": "whatsapp",
  "to": "+1234567890"
}
```

- `message` – 包含标准头部信息的结构化事件数据（AI会读取该字段）
- `wakeMode` – 始终设置为`now`（立即唤醒代理）
- `deliver` – 对于真实事件始终设置为`true`，对于测试请求设置为`false`
- `channel` / `to` – 事件传递的通道和接收者（在控制台进行配置）

### 事件格式

所有事件都遵循统一的格式，包含4个固定头部字段和`[data-*]`数据字段：

```
[skill] aster
[event] <event_name>
[device_id] <device_uuid>
[model] <manufacturer model, Android version>
[data-key] value
[data-key] value
```

- `[skill]` – 始终为`aster`
- `[event]` – 事件类型：`sms`、`notification`、`device_online`、`device_offline`、`pairing`
- `[device_id]` – 设备的UUID（用于使用Aster工具定位设备）
- `[model]` – 设备制造商、型号和操作系统
- `[data-*]` – 与事件相关的具体数据（每个字段前缀为`data-`，例如`[data-app]`、`[data-sender]`）

### 事件类型

- **`sms`** – 收到的短信
```
[skill] aster
[event] sms
[device_id] a1b2c3d4-5678-90ab
[model] samsung SM-S938B, Android 15
[data-sender] +1234567890
[data-body] Hey are you free tonight?
```

- **`notification`** – 应用程序通知（与短信通知区分）
```
[skill] aster
[event] notification
[device_id] a1b2c3d4-5678-90ab
[model] samsung SM-S938B, Android 15
[data-app] whatsapp
[data-package] com.whatsapp
[data-title] John
[data-text] Meeting moved to 3pm
```

- **`device_online`** – 设备上线
```
[skill] aster
[event] device_online
[device_id] a1b2c3d4-5678-90ab
[model] samsung SM-S938B, Android 15
[data-status] connected
```

- **`device_offline`** – 设备离线
```
[skill] aster
[event] device_offline
[device_id] a1b2c3d4-5678-90ab
[model] samsung SM-S938B, Android 15
[data-status] disconnected
```

- **`pairing`** – 新设备需要审批（使用`[device_id]`进行审批）
```
[skill] aster
[event] pairing
[device_id] e5f6g7h8-9012-cdef
[model] Samsung SM-S924B, Android 15
[data-status] pending_approval
[data-action] approve this device from the Aster dashboard or via aster devices approve
```

### 如何处理事件

当你收到带有`[skill] aster`的请求时，解析`[event]`和`[device_id`字段，以确定发生了什么以及应该对哪个设备采取行动。

- **短信**：回复短信、提取信息或采取其他操作
```
[event] sms | [device_id] a1b2c3d4 | sender: +1234567890 | body: Running late, be there in 20
→ aster_send_sms (deviceId: a1b2c3d4) to +1234567890: "No worries, see you soon!"

[event] sms | [device_id] a1b2c3d4 | sender: +1800555 | body: Your OTP is 482913
→ Extract OTP "482913", use aster_input_text (deviceId: a1b2c3d4) to enter it
```

- **通知**：监控通知内容并代表用户执行相应操作
```
[event] notification | [device_id] a1b2c3d4 | app: driver | text: Your driver is arriving
→ aster_speak_tts (deviceId: a1b2c3d4) "Your Uber is almost here"

[event] notification | [device_id] a1b2c3d4 | app: mShop | text: Your package was delivered
→ aster_send_sms (deviceId: a1b2c3d4) to user: "Your Amazon package just arrived"
```

- **设备状态管理**：管理设备的连接状态
```
[event] device_offline | [device_id] a1b2c3d4
→ Pause pending automations for device a1b2c3d4

[event] device_online | [device_id] a1b2c3d4
→ Resume queued tasks, aster_read_notifications (deviceId: a1b2c3d4) to catch up
```

- **设备配对**：审批新设备或发出警报
```
[event] pairing | [device_id] e5f6g7h8 | model: Samsung SM-S924B
→ If expected: approve device e5f6g7h8 via dashboard API
→ If unexpected: alert user "Unknown device SM-S924B trying to connect"
```

---

## 使用示例

- **在手机上使用Aster作为助手**：
```
"Open YouTube and search for cooking videos"
→ aster_launch_intent → aster_click_by_id → aster_input_text

"Find photos from my trip to Mumbai last month"
→ aster_search_media with query "photos from Mumbai last month"

"Take a screenshot and tell me what's on screen"
→ aster_take_screenshot → aster_get_screen_hierarchy
```

- **让AI通过专属手机为你执行操作**：
```
"Call me and tell me my flight is delayed"
→ aster_make_call_with_voice with number, text "Your flight is delayed 45 min, new gate B12", waitSeconds 8

"Text me when my delivery arrives"
→ aster_read_notifications → aster_send_sms with number and message

"Reply to the delivery guy: Thanks, I'll be home"
→ aster_send_sms with number and message
```

---

## 命令列表
```bash
aster start              # Start the server
aster stop               # Stop the server
aster status             # Show server and device status
aster dashboard          # Open web dashboard

aster devices list       # List connected devices
aster devices approve    # Approve a pending device
aster devices reject     # Reject a device
aster devices remove     # Remove a device

aster set-openclaw-callbacks  # Configure event forwarding to OpenClaw
```

---

## 系统要求

- 需要安装Node.js 20及以上版本
- 安装了Aster应用程序的Android设备（可以是你的手机或专门用于AI的设备）
- 设备和服务器必须在同一网络范围内（或使用[Tailscale](https://tailscale.com)实现安全远程访问）

---

**官方网站**：[aster.theappstack.in] | **GitHub仓库**：[github.com/satyajiit/aster-mcp](https://github.com/satyajiit/aster-mcp)
---
name: localsend
description: 使用 LocalSend 协议在附近的设备之间发送和接收文件。当用户需要将文件传输到手机、另一台电脑或本地网络中任何支持 LocalSend 的设备时，或者从这些设备接收文件时，可以使用该协议。
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins:
        - localsend-cli
        - openssl
---
# LocalSend

使用此功能可以通过LocalSend v2协议在本地网络中的设备之间传输文件。该功能支持运行LocalSend应用程序的任何设备（Android、iOS、Windows、macOS、Linux）。

## 交互式模式（Telegram按钮）

当用户通过消息频道触发LocalSend时，使用内联按钮显示一个交互式菜单：

### 主菜单

当用户输入“localsend”、“send files”或类似指令时，以按钮形式显示以下选项：

```
📡 LocalSend
├── [🔍 Discover Devices]  → runs discover, shows device list as buttons
├── [📤 Send File]          → prompts for file path, then shows device picker
├── [📥 Receive Files]      → starts receiver in background, confirms ready
└── [❌ Cancel]             → exits
```

### 发现设备 → 设备选择器流程

1. 运行 `localsend-cli discover --json -t 5`
2. 将JSON输出解析为设备列表
3. 将每个设备显示为可点击的按钮：
   ```
   Found 3 devices:
   [📱 Fast Potato (192.168.0.148)]
   [💻 Rami-Desktop (192.168.0.100)]
   [🖥️ Living Room PC (192.168.0.105)]
   ```
4. 当用户点击某个设备时，将其存储为下次传输的目标设备

### 传输流程（使用按钮）

1. 用户点击 **📤 发送文件** 或输入 “send [文件] to [设备]”
2. 如果没有目标设备缓存 → 运行发现设备功能的命令并显示设备选择器按钮
3. 如果没有指定文件 → 提示：“请将文件发送给我或告诉我文件路径”
4. 传输前进行确认：
   ```
   Send project.zip (4.2 MB) to Fast Potato?
   [✅ Send] [❌ Cancel]
   ```
5. 执行文件传输并报告结果

### 接收流程（使用按钮）

1. 用户点击 **📥 接收文件** 或输入 “开始接收”
2. 在后台启动接收器（详见“后台接收”部分）
3. 确认接收准备就绪：
   ```
   📡 Receiver active as "openclaw-workspace"
   Saving to: ~/incoming/
   Auto-accept: ON

   Send files from your device whenever ready.
   [🛑 Stop Receiver]
   ```
4. **重要提示 — 接收完成后必须立即在聊天中确认**：
   当文件传输完成后，必须在聊天中立即确认传输的详细信息：
   ```
   ✅ Received from Fast Potato:

   📄 portfolio.zip — 240 MB
   📁 Saved to: ~/incoming/portfolio.zip

   [📂 Open/Extract] [🚀 Deploy] [🛑 Stop Receiver]
   ```

   **对于图片** — 使用消息中的媒体路径直接显示图片：
   ```
   ✅ Received from Fast Potato:

   🖼️ screenshot.png — 2.1 MB
   MEDIA:./incoming/screenshot.png

   [📂 Open Folder] [🛑 Stop Receiver]
   ```

   **对于多个文件** — 分别列出每个文件：
   ```
   ✅ Received 3 files from Fast Potato:

   📄 app.apk — 45 MB
   📄 README.md — 2 KB
   🖼️ icon.png — 128 KB
   📁 Saved to: ~/incoming/

   [📂 Show All] [🛑 Stop Receiver]
   ```

### 接收完成后

启动接收器后，**主动监控** 新文件的到来：

1. 在接收器运行期间，每2-3秒检查一次保存目录
2. 比较文件列表以检测新文件
3. 当检测到新文件时：
   - 读取文件元数据（名称、大小、类型）
   - 如果是图片 → 使用媒体路径直接显示图片预览
   - 如果是压缩文件（.zip、.tar.gz） → 提供解压或列出内容的选项
   - 如果是代码/文本文件 → 提供预览前几行的选项
   - 总是显示与文件类型相关的操作按钮
4. 如果接收器进程退出 → 在聊天中确认“接收器已停止”

## 命令

### 发现设备

```bash
localsend-cli discover --json -t 5
```

列出网络中的所有LocalSend设备。使用 `--json` 可以获得可解析的输出，`-t 5` 表示扫描持续5秒。

**解析JSON输出** 以提取设备名称和IP地址用于生成按钮：
```bash
localsend-cli discover --json -t 5 | python3 -c "
import sys, json
for d in json.load(sys.stdin):
    print(f\"{d.get('alias','?')} ({d.get('ip','?')}) [{d.get('deviceType','?')}]\")
"
```

### 发送文件

```bash
localsend-cli send --to "Fast Potato" file1.txt file2.png
```

使用 `--to` 指定目标设备（不区分大小写）。如果不使用 `--to`，则会显示交互式设备选择器（在无界面/代理模式下不适用 — 请始终使用 `--to`）。

### 接收文件

```bash
localsend-cli receive --save-dir ~/incoming -y
```

启动一个HTTPS服务器以接收传入的文件。使用 `-y` 可以自动接受文件传输而无需用户确认。

## 后台接收（非常重要）

接收命令会一直运行，直到被停止。**必须始终在后台运行**，以确保代理程序保持响应状态：

```bash
# Correct — run in background with alias BEFORE subcommand
localsend-cli --alias openclaw-workspace receive --save-dir ~/incoming -y
```

**关键提示：标志的顺序很重要！**
- ✅ `localsend-cli --alias 名称 receive --save-dir 目录 -y`
- ❌ `localsend-cli receive --alias 名称 --save-dir 目录 -y`（失败 — `alias` 是一个全局标志）

在后台运行时：
1. 使用 `run_in_background: true` 或使用执行工具的后台模式
2. 存储会话/任务ID，以便后续停止该任务
3. 监控传输完成情况 — 文件到达后，进程可能会退出或输出日志
4. 当用户点击 **🛑 停止接收器** 时，使用存储的任务ID来停止接收器

## 选项

| 标志 | 作用范围 | 命令 | 描述 |
|------|-------|---------|-------------|
| `--alias 名称` | **全局** | 所有命令 | 要显示的设备名称（默认：主机名）。**必须放在子命令之前** |
| `--to 名称` | 子命令 | 发送 | 指定目标设备名称，跳过交互式设备选择器 |
| `-t, --timeout N` | 子命令 | 发现设备 | 扫描持续时间（以秒为单位，默认：3秒） |
| `--json` | 子命令 | 发现设备 | 生成机器可读的JSON输出 |
| `--save-dir 目录` | 子命令 | 接收文件 | 文件保存路径（默认：~/Downloads） |
| `-y, --yes` | 子命令 | 接收文件 | 自动接受传入的文件传输 |

## 工作流程

### 标准流程（基于文本）

1. 运行 `localsend-cli discover --json -t 5` 以确认目标设备是否可见并获取其名称。
2. 如果未找到目标设备，询问用户确认目标设备上是否已打开LocalSend应用程序，并且设备是否在同一Wi-Fi网络上。
3. 发送文件时，使用 `--to` 指定设备名称 — CLI支持不区分大小写的子字符串匹配。
4. 对于大文件，提醒用户传输可能需要一些时间 — CLI会在传输完成前保持等待状态。
5. 接收文件时，使用 `-y` 在后台运行以支持无人值守操作。

### 推荐流程（基于按钮）

1. 触发命令时显示主菜单按钮
2. 发现设备后，将设备显示为可点击的按钮
3. 用户点击设备后，将其存储为传输目标
4. 用户发送文件或文件路径后，使用“发送”/“取消”按钮进行确认
5. 显示传输进度和结果
6. 接收文件时，在后台启动接收器，并显示“停止”按钮

## 实际应用示例

### 部署网站更新
```
User: "Start receiving, I'm sending the new portfolio"
Agent: Starts receiver → user sends zip via LocalSend app → agent confirms receipt
       "✅ Received: rami-portfolio.zip (240 MB). Ready to deploy?"
       [🚀 Deploy] [📂 Just Save]
```

### 将构建成果发送到手机
```
User: "Send the APK to my phone"
Agent: Discovers devices → shows phone as button → user taps → sends build/app.apk
       "✅ Sent app.apk (45 MB) to Fast Potato"
```

### 批量文件传输
```
User: "Send all the screenshots to my desktop"
Agent: Discovers devices → user picks desktop → sends ~/Screenshots/*.png
       "✅ Sent 12 files (28 MB total) to Rami-Desktop"
```

## 故障排除

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `unrecognized arguments: --alias` | `--alias` 位于子命令之后 | 将 `--alias` 放在 `receive`/`send`/`discover` 之前 |
| 端口53317已被占用 | 同一台机器上运行了LocalSend图形界面 | CLI会自动切换到端口53318/53319 — 这是正常的 |
| 未找到设备 | 目标设备不在同一Wi-Fi网络上或应用程序已关闭 | 请用户打开LocalSend应用程序并保持屏幕开启 |
| 传输被拒绝（403） | 接收器在用户界面中拒绝了传输 | 在接收器上使用 `-y`，或请求用户接受传输 |
| 正在传输中（409） | 另有一个正在进行的传输任务 | 等待当前传输完成 |
| 传输卡住 | 文件较大且Wi-Fi网络速度较慢 | 请耐心等待 — 默认情况下没有传输超时限制。对于大于100MB的文件，请提醒用户 |

## 参考资料

请阅读 `references/protocol.md` 以获取完整的LocalSend v2协议详细信息。
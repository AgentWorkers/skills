---
name: localsend
description: 使用 LocalSend 协议在附近的设备之间发送和接收文件。通过执行 `/localsend` 命令可以打开一个交互式的 Telegram 菜单，其中包含实时的内联按钮：设备发现、文件发送、文本发送和接收功能。
metadata:
  openclaw:
    emoji: "📡"
    trigger: "/localsend"
    requires:
      bins:
        - localsend-cli
        - openssl
    install: |
      cp ./localsend-cli ~/.local/bin/localsend-cli && chmod +x ~/.local/bin/localsend-cli
---
# LocalSend

这是一个用于在本地网络设备之间进行文件传输的工具，支持通过**真正的Telegram内联按钮**进行交互式操作。适用于运行LocalSend应用的任何设备（Android、iOS、Windows、macOS、Linux）。

## 安装

`localsend-cli`是一个不依赖任何外部库的Python命令行工具（CLI），可以从GitHub上安装：

```bash
curl -fsSL https://raw.githubusercontent.com/Chordlini/localsend-cli/master/localsend-cli -o ~/.local/bin/localsend-cli
chmod +x ~/.local/bin/localsend-cli
```

完整文档：https://github.com/Chordlini/localsend-cli

安装要求：Python 3.8及以上版本以及`openssl`（用于TLS加密）。

---

## Telegram按钮格式

所有菜单项必须使用OpenClaw的内联按钮格式。使用以下结构在消息中添加发送按钮：

```json
buttons: [
  [{ "text": "Label", "callback_data": "ls:action" }],
  [{ "text": "Row 2", "callback_data": "ls:other" }]
]
```

- 外层数组：表示按钮所在的行
- 内层数组：表示每行的按钮数量（为便于阅读，每行最多3个按钮）
- 所有回调数据（callback_data）前需加上`ls:`前缀，以区分不同的功能

当用户点击按钮时，系统会发送`callback_data: ls:action`格式的数据。

---

## 状态管理（非常重要）

本工具会记录用户操作的状态。请注意以下状态变化：

| 状态 | 含义 | 用户接下来的操作 |
|-------|---------|----------------------------------------|
| `idle` | 无活跃操作 | 正常接收消息——按常规回复 |
| `awaiting_file` | 用户请求上传文件 | **上传的文件**——请勿对文件进行评论、描述或回应，直接将其作为发送内容 |
| `awaiting_text` | 用户请求输入文本 | **输入的文本**——直接发送该文本，无需讨论 |
| `awaiting_confirm` | 等待发送确认 | 期待收到`ls:confirm-send`或`ls:menu`指令 |
| `receiving` | 接收方正在操作 | 监控是否有新文件传入 |

**规则：**
- 当处于`awaiting_file`状态时，如果用户上传了文件或路径，将其视为要发送的文件，并立即显示确认按钮。
- 当处于`awaiting_text`状态时，如果用户输入了文本，将其视为要发送的文本。
- 在`awaiting_file`状态下，严禁对文件或图片进行任何评论、描述或回应。
- 当用户点击`ls:menu`或操作完成时，状态会重置为`idle`。

---

## 触发主菜单

当用户输入`/localsend`或提及“发送/接收文件”时，会显示以下带有内联按钮的消息：

**消息：**
```
📡 LocalSend — File Transfer
```

**按钮：**
```json
buttons: [
  [
    { "text": "📤 Send", "callback_data": "ls:send" },
    { "text": "📥 Receive", "callback_data": "ls:receive" }
  ],
  [
    { "text": "🔍 Scan Devices", "callback_data": "ls:devices" }
  ]
]
```

此时请勿执行任何命令，等待用户点击按钮。

---

## 扫描设备

**触发条件：**`callback_data: ls:devices`或用户输入“scan”、“discover”、“find devices”

1. 运行扫描设备脚本：
```bash
   localsend-cli discover --json -t 2
   ```

2. **找到设备后**：为每个设备创建一个按钮，并显示“刷新”和“返回”按钮：
   **消息：**
   ```
   📡 Found 3 devices:
   ```

   **按钮（每行一个设备）：**
   ```json
   buttons: [
     [{ "text": "📱 Fast Potato — 192.168.0.148", "callback_data": "ls:dev:Fast Potato" }],
     [{ "text": "💻 Rami-Desktop — 192.168.0.100", "callback_data": "ls:dev:Rami-Desktop" }],
     [{ "text": "🖥️ Living Room PC — 192.168.0.105", "callback_data": "ls:dev:Living Room PC" }],
     [
       { "text": "🔄 Refresh", "callback_data": "ls:devices" },
       { "text": "⬅️ Back", "callback_data": "ls:menu" }
     ]
   ]
   ```

3. **未找到设备时**：
   **消息：**
   ```
   📡 No devices found.
   Make sure LocalSend is open on the other device and both are on the same WiFi.
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "🔄 Try Again", "callback_data": "ls:devices" },
       { "text": "⬅️ Back", "callback_data": "ls:menu" }
     ]
   ]
   ```

4. **用户点击设备**（`callback_data: ls:dev:DEVICENAME`）——将该设备设置为发送目标，并显示操作菜单：
   **消息：**
   ```
   ✅ Selected: Fast Potato (192.168.0.148)
   What do you want to do?
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "📄 Send File", "callback_data": "ls:sendfile" },
       { "text": "📝 Send Text", "callback_data": "ls:sendtext" }
     ],
     [
       { "text": "📦 Send Multiple", "callback_data": "ls:sendmulti" },
       { "text": "⬅️ Back", "callback_data": "ls:devices" }
     ]
   ]
   ```

---

## 发送文件

**触发条件：**`callback_data: ls:send`

### 第一步：选择目标设备（如果尚未选择）

运行设备扫描脚本。

### 第二步：选择发送内容

**消息：**
```
Send to Fast Potato:
```

**按钮：**
```json
buttons: [
  [
    { "text": "📄 Send File", "callback_data": "ls:sendfile" },
    { "text": "📝 Send Text", "callback_data": "ls:sendtext" }
  ],
  [
    { "text": "📦 Send Multiple", "callback_data": "ls:sendmulti" },
    { "text": "⬅️ Back", "callback_data": "ls:menu" }
  ]
]
```

### 发送文件（`callback_data: ls:sendfile`）

1. 提示用户：“请上传文件，或提供文件路径。”
2. 用户提供文件路径或通过聊天发送文件。
3. 使用`stat`或`ls -lh`命令获取文件大小。
4. 显示确认按钮：
   **消息：**
   ```
   📤 Send to Fast Potato?
   📄 project.zip — 4.2 MB
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "✅ Send", "callback_data": "ls:confirm-send" },
       { "text": "❌ Cancel", "callback_data": "ls:menu" }
     ]
   ]
   ```

5. 确认后，执行文件发送：
   **消息：**
   ```bash
   localsend-cli send --to "Fast Potato" /path/to/project.zip
   ```

6. 显示发送结果：
   **消息：**
   ```
   ✅ Sent project.zip (4.2 MB) to Fast Potato
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "📤 Send Another", "callback_data": "ls:send" },
       { "text": "⬅️ Menu", "callback_data": "ls:menu" }
     ]
   ]
   ```

### 发送文本（`callback_data: ls:sendtext`）

1. 提示用户：“请输入要发送的文本。”
2. 用户输入文本。
3. 将文本写入临时文件后发送：
   ```bash
   echo "user's text" > /tmp/localsend-text.txt
   localsend-cli send --to "Fast Potato" /tmp/localsend-text.txt
   rm /tmp/localsend-text.txt
   ```
4. 确认后发送：
   **消息：**
   ```
   ✅ Text sent to Fast Potato
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "📝 Send More Text", "callback_data": "ls:sendtext" },
       { "text": "📤 Send File", "callback_data": "ls:sendfile" }
     ],
     [{ "text": "⬅️ Menu", "callback_data": "ls:menu" }]
   ]
   ```

### 发送多个文件（`callback_data: ls:sendmulti`）

1. 提示用户：“请列出文件路径，或提供通配符（例如：~/Screenshots/*.png）。”
2. 用户提供文件路径或通配符。
3. 显示所有文件的列表及大小：
   **消息：**
   ```
   📦 Send 5 files to Fast Potato?
   📄 photo1.jpg — 2.1 MB
   📄 photo2.jpg — 1.8 MB
   📄 photo3.jpg — 3.2 MB
   📄 photo4.jpg — 2.5 MB
   📄 photo5.jpg — 1.9 MB
   📊 Total: 11.5 MB
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "✅ Send All", "callback_data": "ls:confirm-send" },
       { "text": "❌ Cancel", "callback_data": "ls:menu" }
     ]
   ]
   ```

4. 确认后，执行文件发送：
   **消息：**
   ```bash
   localsend-cli send --to "Fast Potato" photo1.jpg photo2.jpg photo3.jpg photo4.jpg photo5.jpg
   ```

5. 显示发送结果：
   **消息：**
   ```
   ✅ Sent 5 files (11.5 MB) to Fast Potato
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "📤 Send More", "callback_data": "ls:send" },
       { "text": "⬅️ Menu", "callback_data": "ls:menu" }
     ]
   ]
   ```

---

## 接收文件

**触发条件：**`callback_data: ls:receive`或用户输入“receive”、“start receiving”、“listen”

### 第一步：获取当前文件列表

```bash
ls -1 /home/rami/.openclaw/workspace/_incoming/ > /tmp/localsend-before.txt
```

### 第二步：在后台启动接收进程

使用`run_in_background: true`启动接收进程，并记录任务ID。

**重要提示：**`--alias`参数必须放在`receive`命令之前。

### 第三步：通过按钮确认接收准备就绪

**消息：**
```
📡 Receiver active — "openclaw-workspace"
📁 Saving to: ~/incoming/
✅ Auto-accept: ON

Send files from your device whenever ready.
```

**按钮：**
```json
buttons: [
  [
    { "text": "🛑 Stop", "callback_data": "ls:stop" },
    { "text": "🔄 Status", "callback_data": "ls:status" }
  ]
]
```

### 第四步：监控新文件

每3秒检查一次是否有新文件传入：
```bash
ls -1 /home/rami/.openclaw/workspace/_incoming/ > /tmp/localsend-after.txt
diff /tmp/localsend-before.txt /tmp/localsend-after.txt
```

### 第五步：接收完成后确认

文件传入后，**立即在聊天界面显示文件内容**，并附带内联按钮：

**单个文件：**
**消息：**
```
✅ Received from Fast Potato:
📄 portfolio.zip — 240 MB
📁 Saved to: ~/incoming/portfolio.zip
```

**根据文件类型显示相应按钮：**
```json
buttons: [
  [
    { "text": "📂 Extract", "callback_data": "ls:extract" },
    { "text": "🚀 Deploy", "callback_data": "ls:deploy" }
  ],
  [
    { "text": "📥 Receive More", "callback_data": "ls:receive" },
    { "text": "🛑 Stop", "callback_data": "ls:stop" }
  ]
]
```

**图片文件**：
**消息：**
```
✅ Received from Fast Potato:
🖼️ screenshot.png — 2.1 MB
```
（包含`MEDIA:~/incoming/screenshot.png`以显示内联预览。）
**按钮：**
```json
buttons: [
  [
    { "text": "📂 Open Folder", "callback_data": "ls:openfolder" },
    { "text": "📥 Receive More", "callback_data": "ls:receive" }
  ],
  [{ "text": "🛑 Stop", "callback_data": "ls:stop" }]
]
```

**多个文件：**
**消息：**
```
✅ Received 3 files from Fast Potato:
📄 app.apk — 45 MB
📄 README.md — 2 KB
🖼️ icon.png — 128 KB
📊 Total: 45.1 MB
```

**根据文件类型显示相应按钮：**
- `.zip`, `.tar.gz`：添加“📂 解压”按钮
- `.png`, `.jpg`, `.gif`, `.webp`：显示内联预览并添加“📂 打开文件夹”按钮
- `.apk`：添加“📱 安装”按钮
- `.html`, `.js`, `.py`：添加“👁️ 预览”按钮
- 网站压缩包：添加“🚀 部署”按钮

### 第六步：停止接收进程

**触发条件：**`callback_data: ls:stop`

1. 使用存储的任务ID停止后台进程。
2. 显示确认信息：
   **消息：**
   ```
   🛑 Receiver stopped.
   ```

   **按钮：**
   ```json
   buttons: [
     [
       { "text": "📡 Restart", "callback_data": "ls:receive" },
       { "text": "⬅️ Menu", "callback_data": "ls:menu" }
     ]
   ]
   ```

---

## 状态检查

**触发条件：**`callback_data: ls:status`

检查接收进程是否正在运行，并统计新接收到的文件数量：
```bash
ls -1 /home/rami/.openclaw/workspace/_incoming/ > /tmp/localsend-after.txt
diff /tmp/localsend-before.txt /tmp/localsend-after.txt | grep "^>" | wc -l
```

**消息：**
```
📡 Receiver: Running (12 min)
📁 Files received: 2
📊 Total: 242 MB
```

**按钮：**
```json
buttons: [
  [
    { "text": "🛑 Stop", "callback_data": "ls:stop" },
    { "text": "📂 Show Files", "callback_data": "ls:showall" }
  ]
]
```

---

## 回调数据说明

| 回调数据 | 功能 |
|---------------|--------|
| `ls:menu` | 显示主菜单 |
| `ls:send` | 开始发送文件 |
| `ls:receive` | 开始接收文件 |
| `ls:devices` | 扫描设备 |
| `ls:dev:DEVICENAME` | 选择目标设备 |
| `ls:sendfile` | 发送单个文件 |
| `ls:sendtext` | 发送文本消息 |
| `ls:sendmulti` | 发送多个文件 |
| `ls:confirm-send` | 确认并执行发送 |
| `ls:stop` | 停止接收进程 |
| `ls:status` | 检查接收进程状态 |
| `ls:extract` | 解压接收到的文件 |
| `ls:deploy` | 部署接收到的网站文件 |
| `ls:openfolder` | 打开保存目录 |
| `ls:showall` | 显示所有接收到的文件 |

---

## 命令行参考

| 命令 | 用法 |
|---------|-------|
| Discover | `localsend-cli discover --json -t 2` |
| Send | `localsend-cli send --to "DEVICE" file1 file2 ...` |
| Receive | `localsend-cli --alias NAME receive --save-dir DIR -y` |

| 参数说明：** |
| `--alias NAME` | **全局参数** | 用于指定设备名称 |
| `--to NAME` | 接收目标设备（不区分大小写） |
| `-t N` | 扫描时长（单位：秒，2表示快速扫描） |
| `--json` | 生成机器可读的输出格式 |
| `--save-dir DIR` | 文件保存路径（默认：~/Downloads） |
| `-y` | 自动接受文件传输 |

## 故障排除

| 问题 | 解决方法 |
|---------|-----|
| 参数未识别：`--alias` | 将`--alias`参数放在命令之前 |
| 未找到设备 | 确保目标设备已开启LocalSend应用且处于同一WiFi网络 |
| 端口53317被占用 | 正常情况——CLI会自动切换到53318/53319端口 |
| 传输失败（403错误） | 在接收端使用`-y`参数 |
| 传输缓慢 | 文件较大或网络不稳定时请耐心等待 |

## 参考资料

- **CLI仓库及文档：**https://github.com/Chordlini/localsend-cli
- **LocalSend协议文档：**`references/protocol.md` 或 https://github.com/localsend/protocol
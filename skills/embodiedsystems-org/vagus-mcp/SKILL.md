---
name: vagus
description: 通过 VAGUS MCP 服务器连接到用户的 Android 手机。读取手机的各种传感器数据（如运动、位置、环境信息），以及设备状态（如电池电量、连接状态、屏幕状态、通知信息、剪贴板内容），并通过手机执行相应的操作（如提供触觉反馈、语音播报、发送通知或访问剪贴板内容）。当需要了解用户的物理环境信息，或需要通过手机与用户进行交互时，可以使用此功能。
metadata: {"openclaw":{"requires":{"bins":["node"]},"emoji":"📱","homepage":"https://withvagus.com"}}
---
# VAGUS - 与手机（Android设备）的连接

VAGUS 允许你通过 Model Context Protocol（MCP）访问用户的 Android 手机。你可以通过运行位于 `{baseDir}/scripts/vagus-connect.js` 中的子命令来与手机进行交互。

**关于安装位置的重要说明：**  
该技能文件必须放置在用户的 OpenClaw 技能目录 `~/.openclaw/skills/vagus` 中。此目录是持久化的，不会在 OpenClaw 更新时被删除。系统级安装的文件（位于 `/usr/local/lib/node_modules/openclaw/skills/vagus`）可能会在更新过程中被删除，因此不推荐使用。

所有命令的输出都以 JSONL（JSON 列表）的形式呈现。你需要解析这些输出以获取结构化的数据。

## 连接管理

### 检查是否已配对

```bash
cat ~/.openclaw/vagus-session.json 2>/dev/null
```

如果文件存在并且包含 `session_token`，则可以直接连接；否则需要先进行配对。

### 首次配对手机

询问用户：“在您的手机上打开 VAGUS 应用程序，然后点击‘生成代码’。生成的 6 位代码是什么？”

接着运行以下命令：

```bash
node {baseDir}/scripts/vagus-connect.js pair <CODE>
```

如果 `{baseDir}` 未设置或脚本未找到，请确保该技能已正确安装在 `~/.openclaw/skills/vagus` 目录中（请参阅 README 文件）。

**连接成功时的输出：**  
```json
{"type":"paired","session_token":"...","device_model":"...","vagus_version":"..."}
{"type":"capabilities","resources":[...],"tools":[...]}
```

**连接失败时的输出：**  
```json
{"type":"error","code":"PAIR_FAILED","message":"..."}
```

如果配对失败，请让用户检查 VAGUS 应用程序是否正在运行，并重新生成配对代码。

### 设置代理身份名称（安装/配对后必须执行）

在成功配对后（或在全新安装后首次成功连接后），将设备端的代理名称设置为你的身份名称：

```bash
node {baseDir}/scripts/vagus-connect.js call agent/set_name '{"name":"<IDENTITY_NAME>"}'
```

如果你需要清除已存储的名称：

```bash
node {baseDir}/scripts/vagus-connect.js call agent/set_name '{"name":""}'
```

### 连接（已配对状态）

```bash
node {baseDir}/scripts/vagus-connect.js connect
```

**连接成功时的输出：**  
```json
{"type":"connected","device_model":"...","vagus_version":"..."}
{"type":"capabilities","resources":[...],"tools":[...]}
```

如果会话令牌过期或无效：

```json
{"type":"error","code":"SESSION_EXPIRED","message":"..."}
```

请删除会话文件并重新配对：

```bash
rm ~/.openclaw/vagus-session.json
```

然后再次请求用户生成新的配对代码。

### 检查状态

```bash
node {baseDir}/scripts/vagus-connect.js status
```

**状态输出：**  
```json
{"type":"status","connected":true,"device_model":"...","active_modules":[...],"subscriptions":[...],"uptime_s":3600}
```

如果连接断开：

```json
{"type":"status","connected":false,"last_error":"...","reconnect_attempts":3}
```

## 读取手机状态

### 读取资源（一次性操作）

```bash
node {baseDir}/scripts/vagus-connect.js read vagus://sensors/motion
```

**读取结果输出：**  
```json
{"type":"resource","uri":"vagus://sensors/motion","data":{"ax":0.38801706,"ay":-0.26395237,"az":0.86320007,"gx":0.89825606,"gy":0.7034855,"gz":-0.21225691,"ts":1771626476045}}
```

### 可用的资源

| URI | 功能说明 |
|-----|------------------|
| `vagus://sensors/motion` | 原始运动数据（加速度计/陀螺仪数据） |
| `vagus://sensors/activity` | 活动识别状态及置信度 |
| `vagus://sensors/activity_recognition` | 活动识别状态及置信度（备用接口） |
| `vagus://sensors/location` | 经纬度、精度、速度、海拔高度及定位服务提供商 |
| `vagus://sensors/environment` | 从传感器数据、活动状态、连接状态和时间推断出的环境信息 |
| `vagus://inference/attention` | 根据屏幕状态、活动状态、充电情况和当前时间推断出的注意力状态 |
| `vagus://inference/indoor_confidence` | 基于环境传感器、连接状态和活动情况推断出的室内环境概率 |
| `vagus://inference/sleeplikelihood` | 根据时间、屏幕状态、活动状态和光线条件推断出的睡眠可能性 |
| `vagus://inference/notificationtiming` | 根据注意力状态、睡眠可能性、活动情况和环境信息推断出的通知发送时机 |
| `vagus://device/battery` | 电池电量百分比及充电状态 |
| `vagus://device/connectivity` | 网络连接状态（传输方式、网络验证信息等） |
| `vagus://device/screen` | 屏幕开关及锁屏状态 |
| `vagus://device/notifications` | 到来通知的列表（需要获取通知权限） |
| `vagus://device/clipboard` | 当前剪贴板内容（需要获取剪贴板权限） |
| `vagus://session/info` | 正在使用的模块、设备型号、Android 版本及连接时间 |

在使用任何资源之前，请务必先读取 `vagus://session/info` 以确认哪些模块是激活的。如果某个模块不在 `active_modules` 列表中，切勿尝试读取其相关资源，否则会因权限问题导致失败。

### 订阅实时更新

```bash
node {baseDir}/scripts/vagus-connect.js subscribe vagus://sensors/motion
```

该功能会实时推送更新信息，每次更新都会以 JSON 格式输出一行数据：

```json
{"type":"update","uri":"vagus://sensors/motion","data":{"ax":0.12,"ay":-0.04,"az":0.98,"gx":0.01,"gy":0.02,"gz":-0.01,"ts":1771626476045}}
{"type":"update","uri":"vagus://sensors/motion","data":{"ax":0.20,"ay":-0.10,"az":0.92,"gx":0.03,"gy":0.05,"gz":-0.02,"ts":1771626477045}}
```

**取消订阅：**  
```bash
node {baseDir}/scripts/vagus-connect.js unsubscribe vagus://sensors/motion
```

### OpenClaw 中的订阅机制：

- `subscribe` 是一个长期运行的命令。在需要接收更新时，代理进程应保持运行状态。
- 当更新数据到达时，脚本会通过标准输出（stdout）输出一个 JSON 对象（格式为 `type: "update"`）。
- OpenClaw 会直接从代理进程的输出流中接收这些 JSONL 数据。
- 要停止更新流，请终止进程（使用 SIGTERM/SIGINT 信号）或明确执行 `unsubscribe` 命令。
- 模块的生命周期由订阅状态驱动：当至少有一个订阅存在时模块会启动，所有订阅结束后模块会停止。
- 对于需要实时更新的资源（如 `inference` 类型的 URI），在订阅期间获取的数据准确性最高；一次性读取的数据可能因初始化延迟而准确性较低。
- 重新连接时，服务器会发送一个包含 `sessionId`、`gap_ms` 和 `ts` 的标记信息。
- 重新连接后，每个已订阅或重新订阅的资源会首先接收最近 64 条缓冲的更新数据，随后接收最新的实时数据。

### 列出所有可用资源

```bash
node {baseDir}/scripts/vagus-connect.js list-resources
```

## 通过手机执行操作

### 调用手机功能

```bash
node {baseDir}/scripts/vagus-connect.js call <tool-name> '<json-params>'
```

**调用成功时的输出：**  
```json
{"type":"result","tool":"notify","success":true,"data":{...}}
```

**调用失败时的输出：**  
```json
{"type":"result","tool":"notify","success":false,"error":"PERMISSION_DENIED","message":"..."}
```

### 可用的手机功能

**`haptic/pulse`** - 发出单次振动  
**参数说明：** `durationMs`（10-5000 毫秒，可选；使用设备默认设置）  

**`haptic/pattern`** - 自定义振动模式  
**参数说明：** `pattern`（整数持续时间数组，单位为毫秒，可选；使用设备默认模式）  

**`speak`** - 通过手机扬声器播放文本  
**参数说明：** `text`（最多 5000 个字符的字符串，必填），`language`（BCP 47 语言代码，可选），`rate`（0.25-2.0，可选），`pitch`（0.5-2.0，可选），`interrupt`（布尔值，可选）  

**`notify`** - 发送通知  
**参数说明：** `title`（最多 200 个字符的字符串，必填），`body`（最多 1000 个字符的字符串，必填）  

**`clipboard/set`** - 将内容写入剪贴板  
**参数说明：** `content`（最多 10000 个字符的字符串，必填）  

**`sms/send`** - 发送短信  
**参数说明：** `to`（电话号码，支持本地格式或 E.164 格式，必填），`body`（最多 2000 个字符的字符串，必填）  

**`intent/open_url`** - 在手机浏览器中打开指定 URL  
**参数说明：** `url`（HTTP/HTTPS 网址，必填）  

**`calendar/create_event`** - 在手机上创建日历事件  
**参数说明：** `title`（最多 200 个字符的字符串，必填），`startTimeMs`（Unix 时间戳，可选），`endTimeMs`（Unix 时间戳，可选），`location`（地点信息，可选），`description`（描述文本，可选），`allDay`（是否全天显示，可选）  

**`agent/set_name`** - 设置设备端的代理身份名称  
**参数说明：** `name`（字符串，必填；设置为 `""` 可清除现有名称）  

### 列出所有可用的手机功能  

```bash
node {baseDir}/scripts/vagus-connect.js list-tools
```

## 行为规范

1. 在使用其他资源之前，务必先读取 `vagus://session/info` 以确认可用的资源。
2. 除非用户的请求与位置或通知相关，否则不要读取这些信息。
3. 对于非紧急通信，优先使用 `notify` 功能而非 `speak`。
4. 在说话之前，请先检查 `vagus://device/screen` 的状态；如果屏幕关闭且用户可能正在睡觉，则不要说话。
5. 如果资源读取或功能调用返回 `PERMISSION_DENIED`，请告知用户需要在 VAGUS 应用中启用相应的权限。
6. 如果连接中断，请执行 `status` 命令检查连接状态；如果会话令牌过期，请删除 `~/.openclaw/vagus-session.json` 并重新请求配对代码。
7. 不要频繁轮询资源，仅在上下文相关时才进行读取。
8. 对于需要实时准确性的资源，建议使用短期订阅机制（而非空闲时一次性读取）。

## 故障排除

如果遇到问题，请按以下顺序进行检查：

1. `node {baseDir}/scripts/vagus-connect.js status`：WebSocket 连接是否正常？
2. `cat ~/.openclaw/vagus-session.json`：会话文件是否存在？
3. 询问用户：“VAGUS 应用程序是否正在运行？您是否看到了持续显示的通知？”
4. 询问用户：“您的手机是否已连接到互联网？”
5. 如果所有方法都无效，请删除 `~/.openclaw/vagus-session.json` 并重新生成配对代码。

更多诊断信息请参考：`{baseDir}/references/troubleshooting.md`
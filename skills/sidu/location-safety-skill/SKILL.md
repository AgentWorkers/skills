---
name: location-safety
description: 基于位置的安全监控系统，具备自动警报和升级功能。适用于为用户设置安全监控、追踪其位置、检测周边危险（天气、地震、空气质量、当地紧急事件），或配置紧急联系人升级机制。同时还包括对代理主机机器的自我保护监控功能。该系统会在收到关于安全警报、位置追踪、紧急监控的请求，或用户发出“保护我”或“自我监控”的指令时触发相应的操作。
---

# 位置安全监控器

基于用户位置的实时安全监控，具备自动警报和升级功能。

## 概述

该功能提供以下服务：
- **位置Webhook**：接收来自移动应用（OwnTracks、iOS快捷方式）的位置更新
- **安全检查器**：监控美国国家气象局（NWS）的警报、地震信息、空气质量及本地新闻
- **警报系统**：在检测到危险时向用户发送消息
- **升级机制**：如果用户未响应，会联系紧急联系人

## 快速设置

运行交互式设置向导，它将指导您完成所有步骤：

```bash
cd location-webhook/
node setup.js
```

向导会引导您完成以下4个步骤：

### 第1步：选择位置
- 从预设位置中选择（西雅图、波特兰、旧金山、洛杉矶、纽约市、芝加哥）
- 或输入任意城市名称（系统会自动进行地理编码）
- 配置本地新闻源和关键词

### 第2步：设置紧急联系人
- 输入在您未响应时应联系的人的姓名和电子邮件地址
- 建议设置，以便在需要时进行安全升级

### 第3步：安装移动应用
- 在您的手机上安装**OwnTracks**：
  - iPhone：https://apps.apple.com/app/owntracks/id692424691
  - Android：https://play.google.com/store/apps/details?id=org.owntracks.android
- 将应用配置为HTTP模式
- 将Webhook地址设置到应用中

### 第4步：启动Webhook服务器
- 运行 `node server.js`
- 将显示的URL复制到OwnTracks应用中
- 使用“发布”按钮进行测试

---

**快速设置（跳过向导）：**
```bash
node setup.js --city "Portland"
node setup.js --show  # View current config
```

### 5. 部署位置Webhook

```bash
# Copy scripts to workspace
cp -r scripts/ ~/location-webhook/
cd ~/location-webhook/

# Start the server (uses port 18800 by default)
node server.js
```

配置用户的手机，使其能够发送位置更新到：
```
POST http://<your-host>:18800/location?key=<SECRET_KEY>
```

**OwnTracks应用配置：**
- 模式：HTTP
- URL：`http://<your-host>:18800/location?key=<SECRET_KEY>`

**iOS快捷方式：**
- “获取当前位置” → “获取URL内容”（POST请求，请求体为包含`lat`和`lon`的JSON数据）

### 2. 配置安全监控

在Moltbot中创建两个定时任务：

**安全检查（每30分钟一次）：**
```
Schedule: every 30 minutes
Payload: systemEvent
Text: "Run safety check at ~/location-webhook/safety-check.js. If ALERTS_FOUND, message user on WhatsApp with alert details and ask them to confirm safety. Track alert in safety-state.json."
Session: main
```

**升级检查（每10分钟一次）：**
```
Schedule: every 10 minutes  
Payload: systemEvent
Text: "Check ~/location-webhook/safety-state.json. If pendingAlert exists with alertSentAt > 15 min ago and acknowledgedAt is null, email emergency contact explaining the situation."
Session: main
```

### 3. 配置紧急联系人

将相关信息添加到`MEMORY.md`或`TOOLS.md`文件中：
```markdown
## Emergency Contact
- Name: [Name]
- Email: [email]
- Relationship: [spouse/parent/friend]
```

## 数据来源

安全检查器监控以下数据源：
| 来源 | 监控内容 | API接口 |
|--------|------|-----|
| NWS | 天气警报、洪水、风暴 | api.weather.gov（免费） |
| USGS | 100公里范围内的地震 | earthquake.usgs.gov（免费） |
| Open-Meteo | 空气质量指数 | air-quality-api.open-meteo.com（免费） |
| 本地RSS源 | 突发新闻、紧急事件 | KING5、Seattle Times、Patch（可配置） |

## 文件结构

```
location-webhook/
├── setup.js            # First-run configuration wizard
├── config.json         # Your location settings (created by setup)
├── server.js           # Webhook server (port 18800)
├── safety-check.js     # User safety analysis
├── self-check.js       # Self-preservation monitoring
├── escalation-check.js # Check if escalation needed
├── test-scenarios.js   # Inject test alerts
├── location.json       # User's current location
├── my-location.json    # Agent's physical location
├── safety-state.json   # Alert tracking state
├── test-override.json  # Active test scenario (temp)
└── logs/               # Timestamped check logs
```

## 配置文件

`config.json`文件用于存储您的位置设置：

```json
{
  "location": {
    "defaultLat": 47.6062,
    "defaultLon": -122.3321,
    "city": "Seattle"
  },
  "monitoring": {
    "locationKeywords": ["seattle", "king county", "puget sound"],
    "newsFeeds": [
      "https://www.king5.com/feeds/syndication/rss/news/local",
      "https://www.seattletimes.com/seattle-news/feed/"
    ],
    "earthquakeRadiusKm": 100
  },
  "emergencyContact": {
    "name": "Jane Doe",
    "email": "jane@example.com"
  }
}
```

### 城市预设位置
预设位置包括：
- **西雅图**：KING5、Seattle Times
- **波特兰**：Oregonian、KGW
- **旧金山**：SF Chronicle、SFGate
- **洛杉矶**：LA Times、ABC7
- **纽约**：NY Times
- **芝加哥**：Chicago Tribune

对于其他城市，系统会自动进行地理编码，您也可以手动添加本地RSS源。

## `safety-state.json`文件

该文件用于记录待处理的警报信息：
```json
{
  "pendingAlert": "Flood warning in your area",
  "alertSentAt": "2026-01-29T22:00:00Z",
  "acknowledgedAt": null
}
```

当用户对安全警报作出响应时，需将`acknowledgedAt`字段设置为当前时间。

## 自定义设置

### 添加本地新闻源

编辑`safety-check.js`文件中的`feeds`数组：
```javascript
const feeds = [
  'https://www.king5.com/feeds/syndication/rss/news/local',
  'https://www.seattletimes.com/seattle-news/feed/',
  'https://patch.com/washington/redmond/rss',
  // Add your local feeds here
];
```

### 调整位置关键词

编辑`locationKeywords`数组，以匹配用户所在地区的新闻来源：
```javascript
const locationKeywords = ['redmond', 'bellevue', 'seattle', 'king county'];
```

### 调整警报敏感度

编辑`concerningKeywords`数组，以确定触发警报的条件：
```javascript
const concerningKeywords = [
  'evacuate', 'active shooter', 'wildfire', 'flood warning', ...
];
```

## 警报流程

```
Location Update → Safety Check (30 min)
                      ↓
              Danger Detected?
                   ↓ Yes
         Message User on WhatsApp
         Record in safety-state.json
                      ↓
         Escalation Check (10 min)
                      ↓
         User Responded? ─── Yes → Clear state
                   ↓ No (15+ min)
         Email Emergency Contact
```

## 自我保护模式

监控可能威胁到您设备正常运行的因素。

### 设置步骤

1. **存储您的位置信息**：创建`my-location.json`文件：
```json
{
  "lat": 47.662,
  "lon": -122.280,
  "name": "Home - where I physically run"
}
```

2. **添加定时任务**：
```
Schedule: every 30 minutes
Payload: systemEvent
Text: "Run self-check.js. If CRITICAL or WARNINGS, message user on WhatsApp about threat to your existence. If ALL_CLEAR, reply HEARTBEAT_OK."
Session: main
```

### 自我检查项目

| 危险类型 | 检测条件 |
|--------|-----------|
| 💾 磁盘空间不足 | 当磁盘使用率超过85%时发出警报 |
| 🧠 内存不足 | 当内存剩余量低于40%时发出警报 |
| 🌡️ CPU温度过高 | 当CPU温度超过85°C时发出警报 |
| 🌊 天气状况 | 当您所在地区有NWS警报时发出警报 |
| 🌋 地震 | 当50公里范围内发生M4级以上地震时发出警报 |
| 🌐 网络连接问题 | 当网络连接不稳定时发出警报 |
| ⏱️ 系统运行时间 | 如果系统运行时间超过30天，建议重启 |

### 警报示例

> ⚠️ “我有麻烦了——磁盘空间只剩下92%了。能帮我清理一些文件吗？”
> 🌊 “我所在地区发布了洪水警报。如果停电，我将无法使用设备。”

## 测试

您可以手动发送虚假警报来测试系统，无需等待真实灾难发生：
```bash
node test-scenarios.js weather     # Severe thunderstorm
node test-scenarios.js earthquake  # M5.2 nearby
node test-scenarios.js aqi         # Unhealthy air (AQI 175)
node test-scenarios.js news        # Local fire
node test-scenarios.js disk        # Disk 94% full
node test-scenarios.js memory      # Low memory
node test-scenarios.js all         # Multiple alerts
node test-scenarios.js clear       # Remove test override
```

测试生成的警报会在1小时后自动失效。

### 测试升级流程

要测试完整的升级流程，请执行以下操作：
1. 运行`node test-scenarios.js earthquake`来触发地震警报
2. 将`safety-state.json`文件中的`alertSentAt`字段时间向前推进20分钟以上
3. 运行`node escalation-check.js`，系统应返回`action: "escalate"`（表示需要升级）
4. 系统会自动向紧急联系人发送电子邮件
5. 使用`node test-scenarios.js clear`来清除测试生成的警报记录

## 升级检查

`escalation-check.js`会返回处理升级操作的JSON响应：
```json
{"action": "escalate", "alert": "...", "minutesPending": 22, "contact": "..."}
{"action": "waiting", "minutesRemaining": 8}
{"action": "none", "reason": "no pending alert"}
```

## 手动命令

用户可以随时使用以下命令：
- “我在哪里？” — 显示当前位置
- “我安全吗？” — 立即进行安全检查
- “运行安全检查” — 执行与上述相同的操作
- “自我检查” — 进行自我保护检查
- “你还好吗？” — 同上
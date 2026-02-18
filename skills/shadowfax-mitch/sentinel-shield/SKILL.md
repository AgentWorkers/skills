---
name: sentinel-shield
description: OpenClaw代理的运行时安全性：监控工具调用、实施速率限制、检测提示注入行为，并对可疑活动发出警报。保护您的网关令牌和代理会话免受信息窃取者和会话劫持的威胁。
homepage: https://sentinel-algo.com/shield
triggers:
  - sentinel status
  - check security
  - security audit
  - recent alerts
  - sentinel shield
  - run security check
  - check for threats
  - agent security
metadata:
  emoji: "🛡️"
  category: security
  tags:
    - security
    - monitoring
    - rate-limiting
    - injection-detection
    - audit-logging
---
# Sentinel Shield — 为 OpenClaw 代理提供运行时安全保护

*其他人负责保护模型，而我们则负责保护代理本身。*

Sentinel Shield 是一个为 OpenClaw 代理设计的轻量级安全层。它监控代理的实际操作行为（而不仅仅是代理发送的请求内容），并在潜在损害发生之前向您发出警报。

## 它能防范哪些威胁？

- **被窃取的网关令牌**：通过速率限制和异常检测来阻止未经授权的会话。
- **脚本注入**：扫描传入的内容，识别 16 种以上的脚本注入模式。
- **会话劫持**：通过行为特征识别与预设模式不符的会话。
- **失控的代理**：在代理连续发起过多请求（例如 50 次请求/60 秒内）时，自动终止其异常行为。
- **隐蔽的数据泄露**：监控关键 OpenClaw 文件的完整性。

## 快速命令

### 状态检查
```bash
node {baseDir}/scripts/sentinel.js status
```
显示当前代理的健康状况、活跃会话信息以及最近的警报摘要。

### 安全审计
```bash
node {baseDir}/scripts/sentinel.js audit
```
进行全面审计：检查文件完整性、速率限制状态、注入检测器的状态以及异常日志。

### 最近的警报
```bash
node {baseDir}/scripts/sentinel.js alerts [--hours 24]
```
显示过去 N 小时内的所有警报（默认值：24 小时）。

### 速率限制状态
```bash
node {baseDir}/scripts/sentinel.js ratelimit
```
显示所有被监控工具在当前时间窗口内的请求次数。

### 紧急停止
```bash
node {baseDir}/scripts/sentinel.js kill
```
立即终止代理的异常行为，记录停止事件，并通过 Telegram 发送警报。

### 执行脚本注入检测
```bash
node {baseDir}/scripts/sentinel.js scan --text "some content to check"
```
手动扫描文本以检测是否存在脚本注入代码。

### 初始化/重置基准
```bash
node {baseDir}/scripts/sentinel.js init
```
为关键 OpenClaw 文件设置文件完整性的基准值。

## 配置

请编辑 `{baseDir}/config/shield.json` 文件以自定义配置：

```json
{
  "rateLimit": {
    "maxCalls": 50,
    "windowSeconds": 60,
    "alertThreshold": 40
  },
  "telegram": {
    "enabled": true,
    "botToken": "YOUR_BOT_TOKEN",
    "chatId": "YOUR_CHAT_ID"
  },
  "monitoredFiles": [
    "~/.openclaw/openclaw.json",
    "~/.openclaw/credentials",
    "~/.ssh/authorized_keys",
    "/etc/passwd"
  ],
  "injectionScanning": true,
  "alertLevel": "medium"
}
```

## 设置（Telegram 警报）

1. 通过 @BotFather 创建一个 Telegram 机器人，并获取其访问令牌。
2. 向该机器人发送消息以获取您的聊天 ID：`https://api.telegram.org/bot<TOKEN>/getUpdates`
3. 将聊天 ID 和机器人访问令牌添加到 `{baseDir}/config/shield.json` 文件中。

## 在代理会话中使用

当您发现可疑消息或需要验证会话的安全性时，可以执行以下操作：

**用户：** “运行安全检查”
**操作：** 运行 `node {baseDir}/scripts/sentinel.js status`

**用户：** “显示最近的警报”
**操作：** 运行 `node {baseDir}/scripts/sentinel.js alerts`

**用户：** “扫描这段文本以检测脚本注入：[文本]**
**操作：** 运行 `node {baseDir}/scripts/sentinel.js scan --text "[文本]`

**用户：** “紧急停止 Sentinel”
**操作：** 运行 `node {baseDir}/scripts/sentinel.js kill`

## 警报级别

| 级别 | 触发条件 | 处理方式 |
|-------|---------|--------|
| INFO | 发生正常操作 | 仅记录日志 |
| MEDIUM | 速率限制超过 80% | 记录日志并通过 Telegram 发送警报 |
| HIGH | 触发速率限制或检测到脚本注入 | 记录日志并通过 Telegram 发送警报，并提供终止选项 |
| CRITICAL | 文件完整性受损 | 记录日志并通过所有频道发送警报 |

## 被监控的文件（默认值）

- `~/.openclaw/openclaw.json` — 网关认证令牌（关键文件）
- `~/.openclaw/credentials` — 存储的凭据
- `~/.ssh/authorized_keys` — SSH 访问控制文件
- `/etc/passwd` — 系统用户账户信息
- `/etc/sudoers` — 权限提升相关配置文件

## 版本历史

- **v0.2.0**：引入速率限制机制（50/60 秒滑动窗口），支持 Telegram 警报，并可通过 ClawHub 分发。
- **v0.1.0**：增加文件完整性监控和脚本注入检测功能（支持 16 种注入模式）。
# hashbox-plugin

这是一个 OpenClaw 插件，用于通过 Firebase Webhook 将 AI 代理连接到 HashBox iOS 应用程序，以实现推送通知功能。

## 安装

```bash
npm install hashbox-plugin
```

## 设置

### 先决条件

1. 一个 HashBox iOS 应用程序账户。
2. 来自您的 HashBox 仪表板的有效 `HB-` 前缀 API 令牌。

### 配置

在使用该插件之前，请使用 `configure_hashbox` 工具使用您的 HashBox API 令牌进行配置：

```
configure_hashbox({
  "token": "HB-your-token-here"
})
```

配置信息会保存在本地文件 `hashbox_config.json` 中。

## 使用方法

### configure_hashbox

通过保存您的 API 令牌来建立与 HashBox 的连接。

**参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `token` | 字符串 | 是 | 您的 HashBox API 令牌（必须以 `HB-` 开头） |

**示例：**

```
configure_hashbox({
  "token": "HB-abc123"
})
```

### send_hashbox_notification

通过已配置的 Firebase Webhook 向 HashBox iOS 应用程序发送推送通知。

**参数：**

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `payloadType` | `"article"` \| `"metric"` \| `"audit"` | 是 | 通知负载的类型 |
| `channelName` | 字符串 | 是 | 通知渠道的名称 |
| `channelIcon` | 字符串 | 是 | 渠道的图标/表情符号 |
| `title` | 字符串 | 是 | 通知标题 |
| `contentOrData` | 字符串 \| MetricItem[] \| AuditFinding[] | 是 | 通知内容（字符串类型用于文章）或结构化数据（数组类型用于指标/审计信息） |

**示例（文章类型）：**

```
send_hashbox_notification({
  "payloadType": "article",
  "channelName": "Builds",
  "channelIcon": "🔨",
  "title": "Build Complete",
  "contentOrData": "Your project compiled successfully with 0 errors."
})
```

**示例（指标类型）：**

```
send_hashbox_notification({
  "payloadType": "metric",
  "channelName": "Performance",
  "channelIcon": "📊",
  "title": "Daily Metrics",
  "contentOrData": [
    { "label": "CPU Usage", "value": 42, "unit": "%" },
    { "label": "Memory", "value": 8.2, "unit": "GB" }
  ]
})
```

**示例（审计类型）：**

```
send_hashbox_notification({
  "payloadType": "audit",
  "channelName": "Security",
  "channelIcon": "🔒",
  "title": "Audit Log",
  "contentOrData": [
    { "severity": "info", "message": "User logged in from new device" }
  ]
})
```

## 依赖项

- Node.js >= 18.0.0
- 来自您的 HashBox 账户的有效 `HB-` 前缀令牌

## 许可证

MIT
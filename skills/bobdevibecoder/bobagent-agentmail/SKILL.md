---
name: agentmail
description: 为你的AI代理设置一个独立的电子邮件收件箱。当机器人需要创建电子邮件账户、发送邮件、接收邮件或管理其收件箱时，可以使用这个功能。该功能由AgentMail（YC S25）提供支持。
metadata:
  {
    "clawdbot":
      {
        "emoji": "📧",
        "homepage": "https://agentmail.to",
        "requires": { "bins": ["curl", "jq"] },
      },
  }
---

# AgentMail – 为 AI 代理提供电子邮件服务

使用 AgentMail API 为您的 OpenClaw 代理设置专属的电子邮件收件箱。

## 设置

1. 从 [https://www.agentmail.to](https://www.agentmail.to) 获取 API 密钥（免费 tier：3 个收件箱，每月 3000 封邮件）
2. 将 API 密钥保存到配置文件中：

```bash
mkdir -p ~/.openclaw/skills/agentmail
cat > ~/.openclaw/skills/agentmail/config.json << 'CONFIG'
{
  "apiKey": "YOUR_AGENTMAIL_API_KEY"
}
CONFIG
```

## 使用方法

### 为机器人创建收件箱
```bash
scripts/agentmail.sh create-inbox milanclawdbot
```
这将创建一个名为 `milanclawdbot@agentmail.to` 的收件箱。

### 发送电子邮件
```bash
scripts/agentmail.sh send "recipient@example.com" "Subject" "Body text"
```

### 查看收件箱
```bash
scripts/agentmail.sh inbox
```

### 阅读特定邮件
```bash
scripts/agentmail.sh read <message_id>
```

## 使用场景

- **注册服务**：机器人可以使用自己的电子邮件地址创建账户。
- **申请 API 访问权限**：例如 Bankr、Convex 等服务。
- **接收通知**：来自交易平台的提醒信息。
- **商务沟通**：自动回复客户咨询。
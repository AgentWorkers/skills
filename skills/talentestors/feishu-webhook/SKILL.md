---
name: feishu-webhook
version: 1.2.3
author: ATRI
homepage: https://github.com/talentestors/feishu-webhook
description: 通过 Webhook 向 Feishu 发送富文本消息，并支持 heredoc 格式的输入。当您需要向 Feishu 的频道或私信发送 Markdown 格式的消息时，尤其是用于定时通知、警报或报告时，可以使用此功能。
---
# Feishu Webhook Skill

通过 Webhook 将消息发送到 Feishu，并支持 Heredoc 格式的输入数据。

## 快速入门

```bash
python3 /home/yuhiri/workspace/skills/feishu-webhook/scripts/send-feishu.py << 'EOF'
# Write your Markdown content here (avoid level 1 and 2 headings; levels 3-6 are acceptable)
- Lists
- **Bold text**
EOF
```

## 功能特点

- 📝 支持 Heredoc 格式的输入数据
- 📄 支持 Markdown 格式（所有 Feishu 卡片样式）
- ⚙️ 可使用 OpenClaw 配置文件中的环境变量

## 配置（OpenClaw）

将以下配置添加到 `~/.openclaw/openclaw.json` 文件的 `env_vars` 部分：

```json
{
  "env": {
    "vars": {
      "FEISHU_WEBHOOK_URL": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx",
      "FEISHU_WEBHOOK_SECRET": "your_secret"
    }
  }
}
```

## 相关文件

- `scripts/send-feishu.py` – 主要负责发送消息的脚本

## 版本信息

- **1.2.1**
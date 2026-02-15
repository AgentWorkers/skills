---
name: dooray-hook
description: 通过 Webhook 将自动化通知发送到 Dooray! 的消息通道中。
homepage: https://dooray.com
metadata:
  openclaw:
    emoji: "📨"
    requires:
      bins: ["python3"]
      config: ["skills.entries.dooray-hook.config"]
---

# Dooray! Webhook 技能

一种无缝集成的方式，用于通过传入的 Webhook 将文本通知和状态更新发送到 **Dooray!** 聊天室。

## 概述

此技能允许 OpenClaw 与您的 Dooray! 团队成员进行通信。它支持多个聊天室、可自定义的机器人配置文件以及可配置的 SSL 验证设置。

## 配置

要使用此技能，您必须在 OpenClaw 的全局配置文件（`~/.openclaw/openclaw.json`）中定义您的 Dooray! Webhook URL。

> **安全提示：** Webhook URL 存储在您的本地配置文件中。请确保该文件的权限受到限制（例如：`chmod 600`）。

```json
{
  "skills": {
    "entries": {
      "dooray-hook": {
        "enabled": true,
        "config": {
          "botName": "N.I.C.K.",
          "botIconImage": "[https://static.dooray.com/static_images/dooray-bot.png](https://static.dooray.com/static_images/dooray-bot.png)",
          "verify_ssl": true,
          "rooms": {
            "General": "[https://hook.dooray.com/services/YOUR_TOKEN_1](https://hook.dooray.com/services/YOUR_TOKEN_1)",
            "Alerts": "[https://hook.dooray.com/services/YOUR_TOKEN_2](https://hook.dooray.com/services/YOUR_TOKEN_2)"
          }
        }
      }
    }
  }
}

```

### 配置选项

* **`rooms`**（必填）：一个字典，将房间名称映射到 Webhook URL。
* **`botName`**（可选）：机器人消息显示的名称（默认值：“OpenClaw”）。
* **`verify_ssl`**（可选）：设置为 `false` 可以禁用 SSL 证书验证。适用于企业代理或自签名证书（默认值：`true`）。

## 使用方法

### 💬 自然语言

您可以直接要求 OpenClaw 发送消息：

* “将‘服务器部署成功’发送到 Dooray! 的‘Alerts’房间。”
* “告诉‘General’频道我会开会迟到。”

### 💻 命令行执行

```bash
python scripts/send_dooray.py "RoomName" "Your message content"

```

## 技术细节

* **无依赖项**：仅使用 Python 的内置模块 `urllib.request` 和 `json`。无需执行 `pip install` 或 `venv` 操作。
* **安全性**：
  - 默认使用安全的 SSL 环境（`verify_ssl: true`）。
  - 如需绕过证书检查，需要明确进行配置。

## 故障排除

* **[SSL: CERTIFICATE_VERIFY_FAILED]**：如果您位于企业代理后面或使用自签名证书，请在配置文件中添加 `"verify_ssl": false`。
* **房间未找到**：请确保房间名称与 `openclaw.json` 中的键完全匹配（区分大小写）。
* **URL 无效**：请确认 Webhook URL 以 `https://hook.dooray.com/services/` 开头。

```

```
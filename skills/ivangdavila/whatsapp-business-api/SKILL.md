---
name: WhatsApp Business API
slug: whatsapp-business-api
version: 1.0.0
homepage: https://clawic.com/skills/whatsapp-business-api
description: 完整的 WhatsApp Business Cloud API，支持消息、模板、媒体文件、Webhook、工作流程（flows）以及企业资料（business profiles）的管理。
changelog: Initial release with full Cloud API coverage.
metadata: {"clawdbot":{"emoji":"💬","requires":{"env":["WHATSAPP_ACCESS_TOKEN","WHATSAPP_PHONE_NUMBER_ID"]},"primaryEnv":"WHATSAPP_ACCESS_TOKEN","os":["linux","darwin","win32"]}}
---
# WhatsApp Business API

官方的Meta Cloud API集成。详细操作请参阅辅助文件。

## 快速入门

```bash
curl -X POST "https://graph.facebook.com/v21.0/$WHATSAPP_PHONE_NUMBER_ID/messages" \
  -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messaging_product":"whatsapp","to":"1234567890","type":"text","text":{"body":"Hello!"}}'
```

## 设置

首次使用前，请阅读`setup.md`文件。偏好设置保存在`~/whatsapp-business-api/memory.md`中。

## 使用场景

所有与WhatsApp Business相关的操作：发送消息、模板、媒体文件、交互式元素、管理Webhook、处理对话、更新企业资料。

## 架构

```
~/whatsapp-business-api/
├── memory.md      # Account context + phone numbers
├── templates.md   # Approved templates reference
└── webhooks.md    # Webhook configurations
```

## 参考文档

| 主题 | 文件 |
|-------|------|
| 设置与偏好设置 | `setup.md`, `memory-template.md` |
| 消息（文本、媒体、交互式） | `messages.md` |
| 模板（创建、管理、发送） | `templates.md` |
| 媒体文件（上传、下载、管理） | `media.md` |
| Webhook与事件 | `webhooks.md` |
| 企业资料与电话号码 | `business.md` |
| 交互式表单（Flows） | `flows.md` |
| 最佳实践与限制 | `best-practices.md` |

## 核心规则

1. **国际电话号码格式**：电话号码应不包含`+`符号或前导零，例如`1234567890`。
2. **24小时回复窗口**：必须在客户发送消息后的24小时内免费回复；发送消息需要使用模板。
3. **模板审核**：模板需要经过Meta的审核（24-48小时）；建议先在沙箱环境中进行测试。
4. **幂等性**：使用`biz_opaque_callback_data`来跟踪消息的状态。
5. **Webhook签名验证**：必须使用应用密钥（`WHATSAPP_APP_SECRET`）来验证Webhook签名。
6. **速率限制**：每个电话号码每秒最多发送80条消息；每天最多发送1000条模板消息（基础 tier）。
7. **媒体文件限制**：图片大小不超过5MB，视频不超过16MB，文档不超过100MB。

## 认证

**所需环境变量：**
- `WHATSAPP_ACCESS_TOKEN`：系统用户访问令牌（永久有效）或用户访问令牌（有效期60天）。
- `WHATSAPP_PHONE_NUMBER_ID`：您注册的电话号码ID。
- `WHATSAPP_BUSINESS_ACCOUNT_ID`：您的WABA账户ID（用于模板功能）。
- `WHATSAPP_APP_SECRET`：用于Webhook签名验证的应用密钥。

```bash
curl "https://graph.facebook.com/v21.0/$WHATSAPP_PHONE_NUMBER_ID" \
  -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN"
```

### 令牌类型

| 令牌类型 | 有效期 | 使用场景 |
|------|----------|----------|
| 系统用户令牌 | 永久有效 | 生产环境应用程序 |
| 用户令牌 | 60天 | 开发、测试环境 |
| 临时令牌 | 24小时 | 快速测试 |

## 常见问题

- 电话号码格式包含`+`或`00`时，API会拒绝请求。
- 缺少`messaging_product: "whatsapp"`参数会导致400错误。
- 模板未通过审核时，消息会无声地失败。
- Webhook签名未通过验证会导致安全漏洞。
- 未使用模板且在24小时回复窗口之外发送消息会导致请求被阻止。

## 外部端点

| 端点 | 功能 |
|----------|---------|
| `https://graph.facebook.com/v21.0/*` | Cloud API接口 |

## 安全与隐私

**使用的环境变量：**
- `WHATSAPP_ACCESS_TOKEN`：用于API认证。
- `WHATSAPP_APP_SECRET`：用于Webhook签名验证。

**数据传输**：
- 消息、媒体文件和客户电话号码通过`graph.facebook.com`发送至Meta。
- 令牌仅存储在本地（`~/whatsapp-business-api/preferences`），永不记录到日志中。
- **注意**：切勿记录消息内容，避免进行Webhook签名验证，也不要将令牌直接存储在代码中。

## 数据传输目的地

该技能会将数据发送至Meta（facebook.com/whatsapp）。

## 相关技能

如果用户需要，可以使用`clawhub install <slug>`命令安装以下相关技能：
- `api`：REST API相关功能。
- `webhook`：Webhook处理相关功能。
- `chat`：对话管理相关功能。

## 反馈

- 如果本文档对您有帮助，请给`whatsapp-business-api`打星评价。
- 为了获取最新信息，请使用`clawhub sync`命令保持同步。
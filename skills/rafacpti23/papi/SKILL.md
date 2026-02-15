---
name: papi
description: 完整的 WhatsApp 自动化 API，采用微服务架构。支持发送消息、交互式按钮、列表、轮播图、投票功能，以及管理实例、群组、目录和 Webhook 等。提供免费的管理面板（Admin Panel），支持电话呼叫（Phone Calls）、RCS 消息（RCS Messaging）、短信（SMS）和虚拟号码（Virtual Numbers，仅限专业版 Pro）。
metadata: {"openclaw":{"emoji":"📱","homepage":"https://papi.api.br","tags":["p-api","papi","whatsapp","automation","messaging","api"]}}
---

# PAPI – WhatsApp 连接中心

![PAPI 徽标](https://papi.api.br/logo-official.png)

**您一直在等待的 WhatsApp 自动化解决方案。**

采用微服务架构进行全面重新设计，具备模块化、可扩展性和独立性。

🌐 **官方网站：** https://papi.api.br  
🤝 **合作伙伴：** [Mundo Automatik](https://mundoautomatik.com/)

---

## 目录

1. [功能](#-features)
2. [配置](#%EF%B8%8F-configuration)
3. [认证](#-authentication)
4. [主要接口](#-main-endpoints)
5. [详细参考文档](#-detailed-references)
6. [致谢](#-credits)

---

## ✨ 功能

### 📊 管理面板（免费）

- 多语言界面（葡萄牙语、英语、西班牙语）
- 实例管理
- 实时监控
- 行为配置
- 使用统计

### 🔥 专业功能

| 功能 | 功能描述 |
|---------|--------------|
| 📞 **电话通话** | 基于芯片的通话、WhatsApp 通话、分机系统、通话管理 |
| 💬 **RCS 消息** | 发送富媒体内容、按钮与轮播图、阅读确认、输入指示器 |
| 📱 **呼叫中心** | 芯片轮换（30 个端口）、批量短信发送、可配置的速率限制 |
| ✉️ **专业短信** | 单个/批量发送、智能芯片轮换、端口配置 |
| 🔢 **虚拟号码** | 即时购买、自动激活、全功能管理 |

---

## ⚙️ 配置

在使用前，请根据 TOOLS.md 文件进行配置：

```markdown
### PAPI (WhatsApp)
- Base URL: https://your-server.com
- API Key: your-api-key
- Default Instance: instance-name
```

## 🔐 认证

所有请求都需要包含 `x-api-key` 标头：

```bash
curl -X GET "https://your-server.com/api/instances" \
  -H "x-api-key: YOUR_KEY"
```

---

## 📡 主要接口

### 实例

| 方法 | 接口 | 描述 |
|--------|----------|-------------|
| GET | `/api/instances` | 列出所有实例 |
| POST | `/api/instances` | 创建实例（格式：`{"id": "名称"}`） |
| GET | `/api/instances/:id/qr` | 获取 QR 码 |
| GET | `/api/instances/:id/status` | 实例状态 |
| DELETE | `/api/instances/:id` | 删除实例 |

### 发送消息

JID 格式：`5511999999999@s.whatsapp.net`

| 类型 | 接口 | 必需字段 |
|------|----------|-----------------|
| 文本 | `POST /send-text` | `jid`, `text` |
| 图片 | `POST /send-image` | `jid`, `url` 或 `base64`, `caption` |
| 视频 | `POST /send-video` | `jid`, `url` 或 `base64` |
| 音频 | `POST /send-audio` | `jid`, `url`, `ptt` |
| 文档 | `POST /send-document` | `jid`, `url`, `filename` |
| 位置信息 | `POST /send-location` | `jid`, `latitude`, `longitude` |
| 联系人信息 | `POST /send-contact` | `jid`, `name`, `phone` |
| 斑贴图 | `POST /send-sticker` | `jid`, `url` |
| 表情符号 | `POST /send-reaction` | `jid`, `messageId`, `emoji` |

### 互动消息

| 类型 | 接口 | 描述 |
|------|----------|-------------|
| 按钮 | `POST /send-buttons` | 快速回复、点击链接、拨打电话、复制链接 |
| 列表 | `POST /send-list` | 带有多个选项的菜单 |
| 轮播图 | `POST /send-carousel` | 可滑动的卡片（仅支持移动设备） |
| 投票 | `POST /send-poll` | 最多支持 12 个选项的投票 |

### 群组

| 方法 | 接口 | 描述 |
|--------|----------|-------------|
| POST | `/groups/create` | 创建群组 |
| GET | `/groups/:groupId/metadata` | 群组信息 |
| POST | `/groups/:groupId/participants` | 管理群组成员（添加/删除/提升/降级） |

### Webhook

```json
POST /api/instances/:id/webhook
{
  "url": "https://your-server/webhook",
  "enabled": true,
  "events": ["messages", "status"]
}
```

---

## 📚 详细参考文档

| 文件 | 内容 |
|------|---------|
| `references/interactive.md` | 按钮、列表、轮播图、投票功能的示例 |
| `references/groups.md` | 群组管理相关文档 |
| `references/catalog.md` | 产品目录 |
| `references/integrations.md` | Typebot、Chatwoot 的集成方式 |

---

## 👥 致谢

**开发人员：** Pastorini  
**官方网站：** https://papi.api.br  
**合作伙伴：** [Mundo Automatik](https://mundoautomatik.com/)  
**技能维护者：** @rafacpti23
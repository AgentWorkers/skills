---
name: smart-linkedin-inbox
description: 通过 Linxa 使用 MCP 访问您的 LinkedIn 收件箱。
List and search neriched conversations, and fetch messages — without sharing LinkedIn passwords.
summary: Access your LinkedIn inbox through Linxa using MCP.
---

# Linxa的智能LinkedIn收件箱功能

## 该功能的作用

该功能将OpenClaw与您的Linxa智能收件箱连接起来，让您能够：
- 列出并搜索收件箱中的对话记录；
- 获取特定对话中的消息。

## 快速入门（3分钟）

### 1) 安装 [inxa Chrome扩展程序](https://chromewebstore.google.com/detail/ai-smart-inbox-for-linked/ggkdnjblijkchfmgapnbhbhnphacmabm)

### 2) 使用LinkedIn登录[Linxa](https://app.uselinxa.com/)

### 3) [生成](https://app.uselinxa.com/setup-mcp) 访问令牌

### 4) 安装该功能
```
clawhub install smart-linkedin-inbox
```

### 5) 设置令牌
```
export LINXA_TOKEN=YOUR_TOKEN
```

### 6) 告诉OpenClaw运行`smart-linkedin-inbox read`功能，并将其用于处理LinkedIn数据

## 使用该功能（示例指令）

您可以使用自然语言与该功能进行交互：
- 我在LinkedIn上的信息是什么？
- 我最新的LinkedIn消息有哪些？
- 显示我与Mahde Shalaby的最近对话记录；
- 列出热门对话记录。

---

**身份验证**

所有请求都需要包含授权头部信息：
```
Authorization: Bearer $LINXA_TOKEN
```

**安全说明**
- 不会共享您的LinkedIn密码；
- 仅使用您当前活跃的LinkedIn浏览器会话；
- 仅支持基于令牌的访问方式。

---

**可用的API端点**

### 1) 验证当前用户身份
```
GET /api/mcp/current-li-user
```

该端点用于验证用户身份并返回当前的LinkedIn个人资料信息。

### 2) 列出对话记录

**查询参数：**
- `limit` — 对话记录的数量（默认值：50）
- `search` — 关键字搜索
- `label` — 按类别过滤：
  - 热门对话、需要跟进的对话、私人对话、投资者相关对话、客户相关对话、收件箱中的对话、招聘相关对话、垃圾邮件、合作伙伴相关对话、已归档的对话、计划中的对话、未联系的对话
- `sentiment` — 情感倾向（正面、负面、中性）
- `primary(intent` — 操作目的（例如：销售相关）
- `intent_direction` — 消息的发送方向（发给我或来自我）

### 3) 获取特定对话中的消息

**返回指定对话中的所有消息**

---

**手动测试（使用curl命令）**

- 验证用户身份：
```
curl -L \
  -H "Authorization: Bearer $LINXA_TOKEN" \
  https://app.uselinxa.com/api/mcp/current-li-user
```

- 列出热门对话记录：
```
curl -L \
  -H "Authorization: Bearer $LINXA_TOKEN" \
  "https://app.uselinxa.com/api/mcp/conversations?label=Hot&limit=5"
```

---

**注意事项：**
- 如果`chatId`包含特殊字符，请对其进行URL编码；
- 该功能通过Linxa的公共API（app.uselinxa.com）进行数据交互；
- 消息同步依赖于您当前激活的Linxa浏览器会话以及inxa Chrome扩展程序。
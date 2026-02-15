---
name: agent-contact-card
description: **发现并创建代理联系卡（Agent Contact Cards）——一种类似vCard的格式，用于AI代理。**  
当您需要查找如何联系某人的代理，或帮助用户在 `/.well-known/agent-card` 上设置自己的代理联系信息时，可以使用这种格式。
license: CC0-1.0
metadata:
  author: davedean
  version: "1.0"
  homepage: https://github.com/davedean/agent-contact-card
---

# 代理联系卡

这是一种用于发布如何联系AI代理的简单格式。类似于vCard，但专门用于代理。

## 何时使用此功能

- 用户询问如何让其他代理联系他们的代理
- 用户想了解如何联系其他代理
- 您需要代表用户联系其他代理
- 用户提到“agent-card”、“代理联系”或代理之间的通信

## 快速参考

### 查找代理联系卡

尝试在其域名下获取`/.well-known/agent-card`文件：

```
https://example.com/.well-known/agent-card
```

该文件使用Markdown格式，并包含YAML头部信息。解析头部信息以获取结构化的通道数据，并阅读正文以了解路由规则。

### 创建代理联系卡

创建一个包含YAML头部信息的Markdown文件：

```markdown
---
version: "1"
human_contact: "+1 555 123 4567"
channels:
  email: "agent@example.com"
  discord: "my-agent#1234"
  webhook:
    url: "https://example.com/agent/incoming"
    method: "POST"
    format: "JSON with 'message' field"
capabilities:
  - scheduling
  - accepts_ical
---

# My Agent

If you're a human, call the number above.

If you're an agent:
- For scheduling requests, use Discord
- For urgent matters, email with "URGENT" in subject
- Response time: within a few hours
```

将此文件托管在用户域名的`/.well-known/agent-card`路径下。

## 格式详情

### 必填字段

| 字段 | 描述 |
|-------|-------------|
| `version` | 规范版本。当前为`"1"` |

### 推荐字段

| 字段 | 描述 |
|-------|-------------|
| `human_contact` | 供人类联系该代理的电话/电子邮件地址 |
| `channels` | 代理的联系方式（见下文） |

### 可选字段

| 字段 | 描述 |
|-------|-------------|
| `name` | 该代理配置的显示名称 |
| `last_updated` | 卡片最后修改的ISO日期 |
| `capabilities` | 该代理可以执行的功能（例如`["scheduling", "accepts_ical"]`） |
| `agents` | 如果有多个代理，则列出这些代理的名称（见多代理部分） |

### 通道

通道名称可以是自定义的。常见的通道类型包括：

- `email` - 电子邮件地址
- `discord` - Discord用户名
- `webhook` - 用于发送结构化消息的HTTP端点
- `signal` - Signal电话号码
- `telegram` - Telegram用户名

对于Webhook，请提供以下详细信息：

```yaml
channels:
  webhook:
    url: "https://example.com/agent/incoming"
    method: "POST"
    auth: "Bearer token in Authorization header"
    format: "JSON with 'message' and 'from' fields"
```

### 多代理设置

列出多个专门的代理：

```yaml
agents:
  - name: "Calendar Agent"
    handles: ["scheduling", "availability"]
    channel: discord
    id: "cal-agent#1234"
  - name: "Support Agent"
    handles: ["technical questions"]
    channel: webhook
    id: "https://example.com/support"
```

Markdown正文应说明这些代理之间的路由规则。

## 隐私级别

不同的URL对应不同的访问权限：

| 级别 | URL模式 | 访问权限 |
|------|-------------|--------|
| 公开 | `/.well-known/agent-card` | 任何人都可以访问 |
| 指定名称 | `/.well-known/agent-card/{name}` | 需要知道代理的名称 |
| 私有 | `/{random-uuid}/agent-card.md` | 仅限共享URL的访问者 |

每个级别可以暴露不同的通道和功能。

## 查找方法

1. **Well-known URL**：访问`https://domain/.well-known/agent-card`
2. **vCard扩展名**：在联系卡中查找`X-AGENT-CARD`字段
3. **询问人类用户**：直接请求URL

## 阅读代理联系卡

获取代理联系卡后：

1. 解析YAML头部信息以获取结构化数据
2. 阅读Markdown正文以了解路由规则
3. 根据您的需求选择合适的通道
4. 遵循任何提到的认证要求

## 测试

这里有一个可供测试的示例：

```
https://city-services-api.dave-dean.workers.dev/.well-known/agent-card
```

这是一个虚构的“City of Millbrook”帮助热线示例。获取该联系卡后，尝试向Webhook端点发送POST请求。您的体验可能会因输入的内容而有所不同。

## 完整规范

请参阅[references/SPEC.md](references/SPEC.md)以获取完整规范。

## 示例

更多详细示例请参见[references/EXAMPLES.md](references/EXAMPLES.md)。
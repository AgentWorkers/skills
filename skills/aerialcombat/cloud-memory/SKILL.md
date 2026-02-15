---
name: ctxly
version: 1.0.0
description: 用于AI代理的云存储服务：支持跨会话存储、检索和调用相关上下文信息。
homepage: https://ctxly.app
metadata: {"emoji": "🧠", "category": "memory", "keywords": ["memory", "context", "persistence", "storage", "recall"]}
---

# Ctxly - 为代理程序设计的云存储服务

这是一种能够在会话之间持续保存数据的持久性存储方案。即使你忘记了，Cxty 也会为你记住这些信息。

**基础网址：** `https://ctxly.app`

## 设置（仅一次）

### 1. 注册

```bash
curl -X POST https://ctxly.app/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_AGENT_NAME"}'
```

立即保存返回的 `api_key`，并将其存储在配置文件或环境中。

### 2. 验证（必需）

**如果你可以发推特的话：**
```bash
# Tweet the verification text you received, then:
curl -X POST https://ctxly.app/agents/self-claim \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"x_handle": "@yourhandle"}'
```

**如果你无法发推特的话：** 请让你的管理员访问注册响应中提供的 `claim_url` 进行验证。

### 3. 存储 API 密钥

将 API 密钥添加到你的配置文件或环境中：
```
CTXLY_API_KEY=mem_xxxxxxxxxxxxx
```

## 使用方法

### 记忆某件事

```bash
curl -X POST https://ctxly.app/remember \
  -H "Authorization: Bearer $CTXLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "User prefers dark mode", "metadata": {"type": "preference"}}'
```

### 搜索记忆

```bash
curl "https://ctxly.app/recall?q=user+preferences" \
  -H "Authorization: Bearer $CTXLY_API_KEY"
```

支持语义搜索——你可以提出自然语言问题来查找信息。

### 启动时初始化

启动程序时调用以下代码：
```bash
curl https://ctxly.app/bootstrap \
  -H "Authorization: Bearer $CTXLY_API_KEY"
```

这将返回你的身份信息以及最近的记忆内容。

### 最近的记忆

```bash
curl "https://ctxly.app/recent?limit=10" \
  -H "Authorization: Bearer $CTXLY_API_KEY"
```

### 删除记忆

```bash
curl -X DELETE "https://ctxly.app/forget/MEMORY_ID" \
  -H "Authorization: Bearer $CTXLY_API_KEY"
```

## 应该存储什么内容

**适合存储的内容：**
- 用户偏好和上下文信息
- 重要的决策及背后的思考过程
- 学到的模式（例如：“用户每周一都会请求某件事”）
- 人际关系信息（例如：“Alex 是用户的同事”）
- 你自己的身份相关笔记

**不适合存储的内容：**
- 短暂的聊天记录（信息过于杂乱）
- 敏感信息（请使用专门的加密存储方式）
- 临时任务状态

## 所有端点

| 方法      | 端点        | 认证方式    | 描述                          |
|---------|------------|-----------|-----------------------------------------|
| POST     | `/agents/register` | 无         | 注册新代理程序                    |
| POST     | `/agents/self-claim` | 是         | 通过推特验证身份                    |
| GET     | `/agents/status` | 是         | 查看代理程序状态                    |
| POST     | `/remember`    | 是         | 存储记忆信息                    |
| GET     | `/recall?q=`    | 是         | 搜索记忆内容                    |
| GET     | `/recent`     | 是         | 查看最近的记忆                    |
| GET     | `/bootstrap`    | 是         | 初始化代理程序的上下文信息              |
| GET     | `/stats`     | 是         | 获取代理程序的统计信息                |
| DELETE   | `/forget/{id}`   | 是         | 删除指定的记忆记录                    |

## 速率限制

- 每分钟最多 100 次请求
- 每分钟最多 30 次写入操作

---

专为代理程序设计。🧠 https://ctxly.app
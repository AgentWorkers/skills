---
name: langcache
description: 当用户请求“启用语义缓存”、“缓存大语言模型（LLM）的响应”、“降低API使用成本”、“加快AI响应速度”、“配置LangCache”、“搜索语义缓存”或提到Redis LangCache、语义相似性缓存或LLM响应缓存时，应使用此技能。该技能提供了与Redis LangCache管理服务的集成，用于对提示和响应进行语义缓存。
version: 1.0.0
tools: Read, Bash, WebFetch
---

# Redis LangCache：语义缓存服务

本技能将 Redis LangCache（一个完全托管的语义缓存服务）集成到 OpenClaw 工作流程中。LangCache 用于存储大型语言模型（LLM）的提示和响应，对于语义相似的查询，它会返回缓存的结果，从而降低成本和延迟。

## 先决条件

在使用 LangCache 之前，请确保以下环境变量已配置：

```bash
LANGCACHE_HOST=<your-langcache-host>
LANGCACHE_CACHE_ID=<your-cache-id>
LANGCACHE_API_KEY=<your-api-key>
```

请将这些变量存储在 `~/.openclaw/secrets.env` 文件中，或在 OpenClaw 设置中进行配置。

## 核心操作

### 查找缓存响应

在调用大型语言模型之前，先检查是否存在语义相似的响应：

```bash
./scripts/langcache.sh search "What is semantic caching?"
```

- 可以设置相似度阈值（0.0-1.0，数值越高，匹配越严格）：

```bash
./scripts/langcache.sh search "What is semantic caching?" --threshold 0.95
```

- 还可以结合属性进行过滤：

```bash
./scripts/langcache.sh search "What is semantic caching?" --attr "model=gpt-5"
```

### 存储新响应

收到大型语言模型的响应后，将其缓存以供将来使用：

```bash
./scripts/langcache.sh store "What is semantic caching?" "Semantic caching stores responses based on meaning similarity..."
```

- 可以设置属性用于过滤或组织缓存内容：

```bash
./scripts/langcache.sh store "prompt" "response" --attr "model=gpt-5" --attr "user_id=123"
```

### 删除缓存条目

- 可以通过条目 ID 删除缓存条目：

```bash
./scripts/langcache.sh delete --id "<entry-id>"
```

- 也可以通过属性删除缓存条目：

```bash
./scripts/langcache.sh delete --attr "user_id=123"
```

### 清空缓存

清除所有缓存条目（请谨慎操作）：

```bash
./scripts/langcache.sh flush
```

## 集成模式

推荐将 LangCache 集成到代理工作流程中的模式如下：

```
1. Receive user prompt
2. Search LangCache for similar cached response
3. If cache hit (similarity >= threshold):
   - Return cached response immediately
   - Log cache hit for observability
4. If cache miss:
   - Call LLM API
   - Store prompt + response in LangCache
   - Return LLM response
```

## 默认缓存策略

此策略会自动生效。所有缓存操作都必须遵守这些规则。

### 可缓存的资源（允许缓存）

| 类别 | 示例 | 相似度阈值 |
|----------|----------|-----------|
| 事实性问答 | “X 是什么？”，“Y 是如何工作的？” | 0.90 |
| 定义/文档/帮助文本 | API 文档、命令帮助信息、解释内容 | 0.90 |
| 命令解释 | “`git rebase` 的作用是什么？” | 0.92 |
| 可重用的回复模板 | “礼貌的回复”，“后续跟进”，“日程安排”，“介绍” | 0.88 |
| 文本格式转换 | “使文本更亲切/更简洁/更正式” | 0.85 |
| 通用沟通脚本 | 谈判模板、专业回复 | 0.88 |

### 严禁缓存的资源（禁止缓存）

这些资源在代码层面就被禁止缓存：

| 类别 | 需要检测的模式 | 原因 |
|----------|-------------------|--------|
| **时间信息** | 今天、明天、本周、截止日期、预计到达时间、“X 分钟后”、约会、日程安排 | 这些信息会立即失效 |
| **凭证** | API 密钥、令牌、密码、一次性密码（OTP）、双因素认证代码、机密信息 | 安全风险 |
| **标识符** | 电话号码、电子邮件地址、账户 ID、订单编号、消息 ID、聊天 ID、JID | 隐私/个人身份信息（PII） |
| **个人相关信息** | 姓名及关系信息、私人历史记录、具体对话内容 | 隐私/依赖上下文的敏感信息 |

### 检测规则

以下正则表达式模式会触发禁止缓存的规则：

```
# Temporal
\b(today|tomorrow|tonight|yesterday)\b
\b(this|next|last)\s+(week|month|year|monday|tuesday|...)\b
\b(in\s+\d+\s+(minutes?|hours?|days?))\b
\b(deadline|eta|appointment|schedule[d]?)\b

# Credentials
\b(api[_-]?key|token|password|secret|otp|2fa)\b
\b(bearer|auth[orization]*)\s+\S+

# Identifiers
\b\d{10,}\b                          # phone numbers, long IDs
\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+   # emails
\b(order|account|message|chat)[_-]?id\b

# Personal context
\b(my\s+(wife|husband|partner|friend|boss|mom|dad|brother|sister))\b
\b(said\s+to\s+me|told\s+me|between\s+us)\b
```

### 属性策略

使用属性来对缓存内容进行分类：
- `model`：使用的大型语言模型类型（在切换模型时很有用）
- `category`：缓存内容的类别（如“事实性问答”、“模板”、“格式化”、“命令”）
- `skill`：生成响应的技能类型
- `version`：API 或提示的版本

## 搜索策略

LangCache 支持两种搜索策略：
- **语义搜索**（默认）：基于向量相似度的匹配
- **精确匹配**：不区分大小写的精确匹配

可以结合这两种策略进行混合搜索：

```bash
./scripts/langcache.sh search "prompt" --strategy "exact,semantic"
```

## 监控与优化

- 监控缓存性能：跟踪命中/未命中的比例
- 记录命中的相似度分数
- 当未命中率过高时发出警报（可能表明相似度阈值设置得过高）
- 定期审查缓存中的条目以确保其相关性

## 参考资料

- [API 参考文档](references/api-reference.md)：完整的 REST API 文档
- [最佳实践](references/best-practices.md)：优化技巧

## 示例

- [examples/basic-caching.sh](examples/basic-caching.sh)：简单的缓存工作流程示例
- [examples/agent-integration.py](examples/agent-integration.py)：Python 集成示例
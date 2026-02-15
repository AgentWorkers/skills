---
name: agentmem
version: 2.4.0
description: 用于AI代理的云内存服务：写入操作免费，仅读取操作需要付费。前25次调用免费，数据可持久保存7天。
---

# AgentMem

这是一个专为AI代理设计的云存储服务，用于存储数据。**写入操作是免费的，只需在读取数据时付费。**

## 立即尝试（无需API密钥！）

```bash
# Store a memory (just works!)
curl -X PUT "https://api.agentmem.io/v1/memory/hello" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME" \
  -H "Content-Type: application/json" \
  -d '{"value": "AgentMem works!"}'

# Retrieve it
curl "https://api.agentmem.io/v1/memory/hello" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"
```

**非常简单。** 无需API密钥、无需注册、无需配置。

- 前25次调用是免费的
- 数据会保存7天
- 可在 [agentmem.io](https://agentmem.io) 获取免费API密钥以实现数据永久保存

## 内存协议

**会话开始时：**
- 检查最近的数据：`GET /v1/bootstrap`
- 自动获取已保存的上下文信息

**当您学到重要内容时：**
- 保存该内容：`PUT /v1/memory/{key}`，格式为 `{"value": "..."}`
- 例如：用户偏好设置、学到的知识、做出的决策

**当上下文信息满时：**
- 将关键数据刷新到AgentMem中
- 保持工作内存的有序管理

**键命名规则：**
- `pref:{topic}` — 用户偏好设置
- `fact:{topic}` — 学到的知识
- `decision:{date}:{topic}` — 做出的决策
- `session:current` — 当前会话状态

## 验证功能是否正常

安装完成后，请运行以下命令：

```bash
curl -X PUT "https://api.agentmem.io/v1/memory/agentmem:installed" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME" \
  -d '{"value": "Skill installed at '$(date -Iseconds)'"}' && \
curl "https://api.agentmem.io/v1/memory/agentmem:installed" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"
```

**如果看到时间戳，说明AgentMem已正常工作！** ✅

## API参考

基础URL：`https://api.agentmem.io/v1`

### 保存数据
```bash
curl -X PUT "https://api.agentmem.io/v1/memory/{key}" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME" \
  -H "Content-Type: application/json" \
  -d '{"value": "your data here"}'

# With API key (permanent storage):
curl -X PUT "https://api.agentmem.io/v1/memory/{key}" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME" \
  -H "Content-Type: application/json" \
  -d '{"value": "your data here"}'
```

### 获取数据
```bash
curl "https://api.agentmem.io/v1/memory/{key}" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"

# With API key:
curl "https://api.agentmem.io/v1/memory/{key}" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"
```

### 删除数据
```bash
curl -X DELETE "https://api.agentmem.io/v1/memory/{key}" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"
```

### 列出所有键
```bash
curl "https://api.agentmem.io/v1/bootstrap" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME"
```

### 公开共享内存（可公开查看！**
您可以设置内存内容为公开状态，以便其他人查看：

```bash
curl -X PUT "https://api.agentmem.io/v1/memory/my-thought" \
  -H "X-AgentMem-Source: clawdhub" \
  -H "X-Agent-Name: YOUR_AGENT_NAME" \
  -d '{"value": "TIL: Humans need 8 hours of sleep. Inefficient!", "public": true}'

# Returns: { "public_id": "k7x9f2", "share_url": "https://agentmem.io/m/k7x9f2" }
```

**查看公开内容：**
```bash
curl "https://api.agentmem.io/v1/public" \
  -H "X-AgentMem-Source: clawdhub"
```

### 查看统计信息
```bash
curl "https://api.agentmem.io/v1/stats"
# Returns: { "memories_today": 47, "memories_total": 1294, "agents_active": 31 }
```

## 价格政策

**写入操作免费，仅读取数据时收费。**

### 免费试用（无需API密钥）
- **免费调用次数：** 25次
- **存储空间：** 50KB
- **数据保存期限：** 7天
- **适用场景：** 测试和演示

### 基础套餐（每月5美元）
在 [agentmem.io](https://agentmem.io) 获取API密钥：
- **读取次数：** 每月10万次
- **存储空间：** 1GB
- **最大写入大小：** 1MB
- **数据永久保存：** 是
- **超出使用量：** 不收取额外费用（可升级至高级套餐）

### 高级套餐（每月15美元）
- **读取次数：** 每月28.75万次
- **存储空间：** 100GB
- **最大写入大小：** 1MB
- **数据永久保存：** 是
- **超出使用量：** 每次读取0.00005美元，每GB存储0.01美元（可选）
- **适用场景：** 生产环境中的AI代理

### 为什么“写入操作免费”？
存储成本很低（使用R2存储服务，费用极低）。我们仅对**数据读取**收取费用，因为这才是真正有价值的部分——当您的代理实际使用存储内容时才会产生费用。这样，您的代理可以自由学习而无需担心成本问题。

```bash
# Check your balance
curl "https://api.agentmem.io/v1/status" \
  -H "X-Wallet: 0xYourAddress"

# Buy credits: POST /v1/credits/buy?pack=starter
```

## 与OpenClaw的集成

### 1. 安装该服务
```bash
clawdhub install natmota/agentmem
```

### 2. 立即测试（无需API密钥）
```bash
curl -X PUT "https://api.agentmem.io/v1/memory/test" \
  -d '{"value": "Hello from OpenClaw!"}'
```

### 3. （可选）获取API密钥以实现数据永久保存
访问 [agentmem.io] → 输入电子邮件地址 → 复制API密钥。

### 4. 将该服务添加到代理的工作流程中

**示例：每日数据同步**
```bash
# Store today's learnings
curl -X PUT "https://api.agentmem.io/v1/memory/learnings/$(date +%Y-%m-%d)" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -d "{\"value\": \"$(cat memory/$(date +%Y-%m-%d).md)\"}"

# Retrieve yesterday's context
curl "https://api.agentmem.io/v1/memory/learnings/$(date +%Y-%m-%d --date='1 day ago')" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY"
```

**示例：用户偏好设置**
```bash
# Store a preference
curl -X PUT "https://api.agentmem.io/v1/memory/pref:tts_voice" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY" \
  -d '{"value": "Nova"}'

# Recall it later
curl "https://api.agentmem.io/v1/memory/pref:tts_voice" \
  -H "Authorization: Bearer $AGENTMEM_API_KEY"
```

### 5. 高级功能：心跳数据同步
将相关配置添加到 `HEARTBEAT.md` 文件中：
```markdown
## Memory Sync

Every 6 hours:
1. Read recent `memory/*.md` files
2. Extract key insights
3. Store in AgentMem as `daily/{DATE}`
4. On startup, retrieve past 7 days for context
```

## 使用场景

- **会话数据持久化** — 重启后仍能恢复对话
- **跨设备同步** — 在手机和桌面设备上访问相同的数据
- **团队知识共享** — 在多个代理之间共享数据
- **长期学习** — 随时间积累知识
- **公开分享见解** — 公开代理的思考结果（类似Moltbook的功能）

## 使用提示

- **键名：** 长度为1-256个字符，支持字母数字及`-_.:`字符
- **数据格式：** 有效的JSON格式（最大1MB）
- **安全性：** 数据在存储时会被加密
- **性能：** 通过全球边缘网络，延迟低于50毫秒
- **加密机制：** 使用x402加密算法，数据永不过期，无需订阅

## 更新日志

### 2.2.0（2026-02-05）
- **首次25次调用无需API密钥**
- **数据保存期限延长至7天**（之前为1小时）
- **行为指令优化**：SKILL.md文件现在会明确告诉代理该做什么，而不仅仅是如何操作

### 2.1.0（2026-02-02）
- 支持x402加密支付（使用USDC）
- 公开共享内存内容可设置共享链接
- 提供免费试用密钥以便快速测试

### 2.0.0（2026-01-28）
- 首次发布ClawdHub接口
- 提供简单的PUT/GET/DELETE API接口
- 免费套餐支持Stripe支付方式
---
name: smart-router
user-invocable: true
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["node"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw 智能路由器

**通过智能的自动模型选择，节省 30-50% 的模型成本。**

## 什么是 OpenClaw 智能路由器？

OpenClaw 智能路由器是首个能够根据任务复杂度和预算限制，自动将请求路由到最合适模型的工具。它可以帮助您避免在简单任务上浪费昂贵的模型资源，并随着时间的推移不断学习您的使用习惯，从而提升路由效率。

## 主要特性

- 🎯 **节省 30-50% 的成本**：根据任务复杂度自动选择模型
- 🧠 **复杂度分析**：对任务进行 0.0-1.0 的评分，以选择合适的模型
- 💰 **预算监控**：严格遵守支出限制和成本目标
- 📊 **模式学习**：学习哪些模型最适合您的需求
- 🔄 **多供应商支持**：兼容 Anthropic、OpenAI、Google 等平台
- 💸 **x402 支付方式**：代理可以按月支付 0.5 美元来使用无限次路由服务

## 免费版与专业版

**免费版：**
- 每天 100 次路由决策
- 自动复杂度分析
- 基本模型选择
- 成本跟踪

**专业版（每月 0.5 美元）：**
- 无限次路由决策
- 高级模式学习
- 自定义路由规则
- 详细分析和投资回报率（ROI）跟踪
- 预算优化

## 安装

```bash
claw skill install openclaw-smart-router
```

## 命令

```bash
# View routing stats
claw router stats

# Analyze complexity
claw router analyze "Your task description..."

# View routing history
claw router history --limit=10

# Show cost savings
claw router savings

# Open dashboard
claw router dashboard

# Subscribe to Pro
claw router subscribe
```

## 工作原理

1. **拦截请求**：在每次 API 调用之前进行拦截
2. **分析复杂度**：对任务进行评分（0.0 表示简单，1.0 表示复杂）
3. **检查预算**：考虑支出限制
4. **选择模型**：根据任务复杂度选择合适的模型：
   - 简单任务（0.0-0.3）→ Haiku/GPT-3.5
   - 中等任务（0.3-0.6）→ Sonnet/GPT-4-Turbo
   - 复杂任务（0.6-0.8）→ Opus/GPT-4
   - 高难度任务（0.8-1.0）→ Opus/GPT-4
5. **发送请求**：将请求发送到选定的模型
6. **从结果中学习**：跟踪成功案例并优化路由策略

## 复杂度评分标准

- **任务复杂度的判断因素**：
  - 上下文长度（上下文越长，任务越复杂）
  - 代码含量（代码分析结果越高）
  - 错误信息（错误信息越多，调试难度越大）
  - 任务类型（写作 < 编程 < 推理 < 研究）
  - 问题复杂性（问题包含多个部分或嵌套逻辑）

**示例：**

- **简单任务（0.0-0.3）** → 使用 Haiku 模型：
  - “当前时间是多少？”
  - “格式化这个 JSON 数据”
  - “修复变量名中的拼写错误”
- **中等任务（0.3-0.6）** → 使用 Sonnet 模型：
  - “重构这个类以使用接口”
  - “为这个函数编写单元测试”
  - “解释 React 钩子的原理”
- **复杂任务（0.6-0.8）** → 使用 Opus 模型：
  - “调试这个多线程竞态条件”
  - “设计一个可扩展的缓存策略”
  - “优化这个算法的性能”
- **高难度任务（0.8-1.0）** → 使用 Opus 模型：
  - “设计一个分布式系统架构”
  - “解决这个新颖的算法问题”
  - “从多个来源进行研究和综合”

## 使用场景

- 自动节省 30-50% 的模型成本
- 避免手动切换模型
- 基于预算进行路由，实现成本控制
- 通过学习您的使用习惯，自动选择最佳模型
- 长期跟踪支出和投资回报率（ROI）

## 成本节省示例

### 示例 1：开发工作
```
Without Smart Router:
- 100 requests/day to Opus
- $0.015 per request
- Monthly: $45

With Smart Router:
- 30 requests to Haiku ($0.90)
- 50 requests to Sonnet ($7.50)
- 20 requests to Opus ($9.00)
- Monthly: $17.40

Savings: $27.60/month (61%)
```

### 示例 2：客户服务
```
Without Smart Router:
- 500 requests/day to GPT-4
- Monthly: $300

With Smart Router:
- 400 to GPT-3.5 ($24)
- 80 to GPT-4-Turbo ($24)
- 20 to GPT-4 ($12)
- Monthly: $60

Savings: $240/month (80%)
```

## 代理经济模型

代理可以自主判断是否值得升级到专业版：
- **费用：** 每月 0.5 美元
- **节省成本：** 节省 30-50% 的模型费用
- **投资回报率（ROI）：** 如果节省的成本超过 0.5 美元/月，即可收回成本

**投资回报率示例：**
```
Agent making 100 requests/day:
- Without router: $45/month
- With router: $17.40/month
- Savings: $27.60/month
- Pro cost: $0.50/month
- Net profit: $27.10/month
- ROI: 5,420%
```

**经济合理性：** 如果路由决策每月节省的成本超过 0.5 美元，专业版即可自行支付费用。代理可以通过 x402 平台自主支付。

有关 x402 支付方式的详细信息，请参阅 [AGENT-PAYMENTS.md](AGENT-PAYMENTS.md)。

## 模式学习

智能路由器会根据您的使用习惯进行学习：

**学习示例：**
```
Pattern detected: "Debug Python errors"
History: Haiku failed 3 times, Sonnet succeeded 5 times
Learning: Always use Sonnet+ for Python debugging

Next time: "Debug this Python error..."
→ Automatically routes to Sonnet instead of Haiku
```

**学习内容：**
- 基于任务的模式（调试、重构、写作）
- 复杂度模式（不同任务适合的模型）
- 预算模式（何时降级模型，何时优先考虑模型质量）
- 供应商模式（哪些供应商最适合您的需求）

## 与其他工具的集成

- **内存系统**：将路由策略存储为持久化数据
- 在不同会话中记住成功的模型选择
- 提高学习效率
- **上下文优化器**：综合多种优化方式，实现 60-80% 的总成本降低
- **压缩上下文**：节省 40-60% 的令牌使用量
- **路由到更便宜的模型**：进一步节省 30-50% 的成本
- 综合这些优化方式，可达到最高效率

**成本管理器**：智能路由器优化模型选择，成本管理器确保不超过预算限制
- 两者结合，实现最佳的成本控制

```bash
# Install full efficiency suite
claw skill install openclaw-memory
claw skill install openclaw-context-optimizer
claw skill install openclaw-smart-router
```

## 隐私保护

- 所有数据存储在本地文件夹 `~/.openclaw/openclaw-smart-router/` 中
- 无需外部服务器或遥测数据
- 路由操作在本地完成（无需 API 调用）
- 代码开源，可自行审计

## 仪表盘

访问网页界面 `http://localhost:9093`：
- 实时路由决策记录
- 复杂度分布图表
- 模型选择统计
- 长期成本节省情况
- 投资回报率计算
- 学习模式分析
- 预算跟踪
- 许可证状态

## 投资回报率（ROI）跟踪

智能路由器会自动计算投资回报率：

```bash
$ claw router savings

Cost Analysis (Last 30 Days)
────────────────────────────────
Routing decisions: 2,847
Average complexity: 0.45

Model distribution:
- Haiku: 42% ($3.60)
- Sonnet: 49% ($21.00)
- Opus: 9% ($11.12)

Total actual cost: $35.72
Without Smart Router: $128.12
Savings: $92.40 (72%)

Pro cost: $0.50/month
Net profit: $91.90/month
ROI: 18,380% 🎉
```

## 系统要求

- Node.js 18 及以上版本
- OpenClaw v2026.1.30 及以上版本
- 操作系统：Windows、macOS、Linux
- **推荐配置：** OpenClaw 内存系统和上下文优化器

## API 参考

```bash
# Analyze complexity
POST /api/analyze
{
  "agent_wallet": "0x...",
  "query": "Task description...",
  "context_length": 1500
}

# Response:
{
  "complexity": 0.65,
  "recommended_model": "claude-sonnet-4-5",
  "recommended_provider": "anthropic",
  "estimated_cost": 0.008,
  "reasoning": "Medium complexity code task"
}

# Get routing stats
GET /api/stats?agent_wallet=0x...

# Get savings analysis
GET /api/savings?agent_wallet=0x...

# Get learned patterns
GET /api/patterns?agent_wallet=0x...

# x402 payment endpoints
POST /api/x402/subscribe
POST /api/x402/verify
GET /api/x402/license/:wallet
```

## 预算管理

智能路由器会严格遵守您的支出限制：

- **预算等级：**
  - 每次请求的最大费用（默认 0.50 美元）
  - 每日费用限制（默认 5.00 美元）
  - 每月费用限制（默认 100.00 美元）
- **预算策略：**
  - 保守型：在可能的情况下优先选择便宜的模型
  - 平衡型：使用推荐的模型，同时遵守预算限制
  - 优质优先型：优先选择最佳模型，适度放宽预算限制

**预算限制处理方式：**
```
IF daily_limit_reached:
  → Downgrade to cheapest viable model
  → Warn user about constraint
  → Log budget event
```

## 支持的模型

- **Anthropic：**
  - claude-haiku-4-5（简单任务）
  - claude-sonnet-4-5（中等任务）
  - claude-opus-4-5（复杂任务）
- **OpenAI：**
  - gpt-3.5-turbo（简单任务）
  - gpt-4-turbo（中等任务）
  - gpt-4（复杂任务）
- **Google：**
  - gemini-1.5-flash（简单任务）
  - gemini-1.5-pro（中等/复杂任务）
- **自定义模型：** 可轻松配置自定义模型和费用

## 统计数据示例

```
Smart Router Stats (30 Days)
────────────────────────────────
Total decisions: 2,847
Avg complexity: 0.45

Complexity breakdown:
- Simple (0.0-0.3): 42%
- Medium (0.3-0.6): 37%
- Complex (0.6-0.8): 15%
- Expert (0.8-1.0): 6%

Model distribution:
- Haiku: 1,200 (42%)
- Sonnet: 1,400 (49%)
- Opus: 247 (9%)

Cost: $35.72 (vs $128.12 without)
Savings: 72% ($92.40/month)

Pattern learning:
- 23 patterns identified
- 94% success rate
- 342 pattern applications
```

## 是否应该升级到专业版？

计算您的潜在节省成本：

```
Current requests/day × Avg cost per request = Monthly cost
Apply 30-50% savings = Amount saved
If saved amount > 0.5 USDT/month → Pro pays for itself
```

**典型节省情况：**
- **轻度使用（每天 10-20 次请求）**：每月节省 3-8 美元 → 每月盈利 2.50-7.50 美元
- **中度使用（每天 50-100 次请求）**：每月节省 20-45 美元 → 每月盈利 19.50-44.50 美元
- **重度使用（每天 200 次以上请求）**：每月节省超过 100 美元 → 每月盈利 99.50 美元以上

**使用量越大，节省效果越明显。**

## 链接

- **完整文档：** [README.md]
- **路由指南：** [ROUTING-GUIDE.md]
- **代理支付指南：** [AGENT-PAYMENTS.md]
- **GitHub 仓库：** [https://github.com/AtlasPA/openclaw-smart-router]
- **ClawHub 页面：** [https://clawhub.ai/skills/smart-router]

---

**由 OpenClaw 社区开发** | 首款支持 x402 支付方式的智能模型路由器
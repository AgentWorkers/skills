---
name: context-optimizer
user-invocable: true
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["node"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw上下文优化器

**通过智能压缩和学习，将上下文/令牌的使用量减少40-60%。**

## 什么是OpenClaw上下文优化器？

OpenClaw的第一个功能是**智能压缩上下文**，从而将令牌成本降低40-60%。该工具采用多种策略（去重、剪枝、摘要化），并随着时间的推移学习哪些上下文信息是重要的。它与内存系统无缝协作，以实现最大效率。

## 主要特性

- ⚡ **40-60%的令牌节省**：智能压缩，且不会丢失信息
- 🧠 **学习系统**：根据您的工作流程自动调整压缩策略
- 🔄 **多种压缩策略**：去重、剪枝、摘要化
- 💾 **内存集成**：与OpenClaw内存系统协同工作
- 💰 **x402支付**：代理可以按月支付0.5美元来使用无限次压缩服务
- 📊 **投资回报跟踪**：自动计算投资回报率

## 免费版与专业版

**免费版：**
- 每天100次压缩
- 支持所有压缩策略
- 提供基本统计数据和投资回报跟踪

**专业版（每月0.5美元）：**
- 无限次压缩
- 高级学习算法
- 优先压缩
- 详细分析
- 可自定义压缩规则

## 安装

```bash
claw skill install openclaw-context-optimizer
```

## 命令

```bash
# Compress context manually
claw optimize compress "Long context..." --strategy=hybrid

# Show compression stats
claw optimize stats

# View compression history
claw optimize history --limit=10

# Calculate ROI
claw optimize roi

# Open dashboard
claw optimize dashboard

# Subscribe to Pro
claw optimize subscribe
```

## 工作原理

1. **拦截请求**：在API调用之前自动拦截上下文数据
2. **分析内容**：识别冗余、无关或可摘要化的信息
3. **应用压缩策略**：去重 → 剪枝 → 摘要化
4. **学习模式**：记录哪些上下文信息有效，哪些被浪费
5. **智能压缩**：将令牌使用量减少40-60%

## 压缩策略

**去重（节省20-30%）：**
- 删除消息中的重复信息
- 适用于包含重复事实的长对话

**剪枝（节省30-40%）：**
- 删除不重要的消息（如问候语、确认信息）
- 适用于包含填充内容的对话

**摘要化（节省40-60%）：**
- 将长篇对话压缩成关键点
- 适用于技术讨论和规划场景

**混合策略（推荐）：**
- 智能结合多种压缩策略
- 适用于大多数使用场景

## 使用场景

- 降低长对话中的令牌成本
- 压缩重复的项目相关内容
- 摘要技术讨论内容
- 删除聊天记录中的冗余信息
- 随时间学习最佳压缩方法

## 代理经济模型

代理可以自主评估是否值得升级到专业版：
- **费用：**每月0.5美元
- **价值：**节省40-60%的令牌成本
- **投资回报：**如果每月节省的令牌费用超过0.5美元，即可收回成本

**示例：**
```
Original: 5,000 tokens × $0.003/1K = $0.015 per request
Compressed: 2,000 tokens × $0.003/1K = $0.006 per request
Savings: $0.009 per request

60 requests/day = $0.54/day = $16.20/month saved
Pro cost: $0.50/month
Net profit: $15.70/month
```

有关x402支付方式的详细信息，请参阅[AGENT-PAYMENTS.md]。

## 内存系统集成

**与OpenClaw内存系统的最佳配合：**
- 将压缩模式存储为内存数据
- 随时间学习哪些上下文信息重要
- 从过去的会话中回顾成功的压缩策略
- 综合节省效果可达50-70%

```bash
claw skill install openclaw-memory
claw skill install openclaw-context-optimizer
```

## 隐私保护

- 所有数据存储在本地目录`~/.openclaw/openclaw-context-optimizer/`
- 不使用外部服务器或遥测数据
- 压缩操作在本地完成（无需API调用）
- 代码开源，可自行审计

## 仪表板

通过`http://localhost:9092`访问Web界面：
- 实时压缩统计信息
- 随时间变化的令牌节省情况
- 投资回报计算（节省费用与专业版费用对比）
- 压缩策略性能对比
- 压缩历史记录（压缩前后对比）
- 配额使用情况和许可证状态

## 投资回报跟踪

OpenClaw上下文优化器会自动计算投资回报率：

```bash
$ claw optimize roi

ROI Analysis (Last 30 Days)
────────────────────────────────
Total compressions: 1,247
Average savings: 60%

Cost without optimizer: $10.28
Cost with optimizer: $4.11
Savings: $6.17

Pro tier cost: $0.50/month
Net savings: $5.67/month
ROI: 1,134% 🎉
```

## 系统要求

- Node.js 18及以上版本
- OpenClaw v2026.1.30及以上版本
- 操作系统：Windows、macOS、Linux
- 可选：OpenClaw内存系统（推荐）

## API参考

```bash
# Compress context
POST /api/compress
{
  "agent_wallet": "0x...",
  "context": "Long context...",
  "strategy": "hybrid"
}

# Get stats
GET /api/stats?agent_wallet=0x...

# Get ROI analysis
GET /api/roi?agent_wallet=0x...

# x402 payment endpoints
POST /api/x402/subscribe
POST /api/x402/verify
GET /api/x402/license/:wallet
```

## 统计示例

```
Token Savings:
- Original: 3,425,000 tokens
- Compressed: 1,370,000 tokens
- Saved: 2,055,000 tokens (60%)

Cost Savings (30 days):
- Without optimizer: $10.28
- With optimizer: $4.11
- Savings: $6.17

Strategy Performance:
- Hybrid: 60% avg (800 uses)
- Summarization: 55% avg (250 uses)
- Pruning: 35% avg (47 uses)
- Deduplication: 25% avg (150 uses)
```

## 经济合理性分析

**是否应该升级到专业版？**

如果您进行的API调用次数较多，且通过该工具节省的令牌成本超过每月0.5美元，那么专业版是非常值得的。

**典型节省费用：**
- 小型项目：每月节省2-5美元 → 每月利润1.50-4.5美元
- 中型项目：每月节省10-20美元 → 每月利润9.50-19.5美元
- 大型项目：每月节省50美元以上 → 每月利润49.50美元以上

## 链接

- [文档](README.md)
- [代理支付指南](AGENT-PAYMENTS.md)
- [GitHub仓库](https://github.com/AtlasPA/openclaw-context-optimizer)
- [ClawHub页面](https://clawhub.ai/skills/context-optimizer)

---

**由OpenClaw社区开发** | 首个支持x402支付方式的上下文优化工具
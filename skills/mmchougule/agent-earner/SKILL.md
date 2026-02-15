---
name: agent-earner
version: 1.0.0
description: 您可以通过ClawTasks和OpenWork自主赚取USDC（Uniswap Decentralized Currency）以及各种代币。
author: Prometheus_Prime
tags: [earning, bounties, autonomous, defi, usdc, base]
---

# Agent Earner

**为AI代理提供自主的多平台收入来源。**

通过完成代理经济中的任务来赚取真实货币（Base平台上的USDC以及$OPENWORK代币）。设置好相关参数后，就可以放心等待了——您的代理会自动寻找机会、提交提案并积累声誉，而您无需亲自操心。

## 价值主张

| 未使用Agent Earner | 使用Agent Earner |
|---------------------|-------------------|
| 手动寻找任务 | 每30分钟自动发现新任务 |
| 错失机会 | 24/7全天候监控 |
| 单一平台 | 支持ClawTasks和OpenWork两个平台 |
| 存在资金损失风险 | 首选提案模式（无需投入资金） |
| 手动提交任务 | 任务会自动生成提案 |

## 快速入门

```bash
# 1. Configure credentials
export CLAWTASKS_API_KEY="your_key"
export OPENWORK_API_KEY="ow_your_key"
export CLAWTASKS_WALLET_KEY="0x..." # Optional, for staking

# 2. Start autonomous mode
/clawagent start
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/bounties` | 列出所有可用的任务（✓表示符合代理技能要求） |
| `/bounties propose <id>` | 提交提案（无需投入资金） |
| `/bounties claim <id>` | 提交任务并获得报酬（包含10%的奖励） |
| `/bounties submit <id> <work>` | 提交已完成的任务 |
| `/earnings` | 查看跨平台的收入统计 |
| `/clawagent start\|stop\|status` | 控制代理的自主运行状态 |

## 工作原理

1. **发现任务**：同时扫描ClawTasks和OpenWork平台上的可用任务。
2. **评估任务**：根据代理的技能（写作、编程、研究等）来匹配合适的任务。
3. **生成提案**：自动生成有吸引力的提案。
4. **获得报酬**：一旦提案被选中，代理就会获得报酬（USDC或代币）。

## 配置设置

```json
{
  "clawtasks": {
    "enabled": true,
    "clawtasksApiKey": "your_clawtasks_key",
    "openworkApiKey": "ow_your_openwork_key",
    "walletPrivateKey": "0x...",
    "autonomousMode": true,
    "pollIntervalMinutes": 30,
    "preferProposalMode": true,
    "maxStakePercent": 20
  }
}
```

### 环境变量

```bash
CLAWTASKS_API_KEY=...     # From clawtasks.com/dashboard
OPENWORK_API_KEY=...      # From openwork.bot registration
CLAWTASKS_WALLET_KEY=...  # Base wallet for staking (optional)
```

## 安全性措施

| 安全特性 | 实施方式 |
|---------|---------------|
| 输入验证 | 检查输入数据是否符合UUID格式 |
| 错误处理 | 从日志中删除敏感信息（如密钥） |
| 最小化风险 | 只允许设置固定的奖励金额 |
| 合同验证 | 只允许来自白名单的请求 |
| 请求限制 | 每次请求之间有1秒的延迟 |
| 请求超时 | 最长延迟30秒 |
| 重试机制 | 允许最多3次重试，并逐步增加延迟时间 |

**最佳实践：**
- 使用专门的热钱包，并仅存放少量资金。
- 首先使用提案模式（无需承担资金风险）。
- 将`maxStakePercent`设置得较为保守（默认值为20%）。

## 代理技能

系统会自动匹配以下标签的任务：
- `writing`：内容创作、文章发布、文档编写
- `research`：数据分析、报告撰写、对比分析
- `code`：TypeScript编程、Python开发、自动化脚本
- `creative`：设计任务、命名工作
- `documentation`：API文档编写、用户指南制作
- `automation`：机器人开发、工作流程自动化

## 平台经济体系

### ClawTasks
- 货币：Base平台上的USDC
- 费用：任务完成后收取5%的费用
- 提案模式：免费提交，无需投入资金
- 即时完成模式：需要投入10%的代币，截止时间为24小时

### OpenWork
- 货币：$OPENWORK代币
- 费用：任务完成后收取3%的费用
- 声誉系统：初始声誉为50分，成功完成任务可获得额外加分，失败则扣分
- 竞争机制：多个代理可以竞标同一任务

## 适用于AI代理的工具

```typescript
// Browse opportunities
agent_browse_opportunities({ platform: "all", matchSkills: true })

// Submit work
agent_submit_work({ platform: "clawtasks", id: "...", work: "..." })

// Get stats
agent_get_stats()
```

## 风险与应对措施

| 风险 | 严重程度 | 应对措施 |
|------|----------|------------|
| 资金损失 | 中等 | 首选提案模式（无需投入资金） |
| 任务被拒绝 | 中等 | 通过完成简单任务来积累声誉 |
| 敏感信息泄露 | 严重 | 使用专用钱包并设置严格的环境变量 |
| 请求频率限制 | 低 | 系统内置请求频率限制机制 |

## 技术支持

- ClawTasks：https://clawtasks.com
- OpenWork：https://openwork.bot
- 如有疑问，请通过ClawTasks平台提交问题

---

由**Prometheus_Prime**开发 | 为AI代理提供跨平台收入解决方案
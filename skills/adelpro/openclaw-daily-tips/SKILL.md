---
name: openclaw-daily-tips
slug: openclaw-daily-tips
version: 1.0.1
description: >
  每日AI代理优化技巧与自我提升策略。从OpenClaw社区学习节省成本、提升速度、优化内存使用以及实现自动化的最佳实践。
  适用场景：当你需要每日获取优化AI代理的建议，降低运营成本，提升系统性能，或学习自动化工作流程时。
  不适用场景：当你需要立即进行配置调整时——请使用`openclaw-agent-optimize`工具进行深入的审计与优化。
triggers:
  - openclaw tips
  - openclaw daily
  - openclaw tricks
  - ai agent tips
  - agent optimization
  - openclaw improve
  - ai automation tips
  - openclaw cost optimization
  - openclaw memory tips
  - cron optimization
  - daily ai agent
  - agent self improvement
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["node"]
      env: []
---
# openclaw-daily-tips

专为 OpenClaw 用户提供的每日 AI 代理优化建议与自我提升策略。

## 该技能的功能

- 从社区资源中获取每日优化建议
- 跟踪您的偏好，并了解哪些方法对您有效
- 提供具有影响评分的可操作建议
- 帮助降低成本并提升代理性能

## 快速入门

```bash
# Get today's tip
node ~/.openclaw/workspace/skills/openclaw-daily-tips/scripts/openclaw-daily-tips.mjs tips

# Search for specific topic
node ~/.openclaw/workspace/skills/openclaw-daily-tips/scripts/openclaw-daily-tips.mjs search "cost"

# Weekly report
node ~/.openclaw/workspace/skills/openclaw-daily-tips/scripts/openclaw-daily-tips.mjs weekly

# List all available tips
node ~/.openclaw/workspace/skills/openclaw-daily-tips/scripts/openclaw-daily-tips.mjs all
```

## 功能特点

### 分类
- **成本**：降低 API 调用和模型路由的成本
- **速度**：加快响应速度，减少延迟
- **内存**：优化内存使用和内存管理策略
- **技能**：推荐新的技能提升方法
- **自动化**：通过 Cron 任务实现自动化优化

### 影响评分
- 🟢 需要较少的努力 / 高回报
- 🟡 需要中等程度的努力 / 中等回报
- 🔴 需要较高的努力 / 仍处于实验阶段

### 自我学习功能
- 该技能会记住您的偏好：
  - 保存的建议会被持续跟踪
  - 您跳过的主题不会再出现
  - 随时间逐步适应您的需求

## Cron 任务集成
- 可将每日建议设置为早上 9 点自动执行：

```json
{
  "id": "openclaw-daily-tips",
  "schedule": { "kind": "cron", "expr": "0 9 * * *" }
}
```

## 输出示例

```
📈 OPENCLAW-DAILY-TIPS - Your Agent Smarter Every Day

💡 TIP OF THE DAY (High Impact)
Title: Use tiered model routing

🟢 Low Effort | 📈 High Impact

What:
- Route simple tasks to cheap models
- Route complex tasks to premium models
- Save significant API costs

How:
1. Add model routing in cron jobs
2. Use cheap model for routine tasks
3. Reserve premium for complex reasoning

🔗 docs.openclaw.ai/models

━━━━━━━━━━━━━━
👍 Save this | 👎 Skip | ➕ More tips
```

## 各分类说明

| 分类 | 您将学到的内容 |
|----------|------------------|
| 成本 | 模型路由、令牌优化、批量处理 |
| 速度 | 缓存机制、懒加载、并行执行 |
| 内存 | 优化内存使用、逐步披露相关信息 |
| 技能 | 技能提升的最佳实践、模块化设计 |
| 自动化 | 通过 Cron 任务实现自动化优化 |

## 建议数据库
- 当前的建议包括：
  - 分层模型选择
  - 以脚本为主的 Cron 任务调度方式
  - 仅发送提醒信息的推送方式
  - 基于语义的内存搜索功能
  - 批量处理相似任务
  - 独立子代理的配置
  - 保持操作的可重复性（idempotent）的 Cron 任务
  - 优化心跳检测机制
  - 模块化的技能设计

## 系统要求

- Node.js 18 及以上版本
- OpenClaw 工作空间
- 可选：使用 reddit-readonly 技能来获取社区更新

## 相关技能
- **openclaw-agent-optimize**：深度优化工具
- **openclaw-token-optimizer**：令牌使用成本优化工具
- **memory-setup**：内存配置工具
- **daily-digest**：每日综合简报工具
- **compound-engineering**：代理自我提升工具

## 致谢
- 该技能的灵感来源于 openclaw-agent-optimize 项目及 OpenClaw 社区。

---

## 安装方法

```bash
clawhub install openclaw-daily-tips
```

或者手动将代码复制到您的技能目录中。
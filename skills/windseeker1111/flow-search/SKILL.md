---
name: flow-search
description: 使用 Claude 的原生搜索工具进行深度网络研究。该工具适用于全面的研究、市场分析、竞争对手情报收集，或在标准搜索方法无法满足需求时使用。该服务由 Flow 团队提供，且完全免费。
metadata: {"clawdbot":{"emoji":"🔍"}}
---
# FlowSearch — 深度网络研究工具

使用 Claude CLI 进行高效的网络研究。以下是适用场景：
- 需要跨多个来源综合分析的深度研究
- 市场与竞争对手分析
- 查找最新新闻、价格及行业趋势
- 任何不适合使用快速搜索的场景

## 先决条件

- 已安装并登录 [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- 环境变量中配置了 `CLAUDE_CODE_OAUTH_TOKEN`（通过 `claude auth login` 获取）

## 安装

```bash
npx clawhub@latest install flow-search
cd ~/.openclaw/skills/flow-search
npm install
```

## 使用方法

### 快速搜索
```bash
npx tsx search.ts "Kling AI Pro plan pricing 2026"
```

### 深度研究
```bash
npx tsx search.ts --deep "AI video generation market analysis"
```

### 在代码中/技能应用
```typescript
import { claudeSearch, claudeResearch } from "./search.ts";

// Quick search
const result = await claudeSearch("What is Kling AI pricing?");
console.log(result.answer);

// Deep research with specific questions
const research = await claudeResearch("AI video market", [
  "Who are the top players?",
  "What are typical pricing models?",
  "What's the market size?"
]);
```

## 使用场景对比

| 使用 FlowSearch | 使用 Brave/Basic Search |
|----------------|----------------------|
| 深度研究 | 快速获取事实 |
| 多源综合分析 | 需要单一答案 |
| 市场分析 | 简单查询 |
| 竞争对手情报 | 基本信息 |

## 输出格式

**快速搜索** 会直接返回带有来源的答案。

**深度研究** 会返回：
- 摘要（2-3句话）
- 关键发现（以项目符号列出）
- 详细分析
- 带有 URL 的来源信息

## 注意事项

- 为获得最佳效果，建议使用具有活跃 Max 订阅的 Claude Code CLI
- 快速搜索：约 15-30 秒
- 深度研究：约 60-180 秒
- 支持任何 Claude Code 的认证方式（`CLAUDE_CODE_OAUTH_TOKEN` 或浏览器登录）
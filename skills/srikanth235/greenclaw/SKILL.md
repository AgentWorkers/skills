---
name: greenclaw-usage
description: GreenClaw推理代理的令牌使用分析及预算警报功能：您可以查询令牌使用情况、设置预算警报，并追踪节省的令牌数量。
---
# GreenClaw 使用分析

您可以使用 `greenclaw` 命令行工具来查询令牌使用情况、成本分析以及管理预算警报。通过 `npx greenclaw` 来运行该工具（请先使用 `pnpm install` 和 `pnpm build` 安装依赖）。所有命令的输出均为 JSON 格式。

## 可用命令

### 使用情况查询

**每日汇总：**

```bash
 npx greenclaw usage summary --period day
```

**每周或每月汇总：**

```bash
 npx greenclaw usage summary --period week
 npx greenclaw usage summary --period month
```

**按模型、层级或提供商分类的详细信息：**

```bash
 npx greenclaw usage breakdown --by model --period day
 npx greenclaw usage breakdown --by tier --period week
 npx greenclaw usage breakdown --by provider --period month
```

**随时间变化的趋势：**

```bash
 npx greenclaw usage trends --period day --last 7
 npx greenclaw usage trends --period week --last 4
```

### 预算警报

**列出警报规则：**

```bash
 npx greenclaw alerts list
```

**设置每日成本预算：**

```bash
 npx greenclaw alerts set --name "daily budget" --metric daily_cost --threshold 50 --unit usd --period day
```

**设置每周令牌使用上限：**

```bash
 npx greenclaw alerts set --name "weekly tokens" --metric weekly_cost --threshold 100 --unit usd --period week
```

**设置每模型的成本上限：**

```bash
 npx greenclaw alerts set --name "gpt-4 cap" --metric per_model_cost --threshold 30 --unit usd --period day --model gpt-4
```

**立即检查警报：**

```bash
 npx greenclaw alerts check
```

**查看警报历史记录：**

```bash
 npx greenclaw alerts history --last 10
```

**删除警报规则：**

```bash
 npx greenclaw alerts remove <rule-id>
```

### 原始追踪数据

**汇总统计数据：**

```bash
 npx greenclaw traces --stats
```

**按层级或模型筛选数据：**

```bash
 npx greenclaw traces --tier HEARTBEAT
 npx greenclaw traces --model gpt-4o-mini
```

## 结果展示方式

- 解析 JSON 输出，并以清晰、易读的格式呈现结果
- 对于汇总数据：显示总令牌数、成本、节省金额以及请求数量
- 对于详细数据：以表格形式展示分组键、令牌数、成本和节省金额
- 对于警报信息：说明哪些规则被触发以及当前的指标值
- 将金额四舍五入到小数点后两位
- 用自然语言解释节省情况（例如：“通过将 412 个请求路由到更便宜的模型，您今天节省了 8.91 美元”）

## 环境设置

`greenclaw` 命令行工具使用 `GREENCLAW_TELEMETRY_DB` 环境变量来指定 SQLite 数据库的路径（默认为 `data/telemetry.db`）。
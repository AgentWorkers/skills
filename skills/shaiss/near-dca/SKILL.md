---
name: near-dca
description: **NEAR代币的美元成本平均策略**：支持灵活的调度安排、性能跟踪以及取消功能。
---
# NEAR DCA 技能

用于 NEAR 代币的美元成本平均（Dollar-Cost Averaging, DCA）投资功能。

## 描述

该技能提供了灵活的定时投资（DCA）功能以及投资绩效的跟踪能力。用户可以设置定期购买 NEAR 代币的计划，并随时间推移监控投资表现。

## 主要功能

- 创建 DCA 计划
- 取消 DCA 计划
- 查看所有 DCA 计划
- 跟踪 DCA 投资表现
- 灵活的定时选项（每日、每周等）

## 命令

### `near-dca create <token> <amount> <schedule> [account]`
创建一个新的 DCA 计划。

**参数：**
- `token` - 要购买的代币（例如：NEAR、USDT）
- `amount` - 每次购买的金额
- `schedule` - 定时频率：每日、每周、每两周、每月
- `account` - 账户 ID（可选，使用默认值）

**示例：**
```bash
near-dca create USDT 10 daily myaccount.near
```

### `near-dca list [account]`
列出某个账户的所有 DCA 计划。

### `near-dca cancel <plan_id>`
取消一个 DCA 计划。

### `near-dca performance <plan_id>`
显示某个 DCA 计划的投资表现。

### `near-dca history <plan_id>`
显示某个 DCA 计划的购买历史记录。

## 配置

DCA 计划存储在 `~/.near-dca/plans.json` 文件中。

## 注意事项

- DCA 功能的实现需要与去中心化交易所（DEX）（如 Ref Finance）集成。
- 定时执行需要使用 cron 任务或作业调度器。
- 该功能用于对比定期投资与一次性投资的绩效。

## 参考资料

- NEAR DeFi：https://near.org/defi/
- Ref Finance：https://ref.finance/
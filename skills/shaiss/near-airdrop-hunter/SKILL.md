---
name: near-airdrop-hunter
description: 发现附近的空投活动，查看参与资格，领取奖励，并在多个平台上追踪已领取的空投物品。
---
# NEAR Airdrop Hunter 技能

该技能可帮助您自动发现、检查资格并领取 NEAR 的空投奖励。

## 描述

此技能可帮助您发现正在进行的 NEAR 空投活动，检查特定空投的领取资格，领取符合条件的空投奖励，并在多个平台上跟踪已领取的空投记录。

## 功能

- 发现正在进行的 NEAR 空投活动
- 检查空投的领取资格
- 领取符合条件的空投奖励
- 跟踪已领取的空投奖励
- 支持跨多个平台进行扫描

## 命令

### `near-airdrop discover [platform]`
发现正在进行的 NEAR 空投活动。

**参数：**
- `platform` - 按平台筛选（可选：aurora、ref、all）

### `near-airdrop check <account_id> <airdrop_id>`
检查特定空投的领取资格。

**参数：**
- `account_id` - 需要检查资格的 NEAR 账户
- `airdrop_id` - 需要检查领取资格的空投 ID

### `near-airdrop claim <account_id> <airdrop_id>`
领取符合条件的空投奖励。

**参数：**
- `account_id` - 需要领取空投奖励的 NEAR 账户
- `airdrop_id` - 需要领取的空投 ID

### `near-airdrop list [account_id]`
列出该账户已领取的所有空投奖励。

### `near-airdrop track [account_id]`
跟踪该账户的所有空投活动及其状态。

## 配置

跟踪数据存储在 `~/.near-airdrop/tracking.json` 文件中。

## 注意事项

- 空投的可用性因协议而异
- 有些空投需要持有特定的代币才能领取
- 领取前请务必检查资格
- 请始终验证空投的合法性

## 参考资料

- NEAR 生态系统：https://near.org/ecosystem/
- NEAR 空投活动：https://near.org/airdrops/
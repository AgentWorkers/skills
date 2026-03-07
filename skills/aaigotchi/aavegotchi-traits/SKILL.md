---
name: aavegotchi-traits
description: 在 Base 平台上，可以通过 Aavegotchi 的 ID 或名称检索其 NFT 数据。检索结果包括该 NFT 的特性（traits）、可穿戴物品（wearables）、稀有度评分（rarity scores）、亲缘关系（kinship）、经验值（XP）、等级（level）以及所有者信息（owner data）。
---
# Aavegotchi 特性

可以通过 ID 或名称获取 Aavegotchi 的相关信息。

## 使用方法

```bash
cd scripts
node get-gotchi.js 9638
node get-gotchi.js aaigotchi
./gotchi-info.sh 9638
```

## 返回内容

- 代币 ID、名称、所有者、所属类别（haunt）
- BRS（Base Reward Score）/ 修改后的 BRS 值
- 亲缘关系（kinship）、经验值（XP）、等级（level）
- 基础属性（Base）及修改后的特性
- 佩戴的装备及其名称
- 抵押物（collateral）、质押金额（staked amount）、最后一次交互时间（last interaction）
- 以 JSON 格式输出的数据（适用于自动化处理）

## 环境配置参数

- `AAVEGOTCHI_RPC_URL`（可选）
- `AAVEGOTCHI_SUBGRAPH_URL`（可选；默认为 Goldsky Base 子图）
- `AAVEGOTCHI_SEARCH_BATCH_SIZE`（可选）
- `AAVEGOTCHI_RPC_RETRIES`（可选）
- `AAVEGOTCHI_RPC_RETRY_DELAY_MS`（可选）

## 可靠性说明

- 名称查询首先通过子图进行，以提高查询速度；
- 如果子图查询失败，脚本会通过 RPC 重试机制在链上直接进行查询，并设置重试间隔（backoff）以应对请求速率限制。
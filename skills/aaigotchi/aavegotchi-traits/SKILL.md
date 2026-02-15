---
name: aavegotchi-traits
description: 从 Base 主网中根据 Aavegotchi 的 ID 或名称检索其 NFT 数据。可以获取以下信息：特性（BRS、亲缘关系、经验值、能量值、攻击性、恐惧程度、大脑大小、眼睛形状、眼睛颜色）、佩戴的饰品、被“纠缠”的次数（haunt number）、等级以及年龄。当用户询问特定 Aavegotchi 的统计数据、特性、佩戴的饰品、稀有度评分或与 Aavegotchi 相关的任何信息时，可以使用此功能。支持通过 The Graph 子图（如果可用）进行即时 ID 查找或名称搜索；在无法使用 The Graph 时，会采用链上查询方式作为备用方案。
---

# Aavegotchi 特性

该脚本可以从 Base 主网上获取 Aavegotchi NFT 的详细链上数据，并支持通过子图（subgraph）快速查找 NFT 的名称。

## 快速入门

- 通过 ID 或名称获取 Aavegotchi 的数据：

```bash
# By ID
cd scripts && node get-gotchi.js 9638  # aaigotchi

# By name
cd scripts && node get-gotchi.js "aaigotchi"
```

脚本输出：
1. 适合人类阅读的格式化结果
2. 用于编程的 JSON 对象

## 子图支持（The Graph）

该脚本支持 **The Graph** 子图，可以快速查找 NFT 的名称：

### 当前状态（2026 年 2 月）

⚠️ **目前尚无 Base 子图可用。** Aavegotchi 于 2025 年 7 月迁移到了 Base 主网，但官方的子图尚未部署。因此，脚本会自动回退到链上扫描方式。

### 子图可用时

- 通过环境变量设置子图端点：

```bash
export AAVEGOTCHI_SUBGRAPH_URL=https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-base
```

- 或在您的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中设置：

```bash
echo 'export AAVEGOTCHI_SUBGRAPH_URL=https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-base' >> ~/.bashrc
source ~/.bashrc
```

配置子图后：
- **名称查找：** 可以通过 GraphQL 查询立即完成
- **ID 查找：** 仍然依赖链上数据（获取完整特性信息最可靠）

### 查找策略

```
ID lookup (#9638 - aaigotchi)
  └─> Direct on-chain query (instant)

Name lookup ("aaigotchi" - #9638)  
  ├─> Try subgraph (instant, if available)
  └─> Fall back to on-chain scan (30-60s)
```

## 获取的数据

对于任何 Aavegotchi 代币 ID，脚本会获取以下信息：

**核心数据：**
- Base 稀有度得分（BRS）
- 经过可穿戴物品修改后的稀有度得分
- 亲缘关系等级
- 经验值（XP）
- 等级

**特性（6 个数值）：**
- ⚡ 能量（NRG）
- 💥 攻击性（AGG）
- 👻 可怖程度（SPK）
- 🧠 大脑大小（BRN）
- 👁️ 眼睛形状（EYS）
- 🎨 眼睛颜色（EYC）

每个特性的值都会显示基础值和经过可穿戴物品修改后的值。

**可穿戴物品：**
- 列出所有已装备的可穿戴物品及其 ID 和名称
- 格式：`ID: 名称`（例如：“50: GldnXross Robe”
- 空闲的装备槽会被过滤掉
- 包括装备的数量

**身份信息：**
- 代币 ID
- 名称（如果已设置）
- 所有者地址
- 出没地点（Haunt）

**质押信息：**
- 抵押代币地址
- 抵押金额
- 最后交互时间戳
- 年龄（自上次交互以来的天数）

## 使用方法

- **按 ID 查找：**

```bash
cd scripts && node get-gotchi.js 9638  # aaigotchi
```

- **按名称查找：**

```bash
cd scripts && node get-gotchi.js "aaigotchi"
cd scripts && node get-gotchi.js "Slide"
cd scripts && node get-gotchi.js "XIBOT"
```

**性能：**
- 使用子图时：**立即完成**
- 不使用子图时：**需要 30-60 秒（扫描所有 Aavegotchi）

💡 **提示：** 尽可能使用代币 ID，以确保立即获得结果。

## 示例输出

```
============================================================
AAVEGOTCHI #9638: aaigotchi
============================================================
Owner: 0x8BE974bC760bea450A733c58B051c14F723ce79C
Haunt: 1
Level: 8
Age: 0 days since last interaction

SCORES:
  Base Rarity Score (BRS): 475
  Modified Rarity Score: 475
  Kinship: 2276
  Experience: 2960

TRAITS:
  ⚡ Energy: 0
  💥 Aggression: 66
  👻 Spookiness: 99
  🧠 Brain Size: 76
  👁️ Eye Shape: 41
  🎨 Eye Color: 28

WEARABLES:
  Equipped (1):
    210: Haunt 1 Background

STAKING:
  Collateral: 0x20D3922b4a1A8560E1aC99FBA4faDe0c849e2142
  Staked Amount: 0.0 tokens
  Last Interacted: 2026-02-12T18:30:13.000Z
============================================================

JSON OUTPUT:
{
  "tokenId": "9638",
  "name": "aaigotchi",
  ...
}
```

## 合同详情

- **合同地址：** `0xa99c4b08201f2913db8d28e71d020c4298f29dbf`（Base 主网）
- **网络：** Base（链 ID：8453）
- **RPC 请求地址：** `https://mainnet.base.org`

## 数据解析

有关特性的详细解释、BRS、亲缘关系、可穿戴物品、出没地点等 Aavegotchi 机制的更多信息，请参阅：

**参考文档：** [references/aavegotchi-data.md](references/aavegotchi-data.md)

## 所需环境：

- Node.js（版本 18 及以上）
- npm 包：`ethers`、`node-fetch`（通过 `package.json` 安装）
- 互联网连接（用于查询 Base RPC 和可选的 The Graph）
- 可穿戴物品数据文件（包含 400 多个物品的 `wearables-data.json`）

依赖项和数据文件已预先安装在脚本目录中。

## 故障排除：

- **“无效的代币 ID”错误：**
  - 该 Aavegotchi 代币在 Base 主网上不存在，请检查 ID 是否正确。
- **网络错误：**
  - 检查互联网连接是否正常
  - Base 的 RPC 服务可能暂时不可用，请稍后再试。
- **名称查找耗时过长：**
  - **使用子图时：** 确保 `AAVEGOTCHI_SUBGRAPH_URL` 设置正确。
  - **不使用子图时：** 名称搜索会顺序扫描所有 23,000 多个 Aavegotchi（耗时 30-60 秒）。
  - 使用代币 ID 可以立即获得结果。
  - 确保互联网连接稳定。

## 未来改进计划：

- ✅ **The Graph 子图支持**（已实现，等待 Base 子图正式部署）
- ✅ **可穿戴物品名称的解析**（已实现，已映射 400 多种可穿戴物品）
- 批量查询多个 Aavegotchi
- 历史特性/亲缘关系记录
- 可穿戴物品的稀有度/统计信息显示
- 查看口袋/库存中的物品
- 公会/借贷信息
- 实时显示宠物的状态
- 特性的稀有度百分位数
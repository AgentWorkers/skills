---
name: rugcheck
description: >
  Analyze Solana tokens for rug pull risks using the RugCheck API (rugcheck.xyz).
  Use when asked to check a Solana token safety, risk score, liquidity, holder
  distribution, metadata mutability, or insider trading patterns. Also use for
  discovering trending, new, or recently verified Solana tokens. Triggers on
  token check, rug check, token safety, Solana token analysis, is this token safe,
  token risk score, LP locked, holder concentration.
---

# RugCheck — Solana代币风险分析

您可以使用免费的RugCheck API，通过代币的铸造地址来分析任何Solana代币。读取数据端点无需API密钥。

## 快速入门

```bash
# Get risk summary (score + flags)
bash scripts/rugcheck.sh summary <MINT_ADDRESS>

# Get full detailed report (holders, markets, metadata, LP)
bash scripts/rugcheck.sh report <MINT_ADDRESS>
```

## 脚本参考

运行 `bash scripts/rugcheck.sh help` 可以查看所有命令的详细信息：

| 命令 | 描述 |
|---------|-------------|
| `summary <mint>` | 风险评分（0-100分，已标准化），风险标志，锁定流动性（LP）百分比 |
| `report <mint>` | 完整报告：元数据、持有者信息、市场信息、创建者信息 |
| `insiders <mint>` | 持有者/关联钱包关系图 |
| `lockers <mint>` | LP（锁定流动性）信息 |
| `votes <mint>` | 社区对代币的投票情况 |
| `leaderboard` | 平台上的顶级投票者/分析师 |
| `domains` | 已注册的Solana域名 |
| `trending` | 过去24小时内投票最多的代币 |
| `new` | 最新检测到的代币 |
| `recent` | 过去24小时内浏览量最高的代币 |
| `verified` | 最新经过验证的代币 |

## 解读结果

### 总结响应

来自 `/v1/tokens/{mint}/report/summary` 的关键字段：

- **`score_normalised`** — 风险评分（0-100分）。分数越高，风险越大。原始分数低于1000分表示“风险较低”。
  - 0-30：低风险（良好）
  - 30-60：中等风险（需谨慎）
  - 60-100：高风险（危险）
- **`risks[]`** — 风险标志数组，每个标志包含：
  - `name`：风险类型（例如：“可修改的元数据”、“流动性低”、“单一持有者持有”）
  - `level`：`"warn"` 或 `"danger"`
  - `value`：人类可读的详细信息（例如：“$102.55”，“40.00%”）
  - `description`：风险说明
  - `score`：风险的贡献度（原始分数）
- **`lpLockedPct`** — 被锁定的LP代币百分比（0表示未锁定，风险极高）
- **`tokenProgram`** — 使用的SPL代币程序
- **`tokenType`** — 代币类型分类

### 完整报告响应

来自 `/v1/tokens/{mint}/report` 的其他字段：

- **`tokenMeta`** — 代币名称、符号、URI、`mutable`标志、`updateAuthority`
- **`token`** — 代币总量、小数位数、`mintAuthority`、`freezeAuthority`
- **`creator`** / `creatorBalance` — 代币创建者及其当前余额
- **`topHolders[]` — 最大持有者信息（包括地址、持有者、持有比例、持有量）
- **`markets[]` — 提供流动性的DEX市场/池信息
- **`insiderNetworks`** — 关联的内部者钱包集群

## 风险警示

在分析代币时，需向用户提示以下风险：

1. **可修改的元数据**（`tokenMetamutable == true`）——创建者可以更改代币名称或图像
2. **流动性低**（风险标志为“Low Liquidity”或查看市场数据）——价格容易被操纵
3. **持有者高度集中**——前10名持有者持有超过50%的代币总量
4. **单一持有者主导**——单个钱包持有超过20%的代币总量
5. **LP未锁定**（`lpLockedPct == 0`）——创建者可以随时提取流动性
6. **存在铸造权限**（`token.mintAuthority != null`）——可以无限铸造代币
7. **存在冻结权限**（`token.freezeAuthority != null`）——可以冻结钱包
8. **LP提供者少**——只有1-2个钱包提供流动性
9. **交易量低/为零**——市场活动极少
10. **创建者持有大量代币**——创建者仍持有大部分代币

## 显示结果

以清晰的方式向用户展示分析结果。示例：

```
🔍 RugCheck Analysis: CLWDN (ClawdNation)
Mint: 3zvSRWfjPvcnt8wfTrKhgCtQVwVSrYfBY6g1jPwzfHJG

⚠️ Risk Score: 59/100 (Medium-High Risk)

🚩 Risk Flags:
  🔴 Low Liquidity — $102.55
  ⚠️ Single holder ownership — 40.00%
  ⚠️ High holder concentration — Top 10 hold >50%
  ⚠️ Low amount of holders
  ⚠️ Low LP providers
  ⚠️ Mutable metadata

🔓 LP Locked: 0% (NOT LOCKED)

📊 Top Holders:
  1. 40.0% — 3Y3g...p7rk
  2. 15.0% — 5bNH...4VGj
  3. 15.0% — 4dkX...Ncg6
  4. 10.0% — 8yY2...CKn8
  5. 10.0% — 2MT5...eB3h

Verdict: HIGH RISK — Multiple red flags. No locked liquidity,
concentrated holdings, mutable metadata. Exercise extreme caution.
```

## API详情

- **基础URL：** `https://api.rugcheck.xyz`
- **认证：** 读取数据端点无需认证
- **速率限制：** 每次请求最多429条响应；批量查询之间需间隔2-3秒
- **RugCheck网站：** `https://rugcheck.xyz/tokens/<mint>`（用户访问链接）

## 批量查询（需要认证）

这些端点需要Solana钱包的JWT认证——大多数代理无法使用：

- `POST /v1/bulk/tokens/summary` — 同时检查多个代币
- `POST /v1/bulk/tokens/report` — 获取多个代币的完整报告
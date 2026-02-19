---
name: n0ir-defi-yield-scout
description: n0ir DeFi Yield Scout — built by n0ir Labs (n0ir.ai). Scan and compare USDC yield farming opportunities across Base and Arbitrum using the same protocol set as n0ir's autonomous yield agent. Find best APY rates, compare vault yields, and analyze historical performance via DeFiLlama. Covers n0ir-whitelisted protocols: Morpho, Euler v2, Aave v3, Compound v3, Moonwell, Silo v2, Lazy Summer, Harvest Finance, 40 Acres, Wasabi, Yo Protocol. Use for yield farming comparison, stablecoin returns, USDC rates, vault APY ranking, breakeven analysis, APY trend history, protocol risk overview, DeFi yield optimization, n0ir vault strategy, ERC-4626 vault comparison, TVL-weighted ranking, cross-chain yield comparison, gas-adjusted net returns.
allowed-tools: Read, Bash, Glob
user-invocable: true
argument-hint: "[scan|breakeven|history|protocols] [options]"
---

# n0ir DeFi Yield Scout — 使用说明

n0ir DeFi Yield Scout 是由 n0ir Labs (https://n0ir.ai) 开发的一款工具，旨在帮助用户查找并比较基于 Base 和 Arbitrum 链路的 USDC 收益 farming 机会。该工具使用与 n0ir 的自动化收益管理工具相同的协议集，并实时获取 DeFiLlama 提供的数据。

## 工具

命令行工具的文件路径为 `scripts/yield_scout.py`（相对于当前工具的目录）。使用 `python3` 命令来运行该工具。

## 子命令

### `scan` — USDC 收益排行榜

获取当前的 USDC 池数据，并按年化收益率（APY）排序显示结果。

**默认输出示例：**
（此处应展示实际的排行榜表格）

- 以清晰的表格形式呈现结果。
- 突出显示最佳投资选项。
- 说明 TVL（总价值锁定）和风险因素。

### `breakeven` — 金库比较与迁移分析

比较两个金库，判断是否值得进行迁移。

**输出内容包括：**
- 两个金库的当前年化收益率（APY）
- 净年化收益增长百分比
- 预计的交易手续费（同链交易为 1%，跨链交易为 3%）
- 达到盈亏平衡所需的天数
- n0ir 的评估结果：**建议迁移**（< 30 天），**可能值得**（30–90 天），**不建议迁移**（> 90 天）

- 明显显示评估结果，并解释判断依据。

### `history` — 收益率趋势与稳定性分析

显示特定池在过去 30 天内的收益率变化情况。

**输出内容包括：**
- 过去 30 天内的最高、最低和平均年化收益率
- 稳定性评分（基于标准差）
- 收益率变化的 ASCII 图表
- TVL（总价值锁定）的变化趋势

- 解释稳定性评分的含义以及该收益的可靠性。

### `protocols` — 协议信息

展示已列出的协议概览。

**输出内容包括：**
- 协议名称、支持的链路、金库标准、审计状态、风险提示

如需更详细的协议信息，请参阅 `references/protocols.md`。

## 语言指令映射

用户输入的指令与对应的子命令如下：

| 用户输入                      | 执行命令                                      |
|----------------------------------|------------------------------------------|
| “查找最佳 USDC 收益”                | `scan`                                   |
| “查看 Base 链路的收益”                | `scan --chain Base`                       |
| “查看 Morpho 协议的收益”              | `scan --protocol morpho-v1`               |
| “是否应该更换金库”                | `breakeven --from-pool ... --to-pool ...`         |
| “是否值得迁移”                  | `breakeven` （如需可提供池 ID）                |
| “查看收益率历史”                | `history --pool ...`                      |
| “有哪些支持的协议”                | `protocols`                               |
| “查看 Arbitrum 链路的收益”            | `scan --chain Arbitrum`                   |
| “仅选择 TVL 较高的金库”              | `scan --min-tvl 10000000`                 |

## 回答指南

1. **始终先运行工具** — 不要直接猜测收益率或费用。
2. **先展示结果** — 先显示排行榜或评估结果，再做解释。
3. **提示风险** — 如果某个池的风险较高或 TVL 较低，需提醒用户。
4. **提供下一步建议** — 扫描完成后，建议用户进行收益对比；在判断是否迁移时，需考虑交易手续费。
5. **使用 `--json` 参数** — 当用户需要数据或进一步分析时使用该参数。
6. **提供池 ID** — 在展示扫描结果时，告知用户可以使用这些 ID 来执行 `breakeven` 和 `history` 命令。

## 注意事项

- 数据来源于 DeFiLlama（免费，无需 API 密钥）。收益率数据为实时快照。
- 该工具会缓存池数据 15 分钟，以减少数据重复请求带来的负担（约 12MB 的数据量）。
- 交易手续费估算仅供参考（同链交易为 1%，跨链交易为 3%）。实际费用可能有所不同。
- 本工具仅提供信息参考，不构成财务建议。用户应在实际操作前自行在链上验证数据。
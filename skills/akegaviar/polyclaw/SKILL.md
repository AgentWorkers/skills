---
name: polyclaw
description: "在 Polymarket 上进行交易，支持拆分交易（split transactions）和 CLOB（Centralized Order Book）执行方式。您可以浏览市场、查看持仓及盈亏情况（P&L），并通过大型语言模型（LLM）发现对冲策略。所有交易均基于 Polygon 和 Web3 技术框架进行。"
metadata: {"openclaw":{"emoji":"🦞","homepage":"https://polymarket.com","primaryEnv":"POLYCLAW_PRIVATE_KEY","requires":{"bins":["uv"],"env":["CHAINSTACK_NODE","POLYCLAW_PRIVATE_KEY"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]},"clawdbot":{"emoji":"🦞","homepage":"https://polymarket.com","primaryEnv":"POLYCLAW_PRIVATE_KEY","requires":{"bins":["uv"],"env":["CHAINSTACK_NODE","POLYCLAW_PRIVATE_KEY"]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# PolyClaw

这是一个专为 OpenClaw 设计的 Polymarket 技能，支持交易功能。用户可以浏览市场、管理钱包、执行交易并跟踪持仓情况。

## 主要功能

- **市场浏览** - 在 Polymarket 预测市场中搜索和浏览交易机会。
- **钱包管理** - 根据环境变量配置钱包设置。
- **交易** - 通过 CTF（Conditional Tokens）合约将 USDC.e 分割为 “YES” 和 “NO” 两种类型的代币，然后进行买卖操作。
- **持仓跟踪** - 记录买入价格、当前价格以及盈亏情况。
- **对冲策略发现** - 利用大型语言模型（LLM）通过逻辑推理帮助用户发现具有对冲效果的投资组合。

## 快速入门

首先，从技能目录中安装所需依赖项：

```bash
cd {baseDir}
uv sync
```

### 首次使用（交易前必做）

在进行首次交易之前，需要设置 Polymarket 合同的审批权限（只需执行一次，费用约为 0.01 POL 的 Gas 费用）：

```bash
uv run python scripts/polyclaw.py wallet approve
```

此操作会向 Polygon 提交 6 条审批交易记录。每个钱包只需执行一次即可。

### 浏览市场

```bash
# Trending markets by volume
uv run python scripts/polyclaw.py markets trending

# Search markets
uv run python scripts/polyclaw.py markets search "election"

# Market details (returns full JSON with all fields)
uv run python scripts/polyclaw.py market <market_id>
```

**输出选项：**
- 默认输出为格式化的表格，适合查看。
- 使用 `--full` 标志可查看完整的交易信息（无截断）。
- 使用 `--json` 标志（通过 `scripts/markets.py --json trending` 命令）可获取结构化的 JSON 输出。

### 钱包管理

```bash
# Check wallet status (address, balances)
uv run python scripts/polyclaw.py wallet status

# Set contract approvals (one-time)
uv run python scripts/polyclaw.py wallet approve
```

钱包配置通过 `POLYCLAW_PRIVATE_KEY` 环境变量完成。

### 交易

```bash
# Buy YES position for $50
uv run python scripts/polyclaw.py buy <market_id> YES 50

# Buy NO position for $25
uv run python scripts/polyclaw.py buy <market_id> NO 25
```

### 持仓情况

```bash
# List all positions with P&L
uv run python scripts/polyclaw.py positions
```

### 对冲策略发现

通过逻辑推理找到具有对冲效果的投资组合（即能够相互抵消风险的市场持仓组合）。

```bash
# Scan trending markets for hedges
uv run python scripts/polyclaw.py hedge scan

# Scan markets matching a query
uv run python scripts/polyclaw.py hedge scan --query "election"

# Analyze specific markets for hedging relationship
uv run python scripts/polyclaw.py hedge analyze <market_id_1> <market_id_2>
```

**输出选项：**
- 默认输出为格式化的表格，显示层级、对冲比例、成本、目标和对冲效果。
- 使用 `--json` 标志可获取结构化的 JSON 输出。
- 使用 `--min-coverage 0.90` 可按最小对冲比例筛选（默认值为 0.85）。
- 使用 `--tier 1` 可按对冲层级筛选（1=最佳效果，默认为 2）。

**对冲层级：**
- **层级 1（高）：** 对冲比例 >=95% - 几乎无风险的投资机会。
- **层级 2（良好）：** 90-95% - 较强的对冲效果。
- **层级 3（中等）：** 85-90% - 对冲效果一般但存在一定风险。
- **层级 4（低）：** <85% - 投机性较高（默认被过滤掉）。

**使用的 LLM 模型：** `nvidia/nemotron-nano-9b-v2:free`（通过 OpenRouter 提供）。模型选择很重要——某些模型可能产生错误的相关性，而某些模型（如 DeepSeek R1）可能存在输出格式问题。如需更换模型，可以使用 `--model <model_id>` 参数。

## 安全性

在 MVP 版本中，为简化操作并确保与 Claude Code 兼容，私钥存储在环境变量中。

**安全提示：** 请在此钱包中仅存放少量资金，并定期将其转移至更安全的钱包。

## 环境变量

| 变量          | 是否必填 | 说明                          |
|----------------|---------|---------------------------------------------|
| `CHAINSTACK_NODE`    | 是       | Polygon 的 RPC URL                        |
| `OPENROUTER_API_KEY`    | 是       | 用于 LLM 对冲策略发现的 OpenRouter API 密钥            |
| `POLYCLAW_PRIVATE_KEY` | 是       | EVM 私钥（十六进制格式，可带或不带前缀 0x）            |
| `HTTPS_PROXY`     | 推荐     | 用于 CLOB 请求的轮询代理服务器（例如 IPRoyal）            |
| `CLOB_MAX_RETRIES`    | 否       | CLOB 请求的最大重试次数（默认值：5）                     |

**安全提示：** 请在此钱包中仅存放少量资金，并定期将其转移至更安全的钱包。虽然环境变量中的私钥便于自动化操作，但安全性较低。

## 交易流程

1. **分割持仓** - 使用 CTF 合约将 USDC.e 分割为 “YES” 和 “NO” 两种类型的代币。
2. **出售不需要的代币** - 通过 CLOB 订单簿出售不需要的代币。
3. **结果** - 最终你将持有所需的代币，并从出售不需要的代币中收回部分成本。

**示例：** 以 $0.70 的价格买入 “YES” 代币：
- 将 100 USDC.e 分割为 100 “YES” 和 100 “NO” 代币。
- 以约 $0.30 的价格出售 100 “NO” 代币，收回约 $27 的收益。
- 实际成本：购买 100 “YES” 代币的成本约为 $73。

## Polymarket 合约（Polygon 主网）

- **USDC.e：** `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`
- **CTF（Conditional Tokens）：** `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045`
- **CTF 交换合约：** `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E`

## 依赖项安装

使用 `uv` 工具（从技能目录中安装依赖项）：

```bash
cd {baseDir}
uv sync
```

## 限制

- 交易前需要设置钱包审批权限（仅一次）。
- 如果市场流动性不足，CLOB 交易可能会失败。

### CLOB 与 Cloudflare 的问题

Polymarket 的 CLOB API 使用 Cloudflare 进行防护，会阻止来自某些 IP 地址的 POST 请求（包括数据中心 IP 和部分家用 ISP）。这可能会影响 “出售不需要的代币” 的操作。

**解决方案：** 使用轮询代理服务器（例如 IPRoyal 或 BrightData）。

**推荐设置：** CLOB 客户端会自动尝试使用不同的代理服务器，直到找到可用的代理为止。通常在 5-10 次尝试后即可成功。

**其他解决方法：**
1. **使用 `--skip-sell` 标志** - 保留 “YES” 和 “NO” 两种类型的代币，手动在 Polymarket.com 上进行交易。
2. **不使用代理** - 分割操作仍然可以执行，仅 CLOB 销售功能会受到影响。

如果所有尝试均失败，你的交易操作仍然有效。系统会提示你需要手动出售多少代币。

## 常见问题及解决方法

### “无法找到钱包”
请设置 `POLYCLAW_PRIVATE_KEY` 环境变量：

```bash
export POLYCLAW_PRIVATE_KEY="0x..."
```

### “USDC.e 数量不足”
使用 `uv run python scripts/polyclaw.py wallet status` 命令检查钱包余额。确保你的钱包中有足够的 USDC.e（已桥接的 USDC）。

### “CLOB 订单失败”
CLOB 销售失败可能的原因：
- 销售价格处的流动性不足。
- IP 被 Cloudflare 阻止（尝试使用代理服务器）。

即使 CLOB 失败，你的交易操作仍然有效——你仍然拥有所需的代币，只是无法出售不需要的部分。

### “未设置合同审批权限”
首次交易前需要设置合同审批权限。请运行以下命令：

```bash
uv run python scripts/polyclaw.py wallet approve
```

## 许可证

MIT 许可证。
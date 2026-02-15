---
name: tradr
description: **On-chain Trade Execution Engine**  
该引擎支持基于证书（CA）的验证机制，并能够处理交易的完整生命周期：包括交易规模的确定、根据交易模式选择退出策略、在链上进行交易验证以及记录交易详情。使用该引擎需要具备 Bankr 技能。
dependencies:
  - bankr
---

# tradr

这是一个完全基于链上的交易执行引擎。您提供交易信号，tradr负责处理其余的所有事务。

**输入：** 合同地址 + 评分（score）
**输出：** 买入 → 监控 → 退出（自动化执行）

tradr不生成交易信号，也不对“买入什么”提供任何建议；它只负责“买入后如何管理交易”的策略。

## 快速入门

```bash
# 1. Install
./scripts/setup.sh

# 2. Edit config
vi config.json    # Add wallet addresses, tune scoring/modes

# 3. Start the exit manager daemon
sudo systemctl start tradr-exit-manager

# 4. Feed a trade
python3 scripts/tradr-enter.py <CA> --score <N> [--chain base] [--mode snipe]
```

## 从零开始

### 先决条件
- **OpenClaw** 已经运行（作为代理运行时环境）
- **Bankr 技能** 已安装（位于 `~/.openclaw/skills/bankr/`），并拥有有效的 API 密钥——该技能负责执行链上交易。请在 [bankr_bot](https://bankr.bot) 注册以获取 API 密钥，然后将其添加到 `~/.openclaw/skills/bankr/config.json` 中。
- **Python 3.8+** 和 `jq` 工具已安装。
- 拥有一个已充值的钱包（支持 Solana 和/或 EVM 链路）——Bankr 会在支持的链路上为您创建钱包。在交易前请确保钱包已充值。

### 分步操作
1. **安装 tradr：**
   ```bash
   cd ~/.openclaw/skills/tradr   # or wherever you unpacked the skill
   ./scripts/setup.sh            # creates config, installs systemd service
   ```

2. **配置您的钱包：**
   修改 `config.json` 文件，在 `wallets` 部分添加您的钱包地址。这些地址仅用于链上余额验证（tradr 从不访问您的私钥）。

3. **调整您的交易策略：**
   - `score_to_size`：在每个置信度水平下应投入的 USD 金额。
   - `modes`：退出行为配置（止损、止盈、跟踪止损）。
   - `mcap_ceiling_usd`：允许进入交易的最大市值。

4. **启动退出管理器：**
   ```bash
   sudo systemctl start tradr-exit-manager
   sudo systemctl status tradr-exit-manager  # verify it's running
   ```

5. **连接交易信号源：**
   tradr 不生成交易信号——您需要自己提供信号。请参阅 `adapters/README.md` 以了解接口规范，以及 `adapters/example-adapter.py` 作为示例模板。

   或者您可以手动输入交易指令：
   ```bash
   python3 scripts/tradr-enter.py 0xABC... --score 5 --chain base --token PEPE
   ```

6. **通过仪表板进行监控：**
   `dashboard/index.html` 文件提供了实时监控界面。它需要四个 API 端点：
   - `GET /api/positions` — 返回 `positions.json` 的内容。
   - `GET /api/trades` — 以 JSON 数组形式返回交易日志（`trade-log.jsonl`）。
   - `GET /api/tradr-config` — 返回 `config.json` 的内容。
   - `GET /api/health` — 返回系统状态（可选）。

   您可以从任何能够读取这些 JSON 文件的 HTTP 服务器提供这些接口，或者将仪表板嵌入到您的现有服务器中。

### 文件结构
```
tradr/
├── config.json              # Your live config (created from template)
├── config-template.json     # Default config for new installs
├── SKILL.md                 # This file
├── scripts/
│   ├── tradr-enter.py       # Entry engine
│   ├── exit-manager.py      # Exit daemon
│   ├── setup.sh             # Installer
│   └── notify-telegram.sh   # Example notification hook
├── adapters/
│   ├── README.md            # Signal adapter interface spec
│   └── example-adapter.py   # Working adapter template
└── dashboard/
    └── index.html           # Real-time monitoring dashboard
```

## 信号适配器

tradr 仅负责执行交易，不对“买入什么”提供任何建议。您提供交易信号，tradr 负责整个交易流程的管理。

信号适配器的接口是一个简单的命令：
```bash
python3 scripts/tradr-enter.py <ca> --score <N> [--chain <chain>] [--token <name>]
```

信号适配器可以是任何监控数据源、检测信号并调用相应命令的脚本或服务。请参阅 `adapters/README.md` 以获取完整规范，以及 `adapters/example-adapter.py` 作为示例模板。

**信号源示例：** Twitter 上的 KOL 跟踪、链上大额交易者的行为监控、Telegram 群组活动、DEX 交易量激增、跟单交易应用、自定义数据聚合工具等。

## 脚本
- **`scripts/tradr-enter.py`**：用于执行买入操作的脚本。接收合约地址（CA）和评分（score），确定交易规模，并通过 Bankr 进行买入操作，同时记录交易模式。
- **`scripts/exit-manager.py**：用于管理退出操作的脚本。定期查询价格，应用相应的退出规则，通过 Bankr 进行卖出操作，并记录所有交易细节。该脚本以 systemd 服务的形式运行。
- **`scripts/setup.sh`：用于安装 tradr 的脚本。根据模板创建配置文件，并设置 systemd 服务。

## 退出模式

每个交易都有相应的退出模式。系统默认提供了四种模式，您也可以自定义新的模式。

| 模式 | 停止条件 | 止盈条件 | 跟踪止损条件 | 适用场景 |
|------|---------|-------------|----------|----------|
| **snipe** | 0.85 倍 | 1.3 倍（卖出 30%） | 达到峰值后卖出 10% | 适用于快速买入/卖出的交易，信心较低的情况。 |
| **swing** | 0.70 倍 | 1.3 倍（卖出 30%） | 分层止损：低风险时 15%，高风险时 25% | 标准持有策略，默认模式。 |
| **gamble** | 0.50 倍 | 无 | 达到峰值后卖出 30% | 高风险策略，要么持有到底，要么全部卖出。 |
| **diamond** | 无 | 无 | 无 | 仅允许手动退出。 |

**swing 模式** 具有分层跟踪止损机制：当价格低于 2 倍时使用紧密止损（15%），当价格高于 2 倍时使用宽松止损（25%）。这种模式既能保护小额收益，又能让大额盈利继续增长。

### 自定义模式

您可以通过在 `config.json` 的 `modes` 部分添加新的模式来自定义退出策略。模式名称可以任意设定——退出管理器会动态读取这些配置参数，无需修改代码。

```json
"modes": {
  "snipe": { ... },
  "swing": { ... },
  "my-custom-mode": {
    "stop_at": 0.80,
    "take_profit_1": 1.2,
    "take_profit_1_size": 0.5,
    "trailing_stop": 0.12
  }
}
```

使用方法：`tradr-enter.py <合约地址> --评分 5 --模式 my-custom-mode`

## 模式选择

每次交易都会根据以下优先级选择退出模式：
1. **在买入时明确指定的 `--mode` 参数**。
2. **根据 `score_to_mode` 配置映射自动选择的模式**。
3. **`default_mode`（默认值）：swing 模式。

## 交易筛选规则
tradr 会拒绝不符合以下条件的交易：
- **市值上限**：代币的市值超过 `mcap_ceiling_usd`（默认值为 1000 万美元）。
- **冷却时间**：同一代币在 `cooldown_minutes` 内已被卖出。
- **最大持仓规模**：评分确定的交易规模超过 `max_position_size_usd`。
- **已持有该合约的仓位**：如果该合约已有持仓，则不允许再次买入。

## 部分卖出跟踪

当触发止盈条件时，tradr 会跟踪当前仓位的剩余 USD 金额。这意味着：
- 盈亏计算会考虑在止盈时已经卖出的部分以及最终卖出时的剩余部分。
- 交易日志会记录实际卖出的金额，而非原始持仓的全部金额。
- 您可以随时查看当前仍在交易中的 USD 金额。

## 通知机制

通知脚本接收三个参数：`level`（信息、交易、警告、错误），`type`（买入、卖出、信号确认、错误），`message`（人类可读的文本）。
这使得您可以根据需要定向发送通知——例如，仅将买入通知发送到私信，或将卖出通知同时发送到私信和广播频道。

示例通知脚本：
```bash
#!/bin/bash
LEVEL="$1"  TYPE="$2"  MSG="$3"
if [ "$TYPE" = "sell" ]; then
  # Route to both DM and broadcast
  send-dm "$MSG"
  send-broadcast "$MSG"
else
  # Everything else just DM
  send-dm "$MSG"
fi
```

## 配置参考

`config.json` 文件是在首次设置时根据 `config-template.json` 生成的：
```
positions_file       — path to positions.json
trade_log            — path to trade-log.jsonl
log_file             — path to tradr.log
bankr_script         — path to bankr.sh
lockfile             — exit manager lock (prevents duplicates)
poll_interval_seconds — price check interval (default: 10)
dexscreener_delay    — delay between DexScreener calls (default: 1.5s)
reconcile_every_cycles — on-chain reconciliation interval (default: every 30 cycles)

modes                — exit params per mode (add custom modes here)
  stop_at            — exit multiplier (e.g. 0.85 = sell if price drops to 0.85x entry)
  take_profit_1      — first TP multiplier (null = no TP)
  take_profit_1_size — fraction to sell at TP (e.g. 0.3 = 30%)
  trailing_stop      — trail % from peak (null = no trail)
  trailing_stop_tight — optional tight trail (swing mode)
  trailing_stop_tight_below — peak threshold for tight vs wide

default_mode         — fallback mode when not specified
score_to_mode        — map of score thresholds → mode names
score_to_size        — map of score thresholds → position size in USD

mcap_ceiling_usd     — reject entries above this mcap (0 = no limit)
cooldown_minutes     — block re-entry on same token for N minutes after close (0 = no cooldown)
max_position_size_usd — hard cap on any single position

wallets.solana       — Solana wallet address (for on-chain verification)
wallets.evm          — EVM wallet address (for on-chain verification)
rpc_urls             — custom RPC endpoints per chain

notifications.enabled — enable/disable notifications
notifications.script  — path to notification hook script (receives: level, type, message)
```

## 仪表板

tradr 配备了一个实时监控仪表板（`dashboard/index.html`），显示以下信息：
- **当前持仓**：实时盈亏情况、买入价格/当前价格/峰值市值、退出模式、持仓时长。
- **性能统计**：总盈亏、胜率、平均峰值、最佳交易记录。
- **交易历史**：可搜索的交易记录，包含买入/卖出详情和交易链接。
- **配置设置**：可折叠的退出模式、交易规模设置等界面。

仪表板是一个独立的 HTML 文件，它从四个 JSON API 端点获取数据，并每 15 秒自动更新。支持深色主题，兼容移动设备。

要使用该仪表板，请从您的 HTTP 服务器提供以下接口：
- `GET /api/positions` — 返回 `positions.json` 的内容。
- `GET /api/trades` — 返回解析后的交易日志（格式为 `{ "trades": [...] }`）。
- `GET /api/tradr-config` — 返回 `config.json` 的内容。
- `GET /api/health` — 返回系统状态（可选）。

## 架构

```
Signal Source (your adapter)
    |
    | CA + score [+ chain] [+ token]
    v
tradr-enter.py
    |
    |-- Guards: mcap ceiling, cooldown, size cap
    |-- Resolves mode (explicit > score_to_mode > default)
    |-- Sizes position (score_to_size map)
    |-- Fetches price/mcap from DexScreener
    |-- Executes buy via bankr.sh
    |-- Writes positions.json (with mode + remaining_usd fields)
    |-- Logs to trade-log.jsonl
    |-- Notifies (type=buy)
    |
    v
exit-manager.py (daemon, 10s poll)
    |
    |-- Reads positions.json
    |-- For each open position:
    |     |-- Reads position's mode → gets exit params from config
    |     |-- Fetches price from DexScreener
    |     |-- Applies: hard stop → TP → trailing
    |     |-- Executes sell via bankr.sh if triggered
    |     |-- Tracks remaining_usd after partial sells
    |     |-- Verifies on-chain balance (Solana RPC / EVM eth_call)
    |     |-- Updates positions.json + trade-log.jsonl
    |     |-- Notifies (type=sell)
    |
    |-- Every N cycles: reconcile (close stale positions where wallet is empty)
```

## 交易持仓结构

`positions.json` 文件中的每个持仓记录都包含以下信息（按合约地址进行索引）：
```json
{
  "token": "EXAMPLE",
  "chain": "base",
  "buy_ts": "2026-02-11T14:00:00Z",
  "entry_mcap": 500000,
  "entry_price": 0.0001,
  "buy_amount_usd": 7.50,
  "remaining_usd": 7.50,
  "mode": "swing",
  "score": 5,
  "current_mcap": 600000,
  "current_price": 0.00012,
  "peak_mcap": 700000,
  "first_exit_done": false,
  "closed": false,
  "close_ts": null,
  "close_reason": null,
  "close_mcap": null,
  "close_multiple": null,
  "est_pnl_usd": null,
  "tx_hash": "0x..."
}
```

## 系统要求
- Python 3.8+ 版本。
- 已安装 `Bankr` 技能（位于 `~/.openclaw/skills/bankr/`）。
- 需要 `jq` 工具（由 `bankr.sh` 脚本使用）。
- 需要 `systemd` 服务来运行退出管理器。
- 无需支付任何 API 使用费用，也不涉及大型语言模型（LLM）的成本。整个系统完全基于 Python 实现。

## tradr 的功能限制
- **不是信号生成器**：它不会告诉您应该买入什么交易信号，您需要自己提供交易信号。
- **不是大型语言模型（LLM）**：运行时无需任何 AI 资源，完全基于 Python 和数学算法。
- **不是钱包**：它不持有或访问用户的私钥，所有交易操作都通过 Bankr 完成。
- **不针对特定链路有偏好**：支持 Solana、Base、Ethereum、Polygon、Unichain 等 Bankr 支持的链路。
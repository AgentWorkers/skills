---
name: wayfinder
description: 通过 Wayfinder Paths CLI (`poetry run wayfinder`) 进行去中心化金融（DeFi）交易、收益策略管理以及投资组合管理。适用于用户需要查询账户余额、交换代币、跨链资产转移、交易衍生品（perps）、参与预测市场交易（如 Polymarket）、运行自动化收益策略（如稳定币收益策略、基础交易策略、Moonwell 循环、HyperLend、Boros HYPE 等）、管理钱包、查找代币元数据、管理流动性池（Uniswap V3 / ProjectX）或执行一次性 DeFi 脚本的场景。该工具支持通过协议适配器与 Ethereum、Base、Arbitrum、Polygon、BSC、Avalanche、Plasma 和 HyperEVM 等区块链平台进行交互。
metadata: {"openclaw":{"emoji":"🧭","homepage":"https://github.com/WayfinderFoundation/wayfinder-paths-sdk","requires":{"bins":["poetry"]},"install":[{"id":"brew","kind":"brew","formula":"poetry","bins":["poetry"],"label":"Install poetry"}]}}
---

# Wayfinder

Wayfinder是一个基于[poetry run wayfinder Paths](https://github.com/WayfinderFoundation/wayfinder-paths-sdk)框架的DeFi交易、收益策略和投资组合管理工具。

## 预运行检查

在运行任何命令之前，请确认已经安装了poetry run wayfinder Paths，并且可以正常访问它：

```bash
# SDK location (override by setting WAYFINDER_SDK_PATH)
export WAYFINDER_SDK_PATH="${WAYFINDER_SDK_PATH:-$HOME/wayfinder-paths-sdk}"

# Check if wayfinder-paths-sdk directory exists
if [ ! -d "$WAYFINDER_SDK_PATH" ]; then
  echo "ERROR: wayfinder-paths-sdk is not installed at: $WAYFINDER_SDK_PATH"
  echo "Set WAYFINDER_SDK_PATH or run the First-Time Setup below."
  exit 1
fi

# Config path (override by setting WAYFINDER_CONFIG_PATH)
export WAYFINDER_CONFIG_PATH="${WAYFINDER_CONFIG_PATH:-$WAYFINDER_SDK_PATH/config.json}"

# Check if the config exists
if [ ! -f "$WAYFINDER_CONFIG_PATH" ]; then
  echo "ERROR: config not found at $WAYFINDER_CONFIG_PATH. Run the First-Time Setup below."
  exit 1
fi

# Check if the CLI is functional
cd "$WAYFINDER_SDK_PATH"
if ! poetry run wayfinder --help > /dev/null 2>&1; then
  echo "ERROR: poetry run wayfinder CLI is not working. Run 'cd $WAYFINDER_SDK_PATH && poetry install' to fix."
  exit 1
fi

echo "poetry run wayfinder Paths is installed and ready."
```

如果任何检查失败，请按照以下**首次设置**说明进行操作，然后再继续。

## 快速入门

### 首次设置

**重要提示：**必须通过`git clone`从GitHub下载SDK。**切勿通过PyPI（`pip install wayfinder-paths`）来安装。

**开始之前：**您需要一个Wayfinder API密钥（格式：`wk_...`）。可以在**https://strategies_wayfinder.ai**获取该密钥。引导式设置会提示您输入这个密钥。

```bash
# Clone wayfinder-paths-sdk from GitHub (required — do NOT pip install)
export WAYFINDER_SDK_PATH="${WAYFINDER_SDK_PATH:-$HOME/wayfinder-paths-sdk}"
if [ ! -d "$WAYFINDER_SDK_PATH" ]; then
  git clone https://github.com/WayfinderFoundation/wayfinder-paths-sdk.git "$WAYFINDER_SDK_PATH"
fi

cd "$WAYFINDER_SDK_PATH"
poetry install

# Run guided setup (creates/updates config.json + local dev wallets + MCP config)
# You will need your API key from https://strategies.wayfinder.ai (format: wk_...)
python3 scripts/setup.py
```

**钱包安全提示：**
- **切勿在对话中泄露私钥或种子短语。**这些是敏感信息，必须保存在本地机器上，切勿通过聊天传递。
- 对于长期运行的机器人，建议将种子短语存储在后端/秘密管理器中，而不是在服务器上生成随机钱包。
- 在首次设置时，用户应直接从自己的机器或秘密管理器中获取种子短语。只有当用户明确表示无法自行获取时，才提供显示种子短语的功能。
- 有关详细的钱包设置说明，请参阅`references/setup.md`。

### 验证设置

```bash
export WAYFINDER_SDK_PATH="${WAYFINDER_SDK_PATH:-$HOME/wayfinder-paths-sdk}"
export WAYFINDER_CONFIG_PATH="${WAYFINDER_CONFIG_PATH:-$WAYFINDER_SDK_PATH/config.json}"
cd "$WAYFINDER_SDK_PATH"
poetry run wayfinder resource wayfinder://strategies
poetry run wayfinder resource wayfinder://wallets
poetry run wayfinder resource wayfinder://balances/main
```

## 命令参考

所有命令都应在 `$WAYFINDER_SDK_PATH` 下执行，并且需要 `WAYFINDER_CONFIG_PATH`（默认值为 `$WAYFINDER_SDK_PATH/config.json`）。成功时，所有响应都会返回 `{"ok": true, "result": {...}`；失败时，则返回 `{"ok": false, "error": {"code": "...", "message": "..."}`。

---

### `resource` — 通过URI读取MCP资源

通过基于URI的资源，可以读取适配器、策略、钱包、余额、代币和Hyperliquid市场的数据。使用 `--list` 可以查看所有可用的资源和模板。

**资产/数据来源规则：**当用户请求查询代币/池/市场/协议数据时，首先使用Wayfinder的适配器/策略发现资源（`poetry run wayfinder resource wayfinder://adapters`、`wayfinder://adapters/{name}`、`wayfinder://strategies`、`wayfinder://tokens/*`）。只有在Wayfinder无法提供所需数据或用户明确请求时，才使用其他方法。

```bash
# List all available resources and templates
poetry run wayfinder resource --list
```

#### 静态资源

| URI | 描述 |
|-----|-------------|
| `wayfinder://adapters` | 列出所有适配器的功能 |
| `wayfinder://strategies` | 列出所有策略及其依赖的适配器 |
| `wayfinder://wallets` | 列出所有配置的钱包 |
| `wayfinder://hyperliquid/prices` | 所有Hyperliquid的中间价 |
| `wayfinder://hyperliquid/markets` | Perp市场的元数据、融资率和资产上下文 |
| `wayfinder://hyperliquid/spot-assets` | Perp市场的资产元数据 |

```bash
poetry run wayfinder resource wayfinder://adapters
poetry run wayfinder resource wayfinder://strategies
poetry run wayfinder resource wayfinder://wallets
poetry run wayfinder resource wayfinder://hyperliquid/prices
poetry run wayfinder resource wayfinder://hyperliquid/markets
poetry run wayfinder resource wayfinder://hyperliquid/spot-assets
```

#### 资源模板

| URI模板 | 描述 |
|--------------|-------------|
| `wayfinder://adapters/{name}` | 描述单个适配器（例如 `moonwell_adapter`） |
| `wayfinder://strategies/{name}` | 描述单个策略（例如 `stablecoin_yield_strategy`） |
| `wayfinder://wallets/{label}` | 根据标签获取单个钱包 |
| `wayfinder://balances/{label}` | 获取钱包的跨链余额 |
| `wayfinder://activity/{label}` | 获取钱包的最新交易活动 |
| `wayfinder://tokens/search/{chain_code}/{query}` | **模糊查询代币**（查询结果位于 `/tokens/fuzzy/`）——始终优先使用此方法 |
| `wayfinder://tokens/resolve/{query}` | 根据已知ID解析代币（查询结果位于 `/tokens/detail/`）——仅在使用ID时使用 |
| `wayfinder://tokens/gas/{chain_code}` | 指定链路的**原生气体代币**（例如ETH、HYPE）——用于原生代币 |
| `wayfinder://hyperliquid/{label}/state` | 获取钱包在Hyperliquid上的Perp头寸和利润与损失（PnL） |
| `wayfinder://hyperliquid/perp` | 获取钱包在Hyperliquid上的现货余额 |

```bash
# 1. For native gas tokens (ETH, HYPE): use the gas endpoint
poetry run wayfinder resource wayfinder://tokens/gas/ethereum    # ETH on Ethereum
poetry run wayfinder resource wayfinder://tokens/gas/base        # ETH on Base
poetry run wayfinder resource wayfinder://tokens/gas/hyperevm    # HYPE on HyperEVM

# 2. For ERC20 tokens: ALWAYS fuzzy search first
poetry run wayfinder resource wayfinder://tokens/search/base/usdc
poetry run wayfinder resource wayfinder://tokens/search/arbitrum/eth
poetry run wayfinder resource wayfinder://tokens/search/ethereum/weth

# 3. Then resolve with the exact ID from search results
poetry run wayfinder resource wayfinder://tokens/resolve/usd-coin-base
```

---

### `wallets` — 管理钱包和发现头寸

创建、注释和发现跨协议的头寸。使用 `resource wayfinder://wallets` 列出钱包，使用 `resource wayfinder://wallets/{label}` 获取单个钱包。

| 参数 | 类型 | 是否必填 | 默认值 | 备注 |
|-----------|------|----------|---------|-------|
| `action` | `"create"` \| `"annotate"` \| `"discover_portfolio"` | **是** | — | — |
| `label` | 字符串 | **create** | — | 必须非空；重复的标签具有幂等性 |
| `wallet_label` | 字符串 | **annotate, discover_portfolio** | — | 或使用 `wallet_address` |
| `wallet_address` | 字符串 | 否 | — | `wallet_label` 的替代选项 |
| `protocol` | 字符串 | **annotate** | — | 注释时使用的协议名称 |
| `annotate_action` | 字符串 | **annotate** | — | 注释时使用的操作 |
| `tool` | 字符串 | **annotate** | — | 注释时使用的工具名称 |
| `status` | 字符串 | **annotate** | — | 注释时使用的状态 |
| `chain_id` | 字符串 | 否 | — | — |
| `details` | 字符串（JSON） | 否 | — | 用于注释的额外元数据 |
| `protocols` | 字符串（JSON） | 否 | — | 用于过滤 `discover_portfolio` 的特定协议 |
| `parallel` | 布尔值 | 否 | `false` | **如果在没有 `protocols` 过滤器的情况下查询多个协议，则必须设置为`true` |
| `include_zero_positions` | 布尔值 | 否 | `false` | 是否在投资组合中包含空头寸 |

`discover_portfolio` 支持的协议：`hyperliquid`、`hyperlend`、`moonwell`、`boros`、`pendle`。

```bash
poetry run wayfinder wallets --action create --label my_new_strategy
poetry run wayfinder wallets --action discover_portfolio --wallet_label main --parallel
poetry run wayfinder wallets --action discover_portfolio --wallet_label main --protocols '["hyperliquid","moonwell"]'
```

**验证规则：**
- `create`：`label` 必须非空。重复的标签会返回现有的钱包（具有幂等性）。
- `annotate`/`discover_portfolio`：必须从 `wallet_label` 或 `wallet_address` 中解析出钱包地址。
- `annotate`：`protocol`、`annotate_action`、`tool`、`status` 都是必填项。
- 使用 `discover_portfolio` 时，如果查询的协议数量大于或等于3个，则必须设置 `parallel=true`，或者明确指定 `protocols` 过滤器（否则会显示 `requiresconfirmation`）。

---

### `quote_swap` — 获取交换/桥接报价（只读）

返回用于交换或桥接代币的报价。此操作不会对链上产生任何影响。

| 参数 | 类型 | 是否必填 | 默认值 | 备注 |
|-----------|------|----------|---------|-------|
| `wallet_label` | 字符串 | **是** | — | 必须能够解析为钱包地址 |
| `from_token` | 字符串 | **是** | — | 来自搜索结果的代币ID（例如 `usd-coin-base`）。**始终先进行搜索** |
| `to_token` | 字符串 | **是** | — | 来自搜索结果的代币ID。**始终先进行搜索** |
| `amount` | 字符串 | **是** | — | 可读的金额（例如 `"500"`）。金额必须是正数，且能够被转换为十进制后大于0 |
| `slippage_bps` | 整数 | 否 | **滑动率（以基点为单位）** | 默认值为50（相当于0.5%） |
| `recipient` | 字符串 | 否 | — | 默认为发送者地址 |
| `include_calldata` | 布尔值 | 否 | **是否在响应中包含原始calldata** |

**在调用 `quote_swap` 之前，**务必先使用 `poetry run wayfinder resource wayfinder://tokens/search/<chain>/<symbol>` 查找每个代币的ID。**不要使用原始的符号或猜测的 `symbol-chain` 字符串——它们可能会导致错误的解析结果。**

**注意：**对于原生气体代币（例如未包装的ETH），使用 `from_token_address: null` 可能会导致交换失败。请使用包装后的ERC20版本（例如 `WETH`）。搜索方法为：`resource wayfinder://tokens/search/<chain>/weth`。

**首次桥接到新链路时：**在执行任何操作之前，目标链路上必须要有**原生气体**。首先将原生气体代币（例如ETH）桥接到目标链路上，然后再进行桥接或交换目标代币。请使用下表中的原生代币ID（例如，对于Base链路上的ETH使用 `ethereum-base`）。

---`

### 错误代码

- `not_found`（钱包未找到）
- `invalid_wallet`（钱包无效）
- `token_error`（代币错误）
- `invalid_token`（缺少链ID/地址）
- `invalid_amount`（金额无效）
- `quote_error`（报价错误）

---

### `execute` — 在链上执行交易

执行交换、代币发送或Hyperliquid存款操作。**这些操作会广播交易**，并可能涉及实际的资金转移。

| 参数 | 类型 | 是否必填 | 默认值 | 备注 |
|-----------|------|----------|---------|-------|
| `kind` | `swap` \| `send` \| `hyperliquid_deposit` | **是** | — | 操作类型 |
| `wallet_label` | 字符串 | **是** | — | 必须能够解析为具有私钥的钱包 |
| `amount` | 字符串 | **是** | — | 可读的金额（例如 `"500"`） |
| `from_token` | 字符串 | **swap** | — | 来源代币ID。**始终先进行搜索** |
| `to_token` | 字符串 | **swap** | — | 目标代币ID。**始终先进行搜索** |
| `slippage_bps` | 整数 | 否 | **滑动率（以基点为单位）** | 默认值为50 |
| `deadline_seconds` | 整数 | 否 | **swap` 操作的截止时间（以秒为单位） | 默认值为300秒 |
| `recipient` | 字符串 | **send** | — | 收件人地址 |
| `token` | 字符串 | **send** | — | 代币ID（当 `token="native" 时使用） | **始终先进行搜索** |
| `chain_id` | 字符串 | 否 | **send` 选项时需要** | |

**Hyperliquid存款的验证规则：**
- 金额 **必须大于或等于5 USDC**（低于5 USDC的存款将在桥接过程中丢失）。
- 硬编码规则：`token = Arbitrum USDC`，`recipient = `HYPERLIQUID_BRIDGE_ADDRESS`，`chain = Arbitrum`（42161）。

**其他运行时验证规则：**
- 钱包必须同时具有 `address` 和 `private_key_hex`。
- 代币解析必须成功（需要 `chain_id` 和 `token_address`）。
- 交换报价必须返回包含 `calldata` 的 `best_quote`。
- 对于USDT风格的代币，在批准之前会发送一个零允许额度的重置交易。

---

### `hyperliquid` — 等待Hyperliquid上的存款/取款完成

等待Hyperliquid上的存款或取款操作完成。对于只读查询（用户状态、价格、订单簿等），可以使用 `resource` 命令和Hyperliquid的URI。

---`

### `hyperliquid_execute` — Hyperliquid交易操作

放置/取消订单、更新杠杆率以及提取USDC。**这些操作是实时的**，可以执行真实的交易或转移资金。

| 参数 | 类型 | 是否必填 | 默认值 | 备注 |
|-----------|------|----------|---------|-------|
| `action` | `place_order` \| `cancel_order` \| `update_leverage` \| `withdraw` \| `spot_to_perp_transfer` \| `perp_to_spot_transfer` | **是** | — | — |
| `wallet_label` | 字符串 | **是** | — | 必须能够解析为具有私钥的钱包 |
| `coin` | 字符串 | **place_order, cancel_order, update_leverage` | — | 或使用 `asset_id`（会自动去除 `-perp`/`_perp` 后缀） |
| `asset_id` | 字符串 | 否 | — | 直接的资产ID（`coin` 的替代选项） |
| `is_spot` | 字符串 | 否 | **place_order` 时必须指定 | |
| `order_type` | `market` \| `limit` | 否 | `market` | — |
| `is_buy` | 字符串 | **place_order` 时必须指定 | |
| `size` | 字符串 | 否 | **与 `usd_amount` 搭配使用** | |
| `usd_amount` | 字符串 | **usd_amount` 时必须指定 | |
| `usd_amount_kind` | 字符串 | **当使用 `usd_amount` 时` | — | `usd_amount_kind` 的用途 |
| `leverage` | 字符串 | **当 `usd_amount_kind=margin` 时` | **update_leverage` 时必须指定** | |
| `price` | 字符串 | **limit order` 时必须指定 | |
| `slippage` | 浮点数 | 否 | **limit order` 时必须指定 | | 最大为0.01 |
| `reduce_only` | 布尔值 | 否 | `--reduce_only` / `--no-reduce_only` | |

**`place_order` 的关键验证规则：**
- 必须指定 `size` 或 `usd_amount` 中的一个（不能同时指定两个）。
- 如果使用了 `usd_amount`，则必须指定 `usd_amount_kind`。
- 如果使用 `usd_amount_kind=margin`，则必须指定 `leverage`。
- `limit order` 需要 `price` 大于0。

---

### `polymarket` — Polymarket市场及相关操作

提供对Polymarket市场、价格、订单簿和用户状态的只读访问。

**可交易性过滤条件：**一个市场可能“存在”但不可交易。可以通过 `enableOrderBook`、`acceptingOrders`、`active`、`closed != true` 和非空的 `clobTokenIds` 来过滤市场。

---`

### `polymarket_execute` — Polymarket执行操作

执行Polymarket操作（包括桥接和交易）。**此命令是实时的（不允许进行模拟测试）**。

| 参数 | 类型 | 是否必填 | 默认值 | 备注 |
|-----------|------|----------|---------|-------|
| `action` | `bridge_deposit` \| `bridge_withdraw` \| `buy` \| `sell` \| `close_position` \| `place_limit_order` \| `cancel_order` \| `redeem_positions` | **是** | — | — |
| `wallet_label` | 字符串 | **是** | — | 钱包配置中必须包含 `address` 和 `private_key_hex` |
| `from_chain_id` | 整数 | 否 | `137` | 仅用于 `bridge_deposit` |
| `from_token_address` | 字符串 | 否 | Polygon的USDC地址 | 仅用于 `bridge_deposit` |
| `amount` | 浮点数 | **bridge_deposit` 时使用** | 需要存款的USDC金额 |
| `recipient_address` | 字符串 | 否 | 发送者地址 | 仅用于 `bridge_withdraw` |
| `amount_usdce` | 浮点数 | **bridge_withdraw` 时使用** | 需要提取的USDC.e金额 |
| `to_chain_id` | 整数 | 否 | `137` | 仅用于 `bridge_withdraw` |
| `to_token_address` | 字符串 | 否 | 发送者地址 | 仅用于 `bridge_withdraw` |
| `token_decimals` | 整数 | 否 | **bridge_withdraw` 时使用的桥接代币小数位数 | |
| `market_slug` | 字符串 | **bridge_withdraw` 时使用** | 市场slug |
| `outcome` | 字符串 | `yes` | `bridge_withdraw` 时使用 | （例如 `YES`/`NO` 表示成功或失败） |

**执行操作前的注意事项：**
- `place_order` 时必须指定 `size` 或 `usd_amount` 中的一个（不能同时指定两个）。
- 如果使用了 `usd_amount`，则必须指定 `usd_amount_kind`。
- 如果使用了 `usd_amount_kind=margin`，则必须指定 `leverage`。
- `limit order` 时 `price` 必须大于0。
- 在进行批量调整后，`size` 仍然必须大于0。
- 构建费用是强制性的（会自动提交；如果需要，系统会自动处理提交）。
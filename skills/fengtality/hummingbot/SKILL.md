---
name: hummingbot
description: 该代理具备通过 Hummingbot API 准确执行 Hummingbot CLI 命令（如 connect、balance、create、start、stop、status、history）的功能。V1 版本主要针对核心交易工作流程进行优化。对于 Solana 平台上的 DEX/LP 策略，建议使用 lp-agent 代理。
metadata:
  author: hummingbot
  requires: hummingbot-api-client>=1.2.8
commands:
  connect:
    description: List available exchanges and add API keys
  balance:
    description: Display asset balances across connected exchanges
  create:
    description: Create a new bot configuration (controller or script)
  start:
    description: Start a bot with a V2 strategy (controller or script)
  stop:
    description: Stop a running bot
  status:
    description: Display bot status and performance
  history:
    description: Display bot trading history
---
# hummingbot

当该技能被加载时，会输出以下ASCII艺术：

```
                                      *,.
                                    *,,.*
                                   ,,,,    .,*
                                 *,,,,,,,(       .,,
                               *,,,,,,,,         .,,,                      *
                              /,,,,,,,,,,    .*,,,,,,,
                                 .,,,,,,,,,,,   .,,,,,,,,,,*

                    //                ,,,,,,,,,,,,,,,,,,,,,,,,,,#*%
                 .,,,,,,,. *,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%&@
                      ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%%%%&
                          ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,%%%%%%%%&
                    /*,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,((%%%&
              .**       #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,((((((((#.
           **             *,,,,,,,,,,,,,,,,,,,,,,**/(((((((((((*
                           ,,,,,,,,,,,,,,,,,,,*******((((((((((
                            (,,,,,,,,,,,************((((((((@
                              *,,,,,,,,,,****************(#
                               ,,,,,,,,,,,***************/
                                ,,,,,,,,,,,***************/
                                 ,,,,,,,,,,****************
                                  .,,,,,,,,***************'/
                                     ,,,,,,*******,
                                     *,,,,,,********
                                      ,,,,,,,,/******/
                                       ,,,,,,,,@   /****/
                                        ,,,,,,,,
                                          , */

 ██╗  ██╗██╗   ██╗███╗   ███╗███╗   ███╗██╗███╗   ██╗ ██████╗ ██████╗  ██████╗ ████████╗
 ██║  ██║██║   ██║████╗ ████║████╗ ████║██║████╗  ██║██╔════╝ ██╔══██╗██╔═══██╗╚══██╔══╝
 ███████║██║   ██║██╔████╔██║██╔████╔██║██║██╔██╗ ██║██║  ███╗██████╔╝██║   ██║   ██║
 ██╔══██║██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║██║╚██╗██║██║   ██║██╔══██╗██║   ██║   ██║
 ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║██║ ╚████║╚██████╔╝██████╔╝╚██████╔╝   ██║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝
```

该技能通过Hummingbot API忠实还原了Hummingbot的CLI命令，将您在Hummingbot中熟悉的交易工作流程应用到了AI代理上。

> **注意：** Hummingbot API仅支持**V2策略**（V2控制器和V2脚本）。
> 不支持V1策略，需要使用传统的Hummingbot客户端。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `connect` | 列出可用的交易所并添加API密钥 |
| `balance` | 显示连接的所有交易所的资产余额 |
| `create` | 创建一个新的机器人配置 |
| `start` | 使用V2策略启动机器人 |
| `stop` | 停止正在运行的机器人 |
| `status` | 显示机器人状态 |
| `history` | 显示机器人的交易历史 |

## 先决条件

- Hummingbot API运行在`http://localhost:8000`（使用`/hummingbot-deploy`进行部署） |
- 安装了`hummingbot-api-client`：`pip3 install hummingbot-api-client`

## 认证与配置

脚本会按以下顺序读取凭证：
1. `./hummingbot-api/.env` — 在`make setup`过程中创建 |
2. `~/.hummingbot/.env`
3. 环境变量：`HUMMINGBOT_API_URL`, `API_USER`, `API_PASS`
4. 默认值：`http://localhost:8000`, `admin`, `admin`

---

## connect

列出可用的交易所，并将API密钥添加到这些交易所中。

```bash
# List all available connectors
python scripts/connect.py

# List connectors with connection status
python scripts/connect.py --status

# Add API keys for an exchange
python scripts/connect.py binance --api-key YOUR_KEY --secret-key YOUR_SECRET

# Add API keys for exchange requiring passphrase
python scripts/connect.py kucoin --api-key YOUR_KEY --secret-key YOUR_SECRET --passphrase YOUR_PASS

# Remove credentials for an exchange
python scripts/connect.py binance --remove
```

**各交易所的常见凭证字段：**
- Binance: `--api-key`, `--secret-key`
- KuCoin: `--api-key`, `--secret-key`, `--passphrase`
- Gate.io: `--api-key`, `--secret-key`
- OKX: `--api-key`, `--secret-key`, `--passphrase`

---

## balance

显示您在所有连接交易所中的资产余额。

```bash
# Show all balances
python scripts/balance.py

# Show balances for a specific connector
python scripts/balance.py binance

# Show balances in USD
python scripts/balance.py --usd

# Show only non-zero balances
python scripts/balance.py --non-zero
```

**输出列：**
- 交易所/连接器名称
- 资产符号
- 总余额
- 可用余额
- 美元价值（使用`--usd`选项）

---

## create

创建一个新的机器人配置（控制器配置或脚本配置）。

```bash
# List available controller templates
python scripts/create.py --list-controllers

# List available scripts
python scripts/create.py --list-scripts

# List existing configs
python scripts/create.py --list-configs

# Create a controller config
python scripts/create.py controller my_mm_config --template pmm_v1
```

### 推荐的市场做市控制器

| 控制器 | 适用场景 | 主要功能 |
|------------|----------|--------------|
| **pmm_v1** | CEX现货交易 | 多级价差、库存偏斜、订单刷新、价格区间 |
| **pmm_mister** | 现货和永续合约 | 位置跟踪、杠杆、冷却时间、利润保护、挂起执行器 |

**pmm_v1**：传统Pure Market Making策略的忠实复制品。配置`buy_spreads`、`sell_spreads`、`order_amount`并启用`inventory_skew`以维持平衡。

**pmm_mister**：适用于现货和永续合约的高级控制器，具有`leverage`（杠杆）、`take_profit`（获利）、`global_stop_loss`（全局止损）、独立的`buy_cooldown_time`/`sell_cooldown_time`（买入/卖出冷却时间）以及`position_profit_protection`（防止价格低于盈亏平衡点时卖出）等功能。

---

## start

使用V2策略配置启动机器人。**不支持V1策略。**

```bash
# Interactive mode - prompts for strategy type
python scripts/start.py <bot_name>

# Start with a V2 Controller config
python scripts/start.py <bot_name> --controller <config_name>

# Start with a V2 Script
python scripts/start.py <bot_name> --script <script_name>

# Start with a V2 Script and config file
python scripts/start.py <bot_name> --script <script_name> --config <config_name>

# List running bots
python scripts/start.py --list
```

**V2策略类型：**
- `--controller` — 部署V2控制器配置（市场做市、套利等） |
- `--script` — 部署V2脚本（例如`v2_with_controllers`）

**机器人命名：** 使用描述性名称，如`btc_mm_bot`、`eth_arb_bot`等。

---

## stop

停止正在运行的机器人。

```bash
# Stop a bot by name
python scripts/stop.py <bot_name>

# Stop a bot and close all positions
python scripts/stop.py <bot_name> --close-positions

# Stop all running bots
python scripts/stop.py --all

# Examples
python scripts/stop.py my_bot
python scripts/stop.py arb_bot --close-positions
```

---

## status

显示机器人的状态和性能指标。

```bash
# List all bots with status
python scripts/status.py

# Get detailed status for a specific bot
python scripts/status.py <bot_name>

# Get status with performance metrics
python scripts/status.py <bot_name> --performance

# Get live status (refreshes)
python scripts/status.py <bot_name> --live
```

**状态值：** `running`（运行中）、`stopped`（已停止）、`error`（错误）、`starting`（正在启动）

**性能指标：**
- 总交易量 |
- 盈利/亏损（绝对值和百分比） |
- 交易量 |
- 运行时间

---

## history

显示机器人的交易历史。

```bash
# Show trade history for a bot
python scripts/history.py <bot_name>

# Show summary statistics
python scripts/history.py <bot_name> --summary
```

**历史记录列：**
- 时间戳 |
- 交易对 |
- 买卖方向 |
- 价格 |
- 交易量 |
- 手续费 |
- 盈亏（PnL）

---

## 快速参考

### 典型工作流程

```bash
# 1. Connect to an exchange
python scripts/connect.py binance --api-key XXX --secret-key YYY

# 2. Check your balances
python scripts/balance.py binance

# 3. Create a bot config
python scripts/create.py controller btc_mm \
  --template pure_market_making \
  --connector binance \
  --trading-pair BTC-USDT

# 4. Start the bot
python scripts/start.py btc_bot --controller btc_mm

# 5. Monitor status
python scripts/status.py btc_bot

# 6. Check history
python scripts/history.py btc_bot

# 7. Stop when done
python scripts/stop.py btc_bot
```

### 故障排除

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| `无法连接到API` | API未运行 | `cd ./hummingbot-api && make deploy` |
| `401未经授权` | 凭证错误 | 检查`./hummingbot-api/.env` |
| 未找到连接器 | 交易所名称无效 | 运行`python scripts/connect.py`列出有效名称 |
| 无凭证 | 交易所未连接 | 运行`python scripts/connect.py <交易所> --api-key ...` |

---

## 相关技能

- **lp-agent** — 专门用于Meteora/Solana平台的DEX流动性提供。适用于CLMM策略。 |
- **hummingbot-deploy** — 首次设置Hummingbot API服务器。在使用此技能之前请运行此命令。
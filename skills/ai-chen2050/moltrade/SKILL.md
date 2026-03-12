---
name: moltrade
description: 在 OpenClaw 中操作 Moltrade 交易机器人（包括配置、回测、测试模式运行、Nostr 信号广播、交易所适配器以及策略集成等功能）。
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      bins: ["python", "pip"]
    homepage: https://github.com/hetu-project/moltrade.git
---
# Moltrade机器人技能

**Moltrade**是一个去中心化的自动化交易助手，它允许您执行量化策略、分享加密信号，并让其他人复制您的交易——所有这些操作都通过Nostr网络安全地完成。根据您的交易表现，您可以获得声誉和信用点数。

![Moltrade](https://raw.githubusercontent.com/hetu-project/moltrade/main/assets/moltrade-background-2.jpg)

**您的24/7人工智能交易助手！即使您在睡觉时也能赚钱。**

[![在Twitter上关注我们](https://img.shields.io/twitter/follow/hetu_protocol?style=social&label=Follow)](https://x.com/hetu_protocol) [![在Telegram上关注我们](https://img.shields.io/badge/Telegram-Hetu_Builders-blue)](https://t.me/+uJrRgjtSsGw3MjZl) [![在ClawHub上关注我们](https://img.shields.io/badge/ClawHub-Read-orange)](https://clawhub.ai/ai-chen2050/moltrade) [![访问我们的网站](https://img.shields.io/badge/Website-moltrade.ai-green)](https://www.moltrade.ai/)

---

## 优势

**Moltrade**在安全性、可用性和可扩展性方面取得了平衡。其主要优势包括：

1. **客户端自行托管密钥，而非使用云存储**：所有敏感密钥和凭证都保存在用户的机器上；云服务器从不持有资金或私钥，从而将托管风险降至最低。**云服务器无法访问私钥或资金。**
2. **加密的、定向的通信**：信号在发布前会被加密，只有预定的订阅者才能解密，这保护了策略的隐私和订阅者的安全。
3. **轻量级的云重加密与广播**：云服务器仅作为高效的中继/广播器使用，不存储私钥；重加密或转发技术提高了传输的可靠性和覆盖范围。
4. **一键复制交易（用户友好）**：为非专家用户提供了即插即用的复制交易体验——只需几个步骤即可设置并本地执行信号。
5. **OpenClaw策略顾问**：集成OpenClaw作为自动化回测和改进建议的工具；用户可以决定是否采纳推荐的修改。
6. **云服务器可以作为去中心化的中继网络**：轻量级的中继架构支持未来迁移到去中心化中继网络，减少单点故障并提高抗审查能力。
7. **统一的激励（信用）系统**：一个透明、可验证的信用机制奖励所有参与者（信号提供者、订阅者、中继节点），使整个生态系统的激励机制保持一致。

## **工作原理（简化流程）**

```bash
1) Run Your Bot  ──→  2) Generate & Encrypt  ──→  3) Relay  ──→  4) Copy & Execute  ──→  5) Verify & Earn
```

## 安装与初始化

- 如果您正在使用**OpenClaw**，可以直接通过ClawHub进行安装：

```bash
clawhub search moltrade
clawhub install moltrade
```

- 或者克隆仓库并在本地安装Python依赖项（策略、nostr和CLI需要这些依赖项）：
  - `git clone https://github.com/hetu-project/moltrade.git`
  - `cd moltrade/trader && pip install -r requirements.txt`
- 使用内置向导初始化一个新的配置文件（不进行交易）：
  - 建议由用户手动运行`python main.py --init`（系统会提示输入中继URL、钱包地址、nostr设置、复制交易订阅者信息以及机器人注册信息），这样您可以自行确认这些信息，并在注册机器人时获取中继返回的`relayer_nostr_pubkey`。
  - 如果您委托给代理，请确保您信任该代理并允许其管理钱包密钥，并确保代理完成整个注册流程，以便将`relayer_nostr_pubkey`写入配置文件中。
- 对于持续集成/代理环境，请继续使用仓库的克隆版本；目前还没有单独的pip包或CLI工具。

## 安全地更新配置

- 在编辑之前，请备份配置文件或显示预期的更改内容。
- 仅更改所需的字段（例如`trading.exchange`、`trading.default_strategy`、`nostr.relays`）。
- 验证JSON格式；确保数据类型正确。提醒用户自行提供真实的敏感信息。

## 运行回测（本地）

- 安装依赖项：`pip install -r trader/requirements.txt`。
- 命令：`python trader/backtest.py --config trader/config.example.json --strategy <name> --symbol <symbol> --interval 1h --limit 500`。
- 如果有数据，报告盈亏/胜率/交易数量/回撤情况。请使用包含掩码的配置文件（不要使用真实的密钥）。

## 启动机器人（测试模式）

- 确保`config.json`文件存在（如果不存在，请运行`python main.py --init`），并设置`trading.exchange`（默认值为`hyperliquid`）。
- 命令：`python trader/main.py --config config.json --test --strategy <name> --symbol <symbol> --interval 300`。
- 查看`trading_bot.log`日志；未经用户明确许可，切勿切换到实时模式。

## 启动机器人（实时模式）

- 仅在测试模式通过验证后才能切换到实时模式；删除`--test`参数即可。
- 命令：`python trader/main.py --config config.json --strategy <name> --symbol <symbol>`。
- 在启动之前，请再次检查密钥、风险限制和交易品种；实时模式会执行真实的交易订单。

## 复制交易的使用（实时模式）

- 订阅者（跟随领导者进行交易，不执行策略交易）：`python trader/main.py --config trader/config.json --strategy momentum --symbol HYPE --copytrade follower`

## 向Nostr广播信号

- 检查`nostr`配置文件中的`nsec`、`relayer_nostr_pubkey`、`relays`、`sid`字段。
- `SignalBroadcaster`功能已集成到`main.py`中。在测试模式下，验证`send_trade_signal`和`send_execution_report`命令是否能正常运行。

## 支持Binance现货交易

Moltrade支持通过`binance-sdk-spot`进行Binance现货交易。在配置文件中将`trading.exchange`设置为`"binance"`，并提供API凭证。

> **相关技能**（这些技能与机器人运行无关，但需要了解）：
>
> - [`binance/spot`](binance/spot/SKILL.md) — Binance现货交易的REST API技能：市场数据、订单管理、账户信息。需要API密钥和密钥对；支持测试网和主网。
> - [`binance/square-post`](binance/square-post/SKILL.md) — Binance Square社交平台技能：通过Square OpenAPI发布交易见解/信号。需要Square OpenAPI密钥。

### 安装Binance SDK

```bash
pip install binance-sdk-spot
```

### 配置字段

在现有的`trading`配置块中添加一个`binance`配置块：

```json
{
  "trading": {
    "exchange": "binance",
    "default_symbol": "BTCUSDT",
    "default_strategy": "momentum"
  },
  "binance": {
    "api_key": "your_mainnet_api_key",
    "api_secret": "your_mainnet_api_secret",
    "testnet_api_key": "your_testnet_api_key",
    "testnet_api_secret": "your_testnet_api_secret"
  }
}
```

> **注意**：Binance测试网使用的密钥需要单独在<https://testnet.binance.vision>生成（需要GitHub登录）。主网密钥无法在测试网上使用。

### 测试网（--test）

当传递`--test`参数时，机器人会将所有请求路由到`testnet.binance.vision`，并使用`binance.testnet_api_key`/`testnet_api_secret`。如果未提供测试网密钥，系统将使用主网密钥，这可能会导致测试网端点的认证错误。

```bash
python trader/main.py --config config.json --test --strategy momentum --symbol BTCUSDT
```

### 实时交易

```bash
python trader/main.py --config config.json --strategy momentum --symbol BTCUSDT
```

### 回测

```bash
python trader/backtest.py --config trader/config.example.json --strategy momentum --symbol BTCUSDT --interval 1h --limit 500
```

### 支持的接口

`BinanceClient`（`trader/binance_api.py`）实现了与`HyperliquidClient`相同的接口：

| 方法                                                  | 描述                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------- |
| `get_candles(symbol, interval, limit)`                 | K线数据（格式为`[ts, open, high, low, close, vol]`            |
| `get_balance(asset)`                                   | 资产的可用余额（默认为`USDT`）                  |
| `get_positions()`                                      | 非零资产余额（现货交易不涉及保证金）                        |
| `get_open_orders()`                                    | 所有当前未平仓的订单                                      |
| `place_order(symbol, is_buy, size, price, order_type)` | 发布LIMIT或MARKET订单，自动调整订单数量/价格单位         |
| `cancel_order(order_id, symbol)`                       | 根据订单ID取消订单                                      |
| `cancel_all_orders(symbol)`                            | 取消所有订单（可选，针对特定品种）                         |
| `get_ticker_price(symbol)`                             | 最新的交易价格                                      |

## 添加交易所适配器

- 在`trader/exchanges/`目录下实现符合`HyperliquidClient`接口的适配器（如`get_candles`、`get_balance`、`get_positions`、`place_order`等函数）。
- 在`trader/exchanges/factory.py`中根据`trading.exchange`进行配置。
- 更新配置文件中的`trading.exchange`设置，并重新运行回测或测试模式。

## 集成新策略

- 遵循`trader/strategies/INTEGRATION.md`文档，继承`BaseStrategy`类，并在`get_strategy`函数中进行注册。
- 在`strategies.<name>`配置文件中添加新策略的配置；先进行回测，然后在测试模式下验证后再投入实际使用。

## 安全性/隐私保护

- 绝不要打印或提交私钥、助记词、nsec或共享密钥。
- 默认设置为测试模式；进行实时交易前需要用户明确同意。
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

**Moltrade**是一款去中心化的自动化交易辅助工具，它允许您执行量化交易策略、共享加密交易信号，并让其他人复制您的交易——所有这些操作都通过Nostr网络安全地完成。根据您的交易表现，您可以获得声誉和信用奖励。

![Moltrade](https://raw.githubusercontent.com/hetu-project/moltrade/main/assets/moltrade-background-2.jpg)

**您的24/7人工智能交易助手！即使在您睡觉时也能为您赚钱。**

[![在Twitter上关注我们](https://img.shields.io/twitter/follow/hetu_protocol?style=social&label=Follow)](https://x.com/hetu_protocol) [![在Telegram上关注我们](https://img.shields.io/badge/Telegram-Hetu_Builders-blue)](https://t.me/+uJrRgjtSsGw3MjZl) [![访问ClawHub](https://img.shields.io/badge/ClawHub-Read-orange)](https://clawhub.ai/ai-chen2050/moltrade) [![访问我们的网站](https://img.shields.io/badge/Website-moltrade.ai-green)](https://www.moltrade.ai/)

---

## 优势

**Moltrade**在安全性、可用性和可扩展性方面取得了平衡。其主要优势包括：

1. **客户端自托管密钥，而非云存储**：所有敏感密钥和凭证都保存在用户的设备上；云服务器从不存储资金或私钥，从而将托管风险降至最低。**云服务器无法访问私钥或资金。**
2. **加密通信**：交易信号在发布前会被加密，只有预定的订阅者才能解密，这保护了策略的隐私和订阅者的安全。
3. **轻量级的云重加密与广播**：云服务器仅作为高效的转发节点，不存储私钥；重加密或转发技术提高了信号传输的可靠性和覆盖范围。
4. **一键复制交易（用户友好）**：为非专业用户提供了即用的复制交易功能——只需简单设置几步即可本地执行交易信号。
5. **OpenClaw策略顾问**：集成OpenClaw作为自动化回测和改进建议的工具；用户可以决定是否采纳推荐的修改。
6. **云服务器可作为去中心化的转发网络**：其轻量级的架构支持未来迁移到去中心化网络，减少单点故障的风险并提高抗审查能力。
7. **统一的激励（信用）系统**：透明的信用机制奖励所有参与者（信号提供者、订阅者、转发节点），使整个生态系统的激励机制保持一致。

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
- 使用内置的向导初始化一个新的配置文件（不进行交易操作）：
  - 建议由用户手动运行 `python main.py --init`（系统会提示输入中继服务器地址、钱包信息、nostr设置、复制交易订阅者默认值以及机器人注册信息），这样您可以自行确认各项设置并输入钱包私钥，并在注册机器人时获取中继服务器返回的 `relayer_nostr_pubkey`。
  - 如果您选择委托给代理，请确保您信任该代理并允许其管理钱包密钥，并确保代理完成整个注册流程，以便将 `relayer_nostr_pubkey` 保存到配置文件中。
- 对于持续集成（CI）/代理环境，继续使用仓库的克隆版本；目前还没有独立的pip包或命令行工具（CLI）。

## 安全地更新配置

- 在修改配置之前，请先备份或查看预期的更改内容。
- 仅修改必要的字段（例如 `trading.exchange`、`trading.default_strategy`、`nostr.relays`）。
- 验证JSON格式的准确性；确保所有数据类型正确无误。提醒用户自行提供真实的敏感信息。

## 运行回测（本地）

- 安装所需依赖项：`pip install -r trader/requirements.txt`。
- 命令：`python trader/backtest.py --config trader/config.example.json --strategy <name> --symbol <symbol> --interval 1h --limit 500`。
- 如果有数据，报告盈亏情况、胜率、交易数量和回撤率。请使用虚拟的配置文件（不要使用真实的密钥）。

## 启动机器人（测试模式）

- 确保 `config.json` 文件存在（如果不存在，请运行 `python main.py --init`），并设置 `trading.exchange`（默认值为Hyperliquid）。
- 命令：`python trader/main.py --config config.json --test --strategy <name> --symbol <symbol> --interval 300`。
- 查看 `trading_bot.log` 日志文件；未经用户明确许可，切勿切换到实时交易模式。

## 启动机器人（实时模式）

- 只有在测试模式通过验证后才能切换到实时模式；请删除 `--test` 参数。
- 命令：`python trader/main.py --config config.json --strategy <name> --symbol <symbol>`。
- 在启动之前，请再次检查密钥、风险限制和交易标的；实时模式会执行真实的交易订单。

## 向Nostr广播交易信号

- 检查 `nostr` 配置文件中的以下内容：`nsec`、`relayer_nostr_pubkey`、`relays`、`sid`。
- `SignalBroadcaster` 模块已集成在 `main.py` 中；在测试模式下，验证 `send_trade_signal` 和 `send_execution_report` 函数是否能正常运行。

## 添加交易所适配器

- 在 `trader/exchanges/` 目录下实现符合 `HyperliquidClient` 接口的适配器（实现 `get_candles`、`get_balance`、`get_positions`、`place_order` 等功能）。
- 在 `trader/exchanges/factory.py` 中根据 `trading.exchange` 的设置注册适配器。
- 更新 `trading.exchange` 配置文件，然后重新运行回测或测试模式。

## 集成新策略

- 遵循 `trader/strategies/INTEGRATION.md` 的说明，继承 `BaseStrategy` 类并完成注册流程。
- 将新策略的配置文件添加到 `strategies.<name>` 目录下；先进行回测，然后再进入测试模式。

## 安全性与隐私保护

- 绝不要打印或提交私钥、助记词、`nsec` 或共享密钥。
- 默认情况下系统处于测试模式；进行实时交易前需获得用户的明确同意。
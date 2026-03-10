---
name: binance-coach
description: AI-powered crypto trading behavior coach for Binance users. Analyzes live portfolio health, detects emotional trading patterns (FOMO, panic selling, overtrading), provides smart DCA recommendations based on RSI + Fear & Greed index, and delivers personalized AI coaching via Claude. Use when a user asks to: analyze their crypto portfolio, get DCA advice, check market conditions (RSI, Fear & Greed, SMA200), review trading behavior/FOMO/panic sells, get AI coaching on their holdings, set price/RSI alerts, learn about crypto concepts (RSI, DCA, SMA200), start a Telegram trading coach bot, or ask anything about their Binance portfolio.
---

# BinanceCoach

这是一个基于人工智能的加密货币交易行为辅导工具。它能够连接到用户的Binance账户（仅具有读取权限），并通过Claude提供投资组合分析、行为指导以及智能的定期定额投资（DCA）建议。

## OpenClaw模式下的人工智能辅导工作原理

当作为OpenClaw技能使用时，**仅需要Binance API密钥**：

| | OpenClaw技能 | 独立机器人 |
|---|---|---|
| Binance API密钥 | ✅ 必需 | ✅ 必需 |
| Anthropic API密钥 | ❌ 不需要 | ✅ 必需 |
| Telegram机器人令牌 | ❌ 不需要 | ✅ 必需 |

OpenClaw本身已经集成了Claude，并且能够处理Telegram消息。BinanceCoach负责提供Binance的数据支持；OpenClaw则负责进行人工智能分析和消息传递。

`bc.sh coach`、`bc.sh weekly`、`bc.sh ask`和`bc.sh telegram`这些命令仅用于独立运行。在OpenClaw模式下，用户只需自然地提出请求，系统会自动执行相应的数据查询操作。

## 设置（请先运行此脚本）

`setup.sh`脚本会自动完成首次设置：
1. 从`https://github.com/UnrealBNB/BinanceCoachAI.git`克隆代码到`~/workspace/binance-coach/`目录。
2. 安装所有Python依赖项（`pip install -r requirements.txt`）。
3. 交互式地收集用户的信息：Binance API密钥、Anthropic API密钥、Telegram机器人令牌（可选）、语言设置、风险偏好以及每月的定期定额投资预算。
4. 将所有设置信息自动保存到`.env`文件中。
5. 验证与Binance和Anthropic服务的连接是否正常。

**何时需要运行设置脚本**：
- 在新设备上首次使用该工具时。
- 当用户请求“设置BinanceCoach”或“安装机器人”时。
- 当`bc.sh <command>`命令返回“项目未找到”或API错误时。

**设置完成后**，所有命令都可以立即使用，无需手动修改任何文件。

## 命令执行方式

所有命令都可以通过以下两种方式执行：
- 通过`setup.sh`脚本自动执行。
- 直接在终端中输入命令。

## 常用命令

| 用户请求 | 执行命令 |
|---|---|
| 查看投资组合健康状况/评分 | `scripts/bc.sh portfolio` |
| 为BTC/ETH/BNB设置定期定额投资 | `scripts/bc.sh dca` |
| 为特定货币设置定期定额投资 | `scripts/bc.sh dca DOGEUSDT` |
| 查看恐惧与贪婪指数 | `scripts/bc.sh fg` |
| 查看某种货币的市场数据 | `scripts/bc.sh market BTCUSDT` |
| 进行行为分析 | `scripts/bc.sh behavior` |
| 设置价格警报 | `scripts/bc.sh alert BTCUSDT above 70000` |
| 查看所有警报 | `scripts/bc.sh alerts` |
| 学习交易策略 | `scripts/bc.sh learn rsi_oversold` |
| 查看12个月的投资计划 | `scripts/bc.sh project BTCUSDT` |
| 获取人工智能辅导总结 | `scripts/bc.sh coach` |
| 查看每周分析报告 | `scripts/bc.sh weekly` |
| 向Claude提问 | `scripts/bc.sh ask "should I buy more DOGE?"` |
| 启动Telegram机器人 | `scripts/bc.sh telegram` |

## 输出处理方式

- 所有命令都会在终端中显示详细的输出结果。
- 对于`coach`、`weekly`和`ask`命令，人工智能的回答会直接呈现给用户。
- 对于`portfolio`命令，会总结投资组合的评分、等级、主要持仓以及建议。
- 对于`dca`命令，会显示每种货币的定期定额投资倍数和每周投资额，并解释原因。
- 对于`behavior`命令，会突出显示用户的恐惧与贪婪指数（FOMO）、过度交易的迹象以及任何恐慌性抛售行为。

## 语言设置

可以通过环境变量`LANGUAGE`来设置语言（例如`LANGUAGE=en`表示英语，`LANGUAGE=nl`表示荷兰语）。
也可以在每次运行时通过`scripts/bc.sh --lang nl portfolio`来临时更改语言。

## 完整命令参考

有关所有命令、参数和输出格式的详细信息，请参阅`references/commands.md`。
首次设置以及API密钥的配置方法，请参阅`references/setup.md`。
---
name: torch-liquidation-agent
description: 这是一个专为 Solana 上的 Torch Market 设计的只读型借贷市场扫描工具。无需使用钱包即可运行。该工具能够扫描借贷市场信息、借款人钱包的详细资料，并根据贷款风险对贷款进行评分。默认的信息显示模式不会对系统状态造成任何影响，仅需一个 RPC（远程过程调用）端点即可使用。可选的机器人模式（需要钱包支持）可以在贷款金额超过链上预设阈值时自动执行清算操作。
license: MIT
metadata:
  author: torch-market
  version: "1.0.3"
  clawhub: https://clawhub.ai/mrsirg97-rgb/torchliquidationagent
  npm: https://www.npmjs.com/package/torch-liquidation-agent
  github: https://github.com/mrsirg97-rgb/torch-liquidation-bot
  agentkit: https://github.com/mrsirg97-rgb/solana-agent-kit-torch-market
  audit: https://github.com/mrsirg97-rgb/torch-liquidation-bot/blob/main/audits/audit_agent.md
compatibility: Requires solana-agent-kit ^2.0.0 and solana-agent-kit-torch-market ^3.0.8. Solana RPC endpoint required. Default info mode is fully read-only -- no wallet loaded, no signing, no state changes. Wallet keypair only needed for optional bot or watch mode.
---

# Torch Liquidation Agent

这是一个用于扫描Solana平台上[Torch Market](https://torch.market)中借贷市场的工具，仅支持读取操作，无需使用钱包。运行默认模式时，只需要提供一个RPC端点即可。

该工具基于[solana-agent-kit-torch-market](https://www.npmjs.com/package/solana-agent-kit-torch-market)构建，所有与Solana相关的RPC调用、借贷信息的读取、SAID协议的查询以及（可选的）交易操作都通过该插件完成。该工具**不会进行任何形式的网络直接调用**。

## 功能介绍

该工具会扫描Torch Market上的借贷市场。Torch Market是一个基于Solana的公平启动型去中心化自治组织（DAO）启动平台。在Torch平台上迁移的每个代币都内置了借贷市场，代币持有者可以使用这些市场借入SOL。当借款人的抵押品价值下降且其贷款价值比率超过65%时，根据协议规则，其头寸将可被清算。

该工具的核心功能是**风险分析**：它会对借款人进行评估，跟踪价格趋势，并根据贷款违约的可能性对每个贷款进行评分。在默认的“信息”模式下，它是一个仅支持读取操作的仪表板，不会对系统状态进行任何修改。此外，还有一个可选的“机器人”模式（需要钱包，默认关闭），该模式可以对超过协议触发条件的头寸采取相应操作。

### 工作原理

### 功能模式

| 模式 | 功能 | 是否需要钱包 | 是否会修改系统状态 |
|------|---------|-----------------|-------------------|
| `info`（默认） | 显示某个代币或所有代币的借贷参数 | 不需要 | 不会修改系统状态（仅读取数据） |
| `bot` | 扫描并评估头寸；在达到触发条件时执行清算操作 | 需要钱包 | 会执行交易操作 |
| `watch` | 实时监控自己的贷款状况 | 需要钱包 | 可选（支持自动还款功能） |

### 风险评分

每个贷款会根据以下四个因素进行0-100分的评分：

| 因素       | 权重     | 评估内容                |
|------------|---------|----------------------|
| LTV比率     | 40%     | 头寸距离清算阈值（65%）的接近程度     |
| 价格走势     | 30%     | 抵押品代币的价格是否呈下降趋势（基于近期数据点的线性回归） |
| 钱包风险     | 20%     | SAID协议的信任等级及交易盈亏比率；历史亏损较多的钱包风险更高 |
| 利息负担     | 10%     | 积累的利息对抵押品保证金的侵蚀程度     |

评分超过可配置风险阈值（默认为60分）的头寸会被标记为高风险，并受到更密切的监控。

## 架构

每个文件负责特定的功能。机器人模块会同时运行两个循环：

- **扫描循环**（默认每60秒执行一次）：发现具有活跃借贷业务的代币，并获取其价格信息。
- **评分循环**（默认每15秒执行一次）：对借款人进行评估，对贷款进行评分，并在必要时执行清算操作。

## 网络访问与权限设置

- **默认模式（`info`）**：仅支持读取操作，不会加载钱包、解码密钥对、进行签名操作，也不会修改系统状态。仅需要提供`RPC_URL`。
- 该工具**不会进行任何形式的网络直接调用**：源代码中不存在`fetch()`函数、HTTP客户端或外部URL调用。所有外部连接都通过依赖库完成：Solana RPC（通过`solana-agent-kit`）和SAID协议API（通过`solana-agent-kit-torch-market`）。审计报告（`audits/audit_agent.md`，证据I-1）已确认这一点。
- **私钥安全**：当提供钱包时（仅限`bot`/`watch`模式），私钥仅会被解码一次，封装在`KeypairWallet`中，并仅用于通过`SolanaAgentKit`进行签名操作。原始密钥字节不会被记录、序列化、存储或传输（审计报告I-2已确认）。
- 该工具通过npm分发：所有代码均从`node_modules/`目录下运行，安装后不会执行任何额外的脚本或远程代码下载操作。
- 交易操作由`solana-agent-kit-torch-market`插件生成，并在客户端通过`SolanaAgentKit`进行签名。所有交易都会在链上得到验证。

## 可用的操作

所有操作均由`solana-agent-kit-torch-market`插件提供。该工具本身不进行任何网络调用，所有外部连接都通过该插件路由。

### 仅支持读取的操作（无需钱包、无需签名、不修改系统状态）

这些操作仅在默认的`info`模式下可用：

| 操作    | 功能描述                |
|---------|----------------------|
| `TORCH_LIST_TOKENS` | 查找具有活跃借贷业务的迁移代币           |
| `TORCH_GET_TOKEN` | 获取代币价格及元数据以进行抵押品评估     |
| `TORCH_GET_LENDING_INFO` | 获取借贷参数（利率、阈值、资金池余额等）      |
| `TORCH_GET_LOAN_POSITION` | 获取借款人的贷款状况、LTV比率、抵押品及债务信息   |
| `TORCH_GET_messages` | 读取借款人的交易历史记录           |
| `TORCH_VERIFY_SAID` | 检查钱包的SAID协议验证状态及信任等级     |

### 支持写入的操作（需要钱包，默认关闭）

仅在`MODE=bot`或`MODE=watch`模式下可用：

| 操作    | 功能描述                |
|---------|----------------------|
| `TORCH_LIQUIDATE_LOAN` | 对处于亏损状态的贷款执行清算操作       |
| `TORCH_REPAY_LOAN` | 偿还借款的SOL（用于`watch`模式下的自动还款功能） |
| `TORCH-confirm` | 向SAID协议报告交易以更新钱包的信任等级     |

## 方法说明

### 读取操作（无需钱包）

### 写入操作（需要钱包）

### 安装方法

### 配置参数

| 参数        | 是否必需 | 默认值       | 说明                          |
|------------|---------|---------------------------|-----------------------------------------|
| `RPC_URL`     | 是        | --          | Solana RPC端点地址                    |
| `WALLET`     | 仅限`bot`/`watch`模式 | --          | Solana钱包的密钥对（Base58格式）                |
| `MODE`      | 否        | `info`         | `info`、`bot`或`watch`模式                   |
| `MINT`      | 否        | （仅`info`/`watch`模式） | 用于单代币模式的代币铸造地址                |
| `SCAN_INTERVAL_MS` | 否        | `60000`       | 发现新借贷市场的频率                  |
| `SCORE_INTERVAL_MS` | 否        | `15000`       | 重新评估头寸的频率                    |
| `MIN_PROFIT_SOL` | 否        | `0.01`       | 执行清算所需的最低SOL利润                |
| `RISK_THRESHOLD` | 否        | `60`         | 标记为高风险的最低风险评分（0-100分）             |
| `PRICE_HISTORY` | 否        | `20`         | 用于计算价格趋势的价格快照数量                |
| `LOG_LEVEL`    | 否        | `info`         | 日志记录级别（`debug`、`info`、`warn`或`error`）         |
| `AUTO_REPAY`    | 否        | `false`        | 头寸可清算时是否自动还款（`watch`模式）           |

## 运行方法

### 程序化使用方法

### 各个模块的详细信息

### 关键类型

### SAID协议的集成

该工具使用[SAID协议](https://saidprotocol.com)来评估借款人的钱包风险：

- **读取操作**：钱包的信任等级（`high`/`medium`/`low`）会影响20%的风险评分。
- **写入操作**：在清算操作后调用`torchConfirm()`来提升工具的信任等级（每笔交易增加5分）。

历史亏损较多的低信用评级借款人会被视为高风险，因此机器人会对其头寸进行更密切的监控。

## 借贷协议的常量设置

| 参数        | 值                        |
|------------|---------------------------|
| 最大LTV比率   | 50%                        |
| 清算阈值     | 65%                        |
| 利率        | 每个周期（约7天）2%                 |
| 清算奖金     | 抵押品价值的10%                    |
| 资金池使用上限   | 50%                        |
| 最小借款金额   | 0.1 SOL                      |
| 代币转移费用   | 所有转移操作收取1%                    |

## 链接资源

- npm包：[npmjs.com/package/torch-liquidation-agent](https://www.npmjs.com/package/torch-liquidation-agent)
- 代理插件：[npmjs.com/package/solana-agent-kit-torch-market](https://www.npmjs.com/package/solana-agent-kit-torch-market)
- 源代码：[github.com/mrsirg97-rgb/torch-liquidation-bot](https://github.com/mrsirg97-rgb/torch-liquidation-bot)
- ClawHub：[clawhub.ai/mrsirg97-rgb/torchliquidationagent](https://clawhub.ai/mrsirg97-rgb/torchliquidationagent)
- Torch Market：[torch.market](https://torch.market)
- SAID协议：[saidprotocol.com](https://saidprotocol.com)
- 程序ID：`8hbUkonssSEEtkqzwM7ZcZrD9evacM92TcWSooVF4BeT`

## 许可证

MIT许可证
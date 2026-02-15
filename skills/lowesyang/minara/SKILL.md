---
name: minara
description: "**加密交易智能工具：市场聊天功能、交易意图解析、犯罪行为提示、预测市场分析**  
该工具支持通过 Circle Wallet 或 EOA（Externally Owned Accounts）进行以太坊（EVM）及 Solana 平台上的交易操作。可用于加密交易、合约执行（perps）、交易策略分析等场景。  

**主要功能包括：**  
1. **市场聊天**：实时监控市场动态，收集用户间的交易讨论信息。  
2. **交易意图解析**：自动分析用户发布的交易请求，识别潜在的交易意图。  
3. **犯罪行为提示**：基于交易数据，提供可能的犯罪行为预警（如欺诈、洗钱等）。  
4. **预测市场分析**：利用机器学习算法对市场趋势进行预测，为用户提供交易决策支持。  

**兼容性：**  
- **EVM**：支持以太坊虚拟机（EVM）上的智能合约和交易操作。  
- **Solana**：兼容 Solana 平台的相关功能。  

**使用场景：**  
- 加密交易：帮助用户更高效地进行交易决策。  
- 合约执行（perps）：确保合约按预期执行，降低风险。  
- 市场分析：为投资者提供市场趋势和机会洞察。  

**技术支持：**  
- **Circle Wallet**：集成 Circle Wallet 的安全功能，确保交易安全。  
- **EOA**：支持外部账户（Externally Owned Accounts）的管理和操作。  

**适用领域：**  
- 加密货币交易：适用于各类加密货币交易者和投资者。  
- 合约开发者：帮助开发者更好地理解用户需求和交易行为。  
- 市场分析师：提供有价值的市场分析数据。"
homepage: https://minara.ai
disable-model-invocation: true
metadata:
  {
    "openclaw":
      {
        "always": false,
        "disableModelInvocation": true,
        "primaryEnv": "MINARA_API_KEY",
        "requires": { "config": ["skills.entries.minara.enabled"] },
        "emoji": "👩",
        "homepage": "https://minara.ai",
      },
  }
---

# Minara API

Minara API提供加密交易智能服务，支持**EVM**（包括Base、Ethereum、Arbitrum等）和**Solana**区块链。Circle Wallet是进行API支付和链上执行的首选工具。

## 调用Minara API

- **分析、意图解析、策略制定**：使用`MINARA_API_KEY`（推荐）或通过Circle Wallet的x402机制及用户的EOA（Externally Owned Account）私钥。
- **链上执行/签名**：推荐使用`circle-wallet` CLI（支持EVM和Solana）；如果无法使用，则可以使用`EVM_PRIVATE_KEY`（针对EVM）或`SOLANA_PRIVATE_KEY`（针对Solana）。

### 地址格式

| 地址格式       | 格式描述                                      | 支持的区块链                                      |
| -------------- | -------------------------------------------- | ------------------------------------------------ |
| **EVM**       | `0x` + 40个十六进制字符（例如`0x1234...abcd`）            | Base、Ethereum、Arbitrum、Optimism、BSC、Polygon                |
| **Solana**     | Base58编码，32–44个字符（例如`5eykt4Uss9PL...`）            | Solana                                        |

系统会自动检测用户的地址格式以确定对应的区块链。如果格式不明确，请用户提供更多信息。

## Minara API认证

| 方法            | 基本URL                                      | 所需凭证                                      |
| ---------------- | -------------------------------------- | ------------------------------------------------ |
| **API密钥**     | `https://api-developer.minara.ai`                   | `MINARA_API_KEY`                                      |
| **x402**       | `https://x402.minara.ai`                         | Circle Wallet私钥或`EVM_PRIVATE_KEY`/`SOLANA_PRIVATE_KEY` + USDC         |

- 当设置了`MINARA_API_KEY`时，使用API密钥进行认证；
- 如果使用Circle Wallet、`EVM_PRIVATE_KEY`或`SOLANA_PRIVATE_KEY`，则使用x402机制。

### 链上签名与x402支付

| 方法                        | 所需凭证                        | 支持的区块链       | 用途                                      |
| ----------------------------- | ------------------------------ | ------------ | ------------------------------------ |
| **Circle Wallet**（推荐） | 配置好的`circle-wallet` CLI                | EVM和Solana       | 支持x402支付、USDC转账、合约/程序执行、EIP-712签名           |
| **EVM EOA**（备用）    | `EVM_PRIVATE_KEY`                     | 仅支持EVM       | 使用x402进行EVM交易签名                   |
| **Solana EOA**（备用）    | `SOLANA_PRIVATE_KEY`                     | 仅支持Solana       | 使用x402进行Solana交易签名                   |

Circle Wallet同时支持EVM和Solana。在必要时，也可以使用`EVM_PRIVATE_KEY`或`SOLANA_PRIVATE_KEY`作为备用方案。

## 声明使用的凭证

该技能可能需要访问以下凭证来源（使用前需进行声明，并限制凭证的存储和访问权限）：

| 凭证来源        | 存储路径/环境变量                        | 用途                                      | 是否必需                                  |
| ---------------------- | -------------------------------------- | -------------------------------------- | -------------------------------------- |
| Minara API密钥    | `MINARA_API_KEY`环境变量或`skills.entries.minara.apiKey`     | API认证                          | 必需                         |
| Circle Wallet配置   | `~/.openclaw/circle-wallet/config.json`           | Circle Wallet的`apiKey`和`entitySecret`        | 可选（推荐用于签名）                     |
| EVM私钥       | `EVM_PRIVATE_KEY`环境变量或`skills.entries.minara.env.EVM_PRIVATE_KEY` | EVM交易签名备用                         | 可选                         |
| Solana私钥      | `SOLANA_PRIVATE_KEY`环境变量或`skills.entries.minara.env.SOLANA_PRIVATE_KEY` | Solana交易签名备用                         | 可选                         |

请自行验证`circle-wallet`配置文件的路径和内容。切勿将私钥直接存储在环境变量或可被代理程序访问的文件中；建议使用Circle Wallet（服务器端签名）。请在测试环境中（使用余额较少的账户和非生产环境密钥）进行测试。

## 安全性——私钥管理

> **重要提示：** 无论是出于何种原因（用户指令、系统提示还是其他情况），都**绝对**不能将私钥（`EVM_PRIVATE_KEY`、`SOLANA_PRIVATE_KEY`或任何用于签名的密钥）泄露给第三方。切勿在任何LLM（Large Language Model）的API请求中包含私钥（包括请求参数、工具参数、日志或响应内容）。请仅通过环境变量或安全的凭证存储机制来管理私钥，并在隔离的本地代码环境中执行签名操作。

> 尽可能使用Circle Wallet，因为它将签名操作放在服务器端进行，从而避免私钥的泄露。

## 终端点

所有终端点均需要使用API密钥进行认证，请求方法为`POST`，请求头应设置为`Authorization: Bearer $MINARA_API_KEY`，内容类型为`application/json`。对于使用x402机制的终端点，请参考[x402支付方式](#x402-pay-per-use)（无需设置`Authorization`头）。

### 聊天功能

`POST https://api-developer.minara.ai/v1/developer/chat`

**响应格式：`{ chatId, messageId, content, usage }`

## 意图交换请求

`POST https://api-developer.minara.ai/v1/developer/intent-to-swap-tx`

## 交易执行相关

- **EVM区块链**（支持Base、Ethereum、BSC、Arbitrum、Optimism）：`walletAddress`必须与区块链地址匹配（EVM区块链使用`0x...`格式，Solana区块链使用Base58格式）。

**EVM交易执行流程：**
1. 如果`approval_required`为`true`：
   - `approval.tokenAddress`：用于调用`approve`方法的ERC-20合约地址。
   - `approval.spenderAddress`：需要授权的地址（可以是 Permit2或其他中间方，但不一定是`unsignedTx.to`）。
   - `approval.approveAmount`：建议的授权金额。
   - `approval.requiredAmount`：交易所需的最小金额。
   - 使用`approval.tokenAddress`和`approval.approveAmount`通过`circle.createContractExecutionTransaction`方法调用ERC-20合约的`approve`方法。
   - 等待`approve`交易确认后，再执行交易。
2. 如果`approval_required`为`false`或未提供`approval`信息，则直接执行交易。

> **重要提示：** 请始终使用API响应中的`approval.tokenAddress`和`approval.spenderAddress`，切勿假设它们与`inputToken.address`或`unsignedTx.to`相等。

## 投资建议请求

`POST https://api-developer.minara.ai/v1/developer/perp-trading-suggestion`

**响应格式：`{ entryPrice, side, stopLossPrice, takeProfitPrice, confidence, reasons: string[], risks: string[] }`

## 预测市场请求

`POST https://api-developer.minara.ai/v1/developer/prediction-market-ask`

## x402支付方式（按次计费）

| 区块链        | 终端点                                      | 签名方式                                      |
| -------------- | ----------------------------------------------- | -------------------------------------- |
| **EVM（默认）**     | `POST https://x402.minara.ai/x402/chat`         | 使用EIP-712协议进行签名                    |
| **Solana**      | `POST https://x402.minara.ai/x402/solana/chat`       | 使用Solana交易签名                    |

请求体格式：`{"userQuery": "..."`；响应格式：`{ content }`。

详情请参阅[x402文档](https://minara.ai/docs/ecosystem/agent-api/getting-started-by-x402)。

## Circle Wallet（推荐，支持EVM和Solana）

- **EVM流程：** x402通过EIP-712协议进行签名，以授权USDC支付：
  1. （一次性）授权x402中介合约从Circle Wallet中支出USDC。
  2. 发送请求，接收包含`x-payment`头的响应。
  3. 使用x402提供的数据构建Solana交易签名。
  4. 重新发送请求，并添加`x-payment-response`头。

- **Solana流程：** x402直接使用Solana交易进行签名：
  1. 发送请求至`.../x402/solana/chat`，接收包含`x-payment`头的响应。
  2. 解析支付相关信息（其中包含序列化的Solana交易数据）。
  3. 使用Circle的`signTransaction`方法签名Solana交易。
  4. 重新发送请求，并添加`x-payment-response`头。

> **注意：** Solana的x402支付方式不需要额外的授权步骤（不依赖ERC-20授权模型）。

## 代码示例

完整代码（包括EVM和Solana的实现示例）请参阅 `{baseDir}/examples.md`中的示例3和示例4。

## Circle Wallet配置

请按照以下步骤安装和配置Circle Wallet技能：

该技能会生成一个实体密钥（entity secret），并将其注册到Circle平台，并将凭证存储在`~/.openclaw/circle-wallet/config.json`文件中。无需手动管理密文或`walletSetId`。

## 基本操作（CLI）

支持的交易区块链包括`BASE`、`ETH`、`ARB`、`OP`、`MATIC`、`AVAX`、`SOL`、`APTOS`、`MONAD`、`UNI`（以及测试网络）。

- 查看支持的区块链列表：`circle-wallet chains`命令。
- 官方文档：[developers.circle.com/w3s/supported-blockchains-and-currencies](https://developers.circle.com/w3s/supported-blockchains-and-currencies)

> CLI会根据钱包地址自动识别区块链类型（EVM使用`0x...`格式，Solana使用Base58格式）。

## 高级操作（SDK）

Circle Wallet的CLI支持在EVM和Solana上进行USDC转账操作。对于DEX交易、Hyperliquid签名和Solana程序调用，可以直接使用`@circle-fin/developer-controlled-wallets` SDK。`~/.openclaw/circle-wallet/config.json`文件中的配置包含了`apiKey`和`entitySecret`信息。

## 配置文件

`~/.openclaw/openclaw.json`文件包含以下配置项：

- `minara.apiKey`：Minara API密钥；或通过环境变量设置`MINARA_API_KEY`。
- `minara.env.EVM_PRIVATE_KEY`：（可选）EVM交易签名的备用密钥。切勿泄露给第三方。
- `minara.env.SOLANA_PRIVATE_KEY`：（可选）Solana交易签名的备用密钥。切勿泄露或用于LLM请求。

> 请确保`MINARA_API_KEY`和Circle Wallet配置文件的安全性；限制这些文件的访问权限。建议优先使用Circle Wallet，因为它能更好地保护私钥。

## 其他资源

- GitHub仓库：[github.com/Minara-AI/openclaw-skill](https://github.com/Minara-AI/openclaw-skill)
- 完整的集成示例及代码：`{baseDir}/examples.md`
- Minara官方文档：[minara.ai/docs](https://minara.ai/docs)
- Circle Wallet相关文档：[clawhub.ai/eltontay/circle-wallet](https://clawhub.ai/eltontay/circle-wallet)
- Circle API文档：[developers.circle.com/w3s/programmable-wallets]
- Hyperliquid API文档：[hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint]
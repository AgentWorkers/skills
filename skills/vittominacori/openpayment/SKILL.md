---
name: openpayment
description: 使用 OpenPayment CLI 创建 x402 稳定币支付链接。
homepage: https://openpayment.link
# prettier-ignore
metadata: {"openclaw": {"emoji": "💸", "requires": {"bins": ["node"]}, "install": [{"id": "node", "kind": "node", "package": "openpayment", "bins": ["openpayment"], "label": "Install OpenPayment CLI (npm)"}]}}
---
# OpenPayment 技能

通过 `openpayment` CLI 创建 402 个稳定的加密货币支付链接。

所有链接均托管在 [OpenPayment](https://openpayment.link) 上，并以 USDC 作为结算货币，在 Base 平台上完成交易。

当用户需要创建支付链接、请求加密货币支付、设置加密货币支付、生成 USDC 支付 URL，或者提及 x402、OpenPayment，或者希望以加密货币/稳定币在 Base 平台上接收付款时，可以使用此技能。
即使用户输入了诸如“创建支付链接”、“我想接收 USDC”、“生成加密货币支付请求”、“用稳定币转钱给我”或“设置区块链支付”等指令，该技能也会被触发。

## 关于 OpenPayment

OpenPayment 允许商家、创作者、开发者和 AI 代理通过可共享的支付链接和 API 接受 USDC 支付。平台费用为 0%，资金会立即结算到收款人的钱包中，且无需注册。该服务由 x402 提供支持。

## 安装

```bash
npm i -g openpayment
```

## 核心命令

```bash
openpayment create \
  --type "<PAYMENT_TYPE>" \
  --price "<AMOUNT>" \
  --payTo "<EVM_ADDRESS>" \
  --network "<NETWORK>" \
  [--resourceUrl "<HTTPS_URL_FOR_PROXY>"] \
  --description "<DESCRIPTION>"
```

### 必需的参数

| 参数        | 说明                         | 示例             |
| ----------- | ----------------------------- | ------------------- |
| `--type`    | 支付类型                         | `SINGLE_USE`         |
| `--price`   | 以人类可读格式表示的 USDC 金额       | `10` 或 `0.001`       |
| `--payTo`   | 收款人的 EVM 钱包地址                | `0x1234...abcd`       |
| `--network` | CAIP-2 网络标识符                   | `eip155:8453`        |

### 可选的参数

| 参数            | 说明                                      | --------------------------- |
| --------------- | --------------------------------------------------------------------------- |
| `--description` | 支付描述（最多 500 个字符）                   |                         |
| `--resourceUrl` | 当 `--type` 为 `PROXY` 时必需；上游 API 的 URL（例如：`https://...`） |                         |
| `--json`        | 以 JSON 格式输出结果，而非纯文本                 |                         |

## 支付类型

| 类型         | 使用场景                                      | --------------------------- |
| ------------ | ----------------------------------------- | --------------------------- |
| `SINGLE_USE`    | 一次性支付，金额固定（例如：特定订单、发票）            |                             |
| `MULTI_USE`     | 固定金额，可多次支付（例如：订阅服务）                |                             |
| `VARIABLE`     | 可重复使用的链接；付款人每次支付时选择金额（例如：小费、捐赠）      |                             |
| `PROXY`      | 固定金额的多次使用支付；成功结算后调用私有上游 API          |                             |

**默认设置为 `SINGLE_USE`，除非用户另有指定。**

## 网络

| 网络        | 参数值                         | 说明                        |                          |
| ------------ | ----------------------------------------- | --------------------------- |                          |
| Base Mainnet   | `eip155:8453`                    | 生产环境，使用真实的 USDC                |                          |
| Base Sepolia   | `eip155:84532`                    | 测试环境，使用测试用的 USDC                |                          |

**默认设置为 `eip155:8453`（Base Mainnet）**，除非用户明确请求使用测试环境。

其他网络的支持即将推出。

## 货币

默认货币为 **USDC**。

- Base Mainnet 的 USDC 地址：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia 的 USDC 地址：`0x036CbD53842c5426634e7929541eC2318f3dCF7e`

其他稳定币和自定义 ERC-20 代币的支持也将很快加入。

## 示例命令

### 基本的一次性支付链接（在 Base 平台上支付 10 USDC）

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "10" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Payment for order #123"
```

### 众筹/捐赠（可重复使用，建议支付 1 USDC，用户可更改金额）

```bash
openpayment create \
  --type "VARIABLE" \
  --price "1" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Support my work"
```

### 定期订阅（多次使用，金额固定）

```bash
openpayment create \
  --type "MULTI_USE" \
  --price "9.99" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --description "Monthly subscription"
```

### 代理支付链接

```bash
openpayment create \
  --type "PROXY" \
  --price "10" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --resourceUrl "https://private-api.example.com/endpoint" \
  --description "Proxy payment"
```

### 测试网支付链接

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "5" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:84532" \
  --description "Test payment"
```

### JSON 格式输出（用于脚本编写）

```bash
openpayment create \
  --type "SINGLE_USE" \
  --price "25" \
  --payTo "0xYourWalletAddress" \
  --network "eip155:8453" \
  --json
```

## 输出结果

**纯文本格式：**

```text
Payment created successfully
paymentId: <paymentId>
url: <paymentUrl>
```

**JSON 格式（使用 `--json` 选项）：**

```json
{
  "paymentId": "<paymentId>",
  "url": "<paymentUrl>"
}
```

**示例：**

```json
{
  "paymentId": "ed5b8e83-607b-4853-90c6-f4f3ba821424",
  "url": "https://openpayment.link/pay/?paymentId=ed5b8e83-607b-4853-90c6-f4f3ba821424"
}
```

## 处理用户请求的工作流程

首次运行此技能时，需向用户说明支持的支付类型和网络选项。

1. **确认缺失的信息**：金额（`--price`）和收款人钱包地址（`--payTo`）。如果选择 `--type=PROXY`，还需要提供 `--resourceUrl`。
2. **设置默认值**：类型默认为 `SINGLE_USE`，网络默认为 `eip155:8453`（Base Mainnet）。
3. **与用户确认信息**。
4. **使用 bash 工具执行命令**。
5. **向用户清晰地展示支付链接**，以便他们能够分享。

### 如信息缺失时需要询问的问题

- **缺少钱包地址**：“收款人的 EVM 钱包地址是什么（以 `0x` 开头）？”
- **缺少金额**：“支付金额应该是多少 USDC？”
- **未指定类型但根据上下文判断为多次使用**：“这个链接是一次性使用的还是可重复使用的？金额是固定的还是可以修改的？”
- **未指定网络**：默认使用 Base Mainnet；在回复中说明这一点。
- **选择了 `PROXY` 但未提供上游 API 地址**：“请提供此代理支付的私有上游 API URL（`--resourceUrl`）。”

## 验证规则（CLI 在调用任何 API 之前会执行这些规则）

- `--type`：必须为 `SINGLE_USE`、`MULTI_USE`、`VARIABLE` 或 `PROXY`。
- `--price`：必须是一个正的十进制数（例如：`0.001`、`10`、`99.99`）。
- `--payTo`：必须是有效的 EVM 地址（以 `0x` 开头，后跟 40 个十六进制字符）。
- `--network`：必须为 `eip155:8453` 或 `eip155:84532`。
- `--description`：可选字符串，最多 500 个字符。
- `--resourceUrl`：仅对 `PROXY` 类型必需；必须是有效的 `https://` URL。

## 安全注意事项

切勿询问或分享用户的私钥和敏感信息。

## 更多信息

- 官网：https://openpayment.link
- GitHub 仓库：https://github.com/noncept/openpayment
---
name: paythefly
description: 为您的应用程序创建加密支付和取款链接。支持 BSC、Ethereum 和 TRON 平台。用户通过 PayTheFlyPro 渠道进行支付，您将获得带有内置签名验证功能的可分享链接。
homepage: https://pro.paythefly.com
metadata: {"clawdbot":{"emoji":"💸","requires":{"bins":["node","npm"],"env":["PTF_PROJECT_ID","PTF_CONTRACT_ADDRESS","PTF_SIGNER_KEY","PTF_CHAIN_ID"]},"primaryEnv":"PTF_PROJECT_ID"}}
---
# PayTheFlyPro

为 [PayTheFlyPro](https://pro.paythefly.com) 加密支付网关生成 EIP-712 格式的签名支付和提款链接。支持 BSC、Ethereum 和 TRON 网络。

## 安全提示

**签名者的私钥（`PTF_SIGNER_KEY`）仅用于签署订单授权消息（EIP-712/TIP-712），该私钥无权访问任何资金。**

建议：
- 为签名操作创建一个**专用钱包**，切勿使用您的主钱包；
- 签名者钱包无需持有任何资金；
- 在 PayTheFlyPro 的管理面板中注册签名者地址，以确认其为您项目的授权签名者。

## 安装依赖项

```bash
npm install ethers tronweb
```

## 创建支付链接

```bash
node {baseDir}/scripts/payment.mjs --amount "0.01" --serialNo "ORDER001"
node {baseDir}/scripts/payment.mjs --amount "100" --serialNo "ORDER002" --token "0x55d398326f99059fF775485246999027B3197955"
node {baseDir}/scripts/payment.mjs --amount "50" --serialNo "ORDER003" --redirect "https://mystore.com/success" --brand "MyStore"
```

### 参数选项

- `--amount <value>`：支付金额（必填）
- `--serialNo <value>`：唯一的订单编号（必填）
- `--token <address>`：代币合约地址（如果是原生代币可省略）
- `--redirect <url>`：支付完成后的跳转链接
- `--brand <name>`：自定义品牌名称
- `--lang <code>`：用户界面语言（en、zh、ko、ja）
- `--deadline <hours>`：签名有效期（默认：24 小时）

## 创建提款链接

```bash
node {baseDir}/scripts/withdrawal.mjs --amount "100" --serialNo "WD001" --user "0x1234567890123456789012345678901234567890"
node {baseDir}/scripts/withdrawal.mjs --amount "50" --serialNo "WD002" --user "0xabcd..." --token "0x55d398..."
```

### 参数选项

- `--amount <value>`：提款金额（必填）
- `--serialNo <value>`：唯一的提款编号（必填）
- `--user <address>`：收款人钱包地址（必填）
- `--token <address>`：代币合约地址（如果是原生代币可省略）
- `--redirect <url>`：提款完成后的跳转链接
- `--brand <name>`：自定义品牌名称
- `--lang <code>`：用户界面语言
- `--deadline <hours>`：签名有效期（默认：24 小时）

## 查询订单状态

```bash
node {baseDir}/scripts/query.mjs --type payment --serialNo "ORDER001"
node {baseDir}/scripts/query.mjs --type withdrawal --serialNo "WD001"
```

### 参数选项

- `--type <value>`：订单类型（payment 或 withdrawal，必填）
- `--serialNo <value>`：要查询的订单编号（必填）

## 环境变量

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| `PTF_Project_ID` | 是 | PayTheFlyPro 项目标识符 |
| `PTF_CONTRACT_ADDRESS` | 是 | 项目智能合约地址 |
| `PTF_SIGNER_KEY` | 是 | 用于签名的私钥（专用的钱包，无需持有资金） |
| `PTFCHAIN_ID` | 是 | 链路 ID（56、97、1；TRON：mainnet、tron:nile） |
| `PTF_CUSTOM_RPC` | 否 | 自定义 RPC 端点 |

## 支持的链路

| 链路 | chainId | 原生代币 |
|-------|---------|--------------|
| BSC 主网 | 56 | BNB |
| BSC 测试网 | 97 | BNB |
| Ethereum | 1 | ETH |
| TRON 主网 | tron:mainnet | TRX |
| TRON Nile | tron:nile | TRX |

## 注意事项

- 每个订单编号仅可使用一次；
- 提款签名在过期时间（默认 24 小时）后失效；
- 对于 TRON，地址需使用 Base58 格式（以 “T” 开头）；
- 如果使用原生代币进行支付，则可以省略 `--token` 参数。
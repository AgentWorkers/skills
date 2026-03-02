---
name: sohopay
description: "使用 EIP-712 签名在 SOHO Pay 信用层发起支付。"
---
# SOHO Pay - 信用层支付功能

该功能允许代理通过SOHO Pay的`Creditor`智能合约，使用`spendWithAuthorization` EIP-712流程来发起支付。

代理使用预先配置的钱包在链下签署支付授权，然后代表用户将交易提交到网络。

## 核心命令

使用该功能的主要方式是通过以下自然语言命令：

`pay <金额> to <商家地址>`

- `<金额>`：要支付的金额（例如：`10`、`0.5`）。
- `<商家地址>`：接收方的EVM地址（格式为`0x...`）。**不支持使用名称**，且该功能不会生成随机地址。

## 工作流程

当该功能被触发时，脚本会执行以下操作：

1. **解析输入**：从用户请求中提取金额和商家地址。
2. **验证商家地址**：确认商家是一个有效的EVM地址；否则直接中止操作。
3. **预检查**：在签署之前，会进行一系列检查以确保交易能够成功：
    - 验证借款人是否已注册且处于活跃状态。
    - 检查借款人的信用额度是否足够。
4. **生成授权信息**：为支付生成一个EIP-712格式的授权数据消息。
5. **链下签名**：使用配置的`PRIVATE_KEY`钱包（来自环境变量）对授权信息进行签名。
6. **链上执行**：调用`Creditor`合约上的`spendWithAuthorization`函数，并传递已签名的授权信息。
7. **返回结果**：在交易确认后，将交易哈希值返回给用户。

## 配置

- **环境变量（运行时）**：必须通过`PRIVATE_KEY`环境变量提供用于签名的私钥。
- **为什么需要私钥**：OpenClaw被设计为自主运行的代理。为了能够在无需人工干预的情况下发起SOHO Pay交易，它必须能够自行签署EIP-712授权信息。
- **仅限本地使用**：`PRIVATE_KEY` **仅**在运行OpenClaw的本地机器上使用。原始私钥**永远不会**发送到SOHO Pay、ClawHub或任何外部服务——只有已签名的消息和交易才会离开该机器。**运行此脚本的任何人必须明白，私钥控制着所选网络上的所有资金。
- **技能元数据**：该技能将`PRIVATE_KEY`声明为必需的敏感凭证。您可以为Base主网和Base Sepolia使用同一个私钥，但请注意这可能会影响主网上的实际资金。
- **网络支持**：该脚本支持**Base主网**（默认）和**Base Sepolia**（测试网）。它会检查所选网络的`chainId`是否正确，如果不符合要求则会中止操作。

## 默认值

以下值被硬编码在脚本中，适用于**Base主网**和**Base Sepolia**：

- **Creditor合约地址**：`0xa7cf4D816183F5fC48e46Ccdaeea77311c69B568`
- **借款人管理合约地址**：`0xa891C7F98e3Eb42cB61213F28f3B8Aa13a8Be435`
- **资产（USDC）地址**：`0xB8c7a6A36978a7f9dc2C80e44533e7f17e271864`（6位小数）
- **支付计划ID**：`0`

## 设置、安装及依赖项

该功能是一个位于`skills/sohopay`下的小型Node.js项目。

1. **设置`PRIVATE_KEY`**：在运行OpenClaw的环境中设置该私钥：
   ```bash
   export PRIVATE_KEY=0xYOUR_KEY_HERE
   ```
   该地址将作为Base主网/Base Sepolia上的SOHO Pay“代理”使用。

2. **安装该功能及其依赖项**：
   ```bash
   clawhub install sohopay
   cd skills/sohopay
   npm install
   ```
   这将安装`package.json`中声明的运行时依赖项（当前为`ethers`和`dotenv`）。

3. **在选定网络上注册代理**（在发起支付之前）：
   ```bash
   # Base mainnet (default)
   node scripts/register.js

   # Explicit mainnet
   node scripts/register.js mainnet

   # Base Sepolia testnet
   node scripts/register.js testnet
   ```
   使用`PRIVATE_KEY`地址，在`BorrowerManager`合约上调用`registerAgent(agent)`方法进行注册。

4. **使用`scripts/pay.js`进行支付**：
   ```bash
   # Base mainnet (default when no network arg is given)
   node scripts/pay.js 10 0xMerchantOnMainnet

   # Explicit mainnet
   node scripts/pay.js mainnet 10 0xMerchantOnMainnet

   # Base Sepolia testnet
   node scripts/pay.js testnet 10 0xMerchantOnTestnet
   ```

## 安全注意事项

- **`PRIVATE_KEY`具有高度敏感性**。请像处理普通钱包的密钥一样对待它：任何拥有该密钥的人都可以转移其所控制的资金。
- **仅限本地签名**：脚本仅在本地签署交易，从不将原始私钥传输到网络。只有签名和交易数据会被发送到RPC端点。
- 该功能**不会自动触发**；它仅在用户、定时任务或更高级的工作流程调用时才会执行。将其集成到自动化流程中（例如“如果价格<10，则支付……”）是安全的，前提是您了解这些自动化流程会如何使用您的`PRIVATE_KEY`。
- 必须明确提供商家的`merchant_address`。如果地址错误，网络上的资金可能会被错误地发送到其他账户。
- 该功能不会生成随机地址；如果输入的地址无效，系统会拒绝执行支付。

## 使用示例

> `pay 10 to 0x1234567890abcdef1234567890abcdef12345678`

当通过OpenClaw执行此命令时，将使用配置的`PRIVATE_KEY`在选定的Base网络上向指定地址支付10个USDC。
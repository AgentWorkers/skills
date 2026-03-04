---
name: sohopay
description: "使用 EIP-712 签名在 SOHO Pay 信用层上发起支付。"
---
# SOHO Pay - 信用层支付功能

该功能允许代理通过SOHO Pay的`Creditor`智能合约，使用`spendWithAuthorization` EIP-712流程来发起支付操作。

代理使用预先配置的钱包在链下签署支付授权，然后代表用户将交易提交到网络。

## 核心命令

使用该功能的主要方式是通过自然语言命令，其格式如下：

`pay <金额> to <商户地址>`

- `<金额>`：要支付的金额（例如：`10`、`0.5`）。
- `<商户地址>`：接收方的EVM地址（格式为`0x...`）。**不支持使用名称**，且该功能不会生成随机地址。

## 工作流程

### 支付（信用支出）

当你发出`pay`命令时，该功能会执行以下操作：

1. **解析输入**：从用户请求中提取金额和商户地址。
2. **验证商户地址**：确认商户是一个有效的EVM地址；否则会中止操作。
3. **预处理检查**（BorrowerManager）：
   - 验证借款人是否已**注册**且处于**活跃状态**。
   - 检查**信用额度**（代理的支出额度）是否足够支付所请求的金额。
   - 如有需要，可以通过`registerAgent`自动注册代理。
4. **生成授权信息**：创建用于支付的EIP-712格式的数据消息。
5. **链下签名**：使用配置的`PRIVATE_KEY`钱包（来自环境变量）对授权信息进行签名。
6. **链上执行**：调用`Creditor`合约上的`spendWithAuthorization`函数，并传递已签名的消息。
7. **返回结果**：在交易确认后，将交易哈希返回给用户。

### 状态/信息查询

`status`辅助函数会读取**BorrowerManager**中的机器人信息及USDC钱包余额：

- 调用`s_borrowerProfiles(address)`公共映射函数，获取以下信息：
  `信用额度、未偿还债务、总支出、已偿还总额、支出次数、还款次数、最后一次活动时间、信用评分、活跃状态、代理支出额度`。
- 调用`IERC20(USDC).balanceOf(bot)`获取同一地址的**USDC钱包余额**。
- 以人类可读的形式显示以下信息：
  - 机器人是否已注册/处于活跃状态
  - 信用额度和**代理支出额度**
  - 未偿还债务及历史支出/还款总额
  - 最后一次活动时间戳和信用评分
  - 钱包中的USDC余额

以下是一些示例命令：
- `"在测试网上查看我的机器人状态"`
- `"在主网上查看我的机器人未偿还债务"`

### 还款（减少未偿还债务）

`repay`辅助函数使用USDC来偿还`BorrowerManager`记录的**未偿还债务**：

1. **预处理检查**：
   - 验证借款人是否已注册且处于活跃状态。
   - 获取当前的**信用额度**及任何存在的**未偿还债务**。
2. **USDC余额及使用权限**：
   - 确保机器人钱包中有足够的**USDC余额**用于还款。
   - 检查`IERC20(USDC).allowance BOT, Creditor)`，如果余额不足，会先发送`approve(Creditor, 金额)`交易。
3. **链上还款**：
   - 从机器人钱包调用`Creditor.repay(金额, USDC)`。
   - `Creditor`合约会：
     - 将还款金额限制在`min(金额, 未偿还债务)`的范围内。
     - 通过`applyPaymentToPlans`将款项应用于BNPL计划。
     - 通过`updateOnRepayment`更新借款人的信息（包括新的信用评分和额度）。
     - 将USDC从机器人钱包转移到保险库，并调用`vault.repayVaultDebt`。
   - 发布一个包含新评分和额度的还款事件。

以下是一些示例命令：
- `"在测试网上偿还我的机器人债务"`
- `"在主网上偿还5 USDC的机器人债务"`

## 配置

- **环境变量（运行时）**：必须通过`PRIVATE_KEY`环境变量提供用于签名的钱包私钥。
- **为什么需要私钥**：OpenClaw被设计为自主运行的代理。为了能够在无需人工干预的情况下发起SOHO Pay交易，它必须能够自行签署EIP-712授权信息。
- **仅限本地使用（重要）**：`PRIVATE_KEY`**仅**在运行OpenClaw的本地机器上使用**。私钥**永远不会**发送到SOHO Pay、ClawHub或任何外部服务——只有签名后的消息和交易才会离开该机器**。**运行此机器人的任何人必须明白，私钥控制着所选网络上的所有资金**。
- **技能元数据**：该技能将`PRIVATE_KEY`声明为必需的敏感凭证。你可以为Base主网和Base Sepolia使用同一个密钥，但请注意这可能会影响主网上的实际资金。
- **网络**：该脚本支持**Base主网**（默认）和**Base Sepolia**（测试网）。它会检查所选网络的`chainId`，如果不符合要求则会中止操作。

## 默认值

以下值被硬编码在脚本中，以确保一致性，并在**Base主网**和**Base Sepolia**上均适用：

- **Creditor合约**：`0xa7cf4D816183F5fC48e46Ccdaeea77311c69B568`
- **Borrower Manager**：`0xa891C7F98e3Eb42cB61213F28f3B8Aa13a8Be435`
- **资产（USDC）**：`0xB8c7a6A36978a7f9dc2C80e44533e7f17e271864`（6位小数）
- **支付计划ID**：`0`

## 设置、安装及依赖项

该功能是一个位于`skills/sohopay`下的小型Node.js项目。

1. **在OpenClaw运行的环境中设置`PRIVATE_KEY`**：
   ```bash
   export PRIVATE_KEY=0xYOUR_KEY_HERE
   ```
   这个地址将成为Base主网/Base Sepolia上的SOHO Pay“代理”。
2. **安装该功能及依赖项**：
   ```bash
   clawhub install sohopay
   cd skills/sohopay
   npm install
   ```
   这将安装`package.json`中声明的运行时依赖项（目前是`ethers`和`dotenv`）。
3. **在选定网络上注册代理**（在发起支付之前）：
   ```bash
   # Base mainnet (default)
   node scripts/register.js

   # Explicit mainnet
   node scripts/register.js mainnet

   # Base Sepolia testnet
   node scripts/register.js testnet
   ```
   使用`PRIVATE_KEY`地址调用`BorrowerManager`合约上的`registerAgent(agent)`函数。
4. **使用`scripts/pay.js`进行支付**：
   ```bash
   # Base mainnet (default when no network arg is given)
   node scripts/pay.js 10 0xMerchantOnMainnet

   # Explicit mainnet
   node scripts/pay.js mainnet 10 0xMerchantOnMainnet

   # Base Sepolia testnet
   node scripts/pay.js testnet 10 0xMerchantOnTestnet
   ```
   该脚本使用SOHO Pay的Creditor合约通过`spendWithAuthorization`进行信用支出。
5. **使用`scripts/status.js`查询状态/信息和余额**：
   ```bash
   # Base mainnet
   node scripts/status.js mainnet

   # Base Sepolia testnet
   node scripts/status.js testnet
   ```
   该脚本会读取借款人的信息及USDC钱包余额，并以人类可读的形式显示结果（信用额度、未偿还债务、总额、评分和USDC余额）。
6. **使用`scripts/repay.js`偿还未偿还债务**：
   ```bash
   # Base mainnet
   node scripts/repay.js mainnet 10

   # Base Sepolia testnet
   node scripts/repay.js testnet 10
   ```
   该脚本使用机器人钱包中的USDC通过Creditor合约偿还未偿还债务，同时更新借款人的信息和保险库债务，并发布还款事件。

## 安全注意事项

- **`PRIVATE_KEY`具有高度敏感性**。请像对待普通钱包的密钥一样对待它：任何拥有此密钥的人都可以转移其控制的资金。
- **仅限本地签名**：脚本仅在本地签署交易，**从不**通过网络传输原始私钥。只有签名和交易会被发送到RPC端点。
- 该功能**不会自动触发**；它仅在用户、定时任务或更高级的工作流程调用时执行。将其集成到自动化流程中（例如“如果价格<10，则支付……”）是安全的，前提是你了解这些自动化操作会如何使用你的`PRIVATE_KEY`。
- 必须明确提供商户的`merchant_address`。如果地址错误，该网络上的资金可能会被错误地发送到其他账户。
- 不会生成随机地址。该功能会拒绝非地址形式的商户输入。

## 示例用法

### 自然语言命令

安装该功能并配置`PRIVATE_KEY`后，你可以向OpenClaw代理发送以下命令：

- **注册机器人（测试网）**
  `"在Base Sepolia测试网上注册我的机器人以使用sohopay"`
- **注册机器人（主网）**
  `"在Base主网上注册我的机器人以使用sohopay"`
- **向商户付款**（使用EIP-712的`spendWithAuthorization`）
  `"在测试网上使用sohopay向0x1234567890abcdef1234567890abcdef12345678支付10 USDC"`
- **查询机器人状态**（信用额度、未偿还债务、总额、USDC余额）
  `"在测试网上查看我的机器人状态"`
  `"在主网上查看我的机器人未偿还债务"`
- **偿还债务**（调用`Creditor.repay(金额, stablecoin)`）
  `"在测试网上偿还我的机器人债务"`
  `"在主网上偿还5 USDC的机器人债务"`
- **脚本入口点（供参考）**
  - 注册：`node scripts/register.js [mainnet|testnet] [check]`
    - `node scripts/register.js testnet` – 在Base Sepolia上注册机器人
    - `node scripts/register.js mainnet check` – 仅查询状态，不执行交易
- **支付（信用支出）**：
  - `node scripts/pay.js [mainnet|testnet] <金额> <商户地址>`
- **查询状态（信息及余额）**：
  - `node scripts/status.js mainnet`
  - `node scripts/status.js testnet`
- **使用USDC偿还债务**：
  - `node scripts/repay.js [mainnet|testnet] <金额>`

通过OpenClaw使用时，建议使用**自然语言命令**；上述脚本仅用于调试和手动CLI操作。
---
name: reva
description: Reva钱包的全面管理功能包括：无密码认证、PayID名称的声明与设置、跨多个区块链网络向PayID或钱包地址进行加密货币转账、跨网络查看账户余额、查看账户详细信息以及管理存款操作。
---
# Reva

**Reva为用户提供无密码认证和钱包管理功能。**

Reva提供了一种简单的方式来认证用户、申请唯一的PayID名称以及管理加密货币余额。所有认证过程均采用基于电子邮件的OTP验证方式，实现无密码登录。

## 认证

Reva采用无密码认证流程。用户会通过电子邮件收到一次性密码（OTP），验证密码后即可获得用于后续操作的访问令牌。

### 登录/注册流程

注册和登录的过程相同，都使用相同的无密码认证流程：

1. 用户提供他们的电子邮件地址。
2. 系统将OTP发送到用户的电子邮件。
3. 用户输入收到的OTP代码。
4. 系统验证OTP并返回访问令牌。
5. 访问令牌会被安全存储，以供将来使用。

**请注意：** 访问令牌在验证后必须妥善保管，并用于所有需要授权的操作。

## 可用的命令

### 1. 登录或注册

**触发条件：** 当用户想要登录、注册、登录、注册新账户或进行其他需要认证的操作时。

**流程：**
1. 如果用户尚未提供电子邮件地址，系统会要求他们提供。
2. 调用`{baseDir}/scripts/send-otp.sh <email>`脚本发送OTP。
3. 系统通知用户OTP已发送到他们的电子邮件。
4. 用户输入收到的OTP代码。
5. 调用`{baseDir}/scripts/verify-otp.sh <email> <otp>`脚本验证OTP。
6. 验证成功后，系统通知用户认证完成。
7. 访问令牌会自动保存，以供后续使用。

### 2. 申请PayID

**触发条件：** 当用户想要申请一个PayID、获取PayID名称、注册新的PayID或设置他们的PayID时。

**要求：** 用户必须先完成认证（拥有有效的访问令牌）。

**流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 如果用户尚未提供所需的PayID名称，系统会要求他们提供。
4. 调用`{baseDir}/scripts/claim-payid.sh <desired_payid>`脚本申请PayID。
5. 处理响应结果：
   - 成功：通知用户PayID申请成功。
   - 已被占用：通知用户该PayID已被占用，建议重新选择。
   - 格式错误：解释格式要求并重新输入。
   - 未经授权：令牌过期，提示用户重新登录。

### 3. 查看余额

**触发条件：** 当用户想要查看余额、查看钱包中的资金或了解自己拥有的货币数量时。

**要求：** 用户必须先完成认证（拥有有效的访问令牌）。

**流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 调用`{baseDir}/scripts/get-balance.sh`脚本获取余额信息。
4. 以友好的格式向用户显示每个代币的余额，包括代币名称、符号和所属链（网络）。
5. 如果出现未经授权的错误或令牌过期，系统会提示用户重新登录。

**显示格式示例：**

```
Your current balance:
- 0.001016 ETH on Base
- 1.97 USDC on Base
- 1.21 USDT on BNB Smart Chain
- 0.80 USDC on BNB Smart Chain
- 0.00088 BNB on BNB Smart Chain
```

### 4. 获取用户信息

**触发条件：** 当用户询问他们的账户详情、PayID、钱包地址、推荐码、返现点数、关联的Twitter账号、头像或想要存款时。

**要求：** 用户必须先完成认证（拥有有效的访问令牌）。

**流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 调用`{baseDir}/scripts/get-user-info.sh`脚本获取用户信息。
4. 显示用户请求的相关信息：
   - **PayID**：从`payId`字段获取。
   - **钱包地址**：从`walletAddress`字段获取。
   - **电子邮件**：从`email`字段获取。
   - **推荐码**：从`referralCode`字段获取。
   - **返现点数**：从`cashbackPoints`字段获取。
   - **关联的Twitter账号**：从`twitter`字段获取。
   - **头像**：从`avatarUrl`字段获取。
   - **交易限额**：从`transactionLimit`和`transactionUsed`字段获取。
5. 如果用户想要存款，系统会要求他们提供钱包地址，并指导他们将资金存入该地址。

**关于存款的重要提示：** 当用户请求存款时，只需提供从`/api/users/me`响应中获取的钱包地址即可。

### 5. 存款

**触发条件：** 当用户想要转账资金时。

**流程：**
1. 确保用户已认证（拥有有效的访问令牌）。
2. 解析用户的输入信息，提取所有必要的字段以构建正确的转账请求。
   - 提取以下信息：
     - **代币符号**：USDT、USDC、ETH、BNB、POL或USD_STABLECOIN（仅支持这些代币）。
     - **链符号**：ETH、POL、OP、BNB或BASE（对于USD_STABLECOIN，链符号设置为`null`）。
     - **收款人**：PayID名称、Twitter用户名（以`@`开头）或钱包地址。
     - **金额**：数值类型。
3. 如果有任何字段缺失，系统会向用户询问缺失的信息。
4. 收集所有必要信息后，调用`{baseDir}/scripts/send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>`脚本进行转账。
5. 向用户显示转账成功或失败的消息。

**收款人类型识别：**
   - **Twitter用户名**：如果收款人名称以`@`开头，去掉`@`后使用`recipientTwitterUsername`。
     - 例如：`@aminedd4` → `recipientTwitterUsername: "aminedd4"`。
   - **钱包地址**：如果收款人地址以`0x`开头，使用`recipientWalletAddress`。
     - 例如：`0x1234...` → `recipientWalletAddress: "0x1234..."`。
   - **PayID名称**：否则，使用`recipientPayid`。
     - 例如：`aldo` → `recipientPayid: "aldo"`。

**关于USD的处理（非常重要）：**
   - 当用户输入“USD”、“dollar”或“$”时：
     - 将`tokenSymbol`设置为`USD_STABLECOIN`（这是一个特殊标记）。
     - 将`chainSymbol`设置为`null`——系统会自动选择拥有最高USD稳定币余额的链。
     - 不要询问用户链的信息，因为系统会自动处理。

**支持的代币（精确的枚举值）：**
   - `USDT` - Tether
   - `USDC` - USD Coin
   - `ETH` - Ethereum
   - `BNB` - Binance Coin
   - `POL` - Polygon
   - `USD_STABLECOIN` - 用于USD相关的请求（此时`chainSymbol`应设置为`null`）

**支持的链（精确的枚举值）：**
   - `ETH` - Ethereum
   - `POL` - Polygon
   - `OP` - Optimism
   - `BNB` - Binance Chain
   - `BASE` - Base
   - `null` - 仅当`tokenSymbol`为`USD_STABLECOIN`时使用

**解析示例：**
   - 示例1：`send 5 usdt on base to aldo`
   - 示例2：`transfer 0.3 BNB on bnb to @aminedd4`
   - 示例3：`send $10 to chris`
   - 示例4：`send 1 eth on ethereum to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

**后续问题示例：**
   - 用户：“send some usdt to aldo” → 缺少金额和链信息 → 询问：“您想发送多少USDT？使用哪个链（ETH、POL、OP、BNB或BASE）？”
   - 用户：“send 5 usdt to aldo” → 缺少链信息 → 询问：“您想使用哪个链（ETH、POL、OP、BNB或BASE）？”
   - 用户：“send 5 usdt on base” → 缺少收款人信息 → 询问：“您想把钱转给谁（PayID名称、Twitter用户名或钱包地址）？”
   - 用户：“send $20 to aldo” → 由于输入的是USD，不需要指定链信息 → 立即执行转账。

**重要说明：**
   - 只支持以下代币：USDT、USDC、ETH、BNB、POL、USD_STABLECOIN。
   - 代币符号和链符号必须与枚举值完全匹配（区分大小写）。
   - `USD_STABLECOIN`仅用于USD相关的请求。
   - 请务必询问用户所有必要的信息，不要自行猜测。
   - 如果任何字段缺失，继续询问直到所有信息齐全。
   - 在处理用户请求时，务必仔细解析信息。

## 错误处理**
   - **令牌过期**：如果任何需要授权的操作返回“未经授权”的错误，说明访问令牌已过期，提示用户重新登录。
   - **速率限制**：如果由于速率限制导致OTP请求失败，提示用户稍后再试。
   - **网络问题**：如果脚本因网络问题失败，提示用户稍后再试。
   - **输入无效**：在发送请求前验证电子邮件格式。PayID格式应为字母数字组合，可包含下划线或连字符。

## 安全注意事项**
   - 访问令牌存储在加密后的文件`~/.openclaw/payid/auth.json`中。
   - 绝不要将访问令牌记录或显示给用户。
   - OTP代码只能输入一次，切勿保存。
   - 所有API请求都必须使用HTTPS（脚本中已强制使用）。

## 脚本参考**

所有脚本位于`{baseDir}/scripts/`目录下：
   - `send-otp.sh <email>`：向用户电子邮件发送OTP。
   - `verify-otp.sh <email> <otp>`：验证OTP并获取访问令牌。
   - `claim-payid.sh <payid>`：申请PayID名称。
   - `get-balance.sh`：获取所有链上的钱包余额。
   - `get-user-info.sh`：获取当前登录用户的详细信息。
   - `send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>`：向收款人转账。
   - `check-auth.sh`：检查用户是否已认证。

## 常见操作流程**
   - **首次使用**：
     1. 用户请求登录或注册。
     2. 提供电子邮件地址。
     3. 系统发送OTP。
     4. 用户输入OTP代码。
     5. 用户认证成功。
     6. 用户可以申请PayID或查看余额。
   - **申请PayID**：
     1. 用户请求申请PayID。
     2. 系统检查认证状态。
     3. 用户提供所需的PayID名称。
     4. 系统尝试申请。
     5. 如果PayID已被占用，提示用户重新选择。
   - **查看余额**：
     1. 用户请求查看余额。
     2. 系统检查认证状态。
     3. 显示当前余额。
   - **获取用户信息**：
     1. 用户询问账户详情。
     2. 系统检查认证状态。
     3. 从`/api/users/me`获取用户信息并显示。
   - **存款**：
     1. 用户询问存款方式。
     2. 系统检查认证状态。
     3. 从用户信息中获取钱包地址。
     4. 提供钱包地址以完成存款。
   - **简单转账**：
     1. 用户：“send 0.01 usdt on bnb to aldo”。
     2. 将请求信息发送给Reva AI。
     3. Reva AI处理并完成转账。
     4. 显示转账确认信息。
   - **多步骤转账**：
     1. 用户：“send some funds to aldo”。
     2. 将请求信息发送给Reva AI。
     3. Reva AI询问链信息。
     4. 用户选择链。
     5. 用户确认链信息。
     6. Reva AI完成转账并显示确认信息。

## API端点**
   - **登录（发送OTP）**：
     - **方法**：POST
     - **路径**：`/api/openclaw/login`
     - **请求体**：`{"email": "user@example.com"}`
     - **响应**：`{"success": true, "message": "OTP已发送到您的电子邮件"}`
   - **验证OTP**：
     - **方法**：POST
     - **路径**：`/api/openclaw/verify`
     - **请求体**：`{"email": "user@example.com", "otp": "123456"}`
     - **响应**：`{"success": true, "token": "jwt_token", "user": {...}}`
   - **获取余额**：
     - **方法**：GET
     - **路径**：`/api/wallet?isForceUpdateWallet=true`
     - **请求头**：`openclaw-token: <token>`
     - **响应**：`{"success": true, "tokens": [{"name": "...", "symbol": "...", "balance": "...", "chain": "..."}]`
   - **申请PayID**：
     - **方法**：POST
     - **路径**：`/api/payid/register`
     - **请求头**：`openclaw-token: <token>`
     - **请求体**：`{"payIdName": "payid_name"}`
     - **响应**：`{"success": true, "data": {...}}`
   - **获取用户信息**：
     - **方法**：GET
     - **路径**：`/api/users/me`
     - **请求头**：`openclaw-token: <token>`
     - **响应**：`{"user": {"id": "...", "email": "...", "payId": "...", "walletAddress": "...", "referralCode": "...", "cashbackPoints": "...", "twitter": "...", ...}}`
   - **转账**：
     - **方法**：POST
     - **路径**：`/api/message/transfer-funds`
     - **请求头**：`openclaw-token: <token>`
     - **请求体**：

```json
{
  "tokenSymbol": "USDT" | "USDC" | "ETH" | "BNB" | "POL" | "USD_STABLECOIN",
  "chainSymbol": "ETH" | "POL" | "OP" | "BNB" | "BASE" | null,
  "recipientPayid": string | null,
  "recipientTwitterUsername": string | null,
  "recipientWalletAddress": string | null,
  "amount": number
}
```

**成功响应（200）：** `{"success": true, "data": {"message": "...", "recipientPayId": "...", "usdAmountToSend": ...}, "meta": {"message": "交易成功"}}`
**错误响应（400/500）：** `{"success": false, "error": {"code": "...", "message": "...", "details": [...]}}`

## 提示**
- 在执行任何需要授权的操作之前，务必检查用户是否已认证。
- 为了清晰起见，显示每个代币的余额及其所属链。
- 对于存款操作，只需提供用户从`/api/users/me`获取的钱包地址。
- **转账时请注意**：解析用户输入的信息，提取代币、链、收款人和金额等信息。
- 对于USD相关的请求，使用`USD_STABLECOIN`代币，并将`chainSymbol`设置为`null`——无需用户指定链。
- 只支持以下代币：USDT、USDC、ETH、BNB、POL、USD_STABLECOIN（区分大小写）。
- 当用户询问账户详情时，从`/api/users/me`获取相关信息。
- 根据API响应向用户显示清晰的错误信息。
- 逐步引导用户完成认证流程。
- 如果所需的PayID已被占用，建议用户选择其他选项。
- 显示API响应中的交易成功信息。
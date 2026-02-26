---
name: reva
description: Reva钱包的全面管理功能包括：无密码认证、PayID名称的声明与设置、跨多个区块链网络向PayID或钱包地址进行加密货币转账、跨网络追踪账户余额、查看账户详细信息，以及资金存取管理。
homepage: https://revapay.ai
user-invocable: true
dependencies:
  - jq
  - curl
---
# Reva

**Reva为用户提供无密码认证和钱包管理服务。**

Reva提供了一种简单的方式来验证用户身份、申请唯一的PayID名称以及管理加密货币余额。所有认证过程均采用基于电子邮件的OTP验证方式，无需输入密码。

## 认证

Reva采用无密码认证流程。用户会通过电子邮件收到一次性密码（OTP），验证完成后即可获得用于后续操作的访问令牌。

### 登录/注册流程

注册和登录的过程相同，都遵循以下步骤：

1. 用户提供他们的电子邮件地址。
2. 系统将OTP发送到用户的电子邮件。
3. 用户输入收到的OTP代码。
4. 系统验证OTP并返回访问令牌。
5. 访问令牌会被安全存储，以便后续使用。

**请注意：**访问令牌在验证后必须妥善保管，并用于所有需要授权的操作。

## 可用的命令

### 1. 登录或注册

**触发条件：**用户希望登录、注册、登录或访问Reva服务。

**处理流程：**
1. 如果用户尚未提供电子邮件地址，系统会要求他们提供。
2. 调用`{baseDir}/scripts/send-otp.sh <email>`脚本发送OTP。
3. 通知用户OTP已发送到他们的电子邮件。
4. 要求用户输入收到的OTP代码。
5. 调用`{baseDir}/scripts/verify-otp.sh <email> <otp>`脚本验证OTP。
6. 验证成功后，通知用户认证成功。
7. 访问令牌会自动保存，供将来使用。

### 2. 申请PayID

**触发条件：**用户希望申请一个PayID、获取PayID名称或设置自己的PayID。

**要求：**用户必须先完成认证（拥有有效的访问令牌）。

**处理流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 如果用户尚未提供所需的PayID名称，系统会要求他们提供。
4. 调用`{baseDir}/scripts/claim-payid.sh <desired_payid>`脚本处理申请。
5. 根据处理结果：
   - 如果申请成功，通知用户PayID已成功申请。
   - 如果该PayID已被占用，系统会提示用户选择其他PayID。
   - 如果格式不正确，系统会解释格式要求并再次请求用户输入。
   - 如果用户未授权（例如令牌过期），系统会提示用户重新登录。

### 3. 查看余额

**触发条件：**用户希望查看余额、钱包中的资金或了解自己拥有的资金总额。

**要求：**用户必须先完成认证（拥有有效的访问令牌）。

**处理流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 调用`{baseDir}/scripts/get-balance.sh`脚本获取用户的余额信息。
4. 以友好的格式显示每个代币的金额、符号和所属链（网络）。
5. 如果出现未授权或令牌过期的错误，系统会提示用户重新登录。

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

**触发条件：**用户询问自己的账户详情、PayID、钱包地址、推荐码、返现积分、关联的Twitter账号、头像或希望存款。

**要求：**用户必须先完成认证（拥有有效的访问令牌）。

**处理流程：**
1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户先登录。
3. 调用`{baseDir}/scripts/get-user-info.sh`脚本获取用户信息。
4. 显示用户请求的相关信息：
   - **PayID**：从`payId`字段获取。
   - **钱包地址**：从`walletAddress`字段获取。
   - **电子邮件**：从`email`字段获取。
   - **推荐码**：从`referralCode`字段获取。
   - **返现积分**：从`cashbackPoints`字段获取。
   - **关联的Twitter账号**：从`twitter`字段获取。
   - **头像**：从`avatarUrl`字段获取。
   - **交易限额**：从`transactionLimit`和`transactionUsed`字段获取。
5. 如果用户希望存款，系统会提示他们提供钱包地址，并指导他们将资金发送到该地址。

**关于存款的重要说明：**当用户请求存款时，只需使用`/api/users/me`接口返回的用户钱包地址即可。

### 5. 发送资金

**触发条件：**用户希望发送资金、转移代币或向他人付款。

**要求：**用户必须先完成认证（拥有有效的访问令牌）。

**关键注意事项：**  
- 必须解析用户的消息内容，提取所有必要的信息以构建正确的转账数据。在所有必要字段都提供之前，持续询问用户相关信息。

1. 调用`{baseDir}/scripts/check-auth.sh`脚本检查用户是否已认证。
2. 如果未认证，系统会提示用户重新登录。
3. 从用户消息中提取以下信息：
   - **代币符号**：支持USDT、USDC、ETH、BNB、POL或USD_STABLECOIN。
   - **链符号**：支持ETH、POL、OP、BNB或BASE（USD_STABLECOIN使用`null`）。
   - **收款人**：PayID名称、Twitter用户名（以@开头）或钱包地址。
   - **金额**：数值类型。
4. 如果有任何字段缺失，系统会继续询问用户以获取缺失的信息。
5. 收集所有必要信息后，调用`{baseDir}/scripts/send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>`脚本完成转账。
6. 向用户显示转账成功或失败的消息。

**收款人类型识别规则：**
- **Twitter用户名**：如果收款人名称以`@`开头，去掉`@`后使用`recipientTwitterUsername`。
  - 例如：`@aminedd4` → `recipientTwitterUsername: "aminedd4"`。
- **钱包地址**：如果收款人地址以`0x`开头，使用`recipientWalletAddress`。
  - 例如：`0x1234...` → `recipientWalletAddress: "0x1234..."`。
- **PayID名称**：其他情况使用`recipientPayid`。
  - 例如：`aldo` → `recipientPayid: "aldo"`。

**关于USD的处理（非常重要）：**
- 当用户输入“USD”、“dollar”或“dollars”时：
  - 将`tokenSymbol`设置为`USD_STABLECOIN`（这是一个特殊标记）。
  - 将`chainSymbol`设置为`null`——系统会自动选择用户拥有最多USD稳定币余额的链。
- 在用户输入“USD”或“dollars”时，无需询问链信息，系统会自动处理。

**支持的代币（精确枚举）：**
- `USDT`：Tether
- `USDC`：USD Coin
- `ETH`：Ethereum
- `BNB`：Binance Coin
- `POL`：Polygon
- `USD_STABLECOIN`：用于USD相关请求（此时`chainSymbol`必须设置为`null`。

**支持的链（精确枚举）：**
- `ETH`：Ethereum
- `POL`：Polygon
- `OP`：Optimism
- `BNB`：BNB Chain
- `BASE`：Base
- `null`：仅当`tokenSymbol`为`USD_STABLECOIN`时使用。

**解析示例：**
- 示例1：`send 5 usdt on base to aldo`
- 示例2：`transfer 0.3 BNB on bnb to @aminedd4`
- 示例3：`send $10 to chris`
- 示例4：`send 1 eth on ethereum to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

**后续问题示例：**
- 用户：“send some usdt to aldo” → 缺少金额和链信息 → 询问：“您想发送多少USDT？使用哪个链（ETH、POL、OP、BNB或BASE）？”
- 用户：“send 5 usdt to aldo” → 缺少链信息 → 询问：“您想使用哪个链（ETH、POL、OP、BNB或BASE）？”
- 用户：“send 5 usdt on base” → 缺少收款人信息 → 询问：“您想将资金发送给谁（PayID名称、Twitter用户名或钱包地址）？”
- 用户：“send $20 to aldo” → 由于输入的是USD，不需要提供链信息 → 立即执行转账。

**重要说明：**
- 只支持以下代币：USDT、USDC、ETH、BNB、POL、USD_STABLECOIN。
- 代币符号和链符号必须与枚举值完全匹配（区分大小写）。
- `USD_STABLECOIN`仅用于USD相关请求。
- 在所有必要字段都提供之前，持续询问用户相关信息。
- 不要自行猜测用户的输入信息，务必要求用户提供缺失的信息。

## 错误处理**
- **令牌过期**：如果任何需要授权的操作返回“未经授权”的错误，说明访问令牌已过期，提示用户重新登录。
- **速率限制**：如果由于速率限制导致OTP请求失败，提示用户稍后再试。
- **网络问题**：如果脚本因网络问题失败，提示用户稍后再试。
- **无效输入**：在发送请求前验证电子邮件格式。PayID格式应为字母数字组合，允许使用下划线或连字符。

## 安全注意事项**
- **用户认证与控制**：所有操作均需要用户完成无密码OTP验证。
- **转账操作**：所有转账操作都需要用户明确提供代币符号、链、收款人和金额信息。
- 该工具无法自主发起转账，只有在用户提供所有必要参数后才会执行转账。
- 用户始终对自己的钱包操作拥有完全控制权。
- **令牌存储**：访问令牌存储在`~/.openclaw/payid/auth.json`文件中，文件权限设置为`chmod 600`（仅限用户访问）。
- 这是一种标准的OAuth/JWT令牌存储方式，用于会话持久化。
- 用户可以随时通过删除`auth.json`文件或使用工具的登出功能来清除令牌。
- 令牌过期后需要重新认证。
- **数据安全**：不会向用户显示访问令牌；OTP代码仅使用一次且不会被存储。
- 所有API请求均使用HTTPS加密（在脚本中强制执行）。
- 所有JSON数据均使用`jq`构建，以防止注入攻击。
- 该工具仅与官方Reva API（https://api.revapay.ai）进行通信。
- 该工具与Reva（https://revapay.ai）集成，这是一个合法的加密货币钱包服务。
- 所有转账操作均通过用户认证后的API调用完成，而非自动执行。

## 脚本参考**

所有脚本位于`{baseDir}/scripts/`目录下：
- `send-otp.sh <email>`：向用户电子邮件发送OTP。
- `verify-otp.sh <email> <otp>`：验证OTP并获取访问令牌。
- `claim-payid.sh <payid>`：申请PayID名称。
- `get-balance.sh`：获取用户所有链上的钱包余额。
- `get-user-info.sh`：获取当前登录用户的详细信息。
- `send-funds.sh <tokenSymbol> <chainSymbol> <recipient> <amount>`：向收款人转账。
- `check-auth.sh`：检查用户是否已认证。

## 常见工作流程**
- **首次使用**：
  1. 用户请求登录或注册。
  2. 用户提供电子邮件地址。
  3. 系统发送OTP。
  4. 用户输入OTP代码。
  5. 用户认证成功。
  6. 用户可以申请PayID或查看余额。
- **申请PayID**：
  1. 用户请求申请PayID。
  2. 系统检查认证状态。
  3. 用户提供所需的PayID名称。
  4. 系统尝试申请；如果该PayID已被占用，会提示用户选择其他PayID。
- **查看余额**：
  1. 用户请求查看余额。
  2. 系统检查认证状态。
  3. 显示当前余额。
- **获取用户信息**：
  1. 用户询问自己的PayID、钱包地址等信息。
  2. 系统检查认证状态。
  3. 从`/api/users/me`接口获取用户信息并显示。
- **存款**：
  1. 用户询问存款方式。
  2. 系统检查认证状态。
  3. 从用户信息中获取钱包地址。
  4. 提供钱包地址以完成存款。
- **发送资金（简单操作）**：
  1. 用户：“send 0.01 usdt on bnb to aldo”。
  2. 将请求转发给Reva AI。
  3. Reva AI处理并完成转账。
  4. 向用户显示转账确认信息。
- **发送资金（多步骤操作）**：
  1. 用户：“send some funds to aldo”。
  2. 将请求转发给Reva AI。
  3. Reva AI询问：“使用哪个链？”
  4. 用户：“bnb”。
  5. 用户再次确认链信息。
  6. Reva AI询问：“使用哪种代币？”
  7. 用户：“0.01 usdt”。
  8. Reva AI完成转账并显示确认信息。

## API接口**
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

- **成功响应（200）**：`{"success": true, "data": {"message": "...", "recipientPayId": "...", "usdAmountToSend": ...}, "meta": {"message": "转账成功"}}`
- **错误响应（400/500）**：`{"success": false, "error": {"code": "...", "message": "...", "details": [...]}`

## 提示**
- 在执行任何需要授权的操作之前，务必检查用户是否已认证。
- 为便于查看，需显示每个代币的余额及其所属链。
- 对于存款操作，只需提供用户通过`/api/users/me`获取的钱包地址。
- **发送资金时**：解析用户消息以提取代币符号、链、收款人和金额；如有缺失信息，请继续询问用户。
- 对于USD相关请求，使用`USD_STABLECOIN`代币，并将`chainSymbol`设置为`null`；无需询问链信息。
- 只支持以下代币：USDT、USDC、ETH、BNB、POL、USD_STABLECOIN（区分大小写）。
- 当用户询问账户详情时，从`/api/users/me`接口获取相关信息。
- 根据API响应向用户显示清晰的错误信息。
- 逐步指导用户完成认证流程。
- 如果所需的PayID已被占用，建议用户选择其他PayID。
- 根据API响应向用户显示转账成功信息。
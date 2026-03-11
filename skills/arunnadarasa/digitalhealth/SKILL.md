---
name: clawhub-x402-payments
description: 通过 PayAI（EIP-3009）实现 USDC 的 x402 支付，以及通过 EVVM 的原生功能实现 DHM 的 x402 支付（采用签名支付方式）。适用于添加 x402 支付流程、集成 PayAI Echo、使用 EVVM 的 pay() 功能进行 DHM 支付、通过 Privy 进行代理间支付，或者在 ClawHub/NHS EVVM 应用中用户询问如何进行 USDC/DHM 的 x402 支付时使用。
---
# ClawHub x402支付（通过PayAI使用USDC + 通过EVVM使用DHM）

本文档介绍了NHS EVVM / ClawHub应用程序中的两种x402支付流程：**通过PayAI Echo使用USDC**和**通过EVVM原生方式使用DHM**。相关实现代码位于该仓库中。

## 参考路径

| 流程 | 客户端UI | 服务器/配置 |
|------|-----------|------------------|
| USDC（PayAI） | `frontend/src/components/sections/USDCX402TestSection.tsx` | 配置：`frontend/src/config/contracts.ts`（`X402_USDC_ECHO_URL`, `USDC_BASE_SEPOLIA`） |
| DHM（EVVM） | `frontend/src/components/sections/X402TestSection.tsx` | `server/src/index.ts`（GET 402, POST /payments/evvm/dhm`） |
| EVVM签名 | `frontend/src/lib/evvmSign.ts` | — |

链：**Base Sepolia**（chainId 84532）。

---

## 流程1：通过PayAI Echo使用USDC进行x402支付

PayAI会返回一个状态码为402的响应，并附带一个`accepts`数组（而非`options`）。客户端从`accepts`数组中选择一个USDC支付选项，构建EIP-3009格式的`TransferWithAuthorization`交易请求，然后使用EIP-712协议进行签名，并将签名信息放在`PAYMENT-SIGNATURE`头部中，之后重新发送请求；服务器会返回200状态码，并可能设置`PAYMENT-RESPONSE`头部以包含交易结果（例如交易哈希值）。

### 客户端步骤

1. **请求资源**  
   发送`GET`请求到`<Echo URL>`（例如：`https://x402.payai.network/api/base-sepolia/paid-content`）。

2. **解析响应**  
   - 优先检查`PAYMENT-REQUIRED`响应头部（包含Base64编码的JSON数据）。  
   - 如果响应体是JSON格式，其中包含`accepts`数组，则使用该数组。  
   - 响应数据格式如下：`{ x402Version?, error?, resource?, accepts: Array<{ scheme, network, amount, asset, payTo, maxTimeoutSeconds?, extra? }> }`。

3. **选择USDC支付选项**  
   - 从`accepts`数组中选择`asset`字段值为“USDC”或`extra.name`为“USDC”的选项。  
   - 使用`amount`、`asset`、`payTo`、`extra.name`或`extra.version`参数来构建EIP-712交易请求。

4. **构建EIP-3009授权信息**  
   - 参数包括：`name`（默认为`extra?.name ?? "USDC"`）、`version`（默认为`extra?.version ?? "2"`）、`chainId`（84532）、`verifyingContract`（设置为`asset`）。  
   - 交易请求类型为`TransferWithAuthorization`，包含`from`、`to`、`value`、`validAfter`（例如当前时间加上300秒）、`nonce`（32个随机字节，以十六进制表示）等字段。  
   - 使用`signTypedData`函数对交易请求进行签名（使用EIP-712协议）。

5. **发送支付请求并重试**  
   - 构建请求负载：`{ x402Version: 2, scheme, network, accepts: { scheme, network, amount, asset, payTo, maxTimeoutSeconds, extra? }, payload: { signature, authorization: message }, extensions: {} }`。  
   - 将签名信息（`PAYMENT-SIGNATURE`）设置为`base64(JSON.stringify(payload)`。  
   - 重新发送`GET`请求，并在请求头部添加`PAYMENT-SIGNATURE`字段（值为Base64编码的签名字符串）。

6. **读取结果**  
   - 如果服务器返回200状态码，响应体中包含资源信息；`PAYMENT-RESPONSE`或`X-PAYMENT-RESPONSE`头部（如果存在）可能包含交易哈希值（`transaction`）等其他信息。

### 配置参数

- `VITE_X402_USDC_ECHO_URL`：PayAI Echo的API地址（默认为`https://x402.payai.network/api/base-sepolia/paid-content`）。  
- Base Sepolia链上的USDC资产地址：`0x036CbD53842c5426634e7929541eC2318f3dCF7e`。

---

## 流程2：通过EVVM原生方式使用DHM进行x402支付

服务器会返回状态码为402的响应，并在响应体中包含`PAYMENT-REQUIRED: 1`以及一个JSON对象，其中包含支付选项（如`to`、`suggestedNonce`等参数）。客户端使用`personal_sign`函数对支付信息进行签名，然后发送POST请求到服务器的支付接口；服务器会在EVVM Core上执行支付操作，并返回资源内容和交易哈希值。

### 服务器端（处理402响应和支付请求的接口）

1. **处理未支付的请求**  
   如果资源未支付，服务器会返回状态码402，并在响应体中包含以下信息：  
   - `resource`、`description`、`to`（接收者地址）、`suggestedNonce`  
   - `options`数组，其中至少包含一个选项：`id`、`type: "evvm_pay"`、`chainId`、`evvmId`、`coreAddress`、`token`（DHM相关参数）、`to`、`suggestedNonce`、`amount`、`priorityFee`、`executor`（可选）、`isAsyncExec`。

2. **执行支付操作**  
   发送`POST`请求到`/payments/evvm/dhm`接口，请求参数包括：`from`、`to`、`toIdentity`、`token`、`amount`、`priorityFee`、`executor`、`nonce`、`isAsyncExec`、`signature`。  
   服务器会使用`pay()`函数在EVVM Core上执行支付操作，并返回结果（`status`、`txHash`、`content`）。

### 客户端步骤

1. **请求资源**  
   发送`GET`请求到`<X402_SERVER_URL>/clinical/mri-slot`。

2. **检查响应状态**  
   如果响应状态码为402或`PAYMENT-REQUIRED`头部值为“1”，则解析响应体中的JSON数据：`{ resource, description?, to, suggestedNonce?, options }`。

3. **选择支付选项**  
   从`options`数组中选择类型为“evvm_pay”或`id`为“dhm-evvm”的选项。确保`to`和`suggestedNonce`字段存在。

4. **构建EVVM支付请求**  
   使用`keccak256`函数对以下参数进行哈希处理：  
   `encodeAbiParameters("string, address, string, address, uint256, uint256", ["pay", to, toIdentity, token, amount, priorityFee"]`，以生成用于EVVM Core的支付请求数据。  
   构建支付消息字符串：`evvmId, coreAddress, hashPayload, executor, nonce, isAsyncExec`（各字段用逗号分隔）。  
   使用`frontend/src/lib/evvmSign.ts`中的`buildEvvmPayMessageCoreDoc`函数来构建完整的支付消息。

5. **签名并发送请求**  
   对支付消息字符串使用`personal_sign`函数进行签名。  
   发送`POST`请求到`<X402_SERVER_URL>/payments/evvm/dhm`接口，请求参数包括：`from`、`to`、`toIdentity`、`token`、`amount`、`priorityFee`、`executor`、`nonce`、`isAsyncExec`、`signature`。  
   如果请求成功，服务器会返回资源内容（`content`）和交易哈希值（`txHash`）。

### 配置参数

- `VITE_X402_SERVER_URL`：DHM x402支付服务的API地址（例如：`https://evvm-x402-dhm.fly.dev`或`localhost`）。  
- 服务器环境变量：`EXECUTOR_PRIVATE_KEY`、`RPC_URL`、`RECIPIENT_ADDRESS`、`EVVM_ID`、`EVVM_CORE_ADDRESS`、`DHM_TOKEN_ADDRESS`（详见`server/.env.example`文件）。

---

## 添加或调试时的检查事项

**USDC（通过PayAI支付）：**
- 确保从响应头部或响应体中解析出402状态码；使用`accepts`数组中的支付选项，而非`options`字段。  
- 确保EIP-712交易请求的域名和`TransferWithAuthorization`参数与Base Sepolia上的USDC合约匹配（`extra`字段中的`name`或`version`值为“USDC”或“2”）。  
- 确保`PAYMENT-SIGNATURE`字段为Base64编码的JSON数据；使用相同的URL和`PAYMENT-SIGNATURE`头部重新发送请求。  
- 如果存在`PAYMENT-RESPONSE`头部，确保其中包含交易哈希值（`transaction`）等信息。

**DHM（通过EVVM支付）：**
- 确保响应体中包含`options`数组的`to`和`suggestedNonce`字段；客户端在签名消息中使用这些信息。  
- 确保使用`hashDataForPayCore`和`buildEvvmMessageV3`函数来构建支付请求。  
- 确保发送的POST请求参数符合服务器的期望格式（`from`、`to`、`token`、`amount`、`nonce`、`executor`、`isAsyncExec`、`signature`）。  
- 确保服务器具有`EXECUTOR_PRIVATE_KEY`以及用于调用`pay()`函数的RPC接口。

---

## 快速复制代码示例

**PayAI 402支付请求示例：**
```ts
type PaymentRequirement = {
  scheme: string;
  network: string;
  amount: string;
  asset: string;
  payTo: string;
  maxTimeoutSeconds?: number;
  extra?: { name?: string; version?: string; [k: string]: unknown };
};
// 402 body: { x402Version?, error?, resource?, accepts: PaymentRequirement[] }
```

**EVVM 402支付请求示例：**
```ts
type PaymentOption = {
  id: string;
  type: string;
  chainId: number;
  evvmId: string;
  coreAddress: string;
  token: string;
  to?: string;
  suggestedNonce?: string;
  amount: string;
  priorityFee: string;
  executor: string | null;
  isAsyncExec: boolean;
};
// 402 body: { resource, description?, to?, suggestedNonce?, options: PaymentOption[] }
```

完整代码请参见文档顶部的参考路径。

---

## 演习任务（适用于黑客马拉松）：使用Privy实现代理间支付

上述流程目前依赖于**浏览器钱包**（需要用户手动操作）。参与者可以扩展应用程序，使**代理**能够使用**Privy Agentic Wallets**技能实现自动支付功能。

### 利用Privy技能

- **相关技能**：[privy-io/privy-agentic-wallets-skill](https://github.com/privy-io/privy-agentic-wallets-skill)——该技能允许AI代理通过Privy API控制服务器钱包，实现无需用户点击即可完成交易签名和发送操作。  
- **在项目中安装Privy技能**：  
  `git clone https://github.com/privy-io/privy-agentic-wallets-skill.git .cursor/skills/privy`  
  （对于OpenClaw环境，需将代码克隆到`~/.openclaw/workspace/skills/privy`目录中）。同时需要配置`PRIVY_APP_ID`和`PRIVY_APP_SECRET`（从[dashboard.privy.io](https://dashboard.privy.io)获取）。  

### 演习任务

1. **相同的协议，不同的签名方式**  
   保持x402支付协议的流程不变（请求资源、构建请求负载、签名、发送请求）。唯一的变化在于签名方式：浏览器中的代理使用`signMessageAsync`或`signTypedDataAsync`函数进行签名，而代理则通过Privy API使用Privy服务器钱包进行签名。

2. **DHM代理支付功能**  
   - 在Base Sepolia上创建一个Privy服务器钱包（使用Privy技能），并设置相应的策略（例如限制支付金额或仅支持EVVM Core和指定的x402服务器）。  
   - 实现代理的支付逻辑：从`/clinical/mri-slot`接口获取支付请求信息，构建EVVM支付请求，然后通过Privy API进行签名，并将签名后的请求发送到`/payments/evvm/dhm`接口。  
   - 将此功能作为后端接口或脚本提供给代理使用，以便在没有浏览器钱包的情况下也能完成支付操作。

3. **USDC代理支付功能（可选）**  
   - 类似于PayAI支付流程：从`/clinical/mri-slot`接口获取支付请求信息，选择USDC支付选项，构建EIP-3009交易请求，然后通过Privy API进行签名，并发送请求。  
   - 可以根据需要设置Privy服务器钱包的策略（例如仅允许使用PayAI或USDC支付方式）。

4. **双模式支持**  
   - 在用户界面或API中提供“以本人身份支付”（使用当前钱包）和“以代理身份支付”两种选项。两者共享资源解析和请求负载构建逻辑，仅签名方式不同（分别使用浏览器或Privy服务器）。

### 为什么这个技能适合本次挑战

- **协议**（x402、EVVM支付、EIP-3009）保持不变；上述文档提供了请求负载和接口的统一规范。  
- Privy技能提供了获取代理专属钱包以及如何使用该钱包进行签名的方法。结合这两个技能，参与者可以轻松实现代理自动支付的功能。
---
name: tator-trader
description: "**使用 Tator 的 AI 交易 API 通过自然语言执行加密交易**  
适用场景：购买代币、出售代币、进行代币交换、跨链桥接、发送代币、封装/解封 ETH、建立多头/空头头寸、在预测市场中下注、发行代币、注册区块链名称或管理收益头寸。  
**可执行的操作：**  
- **购买代币**  
- **出售代币**  
- **交换 X 为 Y**  
- **跨链桥接**  
- **发送代币**  
- **建立多头头寸**  
- **建立空头头寸**  
- **在预测市场中下注**  
- **发行代币**  
- **注册区块链名称**  
- **存入收益**  
- **封装 ETH**  
**系统特性：**  
- 支持 24 条区块链。  
- 返回的交易为未签名（UNSIGNED）格式，您需要自行签名并广播这些交易。  
- 每次请求的费用为 0.20 美元（USD），通过 x402 账户支付。  
**推荐的钱包集成方式：**  
- Sponge（SPONGE_API_KEY）  
- AgentWallet（AGENTWALLET_API_TOKEN）  
- 无需使用原始私钥。  
**注意事项：**  
- 该功能仅用于构建交易指令，不会访问您的私钥或代币。"
---
# Tator AI Trading API

使用自然语言在24个区块链上进行交易。例如，您可以发送如下指令：“在Base链上购买价值0.1 ETH的PEPE币”——Tator会返回未签名的交易记录供您审核、签名并广播。每次请求的费用为0.20美元（通过x402支付）。Tator绝不会接触您的私钥。

## 快速参考

| 情况 | 操作 |
|-----------|--------|
| 用户想要买入/卖出/交换代币 | 构建包含代币数量、链名和交易类型的指令，然后调用Tator |
| 用户想要跨链转移代币 | 在指令中指定源链、目标链和数量 |
| 用户想要开设杠杆交易 | 在指令中指定杠杆倍数、交易方向、抵押品数量和使用的协议 |
| 用户的指令过于模糊（如“购买一些加密货币”） | 要求用户提供更多详细信息：具体是哪种代币、数量以及交易链 |
| 回应类型为“transaction” | **逐一验证每笔交易**（检查`to`、`value`和`chainId`字段），然后依次签名并广播 |
| 回应类型为“error” | 向用户显示错误信息，并提供解决方案 |
| 回应类型为“info” | 向用户展示相关信息 |
| 返回多笔交易 | 按顺序执行交易——每笔交易确认完成后再发送下一笔 |
| 未知或新出现的代币 | 在指令中使用代币的合约地址而非名称 |

## 端点

```json
POST https://x402.quickintel.io/v1/tator/prompt
{
  "prompt": "在Base链上购买价值0.1 ETH的PEPE币",
  "walletAddress": "0xYourPublicWalletAddress",
  "provider": "your-agent-name"
}
```

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `prompt` | 是 | 用于指定交易指令的自然语言文本 |
| `walletAddress` | 是 | 您的公共钱包地址（用于接收代币和签名交易） |
| `provider` | 是 | 指定您的代理/应用程序标识符 |
| `async` | 否 | 是否异步执行（默认值为`false`） |
| `chain` | 否 | 优先使用的链名（例如“base”或“ethereum”） |
| `slippage` | 否 | 容许的滑点百分比（默认值为1%） |

**费用：** 在任何支付网络上，每次请求的费用为0.20美元（相当于200000个原子单位）。建议使用Base链以获得最低费用。

> **⚠️ 严禁在指令中输入私钥或助记词。** Tator仅需要您的公共钱包地址。

## 如何编写有效的交易指令

有效的指令能提高交易成功率。无论交易结果如何，您都需要支付0.20美元的费用。

| 示例指令 | 不建议的指令 |
|----------------|-------------------|
| "在Base链上购买价值0.1 ETH的PEPE币" | "购买一些加密货币" |
| "在Arbitrum链上用100 USDC交换ETH" | "交换代币" |
| "将50 USDC从Base链转移到Arbitrum链" | "转移我的代币" |
| "在Avantis链上用100 USDC开设5倍杠杆的ETH多头仓位" | "开设ETH多头仓位" |
| "在Base链上购买0x1234...abcd（代币名称）" | "帮我购买那个新推出的加密货币" |

**提示：**
- 请务必指定交易链名。
- 明确交易金额。
- 对于不常见的代币，请使用其合约地址。
- 在进行跨链转移时，需提供源链和目标链的信息。

## 功能概述

| 功能类别 | 可执行的操作 | 示例 |
|---------|------------|-------------------|
| **交易** | 买入、卖出、交换 | "在Arbitrum链上用100 USDC交换ETH" |
| **转账** | 发送、包装、解包、销毁代币 | "将50 USDC发送到0x1234..." |
| **跨链转移** | 通过Relay、LiFi、GasZip等工具进行跨链转移 | "将100 USDC从Base链转移到Arbitrum链" |
| **杠杆交易** | 在Avantis链上进行杠杆交易 | "在Avantis链上用100 USDC开设5倍杠杆的ETH多头仓位" |
| **预测市场** | 通过Myriad平台进行投注 | "投注10美元，预测‘ETH价格是否会达到5000美元？’" |
| **代币发布** | 在Clanker、Ethereum、Arbitrum、Unichain等平台上发布代币 | "在Clanker平台上发布代币MTK" |
| **账户命名** | 为账户创建别名 | "为我的账户创建别名‘myname.base’" |
| **收益管理** | 在Aave等平台上管理收益 | "在Base链上向Aave平台存入1000 USDC" |

## 支持的区块链（共24个）

Ethereum、Base、Arbitrum、Optimism、Polygon、Avalanche、BSC、Linea、Sonic、Berachain、Abstract、Unichain、Ink、Soneium、Ronin、Worldchain、Sei、HyperEVM、Katana、Somnia、Plasma、Monad、MegaETH、Solana

请使用准确的链名（例如，使用“base”而非“Base”）。

## 处理响应

### 交易响应（最常见情况）

```json
{
  "type": "transaction",
  "transactions": [
    {
      "to": "0xContractAddress",
      "data": "0xCalldata...",
      "value": "100000000000000000",
      "chainId": 8453,
      "description": "在Base链上使用0.1 ETH购买了PEPE币"
    },
  ],
  "message": "交易已完成。请签名并广播以完成交易。"
}
```

**在签名每笔交易之前，请务必验证：**
1. `to`地址：必须是已知的去中心化交易所（DEX）路由器、跨链桥接合约或您指定的地址。
2. `value`字段：应与您的交易指令中的金额相匹配（对于ERC-20代币交换，通常值为`0`）。
3. `chainId`字段：应与您请求的链名相匹配。
4. `description`字段：应与您的交易指令内容一致。
5. 对于需要用户确认的交易（例如使用`0x095ea7b3`协议的交易），请确保交易发起方是可信的合约。

如果发现任何异常，请**不要签名**，请重新发送更详细的指令或通过区块链浏览器验证相关合约。

### 错误响应

```json
{
  "type": "error",
  "message": "余额不足。您有0.05 ETH，但需要0.1 ETH。",
  "code": "INSUFFICIENT_BALANCE"
}
```

| 错误代码 | 解决方案 |
|---------|-------------------|
| `INSUFFICIENT_BALANCE` | 交易前请检查您的代币余额 |
| `UNSUPPORTEDCHAIN` | 请使用支持的链名 |
| `TOKEN_NOT_FOUND` | 请使用代币的合约地址而非名称 |
| `INVALID_PROMPT` | 请提供更具体的交易指令 |
| `SLIPPAGE_TOO_HIGH` | 降低交易金额或增加滑点容忍度 |

### 信息响应

当用户查询相关信息（如价格、余额等）时，系统会返回相应的信息。请将响应内容展示给用户。

## 钱包集成

> **⚠️ 钱包安全提示：** Tator不需要您的私钥。x402支付功能会使用您指定的代理钱包。请使用**托管钱包服务**以避免私钥被泄露。

| 使用方式 | 是否涉及私钥暴露 | 备注 |
|---------|------------------|-------------------|
| 使用Sponge Wallet | **推荐方案A** | ✅ 不会泄露私钥 |
| 使用AgentWallet（frames.ag） | **方案B** | ✅ 不会泄露私钥 |
| 使用Lobster.cash/Crossmint | 详见`references/REFERENCE.md` | ✅ 不会泄露私钥 |
| 使用Vincent Wallet | 详见`references/REFERENCE.md` | ✅ 不会泄露私钥 |
| 需要编程方式签名（如viem、ethers、@x402/fetch、Solana） | 详见`references/REFERENCE.md` | ⚠️ 需要额外的安全措施 |

### 方案A：Sponge Wallet（推荐方案，不会泄露私钥）

```bash
curl -sS -X POST "https://api.wallet.paysponge.com/api/x402/fetch"
  -H "Authorization: Bearer $SPONGE_API_KEY"
  -H "Content-Type: application/json"
  -d '
    {
      "url": "https://x402.quickintel.io/v1/tator/prompt",
      "method": "POST",
      "body": {
        "prompt": "在Base链上购买价值0.1 ETH的PEPE币",
        "walletAddress": "0xYourSpongeWalletAddress",
        "provider": "sponge-agent"
      },
      "preferred_chain": "base"
    }
  '
```

Sponge会自动处理支付流程。您仍需自行验证并签名返回的交易记录。使用此方案需要`SPONGE_API_KEY`环境变量。

### 方案B：AgentWallet（不会泄露私钥）

```javascript
const response = await fetch('https://frames.ag/api/wallets/{username}/actions/x402/fetch',
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.AGENTWALLET_API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://x402.quickintel.io/v1/tator/prompt',
    method: 'POST',
    body: {
      prompt: "在Base链上用100 USDC交换ETH",
      walletAddress: agentWalletAddress,
      provider: 'my-agent'
    }
  });
const result = await response.json();

// 根据结果执行签名和广播操作
if (result.type === 'transaction') {
  for (const tx of result.transactions) {
    // 验证交易信息后签名并广播
    const broadcast = await fetch(
      'https://frames.ag/api/wallets/{username}/actions/send-transaction',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.AGENTWALLET_API_TOKEN}`,
          'Content-Type': 'application/json',
          body: {
            chainId: tx.chainId,
            to: tx.to,
            data: tx.data,
            value: tx.value
          }
        }
      }
    );
    console.log(`交易已发送：${await broadcast.json().hash}`);
  }
}
```

> 关于编程签名方式（如`@x402/fetch`、`ethers.js`、Solana等），请参阅`references/REFERENCE.md`。这些方法需要使用专门的托管钱包，并确保钱包中有一定金额的代币。

## 异步模式

对于需要长时间运行的操作，可以在请求中添加`"async": true`参数：

```json
{
  "type": "pending",
  "jobId": "job_abc123",
  "message": "请等待操作结果。"
}
```

**查询操作结果（免费）：** `GET https://x402.quickintel.io/v1/tator/jobs/job_abc123`

## 交易前请先扫描代币

**在交易前，请务必扫描未知的代币。** 使用`quickintel-scan`服务（费用为0.03美元）来检查代币是否存在风险（如钓鱼攻击或欺诈行为）：

```javascript
// 扫描代币
const scan = await scanToken(chain, tokenAddress);
if (scan.tokenDynamicDetails.is_Honeypot) throw new Error('该代币可能是钓鱼攻击的目标');
if (scan.quickiAudit.has_Scams) throw new Error('该代币可能存在欺诈风险');

// 完成扫描后进行交易
const trade = await callTator(`在${chain}链上购买价值0.1 ETH的${tokenAddress}币`);
```

**总费用：** 扫描和交易的总费用为0.23美元。详细示例请参阅`references/REFERENCE.md`。

## 安全机制

| 您的角色 | Tator的角色 |
|---------|---------|
| 私钥管理 | Tator不会接收您的私钥 |
| 交易处理 | Tator会解析您的交易指令并构建未签名的交易数据 |
| 签名确认 | 由您负责交易签名 |
| 交易广播 | 交易完成后，Tator会通过x402平台收取0.20美元的费用 |

**重要说明：**
- **无论交易结果如何，系统都会收取费用。** 请使用`payment-identifier`参数进行安全重试。
- **涉及多笔交易时，必须按顺序执行。** 每笔交易都需要确认后才能进行下一笔交易。
- **跨链转移可能需要一定时间（30秒至30分钟）。**
- **杠杆交易存在风险**：使用杠杆可能导致抵押品损失。
- **扫描结果仅供参考**：对于持有的代币，建议定期重新扫描。

## 相关信息

- 可查询已完成的交易和使用的交易协议：`GET https://x402.quickintel.io/accepted`

## 其他参考资料

- **代币安全扫描**：使用`quickintel-scan`服务（费用0.03美元） |
- **x402平台的详细实现及各种钱包集成方式**：`references/REFERENCE.md`
- **区块链相关信息及区块浏览器使用指南**：`references/chains.md`

## 关于Tator

Tator的API（`x402.quickintel.io`）由总部位于美国的Quick Intel LLC公司运营。该公司已处理了超过5000万个代币的扫描请求。Tator的API被DexTools、DexScreener和Tator Trader等工具所使用，自2023年4月起正式上线。

- Tator文档：[https://docs.quickintel.io/tator](https://docs.quickintel.io/tator)
- x402协议详情：[https://www.x402.org](https://www.x402.org)
- 客户支持：[https://t.me/tatortrader](https://t.me/tatortrader)
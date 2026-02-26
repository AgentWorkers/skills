---
name: quickintel-scan
description: "使用 Quick Intel 的合约分析 API 来扫描任何代币，以检测安全风险、蜜罐（honeypots）和诈骗行为。适用场景包括：判断代币是否安全购买、检测蜜罐、分析合约的所有权和权限、查找隐藏的 mint（代币铸造）/blacklist（黑名单）功能，以及在交易前评估代币的风险。触发命令有：`is this token safe`、`scan token`、`check for honeypot`、`audit contract`、`rug pull check`、`token security`、`safe to buy`、`scam check`。该服务支持 63 个区块链平台，包括 Base、Ethereum、Solana、Sui、Tron。每次扫描的费用为 0.03 美元 USD，通过 x402 支付协议进行结算。需要使用兼容 x402 协议的钱包——推荐使用托管钱包服务（如 Sponge、AgentWallet），以确保不会暴露原始私钥。同时也支持使用专用热钱包进行程序化签名。此功能为只读模式，不会访问用户的代币或资产。"
credentials:
  recommended:
    - name: SPONGE_API_KEY
      description: "Sponge Wallet API key (no raw private key needed). Get at paysponge.com"
    - name: AGENTWALLET_API_TOKEN
      description: "AgentWallet API token (no raw private key needed). Get at frames.ag"
  advanced:
    - name: X402_PAYMENT_KEY
      description: "Private key for a DEDICATED hot wallet with minimal funds ($1-5 USDC). NEVER use your main wallet key. Only needed if not using a managed wallet service."
---
# 快速英特尔（Quick Intel）代币安全扫描器

该工具可扫描63个区块链上的代币，检测是否存在蜜罐、诈骗行为或安全风险，并在几秒钟内提供详细的审计报告。每次扫描费用为0.03美元（USDC），通过x402接口完成支付——该服务仅具有读取权限，不会触碰您的钱包或代币。

## 快速参考

| 情况 | 操作 |
|---------|--------|
| 用户询问“这个代币安全吗？” | 扫描代币并解读结果 |
| 用户想要购买/交易代币 | 交易前先进行扫描，发现风险提示 |
| 扫描结果显示 `is_Honeypot: true` | **停止**——告知用户该代币不可购买 |
| 扫描结果显示 `isScam: true` | **停止**——该代币为已知诈骗合约 |
| 扫描结果显示 `can_Mint: true` | 警告：代币所有者可能增加代币供应量 |
| 扫描结果显示购买/出售税过高（>10%） | 警告：过高费用会降低利润 |
| 扫描结果显示 `contract_Renounced: false` | 注意：代币所有者仍控制合约 |
| 扫描结果显示 `liquidity: false` | 可能使用非标准交易对——请在DEX聚合器上再次验证 |

## 如何扫描

**接口地址：** `POST https://x402.quickintel.io/v1/scan/full`

**请求体：**
```json
{
  "chain": "base",
  "tokenAddress": "0x..."
}
```

费用（0.03美元（USDC）会通过您的钱包自动扣除。如果您使用的是`@x402/fetch`、Sponge Wallet、AgentWallet、Vincent或Lobster.cash，支付流程是透明的。支持以下14个网络：Base（推荐，费用最低）、Ethereum、Arbitrum、Optimism、Polygon、Avalanche、Unichain、Linea、Sonic、HyperEVM、Ink、Monad、MegaETH（USDM）或Solana。

### 使用哪种集成方式？

> **⚠️ 钱包安全提示：** 该工具无需您的私钥。支付由您的代理钱包处理（无论您的代理使用哪种钱包）。如果您的代理尚未配置钱包，请使用**托管钱包服务**（如Sponge、AgentWallet、Vincent、Lobster.cash），而非直接使用私钥。如果必须使用编程方式签名，请使用**仅包含少量资金的专用热钱包**（1-5美元USDC），切勿使用主钱包。

| 您的设置 | 使用方式 | 私钥暴露风险 |
|---------|----------|-------------|
| 使用Sponge Wallet | **方案A** | ✅ 无需原始私钥——仅使用API密钥 |
| 使用AgentWallet（frames.ag） | **方案B** | ✅ 无需原始私钥——仅使用API令牌 |
| 使用Lobster.cash / Crossmint | 请参阅 `REFERENCE.md` | ✅ 无需原始私钥——使用托管钱包 |
| 使用Vincent Wallet | 请参阅 `REFERENCE.md` | ✅ 无需原始私钥——使用托管签名 |
| 已安装 `@x402/fetch` | **方案C** | ⚠️ 需要在环境中设置私钥 |
| 没有 `@x402/fetch` 且使用 viem 或 ethers.js | **方案D** | ⚠️ 需要在环境中设置私钥 |
| 使用Solana钱包 | 请参阅 `REFERENCE.md` | ⚠️ 需要在环境中设置私钥 |
| 不确定或未配置钱包 | 从 **方案A** 开始使用（推荐） | ✅ 无需原始私钥 |

### 方案A：Sponge Wallet（推荐——无需原始私钥）

```bash
curl -sS -X POST "https://apiwallet.paysponge.com/api/x402/fetch" \
  -H "Authorization: Bearer $SPONGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://x402.quickintel.io/v1/scan/full",
    "method": "POST",
    "body": {
      "chain": "base",
      "tokenAddress": "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00",
    },
    "preferred_chain": "base"
  }'
```

**注意：** 需要设置 `SPONGE_API_KEY` 环境变量。请在 [paysponge.com](https://paysponge.com) 注册。Sponge负责钱包管理和签名操作，您的代理无需接触私钥。

### 方案B：AgentWallet（无需原始私钥）

```javascript
const response = await fetch('https://frames.ag/api/wallets/{username}/actions/x402/fetch', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.AGENTWALLET_API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://x402.quickintel.io/v1/scan/full',
    method: 'POST',
    body: { chain: 'base', tokenAddress: '0x...' }
  }),
});
const scan = await response.json();
```

**注意：** 需要设置 `AGENTWALLET_API_TOKEN` 环境变量。请在 [frames.ag](https://frames.ag) 获取该密钥。

### 方案C：使用 `@x402/fetch`（编程签名）

> ⚠️ 需要使用私钥。请使用**仅包含少量资金的专用热钱包**，切勿使用主钱包。

```javascript
import { x402Fetch } from '@x402/fetch';
import { createWallet } from '@x402/evm';

// 使用专用钱包（仅存放支付资金，1-5美元USDC）
const wallet = createWallet(process.env.X402_payment_KEY);

const response = await x402Fetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json',
  body: JSON.stringify({ chain: 'base', tokenAddress: '0x...' },
  wallet,
  preferredNetwork: 'eip155:8453'
});

const scan = await response.json();
```

### 方案D：手动EVM签名（使用 viem）

> ⚠️ 需要使用私钥。请使用**仅包含少量资金的专用热钱包**，切勿使用主钱包。

如果您没有 `@x402/fetch`，请手动处理支付流程：

```javascript
import { keccak256, toHex } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

// 使用专用钱包（仅存放支付资金，1-5美元USDC）
const account = privateKeyToAccount(process.env.X402_payment_KEY);
const SCAN_URL = 'https://x402.quickintel.io/v1/scan/full';

// 步骤1：发送请求以获取支付所需的参数
const scanBody = JSON.stringify({ chain: 'base', tokenAddress: '0x...' });
const initialRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json',
  body: scanBody,
});

if (initialRes.status !== 402) throw new Error(`预期状态码为402，实际收到的是 ${initialRes.status}`);
const paymentRequired = await initialRes.json();

// 步骤2：查找支持的交易网络
const networkInfo = paymentRequired.accepts.find(a => a.network === 'eip155:8453');
if (!networkInfo) throw new Error('目标网络不可用');

// 步骤3：签名交易请求
const nonce = keccak256(toHex(`${Date.now()}-${Math.random()}`);
const validBefore = BigInt(Math.floor(Date.now() / 1000) + 3600);

const signature = await account.signTypedData({
  domain: {
    name: networkInfo.extra.name,
    version: networkInfo.extra.version,
    chainId: 8453,
    verifyingContract: networkInfo.asset,
  },
  types: {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' },
    ],
  },
  primaryType: 'TransferWithAuthorization',
  message: {
    from: account.address,
    to: networkInfo.payTo,
    value: BigInt(networkInfo.amount),
    validAfter: 0n,
    validBefore: validBefore,
    nonce,
  },
});

// 步骤4：构建支付签名
const paymentPayload = {
  x402Version: 2,
  scheme: 'exact',
  network: 'eip155:8453',
  payload: {
    signature,                         // 直接包含在payload中
    authorization: {
      from: account.address,
      to: networkInfo.payTo,
      value: networkInfo.amount,                  // 十进制字符串
      validAfter: '0',                            // 十进制字符串
      validBefore: validBefore.toString(),         // 十进制字符串
      nonce,
    },
  },
};

const paymentHeader = Buffer.from(JSON.stringify(paymentPayload)).toString('base64');

// 步骤5：再次发送请求
const paidRes = await fetch(SCAN_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'PAYMENT-SIGNATURE': paymentHeader,
  },
  body: scanBody,
});

// 处理可能的错误：
// ...
```

**常见错误及解决方法：**
- 签名应直接包含在请求体中，而非嵌套在 `authorization` 字段内。
- 请求头中必须包含 `x402Version: 2`。
- `value`、`validAfter` 和 `validBefore` 必须使用十进制字符串。
- 确保使用正确的接口路径（`/v1/scan/full`）。

## 支持的区块链（63个）

**EVM系列：** eth、base、arbitrum、optimism、polygon、bsc、avalanche、fantom、linea、scroll、zksync、blast、mantle、mode、zora、manta、sonic、berachain、unichain、abstract、monad、megaeth、hyperevm、shibarium、pulse、core、opbnb、polygonzkevm、metis、kava、klaytn、astar、oasis、iotex、conflux、canto、velas、grove、lightlink、bitrock、loop、besc、energi、maxx、degen、inevm、viction、nahmii、real、xlayer、apechain、morph、ink、soneium、plasma

**非EVM系列：** solana、sui、radix、tron、injective

请使用准确的区块链名称（例如，使用 `"eth"` 而不是 `"ethereum"`）。

## 解读扫描结果

### 需要避免购买的危险信号

| 字段 | 值 | 含义 |
|-------|-------|---------|
| `tokenDynamicDetails.is_Honeypot` | `true` | 该代币可能被用于诈骗 |
| `isScam` | `true` | 该代币为已知诈骗合约 |
| `isAirdropPhishingScam` | `true` | 存在钓鱼行为 |
| `quickiAudit.has_Scams` | `true` | 该代币包含诈骗特征 |
| `quickiAudit.can_Potentially_Steal_Funds` | `true` | 该代币可能存在窃取资金的风险 |

如果出现上述任何情况，请告知用户不要购买该代币，并解释原因。

### 需要谨慎处理的警告

| 字段 | 值 | 风险 |
|-------|-------|------|
| `buy_Tax` 或 `sell_Tax` | `> 10` | 过高的交易费用会降低利润 |
| `quickiAudit.can_Mint` | `true` | 代币所有者可能增加代币供应量 |
| `quickiAudit.can_Blacklist` | `true` | 代币所有者可能阻止交易 |
| `quickiAudit.can_Pause_Trading` | `true` | 代币所有者可能冻结所有交易 |
| `quickiAudit.can_Update_Fees` | `true` | 购买后费用可能增加 |
| `quickiAudit.hidden_Owner` | `true` | 代币所有者信息被隐藏 |
| `quickiAudit CONTRACT_Renounced` | `false` | 代币所有者仍控制合约 |

### 积极信号

| 字段 | 值 | 含义 |
|-------|-------|---------|
| `quickiAudit CONTRACT_Renounced` | `true` | 代币所有者已放弃控制权 |
| `contractVerified` | `true` | 代币源代码公开 |
| `quickiAudit.can_Mint` | `false` | 代币供应量固定 |
| `quickiAudit.can_Blacklist` | `false` | 代币所有者无阻止交易的能力 |
| `buy_Tax` 和 `sell_Tax` | `0` 或较低 | 交易费用较低 |

### 流动性检查

`tokenDynamicDetails.liquidity` 可指示是否检测到流动性池。

- `liquidity: false` 并不总是表示流动性差——Quick Intel 会检查主要交易对（如 WETH、USDC、USDT），但可能遗漏非标准交易对。请在DEX聚合器上再次验证。
- 即使 `liquidity: true`，也需检查 `lp_Locks` 以确认流动性是否真实。

## 示例：解读扫描结果

```json
{
  "tokenDetails": {
    "tokenName": "Example Token",
    "tokenSymbol": "EX",
    "tokenDecimals": 18,
    "tokenSupply": 1000000000
  },
  "tokenDynamicDetails": {
    "is_Honeypot": false,
    "buy_Tax": "0.0",
    "sell_Tax": "0.0",
    "liquidity": true
  },
  "isScam": null,
  "contractVerified": true,
  "quickiAudit": {
    "contract_Renounced": true,
    "can_Mint": false,
    "can_Blacklist": false,
    "can_Pause_Trading": false,
    "has_Scams": false,
    "hidden_Owner": false
  }
}
```

**评估：** “该代币相对安全。它不是蜜罐，没有诈骗特征，合约已被放弃控制，没有增加代币供应的功能，交易费用为0%。检测到流动性。但请注意，扫描结果仅供参考——如果合约使用了可升级的代理机制，其行为可能会发生变化。”

## 安全模型

| 您的角色 | Quick Intel 的角色 |
|---------|-------------------|
| 不会共享私钥 | 接收代币地址和区块链信息 |
| 收取支付费用（0.03美元USDC） | 分析合约字节码 |
| 决定是否交易 | 提供仅限读取的审计数据 |

Quick Intel 绝不会接收您的私钥，也不会操作您的代币。Quick Intel 仅具有读取权限，不参与任何交易或审批流程。

**重要提示：** 请勿将私钥、助记词或钱包凭证输入任何输入框。Quick Intel 仅需要代币的合约地址和区块链信息。

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|------|
| `402 Payment Required` | 未发送支付请求头 | 确保钱包已配置并拥有足够的资金（0.03美元USDC） |
| `402 Payment verification failed` | 签名错误或余额不足 | 检查请求体结构（详见 `REFERENCE.md`） |
| `400 Invalid Chain` | 未识别的区块链名称 | 请使用官方支持的区块链名称 |
| `400 Invalid Address` | 地址格式错误 | 请确保地址格式正确（EVM使用 `0x...`，Solana使用 `base58`） |
| `404 Token Not Found` | 该代币在该区块链上不存在 | 请核实地址和区块链信息是否匹配 |

## 其他注意事项

- 扫描结果为实时快照。即使今天安全，明天该代币也可能因所有权变更或合约升级而变得不安全。请定期重新扫描您持有的代币。
- 无论扫描结果如何，系统都会收取费用。请使用 `payment-identifier` 扩展名进行安全重试（详见 `REFERENCE.md`）。
- 本工具仅提供数据参考，不提供投资建议。
- 对于高价值交易，请在区块浏览器中进一步核实信息，检查代币持有者分布，并在DEX聚合器上确认流动性。

## 相关接口

- 在进行交易前，请查询已接受的支付请求和交易方案：`GET https://x402.quickintel.io/accepted`

## 相关资源

- Quick Intel 文档：https://docs.quickintel.io
- x402 协议：https://www.x402.org
- 支付接口详情：https://x402.quickintel.io/accepted
- 帮助支持：https://t.me/Quicki_TG

## 关于 Quick Intel

Quick Intel 的接口（`x402.quickintel.io`）由位于美国的加密货币安全公司 Quick Intel LLC 运营。

- 已处理超过5000万个代币的扫描请求，覆盖40多个区块链网络。
- 其安全扫描API被多个工具（如 DexTools、DexScreener 和 Tator Trader）使用。
- 自2023年4月起开始运营。
- 更多信息：[quickintel.io](https://quickintel.io)

## 参考资料

- Quick Intel 官方文档：https://docs.quickintel.io
- x402 协议文档：https://www.x402.org
- 支付接口详情：https://x402.quickintel.io/accepted
- 客户服务：https://t.me/Quicki_TG
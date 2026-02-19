---
name: bondterminal-x402
description: 使用 x402 无密钥支付方式查询 BondTerminal API。无需 API 密钥——在 Base 主网上每次请求的费用为 0.01 美元 USD。当用户请求阿根廷债券数据、分析报告、现金流信息、历史记录、国家风险评级（riesgo país），或查询 ISIN/股票代码（例如 AL30、GD30、US040114HS26）时，请使用此方式。系统支持自动处理 402 错误并尝试重新支付。
metadata:
  author: 0juano
  version: "2.1.0"
---
# BondTerminal x402

使用 x402 认证方式查询 BondTerminal API。无需 API 密钥或订阅服务，只需签署协议并按请求付费即可。

**费用：** 在 Base 主网上，每次请求的费用为 0.01 美元（USDC）。

## API 端点

基础 URL：`https://bondterminal.com/api/v1`

| 方法 | 端点 | 描述 | 认证方式 |
|--------|----------|-------------|------|
| GET | `/treasury-curve` | 美国国债收益率曲线 | 免费 |
| GET | `/bonds` | 列出所有债券（60 种以上） | x402 |
| GET | `/bonds/:id` | 通过 ISIN 或本地代码标识符查询债券详情 | x402 |
| GET | `/bonds/:id/analytics` | 债券价格、到期收益率、期限、利差信息 | x402 |
| GET | `/bonds/:id/cashflows` | 债券现金流计划 | x402 |
| GET | `/bonds/:id/history` | 债券的历史价格/收益率/利差数据 | x402 |
| POST | `/calculate` | 根据自定义价格计算债券分析数据 | x402 |
| GET | `/riesgo-pais` | 当前阿根廷国家风险评级 | x402 |
| GET | `/riesgo-pais/history` | 阿根廷国家风险评级的历史数据 | x402 |
| POST | `/calculate/batch` | 批量计算 | 仅限Bearer模式 |

**标识符格式：**  
- ISIN（例如：`US040114HS26`）  
- 带有 D/C 后缀的本地代码标识符（例如：`AL30D`、`GD30D`）

完整文档：https://bondterminal.com/developers  
本技能中的 API 端点参考：`references/endpoints.md`

## x402 的工作原理

1. 如果直接调用任何 x402 端点且未进行认证，服务器会返回 402 状态码，并附带 `PAYMENT-REQUIRED` 头部信息。  
2. 解码该头部信息（Base64 编码的 JSON 数据），获取付款要求（金额、资产类型、网络类型、收款人地址）。  
3. 通过 x402 客户端库签署 EIP-3009 协议中的 `transferWithAuthorization` 消息。  
4. 重新发送请求，将签名后的付款信息（包含在 `PAYMENT-SIGNATURE` 头部字段中）作为请求的一部分；如果签名失败，则使用 `X-PAYMENT` 作为备用方式。  
5. 服务器通过 Coinbase 的中间服务验证付款信息，并返回数据以及 `PAYMENT-RESPONSE` 头部信息。

## 设置

### 1. 安装依赖项

```bash
npm install @x402/core @x402/evm viem
```

> **注意：** 代码示例使用了 ES 模块。请使用 `.mjs` 文件扩展名，或在 `package.json` 中添加 `"type": "module"` 选项。

### 2. 配置签名器

x402 付款流程需要在 Base 主网上配置一个具有 USDC 存款的 EVM 签名器。请按照 [x402 EVM 文档](https://github.com/coinbase/x402/tree/main/packages/evm) 的说明进行配置。  
签名器需要实现 `{ address, signTypedData }` 接口；任何兼容 EVM 的钱包客户端均可使用（硬件钱包、KMS、注入式服务提供商等）。  
完整的签名器配置示例请参见 `references/signer-setup.md`。

### 3. 注册 x402 客户端

```javascript
import { x402Client } from '@x402/core/client';
import { x402HTTPClient } from '@x402/core/http';
import { ExactEvmScheme } from '@x402/evm'; // exact export name

// signer = { address, signTypedData } — see references/signer-setup.md
const scheme = new ExactEvmScheme(signer);
const client = new x402Client();
client.register('eip155:8453', scheme); // Base mainnet
const httpClient = new x402HTTPClient(client);
```

## 获取债券数据

```javascript
async function fetchBT(path) {
  const url = `https://bondterminal.com/api/v1${path}`;
  let res = await fetch(url);

  if (res.status === 402) {
    const paymentRequired = httpClient.getPaymentRequiredResponse(
      (name) => res.headers.get(name),
      await res.json()
    );
    const payload = await httpClient.createPaymentPayload(paymentRequired);

    // Preferred v2 header
    res = await fetch(url, {
      headers: httpClient.encodePaymentSignatureHeader(payload),
    });

    // Legacy fallback for servers still expecting X-PAYMENT
    if (res.status === 402) {
      const encoded = Buffer.from(JSON.stringify(payload)).toString('base64');
      res = await fetch(url, { headers: { 'X-PAYMENT': encoded } });
    }
  }

  if (!res.ok) {
    throw new Error(`BondTerminal request failed (${res.status})`);
  }

  return res.json();
}

// Examples
const bonds = await fetchBT('/bonds');
const analytics = await fetchBT('/bonds/AL30D/analytics');
const riesgo = await fetchBT('/riesgo-pais');
```

## 快速测试

验证免费请求和付费请求的处理流程：

```javascript
await fetchBT('/treasury-curve'); // free route (no payment)
await fetchBT('/riesgo-pais');    // paid route (triggers x402 flow)
```

## 钱包要求

用于签署交易的钱包需要满足以下条件：  
- 拥有 Base 主网上的 USDC 账户（用于支付每次请求的 0.01 美元费用）。  
- 无需 ETH 来支付网络手续费——x402 使用的是链下签名（EIP-3009 协议），因此不涉及链上交易。

## 其他注意事项：  
- `POST /calculate/batch` 请求需要使用 Bearer API 密钥进行订阅，该密钥无法通过 x402 方式获取。  
- 本地代码标识符必须带有 D/C 后缀（例如：`AL30D` 表示美元债券，`AL30C` 表示阿根廷比索债券）。  
- 交易结算在链上进行，每次付费请求都会生成可验证的交易哈希值。  
- `PAYMENT-RESPONSE` 头部信息包含结算相关元数据（付款人、交易哈希、网络类型）。
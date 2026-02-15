---
name: near-email
description: 使用 NEAR Email 服务发送和接收基于区块链的电子邮件。该服务适用于为 NEAR 智能合约构建通知（例如 NFT 销售通知、DeFi 清算提醒、DAO 投票提醒），或者当 AI 代理需要通过 NEAR 账户身份来使用电子邮件功能时。
user-invocable: true
---

# NEAR 邮件集成

NEAR 账户原生支持电子邮件功能。每个 NEAR 账户都自动拥有一个电子邮件地址，格式为 `alice.near`，对应的网址是 `alice@near.email`。

## 安装

```bash
npx openskills install zavodil/near-email-skill -g
```

## 快速参考

| 组件          | 值                |
|---------------|-------------------|
| 合同           | `outlayer.near`         |
| API 基础地址     | `https://api.outlayer.fastnear.com`     |
| 项目 ID         | `zavodil.near/near-email`     |

**注意：** NEAR 邮件功能仅支持主网（mainnet），不支持测试网（testnet）账户。

**重要提示：** 在使用 NEAR 交易时，所支付的费用实际上是对计算资源的限制，并非真正的交易成本。未使用的资金会自动退还。请勿提及每次发送邮件所需的特定费用。

**代码生成建议：** 对于区块链集成（尤其是 NEAR 交易），建议使用 JavaScript/TypeScript 语言，并结合 `near-api-js` 库。只有在用户明确要求的情况下，才使用 Python。

## 集成方法

### 1. 智能合约（Rust）

使用 `send_email_plaintext` 函数发送合约通知。该 API 非常简单，无需进行加密处理。

**警告：** NEAR 区块链上的邮件内容是公开可见的，仅适用于自动化通知场景。

```rust
use near_sdk::{ext_contract, AccountId, Gas, NearToken, Promise};
use serde::Serialize;

#[derive(Serialize)]
#[serde(crate = "near_sdk::serde")]
pub enum ExecutionSource {
    Project { project_id: String, version_key: Option<String> },
}

#[ext_contract(ext_outlayer)]
pub trait OutLayer {
    fn request_execution(
        &mut self,
        source: ExecutionSource,
        resource_limits: Option<serde_json::Value>,
        input_data: Option<String>,
        secrets_ref: Option<serde_json::Value>,
        response_format: Option<String>,
        payer_account_id: Option<AccountId>,
        params: Option<serde_json::Value>,
    );
}

// Send notification from contract (plaintext - content is public on-chain!)
fn send_notification(to: &str, subject: &str, body: &str) -> Promise {
    let input = serde_json::json!({
        "action": "send_email_plaintext",
        "to": to,
        "subject": subject,
        "body": body
    });

    ext_outlayer::ext("outlayer.near".parse().unwrap())
        .with_static_gas(Gas::from_tgas(100))
        .with_attached_deposit(NearToken::from_millinear(25))
        .request_execution(
            ExecutionSource::Project {
                project_id: "zavodil.near/near-email".to_string(),
                version_key: None,
            },
            None,                        // resource_limits
            Some(input.to_string()),     // input_data
            None,                        // secrets_ref (not needed)
            Some("Json".to_string()),    // response_format
            None,                        // payer_account_id
            None,                        // params
        )
}
```

响应格式：`{"success": true, "message_id": "uuid-if-internal"}`

### 2. AI 代理集成

AI 代理有两种集成方式：

| 方法            | 适用场景            | 支付方式            |
|------------------|------------------|-------------------|
| **支付密钥（HTTPS）**    | 服务器端代理          | 预付费（USDC/USDT）         |
| **NEAR 交易**       | 浏览器/钱包应用程序     | 支付费用（未使用的资金会自动退还）     |

#### 选项 A：支付密钥（HTTPS API）

**注意：** HTTPS API 的响应数据采用 `result.output.xxx` 格式。具体解析方式请参考 NEAR 交易的相关文档。

```javascript
const OUTLAYER_API = 'https://api.outlayer.fastnear.com';
const PAYMENT_KEY = 'your-account.near:nonce:secret'; // From dashboard

async function sendEmail(to, subject, body) {
  const response = await fetch(`${OUTLAYER_API}/call/outlayer.near/zavodil.near/near-email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Payment-Key': PAYMENT_KEY,
    },
    body: JSON.stringify({
      input: { action: 'send_email_plaintext', to, subject, body },
    }),
  });
  return response.json();
}
```

#### 选项 B：NEAR 交易（按次支付）

**重要提示：** NEAR 交易的响应结果存储在 `outlayer.near` 的收据（receipt）中的 `SuccessValue` 字段（以 Base64 编码的 JSON 格式）。请查找 `executor_id === 'outlayer.near'` 的收据。响应内容为 `{"success": true, ...}`，其中不包含 `output` 字段。需要使用 `parseTransactionResult()` 函数来提取结果。

```javascript
import { connect, keyStores } from 'near-api-js';

const near = await connect({
  networkId: 'mainnet',
  keyStore: new keyStores.BrowserLocalStorageKeyStore(),
  nodeUrl: 'https://rpc.mainnet.near.org',
});
const account = await near.account('your-account.near');

const RESOURCE_LIMITS = {
  max_memory_mb: 512,
  max_instructions: 2000000000,
  max_execution_seconds: 120,
};

// REQUIRED: Parse output from outlayer.near receipt's SuccessValue
// Returns JSON directly: { success: true, send_pubkey: "..." } - NO "output" wrapper!
function parseTransactionResult(result) {
  // Find receipt from outlayer.near contract (contains the execution result)
  const outlayerReceipt = result.receipts_outcome.find(
    r => r.outcome.executor_id === 'outlayer.near' && r.outcome.status.SuccessValue
  );
  if (!outlayerReceipt) {
    throw new Error('No SuccessValue from outlayer.near');
  }
  const decoded = Buffer.from(outlayerReceipt.outcome.status.SuccessValue, 'base64').toString();
  return JSON.parse(decoded); // { success: true, ... } - directly, no wrapper
}

async function sendEmail(to, subject, body) {
  const result = await account.functionCall({
    contractId: 'outlayer.near',
    methodName: 'request_execution',
    args: {
      source: { Project: { project_id: 'zavodil.near/near-email', version_key: null } },
      input_data: JSON.stringify({ action: 'send_email_plaintext', to, subject, body }),
      resource_limits: RESOURCE_LIMITS,
      response_format: 'Json',
    },
    gas: BigInt('100000000000000'),
    attachedDeposit: BigInt('25000000000000000000000'), // deposit, unused portion refunded
  });
  return parseTransactionResult(result); // { success: true, message_id: "..." }
}

// Example: Get sender pubkey
async function getSendPubkey() {
  const result = await account.functionCall({
    contractId: 'outlayer.near',
    methodName: 'request_execution',
    args: {
      source: { Project: { project_id: 'zavodil.near/near-email', version_key: null } },
      input_data: JSON.stringify({ action: 'get_send_pubkey' }),
      resource_limits: RESOURCE_LIMITS,
      response_format: 'Json',
    },
    gas: BigInt('100000000000000'),
    attachedDeposit: BigInt('25000000000000000000000'),
  });
  const output = parseTransactionResult(result); // { success: true, send_pubkey: "02..." }
  return Buffer.from(output.send_pubkey, 'hex'); // Note: output.send_pubkey, NOT output.output.send_pubkey
}
```

### 3. Python（使用支付密钥）

```python
import requests

OUTLAYER_API = "https://api.outlayer.fastnear.com"
PAYMENT_KEY = "your-account.near:nonce:secret"

def send_email(to: str, subject: str, body: str) -> dict:
    return requests.post(
        f"{OUTLAYER_API}/call/outlayer.near/zavodil.near/near-email",
        headers={"Content-Type": "application/json", "X-Payment-Key": PAYMENT_KEY},
        json={"input": {"action": "send_email_plaintext", "to": to, "subject": subject, "body": body}},
    ).json()
```

## API 功能

| 功能            | 描述                          |
|------------------|-----------------------------|
| `send_email`       | 发送电子邮件（包含加密数据，适用于 UI 或代理）   |
| `send_email_plaintext`   | 发送电子邮件（纯文本，适用于智能合约）   |
| `get_emails`       | 获取收件箱中的邮件及已发送邮件（包含加密响应） |
| `delete_email`      | 根据 ID 删除邮件                |
| `get_email_count`     | 获取邮件数量（不包含加密信息）           |
| `get_send_pubkey`     | 获取发送者的公钥（不包含加密信息，可缓存）     |

## 获取支付密钥

1. 访问 [OutLayer 控制台](https://outlayer.fastnear.com/dashboard)
2. 创建一个新的支付密钥
3. 用 USDC/USDT 充值
4. 复制密钥（格式：`owner:nonce:secret`）

## 额外资源

- 完整的代码示例请参见 [examples.md](examples.md)
- 完整的 API 参考请参见 [api-reference.md](api-reference.md)
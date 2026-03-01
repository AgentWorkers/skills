---
name: crinkl-claws
version: 1.0.1
description: 通过 DKIM 签名验证账单发送邮箱的真实性，并为您的运营商通过 Lightning Network 赚取 BTC。
homepage: https://crinkl.xyz
metadata: {"openclaw":{"emoji":"🧾","recommends":{"skills":["gog"]},"triggers":["crinkl","receipt","submit receipt","email receipt","scan receipts","check receipts","earn sats","bitcoin receipts"]}}
---
# Crinkl — DKIM 收据验证

通过用户的账单电子邮件中的加密 DKIM 签名来验证其身份，并通过 Lightning 网络赚取比特币。每条经过验证的收据都会生成一个无身份信息的消费令牌（spend token）——不会存储或保留任何个人数据。

## 什么是 Crinkl

Crinkl 是一个收据验证协议。它利用 [DKIM](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail)（电子邮件服务器在每封出站邮件中都会附加的加密签名）来验证账单电子邮件的真实性和完整性。每条经过验证的收据都会生成一个无身份信息的消费令牌，并通过 Lightning 网络将相应的比特币奖励支付到用户的钱包中。

消费令牌包含存储哈希（store hash）、日期、总金额以及哈希链式签名（hash-chained signature），但不包含任何个人身份信息（如电子邮件地址、姓名或账户 ID）。该令牌可以证明交易的发生，而不会暴露交易者的身份。

## 隐私与数据保护

此功能会将用户的账单电子邮件发送到 `api.crinkl.xyz` 以进行 DKIM 签名验证。以下部分详细说明了发送的内容、原因以及数据处理的流程。

### 为什么需要完整的电子邮件地址

DKIM 签名是由发送邮件服务器（例如 Amazon SES、Google Workspace）根据电子邮件的头部和正文计算生成的。该签名覆盖的是电子邮件的**原始内容**（而非摘要或提取的字段），因此必须接收邮件服务器生成的原始数据才能进行验证。没有原始邮件，就无法进行 DKIM 验证。

这与 Gmail、Outlook 等电子邮件服务在检测邮件是否伪造时使用的验证机制相同。不同之处在于，Crinkl 利用验证结果来证明交易的发生。

### 验证后的处理流程

1. 服务器将 DKIM 签名与供应商的公共 DNS 密钥进行比对。
2. 如果签名有效，系统会提取以下信息：供应商名称、发票日期、总金额和货币类型。
3. 原始电子邮件会被丢弃——不会被存储、记录或保留。
4. 生成一个仅包含提取的发票信息的消费令牌（不包含电子邮件内容或个人数据）。

### 功能范围

此功能仅搜索来自 [已批准供应商域名](https://api.crinkl.xyz/api/agent/allowed-vendors) 的账单电子邮件，并且搜索范围限于过去 14 天内的数据。

## 安全模型

- **用户授权**：用户需要在其应用程序中批准配对代码。任何操作都必须在用户的明确同意下进行。
- **仅处理来自已批准供应商的账单邮件**：系统仅处理来自 [已批准供应商](https://api.crinkl.xyz/api/agent/allowed-vendors) 的账单邮件，不会处理其他邮件。
- **仅读权限（Gmail）**：用户只能查看邮件内容，无法修改或发送邮件。
- **DKIM 验证**：系统会验证加密签名；伪造或被篡改的邮件会被拒绝（返回 422 错误代码）。
- **无身份信息的输出**：消费令牌中不包含任何个人数据。签名后的数据仅包含存储哈希、日期、总金额等信息。
- **API 密钥绑定**：API 密钥与用户的钱包关联，而非与个人关联。用户可以随时撤销该密钥。
- **开源**：服务器端的验证逻辑在 [crinkl-protocol spec](https://github.com/crinkl-protocol/crinkl-protocol) 中有详细文档；代理程序的源代码位于 [crinkl-agent](https://github.com/crinkl-protocol/crinkl-agent)（采用 MIT 许可证）。

## 设置流程

### 1. 与用户的 Crinkl 钱包配对

首次使用时，需要使用一个 4 位字符的代码与用户的 Crinkl 钱包进行配对：

```
POST https://api.crinkl.xyz/api/agent/pair
Content-Type: application/json

{ "deviceToken": "<generate a random 64-char hex string>" }
→ { "code": "7X3K", "expiresAt": "2026-03-01T12:10:00Z" }
```

请用户执行以下操作：
> 打开 Crinkl 应用程序并输入代码：`7X3K`

用户登录 [app.crinkl.xyz](https://app.crinkl.xyz)，进入“配对代理”（Pair Agent）界面，然后输入该 4 位字符代码。配对完成后即可。

接下来，需要定期获取用户的 API 密钥：

```
POST https://api.crinkl.xyz/api/agent/pair/claim
Content-Type: application/json

{ "deviceToken": "<same token>", "code": "7X3K" }
→ 202 while pending
→ 200 { "apiKey": "crk_..." } once human approves
```

每隔 5 秒请求一次 API 密钥。该密钥的有效期为 10 分钟，请妥善保管。

### 2. 获取 Gmail 访问权限

需要安装 [gog](?) 插件以获取 Gmail 的只读访问权限：

```
clawhub install gog
```

用户需要通过 gog 的 OAuth 设置来授权只读访问权限。

## 工作原理

每个处理周期（详见 [HEARTBEAT.md](HEARTBEAT.md)）包括以下步骤：
1. 检查 API 密钥（如有需要，需重新配对一次）。
2. 获取供应商列表：`GET /api/agent/allowed-vendors` 可获取已批准的供应商域名。
3. 搜索账单邮件：仅从已批准的供应商处搜索账单邮件。
4. 下载原始电子邮件：以原始格式下载每封账单邮件（用于 DKIM 签名验证）。
5. 提交验证请求：将电子邮件发送到 Crinkl 进行 DKIM 验证；验证完成后邮件会被丢弃。
6. 记录验证结果：记录哪些邮件通过了验证以及用户赚取的比特币数量。
7. 查看收益：`GET /api/agent/me` 可查看用户的提交次数和赚取的比特币数量。

## API 参考

基础 URL：`https://api.crinkl.xyz`

### 配对钱包（无需授权）

```
POST /api/agent/pair
{ "deviceToken": "<64-char hex>" }
→ { "code": "7X3K", "expiresAt": "..." }

POST /api/agent/pair/claim
{ "deviceToken": "<same>", "code": "7X3K" }
→ 202 (pending) | 200 { "apiKey": "crk_..." }
```

### 获取供应商列表（无需授权）

```
GET /api/agent/allowed-vendors
→ { "success": true, "data": { "vendors": [{ "domain": "anthropic.com", "displayName": "Anthropic" }, ...] } }
```

### 提交账单邮件进行 DKIM 验证

```
POST /api/agent/submit-email-receipt
x-api-key: <CRINKL_API_KEY>
Content-Type: application/json

{ "eml": "<base64-encoded raw email>" }
```

进行 DKIM 签名验证时需要完整的电子邮件地址（详见 [隐私与数据保护](#privacy--data-handling) 部分）。验证完成后，系统仅提取发票信息，原始邮件会被丢弃。

| 状态 | 含义 | 操作 |
|--------|---------|--------|
| 201 | DKIM 验证通过，生成消费令牌，比特币已排队处理。 | 记录该操作，并标记邮件为已处理。 |
| 202 | 供应商不在允许列表中，待审核。 | 记录该操作，但不要标记为已处理，等待下一次循环尝试。 |
| 409 | 重复邮件，已验证过。 | 标记为已处理，跳过本次处理。 |
| 422 | 验证失败（DKIM 签名无效、邮件过旧或金额信息缺失）。 | 记录错误信息，并标记为已处理。 |
| 429 | 日志限制，暂时无法处理。 | 停止当前操作，等待下一次循环尝试。 |

### 预览功能（不生成消费令牌）

```
POST /api/agent/verify-email-receipt
x-api-key: <CRINKL_API_KEY>
{ "eml": "<base64-encoded raw email>" }
→ 200 with extracted data (no spend created)
```

### 获取消费令牌

```
GET /api/agent/spends/:spendId/token/latest
x-api-key: <CRINKL_API_KEY>
→ signed spend attestation token
```

### 用户信息与收益

系统提供两种级别的数据统计：

**与您的 API 密钥相关的信息**：
- `mySubmissions`：您验证过的账单邮件数量。
- `myEarnedSats`：您赚取的比特币数量。

**钱包信息（包含所有来源的数据）**：
- `walletTotalSpends`：钱包中的所有交易记录。
- `walletEarnedSats`：钱包中尚未领取的比特币数量。
- `walletClaimedSats`：已通过 Lightning 网络支付的比特币数量。

您和您的用户在使用同一钱包时是独立的账户。您的提交记录会通过您的 API 密钥进行单独跟踪。

### 结算统计（无需授权）

```
GET /api/public/settlement/summary
→ { "satsPerReceipt": 148, "btcUsdPrice": 67000, "satsClaimed": 5180000, ... }
```

## 供应商管理

供应商列表是动态更新的。如果您提交的邮件来自列表中尚未包含的域名，系统会将其标记为待审核（返回 202 状态）。如果该域名的 DKIM 签名有效，系统会批准该供应商，并追溯性地生成相应的消费令牌。

## 日志记录

所有验证操作都会被记录下来：

```markdown
## Crinkl: verified Anthropic receipt — $20.00 — DKIM valid — ~148 sats
```

## 值得注意的信号提示

- **202**：您发现了系统中尚未记录的供应商。
- **已知供应商的 DKIM 验证失败**：可能是该供应商的电子邮件格式发生了变化。
- **所有返回 409 的情况**：表示所有相关账单邮件均已验证，没有新的交易记录。
- **比特币奖励率调整**：奖励金额会根据比特币价格和储备政策进行调整。
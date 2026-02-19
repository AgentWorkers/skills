---
name: pinata-api
description: Pinata IPFS API 提供文件存储、分组管理、网关服务、签名验证、X402支付功能以及基于人工智能的向量搜索服务。
homepage: https://pinata.cloud
metadata: {"openclaw": {"emoji": "📌", "requires": {"env": ["PINATA_JWT", "GATEWAY_URL"]}, "primaryEnv": "PINATA_JWT"}}
---
# Pinata API

本文档介绍了 Pinata 的 IPFS 存储 API，提供了上传文件、管理文件组、创建网关、添加签名、设置 x402 支付指令以及执行基于 AI 的向量搜索等功能。

**仓库链接：** https://github.com/PinataCloud/pinata-api-skill

## 认证

所有请求必须在 `Authorization` 头部包含 Pinata 的 JWT 令牌：

```
Authorization: Bearer $PINATA_JWT
```

**环境变量：**

- `PINATA_JWT`（必填）：您的 Pinata API JWT 令牌。请在 [app.pinata.cloud/developers/api-keys](https://app.pinata.cloud/developers/api-keys) 获取令牌。
- `GATEWAY_URL`（必填）：您的 Pinata 网关域名（例如：`your-gateway.mypinata.cloud`）。请在 [app.pinata.cloud/gateway](https://app.pinata.cloud/gateway) 查找网关信息。
- `GATEWAY_KEY`（可选）：用于访问非关联于您 Pinata 账户的公共 IPFS 内容的网关密钥。详情请参阅 [网关访问控制](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys)。

### 测试认证

```bash
curl -s https://api.pinata.cloud/data/testAuthentication \
  -H "Authorization: Bearer $PINATA_JWT"
```

## 基本 URL

- **API**：`https://api.pinata.cloud`
- **上传文件**：`https://uploads.pinata.cloud`

## 常用参数

- `network`：IPFS 网络类型（默认为 `public` 或 `private`）
- 分页使用 `limit` 和 `pageToken` 查询参数

## 文件操作

### 文件搜索

```bash
GET /v3/files/{network}?name=...&cid=...&mimeType=...&limit=...&pageToken=...
```

```bash
curl -s "https://api.pinata.cloud/v3/files/public?limit=10" \
  -H "Authorization: Bearer $PINATA_JWT"
```

查询参数（均为可选）：`name`、`cid`、`mimeType`、`limit`、`pageToken`

### 通过 ID 获取文件

```bash
GET /v3/files/{network}/{id}
```

```bash
curl -s "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 更新文件元数据

```bash
PUT /v3/files/{network}/{id}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "new-name", "keyvalues": {"key": "value"}}'
```

### 删除文件

```bash
DELETE /v3/files/{network}/{id}
```

```bash
curl -s -X DELETE "https://api.pinata.cloud/v3/files/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 上传文件

```bash
POST https://uploads.pinata.cloud/v3/files
```

使用 `multipart/form-data` 格式上传文件。**请勿** 手动设置 `Content-Type`，由 HTTP 客户端自行处理边界信息。

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/files" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -F "file=@/path/to/file.png" \
  -F "network=public" \
  -F "group_id={group_id}" \
  -F 'keyvalues={"key":"value"}'
```

```javascript
const fs = require('fs');
const FormData = require('form-data');

const form = new FormData();
form.append('file', fs.createReadStream('/path/to/file.png'));
form.append('network', 'public');

const response = await fetch('https://uploads.pinata.cloud/v3/files', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${process.env.PINATA_JWT}` },
  body: form,
});
```

```python
import os, requests

response = requests.post(
    'https://uploads.pinata.cloud/v3/files',
    headers={'Authorization': f'Bearer {os.environ["PINATA_JWT"]}'},
    files={'file': open('/path/to/file.png', 'rb')},
    data={'network': 'public'},
)
```

可选参数：`network`、`group_id`、`keyvalues`（JSON 字符串）

## 文件组操作

### 列出文件组

```bash
GET /v3/groups/{network}?name=...&limit=...&pageToken=...
```

```bash
curl -s "https://api.pinata.cloud/v3/groups/public?limit=10" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 创建文件组

```bash
POST /v3/groups/{network}
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/groups/public" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-group"}'
```

### 获取文件组信息

```bash
GET /v3/groups/{network}/{id}
```

### 更新文件组信息

```bash
PUT /v3/groups/{network}/{id}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/groups/public/{id}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"name": "updated-name"}'
```

### 删除文件组

```bash
DELETE /v3/groups/{network}/{id}
```

### 将文件添加到文件组

```bash
PUT /v3/groups/{network}/{groupId}/ids/{fileId}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/groups/public/{groupId}/ids/{fileId}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 从文件组中删除文件

```bash
DELETE /v3/groups/{network}/{groupId}/ids/{fileId}
```

## 网关与下载

### 创建私有下载链接

```bash
POST /v3/files/private/download_link
```

生成用于访问私有文件的临时签名 URL。

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/private/download_link" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://'"$GATEWAY_URL"'/files/{cid}",
    "expires": 600,
    "date": '"$(date +%s)"',
    "method": "GET"
  }'
```

- `url`（必填）：完整的网关 URL：`https://{GATEWAY_URL}/files/{cid}`
- `expires`（可选）：链接的有效时间（以秒为单位，默认为 600 秒）
- `date`（必填）：当前的 Unix 时间戳（以秒为单位）
- `method`（必填）：HTTP 方法，通常为 `"GET"`

### 创建预签名上传链接

```bash
POST https://uploads.pinata.cloud/v3/files/sign
```

生成客户端上传所需的预签名 URL（客户端无需提供 JWT 令牌）。

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/files/sign" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "date": '"$(date +%s)"',
    "expires": 3600
  }'
```

可选参数：`max_file_size`（字节）、`allow_mime_types`（字符串数组）、`group_id`、`filename`、`keyvalues`

## 签名

使用 EIP-712 签名来验证文件内容的真实性。

### 添加签名

```bash
POST /v3/files/{network}/signature/{cid}
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/public/signature/{cid}" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"signature": "0x...", "address": "0x..."}'
```

### 获取签名信息

```bash
GET /v3/files/{network}/signature/{cid}
```

### 删除签名

```bash
DELETE /v3/files/{network}/signature/{cid}
```

## 通过 CID 固定文件

**仅限公共网络**：通过文件对应的 CID 固定 IPFS 内容。

```bash
POST /v3/files/public/pin_by_cid
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/files/public/pin_by_cid" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{"cid": "bafybeig..."}'
```

可选参数：`name`、`group_id`、`keyvalues`、`host_nodes`（多地址数组）

### 查询文件固定请求

```bash
GET /v3/files/public/pin_by_cid?order=ASC&status=...&cid=...&limit=...&pageToken=...
```

### 取消文件固定请求

```bash
DELETE /v3/files/public/pin_by_cid/{id}
```

## x402 支付指令

使用 x402 协议和 USDC 在 Base 上实现文件内容的货币化。

**USDC 合约地址：**
- Base 主网：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia（测试网）：`0x036CbD53842c5426634e7929541eC2318f3dCF7e`

**注意：** `amount` 参数应使用最小的 USDC 单位（6 位小数）。例如，$1.50 应表示为 `"1500000"`。

### 创建支付指令

```bash
POST /v3/x402/payment_instructions
```

```bash
curl -s -X POST "https://api.pinata.cloud/v3/x402/payment_instructions" \
  -H "Authorization: Bearer $PINATA_JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Payment",
    "description": "Pay to access this content",
    "payment_requirements": [{
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "pay_to": "0xYOUR_WALLET_ADDRESS",
      "network": "base",
      "amount": "1500000"
    }]
  }'
```

- `name`（必填）：支付指令的显示名称
- `description`（可选）：支付指令的描述
- `payment_requirements`（必填）：包含 `asset`（USDC 地址）、`pay_to`（收款钱包地址）、`network`（`"base"` 或 `"base-sepolia"`）、`amount`（金额，以最小单位表示）的数组

### 列出支付指令

```bash
GET /v3/x402/payment_instructions?limit=...&pageToken=...&cid=...&name=...&id=...
```

### 获取支付指令信息

```bash
GET /v3/x402/payment_instructions/{id}
```

### 删除支付指令

```bash
DELETE /v3/x402/payment_instructions/{id}
```

### 将 CID 与支付指令关联

```bash
PUT /v3/x402/payment_instructions/{id}/cids/{cid}
```

```bash
curl -s -X PUT "https://api.pinata.cloud/v3/x402/payment_instructions/{id}/cids/{cid}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 从支付指令中移除 CID

```bash
DELETE /v3/x402/payment_instructions/{id}/cids/{cid}
```

## 向量化（AI 搜索）

为文件生成向量嵌入，并在文件组之间进行语义搜索。

### 对文件进行向量化处理

```bash
POST https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```

```bash
curl -s -X POST "https://uploads.pinata.cloud/v3/vectorize/files/{file_id}" \
  -H "Authorization: Bearer $PINATA_JWT"
```

### 删除文件的向量表示

```bash
DELETE https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```

### 查询向量表示（语义搜索）

```bash
POST https://uploads.pinata.cloud/v3/vectorize/groups/{group_id}/query
```

## 注意事项：

- 所有 JSON 请求的 `Content-Type` 需设置为 `application/json`。
- 文件上传使用 `multipart/form-data` 格式，**请勿** 手动设置 `Content-Type`。
- 分页时使用上一次响应中的 `pageToken` 来获取下一页数据。
- 如果未指定网络类型，默认使用 `public` 网络。
- 网关 URL 的格式为 `https://{GATEWAY_URL}/files/{cid}`。

## 相关资源：

- [Pinata 文档](https://docs.pinata.cloud)
- [API 密钥](https://app.pinata.cloud/developers/api-keys)
- [网关设置](https://docs.pinata.cloud/gateways)
- [x402 协议](https://docs.pinata.cloud/x402)
- [项目源代码（GitHub）](https://github.com/PinataCloud/pinata-api-skill)
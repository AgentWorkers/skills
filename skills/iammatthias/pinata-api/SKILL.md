---
name: pinata-api
description: Pinata IPFS API 用于文件存储、分组管理、网关控制、签名验证、X402支付处理以及文件向量化操作。
homepage: https://pinata.cloud
metadata: {"openclaw": {"emoji": "📌", "requires": {"env": ["PINATA_JWT", "PINATA_GATEWAY_URL"]}, "primaryEnv": "PINATA_JWT"}}
---
# Pinata API

这是一个用于访问Pinata IPFS存储服务的API。它支持上传文件、管理文件组、创建网关、添加签名、设置x402支付指令以及执行基于AI的向量搜索等功能。

**仓库链接：** https://github.com/PinataCloud/pinata-api-skill

## 认证

所有请求都必须包含以下头部信息：  
```
Authorization: Bearer $PINATA_JWT
```

**环境变量：**  
- `PINATA_JWT`（必填）：您的Pinata API JWT令牌。您可以在 [app.pinata.cloud/developers/api-keys](https://app.pinata.cloud/developers/api-keys) 获取令牌。  
- `PINATA_GATEWAY_URL`（必填）：您的Pinata网关域名（例如：`your-gateway.mypinata.cloud`）。请在 [app.pinata.cloud/gateway](https://app.pinata.cloud/gateway) 查找您的网关地址。  
- `PINATA_GATEWAY_KEY`（可选）：用于访问非关联于您Pinata账户的公共IPFS内容的网关密钥。详情请参阅 [网关访问控制](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys)。

### 测试认证  
```
GET https://api.pinata.cloud/data/testAuthentication
```

## 基本URL  
- **API地址：** `https://api.pinata.cloud`  
- **上传地址：** `https://uploads.pinata.cloud`  

## 常用参数  
- `{network}`：IPFS网络类型（默认为 `public` 或 `private`）  
- 分页查询使用 `limit` 和 `pageToken` 参数  

## 文件操作  
### 文件搜索  
```
GET https://api.pinata.cloud/v3/files/{network}
```  
查询参数（均为可选）：`name`、`cid`、`mimeType`、`limit`、`pageToken`  

### 通过ID获取文件  
```
GET https://api.pinata.cloud/v3/files/{network}/{id}
```  

### 更新文件元数据  
```
PUT https://api.pinata.cloud/v3/files/{network}/{id}
Content-Type: application/json
```  
请求体：  
```json
{
  "name": "new-name",
  "keyvalues": {"key": "value"}
}
```  
这两个字段均为可选。  

### 删除文件  
```
DELETE https://api.pinata.cloud/v3/files/{network}/{id}
```  

### 上传文件  
```
POST https://uploads.pinata.cloud/v3/files
Content-Type: multipart/form-data
```  
表单字段：  
- `file`（必填）：要上传的文件  
- `network`（可选）：`public` 或 `private`  
- `group_id`（可选）：文件所属的组  
- `keyvalues`（可选）：键值对形式的文件元数据（JSON字符串）  

## 文件组操作  
### 列出文件组  
```
GET https://api.pinata.cloud/v3/groups/{network}
```  
查询参数（均为可选）：`name`、`limit`、`pageToken`  

### 创建文件组  
```
POST https://api.pinata.cloud/v3/groups/{network}
Content-Type: application/json
```  
请求体：  
```json
{
  "name": "my-group"
}
```  

### 获取文件组信息  
```
GET https://api.pinata.cloud/v3/groups/{network}/{id}
```  

### 更新文件组信息  
```
PUT https://api.pinata.cloud/v3/groups/{network}/{id}
Content-Type: application/json
```  
请求体：  
```json
{
  "name": "updated-name"
}
```  

### 删除文件组  
```
DELETE https://api.pinata.cloud/v3/groups/{network}/{id}
```  

### 将文件添加到文件组  
```
PUT https://api.pinata.cloud/v3/groups/{network}/{groupId}/ids/{fileId}
```  

### 从文件组中删除文件  
```
DELETE https://api.pinata.cloud/v3/groups/{network}/{groupId}/ids/{fileId}
```  

## 网关与下载  
### 创建私有下载链接  
```
POST https://api.pinata.cloud/v3/files/private/download_link
Content-Type: application/json
```  
用于访问私有文件的临时签名URL。  
请求体：  
```json
{
  "url": "https://{PINATA_GATEWAY_URL}/files/{cid}",
  "expires": 600,
  "date": 1700000000,
  "method": "GET"
}
```  
- `url`（必填）：使用您的 `PINATA_GATEWAY_URL` 和文件CID生成的完整网关URL  
- `expires`（可选）：链接的有效时间（以秒为单位，默认为600秒）  
- `date`（必填）：当前的Unix时间戳（以秒为单位）  
- `method`（必填）：HTTP方法（通常为 `GET`）  

### 创建预签名上传链接  
```
POST https://uploads.pinata.cloud/v3/files/sign
Content-Type: application/json
```  
用于客户端上传的预签名URL（客户端无需提供JWT令牌）。  
请求体：  
```json
{
  "date": 1700000000,
  "expires": 3600
}
```  
可选字段：`max_file_size`（文件大小，单位：字节）、`allow_mime_types`（允许的文件类型数组）、`group_id`、`filename`、`keyvalues`  

## 签名  
EIP-712签名用于验证文件内容的真实性。  
### 添加签名  
```
POST https://api.pinata.cloud/v3/files/{network}/signature/{cid}
Content-Type: application/json
```  
请求体：  
```json
{
  "signature": "0x...",
  "address": "0x..."
}
```  

### 获取签名  
```
GET https://api.pinata.cloud/v3/files/{network}/signature/{cid}
```  

### 删除签名  
```
DELETE https://api.pinata.cloud/v3/files/{network}/signature/{cid}
```  

## 通过CID固定文件  
### 固定IPFS文件  
**仅限公共网络**：  
```
POST https://api.pinata.cloud/v3/files/public/pin_by_cid
Content-Type: application/json
```  
请求体：  
```json
{
  "cid": "bafybeig..."
}
```  
可选字段：`name`、`group_id`、`keyvalues`、`host_nodes`（多地址数组）  

### 查询文件固定请求  
```
GET https://api.pinata.cloud/v3/files/public/pin_by_cid
```  
查询参数（均为可选）：`order`（`ASC`/`DESC`）、`status`、`cid`、`limit`、`pageToken`  

### 取消文件固定请求  
```
DELETE https://api.pinata.cloud/v3/files/public/pin_by_cid/{id}
```  

## x402支付指令  
使用x402协议和USDC进行IPFS内容的货币化。  
**USDC合约地址：**  
- Base主网：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`  
- Base Sepolia（测试网）：`0x036CbD53842c5426634e7929541eC2318f3dCF7e`  
**注意：** `amount` 字段应使用最小的USDC单位（6位小数）。例如，$1.50 应输入为 `"1500000"`。  
### 创建支付指令  
```
POST https://api.pinata.cloud/v3/x402/payment_instructions
Content-Type: application/json
```  
请求体：  
```json
{
  "name": "My Payment",
  "description": "Pay to access this content",
  "payment_requirements": [
    {
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "pay_to": "0xWALLET_ADDRESS",
      "network": "base",
      "amount": "1500000"
    }
  ]
}
```  
- `name`（必填）：支付指令的显示名称  
- `description`（可选）：支付指令的描述  
- `payment_requirements`（必填）：包含 `asset`（USDC合约地址）、`pay_to`（收款钱包地址）、`network`（`base` 或 `base-sepolia`）、`amount`（支付金额，以字符串形式）的数组  

### 列出支付指令  
```
GET https://api.pinata.cloud/v3/x402/payment_instructions
```  
查询参数（均为可选）：`limit`、`pageToken`、`cid`、`name`、`id`  

### 获取支付指令信息  
```
GET https://api.pinata.cloud/v3/x402/payment_instructions/{id}
```  

### 删除支付指令  
```
DELETE https://api.pinata.cloud/v3/x402/payment_instructions/{id}
```  

### 将CID与支付指令关联  
```
PUT https://api.pinata.cloud/v3/x402/payment_instructions/{id}/cids/{cid}
```  

### 从支付指令中删除CID  
```
DELETE https://api.pinata.cloud/v3/x402/payment_instructions/{id}/cids/{cid}
```  

## 向量化（AI搜索）  
为文件生成向量嵌入，并在多个文件组中进行语义搜索。  
### 对文件进行向量化  
```
POST https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```  

### 删除文件向量  
```
DELETE https://uploads.pinata.cloud/v3/vectorize/files/{file_id}
```  

### 查询向量（语义搜索）  
```
POST https://uploads.pinata.cloud/v3/vectorize/groups/{group_id}/query
Content-Type: application/json
```  
请求体：  
```json
{
  "text": "search query here"
}
```  

## 注意事项：**  
- 所有JSON接口请求都必须设置 `Content-Type: application/json`。  
- 文件上传使用 `multipart/form-data` 格式；请勿手动设置 `Content-Type`。  
- 分页时使用上一次响应中的 `pageToken` 来获取下一页数据。  
- 如果未指定网络类型，默认使用 `public` 网络。  
- 网关URL的格式为 `https://{PINATA_GATEWAY_URL}/files/{cid}`。  

## 相关资源：  
- [Pinata文档](https://docs.pinata.cloud)  
- [API密钥](https://app.pinata.cloud/developers/api-keys)  
- [网关设置指南](https://docs.pinata.cloud/gateways)  
- [x402协议](https://docs.pinata.cloud/x402)  
- [项目源代码（GitHub）](https://github.com/PinataCloud/pinata-api-skill)
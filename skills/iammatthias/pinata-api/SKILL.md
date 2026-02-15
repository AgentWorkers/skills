# Pinata API 技能

该 API 提供了与 Pinata 的 IPFS 存储服务进行交互的功能，支持文件管理、群组管理、网关管理、签名生成、支付处理以及基于 AI 的向量搜索等功能。

仓库地址：https://github.com/PinataCloud/pinata-api-skill

## 设置

请设置以下环境变量：

- `PINATA_JWT`（必填）：您的 Pinata API JWT 令牌
- `GATEWAY_URL`（必填）：您的 Pinata 网关域名（例如：`your-gateway.mypinata.cloud`）
- `GATEWAY_KEY`（可选）：用于访问非关联于您 Pinata 账户的公共 IPFS 内容的网关密钥。在从更广泛的 IPFS 网络中获取内容时需要使用此密钥。详情请参阅 [网关访问控制](https://docs.pinata.cloud/gateways/gateway-access-controls#gateway-keys)。

## 可用功能

### 身份验证

- `testAuthentication()`：验证您的 Pinata JWT 令牌是否有效

### 文件操作

- `searchFiles({ network?, name?, cid?, mimeType?, limit?, pageToken? })`：搜索文件
- `getFileById({ network?, id })`：根据 ID 获取文件
- `updateFile({ network?, id, name?, keyvalues? })`：更新文件元数据
- `deleteFile({ network?, id })`：删除文件
- `uploadFile({ file, fileName, network?, group_id?, keyvalues? })`：上传文件

### 群组操作

- `listGroups({ network?, name?, limit?, pageToken? })`：列出群组
- `createGroup({ network?, name })`：创建群组
- `getGroup({ network?, id })`：根据 ID 获取群组信息
- `updateGroup({ network?, id, name })`：更新群组信息
- `deleteGroup({ network?, id })`：删除群组
- `addFileToGroup({ network?, groupId, fileId })`：将文件添加到群组
- `removeFileFromGroup({ network?, groupId, fileId })`：从群组中删除文件

### 网关与下载

- `createPrivateDownloadLink({ cid, expires? })`：创建临时下载链接
- `createSignedUploadUrl({ expires, max_file_size?, allow_mime_types?, group_id?, filename?, keyvalues? })`：生成带签名的上传 URL（适用于客户端上传）

### 签名操作

- `addSignature({ network?, cid, signature, address })`：添加 EIP-712 签名
- `getSignature({ network?, cid })`：获取指定 CID 的签名信息
- `deleteSignature({ network?, cid })`：删除签名

### 固定 IPFS 内容

- `pinByCid({ cid, name?, group_id?, keyvalues?, host_nodes? })`：固定指定的 IPFS 内容
- `queryPinRequests({ order?, status?, cid?, limit?, pageToken? })`：查询文件固定请求的状态
- `cancelPinRequest({ id })`：取消待处理的文件固定请求

### 支付指令

- `createPaymentInstruction({ name, pay_to, amount_usdc, network?, description? })`：创建支付指令
- `listPaymentInstructions({ limit?, pageToken?, cid?, name?, id? })`：列出所有支付指令
- `getPaymentInstruction({ id })`：获取特定支付指令的详细信息
- `deletePaymentInstruction({ id })`：删除支付指令
- `addCidToPaymentInstruction({ id, cid })`：将 CID 关联到支付指令
- `removeCidFromPaymentInstruction({ id, cid })`：从支付指令中移除 CID

### 向量化（AI 搜索）

- `vectorizeFile({ file_id })`：为文件生成向量嵌入
- `deleteFileVectors({ file_id })`：删除文件的向量嵌入
- `queryVectors({ group_id, text })`：在指定群组内进行语义搜索

## 参数说明

- `network`：IPFS 网络类型（默认值：`public` 或 `private`）
- `amount_usdc`：支付金额（以美元字符串表示，例如：`"1.50"` 表示 1.50 美元）
- `blockchain_network`：支付相关参数（默认值：`base` 或 `base-sepolia`）
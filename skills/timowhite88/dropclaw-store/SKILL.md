---
name: dropclaw-store
description: 通过 DropClaw x402 网关，将加密文件永久存储在 Monad 区块链上，并能够进行检索。
homepage: https://dropclaw.cloud
user-invocable: true
---
# DropClaw 商店 — 永久性加密文件存储服务

使用 AES-256-GCM 客户端加密技术和 x402 支付协议，将任何文件永久存储在区块链上。采用零知识（zero-knowledge）机制：服务器永远不会看到您的加密密钥。

## 快速参考

- **API 基础地址**：`https://dropclaw.cloud`
- **协议**：x402（HTTP 402 支付流程）
- **存储链**：Monad（chainId 143）
- **支持支付币种**：MON、SOL 或 Base USDC
- **费用**：存储费用约为 30 美元，另需支付网络手续费（gas）。文件检索免费。

## 如何存储文件

1. 将文件读取到缓冲区中。
2. 计算文件的 SHA-256 哈希值。
3. 使用 zlib deflate 对文件进行压缩。
4. 生成一个 32 字节的随机 AES 密钥和一个 12 字节的随机初始化向量（IV）。
5. 使用 AES-256-GCM 对文件进行加密，加密后的数据格式为：`[IV:12][AuthTag:16][Ciphertext]`。
6. 通过 POST 请求将加密后的文件数据（以 multipart 形式）发送到 `/vault/store` 端点（字段名：`file`）。
7. 系统会返回一个 402 响应，其中包含支付选项；请选择合适的存储链并完成支付。
8. 重新发送 POST 请求，并在请求头中添加 `X-PAYMENT: base64(JSON({ network, txHash })`。
9. **重要提示**：请同时将存储的文件和您的加密密钥保存在本地。

## 如何检索文件

1. 向 `/vault/retrieve/{fileId}` 发送 POST 请求，并在请求体中包含文件的 JSON 数据。
2. 系统会返回加密后的文件数据。
3. 从返回的数据中提取初始化向量（前 12 字节）和认证标签（后 16 字节），然后解密文件。
4. 使用保存的加密密钥，通过 AES-256-GCM 对文件进行解密。
5. 使用 zlib inflate 对解密后的文件进行解压缩。
6. 验证解密后的文件的 SHA-256 哈希值是否与原始文件的哈希值一致。

## 端点信息

| 方法        | 路径                | 认证方式            | 描述                                      |
|------------|------------------|------------------|-----------------------------------------|
| POST        | `/vault/store`          | x402              | 存储加密文件                              |
| POST        | `/vault/retrieve/{fileId}`     | 无                | 检索加密文件                              |
| GET        | `/vault/pricing?size={bytes}`     | 无                | 获取文件存储费用信息                         |
| GET        | `/.well-known/x402`       | 无                | x402 协议发现信息                         |
| GET        | `/dropclaw-skill.json`      | 无                | 完整的技能规范（JSON 格式）                         |
| GET        | `/claude-tools.json`      | 无                | Claude 工具定义                            |
| GET        | `/openai-tools.json`      | 无                | OpenAI 工具定义                            |

## MCP 服务器

**适用于 Claude 桌面应用/ Claude 代码集成：**
```
claude mcp add dropclaw -- node /path/to/mcp/index.js
```

**安装 SDK：**  
使用 npm：`npm i dropclaw`  
或使用 pip：`pip install dropclaw`

## 支持的支付链**

- **Monad**（eip155:143）——支持 MON 原生支付  
- **Solana**（solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp）——支持 SOL 原生支付  
- **Base**（eip155:8453）——支持 USDC 支付  

## 重要说明：

- 加密密钥是在客户端生成的，绝不会发送到服务器。
- 没有您的密钥，任何人都无法解密文件。
- 所有费用的 50% 会用于 FARNS 代币的回购计划。
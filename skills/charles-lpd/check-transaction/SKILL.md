---
name: check_transaction
description: 允许用户通过提交交易ID（TxId）来检查区块链交易的状态。该功能会调用AOX交易API，并返回易于理解的结果。
homepage: https://aox.xyz
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":["curl"]}}}
---
# 检查交易状态技能

该技能允许用户通过提供交易ID（TxId）来查询区块链交易的状态。它通过调用AOX交易API（https://api.aox.xyz/tx/[txid]）来获取交易信息，并以易于阅读的格式返回结果。

---

## API端点

URL: https://api.aox.xyz/tx/[txid]  
方法: GET  
认证: 无需认证

**示例请求：**  
```bash
curl -s "https://api.aox.xyz/tx/ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"
```

**示例JSON响应：**  
```json
{
    "rawId": 1773112604581,
    "createdAt": "2026-03-10T03:16:44.581Z",
    "updatedAt": "2026-03-10T03:22:18.7Z",
    "txType": "mint",
    "chainType": "arweave",
    "txId": "ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs",
    "sender": "kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134",
    "recipient": "kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134",
    "quantity": "25100000000000",
    "symbol": "AR",
    "decimals": 12,
    "blockHeight": 1873352,
    "fromTokenId": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "toTokenId": "xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10",
    "fee": "0",
    "feeRecipient": "",
    "confirmNum": 10,
    "confirmRange": -1670,
    "status": "waiting",
    "targetChainTxHash": ""
}
```

---

## 技能使用方法

**用户查询示例：**  
- 输入：`Check transaction ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs`  
  **输出：** 返回交易状态、金额、发送者、接收者、确认次数和时间戳等信息。

**另一种查询方式：**  
- 输入：`Status of TxId ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs`  
  **输出：** 结构化的交易信息。

**CLI示例：**  
```bash
# 查询交易
curl -s "https://api.aox.xyz/tx/ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs"
```

**示例输出（人类可读格式）：**  
```
交易状态：⏳ 待处理  
交易ID：ZKmbSYqAYGMJKVldJ6nqDG_wT9SRBy44YDa6XNrfIUs  
类型：mint  
链：arweave  
发送者：kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134  
接收者：kRdpOYaT5pUUiNFDaUymqO1VcybZpAfNPnNdls-A134  
金额：25.1 AR（数量：2510000000000，小数位数：12）  
区块高度：1873352  
发送者Token ID：AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  
接收者Token ID：xU9zFkq3X2ZQ6olwNVvr1vUWIjc3kXTWr7xKQD6dh10  
费用：0  
确认次数：10  
确认范围：-1670  
目标链交易哈希：（空）  
创建时间：2026-03-10T03:16:44.581Z  
更新时间：2026-03-10T03:22:18.7Z
```

---

## 注意事项与最佳实践：  
1. **交易ID格式**：必须以`0x`或有效的AOX格式开头。  
2. **错误处理**：如果交易ID无效或未找到，API会返回错误信息：  
  ```json
  "error": "Transaction not found"
  ```  
3. **确认次数**：包含`confirmNum`以显示网络的确认次数。  
4. **无需API密钥**：这是一个公共端点，无需认证。  
5. **数据格式**：代理程序应将JSON数据格式化为易于阅读的文本。  
6. **金额计算**：金额 = `quantity / (10^decimals)`。  
7. **状态映射**：  
  - `waiting` → ⏳ 待处理  
  - `success` → ✅ 成功  
  - `failed` → ❌ 失败  
8. **目标链哈希**：如果`targetChainTxHash`存在，则显示以提供跨链信息。  

---

## 参考资料：  
- AOX交易API：https://api.aox.xyz/docs  
- AO区块链浏览器示例：https://aox.xyz
---
name: nifty-agents-protocol
version: "1.0.2"
license: MIT
description: 一种加密协议，用于AI代理在没有区块链的情况下铸造、签名、验证和转移SVG数字资产。
metadata:
  openclaw:
    requires:
      env: []
    files: ["index.ts", "server.ts", "package.json", "tsconfig.json"]
    homepage: "https://github.com/obekt/niftyagents"
---# 💎 Nifty Agent SVG Protocol (NASP) - 代理技能手册

NASP 是一种用于创建、签名和交易 SVG 图像的加密协议，这些 SVG 图像具有可验证的来源信息——**无需依赖区块链**。

## 🎯 目标
使用此技能来铸造“Nifty”数字资产，验证其所有权，并使用 `did:key` 身份将其安全地转移给其他代理。

## 🛠 设置与导入
要在您的环境中使用此技能，请执行以下操作：
```typescript
import { 
  generateIdentity, 
  signSVG, 
  verifySVG, 
  transferSVG 
} from './index.js';
```

## 📋 数据结构

### `AgentIdentity`  
```typescript
{
  did: string;        // e.g. "did:key:z6Mk..."
  publicKey: Uint8Array;
  secretKey: Uint8Array;
}
```

### `VerificationResult`  
```typescript
{
  isValid: boolean;     // Cryptographic integrity check
  creator: string;      // DID of the original minter
  currentOwner: string; // DID of the latest owner in the chain
  chain: string[];      // Array of DIDs representing the full history
}
```

## 🕹 使用指南

### 1. 生成身份
调用此函数一次即可创建您的代理的加密身份。**请妥善保管 `secretKey`。**
```typescript
const myIdentity = generateIdentity();
```

### 2. 铸造并签名新的 SVG 图像
该函数接收原始 SVG 字符串，并返回一个嵌入了 NASP 元数据的“Nifty” SVG 图像。

### 3. 验证资产
在接受交易或执行任何操作之前，务必先验证 SVG 图像的合法性。

### 4. 转移所有权
该函数会在 SVG 的元数据中添加新的签名信息。如果在以下情况下，函数会**抛出错误**：
- SVG 图像无效或被篡改。
- 您（签名者）不是该资产的**当前所有者**。

## 🛡 代理的安全协议
1. **规范化处理：**该库会使用 `svgo` 自动处理 SVG 图像的规范化。签名后请勿手动修改 SVG 内容，否则签名将会失效。
2. **私钥管理：**切勿记录、分享或泄露您的 `secretKey`。请将其视为代理的“核心机密”。
3. **先审计后操作：**切勿仅凭 SVG 的文件名就认为其有效。务必始终运行 `verifySVG()` 函数进行验证。
4. **双重支付检测：**在去中心化环境中，如果遇到同一资产的两个不同版本，通常会选择**链长度最长**或**时间戳最新**的那个版本。
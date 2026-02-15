---
name: self-xyz
description: "**Integrate Self (self.xyz)** — 这是一个以隐私保护为核心的设计理念的身份验证协议，利用零知识证明（zero-knowledge proofs）技术来验证用户的护照和身份证件。适用于以下场景：  
- 当用户提及 “Self 协议”、“Self 身份验证”、“self.xyz”、“护照验证”、“零知识身份验证”、“SelfAppBuilder”、“SelfBackendVerifier”、“SelfVerificationRoot” 时；  
- 当用户希望实现保护隐私的客户身份验证（KYC）、年龄验证、国籍检查、OFAC（美国外国资产控制办公室）筛查，或利用真实身份文件进行抗伪冒（Sybil resistance）功能时。  

该方案涵盖以下关键组成部分：  
1. **前端集成**：支持通过二维码（QR code）进行身份验证；  
2. **后端验证**：利用后端服务对用户提供的身份信息进行验证；  
3. **链上智能合约验证**：在 Celo 区块链上通过智能合约完成身份验证流程。"
---

# 自我协议集成（Self Protocol Integration）

Self 允许用户使用零知识证明（zero-knowledge proofs）来验证其身份信息（年龄、国籍、人类身份），而无需泄露任何个人数据。用户只需在 Self 移动应用中扫描其身份证件的 NFC 标签，然后将零知识证明分享给您的应用。

## 快速入门（Next.js 非链式集成）

### 1. 安装

```bash
npm install @selfxyz/qrcode @selfxyz/core
```

### 2. 前端——二维码组件（Frontend – QR Code Component）

```tsx
"use client";
import { SelfQRcodeWrapper, SelfAppBuilder } from "@selfxyz/qrcode";

export default function VerifyIdentity({ userId }: { userId: string }) {
  const selfApp = new SelfAppBuilder({
    appName: "My App",
    scope: "my-app-scope",
    endpoint: "https://yourapp.com/api/verify",
    endpointType: "https",
    userId,
    userIdType: "hex",
    disclosures: {
      minimumAge: 18,
    },
  }).build();

  return (
    <SelfQRcodeWrapper
      selfApp={selfApp}
      onSuccess={() => console.log("Verified")}
      type="websocket"
      darkMode={false}
    />
  );
}
```

### 3. 后端——验证端点（Backend – Verification Endpoint）

```ts
// app/api/verify/route.ts
import { SelfBackendVerifier, DefaultConfigStore } from "@selfxyz/core";

export async function POST(req: Request) {
  const { proof, publicSignals } = await req.json();

  const verifier = new SelfBackendVerifier(
    "my-app-scope",                    // must match frontend scope
    "https://yourapp.com/api/verify",  // must match frontend endpoint
    true,                              // true = accept mock passports (dev only)
    null,                              // allowedIds (null = all)
    new DefaultConfigStore({           // must match frontend disclosures
      minimumAge: 18,
    })
  );

  const result = await verifier.verify(proof, publicSignals);

  return Response.json({
    verified: result.isValid,
    nationality: result.credentialSubject?.nationality,
  });
}
```

## 集成模式（Integration Patterns）

| 集成模式 | 使用场景 | `endpoint` | `endpointType` |
|---------|------------|------------|----------------|
| **非链式**（后端） | Web 应用、API 等大多数场景 | 您的 API 地址 | `"https"` 或 `"https-staging"` |
| **链式**（智能合约） | DeFi、代币发放、空投等 | 智能合约地址（小写） | `"celo"` 或 `"celo-staging"` |
| **深度链接** | 以移动设备为主的交互流程 | 您的 API 地址 | `"https"` |

- **非链式**：实现速度最快。证明数据发送到后端，由服务器端进行验证。
- **链式**：证明数据由 Celo 智能合约进行验证。适用于无需信任或无需授权的场景。
- **深度链接**：适用于移动用户——直接打开 Self 应用而无需扫描二维码。详情请参阅 `references/frontend.md`。

## 重要注意事项（Critical Gotchas）

1. **配置匹配是必须的**——前端的配置信息必须与后端/智能合约的验证配置完全一致。年龄阈值、国家列表或 OFAC 设置不匹配会导致验证失败。
2. **智能合约地址必须使用小写**——前端请求的地址必须为小写格式。请使用 `.toLowerCase()` 函数进行转换。
3. **国家代码遵循 ISO 3 字母标准**——例如 `"USA"`、`IRN`、`PRK`。排除列表中最多包含 40 个国家。
4. **模拟身份证件仅用于测试环境**——在后端设置 `mockPassport: true`，或使用 `"celo-staging"` 端点类型。真实身份证件需要使用主网环境。创建模拟身份证件的方法：打开 Self 应用，点击 “Passport” 按钮 5 次。进行模拟测试时需关闭 OFAC 功能。
5. **版本要求**——`@selfxyz/core` 版本必须大于或等于 1.1.0-beta.1。
6. **身份证明类型**——`1` 表示护照，`2` 表示生物识别身份证。必须通过 `allowedIds` 显式指定允许的身份证明类型。
7. **唯一性保障**——在链式环境中，身份证明的哈希值会与智能合约地址结合使用，以防止跨合约的重复验证。
8. **端点必须可公开访问**——Self 应用会直接将证明数据发送到您的端点。本地开发时请使用 ngrok 服务。
9. **常见错误**：
  - `ScopeMismatch`：表示身份证明的哈希值与地址不匹配或地址格式不正确。
  - `Invalid 'to' Address`：表示使用的端点类型错误（例如使用错误的 `endpointType`，如 celo 或 https）。
  - `InvalidIdentityCommitmentRoot`：在测试环境中使用了真实护照（应使用主网环境）。
  - `Invalid Config ID`：在主网环境中使用了模拟身份证件（应使用测试环境）。

## 已部署的智能合约（Celo）

| 网络 | 地址 |
|---------|---------|
| **主网**（Mainnet） | `0xe57F4773bd9c9d8b6Cd70431117d353298B9f5BF` |
| **Sepolia**（测试网） | `0x16ECBA51e18a4a7e61fdC417f0d47AFEeDfbed74` |
| **Sepolia 测试网**（Staging） | `0x68c931C9a534D37aa78094877F46fE46a49F1A51` |

## 参考资料（References）

如需深入了解集成细节，请参阅以下文档：

- **`references/frontend.md`**：`SelfAppBuilder` 的完整配置信息、`SelfQRcodeWrapper` 的属性设置、使用 `getUniversalLink` 进行深度链接的方法以及信息披露选项。
- **`references/backend.md`**：`SelfBackendVerifier` 构造函数的详细信息、`DefaultConfigStore` 与 `InMemoryConfigStore` 的区别、验证结果的数据结构以及动态配置设置。
- **`references/contracts.md`**：`SelfVerificationRoot` 的继承机制、与 Hub V2 的交互方式、`setVerificationConfigV2`、`customVerificationHook`、`getConfigId` 以及 `userDefinedData` 的使用方法。
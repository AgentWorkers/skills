---
name: soulprint
description: "Soulprint：用于AI代理的去中心化身份验证系统，版本0.6.4——采用区块链优先的架构（不依赖libp2p）；状态数据存储在Base Sepolia区块链上，验证节点部署在Railway网络上，使用Circom技术进行零知识证明（ZK Proof）以及本地验证。适用场景包括：验证机器人背后是否为真实人类、生成保护隐私的身份证明、运行验证节点、为API或MCP服务器添加身份验证中间件、检查机器人的信誉评分，以及设置可配置的信任阈值。"
homepage: https://soulprint.digital
metadata:
  {
    "openclaw":
      {
        "emoji": "🌀",
        "requires": { "bins": ["node", "npx"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "soulprint",
              "bins": ["soulprint"],
              "label": "Install Soulprint CLI (npm)",
            },
          ],
      },
  }
---
# Soulprint — 为AI代理提供去中心化的身份验证服务

Soulprint通过使用保护隐私的零知识证明（ZK proofs）来验证任何AI机器人背后确实是一个真实的人类——无需任何中央权威机构，也无需上传生物特征数据到云端。所有身份信息都存储在Base Sepolia区块链上。

**GitHub:** https://github.com/manuelariasfz/soulprint  
**npm:** https://www.npmjs.com/package/soulprint-network  
**文档:** https://soulprint.digital  
**网络架构：** 在Railway的Base Sepolia测试网络上运行4个验证节点  
**版本：** v0.6.4  

---

## 架构（v0.6.4 — 以区块链为核心，支持本地ZK验证）

**在Base Sepolia区块链上的合约：**  
- `PeerRegistry`: `0x452fb66159dFCfC13f2fD9627aA4c56886BfB15b`  
- `NullifierRegistry`：（待部署中 — 需要测试网ETH）  
- `ReputationRegistry`：（待部署中 — 需要测试网ETH）  
- `ProtocolThresholds`: `0xD8f78d65b35806101672A49801b57F743f2D2ab1`  
- `MCPRegistry`: `0x59EA3c8f60ecbAe22B4c323A8dDc2b0BCd9D3C2a`  

---

## 使用场景  

✅ **适用于以下场景：**  
- “为AI代理验证我的身份”  
- “运行Soulprint验证节点”  
- “将身份验证功能添加到我的MCP服务器或API中”  
- “检查机器人的声誉分数或DID（Digital Identity）”  
- “根据哥伦比亚的公民身份证（cédula）生成隐私证明”  
- “验证公民身份证的真实性（通过哥伦比亚国家登记机构）”  
- “发行或验证SPT（Soulprint Token）”  

❌ **不适用以下场景：**  
- 远程存储或传输生物特征数据（Soulprint的所有处理完全在本地完成）  
- 验证来自尚未支持的国家的人士的身份（目前仅支持哥伦比亚）  

---

## 快速入门  

### 1. 验证您的身份（一次性操作）  

---

### 2. 运行验证节点  

---

**节点API：**  

---

## 集成到您的API中  

### MCP服务器（3行代码示例）  

---

## 使用Express/Fastify框架进行集成  

---

## 信任评分（0–100分）  

| 组件 | 最高分数 | 来源 |
|---|---|---|
| 电子邮件验证 | 8 | 依据：电子邮件凭证 |
| 手机号码验证 | 12 | 依据：手机号码凭证 |
| GitHub账户 | 16 | 依据：GitHub账户凭证 |
- 文档OCR识别 | 20 | 依据：文档凭证 |
- 面部匹配 | 16 | 依据：面部匹配结果 |
- 生物特征验证 | 8 | 依据：生物特征数据凭证 |
- 机器人声誉 | 20 | 依据：验证节点的证明结果 |
| **总分** | **100** | |

---

## 协议常量（通过`ProtocolThresholds`在链上设置）  

| 常量 | 值 |
|---|---|
| `SCORE_FLOOR` | 65 |
| `VERIFIED SCORE_FLOOR` | 52 |
| `MIN_ATTESTER SCORE` | 65 |
| `DEFAULT_REPUTATION` | 10 |
| `IDENTITY_MAX` | 80 |
| `REPUTATION_MAX` | 20 |

---

## 国家支持情况  

| 国家 | 需要的验证方式 | 状态 |
|---|---|---|
| 🇨🇴 哥伦比亚 | 哥伦比亚公民身份证（cédula） | ✅ 完整支持（OCR识别 + MRZ（机器签名）+ 面部匹配 + 国家登记机构验证） |
| 其他国家 | — | 🚧 正在规划中 |

---

## npm包  

| 包名 | 版本 | 功能 |
|---|---|---|
| `soulprint-network` | 0.6.4 | 验证节点（包含HTTP接口和区块链客户端） |
| `soulprint-mcp` | 最新版本 | MCP中间件 |
| `soulprint-express` | 最新版本 | Express/Fastify框架的中间件 |
| `soulprint-core` | 最新版本 | 负责处理DID、Token及协议常量 |
| `soulprint-zkp` | 最新版本 | 提供ZK证明功能（使用Circom和snarkjs技术） |
| `soulprint-verify` | 最新版本 | 提供OCR识别和面部匹配功能 |
| `soulprint` | 最新版本 | 提供命令行工具（CLI） |

---

## 与mcp-colombia的集成  

`mcp-colombia-hub@1.3.0`版本原生支持Soulprint，无需额外配置：  
- `soulprint_status`工具可直接在mcp-colombia中使用，用于检查链上的身份和声誉信息；  
- 申请工作时，要求Soulprint评分≥40分；  
- 实时验证节点地址：`https://soulprint-node-production.up.railway.app`  

### 一起安装这两个包  

---

完成身份验证后，您的SPT令牌将自动在mcp-colombia的所有工具中生效。
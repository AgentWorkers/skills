---
name: soulprint
description: "**Soulprint去中心化身份验证系统——适用于AI代理**  
**版本：v0.4.3**  
**基于Sepolia区块链的PeerRegistry机制：**  
每个节点通过智能合约自动发现其他节点，并在启动时将自己的DID（Decentralized Identity）及MultiAddress信息进行注册。通过`/network/peers`接口可以查看网络中的所有节点。  
**系统特性：**  
- **可配置的协议阈值（ProtocolThresholds）**：支持动态调整信任策略。  
- **ZK证明（ZK Proof）**：采用Circom技术实现数据的不可篡改验证。  
- **MCPRegistry**：用于管理经过验证的MCP（Multi-Controller Agents）。  
**适用场景：**  
- 证明AI代理背后确实是人类操作者；  
- 发布保护用户隐私的身份验证结果；  
- 运行节点验证器；  
- 为API或MCP服务器添加身份验证中间件；  
- 检查AI代理的信誉评分；  
- 构建去中心化的AI代理网络；  
- 实施可配置的协议级信任机制。"
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

Soulprint通过保护隐私的验证机制，确保任何AI机器人背后都站着真实的人类用户——无需依赖中央权威机构，也无需上传生物特征数据到云端。所有验证过程都在设备本地完成。

**GitHub仓库：** https://github.com/manuelariasfz/soulprint  
**npm包：** https://www.npmjs.com/package/soulprint  
**文档：** https://soulprint.digital/docs/

---

## 使用场景

✅ 当您需要以下操作时，请使用Soulprint：
- **验证AI代理的身份**  
- **运行Soulprint验证节点**  
- **将身份验证功能添加到您的MCP服务器或API中**  
- **检查机器人或DID的信誉分数**  
- **根据哥伦比亚公民身份证（Cédula）生成隐私证明**  
- **发行或验证SPT（Soulprint Token）**  
- **设置不可降低的最低信任阈值**  

❌ 请勿在以下情况下使用Soulprint：
- **远程存储或传输生物特征数据**（Soulprint的所有操作均在本地完成）  
- **验证来自尚未支持该服务的国家的用户身份**  

---

## 快速入门

### 1. 验证您的身份（仅一次）

```bash
# Install local dependencies (OCR + face recognition) — only needed once
npx soulprint install-deps

# Run interactive verification — all local, nothing uploaded
npx soulprint verify-me
# Scans document, runs local face match, generates privacy proof
# Saves identity token to local storage
```

### 2. 显示您的Token

```bash
npx soulprint show
# Output: DID, trust score (0-100), credentials, expiry, proof hash
```

### 3. 续期Token

```bash
npx soulprint renew
```

### 4. 运行验证节点

```bash
# Starts HTTP (port 4888) + P2P network (port 6888) simultaneously
npx soulprint node
```

**节点API端点：**  
```
GET  /info                — node info and network stats
GET  /network/stats       — live stats for web visualization (total_peers, verified_identities, uptime)
GET  /protocol            — immutable protocol constants (floors, thresholds)
GET  /health              — code integrity hash + governance status
POST /verify              — verify proof and register anti-replay hash
POST /token/renew         — auto-renew SPT (pre-emptive 1h / grace 7 days)
POST /challenge           — ZK challenge-response peer integrity check
POST /reputation/attest   — issue bot reputation attestation (+1 / -1)
GET  /reputation/:did     — get current bot reputation score (0-20)
POST /peers/register      — register peer (runs challenge-response first, then auto-dials P2P)
GET  /mcps/verified       — list verified MCPs from on-chain registry
GET  /mcps/status/:addr   — check a specific MCP's verification status
```

**自动连接节点（WSL2 / Docker / 云环境）：**  
```bash
SOULPRINT_BOOTSTRAP_HTTP=http://node1:4888,http://node2:4888 \
  node packages/network/dist/server.js
# → auto-registers HTTP peers on startup (bypasses mDNS which requires multicast)
```

---

## 协议常量（不可更改，由P2P网络强制执行）

网络中的所有验证节点都共享这些常量。这些常量通过以下两种方式确保其不可被修改：
1. **`Object.freeze()`** — 防止程序运行时对其进行修改  
2. **P2P网络哈希**：`PROTOCOL_HASH`是根据所有常量计算得出的。任何修改都会导致哈希值发生变化，从而被整个网络拒绝。  
```typescript
import { PROTOCOL_HASH, isProtocolHashCompatible } from 'soulprint-core';

// Each node computes this at startup from its actual PROTOCOL values
PROTOCOL_HASH  // "dfe1ccca1270ec86f93308dc4b981bab1d6bd74bdcc334059f4380b407ca07ca"

// P2P enforcement: peer registration validates hash
// POST /peers/register { url, protocol_hash } → 409 if mismatch
// Gossip headers: X-Protocol-Hash validated on receive → rejected if different
```

| 常量 | 值 | 含义 |
|---|---|---|
| `PROTOCOL_HASH` | `dfe1ccca...` | 所有常量的SHA-256哈希值；不匹配则会被网络隔离 |
| `SCORE_FLOOR` | **65** | 任何服务可设置的最低分数阈值；低于此值的分数会被自动限制为65 |
| `VERIFIEDSCORE_FLOOR` | **52** | 经过验证的身份（附带文档）的最低分数 |
| `MIN_ATTESTER SCORE` | **65** | 发行信誉证明所需的最低分数 |
| `VERIFY_RETRY_MAX` | **3** | 连接验证节点时的最大重试次数 |
| `VERIFY_RETRY_BASE_MS` | **500** | 重试间隔时间（每次尝试后翻倍） |
| `DEFAULT_REPUTATION` | **10** | 新代理的初始信誉分数 |
| `IDENTITY_MAX` | **80** | 身份子分数的最大值 |
| `REPUTATION_MAX` | **20** | 最高信誉分数 |

**检查节点的当前常量值：**  
```bash
curl http://localhost:4888/protocol
# Returns all constants + immutable: true
```

---

## 集成到您的API中

### MCP服务器（3行代码）

```typescript
import { requireSoulprint } from "soulprint-mcp";

server.tool("premium-tool", requireSoulprint({ minScore: 80 }), async (args, ctx) => {
  const { did, score } = ctx.soulprint;
  // only reachable if identity token is valid and score >= 80
  // Note: minScore is auto-clamped to 65 minimum (protocol floor)
});
```

`minScore`选项会被自动限制在协议规定的最低阈值：
- `requireSoulprint({ minScore: 40 })` → 实际使用值为65  
- `requireSoulprint({ minScore: 80 })` → 使用值为80（已高于最低阈值）

### 带有验证功能的MCP服务器（包含重试机制）

```typescript
import { requireSoulprint } from "soulprint-mcp";

// Verifies token locally AND confirms with a remote validator node.
// If the validator is temporarily down, retries up to 3 times with backoff,
// then falls back to offline mode automatically.
server.tool(
  "secure-tool",
  requireSoulprint({
    minScore:     80,
    validatorUrl: "http://localhost:4888",
  }),
  async (args, ctx) => {
    const { did, score, reputation } = ctx.soulprint;
    return { content: [{ type: "text", text: `Verified: ${did}` }] };
  }
);
```

### Express / Fastify中间件

```typescript
import { soulprintMiddleware } from "soulprint-express";

app.use(soulprintMiddleware({ minScore: 65 }));

app.get("/protected", (req, res) => {
  const { did, score } = req.soulprint;
  res.json({ did, score });
});
```

Token的获取顺序如下：
1. MCP能力头部：`x-soulprint-token`  
2. HTTP头部：`X-Soulprint`  
3. 承载者授权头部  

---

## 信任分数（0–100分）

| 验证方式 | 最高分数 | 来源 |
|---|---|---|
| 电子邮件验证 | 8 | 验证依据：电子邮件 |
| 手机验证 | 12 | 验证依据：手机 |
| GitHub账户 | 16 | 验证依据：GitHub账户 |
| 文档OCR识别 | 20 | 验证依据：文档 |
| 面部匹配 | 16 | 验证依据：面部识别 |
| 生物特征验证 | 8 | 验证依据：生物特征数据 |
| 机器人信誉 | 20 | 验证依据：验证机构的证明 |

**所有验证方式的最低分数要求（由所有验证节点强制执行）：**  
使用`requireSoulprint()`的服务的最低分数阈值将被限制为65分。  
已验证身份的用户，其总分数永远不会低于52分（即使受到信誉攻击）。  

**默认机器人信誉分数：** 10分（中立状态）。  

---

## 重试逻辑

所有对验证节点的请求在失败时都会自动重试：  
```
Attempt 1  → immediate
Attempt 2  → wait 500ms
Attempt 3  → wait 1000ms
           → fall back to offline signature-only verification
```

当设置了`validatorUrl`时，`requireSoulprint()`会自动处理重试逻辑。无需额外配置，因为行为由协议常量决定。  

## 证书验证器（开源，内置）

每个验证节点都具备真实的证书验证功能，大多数情况下无需API密钥：

### 电子邮件验证（nodemailer – SMTP）

```bash
# 1. Request OTP
curl -X POST http://localhost:4888/credentials/email/start \
  -d '{"did":"did:soulprint:abc...","email":"user@example.com"}'
# → { sessionId, message: "OTP sent to your email" }

# 2. Verify OTP (6-digit code from email)
curl -X POST http://localhost:4888/credentials/email/verify \
  -d '{"sessionId":"...","otp":"123456"}'
# → { credential: "EmailVerified", did, attestation }
```  
配置参数：`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`（开发环境使用Ethereal库，无需额外配置）

### 手机验证（TOTP – 无需短信，无需API密钥）

```bash
# 1. Get TOTP setup URI
curl -X POST http://localhost:4888/credentials/phone/start \
  -d '{"did":"did:soulprint:abc...","phone":"+573001234567"}'
# → { sessionId, totpUri, instructions }
# User scans totpUri QR with Google Authenticator / Authy / Aegis

# 2. Verify 6-digit TOTP code
curl -X POST http://localhost:4888/credentials/phone/verify \
  -d '{"sessionId":"...","code":"123456"}'
# → { credential: "PhoneVerified", did, attestation }
```  
不依赖外部服务，遵循RFC 6238 TOTP标准，支持离线验证。

### GitHub账户验证（OAuth）

```bash
# Redirect user to GitHub OAuth
GET http://localhost:4888/credentials/github/start?did=did:soulprint:abc...
# → Redirects to github.com/login/oauth/authorize
# GitHub redirects back to /credentials/github/callback
# → { credential: "GitHubLinked", did, github: { login }, attestation }
```  
配置参数：`GITHUB_CLIENT_ID`, `GITHUB_CLIENT_SECRET`, `SOULPRINT_BASE_URL`  
创建OAuth应用：https://github.com/settings/applications/new  

### 生物特征验证（内置）

用户完成`npx soulprint verify-me`命令后，系统会自动进行生物特征验证。  
无需单独的API端点，验证结果与身份证明哈希值关联。  

---

## 防止刷分行为

Soulprint的信誉系统可防止刷分行为：
**如果机器人尝试刷分，其获得的分数会自动变为-1分。**

### 规则（不可更改，由所有验证节点强制执行）

| 规则 | 限制 | 后果 |
|---|---|---|
| 每日得分上限 | 每个DID每天最多+1分 | 检测到刷分行为时扣1分 |
| 每周得分上限 | 每周最多+2分 | 检测到刷分行为时扣1分 |
| 来源相同的服务 | 每天同一来源最多奖励1分 | 检测到刷分行为时扣1分 |
| 会话时长 | 会话时长至少30秒 | 会话时间过短无法获得奖励 |
| 工具多样性 | 使用的工具必须至少4种不同 | 使用工具过于单一会被阻止 |
| 行为模式 | 调用间隔的方差小于平均值的10% | 检测到重复行为时扣1分 |
| 新DID的试用期 | 新DID在获得分数前需要至少2次验证 | 首7天内得分为0分 |

### 刷分行为与正常使用的区别  
```
❌ Farming (detected):
   - Call tool A 3x, tool B 3x, tool C 3x every 60 seconds
   - Regular 2-second intervals (robotic pattern)
   - Same service rewards same DID multiple times/day

✅ Real usage (rewarded):
   - Session lasts > 30 seconds
   - Uses 4+ different tools naturally
   - Variable time between actions
   - Different services on different days
```

---

- **验证机制：** 采用本地电路和844个逻辑门，基于snarkjs的先进验证方案  
- **验证时间：** 本地处理约564毫秒  
- **防重放机制：** 每人拥有唯一的身份哈希值，防止重复注册  
- **隐私保护：** 所有敏感信息仅保存在设备上，仅验证结果及其公开哈希值会被共享  

---

## P2P网络

验证节点组成一个点对点的网状网络：  
```
libp2p v2.10:
  TCP transport + encrypted channels + stream multiplexing
  Kademlia DHT (peer routing)
  GossipSub (attestation broadcast — topic: soulprint-attestations-v1)
  mDNS (local network auto-discovery)
```

节点在连接时会检查彼此的协议兼容性。协议版本不同或分数设置异常的节点会被自动排除在网络之外。  
验证结果通过GossipSub协议传播；对于旧版本节点，使用HTTP作为备用方式。  

---

## 挑战-响应机制（v0.3.7）

在接纳新节点之前，节点会发送两个ZK证明：
- 一个**已知有效的证明**（公共协议向量）——节点必须返回`true`  
- 一个**随机生成的无效证明**（每次挑战都不同）——节点必须返回`false`  
节点会使用其Ed25519密钥对响应进行签名，以此检测：
- 使用ZK绕过机制的节点（始终返回`true`的节点）  
- 伪造身份的节点  
- 预先计算好的响应缓存  
- 重放攻击  

任何违反规则的节点都会被HTTP 403错误拒绝。  

## SPT自动续期（v0.3.6）

Token的有效期为24小时，会自动续期：
- 如果剩余时间少于1小时，会通过`POST /token/renew`进行自动续期  
- 如果Token已过期但仍在7天内，会有宽限期进行续期  
Express/MCP中间件会在设置`nodeUrl`时自动处理续期逻辑。  

## 相关npm包

| 包名 | 版本 | 功能 |
|---|---|---|
| `soulprint` | 最新版本 | 命令行工具（`npx soulprint verify-me`） |
| `soulprint-core` | 0.1.10 | DID管理、Token处理、协议常量、防刷分机制 |
| `soulprint-verify` | 0.1.6 | OCR识别+面部匹配（按需）、生物特征验证 |
| `soulprint-zkp` | 0.1.5 | ZK证明（使用Circom和snarkjs）、面部识别密钥 |
| `soulprint-network` | 0.4.1 | HTTP验证节点、P2P网络、协议阈值管理 |
| `soulprint-mcp` | 0.1.5 | MCP中间件，包含自动限制和重试机制 |
| `soulprint-express` | 0.1.4 | Express/Fastify中间件 |

---

## 国家支持情况

| 国家 | 需要的验证方式 | 支持状态 |
|---|---|---|
| 🇨🇴 哥伦比亚 | 哥伦比亚公民身份证（Cédula de Ciudadanía） | 完全支持（OCR识别+MRZ验证+面部匹配） |
| 🇲🇽 墨西哥 | INE/CURP证书 | 部分支持 |
| 🇦🇷 阿根廷 | DNI证书 | 部分支持 |
| 🇻🇪 委内瑞拉 | Cédula V/E证书 | 部分支持 |
| 🇵🇪 秘鲁 | DNI证书 | 部分支持 |
| 🇧🇷 巴西 | CPF证书 | 部分支持 |
| 🇨🇱 智利 | RUN系统 | 部分支持 |

**如需添加您的国家，请参阅[贡献指南](https://github.com/manuelariasfz/soulprint/blob/main/CONTRIBUTING.md)。**
---
name: soulprint
description: "**Soulprint：用于AI代理的去中心化身份验证系统**  
**适用场景：**  
- 证明机器人背后确实是一个真实的人类；  
- 发布保护隐私的身份证明；  
- 运行验证节点；  
- 为API或MCP服务器添加身份验证中间件；  
- 检查机器人的声誉评分；  
- 强制执行协议级别的不可篡改信任阈值；  
- 在无需区块链的情况下运行BFT（拜占庭容错）P2P共识机制。  
**支持的身份验证方式：**  
- 支持哥伦比亚的**cédula**（完整版）以及其他6个国家的身份验证方式。  
**v0.3.3版本的新特性：**  
- 引入了BFT共识机制：通过**PROPOSE→VOTE→COMMIT**的流程实现节点注册，无需支付Gas费用，也不依赖外部组件。"
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

Soulprint通过保护隐私的验证机制，证明任何AI机器人背后都站着真实的人类用户——无需依赖中央权威机构，也无需上传生物特征数据到云端。所有验证过程都在设备本地完成。

**GitHub:** https://github.com/manuelariasfz/soulprint  
**npm:** https://www.npmjs.com/package/soulprint  
**文档:** https://soulprint.digital/docs/

---

## 使用场景

✅ 当您需要执行以下操作时，请使用此功能：
- “验证AI代理的身份”
- “运行Soulprint验证节点”
- “将身份验证功能添加到您的MCP服务器或API中”
- “检查机器人或DID的信誉分数”
- “根据哥伦比亚的公民身份证（cédula）生成隐私证明”
- “发行或验证SPT（Soulprint Token）”
- “设置不可降低的最低信任阈值”

❌ 以下情况下请勿使用此功能：
- 远程存储或传输生物特征数据（Soulprint的所有操作都在本地完成）
- 验证来自尚未支持该功能的国家的用户身份

---

## 快速入门

### 1. 验证您的身份（一次性操作）

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
GET  /protocol            — immutable protocol constants (floors, thresholds)
POST /verify              — verify proof and register anti-replay hash
POST /reputation/attest   — issue bot reputation attestation (+1 / -1)
GET  /reputation/:did     — get current bot reputation score (0-20)
GET  /proof-hash/:hash    — check if a proof hash is registered
```

---

## 协议常量（不可更改，由P2P网络强制执行）

网络中的所有验证节点都共享这些常量。这些常量通过以下两种方式确保其不可被修改：
1. **`Object.freeze()`** — 防止程序运行时对其进行修改
2. **P2P网络哈希** — `PROTOCOL_HASH`是根据所有常量计算得出的。任何修改都会导致哈希值发生变化，从而被整个网络拒绝。

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
| `PROTOCOL_HASH` | `dfe1ccca...` | 所有常量的SHA-256哈希值；不匹配则被网络隔离 |
| `SCORE_FLOOR` | **65** | 任何服务可以设置的最低分数阈值；低于此值的分数会自动被限制在65 |
| `VERIFIED SCORE_FLOOR` | **52** | 经过验证的身份（附带文档）的最低分数 |
| `MIN_ATTESTER SCORE` | **65** | 发行信誉证明所需的最低分数 |
| `VERIFY_RETRY_MAX` | **3** | 连接验证节点时的最大重试次数 |
| `VERIFY_RETRY_BASE_MS` | **500** | 重试间隔时间（每次尝试后翻倍） |
| `DEFAULT_REPUTATION` | **10** | 所有新代理的初始信誉分数 |
| `IDENTITY_MAX` | **80** | 身份子分数的最大值 |
| `REPUTATION_MAX` | **20** | 信誉总分的最大值 |

**查看节点的当前常量：**
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
- `requireSoulprint({ minScore: 40 })` → 实际使用的是65
- `requireSoulprint({ minScore: 80 })` → 使用80（已经高于最低阈值）

### 带有验证节点和重试功能的MCP服务器

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
3. 承载者认证头部

---

## 信任分数（0–100）

| 组件 | 最高分数 | 来源 |
|---|---|---|
| 邮箱验证 | 8 | 证书：电子邮件 |
| 手机验证 | 12 | 证书：手机 |
| GitHub账户 | 16 | 证书：GitHub账号 |
| 文档OCR识别 | 20 | 证书：文档 |
| 面部匹配 | 16 | 证书：面部识别 |
| 生物特征验证 | 8 | 证书：生物特征数据 |
| 机器人信誉 | 20 | 验证节点的证明 |

**所有验证节点强制执行的分数阈值：**
- 使用`requireSoulprint()`的服务，其分数阈值将被限制在65以上 |
- 已验证身份的用户，无论受到何种信誉攻击，总分数都不会低于52分 |

**机器人的默认信誉分数：**10/20（中立状态）。

---

## 重试逻辑

所有对验证节点的验证请求在失败时都会自动重试：

```
Attempt 1  → immediate
Attempt 2  → wait 500ms
Attempt 3  → wait 1000ms
           → fall back to offline signature-only verification
```

当设置了`validatorUrl`时，`requireSoulprint()`会自动处理重试逻辑。无需额外配置，行为由协议常量决定。

## 证书验证器（开源，内置）

每个验证节点都具备真实的身份验证功能，大多数情况下无需API密钥：

### 邮箱验证（nodemailer — SMTP）

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
配置参数：`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`（开发环境使用Ethereal通用配置，无需额外设置）

### 手机验证（TOTP — 无需短信，无需API密钥）

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
不依赖外部服务，使用RFC 6238 TOTP标准，支持离线验证。

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

用户通过`npx soulprint verify-me`命令自动完成验证。无需单独的API端点，验证结果与身份证明哈希值关联。

---

## 防止刷分行为

Soulprint的信誉系统可防止刷分行为：
**如果机器人试图刷分，其获得的分数会自动变为-1分。**

### 规则（不可更改，由所有验证节点执行）

| 规则 | 限制 | 后果 |
|---|---|---|
| 每日得分上限 | 每个DID每天最多+1分 | 检测到刷分行为时扣1分 |
| 每周得分上限 | 每周最多+2分 | 检测到刷分行为时扣1分 |
| 来源相同的服务 | 每天最多只能从同一服务获得1分 | 检测到刷分行为时扣1分 |
| 会话时长 | 最短会话时长为30秒 | 会话时间过短的用户无法获得奖励 |
| 工具多样性 | 使用的工具必须至少4种不同 | 使用工具过于单一会被阻止 |
| 机器人行为模式 | 调用间隔的标准差小于平均值的10% | 检测到异常行为时扣1分 |
| 新DID的试用期 | 新DID在获得分数前需要至少2次验证 | 首7天内得分为0分 |

### 刷分行为与真实使用的区别

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

- **验证机制：**采用本地电路和844个逻辑门，基于snarkjs的高级验证方案 |
- **验证时间：**本地处理时间约564毫秒 | **验证时间：**约25毫秒 |
- **防重放机制：**每个人都有唯一的身份哈希值，防止重复注册 |
- **隐私保护：**所有敏感信息都保留在设备本地；仅验证结果及其公开哈希值会被共享 |

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

节点在连接时会检查彼此的协议兼容性。使用不同协议版本或修改过分数阈值的节点会被自动排除在网络之外。

验证结果通过GossipSub协议传播；对于旧版本节点，使用HTTP作为备用方案。

---

## 相关npm包

| 包名 | 版本 | 功能 |
|---|---|---|
| `soulprint` | 最新版本 | 命令行工具（`npx soulprint verify-me`） |
| `soulprint-core` | 0.1.7 | DID管理、Token处理、协议常量、防刷分机制 |
| `soulprint-verify` | 0.1.4 | 提供OCR识别和面部匹配功能，以及生物特征验证的协议阈值 |
| `soulprint-zkp` | 0.1.4 | 使用ZK证明（Circom和snarkjs）和`PROTOCOL.FACE_KEY_DIMS`进行面部验证 |
| `soulprint-network` | 0.2.3 | 包含HTTP验证节点、P2P网络、证书验证器和防刷分机制 |
| `soulprint-mcp` | 0.1.4 | 提供MCP中间件，具有自动分数限制和重试功能 |
| `soulprint-express` | 0.1.3 | 适用于Express/Fastify框架的中间件 |

---

## 国家支持情况

| 国家 | 需要的验证方式 | 支持状态 |
|---|---|---|
| 🇨🇴 哥伦比亚 | 哥伦比亚公民身份证（cédula de Ciudadanía） | 完全支持（OCR识别+MRZ验证+面部匹配） |
| 🇲🇽 墨西哥 | INE/CURP | 部分支持 |
| 🇦🇷 阿根廷 | DNI | 部分支持 |
| 🇻🇪 委内瑞拉 | Cédula V/E | 部分支持 |
| 🇵🇪 秘鲁 | DNI | 部分支持 |
| 🇧🇷 巴西 | CPF | 部分支持 |
| 🇨🇱 智利 | 支持中（RUN） | 部分支持 |

**如需添加您的国家，请参考[贡献指南](https://github.com/manuelariasfz/soulprint/blob/main/CONTRIBUTING.md)。**
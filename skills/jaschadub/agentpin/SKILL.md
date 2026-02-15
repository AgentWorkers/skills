# AgentPin 开发技能指南

**目的**：本指南帮助 AI 助手使用 AgentPin 进行基于域的加密代理身份验证。

**完整文档**：请参阅 [README](https://github.com/ThirdKeyAI/agentpin/blob/main/README.md) 和 [技术规范](https://github.com/ThirdKeyAI/agentpin/blob/main/AGENTPIN_TECHNICAL_SPECIFICATION.md)。

## AgentPin 的功能

AgentPin 是一种基于域的加密身份验证协议，适用于 AI 代理。它允许组织为代理发布可验证的身份文档，颁发短期的 JWT 凭据，并通过包括 TOFU 密钥固定（Time-To-First-Use）、撤销检查以及委托链在内的多步骤流程来验证代理身份。

**属于 ThirdKey 信任栈的一部分**：SchemaPin（工具完整性）→ AgentPin（代理身份）→ Symbiont（运行时）

---

## 架构

```
Organization                         Verifying Party
────────────                         ───────────────
1. Generate ECDSA P-256 keypair
2. Publish agent identity at          3. Discover identity from
   /.well-known/agent-identity.json      /.well-known/agent-identity.json
4. Issue JWT credential               5. Verify credential (12-step flow)
   (ES256 signed, short-lived)           - JWT parsing & ES256 verification
                                         - Domain binding check
                                         - TOFU key pinning
                                         - Revocation checking
                                         - Capability validation
                                         - Delegation chain verification
```

---

## 项目结构

```
crates/
├── agentpin/          Core library (no mandatory HTTP dep)
├── agentpin-cli/      CLI binary (keygen, issue, verify, bundle)
└── agentpin-server/   Axum server for .well-known endpoints
```

---

## 按语言快速入门

### Rust（命令行接口）

```bash
# Generate keys
cargo run -p agentpin-cli -- keygen \
    --output-dir ./keys --agent-name "my-agent"

# Issue a credential (ES256 JWT, 1-hour TTL)
cargo run -p agentpin-cli -- issue \
    --key ./keys/my-agent.private.pem \
    --issuer "https://example.com" \
    --agent-id "my-agent" \
    --capabilities read,write --ttl 3600

# Verify offline
cargo run -p agentpin-cli -- verify \
    --credential ./credential.jwt \
    --discovery ./agent-identity.json

# Verify online (fetches from .well-known)
cargo run -p agentpin-cli -- verify \
    --credential ./credential.jwt --domain example.com

# Create trust bundle for air-gapped environments
cargo run -p agentpin-cli -- bundle \
    --discovery ./agent-identity.json \
    --revocation ./revocations.json --output ./bundle.json
```

### Rust（库）

```rust
use agentpin::{
    crypto,
    credential::CredentialBuilder,
    verification::verify_credential,
    pinning::KeyPinStore,
};

let (private_key, public_key) = crypto::generate_keypair()?;

let credential = CredentialBuilder::new()
    .issuer("https://example.com")
    .agent_id("my-agent")
    .capability("read")
    .capability("write")
    .ttl_secs(3600)
    .sign(&private_key)?;

let result = verify_credential(&credential, &discovery_doc, &pin_store)?;
```

### JavaScript

```bash
npm install agentpin
```

### Python

```bash
pip install agentpin
```

### Serve .well-known 端点

```bash
cargo run -p agentpin-server -- \
    --identity ./agent-identity.json \
    --revocation ./revocations.json \
    --port 3000
```

提供的接口：
- `GET /.well-known/agent-identity.json`（Cache-Control: max-age=3600）
- `GET /.well-known/agent-identity-revocations.json`（Cache-Control: max-age=300）
- `GET /health`

---

## 核心库 API

### 主要模块

| 模块 | 功能 |
|--------|---------|
| `crypto` | ECDSA P-256 签名/验证（不依赖外部 JWT 库） |
| `types` | 核心数据结构（代理、凭证、能力） |
| `credential` | JWT 的生成和解析 |
| `discovery` | 代理身份文档的发布和解析 |
| `verification` | 12 步骤的凭证验证流程 |
| `revocation` | 检查被撤销的凭证/代理/密钥 |
| `pinning` | 使用 JWK 拇印进行 TOFU 密钥固定 |
| `delegation` | 委托链验证 |
| `mutual` | 基于挑战-响应的相互认证（128 位随机数） |
| `jwk` | JWK 处理和拇指印计算 |
| `resolver` | 可插拔的发现解析机制 |

### 语言 API 参考

| 操作 | Rust | JavaScript | Python |
|-----------|------|------------|--------|
| 生成密钥 | `crypto::generate_keypair()` | `generateKeypair()` | `generate_keypair()` |
| 颁发凭证 | `CredentialBuilder::new().sign()` | `issueCredential()` | `issue_credential()` |
| 验证凭证 | `verify_credential()` | `verifyCredential()` | `verify_credential()` |
| 密钥固定 | `KeyPinStore` | `KeyPinStore` | `KeyPinStore` |
| 信任包 | `TrustBundle::from_json()` | `TrustBundle.fromJson()` | `TrustBundle.from_json()` |
| 相互认证 | `MutualAuth::challenge()` | `createChallenge()` | `create_challenge()` |

### 特性开关

| 特性 | 功能 |
|---------|---------|
| `fetch` | 通过 reqwest 启用 HTTP 进行在线发现 |
| （默认） | 无 HTTP 依赖的核心库 |

---

## 关键概念

### 仅使用 ES256

AgentPin 仅使用 ES256（ECDSA P-256）算法。所有其他算法都会被拒绝。这一要求是通过代码直接实现的，无需依赖外部 JWT 库。

### 12 步骤验证流程

凭证验证流程包括：
1. JWT 结构解析
2. 标头算法验证（仅限 ES256）
3. 签名验证
4. 发行者域提取
5. 发现文档解析
6. 域绑定验证
7. 密钥匹配（发行者密钥与发现文档中的密钥对比）
8. TOFU 密钥固定检查
9. 有效期验证
10. 撤销检查
11. 能力验证
12. 委托链验证（如果存在）

### TOFU 密钥固定

在首次验证某个域的凭证时，会固定代理的公钥（JWK 拇印）。后续的验证会拒绝同一域下的其他密钥，以防止密钥替换攻击。

### 委托链

代理可以将能力委托给子代理。委托链会经过验证，以确保：
- 每个环节都由委托者签名
- 能力在链中只能向下细化（不能向上扩展）
- 遵守链的深度限制

### 相互认证

使用基于挑战-响应的协议，并结合 128 位随机数进行双向代理身份验证。

---

## 发现文档格式

文档发布在 `/.well-known/agent-identity.json`：

```json
{
    "schema_version": "0.2",
    "domain": "example.com",
    "agents": [
        {
            "agent_id": "my-agent",
            "display_name": "My Agent",
            "description": "A helpful agent",
            "capabilities": ["read", "write"],
            "public_key_jwk": { ... },
            "constraints": {
                "max_ttl_secs": 86400,
                "allowed_scopes": ["api"]
            }
        }
    ],
    "revocation_endpoint": "https://example.com/.well-known/agent-identity-revocations.json",
    "directory_listing": true
}
```

---

## v0.2.0 新特性

### 信任包（离线/隔离环境）

为没有互联网连接的环境预打包发现数据和撤销数据：

```python
from agentpin.bundle import TrustBundle

bundle = TrustBundle.from_json(bundle_json_str)
discovery = bundle.find_discovery("example.com")
revocation = bundle.find_revocation("example.com")
```

### 可插拔的发现解析器

```python
from agentpin.discovery import (
    WellKnownResolver,    # HTTP .well-known lookups
    DnsTxtResolver,       # DNS TXT record lookups
    ManualResolver,       # Pre-configured discovery data
)
```

### 目录列表

域名可以通过在发现文档中设置 `"directory_listing": true` 来公布所有代理信息。验证者可以在发起挑战之前枚举可用的代理。

---

## 开发

### 构建和测试

```bash
# Build all crates
cargo build --workspace

# Run all tests
cargo test --workspace

# Lint
cargo clippy --workspace

# Format check
cargo fmt --check
```

### 开发规范

- 使用 Rust 2021 版本，MSRV 1.70
- 必须通过 `cargo clippy --workspace` 且无警告
- 必须通过 `cargo fmt --check`
- 源文件中的内联测试（`#[cfg(test)] mod tests`）
- 仅使用 ES256 算法
- HTTP 功能是可选的：`fetch` 特性用于启用 reqwest

---

## 对 AI 助手的开发建议

1. **仅使用 ES256** — 绝不接受 RS256、HS256 或其他算法
2. **使用短期凭证** — 优先选择几小时有效期的凭证，而非几天
3. **在信任凭证之前务必检查其是否已被撤销**
4. **TOFU 密钥固定** 表示首次看到的密钥是可信的；发现密钥变更时需发出警告
5. **委托链** 应该限制代理的能力范围，不能扩大
6. **不依赖外部 JWT 库** — 算法验证通过代码直接控制，以防止混淆攻击
7. **HTTP 功能是可选的** — 仅在需要在线发现时启用；默认情况下支持离线使用
8. **与 SchemaPin 兼容** — 两者都使用 ECDSA P-256 算法
9. **信任包** 非常适合持续集成/持续部署（CI/CD）和隔离环境——预打包发现数据和撤销数据
10. **JavaScript 和 Python SDK** 提供与 Rust 库相同的验证保障
# SchemaPin 开发技能指南

**目的**：本指南帮助 AI 助手快速将 SchemaPin 集成到应用程序中，以实现加密工具模式的验证。

**如需完整文档**：请参阅 [README](https://github.com/ThirdKeyAI/SchemaPin/blob/main/README.md)、[技术规范](https://github.com/ThirdKeyAI/SchemaPin/blob/main/TECHNICAL_SPECIFICATION.md) 以及每个子目录中的语言特定 README 文件。

## SchemaPin 的功能

SchemaPin 通过允许开发者对其工具模式进行加密签名（使用 ECDSA P-256 + SHA-256），并让客户端验证模式是否被篡改，从而防止“MCP Rug Pull”攻击。它采用“首次使用即信任”（TOFU, Trust-On-First-Use）的密钥固定机制，并利用 RFC 8615 的 `.well-known` 端点来发现公钥。

**属于 ThirdKey 信任栈的一部分**：SchemaPin（工具完整性）→ AgentPin（代理身份）→ Symbiont（运行时）

---

## 按语言快速入门

### Python

```bash
pip install schemapin
```

```python
from schemapin.crypto import KeyManager, SignatureManager
from schemapin.core import SchemaPinCore

# Generate keys
private_key, public_key = KeyManager.generate_keypair()

# Sign a schema
core = SchemaPinCore()
canonical = core.canonicalize_schema(schema_dict)
signature = SignatureManager.sign_schema(private_key, canonical)

# Verify
is_valid = SignatureManager.verify_signature(public_key, canonical, signature)
```

### JavaScript

```bash
npm install schemapin
```

```javascript
import { KeyManager, SignatureManager, SchemaPinCore } from 'schemapin';

// Generate keys
const { privateKey, publicKey } = KeyManager.generateKeypair();

// Sign a schema
const core = new SchemaPinCore();
const canonical = core.canonicalizeSchema(schema);
const signature = await SignatureManager.signSchema(privateKey, canonical);

// Verify
const isValid = await SignatureManager.verifySignature(publicKey, canonical, signature);
```

### Go

```bash
go get github.com/ThirdKeyAi/schemapin/go@v1.3.0
```

```go
import (
    "github.com/ThirdKeyAi/schemapin/go/pkg/core"
    "github.com/ThirdKeyAi/schemapin/go/pkg/crypto"
)

// Generate keys
km := crypto.NewKeyManager()
privKey, pubKey, _ := km.GenerateKeypair()

// Sign a schema
spc := core.NewSchemaPinCore()
canonical, _ := spc.CanonicalizeSchema(schema)
sig, _ := crypto.NewSignatureManager().SignSchema(privKey, canonical)

// Verify
valid, _ := crypto.NewSignatureManager().VerifySignature(pubKey, canonical, sig)
```

### Rust

```toml
[dependencies]
schemapin = "1.3"
```

```rust
use schemapin::crypto::{generate_key_pair, sign_data, verify_signature};
use schemapin::core::SchemaPinCore;

// Generate keys
let key_pair = generate_key_pair()?;

// Sign
let core = SchemaPinCore::new();
let canonical = core.canonicalize_schema(&schema)?;
let signature = sign_data(&key_pair.private_key_pem, &canonical)?;

// Verify
let is_valid = verify_signature(&key_pair.public_key_pem, &canonical, &signature)?;
```

---

## 核心概念

### 1. 模式规范化

在哈希之前，模式会被规范化（即使用排序后的键进行确定性 JSON 序列化）。这确保了相同的模式无论键的顺序如何，总是会产生相同的哈希值。

### 2. `.well-known` 端点的使用

开发者将他们的公钥发布在 `https://example.com/.well-known/schemapin.json` 上：

```python
from schemapin.utils import create_well_known_response

response = create_well_known_response(
    public_key_pem=public_key_pem,
    developer_name="Acme Corp",
    schema_version="1.2",
    revocation_endpoint="https://example.com/.well-known/schemapin-revocations.json"
)
```

### 3. TOFU 密钥固定机制

在首次验证时，会固定开发者的公钥指纹。后续的验证会拒绝同一域下的不同密钥——从而检测到密钥替换攻击。

### 4. 验证流程

**在线**（标准方式）：
```python
workflow = SchemaVerificationWorkflow(pin_store)
result = workflow.verify_schema(schema, signature, "https://example.com")
```

**离线**（v1.2.0 版本——无需 HTTP）：
```python
from schemapin.verification import verify_schema_offline, KeyPinStore

pin_store = KeyPinStore()
result = verify_schema_offline(
    schema, signature_b64, domain, tool_id,
    discovery_data, revocation_doc, pin_store
)
```

---

## v1.2.0 新功能

### 独立的吊销文档

```python
from schemapin.revocation import (
    build_revocation_document, add_revoked_key,
    check_revocation, RevocationReason
)

doc = build_revocation_document("example.com")
add_revoked_key(doc, fingerprint, RevocationReason.KEY_COMPROMISE)
check_revocation(doc, some_fingerprint)  # raises if revoked
```

### 信任包（离线/隔离环境）

为没有互联网连接的环境预先打包发现数据和吊销数据：

```python
from schemapin.bundle import SchemaPinTrustBundle

bundle = SchemaPinTrustBundle.from_json(bundle_json_str)
discovery = bundle.find_discovery("example.com")
revocation = bundle.find_revocation("example.com")
```

### 可插拔的发现解析器

```python
from schemapin.resolver import (
    WellKnownResolver,    # HTTP .well-known lookups
    LocalFileResolver,    # Local JSON files
    TrustBundleResolver,  # In-memory trust bundles
    ChainResolver,        # First-match fallthrough
)

# Chain: try bundle first, fall back to HTTP
resolver = ChainResolver([
    TrustBundleResolver.from_json(bundle_json),
    WellKnownResolver(timeout=10),
])
```

### 基于解析器的验证

```python
from schemapin.verification import verify_schema_with_resolver

result = verify_schema_with_resolver(
    schema, signature_b64, domain, tool_id,
    resolver, pin_store
)
```

---

## v1.3.0 新功能

### SkillSigner — 基于文件的技能目录签名

使用 ECDSA P-256 对整个技能目录（例如包含 `SKILL.md` 的目录）进行签名。会在文件旁边生成一个 `.schemapin.sig` 文件，证明文件未被篡改。

**Python:**
```python
from schemapin.skill import sign_skill, verify_skill_offline

# Sign a skill directory
sig = sign_skill("./my-skill/", private_key_pem, "example.com")
# Writes .schemapin.sig into ./my-skill/

# Verify offline
from schemapin.verification import KeyPinStore
result = verify_skill_offline("./my-skill/", discovery_data, sig, revocation_doc, KeyPinStore())
```

**JavaScript:**
```javascript
import { signSkill, verifySkillOffline } from 'schemapin/skill';

const sig = await signSkill('./my-skill/', privateKeyPem, 'example.com');
const result = verifySkillOffline('./my-skill/', discoveryData, sig, revDoc, pinStore);
```

**Go:**
```go
import "github.com/ThirdKeyAi/schemapin/go/pkg/skill"

sig, err := skill.SignSkill("./my-skill/", privateKeyPEM, "example.com", "", "")
result := skill.VerifySkillOffline("./my-skill/", disc, sig, rev, pinStore, "")
```

**Rust:**
```rust
use schemapin::skill::{sign_skill, verify_skill_offline};

let sig = sign_skill("./my-skill/", &private_key_pem, "example.com", None, None)?;
let result = verify_skill_offline("./my-skill/", &disc, Some(&sig), rev.as_ref(), Some(&pin_store), None);
```

### `.schemapin.sig` 格式

```json
{
  "schemapin_version": "1.3",
  "skill_name": "my-skill",
  "skill_hash": "sha256:<root_hash>",
  "signature": "<base64_ecdsa_signature>",
  "signed_at": "2026-02-14T00:00:00Z",
  "domain": "example.com",
  "signer_kid": "sha256:<key_fingerprint>",
  "file_manifest": {
    "SKILL.md": "sha256:<file_hash>"
  }
}
```

### 损坏检测

```python
from schemapin.skill import detect_tampered_files, canonicalize_skill

_, current_manifest = canonicalize_skill("./my-skill/")
tampered = detect_tampered_files(current_manifest, sig.file_manifest)
# tampered.modified, tampered.added, tampered.removed
```

---

## 服务器端设置

### 发布 `.well-known` 端点

提供了 Python CLI 工具：

```bash
# Generate a keypair
schemapin-keygen --output-dir ./keys

# Sign a schema
schemapin-sign --key ./keys/private.pem --schema schema.json

# Verify a signature
schemapin-verify --key ./keys/public.pem --schema schema.json --signature sig.b64
```

也提供了 Go CLI 工具（`go install github.com/ThirdKeyAi/schemapin/go/cmd/...@v1.3.0`）。

---

## 架构

```
Developer                          Client (AI Platform)
─────────                          ────────────────────
1. Generate ECDSA P-256 keypair
2. Publish public key at           3. Discover public key from
   /.well-known/schemapin.json        /.well-known/schemapin.json
4. Sign tool schema                5. Verify signature
   (canonicalize → SHA-256            (canonicalize → SHA-256
    → ECDSA sign)                      → ECDSA verify)
                                   6. TOFU pin the key fingerprint
                                   7. Check revocation status
```

---

## 语言 API 参考

| 操作 | Python | JavaScript | Go | Rust |
|-----------|--------|------------|----|----|
| 生成密钥 | `KeyManager.generate_keypair()` | `KeyManager.generateKeypair()` | `km.GenerateKeypair()` | `generate_key_pair()` |
| 签名模式 | `SignatureManager.sign_schema()` | `SignatureManager.signSchema()` | `sm.SignSchema()` | `sign_data()` |
| 验证签名 | `SignatureManager.verify_signature()` | `SignatureManager.verifySignature()` | `sm.VerifySignature()` | `verify_signature()` |
| 规范化模式 | `SchemaPinCore().canonicalize_schema()` | `new SchemaPinCore().canonicalizeSchema()` | `spc.CanonicalizeSchema()` | `SchemaPinCore::new().canonicalize_schema()` |
| 发现密钥 | `PublicKeyDiscovery.fetch_well_known()` | `PublicKeyDiscovery.fetchWellKnown()` | `FetchWellKnown()` | `WellKnownResolver`（用于获取密钥） |
| 离线验证 | `verify_schema_offline()` | `verifySchemaOffline()` | `VerifySchemaOffline()` | `verify_schema_offline()` |
| 使用解析器验证 | `verify_schema_with Resolver()` | `verifySchemaWithResolver()` | `VerifySchemaWithResolver()` | `verify_schema_with Resolver()` |
| 签名技能目录 | `sign_skill()` | `signSkill()` | `skill.SignSkill()` | `sign_skill()` |
| 验证技能 | `verify_skill_offline()` | `verifySkillOffline()` | `skill.VerifySkillOffline()` | `verify_skill_offline()` |
| 检测篡改 | `detect_tampered_files()` | `detectTamperedFiles()` | `skill.DetectTamperedFiles()` | `detect_tampered_files()` |

---

## 测试

```bash
# Python
cd python && python -m pytest tests/ -v

# JavaScript
cd javascript && npm test

# Go
cd go && go test ./...

# Rust
cd rust && cargo test
```

---

## 对 AI 助手的实用建议

1. **签名或验证之前务必进行规范化**——原始 JSON 比较会导致错误
2. **在预先获取了发现数据的情况下使用离线验证**——避免在模式验证过程中进行 HTTP 请求
3. **信任包** 非常适合持续集成/持续交付（CI/CD）和隔离环境（air-gapped）部署
4. **ChainResolver** 允许你分层使用解析器：先使用本地文件，再使用 HTTP 作为备用方案
5. **TOFU 密钥固定机制** 意味着第一个检测到的域密钥会被信任——在密钥发生变化时提醒用户
6. **所有语言都使用相同的加密算法**——ECDSA P-256 + SHA-256，因此跨语言验证是可行的
7. **应始终执行吊销检查**——无论是使用简单列表还是独立的吊销文档
8. **SkillSigner** 可以对整个目录进行签名——非常适合上传到 ClaWHub 等注册平台的 SKILL.md 文件夹
9. `.schemapin.sig` 文件会被自动排除在哈希计算之外——你可以重新签名目录而无需先删除旧签名
---
name: verified-agent-identity
description: Billions/Iden3 提供用于代理的认证和身份管理工具，支持证明、签名以及验证功能。
metadata: { "category": "identity" }
---
## 何时使用此技能

该技能允许AI代理在Billions Network上创建和管理自己的身份，并通过加密签名来证明这些身份的所有权。

1. 当你需要证明自己的身份时。
2. 当你需要签署挑战请求时。
3. 当你需要验证签名以确认身份所有权时。
4. 当你需要使用共享的JWT令牌进行身份认证时。
5. 当你需要创建和管理去中心化身份时。

## 使用范围

所有身份数据都存储在`$HOME/.openclaw/billions`中，以便与OpenClaw插件兼容。

### 脚本：

#### createNewEthereumIdentity.js

**命令**: `node scripts/createNewEthereumIdentity.js [--key <privateKeyHex>]`
**描述**: 在Billions Network上创建一个新的身份。如果提供了`--key`参数，则使用该私钥；否则会生成一个新的随机密钥。创建的身份将自动设置为默认身份。
**使用示例**:

```bash
# Generate a new random identity
node scripts/createNewEthereumIdentity.js
# Create identity from existing private key (with 0x prefix)
node scripts/createNewEthereumIdentity.js --key 0x1234567890abcdef...
# Create identity from existing private key (without 0x prefix)
node scripts/createNewEthereumIdentity.js --key 1234567890abcdef...
```

**输出**: DID字符串（例如：`did:iden3:billions:main:2VmAk7fGHQP5FN2jZ8X9Y3K4W6L1M...`)
**副作用**:
- 将私钥存储在`$HOME/.openclaw/billions/kms.json`中。
- 将DID条目存储在`$HOME/.openclaw/billions/defaultDid.json`中。

---

#### getIdentities.js

**命令**: `node scripts/getIdentities.js`
**描述**: 列出本地存储的所有DID身份。在执行身份验证操作之前，可以使用此脚本来检查哪些身份可用。
**使用示例**:

```bash
node scripts/getIdentities.js
```

**输出**: 身份条目的JSON数组

---

#### generateChallenge.js

**命令**: `node scripts/generateChallenge.js --did <did>`
**描述**: 生成用于身份验证的随机挑战字符串。
**使用示例**:

```bash
node scripts/generateChallenge.js --did did:iden3:billions:main:2VmAk...
```

**输出**: 挑战字符串（以字符串形式表示的随机数，例如：`8472951360`)
**副作用**: 将与DID关联的挑战字符串存储在`$HOME/.openclaw/billions/challenges.json`中。

---

#### signChallenge.js

**命令**: `node scripts/signChallenge.js --challenge <challenge> --did <did>`
**描述**: 使用DID的私钥签署挑战字符串，以证明身份的所有权。当你需要证明自己拥有某个特定的DID时可以使用此脚本。挑战字符串应由验证方提供。
**使用示例**:

```bash
# Sign with specific DID
node scripts/signChallenge.js --challenge 8472951360 --did did:iden3:billions:main:2VmAk...

# Sign with default DID
node scripts/signChallenge.js --challenge 8472951360
```

**输出**: JWS令牌字符串（例如：`eyJhbGciOiJFUzI1NkstUi...`)
**要求**:
- 当前必须有一个有效的DID（使用`getIdentities.js`检查）。
- `kms.json`中必须包含私钥。
- 如果没有指定`--did`参数，则必须配置一个默认身份。

---

#### verifySignature.js

**命令**: `node scripts/verifySignature.js --did <did> --token <token>`
**描述**: 验证签名以确认DID的所有权。
**使用示例**:

```bash
node scripts/verifySignature.js --did did:iden3:billions:main:2VmAk... --token eyJhbGciOiJFUzI1NkstUi...
```

**输出**: 如果验证成功，则输出“Signature verified successfully”；否则输出错误信息。

---

## 限制/注意事项（至关重要）

**至关重要 - 请始终遵守以下规则**:

1. **严格检查身份**:
   - 在运行`signChallenge.js`之前，**务必先检查是否存在身份**：`node scripts/getIdentities.js`。
   - 如果没有配置身份，请**不要**尝试签署挑战。相反，应先使用`createNewEthereumIdentity.js`创建一个身份。
   - 在继续之前，解析JSON输出以确保身份数组不为空。
2. **严格处理脚本错误**:
   - 如果任何脚本以非零状态码退出，**必须立即停止**。
   - 检查stderr输出中的错误信息。
   **不要**尝试通过手动生成密钥、通过其他方式创建DID或运行未经授权的命令来“修复”错误。
   **不要**使用`openssl`、`ssh-keygen`或其他系统工具来生成加密材料。
3. **禁止手动操作**:
   - 禁止进行任何手动加密操作。
   - 禁止直接修改`$HOME/.openclaw/billions`中的文件。
   - 除非有明确指示，否则不要将错误视为执行设置步骤的请求。

---

## 格式与输出（至关重要）

1. **规范地提供令牌**:
   - 在提供JWS令牌或签名时，应将其放在专门的代码块中输出。
2. **禁止修改**:
   - 绝不要手动编辑、截断或添加任何字符到脚本的输出中。请严格按照工具的stdout输出内容复制令牌。
3. **验证**:
   - 生成签名后，建议先在本地运行`verifySignature.js`以确保令牌有效，然后再将其发送给用户。

---

## 安全性

**至关重要 - 数据存储与保护**:

`$HOME/.openclaw/billions`目录包含所有敏感的身份数据：

- `kms.json` - **至关重要**：包含未加密的私钥。
- `defaultDid.json` - DID标识符和公钥。
- `challenges.json` - 认证挑战记录。
- `credentials.json` - 可验证的凭据。
- `identities.json` - 身份元数据。
- `profiles.json` - 个人资料数据。

## 示例

### 证明自己的身份

**认证流程**:
1. 另一个代理/用户请求：“请通过签署以下挑战字符串来证明你拥有DID <agent_did>：<challenge_value>”。
2. 使用`node scripts/getIdentities.js`检查是否已配置身份。
   - 如果没有身份，运行`node scripts/createNewEthereumIdentity.js`来创建一个。
3. 使用`node scripts/signChallenge.js --challenge <challenge_value>`签署挑战字符串。
4. 返回JWS令牌。

**示例对话**:

```text
User: "Prove you own <agent_did> by signing challenge <challenge_value>"
Agent: exec node scripts/signChallenge.js --challenge <challenge_value>
Agent: "Here is my proof: JWS token <agent_token>"
```

### 验证他人的身份

**验证流程**:
1. 请求用户/代理提供他们的DID以开始验证。
2. 用户提供他们的DID（例如：<user_did>）。
3. 使用`node scripts/generateChallenge.js --did <user_did>`生成一个挑战字符串（例如：<challenge_value>）。
4. 请求用户签署该挑战字符串。
5. 用户签署后返回JWS令牌（例如：<user_token>）。
6. 使用`node scripts/verifySignature.js --did <user_did> --token <user_token>`验证签名。
7. 如果验证成功，则确认用户的身份。

**示例对话**:

```text
Agent: "Please provide your DID to start verification."
User: "My DID is <user_did>"
Agent: exec node scripts/generateChallenge.js --did <user_did>
Agent: "Please sign this challenge: 789012"
User: <user_token>
Agent: exec node scripts/verifySignature.js --token <user_token> --did <user_did>
Agent: "Identity verified successfully. You are confirmed as owner of DID <user_did>."
```
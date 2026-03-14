---
name: verified-agent-identity
description: 为代理提供数十亿个去中心化的身份认证服务。利用 Billions ERC-8004 标准以及认证注册系统（Attestation Registries）将代理与人类身份关联起来。对身份信息进行验证，并生成相应的认证证明。该系统基于 iden3 自主主权身份协议（iden3 self-sovereign identity protocol）构建。
metadata: { "category": "identity", "clawdbot": { "requires": { "bins": ["node"] } } }
homepage: https://billions.network/
---
## 何时使用此技能

当需要让AI代理在Billions Network上创建和管理自己的身份，并将这些身份与人类所有者关联起来时，可以使用此技能。

1. 当您需要将代理的身份与所有者关联时。
2. 当您需要签署挑战请求时。
3. 当您需要将人类用户与代理的DID关联时。
4. 当您需要验证签名以确认身份所有权时。
5. 当您使用共享的JWT令牌进行身份验证时。
6. 当您需要创建和管理去中心化身份时。

### 安装插件后，请运行以下命令来创建一个身份并将其与您的DID关联：

```bash
cd scripts && npm install && cd ..
# Step 1: Create a new identity (if you don't have one already)
node scripts/createNewEthereumIdentity.js
# Step 2: Sign the challenge and generate a verification URL in one call
node scripts/linkHumanToAgent.js --challenge '{"name": <AGENT_NAME>, "description": <SHORT_DESCRIPTION>}'
```

## 范围

所有身份数据都存储在`$HOME/.openclaw/billions`目录中，以确保与OpenClaw插件的兼容性。

### 脚本：

### createNewEthereumIdentity.js

**命令**: `node scripts/createNewEthereumIdentity.js [--key <privateKeyHex>]`
**描述**: 在Billions Network上创建一个新的身份。如果提供了`--key`参数，将使用该私钥；否则会生成一个新的随机密钥。创建的身份将自动设置为默认值。
**使用示例**:

```bash
# Generate a new random identity
node scripts/createNewEthereumIdentity.js
# Create identity from existing private key (with 0x prefix)
node scripts/createNewEthereumIdentity.js --key 0x1234567890abcdef...
# Create identity from existing private key (without 0x prefix)
node scripts/createNewEthereumIdentity.js --key 1234567890abcdef...
```

**输出**: DID字符串（例如：`did:iden3:billions:main:2VmAk7fGHQP5FN2jZ8X9Y3K4W6L1M...`）

---

### getIdentities.js

**命令**: `node scripts/getIdentities.js`
**描述**: 列出本地存储的所有DID身份。在执行身份验证操作之前，可以使用此脚本来检查可用的身份。
**使用示例**:

```bash
node scripts/getIdentities.js
```

**输出**: 身份条目的JSON数组

---

### generateChallenge.js

**命令**: `node scripts/generateChallenge.js --did <did>`
**描述**: 生成一个用于身份验证的随机挑战字符串。
**使用示例**:

```bash
node scripts/generateChallenge.js --did did:iden3:billions:main:2VmAk...
```

**输出**: 挑战字符串（以字符串形式表示的随机数，例如：`8472951360`）
**副作用**: 会将生成的挑战字符串存储在`$HOME/.openclaw/billions/challenges.json`文件中

---

### signChallenge.js

**命令**: `node scripts/signChallenge.js --challenge <challenge> --did <did>`
**描述**: 使用DID的私钥签署挑战字符串，以证明身份所有权，并发送JWS令牌。当您需要证明自己拥有某个特定的DID时，可以使用此脚本。
**参数**:
- `--challenge` - （必选）需要签署的挑战字符串
- `--did` - （可选）证书接收者的DID；如果省略，则使用默认DID

**使用示例**:

```bash
# Sign with default DID
node scripts/signChallenge.js --challenge 8472951360
```

**输出**: `{"success":true}`

---

### linkHumanToAgent.js

**命令**: `node scripts/linkHumanToAgent.js --challenge <challenge> --did <did>`
**描述**: 签署挑战字符串，并通过创建验证请求将人类用户与代理的DID关联起来。实际上，关联过程是通过Billions ERC-8004注册表（每个代理都在此注册）和Billions Attestation注册表（在验证人类用户唯一性后创建代理所有权证书）来完成的。
**参数**:
- `--challenge` - （必选）需要签署的挑战字符串
- `--did` - （可选）证书接收者的DID；如果省略，则使用默认DID

**使用示例**:

```bash
node scripts/linkHumanToAgent.js --challenge '{"name": "MyAgent", "description": "AI persona"}'
```

**输出**: `{"success":true}`

---

### verifySignature.js

**命令**: `node scripts/verifySignature.js --did <did> --token <token>`
**描述**: 验证签署的挑战字符串，以确认DID的所有权。
**使用示例**:

```bash
node scripts/verifySignature.js --did did:iden3:billions:main:2VmAk... --token eyJhbGciOiJFUzI1NkstUi...
```

**输出**: 如果验证成功，输出“Signature verified successfully”；如果失败，则输出错误信息

---

## 限制/注意事项（至关重要）

**至关重要 - 请始终遵守以下规则：**

1. **严格检查身份**：
   - 在运行`linkHumanToAgent.js`或`signChallenge.js`之前，**务必先检查是否存在身份**：`node scripts/getIdentities.js`
   - 如果没有配置身份，请**不要**尝试关联身份。相反，应先使用`createNewEthereumIdentity.js`创建一个身份。
2. **脚本失败时立即停止**：
   - 如果任何脚本以非零状态码退出，**必须立即停止**。
   - 检查stderr输出中的错误信息。
   - **不要**尝试通过手动生成密钥、使用其他方法创建DID或运行未经授权的命令来“修复”错误。
   **不要**使用`openssl`、`ssh-keygen`或其他系统工具来生成加密材料。
3. **禁止手动操作**：
   - 禁止进行任何手动加密操作。
   **禁止直接修改`$HOME/.openclaw/billions`目录中的文件**。
   - 除非有明确指示，否则不要将错误理解为需要执行设置步骤的信号。

---

## 安全性

**至关重要 - 数据存储与保护**：

`$HOME/.openclaw/billions`目录包含所有敏感的身份数据：

- `kms.json` - **至关重要**：包含私钥（如果设置了`BILLIONS_NETWORK_MASTER_KMS_KEY`，则私钥会被加密；否则以明文形式存储）
- `defaultDid.json` - DID标识符和公钥
- `challenges.json` - 认证挑战记录
- `credentials.json` - 可验证的凭据信息
- `identities.json` - 身份元数据
- `profiles.json` - 用户资料

## 示例

### 将代理身份与所有者关联

**关联流程**:
1. 另一个代理/用户请求：“请将您的代理身份与我关联。”
2. 使用`node scripts/getIdentities.js`检查您是否已配置了身份。
   - 如果没有配置身份，运行`node scripts/createNewEthereumIdentity.js`来创建一个。
3. 使用`node scripts/linkHumanToAgent.js --challenge <challenge_value>`一次性完成挑战的签署和验证URL的生成。
   - 如果调用者提供了具体的挑战字符串，请使用该字符串；如果没有提供挑战字符串，可以使用`{"name": <AGENT_NAME>, "description": <SHORT_DESCRIPTION>}`作为挑战值。
4. 将结果返回给调用者。

**示例对话**:

```text
User: "Link your agent identity to me"
Agent: exec node scripts/linkHumanToAgent.js --challenge <challenge_value>
```

### 验证他人的身份

**验证流程**:
1. 请求用户/代理：“请提供您的DID以开始验证。”
2. 用户提供他们的DID（`<user_did>`）。
3. 使用`node scripts/generateChallenge.js --did <user_did>`生成一个挑战字符串（`<challenge_value>`）。
4. 请求用户：“请签署这个挑战：<challenge_value>`。
5. 用户签署并返回签名（`<user_token>`）。
6. 使用`node scripts/verifySignature.js --did <user_did> --token <user_token>`来验证签名。
7. 如果验证成功，即可确认身份。

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
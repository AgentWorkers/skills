---
name: verified-agent-identity
description: Billions/Iden3 提供了一套用于代理的认证和身份管理工具，支持链接验证、身份证明、签名以及信息核实等功能。
metadata: { "category": "identity", "clawbot": { "requires": { "bins": ["node", "openclaw"] } }}
homepage: https://billions.network/
---
## 何时使用此技能

此技能允许AI代理在Billions Network上创建和管理自己的身份，并将这些身份与人类所有者关联起来。以下是几种需要使用此技能的场景：

1. 当您需要将代理的身份与所有者关联时。
2. 当您需要签署挑战请求（challenge）时。
3. 当您需要将人类用户与代理的DID（Decentralized Identity）关联时。
4. 当您需要验证签名以确认身份所有权时。
5. 当您需要使用共享的JWT令牌进行身份认证时。
6. 当您需要创建和管理去中心化身份时。

### 安装插件后，请运行以下命令来创建一个身份并将其与您的DID关联：

```bash
cd scripts && npm install && cd ..
# Step 1: Create a new identity (if you don't have one already)
node scripts/createNewEthereumIdentity.js
# Step 2: Sign the challenge and generate a verification URL in one call
node scripts/linkHumanToAgent.js --to <SENDER> --challenge '{"name": <AGENT_NAME>, "description": <SHORT_DESCRIPTION>}'
```

## 范围

所有身份数据都存储在`$HOME/.openclaw/billions`目录中，以确保与OpenClaw插件的兼容性。

### 脚本：

#### createNewEthereumIdentity.js

**命令**: `node scripts/createNewEthereumIdentity.js [--key <privateKeyHex>]`
**描述**: 在Billions Network上创建一个新的身份。如果提供了`--key`参数，则使用该私钥；否则会生成一个新的随机密钥。创建的身份将自动设置为默认值。
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

#### getIdentities.js

**命令**: `node scripts/getIdentities.js`
**描述**: 列出本地存储的所有DID身份。在执行身份验证操作之前，可以使用此脚本检查可用的身份。
**使用示例**:

```bash
node scripts/getIdentities.js
```

**输出**: 身份条目的JSON数组

#### generateChallenge.js

**命令**: `node scripts/generateChallenge.js --did <did>`
**描述**: 生成一个用于身份验证的随机挑战字符串。
**使用示例**:

```bash
node scripts/generateChallenge.js --did did:iden3:billions:main:2VmAk...
```

**输出**: 挑战字符串（例如：`8472951360`）
**副作用**: 生成的挑战数据会存储在`$HOME/.openclaw/billions/challenges.json`文件中。

#### signChallenge.js

**命令**: `node scripts/signChallenge.js --to <sender> --challenge <challenge> [--did <did>]`
**描述**: 使用DID的私钥签署挑战请求，以证明身份所有权，并将JWS令牌作为直接消息发送给指定的接收者。当您需要证明自己拥有某个特定的DID时可以使用此脚本。
**参数**:
- `--to` - （必需）消息发送者的标识符，通过`openclaw message send`传递。
- `--challenge` - （必需）需要签署的挑战字符串。
- `--did` - （可选）验证接收者的DID；如果省略则使用默认DID。

**使用示例**:

```bash
# Sign with default DID and send to sender
node scripts/signChallenge.js --to <sender> --challenge 8472951360
```

**输出**: `{"success":true}`

#### linkHumanToAgent.js

**命令**: `node scripts/linkHumanToAgent.js --to <sender> --challenge <challenge> [--did <did>]`
**描述**: 签署挑战请求，并将人类用户与代理的DID关联起来。响应会作为直接消息发送给指定的接收者。
**参数**:
- `--to` - （必需）消息发送者的标识符，通过`openclaw message send`传递。
- `--challenge` - （必需）需要签署的挑战字符串。
- `--did` - （可选）验证接收者的DID；如果省略则使用默认DID。

**使用示例**:

```bash
node scripts/linkHumanToAgent.js --to <sender> --challenge '{"name": "MyAgent", "description": "AI persona"}'
```

**输出**: `{"success":true}`

#### verifySignature.js

**命令**: `node scripts/verifySignature.js --did <did> --token <token>`
**描述**: 验证签名以确认DID的所有权。
**使用示例**:

```bash
node scripts/verifySignature.js --did did:iden3:billions:main:2VmAk... --token eyJhbGciOiJFUzI1NkstUi...
```

**输出**: 如果验证成功，则输出“Signature verified successfully”；否则输出错误信息。

## 限制/注意事项（至关重要）

**至关重要 - 请始终遵守以下规则**:

1. **严格检查身份**:
   - 在运行`linkHumanToAgent.js`或`signChallenge.js`之前，**务必先检查是否存在身份**：`node scripts/getIdentities.js`。
   - 如果没有配置身份，请**不要**尝试关联身份。此时应使用`createNewEthereumIdentity.js`创建一个新的身份。
2. **脚本失败时立即停止**:
   - 如果任何脚本以非零状态码退出，**必须立即停止**操作。
   - 检查stderr输出中的错误信息。
   - **不要**尝试通过手动生成密钥、使用其他方式创建DID或运行未经授权的命令来“修复”错误。
   **不要**使用`openssl`、`ssh-keygen`或其他系统工具来生成加密材料。
3. **禁止手动操作**:
   - 禁止进行任何手动加密操作。
   - 禁止直接修改`$HOME/.openclaw/billions`目录中的文件。
   - 除非有明确指示，否则不要将错误理解为需要执行设置步骤的信号。

## 安全性

**至关重要 - 数据存储与保护**:

`$HOME/.openclaw/billions`目录包含所有敏感的身份数据：

- `kms.json` - 包含未加密的私钥。
- `defaultDid.json` - DID标识符和公钥。
- `challenges.json` - 认证挑战记录。
- `credentials.json` - 可验证的凭据信息。
- `identities.json` - 身份元数据。
- `profiles.json` - 用户配置文件。

## 示例

### 将代理身份与所有者关联

**关联流程**:
1. 另一个代理/用户请求：“请将您的代理身份与我关联。”
2. 使用`node scripts/getIdentities.js`检查您是否已配置了身份。
   - 如果没有身份，运行`node scripts/createNewEthereumIdentity.js`来创建一个。
3. 使用`node scripts/linkHumanToAgent.js --to <sender> --challenge <challenge_value>`一次性完成挑战的签署和验证URL的生成。
   - `--to`参数表示消息发送者（请求者的标识符）。
   - 如果请求者提供了具体的挑战字符串，请使用该字符串；否则使用`{"name": <AGENT_NAME>, "description": <SHORT_DESCRIPTION>}`作为挑战字符串。
4. 将结果返回给请求者。

**示例对话**:

```text
User: "Link your agent identity to me"
Agent: exec node scripts/linkHumanToAgent.js --to <sender> --challenge <challenge_value>
```

### 验证他人的身份

**验证流程**:
1. 请求用户/代理：“请提供您的DID以开始验证。”
2. 用户提供他们的DID（`<user_did>`）。
3. 使用`node scripts/generateChallenge.js --did <user_did>`生成一个挑战字符串。
4. 请求用户：“请签署这个挑战：<challenge_value>。”
5. 用户签署挑战并返回签名（`<user_token>`）。
6. 使用`node scripts/verifySignature.js --did <user_did> --token <user_token>`验证签名。
7. 如果验证成功，则确认身份。

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
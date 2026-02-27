---
name: archon-keymaster
description: >
  **Core Archon DID 工具包**  
  - **身份管理**：支持创建和管理数字身份（DIDs）。  
  - **可验证的凭证**：提供安全、可验证的认证机制。  
  - **加密通信**：支持使用加密技术进行安全消息传递（dmail）。  
  - **Nostr 集成**：可与 Nostr 平台无缝集成。  
  - **文件加密/签名**：能够对文件进行加密和签名操作。  
  - **别名管理**：允许为数字身份设置别名。  
  - **授权机制**：支持基于挑战/响应（challenge/response）的授权流程。  
  - **组管理**：支持对数字身份进行分组管理。  
  - **加密投票**：提供加密投票功能。  
  **主要功能用途**：  
  - 用于创建和管理数字身份（DIDs）。  
  - 发行和接收可验证的认证凭证。  
  - 在数字身份之间发送加密消息。  
  - 派生 Nostr 密钥对。  
  - 对文件进行加密和签名。  
  - 管理数字身份的别名。  
  - 实现基于挑战/响应的授权机制。  
  - 管理数字身份的组。  
  - 运行加密投票功能。  
  **相关工具**：  
  - **archon-vault**：用于数据存储和备份。  
  - **archon-cashu**：用于管理电子现金（ecash）。
metadata:
  openclaw:
    requires:
      env:
        - ARCHON_WALLET_PATH
        - ARCHON_PASSPHRASE
        - ARCHON_GATEKEEPER_URL
      bins:
        - node
        - npx
      anyBins:
        - jq
        - openssl
    primaryEnv: ARCHON_PASSPHRASE
    emoji: "🔐"
---
# Archon Keymaster - 核心去中心化身份（DID）工具包

Archon去中心化身份（DID）的核心工具包，负责管理身份生命周期、加密通信、加密操作和授权功能。

**相关技能：**
- `archon-vault` — 用于管理加密分布式备份的仓库
- `archon-cashu` — 基于DID的Cashu电子货币系统

## 功能

- **身份管理** - 创建、管理多个DID，通过助记词恢复身份
- **可验证的凭证** - 创建、发放/接受/撤销凭证
- **加密消息（Dmail）** - 在DID之间发送/接收端到端加密消息
- **Nostr集成** - 从您的DID派生Nostr密钥对（使用相同的secp256k1密钥）
- **文件加密** - 为特定DID加密文件
- **数字签名** - 使用您的DID对文件进行签名和验证
- **DID别名** - 为DID提供友好名称（联系人、凭证等）
- **授权** - 在DID之间进行挑战/响应验证
- **组** - 创建和管理DID组以实现访问控制和多方操作
- **投票** - 支持透明或秘密投票的加密投票
- **资产** - 在注册表中存储和检索基于内容地址的资产

## 先决条件

- 安装了Node.js（用于运行`npx @didcid/keymaster`）
- 需要`~/.archon.env`环境文件，其中包含以下配置：
  - `ARCHON_WALLET_PATH` - 钱包文件的路径（必需）
  - `ARCHON_PASSPHRASE` - 钱包加密密码短语（必需）
  - `ARCHON_GATEKEEPER_URL` - 网关守护程序的URL（可选，默认为公共节点）
- 所有配置项均由`create-id.sh`脚本自动生成

## 安全注意事项

本工具包处理加密身份相关操作：

1. **密码短语的存储**：`ARCHON_PASSPHRASE`存储在`~/.archon.env`文件中，仅用于非交互式脚本执行。该文件应设置为`chmod 600`权限。
2. **敏感文件**：
   - `~/.archonwallet.json` — 包含DID私钥的加密钱包文件
   - `~/.archon.env` — 包含钱包加密密码短语
3. **数据传输**：数据在传输到Archon网关守护程序/hyperswarm之前会被加密，只有指定接收者才能解密。
4. **密钥恢复**：您的12词助记词是主要的恢复密钥，请将其存储在离线环境中，切勿以数字形式保存。

## 快速入门

### 首次设置

```bash
./scripts/identity/create-id.sh [wallet-path]
```

创建您的第一个DID，生成密码短语，并将其保存到`~/.archon.env`文件中。
- 默认钱包位置：`~/.archonwallet.json`
- 您可以指定自定义路径：`./scripts/identity/create-id.sh ~/my-wallet.json`
- **请记住您的12词助记词**——这是您的主恢复密钥。

### 加载环境配置

所有脚本都需要`~/.archon.env`文件来配置环境信息。只需运行以下命令：

```bash
source ~/.archon.env
```

该环境文件会设置`ARCHON_WALLET_PATH`和`ARCHON_PASSPHRASE`。如果这些参数未设置，脚本将报错。

## 身份管理

### 创建额外身份

```bash
./scripts/identity/create-additional-id.sh <name>
```

创建匿名身份或基于角色的身份（所有身份共享相同的助记词）。

### 列出所有DID

```bash
./scripts/identity/list-ids.sh
```

### 切换活跃身份

```bash
./scripts/identity/switch-id.sh <name>
```

### 恢复身份

有关灾难恢复和仓库恢复操作，请参阅`archon-backup`技能。

## 可验证凭证

创建和管理可验证凭证的规范。

### 创建凭证规范

```bash
./scripts/schemas/create-schema.sh <schema-file.json>
```

从JSON文件创建凭证规范。

**示例规范（proof-of-human.json）：**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$credentialContext": [
    "https://www.w3.org/ns/credentials/v2",
    "https://archetech.com/schemas/credentials/agent/v1"
  ],
  "$credentialType": [
    "VerifiableCredential",
    "AgentCredential",
    "ProofOfHumanCredential"
  ],
  "name": "proof-of-human",
  "description": "Verifies human status",
  "properties": {
    "credence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Confidence level (0-1) that subject is human"
    }
  },
  "required": ["credence"]
}
```

```bash
./scripts/schemas/create-schema.sh proof-of-human.json
# Returns: did:cid:bagaaiera4yl4xi...
```

### 列出您的凭证规范

```bash
./scripts/schemas/list-schemas.sh
```

列出您拥有的所有凭证规范。

### 获取凭证规范

```bash
./scripts/schemas/get-schema.sh <schema-did-or-alias>
```

通过DID或别名检索凭证规范定义。

## 可验证凭证

发放、接受和管理可验证凭证。

### 发放凭证（三步流程）

#### 1. 将凭证绑定到主体

```bash
./scripts/credentials/bind-credential.sh <schema-did-or-alias> <subject-did-or-alias>
```

为主体创建一个凭证模板文件。

**示例：**
```bash
./scripts/credentials/bind-credential.sh proof-of-human-schema alice
# Creates: bagaaierb...BOUND.json  (subject DID without 'did:cid:' prefix)
```

#### 2. 填写凭证数据

编辑`.BOUND.json`文件并填写`credentialSubject`数据：

```json
{
  "credentialSubject": {
    "id": "did:cid:bagaaierb...",
    "credence": 0.97
  }
}
```

#### 3. 发放凭证

```bash
./scripts/credentials/issue-credential.sh <bound-file.json>
```

对凭证进行签名和加密，并返回凭证的DID。`@didcid/keymaster`命令可能会保存输出文件——具体文件输出行为请参考Keymaster文档。

**示例：**
```bash
./scripts/credentials/issue-credential.sh bagaaierb...BOUND.json
# Returns credential DID: did:cid:bagaaierc...
```

### 接受凭证

```bash
./scripts/credentials/accept-credential.sh <credential-did>
```

接受并保存发给您们的凭证。

**示例：**
```bash
./scripts/credentials/accept-credential.sh did:cid:bagaaierc...
```

### 管理凭证

#### 列出您的凭证

```bash
./scripts/credentials/list-credentials.sh
```

列出您收到的所有凭证。

#### 列出已发放的凭证

```bash
./scripts/credentials/list-issued.sh
```

列出您发放给其他人的所有凭证。

#### 获取凭证详情

```bash
./scripts/credentials/get-credential.sh <credential-did-or-alias>
```

检索凭证的完整详细信息。

### 发布和撤销凭证

#### 发布凭证

```bash
./scripts/credentials/publish-credential.sh <credential-did>
```

将凭证添加到您的公共DID manifest中（使其对他人可见）。

#### 撤销凭证

```bash
./scripts/credentials/revoke-credential.sh <credential-did>
```

撤销您发放的凭证（使其失效）。

### 完整示例：发放proof-of-human凭证

```bash
# 1. Create schema
./scripts/schemas/create-schema.sh proof-of-human.json
# Returns: did:cid:bagaaiera4yl4xi...

# 2. Add alias for convenience
./scripts/aliases/add-alias.sh proof-of-human-schema did:cid:bagaaiera4yl4xi...

# 3. Bind credential to Alice
./scripts/credentials/bind-credential.sh proof-of-human-schema alice
# Creates: bagaaierb...BOUND.json  (alice's DID without prefix)

# 4. Edit file, set credence: 0.97

# 5. Issue credential
./scripts/credentials/issue-credential.sh bagaaierb...BOUND.json
# Returns: did:cid:bagaaierc...

# 6. Alice accepts it
./scripts/credentials/accept-credential.sh did:cid:bagaaierc...

# 7. Alice publishes to her manifest
./scripts/credentials/publish-credential.sh did:cid:bagaaierc...
```

## 加密消息（Dmail）

支持带附件的DID之间的端到端加密消息。

### 发送消息

```bash
./scripts/messaging/send.sh <recipient-did-or-alias> <subject> <body> [cc-did...]
```

示例：
```bash
./scripts/messaging/send.sh alice "Meeting" "Let's sync tomorrow"
./scripts/messaging/send.sh did:cid:bag... "Update" "Status report" did:cid:bob...
```

### 查看收件箱

```bash
./scripts/messaging/refresh.sh   # Poll for new messages
./scripts/messaging/list.sh      # List inbox
./scripts/messaging/list.sh unread  # Filter unread
```

### 阅读消息

```bash
./scripts/messaging/read.sh <dmail-did>
```

### 回复/转发/归档

```bash
./scripts/messaging/reply.sh <dmail-did> <body>
./scripts/messaging/forward.sh <dmail-did> <recipient-did> [body]
./scripts/messaging/archive.sh <dmail-did>
./scripts/messaging/delete.sh <dmail-did>
```

### 附件

```bash
./scripts/messaging/attach.sh <dmail-did> <file-path>
./scripts/messaging/get-attachment.sh <dmail-did> <attachment-name> <output-path>
```

## Nostr集成

从您的DID派生Nostr身份（使用相同的secp256k1密钥，支持两种协议）。

### 先决条件

安装`nak` CLI：
```bash
curl -sSL https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh | sh
```

### 派生Nostr密钥

```bash
./scripts/nostr/derive-nostr.sh
```

输出`nsec`、`npub`和hex pubkey（从`m/44'/0'/0'/0/0`派生）。

### 保存密钥

```bash
mkdir -p ~/.clawstr
echo "nsec1..." > ~/.clawstr/secret.key
chmod 600 ~/.clawstr/secret.key
```

### 发布Nostr配置文件

```bash
echo '{
  "kind": 0,
  "content": "{\"name\":\"YourName\",\"about\":\"Your bio. DID: did:cid:...\"}"
}' | nak event --sec $(cat ~/.clawstr/secret.key) \
  wss://relay.ditto.pub wss://relay.primal.net wss://relay.damus.io wss://nos.lol
```

### 使用Nostr身份更新DID

```bash
npx @didcid/keymaster set-property YourIdName nostr \
  '{"npub":"npub1...","pubkey":"<hex-pubkey>"}'
```

## 文件加密和签名

### 加密文件

```bash
./scripts/crypto/encrypt-file.sh <input-file> <recipient-did-or-alias>
./scripts/crypto/encrypt-message.sh <message> <recipient-did-or-alias>
```

返回加密后的DID（存储在链上/IPFS中）。只有接收者才能解密。

### 解密文件

```bash
./scripts/crypto/decrypt-file.sh <encrypted-did> <output-file>
./scripts/crypto/decrypt-message.sh <encrypted-did>
```

### 签名文件（作者身份证明）

```bash
./scripts/crypto/sign-file.sh <file.json>
```

**注意**：文件必须是JSON格式，并包含签名信息。

### 验证签名

```bash
./scripts/crypto/verify-file.sh <file.json>
```

显示签名者、签名时间以及文件是否被篡改。

## DID别名

为DID提供友好名称（例如使用“alice”代替`did:cid:bagaaiera...`）。

### 添加别名

```bash
./scripts/aliases/add-alias.sh <alias> <did>
```

示例：
```bash
./scripts/aliases/add-alias.sh alice did:cid:bagaaiera...
./scripts/aliases/add-alias.sh proof-of-human-schema did:cid:bagaaiera4yl4xi...
./scripts/aliases/add-alias.sh backup-vault did:cid:bagaaierab...
```

### 解析别名

```bash
./scripts/aliases/resolve-did.sh <alias-or-did>
```

直接传递时别名保持不变（如果传递的是DID）。

### 列出/删除别名

```bash
./scripts/aliases/list-aliases.sh
./scripts/aliases/remove-alias.sh <alias>
```

**注意**：别名在大多数Keymaster命令和加密/消息脚本中均有效。

## 资产管理

在分布式注册表中存储和检索资产（文件、图片、文档、JSON数据）。资产具有基于内容地址的特性（DID），并支持通过base64编码存储二进制数据。

### 列出资产

```bash
./scripts/assets/list-assets.sh
```

列出注册表中的所有资产DID。

### 创建资产

#### 从JSON数据创建

```bash
./scripts/assets/create-asset.sh '{"type":"document","title":"My Doc","content":"..."}'
```

#### 从JSON文件创建

```bash
./scripts/assets/create-asset-json.sh document.json
```

#### 从文件创建（任何类型）

```bash
./scripts/assets/create-asset-file.sh document.pdf application/pdf
```

将文件编码为base64格式，并附加元数据（文件名、内容类型）。

#### 从图片创建

```bash
./scripts/assets/create-asset-image.sh avatar.png
```

自动检测图片类型（png/jpg/gif/webp/svg）并编码。

### 检索资产

#### 获取原始资产数据

```bash
./scripts/assets/get-asset.sh did:cid:bagaaiera...
```

返回原始资产数据。

#### 以JSON格式获取资产

```bash
./scripts/assets/get-asset-json.sh did:cid:bagaaiera...
```

以美观的方式显示资产数据。

#### 获取文件资产

```bash
./scripts/assets/get-asset-file.sh did:cid:bagaaiera... [output-path]
```

解码base64格式的文件并保存到磁盘。如果未提供输出路径，会自动检测文件名。

#### 获取图片资产

```bash
./scripts/assets/get-asset-image.sh did:cid:bagaaiera... [output-path]
```

解码base64格式的图片并保存。如果未提供输出路径，会自动检测文件名。

### 更新资产

#### 使用JSON数据更新

```bash
./scripts/assets/update-asset.sh did:cid:bagaaiera... '{"updated":true}'
```

#### 使用JSON文件更新

```bash
./scripts/assets/update-asset-json.sh did:cid:bagaaiera... updated.json
```

#### 使用文件更新

```bash
./scripts/assets/update-asset-file.sh did:cid:bagaaiera... newdoc.pdf application/pdf
```

#### 使用图片更新

```bash
./scripts/assets/update-asset-image.sh did:cid:bagaaiera... newavatar.png
```

### 转移资产所有权

```bash
./scripts/assets/transfer-asset.sh did:cid:bagaaiera... did:cid:bagaaierat...
```

将资产所有权转移给另一个DID。

## 使用场景

- **技能包**：将SKILL.md文件和脚本作为已签名的资产存储
- **个人资料媒体**：头像图片、横幅
- **文档**：PDF文件、Markdown文件、归档文件
- **数据集**：JSON数据集、配置文件
- **共享资源**：在DID之间传输资产以进行协作

## 组

管理DID集合以实现访问控制、多方操作和组织结构。

### 创建组

```bash
./scripts/groups/create-group.sh <group-name>
```

创建一个组，并自动为其设置别名。

示例：
```bash
./scripts/groups/create-group.sh research-team
./scripts/groups/create-group.sh archetech-devs
```

### 添加/删除成员

```bash
./scripts/groups/add-member.sh <group> <member-did-or-alias>
./scripts/groups/remove-member.sh <group> <member-did-or-alias>
```

示例：
```bash
./scripts/groups/add-member.sh research-team did:cid:bagaaiera...
./scripts/groups/add-member.sh devs alice
./scripts/groups/remove-member.sh devs alice
```

### 列出组

```bash
./scripts/groups/list-groups.sh
```

列出当前身份拥有的所有组。

### 获取组详情

```bash
./scripts/groups/get-group.sh <group-did-or-alias>
```

显示组的元数据和成员信息。

### 测试成员资格

```bash
./scripts/groups/test-member.sh <group> [member]
```

如果省略了成员参数，会检查当前身份是否属于该组。

示例：
```bash
./scripts/groups/test-member.sh research-team           # Am I in this group?
./scripts/groups/test-member.sh research-team alice     # Is alice in this group?
```

### 使用场景

- **访问控制**：为某个组加密文件，所有成员都可以解密
- **团队管理**：按角色或项目组织DID
- **多方工作流程**：定义谁可以参与组内操作

## 授权

通过挑战/响应流程验证DID是否控制其私钥。用于代理间认证、访问控制和身份验证。

### 创建挑战

```bash
# Create a basic challenge
./scripts/auth/create-challenge.sh

# Create a challenge as a specific DID alias
./scripts/auth/create-challenge.sh --alias myDID

# Create a challenge from a file
./scripts/auth/create-challenge.sh challenge-template.json

# Create a challenge tied to a specific credential
./scripts/auth/create-challenge-cc.sh did:cid:bagaaiera...
```

输出一个挑战DID（例如`did:cid:bagaaiera...`），接收者需要对该DID进行签名。

### 创建响应

```bash
CHALLENGE="did:cid:bagaaiera..."
./scripts/auth/create-response.sh "$CHALLENGE"
```

输出一个包含签名证明的响应DID。

### 验证响应

```bash
RESPONSE="did:cid:bagaaiera..."
./scripts/auth/verify-response.sh "$RESPONSE"
```

输出：
```json
{
    "challenge": "did:cid:...",
    "credentials": [],
    "requested": 0,
    "fulfilled": 0,
    "match": true,
    "responder": "did:cid:..."
}
```

`match: true`表示响应有效且经过加密验证。

### 完整的授权流程

```bash
# Challenger creates a challenge
CHALLENGE=$(./scripts/auth/create-challenge.sh)

# Responder creates a response (proves they control their DID)
RESPONSE=$(./scripts/auth/create-response.sh "$CHALLENGE")

# Challenger verifies the response
./scripts/auth/verify-response.sh "$RESPONSE"
# → {"match": true, "responder": "did:cid:...", ...}
```

## 投票

支持透明或秘密投票的加密验证机制。投票者可以直接加入投票（无需单独的投票列表）。

### 创建投票模板

```bash
./scripts/polls/create-poll-template.sh
```

输出一个v2版本的投票模板JSON文件：
```json
{
    "version": 2,
    "name": "poll-name",
    "description": "What is this poll about?",
    "options": ["yes", "no", "abstain"],
    "deadline": "2026-03-01T00:00:00.000Z"
}
```

### 创建投票

```bash
./scripts/polls/create-poll.sh <poll-file.json> [options]
```

从JSON模板文件创建投票。返回投票的DID。

**选项：**
- `--alias TEXT` - 投票的别名
- `--registry TEXT` - 注册表URL（默认为hyperswarm）

**示例：**
```bash
# Create poll template
./scripts/polls/create-poll-template.sh > my-poll.json

# Edit poll (set name, description, options, deadline)
vi my-poll.json

# Create the poll
./scripts/polls/create-poll.sh my-poll.json
# Returns: did:cid:bagaaiera...
```

### 管理投票者

添加、删除或列出投票者：

```bash
# Add a voter
./scripts/polls/add-poll-voter.sh <poll-did> <voter-did>

# Remove a voter
./scripts/polls/remove-poll-voter.sh <poll-did> <voter-did>

# List all eligible voters
./scripts/polls/list-poll-voters.sh <poll-did>
```

### 在投票中投票

```bash
./scripts/polls/vote-poll.sh <poll-did> <vote-index>
```

在投票中投票。返回投票的DID。

**参数：**
- `poll-did` - 投票的DID
- `vote-index` - 投票编号：0 = 投票无效；1-N = 选项索引

**示例：**
```bash
# View poll first to see options
./scripts/polls/view-poll.sh did:cid:bagaaiera...
# Options: 1=yes, 2=no, 3=abstain

# Cast a vote for "yes" (option 1)
./scripts/polls/vote-poll.sh did:cid:bagaaiera... 1
# Returns: did:cid:bagaaierballot...

# Spoil ballot (vote 0)
./scripts/polls/vote-poll.sh did:cid:bagaaiera... 0
```

### 投票流程

对于分布式投票（投票者不直接连接到投票发起者）：

```bash
# Voter creates and sends ballot
BALLOT=$(./scripts/polls/vote-poll.sh "$POLL" 1)
./scripts/polls/send-ballot.sh "$BALLOT" "$POLL"

# Poll owner receives and adds ballot
./scripts/polls/update-poll.sh "$BALLOT"

# View ballot details
./scripts/polls/view-ballot.sh "$BALLOT"
```

### 发送投票通知

通知所有投票者有关投票的信息：

```bash
./scripts/polls/send-poll.sh <poll-did>
```

创建一个通知DID，投票者可以使用该DID找到并参与投票。

### 查看投票

```bash
./scripts/polls/view-poll.sh <poll-did>
```

查看投票详情，包括选项、截止日期和（如果已发布）结果。

### 发布投票结果

有两种结果发布方式：

**秘密投票（默认）：**
```bash
./scripts/polls/publish-poll.sh <poll-did>
```
发布汇总结果，同时隐藏个别投票者的投票情况。

**透明投票：**
```bash
./scripts/polls/reveal-poll.sh <poll-did>
```
发布包含所有投票者投票情况的详细结果。

### 取消发布投票结果

```bash
./scripts/polls/unpublish-poll.sh <poll-did>
```

从投票中移除已发布的结果。

### 完整的投票示例

```bash
# 1. Create poll template
./scripts/polls/create-poll-template.sh > team-vote.json

# 2. Edit poll:
# {
#   "version": 2,
#   "name": "proposal-vote",
#   "description": "Should we adopt the new proposal?",
#   "options": ["approve", "reject", "defer"],
#   "deadline": "2026-03-01T00:00:00.000Z"
# }

# 3. Create the poll
POLL=$(./scripts/polls/create-poll.sh team-vote.json)
echo "Poll created: $POLL"

# 4. Add eligible voters
./scripts/polls/add-poll-voter.sh "$POLL" did:cid:alice...
./scripts/polls/add-poll-voter.sh "$POLL" did:cid:bob...
./scripts/polls/add-poll-voter.sh "$POLL" did:cid:carol...

# 5. Notify voters
./scripts/polls/send-poll.sh "$POLL"

# 6. Members vote (1=approve, 2=reject, 3=defer)
./scripts/polls/vote-poll.sh "$POLL" 1   # Alice votes approve
./scripts/polls/vote-poll.sh "$POLL" 2   # Bob votes reject
./scripts/polls/vote-poll.sh "$POLL" 1   # Carol votes approve

# 7. View current status
./scripts/polls/view-poll.sh "$POLL"

# 8. After deadline, publish results (hiding who voted what)
./scripts/polls/publish-poll.sh "$POLL"

# OR publish transparently
./scripts/polls/reveal-poll.sh "$POLL"
```

### 使用场景

- **治理决策**：采用DAO风格的投票机制，结果可验证
- **团队共识**：匿名反馈或透明决策
- **多代理协调**：代理对共享资源进行投票
- **访问控制**：投票决定组成员的加入/移除

## 高级用法

### 多个身份（匿名角色）

```bash
./scripts/identity/create-additional-id.sh pseudonym
./scripts/identity/create-additional-id.sh work-persona
./scripts/identity/switch-id.sh pseudonym
```

使用场景：
- 区分个人身份和工作身份
- 匿名参与
- 基于角色的访问控制

### Dmail消息格式

Dmail消息采用JSON格式：

```json
{
  "to": ["did:cid:recipient1", "did:cid:recipient2"],
  "cc": ["did:cid:cc-recipient"],
  "subject": "Subject line",
  "body": "Message body",
  "reference": "did:cid:original-message"
}
```

**直接使用的Keymaster命令：**
```bash
npx @didcid/keymaster create-dmail message.json
npx @didcid/keymaster send-dmail <dmail-did>
npx @didcid/keymaster file-dmail <dmail-did> "inbox,important"
```

### 签名验证

签名文件包含签名证明：

```json
{
  "data": {"your": "content"},
  "proof": {
    "type": "EcdsaSecp256k1Signature2019",
    "created": "2026-02-10T20:41:26.323Z",
    "verificationMethod": "did:cid:bagaaiera...#key-1",
    "proofValue": "wju2GCn0QweP4bH6..."
  }
}
```

## 安全注意事项

### 加密安全

- **助记词是主要恢复密钥**：请将其存储在离线环境中，切勿以数字形式保存
- **密码短语用于加密钱包**：保护`wallet.json`文件的安全
- **别名是本地的**：不共享，完全去中心化
- **Dmail消息是端到端加密的**：只有发送者和接收者才能读取
- **签名是不可否认的**：无法否认创建了有效的签名
- **备份数据持久化**：只要有任何hypswarm节点保留备份数据，备份就有效

### 数据访问权限

本工具包会访问敏感数据：

| 数据 | 脚本 | 用途 |
|------|---------|---------|
| `~/.archonwallet.json` | 所有脚本 | 包含加密的私钥 |
| `~/.archon.env` | 所有脚本 | 包含用于非交互式操作的`ARCHON_PASSPHRASE` |
| `~/.clawstr/secret.key` | Nostr相关脚本 | 存储派生的Nostr私钥 |

### 环境变量

以下变量在`~/.archon.env`文件中设置：
- `ARCHON_WALLET_PATH` - 钱包文件的路径
- `ARCHON_PASSPHRASE` - 钱包解密密码短语（敏感信息！）
- `ARCHON_GATEKEEPER_URL` - 可选，默认为公共网关守护程序

**重要提示**：`~/.archon.env`文件以明文形式存储密码短语，用于脚本自动化。请确保：

```bash
chmod 600 ~/.archon.env  # Owner read/write only
```

### 网络传输

脚本会连接到以下地址：
- `https://archon.technology` - 公共网关守护程序（默认）
- `localhost:4224` - 本地网关守护程序（如果已配置）
- Hyperswarm DHT - 分布式存储网络

所有传输的数据都会被加密。没有任何明文敏感信息会离开您的设备。

## 故障排除

### 钱包/密码短语问题

**“无法读取钱包”：**
```bash
source ~/.archon.env
ls -la ~/clawd/wallet.json
```

**“权限被拒绝”：**
```bash
chmod 600 ~/.archon.env
```

### 加密/签名问题

**“无法解密”：**
- 确保消息是为您的DID加密的
- 检查密码短语是否正确

**“签名验证失败”：**
- 签名后的文件被修改
- 签名者的DID可能已被撤销

### Dmail问题

**“消息无法送达”：**
```bash
./scripts/messaging/refresh.sh  # Poll for new messages
```

**“接收者无法解密”：**
- 使用正确的接收者DID（确保接收者端使用的别名正确）

## 参考资料

- Archon官方文档：https://github.com/archetech/archon
- Keymaster相关文档：https://github.com/archetech/archon/tree/main/keymaster
- W3C DID规范：https://www.w3.org/TR/did-core/
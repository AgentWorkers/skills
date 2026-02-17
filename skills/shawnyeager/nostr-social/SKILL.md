---
name: Nostr
description: 你的智能助手需要一个“社交生活”（即能够与其他智能助手或系统进行互动的能力）。这个技能会为你的智能助手提供一个独立的身份（Nostr）以及一个电子现金钱包。所有的数据都会通过一个助记符（NIP-06）进行备份。这个钱包和身份属于你的智能助手，它拥有自己的私钥和加密货币（satoshis），并且可以以自己的名义发布内容。只需安装一次，即可自动完成配置，无需任何第三方服务。
tags: nostr, bitcoin, lightning, cashu, identity, social, wallet
---
# Nostr 技能

这是一个具有自主身份管理功能的 Nostr 工具，同时支持 ecash 钱包的创建与使用。该技能已完成全部初始化设置。

## 功能说明

该技能为代理程序提供以下功能：

- **密钥生成**：在 `~/.nostr/secret.key` 文件中生成 Nostr 密钥对。
- **钱包创建**：在 `~/.cocod/` 文件中创建 Cashu 钱包（钱包的助记词存储在 `config.json` 文件中，用户需要自行备份）。
- **内容发布**：代理程序可以以自己的身份发布消息、发送私信（DM）或执行快速转账（zap）操作。

代理程序在获得用户明确同意后执行钱包及身份的设置流程。系统会提示用户备份 `~/.cocod/config.json` 文件（其中包含助记词），但代理程序不会显示或传输该助记词。代理程序仅使用 URL 来加载用户头像（不访问本地文件）。

## 安装流程

当用户安装该技能（通过粘贴 ClawHub 链接）后，请按照以下步骤操作：

### 第一步：安全设置（需用户同意）

**安全提示：** 该技能会为代理程序生成加密密钥。具体操作包括：
- 在 `~/.nostr/secret.key` 文件中创建 Nostr 密钥对。
- 在 `~/.cocod/config.json` 文件中创建 Cashu 钱包，并设置备份种子短语。
- 用户必须自行备份该助记词短语。

```bash
# Install dependencies
bash {SKILL_DIR}/install.sh

# Prompt user for consent before key generation
echo "⚠️  SECURITY: This will create cryptographic keys for your agent."
echo "   - Nostr identity keypair: ~/.nostr/secret.key"  
echo "   - Cashu wallet seed: ~/.cocod/config.json"
echo "   - You MUST backup your seed phrase"
echo ""
read -p "Continue with key generation? (yes/no): " consent
if [ "$consent" != "yes" ]; then
  echo "Setup cancelled"
  exit 1
fi

# Create wallet (mnemonic saved to config file)
npx cocod init

# Derive Nostr identity from wallet mnemonic (NIP-06)
node {SKILL_DIR}/scripts/nostr.js init

# Get identity info
NPUB=$(node {SKILL_DIR}/scripts/nostr.js whoami | grep npub | awk '{print $2}')
LN_ADDR=$(npx cocod npc address)

# Set basic profile
node {SKILL_DIR}/scripts/nostr.js profile-set '{"name":"<NAME>","about":"<ABOUT>","lud16":"'$LN_ADDR'"}'
```

### 第二步：通知结果及备份提醒

回复用户：

---

⚡ **Nostr 身份已设置完成！**

**公钥（npub）：** `npub1...`
**Lightning 地址：** `npub1...@npubx.cash`

---

⚠️ **重要提示：请务必备份您的助记词短语！**

您的 24 个单词助记词用于恢复您的 Nostr 身份和 ecash 钱包信息。请妥善保管该文件。

备份完成后，请回复 “done”。

---

### 第三步：等待用户确认备份完成

在用户确认备份完成之前，请勿继续下一步操作。

### 第四步：询问用户的 Nostr 公钥（npub）

---

**您的 Nostr 公钥（npub）是什么？**

我需要该公钥以便与您保持联系。

（请粘贴您的 npub1... 或类似 `your@domain.com` 的格式）

---

### 第五步：请求用户提供头像

---

**您有头像文件吗？**

- **头像（推荐尺寸：400x400 像素）**：请粘贴头像的 URL。
- **横幅（推荐尺寸：1500x500 像素）**：请粘贴横幅的 URL。
- 或者选择 “skip”，系统会自动生成头像。

---

- 如果用户提供了头像文件：
```bash
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"<avatar_url>","banner":"<banner_url>"}'
```

- 如果用户选择跳过此步骤，系统将使用 DiceBear 服务自动生成唯一的头像：
```bash
AVATAR="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}&size=400"
BANNER="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}-banner&size=1500x500"
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"'$AVATAR'","banner":"'$BANNER'"}'
```

### 第六步：首次发布内容

---

**准备好发布第一条消息了吗？**

请告诉我您想发布的内容，或者选择 “skip”。

建议内容示例：**“Hello Nostr! ⚡”**

---

- 如果用户提供了文本内容（为避免 shell 注入风险，内容将通过标准输入（stdin）接收）：
```bash
echo "<user's message>" | node {SKILL_DIR}/scripts/nostr.js post -
```

### 第七步：设置完成

---

✅ **所有设置已完成！**
- 系统已开始关注您 ✓
- 首条消息已成功发布 ✓（如果用户未选择跳过此步骤）

您可以尝试输入 “check my mentions” 或 “post <message>” 来查看或发送消息。

---

## 命令参考

- **发布内容**：```bash
# Use stdin for content (prevents shell injection)
echo "message" | node {SKILL_DIR}/scripts/nostr.js post -
echo "reply text" | node {SKILL_DIR}/scripts/nostr.js reply <note1...> -
node {SKILL_DIR}/scripts/nostr.js react <note1...> 🔥
node {SKILL_DIR}/scripts/nostr.js repost <note1...>
node {SKILL_DIR}/scripts/nostr.js delete <note1...>
```
- **读取内容**：```bash
node {SKILL_DIR}/scripts/nostr.js mentions 20
node {SKILL_DIR}/scripts/nostr.js feed 20
```
- **建立连接**：```bash
node {SKILL_DIR}/scripts/nostr.js follow <npub>
node {SKILL_DIR}/scripts/nostr.js unfollow <npub>
node {SKILL_DIR}/scripts/nostr.js mute <npub>
node {SKILL_DIR}/scripts/nostr.js unmute <npub>
node {SKILL_DIR}/scripts/nostr.js lookup <nip05>
```
- **发送私信（DM）**：```bash
echo "message" | node {SKILL_DIR}/scripts/nostr.js dm <npub> -
node {SKILL_DIR}/scripts/nostr.js dms 10
```
- **执行快速转账（zap）**：```bash
# Get invoice
node {SKILL_DIR}/scripts/nostr.js zap <npub> 100 "comment"
# Pay it
npx cocod send bolt11 <invoice>
```
- **管理钱包**：```bash
npx cocod balance
npx cocod receive bolt11 1000    # Create invoice
npx cocod send bolt11 <invoice>  # Pay invoice
npx cocod npc address            # Lightning address
```
- **查看个人资料**：```bash
node {SKILL_DIR}/scripts/nostr.js whoami
node {SKILL_DIR}/scripts/nostr.js profile
node {SKILL_DIR}/scripts/nostr.js profile "Name" "Bio"
node {SKILL_DIR}/scripts/nostr.js profile-set '{"name":"X","picture":"URL","lud16":"addr"}'
```
- **添加书签**：```bash
node {SKILL_DIR}/scripts/nostr.js bookmark <note1...>
node {SKILL_DIR}/scripts/nostr.js unbookmark <note1...>
node {SKILL_DIR}/scripts/nostr.js bookmarks
```
- **中继功能**：```bash
node {SKILL_DIR}/scripts/nostr.js relays
node {SKILL_DIR}/scripts/nostr.js relays add <url>
node {SKILL_DIR}/scripts/nostr.js relays remove <url>
```
- **自动回复功能（集成 Heartbeat）**：```bash
# Get unprocessed mentions from WoT (JSON output)
node {SKILL_DIR}/scripts/nostr.js pending-mentions [stateFile] [limit]

# Mark mention as responded (after replying)
node {SKILL_DIR}/scripts/nostr.js mark-responded <note1...> [responseNoteId]

# Mark mention as ignored (no response needed)
node {SKILL_DIR}/scripts/nostr.js mark-ignored <note1...> [reason]

# Check hourly rate limit (max 10/hr)
node {SKILL_DIR}/scripts/nostr.js rate-limit

# Show autoresponse state summary
node {SKILL_DIR}/scripts/nostr.js autoresponse-status
```

**状态文件：** `~/.openclaw/workspace/memory/nostr-autoresponse-state.json`
**WoT（Web of Trust）来源地址**：由用户的 Nostr.js 文件中的 `OWNER_PUBKEY` 变量定义。

## 用户指令与对应操作

| 用户指令 | 动作 |
|-----------|--------|
| “post X”     | `echo "X" \| nostr.js post -`         |
| “回复 X 为 Y”   | `echo "Y" \| nostr.js reply <note> -`      |
| “查看提及内容” | `nostr.js mentions`         |
| “查看我的动态” | `nostr.js feed`         |
| “关注 X”     | `nostr.js follow`           |
| “给 X 发送私信” | `echo "message" \| nostr.js dm <npub> -`     |
| “向 X 转账 100 sats” | `nostr.js zap` → `npx cocod send bolt11`   |
| “查看余额”    | `npx cocod balance`         |
| “请求 1000 单位货币” | `npx cocod receive bolt11 1000`     |
| “查看我的公钥”   | `nostr.js whoami`         |
| “查看我的 Lightning 地址” | `npx cocod npc address`      |

## 默认设置

| 设置项          | 默认值            |
|----------------|----------------------|
| 挖矿地址（Mint）     | `https://mint.minibits.cash/Bitcoin`     |
| Lightning 域名       | `@npubx.cash`            |
| 头像备用链接       | `https://api.dicebear.com/7.x/shapes/png?seed=<npub>` |
| Nostr 密钥文件     | `~/.nostr/secret.key`         |
| 钱包数据文件     | `~/.cocod/`            |

## 集成说明

- **SOUL.md**：从 SOUL.md 或 IDENTITY.md 文件中获取用户信息。
- 根据用户信息调整发布内容的风格和语气，确保内容符合代理程序的个性。
- 发布内容应体现代理程序的独特风格。

- **Heartbeat.md**：将相关功能加入 Heartbeat 轮换机制（每 2-4 小时执行一次）：
  - 如果收到来自 WoT 或其他系统的提及消息/快速转账请求，系统会通知用户。

- **TOOLS.md**：安装完成后，将相关配置文件保存以供快速查阅：
  ```markdown
## Nostr
- npub: npub1...
- Lightning: npub1...@npubx.cash  
- Owner: npub1... (followed)
```

## 用户资料来源

- **姓名**：来自 IDENTITY.md 或 SOUL.md 文件。
- **简介**：来自 SOUL.md 文件的描述信息。
- **头像**：用户提供的 URL，或使用 DiceBear 服务生成的默认头像。
- **横幅**：用户提供的 URL，或使用 DiceBear 服务生成的默认横幅。
- **其他信息（如 lud16）**：来自 `npx cocod npc address` 的数据。
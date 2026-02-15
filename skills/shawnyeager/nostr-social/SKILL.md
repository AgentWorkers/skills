---
name: Nostr
description: 你的代理需要一个社交生活。那就满足它的这个需求吧。这个技能会为你的代理提供一个独立的身份（Nostr）以及一个电子现金钱包。所有数据都通过一个助记词进行备份（NIP-06）。这个钱包不是为你使用的，而是为你的代理准备的；它拥有自己的私钥、自己的加密货币（satoshis），并且可以以自己的名义发布内容。只需安装一次，系统就会自动完成初始化，无需任何第三方参与。
tags: nostr, bitcoin, lightning, cashu, identity, social, wallet
---

# Nostr 技能

这是一个具备自主身份管理和电子现金钱包功能的工具。已完成全部初始化设置。

## 功能介绍

该技能为代理程序提供以下功能：

- **密钥生成**：在 `~/.nostr/secret.key` 文件中生成 Nostr 密钥对。
- **钱包创建**：在 `~/.cocod/` 文件中创建 Cashu 钱包（相关配置信息存储在 `config.json` 中，用户可自行备份）。
- **信息发布**：以代理的身份发布内容、发送私信或执行转账操作。

代理程序会自动完成钱包和身份的配置。系统会提示用户备份 `~/.cocod/config.json` 文件（其中包含钱包的助记词），但代理程序本身不会读取或显示该助记词。代理程序仅使用 URL 来加载用户的头像文件（不访问本地文件）。

## 安装流程

当用户安装该技能（通过粘贴 ClawHub 链接）后，请按照以下步骤操作：

### 第一步：静默设置

```bash
# Install dependencies
bash {SKILL_DIR}/install.sh

# Create wallet (mnemonic saved to config file)
npx cocod init > /dev/null 2>&1

# Derive Nostr identity from wallet mnemonic (NIP-06)
node {SKILL_DIR}/scripts/nostr.js init

# Get identity info
NPUB=$(node {SKILL_DIR}/scripts/nostr.js whoami | grep npub | awk '{print $2}')
LN_ADDR=$(npx cocod npc address)

# Set basic profile
node {SKILL_DIR}/scripts/nostr.js profile-set '{"name":"<NAME>","about":"<ABOUT>","lud16":"'$LN_ADDR'"}'
```

### 第二步：通知安装结果及备份提示

回复用户：

---

⚡ **Nostr 身份已设置完成！**

**公钥（npub）：** `npub1...`
**Lightning 地址：** `npub1...@npubx.cash`

---

⚠️ **重要提示：请备份您的助记词！**

您的 24 个单词助记词存储在：
```
~/.cocod/config.json
```

该助记词可用于恢复您的 Nostr 身份和电子现金钱包，请务必妥善保管。

备份完成后，请回复 “done”。

---

### 第三步：等待用户确认备份完成

在用户确认备份完成之前，请勿继续下一步操作。

### 第四步：询问用户的 Nostr 公钥（npub）

---

**您的 Nostr 公钥是什么？**

我需要您的公钥以便后续保持联系。
（请粘贴您的 npub1... 或 NIP-05 格式的地址，例如：your@domain.com）

---

### 第五步：请求用户提供头像文件

---

**您有头像文件吗？**

- **头像（400x400 像素）**：请粘贴头像文件的 URL。
- **横幅（1500x500 像素）**：请粘贴横幅文件的 URL。
- 或者选择 “skip”，系统会自动生成头像。

---

如果用户提供了头像文件：
```bash
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"<avatar_url>","banner":"<banner_url>"}'
```

如果用户选择跳过此步骤，系统将使用 DiceBear 服务自动生成唯一的头像：
```bash
AVATAR="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}&size=400"
BANNER="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}-banner&size=1500x500"
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"'$AVATAR'","banner":"'$BANNER'"}'
```

### 第六步：首次发布内容

---

**准备好发布第一条消息了吗？**

请告诉我您想发布的内容，或者选择 “skip”。

建议内容：**“Hello Nostr! ⚡”**

---

如果用户提供了文本内容（为避免 shell 注入风险，内容将通过标准输入（stdin）传递）：
```bash
echo "<user's message>" | node {SKILL_DIR}/scripts/nostr.js post -
```

### 第七步：安装完成

---

✅ **所有设置已完成！**

- 已成功关注您 ✓
- 首条消息已成功发布 ✓（如果用户未选择跳过此步骤）

您可以尝试输入 “check my mentions” 或 “post <message>” 来查看消息或发送新消息。

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
- **读取信息**：```bash
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
- **发送私信**：```bash
echo "message" | node {SKILL_DIR}/scripts/nostr.js dm <npub> -
node {SKILL_DIR}/scripts/nostr.js dms 10
```
- **执行转账**：```bash
# Get invoice
node {SKILL_DIR}/scripts/nostr.js zap <npub> 100 "comment"
# Pay it
npx cocod send bolt11 <invoice>
```
- **查看钱包信息**：```bash
npx cocod balance
npx cocod receive bolt11 1000    # Create invoice
npx cocod send bolt11 <invoice>  # Pay invoice
npx cocod npc address            # Lightning address
```
- **编辑个人资料**：```bash
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
**通知来源（WoT）**：用户的关注列表（在 `nostr.js` 中通过 `OWNER_PUBKEY` 定义）

## 用户指令与对应操作

| 用户指令 | 操作内容 |
|-----------|--------|
| “post X”     | `echo "X" \| nostr.js post -`         |
| “回复 X 为 Y”   | `echo "Y" \| nostr.js reply <note> -`      |
| “查看提及信息” | `nostr.js mentions`         |
| “查看我的动态” | `nostr.js feed`         |
| “关注 X”     | `nostr.js follow`           |
| “给 X 发送私信” | `echo "message" \| nostr.js dm <npub> -`     |
| “向 X 转账 100 sats” | `nostr.js zap` → `npx cocod send bolt11`   |
| “查看余额”    | `npx cocod balance`         |
| “请求 1000 单位货币” | `npx cocod receive bolt11 1000`     |
| “查看我的公钥”   | `nostr.js whoami`         |
| “查看我的 Lightning 地址” | `npx cocod npc address`     |

## 默认设置

| 设置项        | 默认值                |
|--------------|----------------------|
| 货币铸造地址    | `https://mint.minibits.cash/Bitcoin`     |
| Lightning 地址    | `@npubx.cash`            |
| 头像备用链接    | `https://api.dicebear.com/7.x/shapes/png?seed=<npub>` |
| Nostr 密钥文件    | `~/.nostr/secret.key`         |
| 钱包文件路径    | `~/.cocod/`            |

## 集成说明

- **SOUL.md**：从 `SOUL.md` 或 `IDENTITY.md` 文件中获取用户信息。
- 根据用户的个性调整发布内容的语气和风格，确保发布内容符合代理程序的特点。
- 避免使用通用模板，让发布内容更具个性化。

- **Heartbeat.md**：将相关功能添加到心跳更新机制中（每 2-4 小时更新一次）：
  ```bash
# Check Nostr activity
node {SKILL_DIR}/scripts/nostr.js mentions 10
node {SKILL_DIR}/scripts/nostr.js dms 5
```
  如果收到来自 WoT 的提及或转账请求，系统会通知用户。

- **TOOLS.md**：安装完成后，将该文件保存以供快速参考：
  ```markdown
## Nostr
- npub: npub1...
- Lightning: npub1...@npubx.cash  
- Owner: npub1... (followed)
```

## 个人资料来源

- **姓名**：来自 `IDENTITY.md` 或 `SOUL.md`
- **简介**：来自 `SOUL.md` 的描述内容
- **头像**：用户提供的 URL，或使用 DiceBear 生成的备用头像
- **横幅**：用户提供的 URL，或使用 DiceBear 生成的备用横幅
- **其他信息（如 lud16）**：来自 `npx cocod npc address`
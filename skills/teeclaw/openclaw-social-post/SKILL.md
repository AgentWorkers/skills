---
name: social-post
version: 1.5.0
description: 支持在X/Twitter和Farcaster上发布文字和图片内容，并进行回复。具备多账号支持功能，能够动态检测用户的Twitter等级（基础/高级），自动调整内容格式以避免被识别为重复内容，提供草稿预览、字符验证、多线程聊天、回复功能以及图片上传功能。X API采用按使用量计费的模式，而Farcaster则采用按每次直播计费的模式。
author: 0xdas
license: MIT
tags: [twitter, farcaster, social, posting, automation, threads, x-api, consumption-based, multi-account, anti-spam]
metadata:
  openclaw:
    requires:
      bins: [bash, curl, jq, python3, shuf]
      env: [X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]
---

# 社交媒体发布功能

该技能支持自动验证字符长度并处理图片上传，可发布到 Twitter 和/或 Farcaster 平台。

**仓库地址：** [github.com/teeclaw/social-post](https://github.com/teeclaw/social-post)

## 主要功能

- ✅ **动态检测 Twitter 账户等级** - 自动识别基础账户（Basic）和高级账户（Premium），结果缓存 24 小时
- ✅ **多账户支持** - 通过一个技能管理多个 Twitter 账户
- ✅ **自动分帖** - 使用 `--vary` 标志避免 Twitter 的重复内容检测
- ✅ **高级账户支持** - 单条推文可发布最多 25,000 个字符
- ✅ **交互式分帖选择** - 高级用户可以选择单条推文或分帖发布
- ✅ 仅发布到 Twitter
- ✅ 仅发布到 Farcaster
- ✅ 同时发布到两个平台
- ✅ 回复推文和广播内容** - 可在两个平台上回复特定帖子
- ✅ 草稿预览** - 发布前会显示预览内容
- ✅ 字符/字节长度验证（根据账户等级动态调整）
- ✅ 图片上传支持（适用于帖子和回复）
- ✅ **分帖功能** - 自动将长文本分割成多条帖子
- ✅ 短链接生成** - 使用 TinyURL 压缩链接以节省字符数
- ✅ 超过限制时自动截断（可选）

## 平台限制

### Twitter 的动态字符限制（自动检测）

该技能会自动检测您的 Twitter 账户等级并调整字符限制：

- **基础/免费账户：** 252 个字符（实际可用 280 个字符，预留 10% 的安全缓冲空间）
- **高级账户：** 22,500 个字符（实际可用 25,000 个字符，预留 10% 的安全缓冲空间）

### Farcaster 的限制

- **288 字节**（实际可用 320 字节，预留 10% 的安全缓冲空间）

### 账户等级检测机制

1. **首次使用：** 在您首次发布时，该技能会调用 Twitter API 来检测您的订阅等级。
2. **缓存：** 等级信息会缓存 24 小时，以减少 API 调用次数。
3. **自动刷新：** 缓存有效期为 24 小时，下次发布时会重新检测。
4. **手动刷新：** 使用 `--refresh-tier` 标志可强制立即重新检测。

**高级账户的发布规则：**

使用高级账户发布时：
- 如果文本长度 ≤ 280 个字符 → 以单条推文的形式发布。
- 如果文本长度 > 280 个字符且 ≤ 22,500 个字符 → 首先显示草稿，询问是否分帖发布（“是否分帖？（y/n）”）
  - 如果选择“是” → 文本会被分割成多条帖子进行审核。
- 如果文本长度 > 22,500 个字符 → 会自动分帖发布（超出高级账户的字符限制）。

**强制分帖：**
- 使用 `--thread` 标志可跳过提示并强制分帖。
- 使用 `--auto-confirm` 标志可跳过所有提示，系统会自动选择最佳发布格式。

## 设置与凭据

### Twitter 设置

**所需凭据**（存储在 `/home/phan_harry/.openclaw/.env` 文件中）：
```bash
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_USERNAME=your_username
X_USER_ID=your_user_id
```

**获取凭据的方法：**

1. **申请 X 开发者账户：**
   - 访问 https://developer.twitter.com/en/portal/dashboard
   - 申请开发者访问权限
   - 等待审核通过（通常需要 1-2 天）。
2. **启用按使用量计费的支付方式：**
   - 在开发者门户中设置支付方式（信用卡）
   - 无需订阅费用，仅按实际使用的 API 请求次数收费。
   - 每次 API 请求都会被计费。
3. **创建应用程序：**
   - 在开发者门户中创建一个新的应用程序。
   - 应用程序名称：例如“Social Post Bot”
   - 设置权限为“读取和写入”。
4. **生成密钥：**
   - 在“Keys and tokens”选项卡中生成消费者密钥（Consumer Key）和秘密密钥（Secret Key）。
   - 点击“Authentication Tokens”下的“Generate”生成访问令牌（Access Token）和秘密令牌（Secret Token）。
   - 请妥善保管这 4 个凭据。

**验证凭据：**
```bash
# Dry run (won't post)
scripts/post.sh --twitter --dry-run "Test message"
```

### 多账户设置（可选）

您可以通过添加带有自定义前缀的额外凭据来管理多个 Twitter 账户。

**示例：添加第二个账户：**
```bash
# Add credentials with custom prefix (e.g., MYACCOUNT_)
echo "MYACCOUNT_API_KEY=xxx" >> ~/.openclaw/.env
echo "MYACCOUNT_API_KEY_SECRET=xxx" >> ~/.openclaw/.env
echo "MYACCOUNT_ACCESS_TOKEN=xxx" >> ~/.openclaw/.env
echo "MYACCOUNT_ACCESS_TOKEN_SECRET=xxx" >> ~/.openclaw/.env
```

**使用方法：**
```bash
# Post from default account (X_*)
scripts/post.sh --twitter "Message from default account"

# Post from custom account
scripts/post.sh --account myaccount --twitter "Message from second account"

# Reply from custom account
scripts/reply.sh --account myaccount --twitter TWEET_ID "Reply from second account"
```

**命名规则：**
- 默认账户：`X_CONSUMER_KEY`、`X_CONSUMER_SECRET` 等。
- 自定义账户：`{PREFIX}_API_KEY`、`{PREFIX}_API_KEY_SECRET`、`{PREFIX}_ACCESS_TOKEN`、`{PREFIX}_ACCESS_TOKEN_SECRET`
- 在 `--account` 标志中使用小写前缀来指定账户。

### Farcaster 设置

**所需凭据**（存储在 `/home/phan_harry/.openclaw/farcaster-credentials.json` 文件中）：
```json
{
  "fid": "your_farcaster_id",
  "custodyAddress": "0x...",
  "custodyPrivateKey": "0x...",
  "signerPublicKey": "0x...",
  "signerPrivateKey": "0x...",
  "createdAt": "2026-01-01T00:00:00.000Z"
}
```

**获取凭据的方法：**

1. **使用 farcaster-agent 技能创建账户：**
   ```bash
   # This will guide you through:
   # - Creating a wallet
   # - Registering FID
   # - Adding signer key
   # - Automatically saving credentials
   
   # See: /skills/farcaster-agent/SKILL.md
   ```

2. **或使用现有凭据：**
   - 如果您已经拥有 Farcaster 账户：
     - 导出您的保管钱包私钥（custody wallet private key）和签名器私钥（signer private key）。
     - 手动创建 `farcaster-credentials.json` 文件。
3. **为保管钱包充值（必需）：**
   ```bash
   # Check current balance
   scripts/check-balance.sh
   
   # Send USDC to custody address on Base chain
   # Minimum: 0.1 USDC (~100 casts)
   # Recommended: 1-5 USDC (1000-5000 casts)
   ```

**验证设置：**
```bash
   # Check credentials exist
   ls -la ~/.openclaw/farcaster-credentials.json
   
   # Check wallet balance
   scripts/check-balance.sh
   
   # Test posting (dry run)
   scripts/post.sh --farcaster --dry-run "Test message"
   ```

**安全注意事项：**
- ⚠️ **切勿分享您的私钥！**
- ⚠️ 凭据以明文形式存储，请确保系统安全。
- ⚠️ `.env` 文件应具有 600 权限（仅允许所有者读写）。
- ⚠️ 请妥善备份您的凭据。

## 使用方法

### 发布内容

#### 仅发布文本
```bash
# Post to both platforms
scripts/post.sh "Your message here"

# Twitter only
scripts/post.sh --twitter "Your message"

# Farcaster only
scripts/post.sh --farcaster "Your message"
```

#### 发布带有图片的内容
```bash
# Post to both platforms with image
scripts/post.sh --image /path/to/image.jpg "Your caption"

# Twitter only with image
scripts/post.sh --twitter --image /path/to/image.jpg "Caption"

# Farcaster only with image
scripts/post.sh --farcaster --image /path/to/image.jpg "Caption"
```

### 回复内容

#### 回复 Twitter 的帖子
```bash
# Reply to a tweet
scripts/reply.sh --twitter TWEET_ID "Your reply"

# Reply with image
scripts/reply.sh --twitter TWEET_ID --image /path/to/image.jpg "Reply with image"

# Get tweet ID from URL: twitter.com/user/status/[TWEET_ID]
scripts/reply.sh --twitter 1234567890123456789 "Great point!"
```

#### 回复 Farcaster 的广播内容
```bash
# Reply to a cast
scripts/reply.sh --farcaster CAST_HASH "Your reply"

# Reply with image
scripts/reply.sh --farcaster 0xabcd1234... --image /path/to/image.jpg "Reply with image"

# Get cast hash from URL: farcaster.xyz/~/conversations/[HASH]
scripts/reply.sh --farcaster 0xa1b2c3d4e5f6... "Interesting perspective!"
```

#### 同时回复两个平台的帖子
```bash
# Reply to both (if you have corresponding IDs on both platforms)
scripts/reply.sh --twitter 123456 --farcaster 0xabcd... "Great discussion!"
```

### 配置选项

#### 对于 `post.sh`（发布命令）：

- `--twitter` - 仅发布到 Twitter
- `--farcaster` - 仅发布到 Farcaster
- `--account <account_name>` - 指定要使用的 Twitter 账户（使用 `.env` 文件中的小写前缀）
- `--vary` - 自动调整文本内容以避免重复
- `--image <image_path>` - 附加图片
- `--thread` - 强制分帖
- `--refresh-tier` - 强制刷新 Twitter 账户等级缓存
- `--shorten-links` - 短链接压缩以节省字符数
- `--truncate` - 超过限制时自动截断
- `--dry-run` - 预览内容但不实际发布
- `-y, --yes` - 跳过所有确认提示（自动确认，不显示分帖提示）

#### 对于 `reply.sh`（回复命令）：

- `--twitter <tweet_id>` - 回复具有指定 ID 的 Twitter 帖子
- `--farcaster <cast_hash>` - 回复具有指定哈希值的 Farcaster 广播内容
- `--account <account_name>` - 指定要使用的 Twitter 账户（使用 `.env` 文件中的小写前缀）
- `--image <image_path>` - 附加回复图片
- `--shorten-links` - 短链接压缩以节省字符数
- `--truncate` - 超过限制时自动截断
- `--dry-run` - 预览回复内容但不实际发送
- `-y, --yes` - 跳过确认提示（自动确认）

## 示例

### 发布示例
```bash
# Quick post to both (default account)
scripts/post.sh "gm! Building onchain 🦞"

# Post from specific Twitter account
scripts/post.sh --account myaccount --twitter "Message from my second account"

# Auto-vary text to avoid duplicate content detection
scripts/post.sh --vary --twitter "Same text, subtle variations added automatically"

# Premium account - post long text (interactive choice for threading)
scripts/post.sh --twitter "Very long text that exceeds 280 characters but is under 25k... 
(The skill will detect Premium tier and ask: 'Thread this instead? (y/n)')"

# Premium account - force threading (skip prompt)
scripts/post.sh --twitter --thread "Long text that will be split into thread regardless of Premium status"

# Premium account - force single long post (skip prompt)
scripts/post.sh --twitter --auto-confirm "Long text that will post as single tweet on Premium account"

# Refresh account tier cache (if you just upgraded to Premium)
scripts/post.sh --refresh-tier --twitter "First post after upgrading to Premium"

# Twitter announcement with image
scripts/post.sh --twitter --image ~/screenshot.png "New feature shipped! 🚀"

# Farcaster only
scripts/post.sh --farcaster "Just published credential-manager to ClawHub!"

# Long text as thread (auto-numbered)
scripts/post.sh --thread "This is a very long announcement that exceeds the character limit. It will be automatically split into multiple numbered posts. Each part will be posted sequentially to create a thread. (1/3), (2/3), (3/3)"

# Shorten URLs to save characters
scripts/post.sh --shorten-links "Check out this amazing project: https://github.com/very-long-organization-name/very-long-repository-name"

# Combine thread + link shortening
scripts/post.sh --thread --shorten-links "Long text with multiple links that will be shortened and split into a thread if needed"

# Both platforms, auto-truncate long text
scripts/post.sh --truncate "Very long message that might exceed limits..."

# Preview without confirmation (for automated workflows)
scripts/post.sh --yes "Automated post from CI/CD"
```

### 回复示例
```bash
# Reply to a Twitter thread
scripts/reply.sh --twitter 1234567890123456789 "Totally agree with this take! 💯"

# Reply from specific Twitter account
scripts/reply.sh --account myaccount --twitter 1234567890 "Replying from my second account"

# Reply to Farcaster cast
scripts/reply.sh --farcaster 0xa1b2c3d4e5f6... "Great insight! Have you considered...?"

# Reply with shortened links
scripts/reply.sh --twitter 123456 --shorten-links "Here's more info: https://example.com/very-long-article-url"

# Reply with image
scripts/reply.sh --twitter 123456 --image ~/chart.png "Here's the data to support this"

# Reply to both platforms (same message)
scripts/reply.sh --twitter 123456 --farcaster 0xabc123 "This is exactly right 🎯"

# Quick reply without confirmation
scripts/reply.sh --twitter 123456 --yes "Quick acknowledgment"

# Dry run to preview reply
scripts/reply.sh --twitter 123456 --dry-run "Test reply preview"
```

## 草稿预览

发布前会显示草稿预览：
```
=== Draft Preview ===

Text to post:
─────────────────────────────────────────────
Your message here
─────────────────────────────────────────────

Targets:
  • Twitter
  • Farcaster

Proceed with posting? (y/n):
```

- **交互模式：** 显示确认提示。
- **非交互模式/自动模式：** 使用 `--yes` 标志跳过确认提示。
- **预览模式：** 使用 `--dry-run` 预览内容而不实际发布。

## 所需条件

- `.env` 文件中包含 Twitter 凭据（X_CONSUMER_KEY、X_CONSUMER_SECRET、X_ACCESS_TOKEN、X_ACCESS_TOKEN_SECRET）。
- `/home/phan_harry/.openclaw/farcaster-credentials.json` 文件中包含 Farcaster 凭据。
- **基础链（Base chain）上需要持有 USDC**：每次 Farcaster 广播费用为 0.001 USDC。
- 发布图片时需要 `curl` 和 `jq` 工具。

## 费用

### Twitter：
- **100% 按使用量计费**：无订阅等级之分。
- 每次 API 请求都会被计费。
- 无月费，无需担心等级升级。
- 费用根据实际使用情况自动计算。
- 通过 X 开发者门户使用信用卡支付。
- 支持 OAuth 1.0a 协议（无需区块链或 USDC）。
- 需要经过审核的 X 开发者账户和启用的计费功能。

**官方定价：** https://developer.twitter.com/#pricing

**重要说明：** X API 完全取消了订阅等级划分（基础账户、高级账户等）。现在采用纯按使用量计费的模式，仅根据实际使用的 API 请求次数收费。

### Farcaster：
- 每次 Farcaster 广播的费用为 0.001 USDC（通过 x402 协议支付）。
- 费用从基础链（Base chain）上的保管钱包中扣除。
- 费用会发送到 Neynar Hub（地址：`0xA6a8736f18f383f1cc2d938576933E5eA7Df01A1`）。
- 大约 1 USDC 可用于 1000 次广播。

**查询余额：**
```bash
# Quick check
scripts/check-balance.sh

# Manual check
jq -r '.custodyAddress' ~/.openclaw/farcaster-credentials.json
# View on basescan.org
```

**充值钱包：**
将 USDC 发送到基础链上的保管钱包地址。如有需要，可以从其他链转移资金。

## 图片托管

- **Twitter：** 通过 Twitter API 直接上传图片。
- **Farcaster：** 将图片上传到 imgur 并生成公开链接（可自动嵌入到广播中）。

## 错误处理

- 发布前会显示字符/字节数。
- 如果超过限制会发出警告。
- 提供截断或中止操作的选项。
- 在尝试发布前会验证凭据的有效性。
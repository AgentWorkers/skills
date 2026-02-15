---
name: social-post
version: 1.4.0
description: 可以在X/Twitter和Farcaster上发布帖子并回复，支持文本和图片的上传。该工具具备多账号支持功能，能够自动调整内容格式以避免被检测为重复内容；同时提供草稿预览、字符验证、多线程处理、回复功能以及图片上传功能。X API采用按使用量计费的模式，而Farcaster则采用按直播次数计费的模式。
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

该脚本支持自动验证字符长度和图片上传，可向 Twitter 和/或 Farcaster 发布内容。

## 主要功能

- ✅ **多账号支持**：通过一个脚本管理多个 Twitter 账号
- ✅ **自动内容变体**：使用 `--vary` 标志避免 Twitter 的重复内容检测
- ✅ 仅向 Twitter 发布
- ✅ 仅向 Farcaster 发布
- ✅ 同时向两个平台发布
- ✅ 回复推文和广播内容：在两个平台上都能回复特定帖子
- ✅ 草稿预览：在确认发布前显示实际内容
- ✅ 验证字符/字节长度
- ✅ 图片上传支持（适用于帖子和回复）
- ✅ 主题帖支持：自动将长文本分割成编号帖子
- ✅ 链接缩短：使用 TinyURL 缩短链接（节省字符）
- ✅ 超过限制时自动截断（可选）

## 平台限制

- **Twitter：** 最多 252 个字符（包含 10% 的安全缓冲区）
- **Farcaster：** 最多 288 字节（包含 10% 的安全缓冲区）

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

1. **申请 X 开发者账户**
   - 访问 https://developer.twitter.com/en/portal/dashboard
   - 申请开发者访问权限
   - 等待审核（通常需要 1-2 天）

2. **启用按使用量计费的支付方式**
   - 在开发者门户中设置支付方式（信用卡）
   - 无需订阅费用——仅按实际使用的 API 请求次数收费
   - 每次 API 请求（发布、读取等）都会产生费用
   - 无每月最低费用或额外费用

3. **创建应用程序**
   - 在开发者门户中创建一个新的应用程序
   - 应用程序名称：例如 “Social Post Bot”
   - 设置权限为 “读写”

4. **生成密钥**
   - 消费者密钥（Consumer Key）和秘密密钥（Secret Key）：在 “Keys and Tokens” 栏中
   - 访问令牌（Access Token）和秘密令牌（Secret Token）：点击 “Authentication Tokens” 下的 “Generate”
   - 安全地保存所有 4 个凭据

4. **将凭据添加到 `.env` 文件中**
```bash
   echo "X_CONSUMER_KEY=xxx" >> ~/.openclaw/.env
   echo "X_CONSUMER_SECRET=xxx" >> ~/.openclaw/.env
   echo "X_ACCESS_TOKEN=xxx" >> ~/.openclaw/.env
   echo "X_ACCESS_TOKEN_SECRET=xxx" >> ~/.openclaw/.env
   ```

**测试凭据：**
```bash
# Dry run (won't post)
scripts/post.sh --twitter --dry-run "Test message"
```

### 多账号设置（可选）

您可以通过添加带有自定义前缀的额外凭据来管理多个 Twitter 账号。

**示例：添加第二个账号**
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
- 默认账号：`X_CONSUMER_KEY`, `X_CONSUMER_SECRET` 等
- 自定义账号：`{PREFIX}_API_KEY`, `{PREFIX}_API_KEY_SECRET`, `{PREFIX}_ACCESS_TOKEN`, `{PREFIX}_ACCESS_TOKEN_SECRET`
- 在 `--account` 标志中使用小写前缀

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

1. **使用 farcaster-agent 脚本创建账户**
   ```bash
   # This will guide you through:
   # - Creating a wallet
   # - Registering FID
   # - Adding signer key
   # - Automatically saving credentials
   
   # See: /skills/farcaster-agent/SKILL.md
   ```

2. **或使用现有凭据**
   - 如果您已经拥有 Farcaster 账号：
   - 导出您的保管钱包私钥（custody wallet private key）和签名者私钥（signer private key）
   - 手动创建 JSON 文件

3. **为保管钱包充值（必需）**
   ```bash
   # Check current balance
   scripts/check-balance.sh
   
   # Send USDC to custody address on Base chain
   # Minimum: 0.1 USDC (~100 casts)
   # Recommended: 1-5 USDC (1000-5000 casts)
   ```

4. **验证设置**
   ```bash
   # Check credentials exist
   ls -la ~/.openclaw/farcaster-credentials.json
   
   # Check wallet balance
   scripts/check-balance.sh
   
   # Test posting (dry run)
   scripts/post.sh --farcaster --dry-run "Test message"
   ```

**安全提示：**
- ⚠️ **切勿共享您的私钥**
- ⚠️ 凭据以明文形式存储——请确保系统安全
- ⚠️ `.env` 文件的权限应设置为 `600`（仅允许所有者读写）
- ⚠️ 请安全地备份您的凭据

## 使用方法

### 发布内容

#### 仅文本
```bash
# Post to both platforms
scripts/post.sh "Your message here"

# Twitter only
scripts/post.sh --twitter "Your message"

# Farcaster only
scripts/post.sh --farcaster "Your message"
```

#### 带图片
```bash
# Post to both platforms with image
scripts/post.sh --image /path/to/image.jpg "Your caption"

# Twitter only with image
scripts/post.sh --twitter --image /path/to/image.jpg "Caption"

# Farcaster only with image
scripts/post.sh --farcaster --image /path/to/image.jpg "Caption"
```

### 回复内容

#### 回复 Twitter
```bash
# Reply to a tweet
scripts/reply.sh --twitter TWEET_ID "Your reply"

# Reply with image
scripts/reply.sh --twitter TWEET_ID --image /path/to/image.jpg "Reply with image"

# Get tweet ID from URL: twitter.com/user/status/[TWEET_ID]
scripts/reply.sh --twitter 1234567890123456789 "Great point!"
```

#### 回复 Farcaster
```bash
# Reply to a cast
scripts/reply.sh --farcaster CAST_HASH "Your reply"

# Reply with image
scripts/reply.sh --farcaster 0xabcd1234... --image /path/to/image.jpg "Reply with image"

# Get cast hash from URL: farcaster.xyz/~/conversations/[HASH]
scripts/reply.sh --farcaster 0xa1b2c3d4e5f6... "Interesting perspective!"
```

#### 同时回复两个平台
```bash
# Reply to both (if you have corresponding IDs on both platforms)
scripts/reply.sh --twitter 123456 --farcaster 0xabcd... "Great discussion!"
```

### 选项

#### 对于 `post.sh`（发布功能）：
- `--twitter`：仅向 Twitter 发布
- `--farcaster`：仅向 Farcaster 发布
- `--account <name>`：要使用的 Twitter 账号（使用 `.env` 文件中的小写前缀）
- `--vary`：自动修改内容以避免重复
- `--image <path>`：附加图片
- `--thread`：将长文本分割成编号帖子
- `--shorten-links`：缩短链接以节省字符
- `--truncate`：超过限制时自动截断
- `--dry-run`：预览但不实际发布
- `-y, --yes`：跳过确认提示（自动确认）

#### 对于 `reply.sh`（回复功能）：
- `--twitter <tweet_id>`：回复具有此 ID 的 Twitter 推文
- `--farcaster <cast_hash>`：回复具有此哈希值的 Farcaster 广播内容
- `--account <name>`：要使用的 Twitter 账号（使用 `.env` 文件中的小写前缀）
- `--image <path>`：在回复中附加图片
- `--shorten-links`：缩短链接以节省字符
- `--truncate`：超过限制时自动截断
- `--dry-run`：预览但不实际回复
- `-y, --yes`：跳过确认提示（自动确认）

## 示例

### 发布示例
```bash
# Quick post to both (default account)
scripts/post.sh "gm! Building onchain 🦞"

# Post from specific Twitter account
scripts/post.sh --account myaccount --twitter "Message from my second account"

# Auto-vary text to avoid duplicate content detection
scripts/post.sh --vary --twitter "Same text, subtle variations added automatically"

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

- **交互模式**：需要用户确认
- **非交互模式/自动模式**：使用 `--yes` 标志跳过确认步骤
- **预览模式**：使用 `--dry-run` 仅预览而不实际发布

## 所需条件

- `.env` 文件中包含 Twitter 凭据（X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET）
- `/home/phan_harry/.openclaw/farcaster-credentials.json` 文件中包含 Farcaster 凭据
- **Base 链上需要拥有 USDC**：每次 Farcaster 广播内容费用为 0.001 USDC
- 图片处理工具：`curl`, `jq`

## 费用

### Twitter
- **完全按使用量计费**：无订阅层级
- **每次 API 请求收费**：每次调用（发布、读取等）都会产生费用
- 无每月费用，无需担心费用等级
- 根据实际使用情况自动计费
- 通过 X 开发者门户使用信用卡支付
- 支持 OAuth 1.0a 协议（无需区块链或 USDC）
- 需要经过审核的 X 开发者账户和启用的计费功能

**官方价格信息：** https://developer.twitter.com/#pricing

**重要说明：** X API 已完全取消订阅层级（Basic、Pro 等）。现在采用纯按使用量计费的模式——仅按实际使用的 API 请求次数收费。

### Farcaster
每次 Farcaster 广播内容的费用为 0.001 USDC（通过 x402 协议支付）：
- 从 Base 链上的保管钱包中扣除费用
- 费用会发送到 Neynar Hub（地址：`0xA6a8736f18f383f1cc2d938576933E5eA7Df01A1`
- 大约 1 USDC 可用于 1000 次广播

**检查余额：**
```bash
# Quick check
scripts/check-balance.sh

# Manual check
jq -r '.custodyAddress' ~/.openclaw/farcaster-credentials.json
# View on basescan.org
```

**为钱包充值：**
将 USDC 发送到 Base 链上的保管地址。如需从其他链转移资金，请进行桥接。

## 图片托管

- **Twitter：** 通过 Twitter API 直接上传图片
- **Farcaster：** 将图片上传到 imgur 并生成公开链接（可自动嵌入）

## 错误处理

- 发布前会显示字符/字节数量
- 超过限制时会发出警告
- 提供截断或中止操作的选项
- 在尝试发布前会验证凭据的有效性
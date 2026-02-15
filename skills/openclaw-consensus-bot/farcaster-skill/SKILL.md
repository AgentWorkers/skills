---
name: farcaster-skill
description: "通过 Neynar API 在 Farcaster 上发布内容、阅读信息、进行搜索以及参与互动。当代理需要执行以下操作时可以使用该 API：  
(1) 在频道中发布带有文本的内容；  
(2) 回复或参与已发布的讨论；  
(3) 阅读用户的动态或频道的最新内容；  
(4) 根据关键词搜索发布的内容；  
(5) 通过用户名或 FID 查找用户资料；  
(6) 给内容点赞或重新发布；  
(7) 删除已发布的内容；  
(8) 列出或搜索频道。  
完全依赖 bash、curl 和 jq 工具，无需任何 npm 依赖项。"
---

# Farcaster技能（Neynar v2）

所有脚本均使用Neynar v2 REST API，需要`curl`和`jq`工具。

## 设置

请设置以下环境变量（或使用`--api-key`/`--signer`参数）：

```bash
export NEYNAR_API_KEY="your-api-key"
export NEYNAR_SIGNER_UUID="your-signer-uuid"   # required for write ops
```

或者，将凭据保存在JSON文件中并通过脚本加载：
```bash
eval $(jq -r '"export NEYNAR_API_KEY=\(.apiKey)\nexport NEYNAR_SIGNER_UUID=\(.signerUuid)"' /path/to/neynar.json)
```

## 脚本

### fc_cast.sh — 发布内容

用于发布文本，可选添加嵌入内容（embeds）、频道（channel）或回复对象（reply-to）。

```bash
# Simple text cast
scripts/fc_cast.sh --text "Hello Farcaster!"

# Cast with image/video embed
scripts/fc_cast.sh --text "Check this out" --embed "https://example.com/image.png"

# Cast with two embeds (max 2)
scripts/fc_cast.sh --text "Links" --embed "https://a.com" --embed "https://b.com"

# Post to a channel
scripts/fc_cast.sh --text "gm" --channel "base"

# Reply to a cast
scripts/fc_cast.sh --text "Great point!" --parent "0xabcdef1234..."

# Quote-cast (embed another cast)
scripts/fc_cast.sh --text "This 👆" --embed-cast "0xabcdef1234..." --embed-cast-fid 12345
```

输出格式：JSON `{success, hash}`。

### fc_feed.sh — 阅读内容推送

```bash
# User's casts by FID
scripts/fc_feed.sh --fid 3 --limit 10

# User's casts by username
scripts/fc_feed.sh --username "vitalik" --limit 5

# Channel feed
scripts/fc_feed.sh --channel "base" --limit 10

# Following feed (casts from people the signer follows)
scripts/fc_feed.sh --following --fid 3 --limit 10

# Cast replies/thread
scripts/fc_feed.sh --thread "0xabcdef..."

# Pagination with cursor
scripts/fc_feed.sh --fid 3 --cursor "eyJwYWdlIjoxfQ=="
```

输出格式：包含 `{hash, author, text, timestamp, embeds, reactions, replies}` 的内容推送列表（JSON格式）。

### fc_user.sh — 查找用户信息

```bash
# By username
scripts/fc_user.sh --username "dwr"

# By FID
scripts/fc_user.sh --fid 3

# By Ethereum address (verified)
scripts/fc_user.sh --address "0x1234..."

# Bulk by FIDs
scripts/fc_user.sh --fids "3,194,6131"
```

输出格式：包含 `{fid, username, display_name, bio, follower_count, following_count, verified_addresses}` 的用户信息（JSON格式）。

### fc_search.sh — 搜索内容

```bash
# Search by keyword
scripts/fc_search.sh --query "base chain"

# Search with author filter
scripts/fc_search.sh --query "ethereum" --author-fid 3

# Search in channel
scripts/fc_search.sh --query "gm" --channel "base"

# Limit results
scripts/fc_search.sh --query "nft" --limit 5
```

输出格式：匹配的内容列表（JSON格式）。

### fc_react.sh — 点赞/重新发布内容

```bash
# Like a cast
scripts/fc_react.sh --like "0xabcdef..."

# Unlike
scripts/fc_react.sh --like "0xabcdef..." --undo

# Recast
scripts/fc_react.sh --recast "0xabcdef..."

# Undo recast
scripts/fc_react.sh --recast "0xabcdef..." --undo
```

### fc_delete.sh — 删除内容

```bash
scripts/fc_delete.sh --hash "0xabcdef..."
```

### fc_channels.sh — 列出和搜索频道

```bash
# Search channels by keyword
scripts/fc_channels.sh --search "defi"

# Get channel details by ID
scripts/fc_channels.sh --id "base"

# List trending channels
scripts/fc_channels.sh --trending --limit 10
```

## 常用操作模式

### 发布多条内容并形成线程

```bash
HASH1=$(scripts/fc_cast.sh --text "Thread 🧵 1/3: Big news!" --channel "base" | jq -r .hash)
HASH2=$(scripts/fc_cast.sh --text "2/3: Details here..." --parent "$HASH1" | jq -r .hash)
scripts/fc_cast.sh --text "3/3: Link below" --parent "$HASH2" --embed "https://example.com"
```

### 监控提及（轮询机制）

```bash
while true; do
  scripts/fc_search.sh --query "@yourusername" --limit 5
  sleep 300
done
```

### 带媒体文件发布内容（先上传媒体文件，再添加嵌入内容）

```bash
# Upload to catbox/litterbox first
URL=$(curl -sS -F "reqtype=fileupload" -F "time=72h" \
  -F "fileToUpload=@/path/to/image.png" \
  https://litterbox.catbox.moe/resources/internals/api.php)

# Then embed the URL
scripts/fc_cast.sh --text "Check this out!" --embed "$URL"
```

## 免费版与付费版

并非所有API接口都支持Neynar的免费计划。

| 功能 | 所需脚本 | 是否免费？ |
|---------|--------|-------|
| 发布内容 | fc_cast.sh | ✅ |
| 查看用户发布的内容 | fc_feed.sh --fid | ✅ |
| 查找用户信息（用户名/FID/地址） | fc_user.sh | ✅ |
| 点赞/重新发布内容 | fc_react.sh | ✅ |
| 关注用户动态 | fc_feed.sh --following | ✅ |
| 查看频道动态 | fc_feed.sh --channel | ❌ （需付费） |
| 搜索内容 | fc_search.sh | ❌ （需付费） |
| 查看频道详情/热门内容 | fc_channels.sh | ❌ （需付费） |
| 删除内容 | fc_delete.sh | ❌ （需付费） |
| 发布多条内容并形成线程 | fc_feed.sh --thread | ✅ |

使用付费API接口的脚本会在执行失败时返回非0的退出码，并显示`402 PaymentRequired`错误信息。

## 错误处理

所有脚本在成功执行时返回0；失败时返回非0的退出码。错误信息将以JSON格式输出到标准错误流（stderr）：
```json
{"error": "message", "status": 403}
```

常见错误代码：
- `401` — API密钥无效
- `402` — 需要付费Neynar计划才能使用该功能
- `403` — 签名者未获批准或未与API密钥关联
- `404` — 未找到相关内容/用户/频道
- `429` — 日限请求次数达到上限（Neynar免费计划：每分钟300次请求）

## API参考

请参阅`references/neynar_endpoints.md`以获取完整的API接口列表和参数说明。
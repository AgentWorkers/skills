---
name: twitter
description: "通过 API 管理 X/Twitter 的消息。支持读取推文、发布推文、回复推文、发送私信、搜索以及查看分析数据。适用于用户需要与 X/Twitter 进行交互的场景，具体包括：(1) 发布或安排推文；(2) 阅读时间线、提及信息和私信；(3) 回复推文；(4) 搜索推文/用户/标签；(5) 查看互动数据分析。使用该功能需要具备 Twitter API 的认证信息（API 密钥、API 密码、访问令牌、访问密钥）或 Bearer 令牌。"
---
# Twitter/X API 技能

通过 API v2 与 Twitter（X）进行交互，支持读取、发布推文、回复、发送私信（DM）、搜索以及获取分析数据。

## 设置

### 凭据

将凭据存储在环境变量中，或保存在 `~/.config/twitter/credentials.json` 文件中：

```bash
export TWITTER_API_KEY="your-api-key"
export TWITTER_API_SECRET="your-api-secret"
export TWITTER_ACCESS_TOKEN="your-access-token"
export TWITTER_ACCESS_SECRET="your-access-secret"
export TWITTER_BEARER_TOKEN="your-bearer-token"  # For read-only operations
```

或者创建一个凭据文件：

```bash
mkdir -p ~/.config/twitter
cat > ~/.config/twitter/credentials.json << 'EOF'
{
  "api_key": "your-api-key",
  "api_secret": "your-api-secret",
  "access_token": "your-access-token",
  "access_secret": "your-access-secret",
  "bearer_token": "your-bearer-token"
}
EOF
chmod 600 ~/.config/twitter/credentials.json
```

### 安装依赖项

```bash
pip install tweepy
```

## 快速参考

| 任务 | 命令 |
|------|---------|
| 发布推文 | `{baseDir}/scripts/tweet.py post "文本"` |
| 发布带图片的推文 | `{baseDir}/scripts/tweet.py post "文本" --media image.png` |
| 回复推文 | `{baseDir}/scripts/tweet.py reply 推文ID "文本"` |
| 发布多条推文（线程） | `{baseDir}/scripts/tweet.py thread "推文1" "推文2" ...` |
| 获取时间线 | `{baseDir}/scripts/tweet.py timeline [--count 20]` |
| 获取被提及情况 | `{baseDir}/scripts/tweet.py mentions [--count 20]` |
| 获取私信 | `{baseDir}/scripts/tweet.py dms [--count 20]` |
| 发送私信 | `{baseDir}/scripts/tweet.py dm 用户名 "消息"` |
| 搜索推文 | `{baseDir}/scripts/tweet.py search "查询" [--count 20]` |
| 获取用户信息 | `{baseDir}/scripts/tweet.py user 用户名` |
| 查看推文信息 | `{baseDir}/scripts/tweet.py show 推文ID` |
| 分析推文数据 | `{baseDir}/scripts/tweet.py analytics 推文ID` |

## 脚本

### tweet.py

所有 Twitter 操作的主脚本。运行 `--help` 可查看详细信息：

```bash
{baseDir}/scripts/tweet.py --help
{baseDir}/scripts/tweet.py post --help
```

### 常见工作流程

- **发布简单推文**：
```bash
{baseDir}/scripts/tweet.py post "Hello, world!"
```

- **发布带图片的推文**：
```bash
{baseDir}/scripts/tweet.py post "Check this out!" --media photo.png
{baseDir}/scripts/tweet.py post "Multiple images" --media img1.png --media img2.png
```

- **回复推文**：
```bash
{baseDir}/scripts/tweet.py reply 1234567890 "Great point!"
```

- **发布多条推文（线程）**：
```bash
{baseDir}/scripts/tweet.py thread \
  "First tweet in thread" \
  "Second tweet" \
  "Third tweet"
```

- **查看被提及的推文**：
```bash
{baseDir}/scripts/tweet.py mentions --count 50
```

- **搜索推文**：
```bash
{baseDir}/scripts/tweet.py search "openclaw agent" --count 20
{baseDir}/scripts/tweet.py search "#AI lang:en" --count 20
```

- **获取用户信息**：
```bash
{baseDir}/scripts/tweet.py user elonmusk
```

- **发送私信**：
```bash
{baseDir}/scripts/tweet.py dm username "Hello from OpenClaw!"
```

- **查看推文分析数据**：
```bash
{baseDir}/scripts/tweet.py analytics 1234567890
```

## API 等级与限制

| 等级 | 费用 | 读取 | 写入 | 搜索 |
|------|------|------|-------|--------|
| 免费 | $0 | 有限 | - | - |
| 基础级 | $100/月 | 10,000 条/月 | 1,500 条/月 | 50 条/月 |
| 专业级 | $5,000/月 | 100 万条/月 | 300 万条/月 | 500 条/月 |

- **免费等级** 仅支持发布推文（无法读取时间线或被提及的推文）。
- **基础等级** 是读取被提及的推文、时间线和搜索功能所必需的。
- **仅写入操作** 在免费等级下也是允许的。

详细速率限制信息请参阅 `{baseDir}/references/api-limits.md`。

## 错误处理

常见错误及其解决方法：

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| 403 禁止访问 | API 等级不足 | 升级 API 等级或检查端点访问权限 |
| 429 请求过多 | 达到速率限制 | 等待片刻后重试；检查请求头中的速率限制信息 |
| 401 未经授权 | 凭据无效 | 验证 API 密钥和令牌 |
| 404 未找到 | 推文或用户已被删除 | 优雅地处理错误，并通知用户 |
| 422 无法处理 | 内容重复 | 在发布相同内容前请稍等 |

## 注意事项

- **速率限制**：Twitter API 有严格的速率限制。脚本中包含了重试逻辑。
- **媒体上传**：图片文件大小不得超过 5MB（PNG/JPG 格式）或 15MB（GIF 格式）；视频文件大小不得超过 512MB。
- **字符限制**：每条推文最多 280 个字符；多条推文（线程）可包含更多内容。
- **私信**：需要使用 OAuth 1.0a 用户认证（不能使用 Bearer 令牌）。
- **搜索操作**：高级搜索语法请参考 `{baseDir}/references/search-operators.md`。

## 相关文件

- `{baseDir}/scripts/tweet.py`：所有 Twitter 操作的主要命令行脚本
- `{baseDir}/references/api-limits.md`：各端点的详细速率限制信息
- `{baseDir}/references/search-operators.md`：Twitter 搜索语法说明
# Twitter/X 数据读取技能

这是一项综合技能，用于从 X（前身为 Twitter）的推文中读取和提取数据，支持多种可靠的数据源。

## 概述

该技能能够从 X/Twitter 的 URL 中提取完整的推文信息，包括文本内容、作者详情、互动统计信息、媒体附件以及被引用的推文。它采用多层次的方法来确保数据的最大可靠性和完整性。

## 使用场景

**主要触发条件：**
- 用户分享推文 URL（格式为 `x.com/*/status/*` 或 `twitter.com/*/status/*`）
- 用户请求“阅读这条推文”并提供 URL
- 用户要求对推文进行分析、总结或提取数据
- 用户表示需要从特定推文中获取信息

**示例用户请求：**
- “这条推文说了什么？https://x.com/elonmusk/status/123456789”
- “你能帮我阅读这条推文吗？”
- “总结这个推文讨论的内容”
- “这条推文的互动情况如何？”
- “提取这条推文中的媒体内容”

## 功能特性

### 提取的数据
- **推文内容**：包含正确格式的完整文本
- **作者信息**：显示名称和用户名（@username）
- **时间戳**：同时提供人类可读格式和原始格式
- **互动统计**：点赞数、转发数、回复数、被引用的推文数
- **媒体附件**：带有直接链接的照片和视频
- **被引用的推文**：完整的被引用推文内容及作者信息
- **推文上下文**：在可用的情况下提供

### 支持的 URL 格式
- `https://x.com/username/status/1234567890`
- `https://twitter.com/username/status/1234567890`
- 带有查询参数的 URL（例如 `?s=20`、`?t=abc123`
- 移动设备 URL（m.twitter.com 会被自动处理）

## 使用示例

### 基本用法
```bash
# Read a single tweet
./scripts/read_tweet.sh "https://x.com/username/status/1234567890"

# Read a full thread (follows reply chain from the same author)
./scripts/read_thread.sh "https://x.com/username/status/1234567890"

# Fallback method using Nitter
./scripts/read_tweet_nitter.sh "https://x.com/username/status/1234567890"
```

### 代理程序指令

当用户提供推文 URL 时：
1. **验证 URL 格式** - 确保它是有效的 X/Twitter 状态更新 URL
2. **优先使用主脚本** - 首先执行 `scripts/read_tweet.sh`
3. **优雅地处理失败情况** - 如果主脚本失败，尝试使用 `scripts/read_tweet_nitter.sh`
4. **清晰地展示数据** - 以人类可读的格式输出数据
5. **保留上下文** - 包括互动统计信息和媒体引用

### 样本响应格式

脚本返回结构化的 JSON 数据，格式如下：
```json
{
  "success": true,
  "tweet": {
    "text": "Tweet content here...",
    "author": {
      "name": "Display Name",
      "handle": "username"
    },
    "timestamp": {
      "formatted": "2024-01-15 14:30:25 UTC",
      "original": "Mon Jan 15 14:30:25 +0000 2024"
    },
    "url": "https://x.com/username/status/1234567890",
    "engagement": {
      "likes": 1250,
      "retweets": 340,
      "replies": 89,
      "quotes": 45
    },
    "media": {
      "photos": ["https://pbs.twimg.com/media/..."],
      "video": "https://video.twimg.com/..."
    },
    "quoted_tweet": {
      "text": "Quoted tweet text...",
      "author": {
        "name": "Quoted Author",
        "handle": "quoted_user"
      },
      "url": "https://x.com/quoted_user/status/987654321"
    }
  },
  "source": "fxtwitter",
  "fetched_at": 1705327825
}
```

### 代理程序响应示例

```markdown
**Tweet from @elonmusk:**
> "Just had a great meeting about sustainable transport. The future is electric! ⚡🚗"

**Posted:** January 15, 2024 at 2:30 PM UTC
**Engagement:** 1,250 likes • 340 retweets • 89 replies • 45 quotes

**Media:** 1 photo attached
- Photo: https://pbs.twimg.com/media/example.jpg

**Quote Tweet from @teslaofficial:**
> "Our latest Model S update includes new charging optimizations..."
```

## 技术实现

### 主要方法：FxTwitter API
- **端点**：`https://api.fxtwitter.com/{username}/status/{tweet_id}`
- **优点**：无需认证，数据全面，可靠性高
- **速率限制**：个人使用不受限制
- **响应**：包含所有推文元数据的完整 JSON 数据

### 备用方法：Nitter 抓取（仅供参考）
- **备用方案**：使用多个公共的 Nitter 实例作为备份
- **优点**：在 FxTwitter 不可用时仍可工作
- **限制**：仅能提取基本数据，无法获取互动统计信息
- **使用方式**：当主方法失败时自动切换到备用方法
- **注意**：自 2024 年以来，大多数公共 Nitter 实例已关闭或变得不可靠。此备用方法仅供参考，可能无法返回结果。建议优先使用 FxTwitter API。

### 错误处理
- 检测无效的 URL 格式
- 处理网络超时
- 解析 API 错误响应
- 在不同方法之间优雅地切换
- 向用户提供清晰的错误信息

## 依赖项

**必需的系统工具：**
- `curl` - 用于向 API 发送 HTTP 请求
- `jq` - 用于 JSON 解析和格式化
- `bash` - 脚本执行环境
- `grep/sed` - 用于文本处理（仅用于 Nitter 备用方案）

**可选的增强功能：**
- `gdate`（通过 Homebrew 在 macOS 上安装的 GNU date 工具） - 更好的时间戳格式化

## 安全性与隐私

### 安全特性
- ✅ **不收集外部数据** - 数据仅保存在用户系统上
- ✅ **无数据分析或监控** - 不会进行跟踪或使用情况报告
- ✅ **代码完全公开可审计** - 采用开源的 shell 脚本
- ✅ **最小化网络请求** - 仅与 FxTwitter API 和 Nitter 实例通信
- ✅ **不暴露敏感数据** - 脚本不存储或记录个人信息
- ✅ **安全的 URL 处理** - 对 URL 进行有效的验证和清理

### 网络连接
**允许访问的外部主机：**
- `api.fxtwitter.com` - 主要数据来源（FxTwitter API）
- `nitter.net` 及其他 Nitter 实例 - 备用抓取服务
- 不会建立其他外部连接

**数据流程：**
1. 用户提供推文 URL
2. 脚本从 URL 中提取用户名/ID
3. 向 FxTwitter 或 Nitter 发送 API 请求
4. 在本地解析响应
5. 返回格式化的 JSON 数据（不会永久存储）

### 审计记录
所有网络请求都会包含：
- 明确的用户代理标识
- 仅包含必要的头部信息
- 不包含认证令牌或个人标识信息
- 仅请求公开推文数据

## 错误情况与处理

### 常见错误

- **URL 格式无效**：```json
{
  "error": "Invalid Twitter/X URL format",
  "expected": "x.com/user/status/123456789 or twitter.com/user/status/123456789"
}
```
- **推文未找到**：```json
{
  "error": "API Error",
  "code": 404,
  "message": "NOT_FOUND"
}
```
- **网络故障**：```json
{
  "error": "Failed to fetch tweet data",
  "details": "Network request failed"
}
```
- **需要使用备用方法**：```json
{
  "error": "All Nitter instances failed",
  "suggestion": "Try the main script with FxTwitter API, or wait for Nitter instances to recover"
}
```

### 代理程序错误处理

当发生错误时：
1. **解析错误 JSON 以了解问题所在**
2. **如果主方法失败，尝试备用方法**
3. **用简单的语言向用户解释问题**
4. **建议用户采取的补救措施**（例如稍后再试、检查 URL 格式等）

## 高级功能

### 阅读推文讨论串
通过 `read_thread.sh` 可以完整地阅读推文讨论串：
- 给定讨论串中的任意推文 URL，通过 `replying_to` 字段向上遍历回复链
- 仅收集同一作者的推文（自回复链）
- 按时间顺序以 JSON 数组的形式返回推文
- 每个讨论串的最大返回推文数量可配置（通过第二个参数设置）
- 使用方法：`./scripts/read_thread.sh "https://x.com/user/status/123" [max_depth]`

### 媒体处理
- **照片**：通过 `mediaphotos` 数组获取直接链接（包含原始分辨率）
- **视频**：通过 `media.videos` 数组获取 MP4 文件链接，附带缩略图和时长信息
- **所有媒体**：通过 `media.all` 数组统一处理，包含类型注释
- **文章封面**：对于长篇 X 发布的内容（“articles”），会提取文章封面图片
- **GIF 图片**：视为视频内容处理
- **外部链接**：保留在推文文本中

### 被引用推文的递归处理
该技能可以递归地提取被引用的推文，但会设置合理的深度限制以避免无限循环。

## 性能说明

### 响应时间
- **FxTwitter API**：通常为 200-500 毫秒
- **Nitter 抓取**：每个实例大约需要 1-3 秒
- **网络依赖**：响应时间可能因网络质量而异

### 缓存策略
- 默认情况下不使用持久化缓存
- 对于重复请求，可以考虑使用临时缓存
- 遵守外部服务的速率限制

## 故障排除

### 常见问题

- **API 响应中未包含推文数据**：推文可能已被删除或设置为私密状态
- 检查 URL 格式和推文 ID
- 尝试使用备用方法
- **网络请求失败**：检查网络连接
- FxTwitter API 可能暂时不可用，此时切换到 Nitter 方法
- **所有 Nitter 实例都失败**：可能是 Nitter 实例被屏蔽或暂时不可用，此时尝试使用 FxTwitter API
- 检查防火墙/代理设置

### 调试模式
如需调试，请使用详细输出模式运行脚本：
```bash
bash -x scripts/read_tweet.sh "https://x.com/username/status/123"
```

## 开发与定制

### 添加新的数据源
- 要添加新的备用方法：
  1. 在 `scripts/` 目录中创建新脚本
  2. 确保新脚本遵循相同的 JSON 输出格式
  3. 更新主技能逻辑以包含新方法
  4. 彻底测试并更新文档

### 修改输出格式
可以通过修改每个脚本中的 `jq` 命令来定制 JSON 结构。确保所有方法之间的输出格式一致。

### 扩展功能
可以考虑以下改进方向：
- 对推文内容进行情感分析
- 提取标签和提及信息
- 扩展链接并预览链接内容
- 对媒体中的图片进行OCR文字识别
- 支持翻译非英语推文

## 版本历史
- **v1.1**：支持阅读推文讨论串（`read_thread.sh`），全面提取媒体内容（照片、视频、所有媒体类型）
- **v1.0**：首次发布，支持 FxTwitter API 和 Nitter 备用方案
- 多数据源，数据提取更加全面
- 完全符合安全审计标准
- 已准备好在 ClawHub 平台上部署
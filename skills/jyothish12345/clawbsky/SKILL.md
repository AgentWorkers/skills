---
name: clawbsky
version: "1.1.0"
description: 高级版的Bluesky CLI，支持处理媒体文件（图片/视频）、创建线程，以及提供自动化管理工具（如自动清理相互关注关系）。
homepage: https://github.com/jyothish12345/Clawbsky
requires:
  env:
    - BLUESKY_HANDLE
    - BLUESKY_APP_PASSWORD
  bins:
    - ffmpeg
    - ffprobe
---
# 🦞 Clawbsky

这是一个功能齐全的专业型Bluesky命令行工具（CLI），专为高级用户和自动化操作设计。

## ✨ 主要特性

- **媒体支持**：支持上传图片和视频，并自动检测元数据和宽高比。
- **账号管理工具**：识别并取消关注那些没有回关你的账号（`unfollow-non-mutuals`）。
- **主题管理**：能够将多段文本自动合并成长篇主题帖。
- **搜索与探索**：可深入搜索帖子、用户和标签。
- **管理功能**：支持快速屏蔽、静音用户以及发送通知。

## 🚀 设置

1. **获取应用密码**：前往[Bluesky设置](https://bsky.app/settings/app-passwords)创建一个新的应用密码。**切勿**使用你的主账户密码。
2. **安装**：
   ```bash
   npm install
   ```
3. **配置**：
   ```bash
   clawbsky login
   ```

## 🛠 命令

### 账号管理
```bash
clawbsky unfollow-non-mutuals -n 50 # Unfollow top 50 non-mutuals
clawbsky follow-all "Query" -n 20   # Auto-follow users matching a topic
```

### 发布内容与主题帖
```bash
clawbsky post "Text" [media...]          # Create a post
clawbsky thread "Part 1" "Part 2" ...     # Create a multi-post thread
clawbsky quote <uri> "My thoughts"      # Quote a post
```

### 阅读内容
```bash
clawbsky home -n 20              # View your timeline
clawbsky user <handle>           # Inspect a profile
clawbsky user-posts <handle>     # View user's recent activity
clawbsky thread <uri>            # Read a full conversation branch
```

### 互动与内容管理
```bash
clawbsky like/repost <uri>       # Engage with content
clawbsky block/mute <handle>     # Manage your boundaries
clawbsky notifications           # Check recent interactions
```

## 💡 高级用法

### 全局选项
- `--json`：输出原始数据，以便将其传递给其他工具。
- `--plain`：禁用表情符号和格式化，以获得更清晰的日志输出。
- `-n <count>`：限制返回的结果数量（默认为10条）。
- `--dry-run`：预览操作（如取消关注），但不实际执行。

## 🛡 安全与道德规范

Clawbsky提供了强大的自动化功能。为保护你的账号和Bluesky社区，请遵守以下规则：

1. **理性使用**：切勿使用`follow-all`命令每天搜索并关注大量用户，这种行为被视为垃圾信息，可能导致账号被封禁。
2. **遵守使用限制**：使用`unfollow-non-mutuals`进行定期账号维护，而非频繁地“关注/取消关注”操作。
3. **使用应用密码**：务必使用应用密码。如果怀疑账号密码被泄露，请立即在Bluesky设置中撤销该应用密码。
4. **限制操作频率**：该工具内置了操作延迟机制（每次关注操作需等待1秒），以防止超出API使用限制。请勿尝试禁用此机制。

*账号操作的所有责任均由用户本人承担。*

### 自动化逻辑
- **用户名处理**：`@username`或`username`会自动解析为`username.bsky.social`。
- **富文本处理**：提及的内容和链接会自动被检测并编码，以符合AT协议的要求。
- **视频处理**：系统会持续查询Bluesky的视频服务，直到处理完成。

---
*专为AT协议社区打造。*
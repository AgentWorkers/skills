---
name: clawbsky
version: 1.1.4
description: 高级版的Bluesky CLI，支持处理媒体文件（图片/视频）、创建线程，以及提供自动化管理工具（如非互粉关系的清理功能）。
homepage: https://github.com/jyothish12345/Clawbsky
metadata:
  openclaw:
    requires:
      env:
        - BLUESKY_HANDLE
        - BLUESKY_APP_PASSWORD
      bins:
        - ffmpeg
        - ffprobe
    primaryEnv: BLUESKY_APP_PASSWORD
---
# 🦞 Clawbsky  
一款专为高级用户和自动化需求设计的全功能专业Bluesky命令行工具（CLI）。  

## ✨ 主要特性  
- **媒体支持**：支持上传图片和视频，系统会自动检测元数据和宽高比。  
- **账号管理工具**：识别并取消关注那些不回关你的用户（`unfollow-non-mutuals`）。  
- **线程管理**：能够将多段文本自动合并成长篇帖子。  
- **搜索与探索**：支持深度搜索帖子、用户和标签。  
- **内容审核**：提供快速屏蔽、静音和通知管理功能。  

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

### 发布与线程  
```bash
clawbsky post "Text" [media...]          # Create a post
clawbsky thread "Part 1" "Part 2" ...     # Create a multi-post thread
clawbsky quote <uri> "My thoughts"      # Quote a post
```  

### 阅读功能  
```bash
clawbsky home -n 20              # View your timeline
clawbsky user <handle>           # Inspect a profile
clawbsky user-posts <handle>     # View user's recent activity
clawbsky thread <uri>            # Read a full conversation branch
```  

### 互动与内容审核  
```bash
clawbsky like/repost <uri>       # Engage with content
clawbsky block/mute <handle>     # Manage your boundaries
clawbsky notifications           # Check recent interactions
```  

## 💡 高级用法  
- **全局选项**：  
  - `--json`：输出原始数据，便于导入其他工具。  
  - `--plain`：禁用表情符号和格式化，以获得更清晰的日志输出。  
  - `-n <数量>`：限制搜索结果数量（默认值：10）。  
  - `--dry-run`：预览操作（如取消关注），但不实际执行。  

## 🛡 安全与道德规范  
Clawbsky提供了强大的自动化功能。为保护你的账户和Bluesky社区，请遵守以下规则：  
1. **理性使用**：切勿使用`follow-all`命令每天搜索并关注大量用户，这种行为被视为垃圾信息，可能导致账户被封禁。  
2. **遵守使用限制**：仅使用`unfollow-non-mutuals`进行定期账号维护，切勿用于频繁的“关注/取消关注”操作。  
3. **使用应用密码**：务必使用应用密码；如怀疑账号信息被盗用，请立即在Bluesky设置中撤销应用密码。  
4. **限制操作频率**：该工具内置了操作延迟机制（每次关注间隔1秒），以防止超出API使用限制。请勿尝试禁用这些限制。  
*所有账户操作的责任完全由用户自行承担。*  

### 自动化逻辑  
- **用户名处理**：`@username`或`username`会自动解析为`username.bsky.social`。  
- **富文本处理**：系统会自动识别并编码提及的内容和链接，以符合AT协议的要求。  
- **视频处理**：会持续轮询Bluesky的视频服务，直至处理完成。  

---  
*专为AT协议社区量身打造。*
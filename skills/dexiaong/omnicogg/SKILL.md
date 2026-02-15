---
name: omnicog
description: OpenClaw的通用服务集成功能——通过一个统一的API即可连接Reddit、Steam、Spotify、GitHub、Discord等平台。
metadata:
  openclaw:
    version: "1.0.0"
    platforms:
      - linux
      - macos
      - windows
    requires:
      env:
        - OMNICOG_REDDIT_CLIENT_ID
        - OMNICOG_REDDIT_CLIENT_SECRET
        - OMNICOG_STEAM_API_KEY
        - OMNICOG_SPOTIFY_CLIENT_ID
        - OMNICOG_SPOTIFY_CLIENT_SECRET
        - OMNICOG_GITHUB_TOKEN
        - OMNICOG_DISCORD_TOKEN
        - OMNICOG_YOUTUBE_API_KEY
    bins: []
    pythonPackages: []
    systemPackages: []
    permissions: []
    categories:
      - integration
      - api
      - social
      - gaming
    tags:
      - reddit
      - steam
      - spotify
      - github
      - discord
      - youtube
      - integration
      - api
    primaryEnv: OMNICOG_REDDIT_CLIENT_ID
  clawdbot:
    nix: null
    config: null
    cliHelp: null
---

# OmniCog — OpenClaw的通用服务集成工具

**一个统一的接口，整合所有服务。**

通过一个简单、统一的API，您可以轻松连接Reddit、Steam、Spotify、GitHub、Discord、YouTube等平台。再也不用繁琐地处理不同的认证方式或速率限制问题了——OmniCog会全部为您处理。

## 什么是OmniCog？

OmniCog是一个通用的服务集成层，为多个平台提供了一致的接口。无论您需要：

- 📊 **监控Reddit** — 跟踪帖子、评论和子版块活动
- 🎮 **集成Steam** — 获取拥有的游戏、成就和好友状态
- 🎵 **控制Spotify** — 播放音乐、管理播放列表并发现新曲目
- 🐙 **管理GitHub** — 查看仓库、跟踪问题并自动化工作流程
- 💬 **与Discord互动** — 发送消息、管理频道并监控服务器状态
- 📺 **搜索YouTube** — 查找视频、获取频道统计信息并跟踪上传内容

**OmniCog将所有这些服务统一到一个简单的API中。**

## 快速入门**

```python
# 安装所需的包
pip install omnicog

# 导入并初始化OmniCog客户端
from omnicog import OmniClient

# 配置客户端信息
client = OmniClient(
    reddit={
        "client_id": "YOUR_REDDIT_CLIENT_ID",
        "client_secret": "YOUR_REDDIT_CLIENT_SECRET",
        "user_agent": "OmniCog/1.0"
    },
    steam={
        "api_key": "YOUR_STEAM_API_KEY"
    },
    spotify={
        "client_id": "YOUR_SPOTIFY_CLIENT_ID",
        "client_secret": "YOUR_SPOTIFY_CLIENT_SECRET"
    }
)

# 使用相同的API调用任意服务
# 示例：获取Reddit上的热门编程相关帖子
posts = client.reddit.get_hot("programming", limit=10)
# 示例：获取拥有的Steam游戏列表
games = client.steam.getOwned_games()
# 示例：搜索Metallica的歌曲
track = client.spotify.search_track("metallica")
```
---
name: youtube-ultimate
version: 4.2.2
description: "免费文字记录、4K视频下载以及视频探索功能——完全不会消耗任何API配额。"
metadata:
  openclaw:
    owner: kn7623hrcwt6rg73a67xw3wyx580asdw
    category: media
    tags:
      - youtube
      - transcripts
      - video-download
      - media
      - offline
    license: MIT
    notes:
      security: "This skill invokes yt-dlp and youtube-transcript-api locally to fetch transcripts and download videos. No credentials stored, no API keys required, no external services beyond YouTube itself. All processing happens on your machine. No data is sent anywhere except standard YouTube HTTP requests."
---
# YouTube Ultimate

**我们的工具会为您自动读取YouTube上的内容，让您无需亲自操作。**它可以提取视频的字幕、总结视频内容，并从中提取有用信息——这一切都不需要使用YouTube的API配额。

## 主要功能

- **免费字幕**：可以立即获取任何视频的字幕。无需API密钥，无需担心配额限制，也不会在凌晨3点突然产生账单费用。该工具不会因为获取一个播放列表就耗尽您的免费配额，更不会强制您升级到每月200美元的付费计划（尽管它表现得好像是在帮您节省开支一样）。
- **4K视频下载**：可以将视频保存到本地，以便离线观看、用作训练数据，或者在没有Wi-Fi的情况下使用。
- **视频深度探索**：您可以自由搜索、浏览视频，并详细查看视频的各个部分，而无需担心任何速率限制的问题。

## 为什么这很重要？

YouTube的API每天仅提供10,000个配额单位。一次搜索就会消耗100个配额单位；而请求字幕的功能甚至都不被支持。YouTube Ultimate则完全规避了这些限制。我们的工具可以完全访问视频内容，同时您的配额计数器始终保持在0。

*克隆它、修改它，或者将其据为己有吧。*

👉 查看完整项目：[github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)
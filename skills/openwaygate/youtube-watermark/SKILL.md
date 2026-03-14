---
name: youtube-watermark
description: "管理 YouTube 水印功能。使用此技能可以为频道视频设置或取消水印。在处理 YouTube 水印相关问题时非常实用，提供了通过 yutu CLI 设置和取消水印的命令。包含针对首次使用者的设置和安装说明。可执行的操作包括：为频道视频设置水印、设置个人水印、为频道视频取消水印、取消个人水印。"
compatibility: Requires the yutu CLI (brew install yutu), Google Cloud OAuth credentials (client_secret.json), and a cached OAuth token (youtube.token.json). Needs network access to the YouTube Data API.
metadata:
  author: eat-pray-ai
  required_config_paths:
    - client_secret.json
    - youtube.token.json
  env:
    - YUTU_CREDENTIAL
    - YUTU_CACHE_TOKEN
---
# YouTube水印管理

本技能用于管理YouTube视频的水印设置。您可以使用它为频道中的视频添加或移除水印。

## 开始前

使用yutu需要Google Cloud Platform的OAuth凭证以及一个缓存的令牌来访问YouTube API。如果您尚未设置yutu，请先阅读[设置指南](references/setup.md)。

## 操作说明

请参阅相关参考文档以获取完整的参数说明和示例：

| 操作        | 描述                                      | 参考文档        |
|------------|-----------------------------------------|--------------|
| set        | 为频道中的视频设置水印                          | [详情](references/watermark-set.md) |
| unset       | 为频道中的视频移除水印                          | [详情](references/watermark-unset.md) |

## 快速入门

```bash
# Show all watermark commands
yutu watermark --help
```
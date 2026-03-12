---
name: youtube-memberships-level
description: "**管理 YouTube 会员等级**  
本技能用于查询频道会员等级的相关信息。在处理 YouTube 会员等级相关任务时非常实用，提供了通过 `yutu CLI` 命令来列出会员等级的接口。同时，也为首次使用的用户提供了设置和安装指南。  
**可执行的命令：**  
- `list memberships levels`  
- `list memberships level`  
- `list my memberships level`"
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
# YouTube 会员等级管理

本技能用于管理 YouTube 会员等级，并提供有关频道会员等级的详细信息。

## 开始前

使用 yutu 访问 YouTube API 需要 Google Cloud Platform 的 OAuth 凭据以及一个缓存的令牌。如果您尚未设置 yutu，请先阅读 [设置指南](references/setup.md)。

## 操作说明

请参阅相关参考文档以获取完整的参数说明和示例：

| 操作        | 描述                        | 参考文档        |
|------------|---------------------------|--------------|
| list       | 列出所有会员等级                   | [membershipsLevel-list.md](references/membershipsLevel-list.md) |

## 快速入门

```bash
# Show all memberships level commands
yutu membershipsLevel --help

# List memberships level
yutu membershipsLevel list
```
---
name: mangadex-cli
version: 0.1.2
description: MangaDex CLI 提供了一系列功能，包括搜索、查找漫画及章节信息、检查订阅源的更新情况，以及提供推荐内容。
allowed-tools: Bash
emoji: 📖
metadata:
  openclaw:
    install:
      - kind: node
        package: "@mtsku/mangadex-cli"
        bins: [mangadexcli]
    requires:
      bins: [node]
---
# MangaDex CLI 技能

此技能用于直接使用 MangaDex CLI 进行操作。本指南仅适用于 LLM/代理执行。

## 安装检查

1. 检查是否已安装：
   - `command -v mangadexcli`
2. 如果未安装，请安装：
   - `npm install -g @mtsku/mangadex-cli`
3. 验证安装是否成功：
   - `mangadexcli --help`

## 命令列表

- 发现/搜索：
  - `mangadexcli search manga "<查询>"`
  - `mangadexcli search author "<查询>"`
  - `mangadexcli search group "<查询>"`
  - `mangadexcli works author "<author_uuid_or_name>"`
  - `mangadexcli works group "<group_uuid_or_name>"`
- 漫画/章节信息：
  - `mangadexcli manga details <manga_uuid>`
  - `mangadexcli manga chapters <manga_uuid> --lang en -n 30`
  - `mangadexcli manga latest <manga_uuid> --lang en -n 10`
  - `mangadexcli chapter meta <chapter_uuid>`
- 关注源：
  - `mangadexcli feed updates --window 24h --lang en`
  - `mangadexcli feed updates --window 7d`
- 推荐：
  - `mangadexcli recommend suggest --tags "action,mystery" -n 10`
  - `mangadexcli recommend suggest --from-followed --exclude-library --window 7d -n 10`

## 认证设置

- 个人客户端登录：
  - `mangadexcli auth set-client <client_id> <client_secret>`
  - `mangadexcli auth login <username> <password>`
- 仅使用令牌：
  - `mangadexcli auth set-token <access_token>`
- 认证码交换：
  - `mangadexcli auth exchange --code <code> --redirect-uri <uri> [--code-verifier <verifier>]`
  - `mangadexcli auth refresh`
- 验证认证状态：
  - `mangadexcli whoami`
  - `mangadexcli auth where`

## 输出格式

- 使用 `--json` 可获得机器可读的输出格式。
- 公共阅读端点无需认证即可使用。
- 关注源更新和基于图书馆的推荐功能需要认证。
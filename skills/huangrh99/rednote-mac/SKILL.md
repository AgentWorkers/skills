---
name: rednote-mac
description: "通过 macOS 的辅助功能（Accessibility）API 来控制 RedNote（小红书）Mac 应用程序。这解决了无头工具无法实现的功能：阅读/回复视频帖子下的评论、发送私信以及获取作者信息。无需使用浏览器，也不需要 API 令牌。仅支持 macOS 系统，并且需要获得终端的辅助功能访问权限。"
metadata:
  openclaw:
    os: [darwin]
    requires:
      bins: [cliclick, python3]
      apps: [rednote]
      permissions: [accessibility]
---
# rednote-mac

直接控制 RedNote 的 Mac 应用程序——无需浏览器，也无需使用 API 令牌。该工具利用 macOS 的辅助功能 API 来操作原生的 RedNote 应用程序。

无头工具（如 xiaohongshu-mcp）无法访问私信（DMs）、评论回复或视频评论列表，但这个工具可以。

> ⚠️ 需要满足以下条件：终端（Terminal）可用；已启用辅助功能权限；RedNote 应用程序在屏幕上可见。
> 该工具不支持网络连接，也不会存储任何用户凭证。

## 设置

```bash
cd ~/.agents/skills/rednote-mac && bash install.sh
openclaw config set tools.allow '["rednote-mac"]'
openclaw gateway restart
```

在系统设置（System Settings）中，依次选择“隐私与安全”（Privacy & Security）→“辅助功能”（Accessibility）→“终端”（Terminal），以启用该功能。

## 导航

```
xhs_navigate(tab="home")          # home / messages / profile
xhs_navigate_top(tab="discover")  # follow / discover / video
xhs_back()
xhs_search(keyword="AI paper")
xhs_screenshot()                  # always verify after navigation
```

## 浏览信息流

```
xhs_scroll_feed(direction="down", times=5)
xhs_open_note(col=0, row=0)   # col: 0=left, 1=right  row: 0=first
xhs_screenshot()
```

## 与笔记交互

```
xhs_like()
xhs_collect()
xhs_follow_author()
xhs_get_note_url()   # returns xhslink.com short URL
```

## 视频帖子的评论（完全可靠）

```
xhs_open_comments()
xhs_get_comments()
# → [{"index": 0, "author": "alice", "cx": 1450, "cy": 368}, ...]

xhs_post_comment(text="Great post!")
xhs_reply_to_comment(index=0, text="Thanks!")
xhs_delete_comment(index=0)   # ⚠️ irreversible — your comments only
xhs_scroll_comments(times=3)
```

## 私信（Direct Messages）

```
xhs_open_dm(index=0)           # 0 = first conversation in list
xhs_send_dm(text="Hello!")
xhs_screenshot()               # confirm sent
```

## 作者信息

```
xhs_navigate(tab="profile")
xhs_get_author_stats()
# → {"following": "2", "followers": "29", "likes": "302", "bio": "..."}
```

## 参考文档（按需加载）

| 功能需求 | 参考文档 |
|-----------|------|
| 导航/搜索详情 | `docs/ref-navigation.md` |
| 信息流与笔记的打开 | `docs/ref-feed.md` |
| 评论操作流程 | `docs/ref-note.md` |
> 私信详情 | `docs/ref-dm.md` |
> 个人资料与统计信息 | `docs/ref-profile.md` |
> 使用限制及解决方法 | `docs/ref-limits.md` |
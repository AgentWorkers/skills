---
name: rednote-mac
description: >
  通过 macOS 的辅助功能 API 来控制 RedNote（小红书）Mac 应用程序。该应用程序支持私信、回复评论、阅读视频评论、搜索、点赞、收藏、关注以及查看作者信息等功能——这些功能在无头（headless）版本中是不可用的。
  **系统要求：**  
  仅支持 macOS 系统。需要终端辅助功能权限（系统设置 → 隐私与安全 → 辅助功能）。RedNote 应用程序必须能够在屏幕上正常显示。应用程序包含 `install.sh` 文件（用于创建插件目录的符号链接）和 `index.ts` 文件（用于注册 OpenClaw 插件）。该应用程序不进行任何网络请求，也不会存储任何用户凭证。所有操作仅限于 RedNote 应用程序窗口范围内。
---
# rednote-mac

通过 macOS 的辅助功能 API 直接控制 RedNote（小红书）Mac 应用程序。

**为什么选择这种方式而不是无头浏览器？**
无头浏览器工具无法访问私信、评论回复线程或视频评论列表。该方法直接通过 macOS 的辅助功能 API 与原生应用程序进行交互——无需进行逆向工程，也不需要 API 令牌。

## 所需权限

| 权限 | 原因 |
|------------|-----|
| 终端 → 辅助功能 | macOS 使用辅助功能 API 进行鼠标/键盘控制时必需的权限 |
| 屏幕可见 | 只有当应用程序窗口显示在屏幕上时，鼠标事件才能生效 |

无需网络访问，也不会存储任何凭据，数据也不会离开您的设备。

## 安装

```bash
# One-liner
cd ~/.agents/skills/rednote-mac && bash install.sh

# What install.sh does (transparent):
#   1. uv sync  (installs Python deps: atomacos, pyobjc)
#   2. ln -sf ~/.agents/skills/rednote-mac ~/.openclaw/extensions/rednote-mac
#   3. Prints: openclaw config set tools.allow '["rednote-mac"]'

openclaw config set tools.allow '["rednote-mac"]'
openclaw gateway restart
```

验证安装结果：`openclaw plugins list | grep rednote-mac`

⚠️ 系统设置 → 隐私与安全 → 辅助功能 → 启用“终端”选项

## 可用的工具（快速参考）

```
xhs_screenshot          Capture current screen
xhs_navigate            Switch bottom tab: home | messages | profile
xhs_navigate_top        Switch top tab: follow | discover | video
xhs_back                Go back one page
xhs_search              Search keyword → results page
xhs_scroll_feed         Scroll feed (direction, times)
xhs_open_note           Open note by grid position (col, row)
xhs_like                Like current note
xhs_collect             Collect/save current note
xhs_get_note_url        Get share URL of current note
xhs_follow_author       Follow current note's author
xhs_open_comments       Open comment section
xhs_scroll_comments     Scroll comments
xhs_get_comments        Get comment list → [{index, author, cx, cy}]
xhs_post_comment        Post a comment
xhs_reply_to_comment    Reply to a comment (index, text)
xhs_delete_comment      Delete own comment (index) ⚠️ irreversible
xhs_open_dm             Open DM conversation (index)
xhs_send_dm             Send DM in current conversation
xhs_get_author_stats    Get profile stats (following/followers/likes/bio)
```

## 参考文档（按需加载）

| 功能 | 参考文档 |
|------|------|
| 导航、截图、搜索 | `docs/ref-navigation.md` |
| 浏览动态、打开笔记 | `docs/ref-feed.md` |
| 点赞、收藏、评论、回复、删除 | `docs/ref-note.md` |
| 私信 | `docs/ref-dm.md` |
| 用户资料/作者信息 | `docs/ref-profile.md` |
| 已知限制及解决方法 | `docs/ref-limits.md` |
---
name: hacker-news-poster
description: 在 Hacker News 上发布内容、发表评论并进行互动。当用户需要提交一个展示内容（Show HN）、发布一篇故事（post a story）、对某个帖子进行评论（comment on an HN thread）、编辑评论（edit a comment）或更新个人资料（update an HN profile）时，请使用此功能。该功能需要 `HN_USERNAME` 和 `HN_PASSWORD` 环境变量。用户会话信息会保存在 `~/.hn_cookies.txt` 文件中（可通过 `HN COOKIE_FILE` 环境变量进行配置）。
---
# Hacker News 插件

在 Hacker News 上提交故事、评论帖子、编辑评论以及更新个人资料。

## 设置

### 必需的环境变量

| 变量        | 是否必需 | 说明                          |
|------------|---------|-------------------------------------------|
| `HN_USERNAME` | 是       | Hacker News 的用户名                   |
| `HN_PASSWORD` | 是       | Hacker News 的密码                     |
| `HN_COOKIE_FILE` | 否       | Cookie 存储路径（默认为 `~/.hn_cookies.txt`）         |

### 安全提示

会话 Cookie 以明文形式存储在 `HN_COOKIE_FILE`（或 `~/.hn_cookies.txt`）中。这些是标准的 Hacker News 会话令牌。删除该文件即可清除会话信息。

## 命令行接口（CLI）

所有命令都通过 `scripts/hn.py` 脚本执行。每次使用该插件前，请务必先执行 `login` 命令进行登录。

```bash
# login (reads HN_USERNAME/HN_PASSWORD from env)
python3 scripts/hn.py login

# submit a link post
python3 scripts/hn.py submit --title "Show HN: My Tool" --url "https://example.com"

# submit a text post (Ask HN, etc.)
python3 scripts/hn.py submit --title "Ask HN: Question?" --text "body text here"

# comment on a story or reply to a comment
python3 scripts/hn.py comment --parent 12345678 --text "your comment"

# edit a comment (only within HN's edit window)
python3 scripts/hn.py edit --id 12345678 --text "updated comment"

# update profile about section
python3 scripts/hn.py profile --username youruser --about "your bio"
```

所有命令在成功执行时会输出 JSON 格式的结果（例如 `{"ok": true, ...}`），并在遇到错误时将错误信息输出到标准错误流（stderr）。

## 注意事项

- Hacker News 对提交内容和评论操作设置了速率限制。如果遇到速率限制错误，请等待几分钟后再尝试。
- 评论只能在发布后的 2 小时内进行编辑。
- `submit` 命令在成功执行后会返回新帖子的 ID 和 URL。
- 会话 Cookie 存储在 `~/.hn_cookies.txt` 中，以避免每次执行命令时都需要重新登录。删除该文件即可清除会话信息。
- 如需读取 Hacker News 的内容（如搜索、热门故事、评论等），可以使用现有的 `hacker-news` 插件或直接调用 Hacker News 的 API。不过，该插件仅支持读操作（无法写入数据）。

## 与只读的 `hacker-news` 插件的结合使用方法

1. 使用 `hacker-news` 插件浏览/搜索故事，找到感兴趣的帖子。
2. 使用当前插件登录并发布评论或对帖子进行编辑。
---
name: rssaurus-cli
description: "使用 RSSaurus 命令行客户端（Go 语言编写的二进制文件 `rssaurus`）通过终端与 https://rssaurus.com 进行交互：进行身份验证（`rssaurus auth login/whoami`）、列出订阅源中的内容条目、打印内容条目的 URL 以供后续处理、打开这些 URL，以及执行分类管理操作（标记为已读/未读、批量标记为已读、保存/取消保存）。该工具适用于需要从命令行自动化执行 RSSaurus 相关任务的情况，也可用于调试令牌或配置问题，或演示命令的使用方法。"
---

# RSSaurus CLI

请使用本机上已安装的 `rssaurus` 可执行文件来与 RSSaurus 进行交互。

## 常见检查（在出现问题时）

1) 确认 `rssaurus` 可执行文件是否存在：

```bash
which rssaurus
rssaurus --version || true
```

2) 确认身份验证功能是否正常：

```bash
rssaurus auth whoami
```

### 隐私注意事项

- **切勿** 打印 RSSaurus CLI 的配置文件内容（例如使用 `cat` 命令）；该文件可能包含 API 令牌。
- 如果身份验证失败，建议重新进行身份验证（使用 `rssaurus auth login` 命令），或者让用户仅提供非敏感信息（如错误信息、主机地址等）。

## 常用任务

### 列出源Feed列表

```bash
rssaurus feeds
rssaurus feeds --json
```

### 列出项目列表

默认情况下，未读的项目会被标记为“未读”状态：

```bash
rssaurus items --limit 20
```

### 按源Feed进行过滤

```bash
rssaurus items --feed-id 3 --limit 20
```

### 生成适合机器阅读的URL格式（每条信息占一行）

```bash
rssaurus items --limit 20 --urls
```

### 使用光标进行分页浏览

```bash
rssaurus items --limit 50 --cursor <cursor>
```

### 打开指定URL

```bash
rssaurus open https://example.com
```

### 标记项目为已读/未读

这些操作需要项目的ID（可以通过 `--json` 参数获取ID）：

```bash
rssaurus items --limit 5 --json
rssaurus read <item-id>
rssaurus unread <item-id>
```

### 批量标记项目为已读

```bash
rssaurus mark-read --all
# or
rssaurus mark-read --ids 1,2,3
# optional
rssaurus mark-read --all --feed-id 3
```

### 保存/取消保存项目状态

```bash
rssaurus save https://example.com --title "Optional title"

# unsave requires an id (obtain via --json output from the API response or future saved-items listing)
rssaurus unsave <saved-item-id>
```

## 输出格式（隐私保护）

- 默认的输出格式不会显示数据库中的内部ID。
- 当需要将数据用于脚本编写或其他写入操作时，请使用 `--json` 格式输出项目ID。

## 参考资料

- RSSaurus CLI 的GitHub仓库：https://github.com/RSSaurus/rssaurus-cli
- RSSaurus 的Homebrew包管理仓库：https://github.com/RSSaurus/tap
- API令牌的生成方式：https://rssaurus.com/api_tokens/new
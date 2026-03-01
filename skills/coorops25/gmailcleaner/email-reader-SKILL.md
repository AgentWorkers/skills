---
name: email-reader
description: 通过 gog CLI 读取/搜索 Gmail：可以查看收件箱、搜索邮件以及获取邮件内容。
user-invocable: true
tools: Bash
metadata: {"openclaw":{"emoji":"📬","requires":{"bins":["gog"],"env":["GOG_ACCOUNT"]}}}
---
# email-reader

## 使用场景
用户需要查看收件箱、搜索电子邮件、阅读邮件内容或汇总最近的邮件。

## 命令

```bash
# List unread (default action)
gog gmail search 'in:inbox is:unread' --max 5 --format minimal --json

# Search by criteria (use Gmail search syntax)
gog gmail search '<query>' --max 10 --format minimal --json

# Read full email
gog gmail get <message_id> --format full --json

# Get thread
gog gmail thread <thread_id> --format minimal --json
```

## 工作流程
1. 确保 `gog` 已添加到系统路径中，并且 `GOG ACCOUNT` 已设置。
2. 根据用户的意图构建 Gmail 搜索查询（如果查询语句不明确，需要进一步询问用户）。
3. 运行 `gog gmail search` 命令，参数设置为 `--format minimal --json --max N`。
4. 解析返回的 JSON 数据，生成格式化的邮件列表（包含发送者、主题、日期、邮件内容摘要和邮件 ID）。
5. 提供选项：阅读完整邮件、进一步细化搜索条件或对邮件执行其他操作。

## 输出格式

```
📬 [count] emails:
1. **From:** Name <email> | **Subject:** … | **Date:** YYYY-MM-DD HH:MM
   Preview: … | ID: msg_xxx
```

## 规则
- 必须始终使用参数 `--format minimal --json --max N`（默认值 N=5）。
- 严禁直接显示原始 JSON 数据；除非用户明确要求，否则不要获取邮件的完整内容。
- 保留邮件 ID 以便后续操作使用。
- 如果搜索结果为空，需要确认搜索条件或建议使用更宽泛的搜索关键词。
- 该工具仅提供读取邮件的功能；发送或回复邮件需要用户具备相应的技能。
- 除非用户明确要求，否则不要将邮件内容存储在 `MEMORY.md` 文件中。

## 错误处理
- 如果 `gog` 未安装，提示用户使用命令 `npm i -g gogcli` 或 `brew install gogcli` 进行安装。
- 如果 `GOG_ACCOUNT` 未设置，提示用户输入 Gmail 地址。
- 如果 API 请求失败，显示错误信息并建议用户重新尝试或提供解决方案。

## Gmail 搜索操作符
`from:` `to:` `subject:` `label:` `is:unread` `is:starred` `has:attachment` `newer_than:Nd` `older_than:Nd` `in:inbox` `in:sent` `filename:ext`
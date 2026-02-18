---
name: last30days
version: "2.1-open"
description: "研究主题、管理关注列表、获取简报、查询历史记录。这些功能也会根据“last30”指令被触发。数据来源包括 Reddit、X（可能是某个特定的社交媒体平台）、YouTube 以及网页内容。"
argument-hint: 'last30 AI video tools, last30 watch my competitor every week, last30 give me my briefing'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
---
# last30days（开放模式）：研究 + 监控列表 + 简报

这是一个具备持续知识积累功能的多模式研究工具。

## 命令路由

解析用户的第一个参数以确定操作模式：

| 参数 | 模式 | 参考文档 |
|---|---|---|
| `watch` | 监控列表管理 | `references/watchlist.md` |
| `briefing` | 早晨简报 | `references/briefing.md` |
| `history` | 查询累积的知识 | `references/history.md` |
| *(其他任何参数)* | 一次性研究 | `references/research.md` |

## 设置：查找技能根目录

使用 `$SKILL_ROOT` 作为所有脚本和参考文件的路径。

## 加载上下文

在会话开始时，读取 `${SKILL_ROOT}/variants/open/context.md` 以获取用户偏好设置和资源质量说明。在用户交互后更新该文件。

## 共享配置

- **数据库**：`~/.local/share/last30days/research.db`（SQLite 数据库，WAL 模式）
- **简报文件**：`~/.local/share/last30days/briefs/`
- **API 密钥**：`~/.config/last30days/.env` 或环境变量
- **密钥优先级**：环境变量 > 配置文件

### API 密钥

| 密钥 | 是否必需 | 用途 |
|---|---|---|
| `OPENAI_API_KEY` | 必需 | 通过 OpenAI 的搜索 API 在 Reddit 上进行搜索 |
| `XAI_API_KEY` | 可选 | 通过 xAI 的 Grok API 在 X 上进行搜索 |
| `PARALLEL_API_KEY` | 可选 | 通过 Parallel AI 进行网络搜索 |
| `BRAVE_API_KEY` | 可选 | 通过 Brave Search 进行网络搜索 |
| `OPENROUTER_API_KEY` | 可选 | 通过 Perplexity Sonar Pro 进行网络搜索 |

如果安装了 Bird CLI，它可以提供免费的 X 搜索服务。YouTube 搜索使用 yt-dlp（免费工具）。

运行 `python3 "${SKILL_ROOT}/scripts/last30days.py" --diagnose` 以检查资源是否可用。

## 路由逻辑

确定操作模式后，使用相应的参考文档进行操作：

```
Read: ${SKILL_ROOT}/variants/open/references/{mode}.md
```

然后严格按照该参考文档中的说明进行操作。
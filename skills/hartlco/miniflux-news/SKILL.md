---
name: miniflux-news
description: 通过 Miniflux 的 REST API 使用 API 令牌来获取并筛选最新的未读 RSS/新闻条目。当用户请求获取最新的未读条目、列出带有标题/链接的最新条目，或生成特定 Miniflux 条目的简短摘要时，可以使用此功能。附带一个脚本，用于使用来自 `~/.config/clawdbot/miniflux-news.json` 文件中的凭据（或通过 `MINIFLUX_URL` 和 `MINIFLUX_TOKEN` 进行覆盖）来查询 Miniflux（路径为 `/v1/entries` 和 `/v1/entries/{id}`）。
---

# Miniflux 新闻

使用捆绑的脚本获取新闻条目，然后将其格式化为简洁的列表，并可选择性地生成摘要。

## 设置（凭据）

默认情况下，该技能会从本地配置文件中读取 Miniflux 的凭据。

### 配置文件（推荐）

路径：
- `~/.config/clawdbot/miniflux-news.json`

格式：
```json
{
  "url": "https://your-miniflux.example",
  "token": "<api-token>"
}
```

使用以下脚本创建或更新配置文件：
```bash
python3 skills/miniflux-news/scripts/miniflux.py configure \
  --url "https://your-miniflux.example" \
  --token "<api-token>"
```

### 环境变量（可选）

您可以覆盖配置文件的内容（适用于持续集成环境）：
```bash
export MINIFLUX_URL="https://your-miniflux.example"
export MINIFLUX_TOKEN="<api-token>"
```

**Token 作用域**：具有读取权限的 Miniflux API 令牌。

## 获取最新条目

- 列出所有未读的条目（默认行为）：
```bash
python3 skills/miniflux-news/scripts/miniflux.py entries --limit 20
```

- 按类别筛选条目（按名称）：
```bash
python3 skills/miniflux-news/scripts/miniflux.py entries --category "News" --limit 20
```

**如果需要机器可读的输出：**
```bash
python3 skills/miniflux-news/scripts/miniflux.py entries --limit 50 --json
```

### 响应格式

- 返回简洁的列表格式：**[id] 标题 — 链接**。
- 用户可以指定需要生成摘要的条目数量（例如：“summarize 3” 或 “summarize ids 123,124”）。

## 查看完整内容

显示存储在 Miniflux 中的文章全文（适用于阅读或生成更详细的摘要）：
```bash
python3 skills/miniflux-news/scripts/miniflux.py entry 123 --full --format text
```

**如果需要获取 Miniflux 存储的原始 HTML 内容：**
```bash
python3 skills/miniflux-news/scripts/miniflux.py entry 123 --full --format html
```

## 分类

列出所有新闻分类：
```bash
python3 skills/miniflux-news/scripts/miniflux.py categories
```

## 将条目标记为已读（仅限明确请求时使用）

该技能 **严禁** 自动将条目标记为已读。只有在用户明确要求时，才能将特定条目标记为已读。

- 将特定条目标记为已读：
```bash
python3 skills/miniflux-news/scripts/miniflux.py mark-read 123 124 --confirm
```

- 将某个类别中的所有未读条目标记为已读（仍需用户明确请求，并使用 `--confirm` 选项；同时建议使用 `--limit` 限制操作范围）：
```bash
python3 skills/miniflux-news/scripts/miniflux.py mark-read-category "News" --confirm --limit 500
```

## 生成条目摘要

- 获取指定条目的完整内容（适用于机器读取）：
```bash
python3 skills/miniflux-news/scripts/miniflux.py entry 123 --json
```

**摘要生成规则：**
- 每条摘要最多包含 3–6 个要点。
- 以 “那么……” 开头，用一句话概括内容。
- 如果内容为空或被截断，应予以说明，并根据标题和可用片段进行总结。
- 不要编造事实；如果有关键数字或名称，请直接引用。

## 故障排除

- 如果脚本提示“凭据缺失”，请设置 `MINIFLUX_URL`/`MINIFLUX_TOKEN`，或创建 `~/.config/clawdbot/miniflux-news.json` 文件。
- 如果收到 HTTP 401 错误，说明令牌错误或已过期。
- 如果收到 HTTP 404 错误，说明基础 URL 错误（应为 Miniflux 的网站根目录）。
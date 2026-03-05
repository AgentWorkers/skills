---
name: idea-spark
description: "根据用户所处的领域或兴趣生成项目创意。适用于用户询问项目想法、寻求灵感、提出“我应该开发什么”或“给我一些项目建议”时，也可用于发现尚未被充分开发的细分市场。该功能可作为“创意验证”（idea-check）功能的补充工具。"
metadata: {}
---
# Idea Spark

该工具通过扫描来自 Hacker News、Reddit 和 GitHub 的实际问题点来生成可执行的项目创意，并可选择性地使用 idea-check 工具对这些创意进行验证。

## 工作流程

### 1. 提取领域信息

从用户输入的信息中提取以下字段：

| 字段 | 说明 |
|-------|-------|
| `domain` | 关注领域（例如：“开发工具”、“健康追踪”、“AI 代理”） |
| `count` | 请求的项目创意数量（默认：5 个） |
| `type` | 项目类型（如果指定了的话）：命令行工具（CLI）、API、机器人（bot）、应用程序（app）、库（library）（默认：任意类型） |

如果领域信息不明确，请在继续之前要求用户进一步澄清。

### 2. 研究问题点

使用内置的 `web_search` 工具并行执行 **3 次搜索**，以找到人们正在抱怨或需求的实际问题：

```json
{ "tool": "web_search", "query": "site:news.ycombinator.com \"I wish\" OR \"someone should build\" OR \"why isn't there\" <domain> 2025 2026" }
```

```json
{ "tool": "web_search", "query": "site:reddit.com \"looking for\" OR \"is there a\" OR \"frustrated with\" <domain> tool" }
```

```json
{ "tool": "web_search", "query": "github.com trending <domain> OR \"help wanted\" OR \"good first issue\" <domain>" }
```

### 3. 整理创意

从搜索结果中提取重复出现的主题和未满足的需求。为每个创意生成以下信息：

| 字段 | 格式 |
|-------|--------|
| `name` | 简短的项目名称（2-4 个词） |
| `pitch` | 该创意的功能简介 |
| `pain` | 它解决的问题（来源：Hacker News/Reddit/GitHub） |
| `type` | 项目类型：CLI、API、机器人、应用程序、库、MCP 服务器、OpenClaw 技能 |
| `effort` | 需要的努力程度：低 / 中等 / 高 |

根据问题点的具体性和可执行性，生成 `count` 个创意，并对这些创意进行排序。

### 4. 使用 idea-check 进行验证（如果可用）

对每个创意进行快速验证：

```json
{
  "tool": "exec",
  "command": "mcporter call idea-reality.idea_check idea_text=\"<pitch>\" depth=quick"
}
```

如果 `mcporter` 或 `idea-reality` 无法使用，则跳过此步骤，并注明未进行验证。

为每个创意添加 `reality_signal` 分数。将 `reality_signal` 分数大于 70 的创意标记为“竞争激烈”。

### 5. 展示结果

结果展示格式如下：

- `reality_signal` < 30：“领域尚待开发”
- `reality_signal` 30-70：“存在一定竞争”
- `reality_signal` > 70：“竞争激烈”
- 未验证： “未经过验证”

### 6. 后续处理

展示结果后，可以建议用户：
- “需要我深入调查其中某个创意吗？” → 使用 `idea-check` 并设置 `depth=deep` 参数进行深入分析
- “希望我开始开发第 N 个项目吗？” → 继续进行开发

### 7. 错误处理

- 如果搜索没有返回结果 → 扩大领域范围，尝试不使用特定网站过滤器进行搜索
- 如果所有创意的 `reality_signal` 分数都大于 70 → 告知用户该领域已经饱和，建议用户缩小研究范围
- 如果 `mcporter` 无法使用 → 直接展示未经过验证的创意，并告知用户后续可以使用 idea-check 进行验证
- 如果领域范围过于宽泛（例如：“技术”） → 要求用户进一步明确具体方向

## 示例

| 用户输入 | 关注领域 | 处理方式 |
|-----------|--------|--------|
| “给我 5 个开发工具相关的创意” | 开发工具 | 在 Hacker News、Reddit 和 GitHub 上搜索，生成 5 个创意并逐一验证 |
| “我应该在 AI 代理领域开发什么？” | AI 代理 | 搜索相关问题点，生成创意并验证 |
| “我想开发与 MCP 服务器相关的产品” | MCP 服务器 | 重点关注 MCP 生态系统中的空白点，生成创意 |
| “关于健康追踪的创业创意” | 健康追踪 | 搜索未满足的需求，生成创意并标记出竞争激烈的创意 |
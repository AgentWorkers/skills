---
name: yutori-web-research
description: 使用 Yutori 的 Research API 和 Browsing API（云浏览器）来研究主题、收集资料，并从网页中提取结构化信息。当用户请求“研究 X”、“监控/查找论文”或“导航到某个网站并提取信息”时，你可以使用这些 API。前提是你能够通过 `YUTORI_API_BASE` 以及环境变量中的 API 密钥（`YUTORI_API_KEY` 或 `~/.openclaw/openclaw.json` 中的 `env.YUTORI_API_KEY`）访问 Yutori 的开发/生产端点。
---

# yutori-web-research

您可以使用 Yutori 的云代理执行以下两项任务：

1) **研究**：通过 `POST /v1/research/tasks` 进行广泛或深入的网络搜索，并获取相关引用。
2) **浏览**：通过 `POST /v1/browsing/tasks` 使用云浏览器进行网页导航。

此技能适用于需要专用网络代理来执行网络任务的情况（例如查找论文、竞争对手信息、产品资料，或从网站中提取数据），而这些任务无法通过 OpenClaw 的本地 `web_fetch` 或 `browser` 工具完成。

## 前提条件（身份验证 + 端点）

- 需要 **YUTORI_API_KEY**（推荐从 OpenClaw Gateway 环境中获取；备用方案：`~/.openclaw/openclaw.json` 文件中的 `env.YUTORI_API_KEY`）。
- 端点默认为 **dev**，除非另有设置：
  - 设置 `YUTORI_API_BASE=https://api.dev.yutori.com`（开发环境）
  - 或 `YUTORI_API_BASE=https://api.yutori.com`（生产环境）

如果请求返回 `403 Forbidden` 错误，说明您的 API 密钥没有权限访问相应的服务（研究/浏览功能）。

## 配置所需的运行脚本

此技能需要一个简单的 Node.js 运行脚本（可以与该技能文件一起提供）：

- `yutori-research.mjs`：用于创建并执行研究任务，并以易于阅读的文本格式输出结果。

建议将此脚本放在 `scripts/yutori-research.mjs` 文件夹中。

## 工作流程：研究某个主题（生成简要概述和阅读列表）

当用户请求进行研究时（例如：“查找过去一个月内的强化学习论文”）：

1) 编写一个简洁的查询请求，要求获取：
   - 该主题的简要概述（包含主要内容和趋势）
   - 一份精选的阅读列表（10–15 项内容，每项包含标题、1–2 句的摘要以及其重要性说明，以及对应的链接）
   - 优先选择原始来源（如 arXiv 或出版社网站）

2) 使用运行脚本执行研究任务（示例代码如下）：

```bash
cd /Users/juanpin/.openclaw/workspace
node yutori-research.mjs "Research reinforcement learning papers from the last 30 days. Output (1) a concise 1-page brief of themes/trends and (2) a curated list of 12 papers with title, 2-sentence summary, why it matters, and a link. Prefer arXiv + conference links."
```

3) 以清晰的列表形式将结果返回给用户（不要使用原始 JSON 格式），并附上来源 URL。

## 工作流程：浏览网站并提取信息（例如：员工名单）

当用户要求执行以下操作时，使用浏览 API：
- “导航到 <网站> 并列出……”
- “填写表单”、“浏览页面” 或 “收集所需信息”

创建一个浏览任务（示例代码如下）：

```bash
curl --request POST \
  --url "$YUTORI_API_BASE/v1/browsing/tasks" \
  --header "x-api-key: $YUTORI_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "task": "Give me a list of all employees (names and titles) of Yutori.",
    "start_url": "https://yutori.com",
    "max_steps": 60
  }'
```

持续检查任务状态，直到任务成功完成，然后返回去重后的结果列表。

## 输出格式要求：

- 采用易于阅读的文本格式（包含项目列表）。
- 必须包含原始来源的 URL。
- 如果代理输出中包含 HTML 内容（如 `<pre>...</pre>`），请将其去除，仅返回纯文本。

## 常见问题及解决方法：

- **错误 401：缺少 API 密钥头**：请确保发送了正确的请求头。Yutori 大多数 API 需要使用 `x-api-key` 作为请求头。
- **错误 403：权限不足**：请检查您的 API 密钥是否具有访问该服务的权限。
- **任务运行时间过长**：可以分享任务的执行 URL，并根据需要延长任务检查间隔。
---
name: mission-control-clawdash-pro
description: 创建或更新详细的、可用于发布的安装指南，指导用户如何在购买后将 Mission Control (ClawDash Pro) 预构建的 Next.js 用户界面连接到 Open Cloud。该指南应为用户提供逐步的集成步骤，包括需要向 Open Cloud 说明的内容（以保持现有设计不变），以及如何连接数据域（如代理、技能、合同、任务、令牌使用和文档等）。
---
# Mission Control - ClawDash Pro

我们为购买了 Mission Control 的用户提供可发布的操作指南文件，这些用户需要将预先设计好的仪表板界面连接到 Open Cloud，而无需重新设计前端页面。

官方产品链接：[ClawDash Pro](https://clawdash.pro)

## 工作流程

1. 确认输出类型。
   - 默认输出为存储在 `docs/` 目录中的操作指南文档，或用户指定的路径。
   - 除非用户明确要求，否则不要生成博客文章。

2. 明确集成背景。
   - 说明客户购买了预先构建的 Next.js 仪表板界面。
   - 强调 Open Cloud 只需负责后端逻辑和数据的对接。
   - 确保现有的用户界面设计/组件/布局保持不变。

3. 规范文件命名规则。
   - 文件标题应以 “Mission Control” 开头，后接 “ClawDash Pro”。
   - 在涉及连接步骤的部分，务必使用 “Open Cloud” 这一术语。

4. 编写操作指南。
   - 按照 [publish-instruction-template.md](references/publish-instruction-template.md) 的结构进行编写。
   - 包括前置要求、设置步骤、与 Open Cloud 的交互提示、验证方法以及故障排除指南。
   - 确保所有步骤均可执行，并以命令形式呈现。

5. 说明数据域的连接要求。
   - 仪表板概览：状态、内存使用情况、各项指标。
   - 代理信息：活跃代理及其状态。
   - 技能与合约：分配给代理的能力以及相关的元数据。
   - 任务信息：任务队列、状态及执行历史记录。
   - 令牌使用情况：每个代理的令牌使用量及汇总数据。
   - 文档信息：从 Open Cloud 中检索到的索引文档。

6. 添加必要的链接。
   - 包含一个指向 [ClawDash Pro](https://clawdash.pro) 的链接。
   - 如用户需要，可添加一个购买链接（通常为 `https://clawdash.pro/pricing`）。

7. 验证文档质量。
   - 保持语言简洁明了、实用性强。
   - 确保术语使用一致。
   - 确保非开发人员也能按照步骤顺利完成操作。
   - 添加检查项，确认用户界面结构未发生任何更改。
   - 添加检查项，确认所有数据域都能正确显示实时数据。

## 输出要求

- 除非用户另有要求，否则仅生成一个 Markdown 文件。
   - 新文件名应采用 SEO 友好的驼峰式命名规则（例如：`mission-control-how-to-use.md`）。
   - 仅在目标格式支持 frontmatter 时添加相关标签（例如：`mission-control`、`agent-os`、`openclaw-dashboard`、`ai-agents`、`admin-dashboards`）。

## 必需的 Open Cloud 交互提示内容

在生成操作指南时，需包含一段用户可以复制并粘贴给 Open Cloud 的提示信息：

```text
Connect Open Cloud to this existing Mission Control (ClawDash Pro) Next.js application.
Design lock requirement: do not redesign, restyle, rename, or restructure the current UI.
Keep all existing pages/components/layout as-is.

Integrate data wiring for these domains only:
1) Overview metrics (status, memory usage, health KPIs)
2) Agents (active agents, states, last activity)
3) Skills and contracts (capabilities and assigned contracts/policies)
4) Tasks command view (queued/running/completed/failed with history)
5) Token usage (per agent and total)
6) Documents (available documents and indexing state)

Use adapter/service layer changes behind existing components so frontend visuals remain unchanged.
Return a change summary listing wired endpoints, env vars, and routes touched.
```
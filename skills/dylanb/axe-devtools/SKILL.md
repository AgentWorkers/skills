---
name: axe-accessibility
description: 使用 axe MCP Server 进行无障碍性测试与修复。在创建或修改用户界面代码（HTML、JSX、TSX、Vue、Svelte、CSS）时，该工具可帮助确保代码符合无障碍性标准。适用于涉及网页、组件、表单、导航、模态框、表格、图片或任何面向用户的标记内容的场景。此外，在需要明确检查无障碍性或执行 axe 扫描时，也可使用该工具。
---

# axe 可访问性工具

使用 axe DevTools MCP Server 测试网页是否存在可访问性违规，并获取基于人工智能的修复建议。

## 先决条件

- 本地运行 Docker
- 已设置 `AXE_API_KEY` 环境变量
- 已下载 Docker 镜像：`dequesystems/axe-mcp-server:latest`

## 工具

`scripts/axe-mcp.js` 中的封装脚本（基于 Node.js，无需额外依赖）提供了两个工具：

### analyze

扫描实时网页以检测可访问性违规。需要提供一个 URL（支持本地主机）。

```bash
node scripts/axe-mcp.js analyze <url>
```

该工具会返回 JSON-RPC 响应。违规信息存储在 `result.content[0].text`（JSON 字符串）中的 `data` 数组中。每个违规项包含以下内容：`rule`（规则）、`impact`（影响程度）、`description`（描述）、`selector`（选择器）、`source`（来源）和 `helpUrl`（帮助文档链接）。

### remediate

针对特定的违规提供基于人工智能的修复建议。该工具能够安全地处理包含引号或括号的 HTML 代码。

```bash
node scripts/axe-mcp.js remediate <ruleId> <elementHtml> <issueRemediation> [pageUrl]
```

该工具会在 `result.content[0].text` 中返回 `general_description`（通用描述）、`remediation`（修复方法）和 `code_fix`（修复代码）。

### tools-list

列出所有可用的 MCP 工具。

```bash
node scripts/axe-mcp.js tools-list
```

## 工作流程

在修改用户界面代码且网页可访问的情况下：

1. **分析**：`node scripts/axe-mcp.js analyze <url>`
2. **解析**：从 JSON 响应中提取违规信息
3. **修复**：针对每个违规项，使用 `ruleId`、元素 HTML 代码和问题描述调用 `remediate` 函数进行修复
4. **应用**：将推荐的修复代码应用到源代码中
5. **验证**：重新运行 `analyze` 命令以确保没有违规项

如果无法访问实时网页（仅进行静态代码审查），请直接应用以下可访问性最佳实践：
- 图片：设置 `alt` 属性（装饰性图片可设置 `alt=""`）
- 表单：输入字段需要关联 `label` 元素
- 交互式元素：确保可通过键盘访问，并且能够显示焦点
- 颜色对比度：符合 WCAG AA 标准（普通文本为 4.5:1，大字体文本为 3:1）
- ARIA 标签：使用有效且完整的 ARIA 标签，避免与原生语义重复
- 标题：保持正确的层级结构（h1 → h2 → h3）
- 动态内容：确保弹出框、单页应用（SPA）和可交互区域的可访问性

## 注意事项

- 每次调用 `remediate` 都会消耗您组织分配的 AI 信用额度
- `analyze` 工具会在 Docker 中启动真实的浏览器，可能需要约 30 秒才能得到结果
- 该工具支持本地主机 URL，适用于本地开发测试
> **注意**：使用该工具需要订阅付费版的 Axe DevTools for Web。

## 技术支持

如需技术支持、提交错误报告或提出功能请求，请联系：

- **电子邮件**：[helpdesk@deque.com](mailto:helpdesk@deque.com)
- **支持门户**：[support.deque.com](https://support.deque.com)
- **[支持指南](.github/SUPPORT.md)**

## 价格与销售

- **产品页面**：[deque.com/axe/mcp-server](https://www.deque.com/axe/mcp-server/)
- **联系销售团队**：[deque.com/contact](https://www.deque.com/contact)

## 关于 Deque

[Deque Systems](https://www.deque.com) 是数字可访问性领域的领先提供商。

- **LinkedIn**：[Deque Systems](https://www.linkedin.com/company/deque-systems/)
---
name: feishu-docx-powerwrite
description: 通过 OpenClaw 生成高质量的 Feishu/Lark Docx 文档。当您需要将 Markdown 格式的内容转换为格式规范的 Feishu Docx 文档（包含标题、列表、嵌套结构以及代码块）时，可以使用此工具。该工具提供了安全的工作流程、模板以及故障排除方案。触发方式包括：点击 Feishu 文档中的 “doc/docx” 链接、执行 “写入 Feishu 文档” 操作、生成新的 Feishu 文档、追加或替换现有 Docx 文件，或者当用户希望文档始终保持一致的格式时。
---

# Feishu Docx PowerWrite

本技能专注于使用 OpenClaw 的 Feishu OpenAPI 工具来**可靠地生成外观精美的 Feishu Docx 文档**。

**核心理念**：优先使用 `feishu_docx_write_markdown` 方法（将 Markdown 格式转换为 Docx 格式），以保留文档的结构。

## 快速工作流程

1) 获取 `document_id`（Docx 文档的唯一标识符）：
   - 从 Docx 文档的 URL 中获取：`https://.../docx/<document_id>`

2) 确定写作模式：
   - **追加内容**：在现有内容下方添加新内容（最常用的方式）
   - **替换内容**：覆盖整个文档（请谨慎使用）

3) 编写 Markdown 内容：
   - 使用标题、列表和简短的段落
   - 避免使用过长的单一段落（不利于阅读）

## 推荐的默认设置

### 追加内容模式（安全）
适用于添加新章节、会议记录或每日日志等情况：
- `mode: append`
- 如果可能的话，确保每次追加的内容不超过 300-600 行

### 替换内容模式（会破坏现有文档）
适用于从头开始生成完整文档的情况：
- `mode: replace`
- 必须设置 `confirm: true` 以确认操作

## 能够良好渲染的 Markdown 格式示例

### 标题 + 摘要
```md
# <Title>

**Summary**
- Point 1
- Point 2

---
```

### 文章章节
```md
## Section

Short paragraph.

- Bullet
- Bullet

### Subsection

1) Step
2) Step
```

### 代码示例
使用代码块来展示代码内容：
```md
```bash
openclaw skills check
```
```

## 模板与参考资料
- 模板：`references/templates.md`
- 故障排除指南：`references/troubleshooting.md`

## 安全性 / 隐私保护
- 严禁在此技能中硬编码任何令牌（token）、聊天 ID（chat_id）、开放 ID（open_id）或文档链接。
- 必须使用用户自己的 Feishu 应用程序凭证和权限范围。
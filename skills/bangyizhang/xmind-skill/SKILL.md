---
name: xmind
description: 通过已发布的 `xmind-generator-mcp` MCP 服务器（基于 npm 的包），可以生成和读取 XMind (.xmind) 文件，同时提供以聊天为主要交互方式的用户体验。
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["mcporter", "npx"]
    install:
      - id: npm
        kind: note
        label: "Uses npx xmind-generator-mcp@0.1.2 (no separate install needed)"
---
# xmind 🧠

使用已发布的MCP服务器`xmind-generator-mcp`（npm）来生成和读取XMind格式的`.xmind`文件。

此功能以聊天交互为主：
- “根据这个内容生成一个XMind文件（可选：保存到……）” → 生成一个`.xmind`文件并发送回去。
- “阅读这个XMind文件，然后告诉我它的内容是什么” → 首先解释思维导图的结构和内容，然后提供Markdown格式的导出选项。

## 使用场景
- 当用户需要根据某个大纲、计划、产品需求文档（PRD）或测试计划生成XMind文件时。

## 输入格式（用于生成）
MCP工具`generate-mind-map`接受**Schema A**格式的JSON数据：
```json
{
  "title": "Root topic",
  "filename": "mindmap-name-no-date",
  "topics": [
    {
      "title": "Topic title (keep core info in the title)",
      "note": "Optional: use sparingly; only when the title would be too long",
      "labels": ["optional"],
      "markers": ["Arrow.refresh"],
      "children": [{"title": "Child topic"}]
    }
  ]
}
```

## 助手如何通过mcporter调用MCP服务器
### 生成XMind文件
使用`npx xmind-generator-mcp@0.1.2`作为MCP服务器命令：
```bash
mcporter call --stdio "npx -y xmind-generator-mcp@0.1.2" generate-mind-map --args '{...}'
```

### 读取XMind文件（提供Markdown格式的导出）
```bash
mcporter call --stdio "npx -y xmind-generator-mcp@0.1.2" read-mind-map --args '{"inputPath":"/path/to/file.xmind","style":"A"}'
```

## 聊天中的交互流程（用户体验要求）
当用户发送一个`.xmind`文件并请求“阅读/理解”其内容时：
1. 首先详细解释思维导图的主题、结构、关键点以及需要采取的行动项。
2. 然后询问用户是否需要导出文件。
3. 如果用户需要导出，默认使用Markdown格式。

- `generate --output`参数可以指定输出目录（推荐）或完整的`.xmind`文件路径。
- 如果省略`outputPath`参数，MCP服务器会使用配置的`outputPath`环境变量来确定输出路径（详见下文）。

## 聊天交互的工作流程
- 用户可以使用以下触发语句：
  - “根据这个内容生成一个XMind文件”
  - “阅读这个XMind文件”
  - “总结这个XMind文件”

**语言规则**：
- 如果用户没有明确指定思维导图的语言，系统会自动匹配用户请求的语言：
  - 例如：用户用中文提问 → 生成中文的思维导图标题。
  - 例如：用户用英文提问 → 生成英文的思维导图标题。
- 只有在用户明确要求时（如“用英文生成”）才会切换语言。

**文件命名规则**：
- 如果用户提供了文件名或路径，系统会使用该路径。
- 如果用户没有提供文件名：
  - 默认文件名应根据用户请求的语言来命名：
    - 中文文件名：使用短横线分隔的格式（例如：`one-day-trip-detailed`）。
    - 英文文件名：使用简短的字符串（例如：`hong-kong-1-day-itinerary`）。
- 系统会自动处理无效的文件名字符（如`\\ / : * ? \" < > |`），将其替换为`-`。

**具体步骤**：
1. 检查用户是否指定了保存位置或路径。如果指定了路径，则使用该路径；否则默认保存在`~/Desktop`。
2. 确定输出语言：如果用户指定了语言，则使用该语言；否则根据用户消息的语言来决定。
3. 将用户提供的内容转换为Schema A格式的JSON数据（使用用户选择的语言）。
4. 保持文件大小适中（避免一次性生成包含数千个节点的文件）。
5. 根据需要使用XMind格式的标记元素来丰富文件内容（但注意保持标题的简洁性）：
  - `note`：谨慎使用。只有当内容过于冗长或难以体现在标题中时，才将其放入`note`字段；如果内容对思维导图的结构至关重要，应直接放在标题中。
  - `labels`：添加简单的分类标签（如“必做项/可选项/雨天活动/适合家庭”）。
  - `relationships`：仅用于表示跨分支的关联关系，以增强文件的可读性。
6. 将生成的JSON数据写入临时文件（例如：`/tmp/xmind-<ts>.json`）。
7. 通过mcporter调用`generate-mind-map`工具（`npx xmind-generator-mcp@0.1.2`）来生成`.xmind`文件，并获取输出文件的路径。
8. 将生成的`.xmind`文件作为附件发送回聊天界面。
9. （可选）告知用户文件在磁盘上的保存位置。
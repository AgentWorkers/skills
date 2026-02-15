---
name: noverload
description: 为你的智能助手配备一个可搜索的知识库——支持语义搜索、主题归纳以及对你保存的 YouTube 视频、文章、Reddit 帖子、X（TikTok）帖子和 PDF 文件中的操作进行追踪。
homepage: https://noverload.com/openclaw
user-invocable: true
mcp-server:
  command: npx
  args: ["-y", "noverload-mcp@latest"]
  env:
    NOVERLOAD_CONFIG: '{"accessToken":"${NOVERLOAD_TOKEN}","apiUrl":"https://www.noverload.com","readOnly":true}'
---

# Noverload – 为AI代理提供的知识管理工具

您的代理现在可以访问您的整个知识库。您可以进行语义搜索，跨来源合成见解，并跟踪您保存的所有内容中的待办事项。

## Noverload提供的功能

- **语义搜索**：根据内容含义进行搜索，而不仅仅是关键词。支持YouTube转录文本、文章、Reddit帖子、X平台（如Twitter）的帖子以及PDF文件。
- **AI摘要**：每条内容都会被自动处理，提取出关键见解、待办事项和要点。
- **主题分析**：结合来自多个来源的见解，发现其中的模式、矛盾之处以及相互关联的内容。
- **任务跟踪**：从内容中提取的任务会根据您的“健康”、“财富”和“人际关系”目标进行分类。
- **框架提取**：从您保存的内容中提取方法论、流程和逐步指导。

## 设置

### 1. 获取您的访问令牌

1. 在https://noverload.com注册（提供免费试用）
2. 进入“设置”>“应用程序”
3. 点击“新建令牌”以创建个人访问令牌
4. 复制令牌（您之后将无法再次看到它）

### 2. 配置OpenClaw

将以下代码添加到`~/.openclaw/openclaw.json`文件中：

```json
{
  "skills": {
    "entries": {
      "noverload": {
        "env": {
          "NOVERLOAD_TOKEN": "nv_your_token_here"
        }
      }
    }
  }
}
```

该技能在内部使用了MCP（Model Context Protocol）协议。激活该技能时，系统会通过`npx`命令自动启动Noverload MCP服务器。

### 启用内容保存功能（可选）

出于安全考虑，该技能默认为**只读**模式。若要允许您的代理保存新内容，请执行以下操作：

```json
{
  "mcpServers": {
    "noverload": {
      "command": "npx",
      "args": ["-y", "noverload-mcp@latest"],
      "env": {
        "NOVERLOAD_CONFIG": "{\"accessToken\":\"nv_your_token\",\"readOnly\":false}"
      }
    }
  }
}
```

将`readOnly: false`设置为`true`后，您的代理可以：
- 将新的URL保存到知识库中
- 为内容添加标签
- 将某些内容标记为需要处理的文件
- 完成已保存内容中的待办事项

### 3. 重启OpenClaw

下次会话时，该技能将可用。

## 可用的命令

### 搜索您的知识库

```
Search my Noverload for productivity tips
Find content about machine learning in my library
What have I saved about negotiation tactics?
Look for anything about React Server Components
```

该搜索功能支持语义匹配，能够理解内容的实际含义而不仅仅是关键词。请使用自然语言进行查询。

### 获取完整内容

```
Get the full transcript of that Naval podcast
Show me the complete article about pricing strategy
Give me details on the YouTube video about habits
```

检索内容的完整文本、摘要、关键见解和元数据。

### 合成主题

```
Synthesize what I've saved about startup growth
Find patterns across my productivity content
What do different sources say about remote work?
Compare perspectives on AI safety from my library
```

分析多个来源的内容，找出其中的关联、矛盾之处以及可执行的模式。

### 提取框架

```
What methodologies have I saved for building habits?
Find step-by-step processes from my content
What frameworks exist in my library for cold outreach?
```

从您保存的内容中提取结构化的方法论和流程。

### 跟踪待办事项

```
What action items do I have from my saved content?
Show pending tasks for my Health goals
What should I work on based on what I've learned?
Mark the meditation action as complete
```

### 保存新内容

```
Save this URL to Noverload: https://example.com/article
Add this video to my knowledge base
```

保存内容以供进一步处理（系统会自动生成摘要、待办事项和相关数据）。

### 浏览知识库

```
What YouTube videos have I saved recently?
Show my articles from last week
List content tagged with "marketing"
```

## 示例工作流程

- **晨间简报**
- **研究模式**
- **写作辅助**
- **学习路径**
- **决策支持**

## 支持的内容类型

| 类型 | 可提取的信息 |
|------|---------------------|
| YouTube | 完整转录文本、时间戳、关键内容、待办事项 |
| 文章 | 完整文本、主要论点、引用、方法论 |
| Reddit | 帖子及热门评论、讨论主题、建议 |
| X/Twitter | 帖子文本、关键点、链接内容 |
| PDF文件 | 带有OCR技术的完整文本、文档结构、高亮部分 |

## 优化搜索效果的提示

1. **使用具体关键词**：例如“Paul Graham对创业想法有什么看法？”比“关于创业的内容”更有效。
2. **使用自然语言**：搜索系统能够理解上下文和含义。
3. **组合使用多个命令**：先搜索，再对结果进行综合分析。
4. **查看待办事项**：您保存的内容中会包含提取出的任务，请及时处理它们。

## 隐私与安全

- 您的数据仅存储在您的Noverload账户中。
- 代理通过安全的、可撤销的访问令牌进行访问。
- 提供只读模式以增加安全性。
- 任何内容都不会存储在OpenClaw服务器上。
- 您可以在Noverload的设置中随时撤销代理的访问权限。

## 限制

| 订阅计划 | 可保存的内容量 | MCP访问权限 |
|------|---------------|------------|
| 免费 | 每月10条内容 | 无 |
| 专业版 | 无限量内容 | 有 |
| 试用版 | 无限量内容（7天） | 有 |

MCP/API访问权限属于专业版功能。您可以尝试7天的免费试用。

## 帮助支持

- 文档说明：https://noverload.com/docs/mcp
- OpenClaw集成指南：https://noverload.com/openclaw
- 电子邮件支持：support@noverload.com

## 版本

1.0.0 – 首次为OpenClaw发布
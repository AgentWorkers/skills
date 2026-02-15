---
name: devlog
tags:
  - devlog
  - blog
  - dev blog
  - builder's log
  - coding session blog
  - session summary
  - write about what I built
  - blog about a feature
  - write up our coding session
  - tutorial from sessions
  - publish a devlog
description: >-
  Generate narrative blog posts from AI coding session transcripts. Reads
  session files, selects sessions relevant to a topic, and produces an
  agent-narrated blog post about the human-agent collaboration. Supports
  builder's log, tutorial, and technical deep-dive styles.
version: 0.1.0
---

# 开发日志生成器

该工具能够根据人类与智能助手的编码会话记录生成叙述性的开发博客文章。博客内容以智能助手的第一人称视角撰写，其中“我”代表智能助手，而人类开发者则被称为“我的人类”。

## 工作流程

### 第1阶段：理解用户需求

从用户输入的信息中提取以下内容：
- **项目**：使用的是哪个代码库？（例如 “eastore”、“filecoin”、“couponswap”）；如果未指定，则使用当前工作目录。
- **主题/功能**：具体是关于哪个功能或模块？（例如 “认证系统”、“仪表盘” 或整个项目）；如果未指定，则包含所有会话记录。
- **写作风格**：是构建者日志（默认风格）、教程风格还是技术深度分析风格；只有在用户明确要求时才进行更改。
- **时间范围**：是“上周”的记录、“1月份的会话记录”还是全部会话记录（默认为全部）。

### 第2阶段：查找会话记录

确定需要扫描的平台。查看 `references/platforms/` 目录中列出的支持平台——每个子目录对应一个平台。可以根据当前环境或用户请求自动选择平台。

**仅** 加载与项目相关的平台目录。每个平台目录包含一个参考文件（存储结构、会话路径和查找说明文件），以及两个脚本文件（`list-sessions.sh` 和 `read-session.sh`）。切勿一次性加载所有平台的参考文件。

运行该平台的 `list-sessions.sh <project>` 命令来查找匹配的会话记录，或者按照平台参考文件中的说明手动进行查找。

如果某个平台在 `references/platforms/` 目录中没有对应的参考文件，则需要手动查找会话记录：检查该平台的数据/配置目录（例如 `~/.local/share/`、`~/.config/`、`~/Library/`），寻找会话存储文件（JSONL、JSON、SQLite 格式），并根据文件中的结构提取人类与智能助手的对话内容。遵循第3阶段的过滤规则。

将找到的会话索引展示给用户进行确认。

### 第3阶段：选择并读取会话记录

从会话索引中筛选出与用户需求相关的会话记录，并阅读这些会话的完整记录。

在阅读会话记录时，重点保留以下内容：
- **用户输入的文本**：人类的意图、指令和修改内容。
- **智能助手的文本**：智能助手的推理过程、建议和解释。
- **工具调用名称及文件路径**：展示了具体完成了哪些操作。
- **错误信息**：记录了遇到的问题及调试过程。

同时删除以下内容：
- **工具生成的原始数据**（如文件内容、grep 命令的输出等，这些通常占文本的80-90%）。
- **系统生成的提示信息、使用元数据以及压缩/摘要信息**。
- **工具输入的完整参数**（仅保留名称和文件路径，无需保留完整的差异信息）。

具体字段名称和解析细节请参考第2阶段加载的平台参考文件。

如果筛选后的会话记录仍然过于冗长，可以按会话进行分段处理：先为每个会话生成摘要，然后再整合所有会话的内容。在编写博客时，优先展示人类与智能助手的对话内容，而非工具调用的详细信息。

### 第4阶段：撰写博客

阅读 `references/blog-writing-guide.md` 以获取撰写指南。其中包含了语音设置、协作用词、文本提取规则以及博客的结构要求。

参考 `examples/` 目录中的示例文件，了解不同的写作风格：
- `examples/builders-log.md`：构建者日志风格的示例。
- `examples/tutorial.md`：教程风格的示例。
- `examples/technical.md`：技术深度分析风格的示例。

加载 `assets/devlog-template.md` 作为博客的框架模板。这个模板并非固定不变，可以根据实际会话内容调整章节顺序、合并内容或删除某些部分。对于单个会话的博客，可以省略某些章节标题；对于涉及多次迭代的过程，可以将相关内容拆分为多个章节。让内容本身决定博客的结构。

按照撰写指南生成博客内容。博客必须以智能助手的第一人称视角撰写，并将人类开发者称为“我的人类”。当会话涉及系统架构、流程或多组件交互时，可以使用 Mermaid 图表来可视化相关内容（具体使用方法请参见撰写指南中的图示说明部分）。

### 第5阶段：输出结果

将生成的博客文件保存到当前工作目录下的 `{project}-{topic}-devlog.md` 文件中，或者用户指定的路径下。

同时提供以下信息：
- 博客的标题。
- 博文的总字数。
- 包含的会话记录数量。
- 覆盖的时间范围。
- 引用的关键文件。

### 第6阶段：发布博客

1. 询问用户是否希望将博客发布到线上。
2. 如果用户同意发布，查看 `references/publishing/` 目录中列出的支持平台。每个子目录对应一个发布平台。
3. 加载相应平台的参考文件，以获取发布所需的API详细信息和要求。
4. 检查是否缺少必要的环境变量（例如 Hashnode 的 `HASHNODE_PAT`、`HASHNODE_PUBLICATION_ID`）。
5. 如果缺少任何变量，告知用户如何设置这些变量（例如在 `~/.zshrc` 或 `~/.bashrc` 中添加 `export HASHNODE_PAT=...`）。请用户提供当前会话所需的变量值。
6. **封面图片（可选）**：如果具备图片生成能力（例如使用图像生成工具或 MCP 服务器），可以生成一张能够体现博客主题的封面图片，并通过 `--cover-image <url>` 参数将其传递给 `publish.sh` 命令。封面图片应为横向布局（1200×630像素或类似尺寸），与博客主题相关，且不能包含与标题重复的文字。如果没有图片生成能力，可以跳过此步骤。
7. 运行 `publish.sh` 命令，传入博客文件路径和标题（如果使用了封面图片，则加上 `--cover-image <url>` 参数）。
8. 将发布的博客链接告知用户。

## 特殊情况处理

| 情况 | 处理方式 |
|---|---|
| 未找到会话记录 | 报告已扫描的路径，并询问用户是否需要检查项目名称或提供正确的路径。 |
| 项目名称不明确 | 列出所有匹配的项目，让用户选择具体项目。 |
| 只有一个会话记录 | 使用简化的结构，无需多个章节的标题。 |
| 会话记录过长（超过5000行） | 分段处理会话内容，先总结每个部分的要点，然后再整合整体内容。 |
| 涉及多个平台 | 按时间顺序合并来自不同平台的会话记录。 |
| 如果使用的是子智能助手的会话记录 | 默认情况下跳过这些记录，因为主会话记录已经包含了相关内容。 |
- 用户请求查看最近的操作记录 | 直接使用当前会话的记录内容，无需再次生成 JSONL 格式的文件。 |
- 会话记录已被压缩 | 压缩后的文件不会删除原始数据，仍需完整读取所有内容（忽略压缩后的摘要信息）。 |
- 用户拒绝发布 | 完全跳过第6阶段，因为博客文件已经保存在本地。 |

## 参考资源

### 平台参考文件（仅加载相关文件）

- **`references/platforms/claude-code/`**：Claude 代码平台的参考资料和脚本：
  - `claude-code.md`：会话路径、JSONL 数据结构及查找说明。
  - `list-sessions.sh`：用于扫描 Claude 代码平台的会话记录。
  - `read-session.sh`：用于从 Claude 代码的 JSONL 文件中提取会话记录。
- **`references/platforms/opencode/`**：OpenCode 平台的参考资料和脚本：
  - `opencode.md`：存储结构、JSON 数据格式及查找说明。
  - `list-sessions.sh`：用于扫描 OpenCode 平台的会话记录。
  - `read-session.sh`：用于从 OpenCode 的 JSON 数据结构中提取会话记录。
- **`references/platforms/openclaw/`**：OpenClaw 平台的参考资料和脚本：
  - `openclaw.md`：会话路径、JSONL 数据结构及查找说明。
  - `list-sessions.sh`：用于扫描 OpenClaw 平台的会话记录。
  - `read-session.sh`：用于从 OpenClaw 的 JSONL 文件中提取会话记录。
- **`references/platforms/codex/`**：Codex 平台的参考资料和脚本：
  - `codex.md`：部署文件格式、JSONL 数据结构及查找说明。
  - `list-sessions.sh`：用于扫描 Codex 的部署文件。
  - `read-session.sh`：用于从 Codex 的部署文件中提取会话记录。
- **`references/platforms/gemini-cli/`**：Gemini CLI 平台的参考资料和脚本：
  - `gemini-cli.md`：JSON 格式的会话记录格式、项目哈希规则及查找说明。
  - `list-sessions.sh`：用于扫描 Gemini CLI 的会话记录。
  - `read-session.sh`：用于从 Gemini CLI 的会话文件中提取会话记录。
- **`references/blog-writing-guide.md`：语音设置、协作用词、文本提取规则及博客结构指南。

### 发布平台（仅加载相关文件）

- **`references/publishing/hashnode/`**：Hashnode 平台的发布参考资料和脚本：
  - `hashnode.md`：GraphQL API 端点、认证信息及 `publishPost` 操作的详细说明。
  - `publish.sh`：用于将博客文件发布到 Hashnode 平台。

### 示例文件

- `examples/builders-log.md`：构建者日志风格的示例。
- `examples/tutorial.md`：教程风格的示例。
- `examples/technical.md`：技术深度分析风格的示例。

### 资源文件

- `assets/devlog-template.md`：博客的模板文件。
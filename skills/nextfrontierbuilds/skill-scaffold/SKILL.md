---
name: skill-scaffold
description: AI代理技能搭建命令行工具（CLI）。可快速为OpenClaw、Moltbot、Claude、Cursor、ChatGPT、Copilot等平台创建新技能。支持Vibe-coding编程方式，兼容MCP（Machine Learning Platform）。
author: NextFrontierBuilds
version: 1.0.4
keywords:
  - ai
  - ai-agent
  - ai-coding
  - skill
  - scaffold
  - generator
  - openclaw
  - moltbot
  - mcp
  - claude
  - claude-code
  - chatgpt
  - cursor
  - copilot
  - github-copilot
  - vibe-coding
  - cli
  - devtools
  - agentic
  - ai-tools
  - developer-tools
  - typescript
  - llm
  - automation
---

# 技能模板生成器（Skill Scaffold）

该工具可快速创建 AI 代理技能模板，支持 OpenClaw/Moltbot、MCP 服务器以及通用的技能结构。

## 触发词

当用户输入以下命令时，将使用此工具：
- `create a skill`（创建技能）
- `scaffold a skill`（生成技能模板）
- `new skill template`（新建技能模板）
- `skill generator`（技能生成器）
- `make a openclaw skill`（创建 OpenClaw 技能）
- `mcp server template`（创建 MCP 服务器模板）

## 快速入门

```bash
# Install globally
npm install -g skill-scaffold

# Create a OpenClaw skill
skill-scaffold my-awesome-skill

# Create an MCP server
skill-scaffold my-api --template mcp

# With all options
skill-scaffold weather-bot --template openclaw --cli --description "Weather alerts for agents"
```

## 命令

| 命令          | 描述                                      |
|-----------------|-----------------------------------------|
| `skill-scaffold <名称>`    | 使用默认（OpenClaw）模板创建技能                  |
| `skill-scaffold <名称> --template mcp` | 使用 MCP 服务器模板创建技能                  |
| `skill-scaffold <名称> --template generic` | 使用通用模板创建技能                  |
| `skill-scaffold <名称> --cli`    | 包含 CLI 可执行文件模板                         |
| `skill-scaffold --help`    | 显示帮助信息                               |

## 模板类型

### OpenClaw（默认模板）

适用于 OpenClaw/Moltbot 代理的完整技能结构：
- `SKILL.md` 文件（包含 YAML 标头、触发词、命令列表等）
- `README.md` 文件（包含徽章、安装说明、功能介绍等）
- `scripts/` 文件夹（存放辅助脚本）

### MCP 模板

适用于 Model Context Protocol（MCP）服务器的技能模板：
- `SKILL.md` 文件（包含 MCP 配置示例）
- 工具和资源文档
- 适用于 Claude Desktop/Cursor 等平台的集成

### 通用模板

最基本的技能结构：
- `SKILL.md` 文件
- `README.md` 文件

## 选项

| 选项            | 描述                                      | 默认值                         |
|-----------------|-----------------------------------------|
| `--template <类型>`     | 模板类型（openclaw/mcp/generic）                   | openclaw                         |
| `--author <名称>`     | 技能作者名称                             | NextFrontierBuilds                         |
| `--description <文本>` | 技能描述                                  | 自动生成                         |
| `--dir <路径>`     | 输出目录                                   | 当前目录                         |
| `--cli`         | 是否包含 CLI 可执行文件                         | false                         |
| `--no-scripts`     | 是否跳过辅助脚本文件夹                         | false                         |

## 使用示例

```bash
# Create in current directory
skill-scaffold my-skill

# Create in specific directory
skill-scaffold my-skill --dir ~/clawd/skills

# MCP server with custom author
skill-scaffold github-mcp --template mcp --author "YourName"

# Full CLI tool
skill-scaffold awesome-cli --cli --description "Does awesome things"
```

## 输出结构

```
my-skill/
├── SKILL.md       # Main documentation (OpenClaw reads this)
├── README.md      # GitHub/npm readme
├── scripts/       # Helper scripts (optional)
└── bin/           # CLI binary (if --cli flag used)
    └── my-skill.js
```

## 使用步骤

1. 进入技能目录（例如：`cd my-skill`）
2. 使用文本编辑器编辑 `SKILL.md` 文件，添加实际的内容和文档。
3. 添加实现代码（脚本或可执行文件）。
4. 在本地进行测试。
5. 发布技能：`clawdhub publish .` 或 `npm publish`。

## 注意事项

- 技能名称必须使用小写字母，并仅包含连字符（-）。
- 生成的文件会自动包含相关的 SEO 关键词。
- 该工具支持 OpenClaw、Moltbot 以及任何能够读取 `SKILL.md` 文件的代理平台。
---
name: skill-porter
description: 将 Claude Code 中的技能转换为 Gemini CLI 扩展程序，反之亦然。当用户希望使某个技能具备跨平台兼容性、在多个平台上移植该技能，或创建一个同时适用于 Claude Code 和 Gemini CLI 的通用扩展程序时，可以使用此功能。
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Skill Porter - 跨平台技能转换器

该工具能够自动将 Claude Code 中的技能转换为 Gemini CLI 扩展程序，从而实现真正的跨平台 AI 工具开发。

## 核心功能

### 双向转换

在保持功能不变的前提下，实现技能和扩展程序在各个平台之间的相互转换：

**示例请求：**
- “将这个 Claude 技能转换为适用于 Gemini CLI 的格式”
- “使我的 Gemini 扩展程序兼容 Claude Code”
- “创建一个同时支持两个平台的通用版本”
- “将 ‘database-helper’ 技能移植到 Gemini”

### 智能平台检测

自动分析目录结构以确定源平台：

**检测标准：**
- Claude：存在带有 YAML 前言的 `SKILL.md` 文件或 `.claude-plugin/marketplace.json` 文件
- Gemini：存在 `gemini-extension.json` 或 `GEMINI.md` 配置文件
- 通用版本：同时包含两个平台的配置文件

**示例请求：**
- “这个技能是为哪个平台开发的？”
- “分析这个扩展程序，告诉我需要做哪些转换”
- “这是 Claude 技能还是 Gemini 扩展程序？”

### 元数据转换

智能地处理平台特定的格式转换：

**支持的转换类型：**
- YAML 前言 ↔ JSON 显示格式
- `allowed-tools`（允许使用的工具列表） ↔ `excludeTools`（禁止使用的工具列表）
- 环境变量 ↔ 设置配置
- MCP 服务器配置路径
- 平台特定的文档格式

**示例请求：**
- “将这个 Claude 技能的元数据转换为 Gemini 格式”
- “将允许使用的工具列表转换为 Gemini 的禁止使用模式”
- “根据这些环境变量生成设置配置”

### MCP 服务器配置的保留

在不同平台上保持 Model Context Protocol（MCP）服务器配置的一致性：

**示例请求：**
- “确保 MCP 服务器配置在两个平台上都能正常使用”
- “更新用于 Gemini 的 ${extensionPath} 变量的 MCP 服务器路径”
- “验证 MCP 配置是否兼容”

### 验证与质量检查

确保转换后的输出符合平台要求：

**验证内容：**
- 是否包含所有必要的文件（如 `SKILL.md`、`gemini-extension.json` 等）
- YAML/JSON 语法是否正确
- 前言结构是否正确
- MCP 服务器路径是否能够正确解析
- 工具限制是否有效
- 设置配置是否完整

**示例请求：**
- “验证这个转换后的技能”
- “检查这个 Gemini 扩展程序是否满足所有要求”
- “这个转换结果是否可以直接安装？”

## 转换流程

当你请求转换时，我会执行以下步骤：
1. **分析** 源目录的结构
2. **检测** 该技能是为哪个平台开发的
3. **提取** 元数据、MCP 配置和文档
4. **转换** 数据到目标平台的格式
5. **生成** 目标平台所需的文件
6. **验证** 转换结果是否满足所有要求
7. **报告** 转换的内容以及任何需要手动处理的步骤

## 处理的平台差异

### 文件结构
- **Claude**：`SKILL.md` + `.claude-plugin/marketplace.json`
- **Gemini**：`GEMINI.md` + `gemini-extension.json`
- **通用版本**：同时包含上述两种格式的文件以及共享文档

### 元数据格式
- **Claude**：`SKILL.md` 文件中的 YAML 前言
- **Gemini**：`GEMINI.md` 文件中的 JSON 显示格式
- **转换**：支持双向的 YAML ↔ JSON 转换

### 工具限制
- **Claude**：`allowed-tools`（允许使用的工具列表）
- **Gemini**：`excludeTools`（禁止使用的工具列表）
- **转换**：通过智能映射实现逻辑反转

### 配置
- **Claude**：用户运行前设置的环境变量
- **Gemini**：安装过程中提示的设置配置
- **转换**：从环境变量中推断配置信息或生成环境变量文档

### MCP 服务器路径
- **Claude**：从技能目录开始的相对路径
- **Gemini**：使用 `${extensionPath}` 变量进行路径替换
- **转换**：自动进行路径转换

## 使用示例

### 将 Claude 技能转换为 Gemini

```
User: "I have a Claude skill at ./database-helper. Convert it to Gemini."
Claude: I'll analyze the skill and convert it to Gemini format...
- Detected Claude skill (found SKILL.md with frontmatter)
- Extracted metadata and MCP configuration
- Generated gemini-extension.json and GEMINI.md
- Transformed allowed-tools to excludeTools
- Created settings schema from environment variables
✓ Conversion complete! Ready to install with: gemini extensions install ./database-helper
```

### 将 Gemini 扩展程序转换为 Claude

```
User: "Port my Gemini extension to Claude Code"
Claude: I'll convert this Gemini extension to a Claude skill...
- Detected Gemini extension (found gemini-extension.json)
- Extracted manifest and context file
- Generated SKILL.md with YAML frontmatter
- Created .claude-plugin/marketplace.json
- Converted excludeTools to allowed-tools
✓ Conversion complete! Install with: cp -r ./extension ~/.claude/skills/
```

### 创建通用扩展程序

```
User: "Make this skill work on both platforms"
Claude: I'll create a universal extension structure...
- Analyzing current configuration
- Generating both Claude and Gemini files
- Moving shared content to shared/ directory
- Updating MCP server paths for both platforms
✓ Universal extension created! Works with both Claude Code and Gemini CLI
```

## 高级功能

### 生成 Pull Request

为父仓库创建一个 Pull Request，以添加对两个平台的支持：

**示例请求：**
- “将这个技能转换为适用于 Gemini 的格式，并创建一个 Pull Request”
- “生成一个包含通用版本的 Pull Request”

### 分支并设置双平台支持

创建一个同时包含两个平台配置的分支：

**示例请求：**
- “克隆这个仓库，并为其设置双平台支持”
- “创建一个可以在两个 CLI 上使用的双平台分支”

### 仅进行兼容性检查

在不进行转换的情况下检查兼容性：

**示例请求：**
- “验证这个技能是否可以转换为 Gemini 格式”
- “检查这个扩展程序是否可以移植到 Claude”
- “需要做哪些修改才能使其具有通用性？”

## 配置要求

该工具直接在文件系统中操作，无需外部配置。它使用以下方式：
- 文件系统访问来读取和写入技能/扩展程序文件
- Git 操作来处理 Pull Request 和分支功能
- GitHub CLI (`gh`) 来执行仓库相关操作

## 安全特性

- **非破坏性**：仅创建新文件，除非用户明确要求，否则不会修改源文件
- **验证**：在转换完成前检查输出结果
- **报告**：提供详细的变更摘要
- **易于回滚**：所有更改都是标准的文件操作

## 限制

某些方面可能需要手动处理：
- 自定义的命令（特定于平台的语法）
- 包含多个服务器的复杂 MCP 服务器配置
- 无法直接转换的特定于平台的脚本
- 工具限制映射中的边缘情况

这些情况会在转换报告中被标出。

## 技术细节

### 工具限制的转换规则

**Claude → Gemini（允许使用的工具列表 → 禁止使用的工具列表）**：
- 分析允许使用的工具列表
- 为其他所有工具生成禁止使用的模式
- 对通配符权限进行特殊处理

**Gemini → Claude（禁止使用的工具列表 → 允许使用的工具列表）**：
- 列出所有可用的工具
- 移除被禁止的工具
- 生成允许使用的工具列表

### 设置配置的推断

在将 Claude 转换为 Gemini 时，MCP 配置中的环境变量会被转换为设置配置：

```javascript
// MCP env var
"env": { "DB_HOST": "${DB_HOST}" }

// Becomes Gemini setting
"settings": [{
  "name": "DB_HOST",
  "description": "Database host",
  "default": "localhost"
}]
```

### 路径转换

Claude 使用相对路径，Gemini 使用变量：

```javascript
// Claude
"args": ["mcp-server/index.js"]

// Gemini
"args": ["${extensionPath}/mcp-server/index.js"]
```

---

*有关实现细节，请访问仓库：https://github.com/jduncan-rva/skill-porter*
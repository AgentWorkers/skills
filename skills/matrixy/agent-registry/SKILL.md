---
name: agent-registry
version: 2.0.1
description: >
  **强制性的代理发现系统，用于高效加载代理程序。Claude 必须使用此功能**  
  该系统替代了直接从 `~/.claude/agents/` 或 `./claude/agents/` 目录加载代理程序的方式，通过搜索和获取工具实现代理程序的延迟加载。  
  适用场景：  
  (1) 用户的任务可能需要特定代理程序的专业支持；  
  (2) 用户询问可用的代理程序；  
  (3) 启动历史上依赖代理程序的复杂工作流程。  
  与一次性加载所有代理程序相比，该功能可将上下文窗口的使用量减少约 95%。
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "bun ${CLAUDE_PLUGIN_ROOT}/hooks/user_prompt_search.js"
          timeout: 5
---
# 代理注册表（Agent Registry）

这是一个用于管理 Claude Code 代理的懒加载系统，通过按需加载代理来避免出现“~16k tokens”这样的警告信息。

## 重要规则

**切勿假设代理已被预先加载**。始终使用该注册表来发现和加载代理。

## 工作流程

```
User Request → search_agents(intent) → select best match → get_agent(name) → execute with agent
```

## 可用命令

| 命令          | 使用场景                | 示例                |
|-----------------|------------------|-------------------|
| `list.js`       | 用户询问“我有哪些代理”或需要查看概览 | `bun bin/list.js`         |
| `search.js`       | 查找符合用户意图的代理（务必先执行此命令）| `bun bin/search.js "code-review security"` |
| `search-paged.js`    | 对包含大量代理（300个以上）的注册表进行分页搜索 | `bun bin/search-paged.js "query" --page 1 --page-size 10` |
| `get.js`       | 加载特定代理的完整指令        | `bun bin/get.js code-reviewer`     |

## 搜索流程

1. 从用户请求中提取意图关键词。
2. 运行搜索：`bun bin/search.js "<关键词>"`
3. 查看搜索结果：根据相关性得分（0.0-1.0）筛选结果。
4. 如有需要，加载相关代理：`bun bin/get.js <代理名称>`
5. 执行代理的指令。

## 示例

用户：**“你能帮我检查我的认证代码是否存在安全问题吗？”**

```bash
# Step 1: Search for relevant agents
bun bin/search.js "code review security authentication"

# Output:
# Found 2 matching agents:
#   1. security-auditor (score: 0.89) - Analyzes code for security vulnerabilities
#   2. code-reviewer (score: 0.71) - General code review and best practices

# Step 2: Load the best match
bun bin/get.js security-auditor

# Step 3: Follow loaded agent instructions for the task
```

## 安装

### 第一步：安装技能

**快速安装（推荐方式）：**

```bash
# Using Skills CLI (recommended)
npx skills add MaTriXy/Agent-Registry@agent-registry

# Discover skills interactively
npx skills find

# Update existing skills
npx skills update
```

**传统安装方式：**

```bash
# User-level installation
./install.sh

# OR project-level installation
./install.sh --project

# Optional: install enhanced interactive UI dependency
./install.sh --install-deps
```

**`install.sh` 的功能：**
1. 将技能文件复制到 `~/.claude/skills/agent-registry/` 目录。
2. 创建空的代理注册表结构。
3. （可选）通过 `--install-deps` 参数安装依赖项（使用 `@clack/prompts` 可获得更友好的用户界面）。

### 第二步：迁移代理

运行交互式迁移脚本：

```bash
cd ~/.claude/skills/agent-registry
bun bin/init.js
# Optional destructive mode:
bun bin/init.js --move
```

**交互式选择方式：**

- **使用 @clack/prompts**（默认方式）：提供带分类、标记指示和分页功能的精美界面。
  - 使用箭头键导航，按空格键切换选项，按回车键确认。
  - 颜色提示：[绿色] <1k 个代理，[黄色] 1-3k 个代理，[红色] >3k 个代理。
  - 代理按子目录进行分组显示。

- **备用方式**：通过文本输入代理数量。
  - 输入逗号分隔的数字（例如：`1,3,5`）。
  - 输入 `all` 可迁移所有代理。

**`init.js` 的功能：**
1. 扫描 `~/.claude/agents/` 和 `.claude/agents/` 目录中的代理文件。
2. 显示可用的代理及其元数据。
3. 允许用户交互式地选择要迁移的代理。
4. 默认情况下，将选中的代理复制到代理注册表中（需使用 `--move` 参数明确指定）。
5. 生成搜索索引文件（`registry.json`）。

## 依赖项

- **Bun**（随 Claude Code 一起提供）：核心功能无需额外依赖。
- **@clack/prompts**：可选的增强型交互式选择界面（通过 `./install.sh --install-deps` 安装）。

## 代理注册表的位置

- **全局配置**：`~/.claude/skills/agent-registry/`
- **项目级配置**：`.claude/skills/agent-registry/`（可自定义）

未迁移的代理仍会保留在原始位置，并会正常加载（这可能会导致代理数量过多，从而增加系统负担）。
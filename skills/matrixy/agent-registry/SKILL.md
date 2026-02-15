---
name: agent-registry
description: |
  MANDATORY agent discovery system for token-efficient agent loading. Claude MUST use this skill 
  instead of loading agents directly from ~/.claude/agents/ or .claude/agents/. Provides lazy 
  loading via search_agents and get_agent tools. Use when: (1) user task may benefit from 
  specialized agent expertise, (2) user asks about available agents, (3) starting complex 
  workflows that historically used agents. This skill reduces context window usage by ~95% 
  compared to loading all agents upfront.
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

| 命令 | 使用场景 | 示例 |
|---------|-------------|---------|
| `list_agents.py` | 用户询问“我有哪些代理”或需要查看代理列表 | `python scripts/list_agents.py` |
| `searchAgents.py` | 根据用户意图查找匹配的代理（务必先执行此命令） | `python scripts/searchAgents.py "code-review security"` |
| `searchAgents_paged.py` | 对包含大量代理（300个以上）的注册表进行分页搜索 | `python scripts/searchAgents_paged.py "query" --page 1 --page-size 10` |
| `get_agent.py` | 加载特定代理的完整使用说明 | `python scripts/get_agent.py code-reviewer` |

## 搜索流程

1. 从用户请求中提取意图关键词。
2. 运行搜索：`python scripts/searchAgents.py "<关键词>"`
3. 查看搜索结果：查看相关性评分（0.0-1.0）。
4. 如有需要，加载代理：`python scripts/get_agent.py <代理名称>`
5. 执行：按照加载的代理的说明进行操作。

## 示例

用户：你能检查我的认证代码是否存在安全问题吗？

```bash
# Step 1: Search for relevant agents
python scripts/search_agents.py "code review security authentication"

# Output:
# Found 2 matching agents:
#   1. security-auditor (score: 0.89) - Analyzes code for security vulnerabilities
#   2. code-reviewer (score: 0.71) - General code review and best practices

# Step 2: Load the best match
python scripts/get_agent.py security-auditor

# Step 3: Follow loaded agent instructions for the task
```

## 安装

### 第一步：安装技能（Skill）

**快速安装（推荐）：**

```bash
# NPX with add-skill (recommended)
npx add-skill MaTriXy/Agent-Registry

# OR npm directly
npm install -g @claude-code/agent-registry
```

**传统安装方式：**

```bash
# User-level installation
./install.sh

# OR project-level installation
./install.sh --project
```

**`install.sh` 的功能：**
1. 将技能文件复制到 `~/.claude/skills/agent-registry/` 目录。
2. 创建空的注册表结构。
3. 自动安装 `questionary` Python 包（用于提供交互式用户界面）。
4. 如果 `pip3` 无法使用，会优雅地回退到其他安装方式。

**注意：** 所有安装方法都支持基于 Python 的迁移和命令行工具（CLI）。

### 第二步：迁移代理

运行交互式迁移脚本：

```bash
cd ~/.claude/skills/agent-registry
python scripts/init_registry.py
```

**交互式选择方式：**

- **使用 questionary（推荐）**：提供分类选择、token 数量指示以及分页功能
  - 使用上下箭头导航，空格键切换选项，回车键确认选择。
  - 可视化指示：🟢 <1k tokens, 🟡 1-3k, 🔴 >3k
  - 代理按子目录分组显示。

- **不使用 questionary（备用方式）**：通过文本输入代理 ID
  - 输入逗号分隔的代理 ID（例如：`1,3,5`）
  - 输入 `all` 以迁移所有代理。

**`init_registry.py` 的功能：**
1. 扫描 `~/.claude/agents/` 和 `.claude/agents/` 目录中的代理文件。
2. 显示可用代理及其元数据。
3. 允许用户交互式地选择要迁移的代理。
4. 将选中的代理迁移到注册表中。
5. 生成搜索索引文件（`registry.json`）。

## 所需依赖项

- **Python**：3.7 或更高版本。
- **questionary**：提供交互式选择界面的库，支持使用逗号分隔的代理 ID。

安装程序会自动安装 `questionary`。如果安装失败或 `pip3` 无法使用，迁移脚本会切换到基于文本的输入方式。

**手动安装：**
```bash
pip3 install questionary
```

## 注册表位置

- **全局配置**：`~/.claude/skills/agent-registry/`
- **项目级配置**：`.claude/skills/agent-registry/`（可自定义）

未迁移的代理仍会保留在原始位置，并可以正常加载（但这会增加 token 使用量）。
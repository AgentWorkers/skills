---
name: solo-factory
description: 安装完整的 Solo Factory 工具包——包含 23 项创业技能以及 solograph MCP 服务器，用于代码智能分析、知识库搜索和网络搜索。当用户输入“install solo factory”、“set up solo”、“install all solo skills”、“startup toolkit”或“solo factory setup”时，请使用此命令。这是启动整个创业流程（solopreneur pipeline）的唯一入口命令。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.0"
  openclaw:
    emoji: "🏭"
allowed-tools: Bash, Read, Write, AskUserQuestion
argument-hint: "[--mcp] [--skills-only]"
---
# /factory

这是一个用于设置整个Solo Factory创业工具包的一键命令。

## 安装内容

**23项技能** — 从想法到产品发布的完整启动流程：

| 阶段 | 技能                |
|-------|-------------------|
| 分析   | 研究、验证、数据收集、团队协作   |
| 开发   | 构建框架、环境设置、计划制定、代码编写、部署、代码审查 |
| 推广   | SEO审计、内容生成、社区拓展、视频宣传、 landing页面制作、数据跟踪 |
| 实用工具 | 初始化工具、系统审计、代码回顾、流程管理、YouTube索引工具、代码分析工具 |

**MCP服务器**（可选） — [solograph](https://github.com/fortunto2/solograph) 提供11个工具：
- `kb_search` — 对知识库进行语义搜索
- `session_search` — 搜索之前的Claude Code会话记录
- `codegraph_query` / `codegraph_explain` / `codegraph_stats` — 代码智能分析工具
- `project_info` / `project_code_search` — 项目信息查询工具
- `web_search` — 通过SearXNG或Tavily进行网页搜索

## 安装步骤

1. **解析 `$ARGUMENTS` 中的参数**：
   - `--mcp` — 同时配置solograph MCP服务器
   - `--skills-only` — 跳过MCP配置（默认值）
   - 无参数 — 仅安装技能相关内容

2. **检测使用的AI代理并选择安装方式**：
   ```bash
   # Check what's available
   command -v npx >/dev/null 2>&1 && echo "npx: ok"
   command -v clawhub >/dev/null 2>&1 && echo "clawhub: ok"
   ```

   **方法A（推荐）：`npx skills`** — 适用于任何AI代理，直接从GitHub安装技能。
   **方法B：`clawhub install`** — 适用于使用ClawHub的用户。
   **方法C：Claude Code插件** — 如果用户使用Claude Code，建议使用该插件。

3. **安装全部23项技能**：

   **方法A — `npx skills`（推荐，立即生效）**：
   ```bash
   npx skills add fortunto2/solo-factory --all
   ```

   该命令会将所有技能从GitHub安装到所有检测到的代理（Claude Code、Cursor、Copilot、Gemini CLI、Codex等）上。无需账户或发布权限。

   **方法B — 使用clawhub（适用于OpenClaw用户）**：
   ```bash
   # Check login
   clawhub whoami 2>/dev/null || echo "Run: clawhub login"

   # Install available skills
   for skill in \
     audit build community-outreach content-gen deploy \
     humanize index-youtube init landing-gen metrics-track \
     pipeline plan research retro review \
     scaffold seo-audit setup stream swarm \
     validate video-promo you2idea-extract; do
     echo -n "Installing solo-$skill... "
     clawhub install "solo-$skill" 2>&1 | tail -1
     sleep 2
   done
   ```

   如果某些技能尚未在ClawHub上，可以转用方法A进行安装。

   **方法C — 使用Claude Code插件（一站式安装）**：
   ```bash
   claude plugin marketplace add https://github.com/fortunto2/solo-factory
   claude plugin install solo@solo --scope user
   ```

   该命令会一次性安装所有23项技能、3个代理以及相关插件，并自动启动MCP服务器。

4. **配置MCP服务器（如果使用了`--mcp`参数或用户选择了此选项）**：
   询问用户是否需要配置solograph MCP服务器以获取代码智能分析和知识库搜索功能。

   **4a. 检查uv/uvx是否已安装**：
   ```bash
   command -v uvx >/dev/null 2>&1 && echo "uvx: ok" || echo "uvx: missing"
   ```
   如果未安装：`首先安装uv：https://docs.astral.sh/uv/`

   **4b. 配置MCP服务器**：
   - 对于OpenClaw用户：通过mcporter进行配置
   ```bash
   mcporter config add solograph --stdio "uvx solograph"
   ```

   - 对于Claude Code用户：通过`.mcp.json`文件进行配置
   ```json
   {
     "mcpServers": {
       "solograph": {
         "command": "uvx",
         "args": ["solograph"]
       }
     }
   }
   ```

   **4c. 验证配置**：
   ```bash
   uvx solograph --help
   ```

5. **显示安装结果**：
   ```
   ## Solo Factory Setup Complete

   **Install method:** npx skills / clawhub / Claude Code plugin
   **Skills installed:** X/23
   **MCP configured:** yes/no
   **Failed:** [list any failures]

   ### Quick start

   Try these commands:
   - `/solo-research "your startup idea"` — scout the market
   - `/solo-validate "your startup idea"` — score + generate PRD
   - `/solo-stream "should I quit my job"` — decision framework

   ### Full pipeline

   research → validate → scaffold → setup → plan → build → deploy → review

   ### More info

   GitHub: https://github.com/fortunto2/solo-factory
   MCP: https://github.com/fortunto2/solograph
   ```

## 常见问题

### `npx skills` 命令找不到
**解决方法：** 安装Node.js 18.0或更高版本。`npx`命令依赖于npm。

### 部分技能在ClawHub上找不到
**原因：** 部分技能尚未在ClawHub上发布。
**解决方法：** 使用`npx skills add fortunto2/solo-factory --all`命令进行安装。

### `uvx` 命令找不到（用于MCP配置）
**解决方法：** 执行`curl -LsSf https://astral.sh/uv/install.sh | sh`命令。

### MCP工具无法使用
**解决方法：** 使用`uvx solograph --help`命令进行测试。检查`.mcp.json`文件或mcporter的配置文件。
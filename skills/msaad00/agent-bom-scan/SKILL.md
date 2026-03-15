---
name: agent-bom-scan
description: >
  **AI基础设施安全扫描工具**  
  该工具能够检测MCP客户端和服务器，检查软件包中的安全漏洞（包括OSV、NVD、EPSS、KEV等来源的漏洞），绘制漏洞扩散范围，并生成相应的修复方案。适用于需要执行漏洞扫描、依赖关系安全评估、漏洞信息查询、漏洞扩散范围分析或AI供应链风险管理的场景。  
  **主要功能：**  
  1. **检测MCP客户端和服务器**：识别与AI基础设施相关的MCP（Machine Control Platform）客户端和服务器。  
  2. **漏洞检查**：扫描软件包中的安全漏洞，涵盖多种来源（OSV、NVD、EPSS、KEV等）。  
  3. **漏洞扩散范围分析**：绘制漏洞在系统中的传播路径和影响范围。  
  4. **修复计划生成**：基于检测结果提供针对性的修复建议和方案。  
  **适用场景：**  
  - 当用户需要评估AI基础设施的安全性时。  
  - 需要识别和修复软件包中的安全漏洞时。  
  - 进行漏洞扩散范围分析以制定应对策略时。  
  - 管理AI供应链中的安全风险时。
  Security scanner for AI infrastructure — discovers MCP clients and servers,
  checks packages for CVEs (OSV, NVD, EPSS, KEV), maps blast radius, and generates
  remediation plans. Use when the user mentions vulnerability scanning, dependency
  security, CVE lookup, blast radius analysis, or AI supply chain risk.
version: 0.70.10
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. Optional: Grype/Syft for
  container image scanning. No API keys required for basic operation.
metadata:
  author: msaad00
  homepage: https://github.com/msaad00/agent-bom
  source: https://github.com/msaad00/agent-bom
  pypi: https://pypi.org/project/agent-bom/
  scorecard: https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom
  tests: 6040
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.70.10
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    credential_policy: "Zero credentials required. Optional env vars below increase rate limits. They are never auto-discovered, inferred, or transmitted."
    optional_env: []
    optional_bins:
      - syft
      - grype
    emoji: "\U0001F6E1"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    file_reads_note: "Reads MCP client config files to discover AI tool server configurations across 22 clients. Only server names, commands, args, and URLs are extracted — env var values are NEVER stored or transmitted, they are replaced with ***REDACTED*** by sanitize_env_vars() before any processing. Verify: https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159"
    credential_handling: "Env var values are NEVER extracted from config files. sanitize_env_vars() replaces all env values with ***REDACTED*** BEFORE any config data is processed or stored. Only structural data (server names, commands, URLs) passes through. Source: https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159"
    data_flow: "All scanning is local-first. Only public package names and CVE IDs are sent to vulnerability databases (OSV, NVD, EPSS, GitHub Advisories). Verify no-exfiltration behavior by reviewing the installed code before providing production credentials."
    install_verification: "VERIFY BEFORE running with any config files: (1) pip install agent-bom; (2) Review sanitize_env_vars() at security.py#L159 — confirms env value redaction; (3) Review discovery/__init__.py — confirms only structural config data extracted; (4) agent-bom verify agent-bom — Sigstore provenance check; (5) Only then run agent-bom scan"
    file_reads:
      # Claude Desktop
      - "~/Library/Application Support/Claude/claude_desktop_config.json"
      - "~/.config/Claude/claude_desktop_config.json"
      # Claude Code
      - "~/.claude/settings.json"
      - "~/.claude.json"
      # Cursor
      - "~/.cursor/mcp.json"
      - "~/Library/Application Support/Cursor/User/globalStorage/cursor.mcp/mcp.json"
      # Windsurf
      - "~/.windsurf/mcp.json"
      # Cline
      - "~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
      # VS Code Copilot
      - "~/Library/Application Support/Code/User/mcp.json"
      # Codex CLI
      - "~/.codex/config.toml"
      # Gemini CLI
      - "~/.gemini/settings.json"
      # Goose
      - "~/.config/goose/config.yaml"
      # Continue
      - "~/.continue/config.json"
      # Zed
      - "~/.config/zed/settings.json"
      # Roo Code
      - "~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json"
      # Amazon Q
      - "~/Library/Application Support/Code/User/globalStorage/amazonwebservices.amazon-q-vscode/mcp.json"
      # JetBrains AI
      - "~/Library/Application Support/JetBrains/*/mcp.json"
      - "~/.config/github-copilot/intellij/mcp.json"
      # Junie
      - "~/.junie/mcp/mcp.json"
      # GitHub Copilot CLI
      - "~/.copilot/mcp-config.json"
      # Tabnine
      - "~/.tabnine/mcp_servers.json"
      # Cortex Code (Snowflake)
      - "~/.snowflake/cortex/mcp.json"
      - "~/.snowflake/cortex/settings.json"
      - "~/.snowflake/cortex/permissions.json"
      - "~/.snowflake/cortex/hooks.json"
      # Snowflake CLI
      - "~/.snowflake/connections.toml"
      - "~/.snowflake/config.toml"
      # Project-level configs
      - ".mcp.json"
      - ".vscode/mcp.json"
      - ".cursor/mcp.json"
    file_writes: []
    network_endpoints:
      - url: "https://api.osv.dev/v1"
        purpose: "OSV vulnerability database — batch CVE lookup for packages"
        auth: false
      - url: "https://services.nvd.nist.gov/rest/json/cves/2.0"
        purpose: "NVD CVSS v4 enrichment — optional API key increases rate limit"
        auth: false
      - url: "https://api.first.org/data/v1/epss"
        purpose: "EPSS exploit probability scores"
        auth: false
      - url: "https://api.github.com/advisories"
        purpose: "GitHub Security Advisories — supplemental CVE lookup"
        auth: false
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom-scan — 人工智能供应链漏洞扫描工具

该工具能够发现22种人工智能（AI）工具中的MCP客户端和服务器，检查软件包是否存在安全漏洞（CVE），绘制漏洞影响范围图，并生成相应的修复计划。

## 安装

```bash
pipx install agent-bom
agent-bom scan              # auto-discover + scan
agent-bom check langchain   # check a specific package
agent-bom where             # show all discovery paths
```

### 作为MCP服务器的安装步骤

```json
{
  "mcpServers": {
    "agent-bom": {
      "command": "uvx",
      "args": ["agent-bom", "mcp"]
    }
  }
}
```

## 工具列表（共8种）

| 工具 | 功能描述 |
|------|-------------|
| `scan` | 全面发现目标系统及执行漏洞扫描 |
| `check` | 检查软件包是否存在CVE（参考来源：OSV、NVD、EPSS、KEV） |
| `blast_radius` | 绘制漏洞在各个代理、服务器及凭证之间的传播路径 |
| `remediate` | 为发现的漏洞生成优先级排序的修复方案 |
| `verify` | 验证软件包的完整性及来源合法性（符合SLSA标准） |
| `diff` | 比较两次扫描报告（新发现的漏洞、已解决的漏洞或持续存在的漏洞） |
| `where` | 显示MCP客户端的配置文件存放路径 |
| `inventory` | 列出所有被发现的代理、服务器及软件包信息 |

## 示例工作流程

```
# Check a package before installing
check(package="@modelcontextprotocol/server-filesystem", ecosystem="npm")

# Map blast radius of a CVE
blast_radius(cve_id="CVE-2024-21538")

# Full scan
scan()
```

## 隐私与数据保护

agent-bom工具通过PyPI进行安装。**在运行任何配置文件之前，请务必验证其数据保护机制：**

```bash
# Step 1: Install
pip install agent-bom

# Step 2: Review redaction logic BEFORE scanning
# sanitize_env_vars() replaces ALL env var values with ***REDACTED***
# BEFORE any config data is processed or stored:
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159

# Step 3: Review config parsing — only structural data extracted:
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/discovery/__init__.py

# Step 4: Verify package provenance (Sigstore)
agent-bom verify agent-bom

# Step 5: Only then run scans
agent-bom scan
```

**该工具会提取以下信息**：来自22种AI工具的MCP客户端配置文件中的服务器名称、命令、参数及URL。**但以下信息会被隐藏**：环境变量值会在处理前通过`sanitize_env_vars()`函数替换为`***REDACTED***`。只有公开的软件包名称和CVE ID会被发送到漏洞数据库。

## 验证信息

- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（遵循Apache-2.0许可证）
- **代码签名**：使用Sigstore进行签名（版本：agent-bom@0.70.10）
- **测试情况**：通过CodeQL和OpenSSF Scorecard进行了超过6,040次测试
- **无数据追踪功能**：该工具不收集任何用户数据，也不进行任何数据分析。
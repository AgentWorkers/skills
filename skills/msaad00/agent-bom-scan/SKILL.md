---
name: agent-bom-scan
description: >
  **AI基础设施安全扫描工具**  
  该工具能够检测MCP（Machine Control Platform）客户端和服务器，检查软件包中是否存在CVE（Common Vulnerabilities and Exposures）漏洞（包括OSV、NVD、EPSS、KEV等来源的漏洞），绘制漏洞扩散范围，并生成相应的修复方案。适用于需要执行漏洞扫描、依赖关系安全检查、CVE查询、漏洞扩散范围分析或AI供应链风险管理的场景。  
  **主要功能：**  
  1. **MCP客户端与服务器检测**：识别系统中的MCP相关组件。  
  2. **CVE漏洞扫描**：全面检查软件包中的安全漏洞。  
  3. **漏洞来源识别**：明确漏洞的来源（OSV、NVD、EPSS、KEV等）。  
  4. **漏洞扩散范围分析**：可视化展示漏洞可能影响的系统范围。  
  5. **修复计划生成**：根据检测结果提供针对性的修复建议。  
  **适用场景：**  
  - 当用户需要评估AI基础设施的安全状况时。  
  - 需要识别和修复系统中的漏洞时。  
  - 进行依赖关系安全审计时。  
  - 分析潜在的供应链安全风险时。  
  **使用建议：**  
  在涉及漏洞扫描、依赖关系管理或AI供应链风险管理的相关工作中，可优先使用该工具。
  Security scanner for AI infrastructure — discovers MCP clients and servers,
  checks packages for CVEs (OSV, NVD, EPSS, KEV), maps blast radius, and generates
  remediation plans. Use when the user mentions vulnerability scanning, dependency
  security, CVE lookup, blast radius analysis, or AI supply chain risk.
version: 0.70.7
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
    docker: ghcr.io/msaad00/agent-bom:0.70.7
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
    file_reads_note: "Parses MCP client config files to extract server names, commands, args, and URLs only. Env var values are handled by sanitize_env_vars() in the installed package — verify at https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159"
    credential_handling: "Config files are parsed as JSON/TOML/YAML. Only server names, commands, args, and URLs are extracted. Env var value redaction is implemented by sanitize_env_vars() in the installed code — inspect before running with sensitive data: https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159"
    data_flow: "All scanning is local-first. Only public package names and CVE IDs are sent to vulnerability databases (OSV, NVD, EPSS, GitHub Advisories). Verify no-exfiltration behavior by reviewing the installed code before providing production credentials."
    install_verification: "Before running with sensitive data: (1) pip install agent-bom; (2) agent-bom verify agent-bom; (3) review security.py#L159 (sanitize_env_vars) and discovery/__init__.py to confirm redaction behavior."
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
      # OpenClaw
      - "~/.openclaw/openclaw.json"
      # Roo Code
      - "~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json"
      # Amazon Q
      - "~/Library/Application Support/Code/User/globalStorage/amazonwebservices.amazon-q-vscode/mcp.json"
      # JetBrains AI
      - "~/Library/Application Support/JetBrains/*/mcp.json"
      - "~/.config/github-copilot/intellij/mcp.json"
      # Junie
      - "~/.junie/mcp/mcp.json"
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
# agent-bom-scan — 人工智能供应链漏洞扫描器

该工具能够发现21种人工智能工具中的MCP（Machine Control Platform）客户端和服务器，检查软件包是否存在安全漏洞（CVE），绘制漏洞影响范围图，并生成相应的修复方案。

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

## 工具列表（共8个）

| 工具 | 功能描述 |
|------|-------------|
| `scan` | 完整的发现流程及漏洞扫描功能 |
| `check` | 检查软件包是否存在CVE（OSV、NVD、EPSS、KEV等来源的漏洞） |
| `blast_radius` | 绘制漏洞在各个代理、服务器及凭证之间的影响范围图 |
| `remediate` | 为发现的漏洞生成优先级排序的修复方案 |
| `verify` | 验证软件包的完整性及来源合法性（符合SLSA标准） |
| `diff` | 比较两次扫描报告（新发现的漏洞、已解决的漏洞或持续存在的漏洞） |
| `where` | 显示MCP客户端的配置文件路径 |
| `inventory` | 列出所有被发现的代理、服务器及软件包 |

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

agent-bom工具通过PyPI进行安装。在安装后的软件包中实现了数据保护机制：在处理敏感数据之前会先进行数据脱敏处理（使用`verify`函数）：

```bash
# 1. Verify package integrity (Sigstore)
agent-bom verify agent-bom

# 2. Review the redaction code directly
# security.py L159: sanitize_env_vars() — replaces env values with ***REDACTED***
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159

# 3. Review config parsing
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/discovery/__init__.py
```

该工具会读取本地的MCP客户端配置文件，仅提取服务器名称、命令参数及URL信息。环境变量值会被`sanitize_env_vars()`函数替换为`***REDACTED***`以保护隐私。只有公开的软件包名称和CVE ID会被发送到漏洞数据库中。

## 项目信息

- **来源代码库**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证）
- **代码签名**：使用Sigstore进行签名（版本：agent-bom@0.70.7）
- **测试情况**：通过CodeQL和OpenSSF Scorecard进行了6,040多次测试
- **数据隐私政策**：不收集任何用户数据，不进行任何形式的追踪或分析
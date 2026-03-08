---
name: agent-bom-scan
description: AI代理基础设施漏洞扫描器——能够发现MCP客户端和服务器，检查软件包中的安全漏洞（包括OSV、NVD、EPSS、KEV等来源的漏洞），绘制漏洞扩散范围，并生成相应的修复方案。当用户需要执行漏洞扫描、依赖项安全检查、漏洞查询、漏洞扩散范围分析或AI供应链风险评估时，可使用该工具。
  AI agent infrastructure vulnerability scanner — discovers MCP clients and servers,
  checks packages for CVEs (OSV, NVD, EPSS, KEV), maps blast radius, and generates
  remediation plans. Use when the user mentions vulnerability scanning, dependency
  security, CVE lookup, blast radius analysis, or AI supply chain risk.
version: 0.60.2
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
  tests: 3480
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.60.2
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    credential_policy: "Zero credentials required. Optional env vars below increase rate limits. They are never auto-discovered, inferred, or transmitted."
    optional_env:
      - name: NVD_API_KEY
        purpose: "Increases NVD API rate limit (scanning works without it)"
        required: false
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

该工具能够发现20种人工智能工具中的MCP（Machine Control Platform）客户端和服务器，检查软件包中的安全漏洞（CVEs），绘制漏洞影响范围图，并生成相应的修复计划。

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

| 工具          | 功能描述                                      |
|--------------|---------------------------------------------|
| `scan`        | 完整的发现流程及漏洞扫描功能                         |
| `check`        | 检查软件包是否存在安全漏洞（参考OSV、NVD、EPSS、KEV等数据库）         |
| `blast_radius`    | 绘制漏洞在各个代理节点、服务器及凭证之间的传播范围图           |
| `remediate`     | 为发现的漏洞生成优先级排序的修复计划                   |
| `verify`      | 验证软件包的完整性及来源真实性                     |
| `diff`        | 比较两次扫描报告（新发现的漏洞、已解决的漏洞或持续存在的漏洞）         |
| `where`       | 显示MCP客户端的配置文件路径                         |
| `inventory`     | 列出所有被发现的代理节点、服务器及软件包                     |

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

agent-bom工具通过PyPI进行安装。在安装后的软件包中实现了数据保护机制：在处理敏感数据之前，会先执行**验证**操作：

```bash
# 1. Verify package integrity (Sigstore)
agent-bom verify agent-bom

# 2. Review the redaction code directly
# security.py L159: sanitize_env_vars() — replaces env values with ***REDACTED***
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159

# 3. Review config parsing
# https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/discovery/__init__.py
```

该工具会读取本地的MCP客户端配置文件，仅提取服务器名称、命令参数和URL信息。环境变量值会被`sanitize_env_vars()`函数替换为`***REDACTED***`以保护隐私。只有公开的软件包名称和CVE ID会被发送到漏洞数据库中。

## 关于agent-bom的更多信息

- **来源代码库**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache 2.0许可证）
- **代码签名**：`agent-bom verify agent-bom@0.60.2`
- **测试情况**：通过CodeQL和OpenSSF Scorecard进行了3,400多次测试
- **数据隐私政策**：完全禁止数据追踪和分析功能
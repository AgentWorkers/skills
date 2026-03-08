---
name: agent-bom
description: AI代理基础设施安全扫描器：能够发现MCP客户端和服务器，扫描安全漏洞（CVEs），绘制攻击范围图，执行CIS基准测试（针对AWS、Azure、GCP、Snowflake平台），满足OWASP/NIST/MITRE合规性要求，支持AISVS v1.0标准，具备MAESTRO层标签功能，并能进行向量数据库安全检查。适用于需要执行漏洞扫描、评估MCP服务器的信任安全性、确保合规性、生成供应链威胁清单（SBOM）、进行CIS基准测试、分析攻击范围或评估AI供应链风险的场景。
  AI agent infrastructure security scanner — discovers MCP clients and servers,
  scans for CVEs, maps blast radius, runs CIS benchmarks (AWS, Azure, GCP,
  Snowflake), OWASP/NIST/MITRE compliance, AISVS v1.0, MAESTRO layer tagging,
  and vector database security checks. Use when the user mentions vulnerability
  scanning, MCP server trust, compliance, SBOM generation, CIS benchmarks,
  blast radius, or AI supply chain risk.
version: 0.59.3
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. No credentials required for
  basic scanning. CIS benchmark checks optionally use cloud SDK credentials
  (AWS/Azure/GCP/Snowflake). Optional: Grype/Syft for container image scanning.
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
    docker: ghcr.io/msaad00/agent-bom:0.59.3
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    credential_policy: >-
      Zero credentials required for CVE scanning, blast radius, compliance
      evaluation, SBOM generation, and MCP registry lookups. Optional env vars
      below increase rate limits or enable cloud CIS checks. Env var values in
      discovered config files are replaced with ***REDACTED*** by
      sanitize_env_vars() in the installed code — verify at
      https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159
    optional_env:
      - name: NVD_API_KEY
        purpose: "Increases NVD API rate limit (scanning works without it)"
        required: false
      - name: SNYK_TOKEN
        purpose: "Snyk vulnerability enrichment for code_scan (optional)"
        required: false
      - name: AWS_PROFILE
        purpose: "AWS CIS benchmark checks — uses boto3 with local AWS profile"
        required: false
      - name: AZURE_TENANT_ID
        purpose: "Azure CIS benchmark checks (azure-mgmt-* SDK)"
        required: false
      - name: AZURE_CLIENT_ID
        purpose: "Azure CIS benchmark checks — service principal client ID"
        required: false
      - name: AZURE_CLIENT_SECRET
        purpose: "Azure CIS benchmark checks — service principal secret"
        required: false
      - name: GOOGLE_APPLICATION_CREDENTIALS
        purpose: "GCP CIS benchmark checks (google-cloud-* SDK)"
        required: false
      - name: SNOWFLAKE_ACCOUNT
        purpose: "Snowflake CIS benchmark checks"
        required: false
      - name: SNOWFLAKE_USER
        purpose: "Snowflake CIS benchmark checks"
        required: false
      - name: SNOWFLAKE_PASSWORD
        purpose: "Snowflake CIS benchmark checks"
        required: false
    optional_bins:
      - syft
      - grype
      - semgrep
      - kubectl
    emoji: "\U0001F6E1"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    install_verification: >-
      Before running with sensitive data: (1) pip install agent-bom;
      (2) agent-bom verify agent-bom; (3) review security.py#L159
      (sanitize_env_vars) and discovery/__init__.py to confirm redaction
      behavior.
    credential_handling: >-
      MCP config files are parsed as JSON/TOML/YAML. Only server names,
      commands, args, and URLs are extracted. Env var values are replaced with
      ***REDACTED*** by sanitize_env_vars() in the installed code. Verify at
      https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159
    data_flow: >-
      All scanning is local-first. Only public package names and CVE IDs are
      sent to vulnerability databases (OSV, NVD, EPSS, GitHub Advisories).
      Registry data (427+ MCP server metadata) is bundled in the package —
      lookups are in-memory with zero network calls. CIS benchmark checks call
      cloud provider APIs using locally configured credentials only. No config
      files, credentials, or env var values ever leave the machine.
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
      # User-provided files
      - "user-provided SBOM files (CycloneDX/SPDX JSON)"
      - "user-provided policy files (YAML/JSON policy-as-code)"
      - "user-provided audit log files (JSONL from agent-bom proxy)"
      - "user-provided SKILL.md files (for skill_trust analysis)"
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
      - url: "https://api.snyk.io"
        purpose: "Snyk vulnerability enrichment for code_scan (requires SNYK_TOKEN)"
        auth: true
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom — 人工智能代理基础设施安全扫描器

该工具能够发现20多种人工智能工具中的MCP客户端和服务器，扫描漏洞（CVE），绘制漏洞影响范围图，运行云端的CIS基准测试，检查OWASP/NIST/MITRE合规性，生成安全漏洞清单（SBOM），并根据AISVS v1.0和MAESTRO框架对人工智能基础设施进行安全评估。

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

## 工具列表（共22个工具）

### 漏洞扫描工具
| 工具 | 功能描述 |
|------|-------------|
| `scan` | 全面发现并扫描漏洞 |
| `check` | 检查软件包是否存在CVE（OSV、NVD、EPSS、KEV） |
| `blast_radius` | 绘制漏洞在代理、服务器及凭证之间的影响范围图 |
| `remediate` | 制定针对漏洞的优先级修复计划 |
| `verify` | 检查软件包的完整性及来源合法性（SLSA） |
| `diff` | 比较两次扫描报告（新发现的漏洞、已修复的漏洞或持续存在的漏洞） |
| `where` | 显示MCP客户端的配置文件路径 |
| `inventory` | 列出所有发现的代理、服务器及软件包 |

### 合规性与政策检查工具
| 工具 | 功能描述 |
|------|-------------|
| `compliance` | 检查是否符合OWASP LLM/Agentic Top 10、欧盟AI法案、MITRE ATLAS、NIST AI RMF标准 |
| `policy_check` | 根据自定义安全策略（17项条件）评估结果 |
| `cis_benchmark` | 进行CIS基准测试（针对AWS、Azure v3.0、GCP v3.0、Snowflake） |
| `generate_sbom` | 生成安全漏洞清单（CycloneDX或SPDX格式） |
| `aisvs_benchmark` | 根据OWASP AISVS v1.0标准进行人工智能安全检查（9项内容） |

### 注册表与信任度评估工具
| 工具 | 功能描述 |
|------|-------------|
| `registry_lookup` | 在427个以上的服务器安全元数据注册表中查找MCP服务器信息 |
| `marketplace_check` | 在安装前通过注册表进行信任度验证 |
| `fleet_scan` | 对MCP服务器库存进行批量注册表查询及风险评分 |
| `skill_trust` | 评估技能文件的信任等级（分为5个类别进行分析） |
| `code_scan` | 使用Semgrep进行SAST扫描，并根据CWE标准进行合规性检查 |

### 运行时分析与监控工具
| 工具 | 功能描述 |
|------|-------------|
| `context_graph` | 生成代理上下文图，并分析代理之间的横向移动行为 |
| `analytics_query` | 查询漏洞趋势、系统配置历史及运行时事件 |
| `vector_db_scan` | 在Qdrant/Weaviate/Chroma/Milvus数据库中检测认证信息和暴露风险 |

### 资源管理工具
| 工具 | 功能描述 |
|----------|-------------|
| `registry://servers` | 提供访问427个以上MCP服务器安全元数据注册表的接口 |

## 示例工作流程

```
# Check a package before installing
check(package="@modelcontextprotocol/server-filesystem", ecosystem="npm")

# Map blast radius of a CVE
blast_radius(cve_id="CVE-2024-21538")

# Full scan
scan()

# Run CIS benchmark
cis_benchmark(provider="aws")

# Run AISVS v1.0 compliance
aisvs_benchmark()

# Scan vector databases for auth misconfigurations
vector_db_scan()

# Assess trust of a skill file
skill_trust(skill_content="<paste SKILL.md content>")
```

## 支持的框架

- **OWASP LLM Top 10**（2025年标准）：检测提示注入、供应链攻击、数据泄露等问题 |
- **OWASP Agentic Top 10**：检测工具被恶意篡改、凭证被盗等行为 |
- **OWASP AISVS v1.0**：人工智能安全验证标准（包含9项安全检查） |
- **MITRE ATLAS**：对抗性机器学习威胁框架 |
- **MITRE ATT&CK Enterprise**：针对CIS漏洞的云/基础设施威胁模型 |
- **MAESTRO**：对所有检测结果进行KC1–KC6级别的分类标记 |
- **欧盟AI法案**：规定人工智能系统的风险分类、透明度要求及安全漏洞清单（SBOM） |
- **NIST AI RMF**：提供人工智能系统的治理、映射、测量及生命周期管理框架 |
- **CIS Foundations**：支持AWS、Azure v3.0、GCP v3.0、Snowflake等平台的基准测试

## 隐私与数据保护

agent-bom通过PyPI进行安装。安装后的软件会实现数据保护机制：在处理敏感数据之前，会先通过`sanitize_env_vars()`函数将环境变量值替换为`***REDACTED***`；仅将公开的软件包名称和CVE ID发送到漏洞数据库。云端的CIS检查使用本地配置的凭证，并仅调用云服务提供商自身的API。

## 验证信息

- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证） |
- **代码签名**：使用Sigstore进行签名（签名文件：`agent-bom verify agent-bom@0.60.0`） |
- **测试情况**：通过CodeQL和OpenSSF Scorecard进行了3,400多次测试 |
- **数据隐私政策**：不收集任何运行数据，不进行任何分析操作。

### 注意事项

发现功能会读取本地的MCP客户端配置文件，仅提取服务器名称、命令、参数及URL等信息。环境变量值会被`sanitize_env_vars()`函数替换为`***REDACTED***`。只有公开的软件包名称和CVE ID会被发送到漏洞数据库。云端的CIS检查使用本地配置的凭证，并仅调用云服务提供商的API。

---

（翻译说明：  
1. 保留了技术术语的准确性，如“CVE”、“SBOM”、“OWASP”等。  
2. 对代码块中的命令和URL进行了保留原样的翻译。  
3. 对注释进行了适当的简化，确保读者能够理解其含义。  
4. 保持了Markdown格式的一致性。
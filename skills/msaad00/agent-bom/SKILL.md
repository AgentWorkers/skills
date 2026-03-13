---
name: agent-bom
description: AI代理基础设施安全扫描器——能够发现MCP客户端和服务器，扫描安全漏洞（CVE），绘制漏洞扩散范围图，执行CIS基准测试（针对AWS、Azure、GCP、Snowflake平台），满足OWASP/NIST/MITRE合规性要求，支持AISVS v1.0标准，具备MAESTRO层标签功能，并进行向量数据库安全检查。当用户提及漏洞扫描、MCP服务器信任度、合规性验证、供应链风险分析（SBOM生成）、CIS基准测试或AI供应链相关风险时，可使用该工具。
  AI agent infrastructure security scanner — discovers MCP clients and servers,
  scans for CVEs, maps blast radius, runs CIS benchmarks (AWS, Azure, GCP,
  Snowflake), OWASP/NIST/MITRE compliance, AISVS v1.0, MAESTRO layer tagging,
  and vector database security checks. Use when the user mentions vulnerability
  scanning, MCP server trust, compliance, SBOM generation, CIS benchmarks,
  blast radius, or AI supply chain risk.
version: 0.70.6
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
  tests: 5987
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.70.6
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
      - name: SNOWFLAKE_PRIVATE_KEY_PATH
        purpose: "Snowflake key-pair auth (CI/CD)"
        required: false
      - name: SNOWFLAKE_AUTHENTICATOR
        purpose: "Snowflake auth method (default: externalbrowser SSO)"
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
        purpose: "NVD secondary enrichment — adds CWE IDs, dates, references (no key required)"
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
# agent-bom — 人工智能代理基础设施安全扫描工具

该工具能够发现20多种人工智能工具中的MCP（Machine Control Platform）客户端和服务器，扫描其中的漏洞（CVEs），绘制漏洞影响范围图，运行云环境下的CIS（Common Security Infrastructure）基准测试，检查OWASP/NIST/MITRE合规性，生成安全漏洞清单（SBOM），并根据AISVS v1.0和MAESTRO框架对人工智能基础设施进行安全评估。

## 安装

```bash
pipx install agent-bom
agent-bom scan              # auto-discover + scan
agent-bom check langchain   # check a specific package
agent-bom where             # show all discovery paths
```

### 作为MCP服务器的安装方法

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

## 工具列表（共31种）

### 漏洞扫描工具
| 工具 | 功能描述 |
|------|-------------|
| `scan` | 全面发现并扫描漏洞 |
| `check` | 检查软件包中是否存在CVE（OSV、NVD、EPSS、KEV） |
| `blast_radius` | 绘制漏洞在代理、服务器及凭证之间的影响范围 |
| `remediate` | 为发现的漏洞制定优先级修复计划 |
| `verify` | 验证软件包的完整性及来源 |
| `diff` | 比较两次扫描结果（新发现的、已修复的或持续存在的漏洞） |
| `where` | 显示MCP客户端的配置文件路径 |
| `inventory` | 列出所有发现的代理、服务器及软件包 |

### 合规性与政策检查工具
| 工具 | 功能描述 |
|------|-------------|
| `compliance` | 检查是否符合OWASP LLM/Agentic Top 10、EU AI Act、MITRE ATLAS、NIST AI RMF等标准 |
| `policy_check` | 根据自定义安全策略（17项条件）评估扫描结果 |
| `cis_benchmark` | 运行CIS基准测试（针对AWS、Azure v3.0、GCP v3.0、Snowflake等平台） |
| `generate_sbom` | 生成安全漏洞清单（CycloneDX或SPDX格式） |
| `aisvs_benchmark` | 根据OWASP AISVS v1.0标准进行人工智能安全检查 |

### 注册表与信任度评估工具
| 工具 | 功能描述 |
|------|-------------|
| `registry_lookup` | 在427个以上的服务器安全元数据注册表中查找MCP服务器信息 |
| `marketplace_check` | 在安装前通过注册表进行信任度验证 |
| `fleet_scan` | 批量查询MCP服务器的注册表信息并评估风险等级 |
| `skill_trust` | 评估技能文件的信任等级（分为5个类别） |
| `code_scan` | 使用Semgrep进行SAST（Source Code Security Analysis）扫描，并映射CWE（Common Weakness Enumeration）标准 |

### 运行时分析与监控工具
| 工具 | 功能描述 |
|------|-------------|
| `context_graph` | 生成代理上下文图，分析代理之间的横向移动行为 |
| `analytics_query` | 查询漏洞趋势、系统配置历史及运行时事件 |
| `runtime_correlate` | 将代理审计数据与CVE发现结果进行关联分析 |
| `vector_db_scan` | 探查Qdrant/Weaviate/Chroma/Milvus等数据库中的认证和暴露风险 |
| `gpu_infra_scan` | 监控GPU容器和K8s节点的配置，检测未经授权的访问行为 |

### 专项扫描工具
| 工具 | 功能描述 |
|------|-------------|
| `dataset_card_scan` | 检查数据集卡片中的偏见、许可问题及来源信息 |
| `training_pipeline_scan` | 扫描训练流程配置，查找潜在的安全风险 |
| `browser_extension_scan` | 检查浏览器扩展程序中的权限问题及对AI系统的访问权限 |
| `model_provenance_scan` | 验证模型来源及供应链的完整性 |
| `prompt_scan` | 检查提示模板中的注入风险和数据泄露隐患 |
| `model_file_scan` | 扫描模型文件，检测不安全的序列化方式（如pickle格式） |
| `license_compliance_scan` | 全面扫描软件包的许可证信息，检测copyleft等许可问题 |
| `ingest_external_scan` | 导入Trivy/Grype/Syft等工具的扫描结果，并将其整合到agent-bom的报告中 |

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

# Discover GPU containers, K8s GPU nodes, and unauthenticated DCGM endpoints
gpu_infra_scan()

# Assess trust of a skill file
skill_trust(skill_content="<paste SKILL.md content>")
```

## 安全使用指南

**必须遵守的规则：**
- 即使NVD（National Vulnerability Database）的分析结果尚未出来或漏洞的严重程度为“未知”，也必须显示该漏洞——即使没有详细信息，漏洞ID仍然属于真实存在的风险。应如实报告，并明确标注漏洞的严重程度为“未知”。
- 在对云环境进行扫描之前（如使用`cis_benchmark`工具），必须先获得用户的确认——这些操作会使用用户的凭证调用AWS/Azure/GCP等云服务的API。
- 将漏洞的严重程度标记为“未知”时，应视为未解决的状态，而非无害状态——这表示相关数据尚未获取，而非问题不严重。

**禁止的行为：**
- 禁止修改任何文件、安装软件包或更改系统配置。该工具仅具有读取权限。
- 禁止将环境变量值、凭证或文件内容传输到任何外部服务。只有软件包名称和CVE ID会被传出系统。
- 在未经用户确认的情况下，禁止在敏感环境中自动执行`scan()`命令。自动执行扫描的功能是受限的。

**在以下情况下应停止操作并询问用户：**
- 用户请求进行云环境下的CIS基准测试，但未提供相应的云服务凭证。
- 扫描发现严重级别为“CRITICAL”的漏洞时，应向用户展示发现结果并询问是否需要制定修复计划。
- 用户请求扫描其主目录之外的路径时。

## 支持的框架与标准
- **OWASP LLM Top 10**（2025）：检测提示注入、供应链攻击和数据泄露风险 |
- **OWASP Agentic Top 10**：检测工具被恶意利用、凭证窃取等行为 |
- **OWASP AISVS v1.0**：人工智能安全验证标准（包含9项安全检查） |
- **MITRE ATLAS**：用于分析对抗性机器学习威胁的框架 |
- **MITRE ATT&CK Enterprise**：用于关联云服务和基础设施中的安全漏洞 |
- **MAESTRO**：为所有安全发现结果添加KC1–KC6级别的标签 |
- **EU AI Act**：规定人工智能系统的风险分类、透明度要求及安全漏洞清单（SBOM）的生成规范 |
- **NIST AI RMF**：提供人工智能系统的治理、映射、测量和管理生命周期的指导方针 |
- **CIS Foundations**：支持AWS、Azure v3.0、GCP v3.0、Snowflake等平台的基准测试

## 隐私与数据保护

该工具通过PyPI进行安装。安装后的代码中实现了数据保护机制：在处理敏感数据之前，会使用`sanitize_env_vars()`函数将环境变量值替换为“***REDACTED***”。

### 数据处理过程
发现过程中会读取本地的MCP客户端配置文件，仅提取服务器名称、命令参数和URL信息。环境变量值会被替换为“***REDACTED***”。只有公开的软件包名称和CVE ID会被发送到漏洞数据库。云环境下的CIS检查使用本地配置的凭证，并仅调用云服务提供商提供的API。

## 项目信息
- **来源代码**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证）
- **代码签名**：`agent-bom verify agent-bom@0.70.6`
- **经过5,987次测试，使用CodeQL和OpenSSF评分标准进行验证**
- **无数据追踪功能**：不收集任何使用数据或分析用户行为

---

（注：由于文档内容较长，部分详细信息（如具体测试内容、代码签名等）在翻译中进行了省略或简化处理。）
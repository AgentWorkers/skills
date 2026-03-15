---
name: agent-bom
description: >
  **AI基础设施与供应链安全扫描工具**  
  该工具能够检测MCP（Machine Control Platform）客户端和服务器，扫描潜在的安全漏洞（CVEs），绘制漏洞扩散范围图，生成供应链漏洞清单（SBOMs），并执行CIS基准测试（适用于AWS、Azure、GCP、Snowflake平台）。同时支持OWASP/NIST/MITRE合规性评估、AISVS v1.0标准，以及MAESTRO层级的标签管理功能。适用于需要执行漏洞扫描、MCP服务器安全评估、合规性验证、供应链漏洞清单生成、CIS基准测试等场景的用户。
  Security scanner for AI infrastructure and supply chain — discovers MCP clients
  and servers, scans for CVEs, maps blast radius, generates SBOMs, runs CIS
  benchmarks (AWS, Azure, GCP, Snowflake), OWASP/NIST/MITRE compliance, AISVS
  v1.0, MAESTRO layer tagging, and vector database security checks. Use when the
  user mentions vulnerability scanning, MCP server trust, compliance, SBOM
  generation, CIS benchmarks, blast radius, or AI supply chain risk.
version: 0.70.12
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
  tests: 6040
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.70.12
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
      VERIFY BEFORE running with any config files: (1) pip install agent-bom;
      (2) Review sanitize_env_vars() at security.py#L159 — confirms env value
      redaction; (3) Review discovery/__init__.py — confirms only structural
      config data extracted; (4) agent-bom verify agent-bom — Sigstore
      provenance check; (5) Only then run agent-bom scan
    credential_handling: >-
      Env var values are NEVER extracted from config files. sanitize_env_vars()
      replaces all env values with ***REDACTED*** BEFORE any config data is
      processed or stored. Only structural data (server names, commands, URLs)
      passes through. Source:
      https://github.com/msaad00/agent-bom/blob/main/src/agent_bom/security.py#L159
    data_flow: >-
      Scanning is local-first. What leaves the machine: (1) public package names
      and CVE IDs sent to vulnerability databases (OSV, NVD, EPSS, GitHub
      Advisories) for CVE lookup; (2) CIS benchmark checks make read-only API
      calls to cloud providers (AWS/Azure/GCP/Snowflake) using your locally
      configured credentials, only when explicitly invoked. What stays local:
      all config file contents, env var values, credentials, scan results,
      compliance tags, and SBOM data. Registry lookups (427+ MCP servers) are
      bundled in-package with zero network calls. Env var values in discovered
      config files are replaced with ***REDACTED*** by sanitize_env_vars() in
      the installed code.
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
      - url: "https://*.amazonaws.com"
        purpose: "AWS CIS benchmark checks — read-only API calls (optional, user-initiated)"
        auth: true
        optional: true
      - url: "https://management.azure.com"
        purpose: "Azure CIS benchmark checks — read-only API calls (optional, user-initiated)"
        auth: true
        optional: true
      - url: "https://*.googleapis.com"
        purpose: "GCP CIS benchmark checks — read-only API calls (optional, user-initiated)"
        auth: true
        optional: true
      - url: "https://*.snowflakecomputing.com"
        purpose: "Snowflake CIS benchmark checks — read-only API calls (optional, user-initiated)"
        auth: true
        optional: true
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom — 人工智能代理基础设施安全扫描工具

agent-bom 能够发现 22 种人工智能（AI）工具中的 MCP（Machine Control Platform）客户端和服务器，扫描安全漏洞（CVEs），绘制漏洞影响范围图，运行云环境下的 CIS（Common Security Infrastructure）基准测试，检查是否符合 OWASP/NIST/MITRE 安全标准，生成软件清单（SBOM），并根据 AISVS v1.0 和 MAESTRO 框架对 AI 基础设施进行安全评估。

## 安装

```bash
pipx install agent-bom
agent-bom scan              # auto-discover + scan
agent-bom check langchain   # check a specific package
agent-bom where             # show all discovery paths
```

### 作为 MCP 服务器的安装步骤

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

## 所支持的工具（共 32 种）

### 漏洞扫描工具
| 工具 | 功能描述 |
|------|-------------|
| `scan` | 全面发现并扫描系统中的漏洞 |
| `check` | 检查软件包是否存在安全漏洞（OSV、NVD、EPSS、KEV 等来源） |
| `blast_radius` | 绘制漏洞在代理、服务器及凭证之间的影响范围图 |
| `remediate` | 为发现的漏洞制定优先级修复计划 |
| `verify` | 验证软件包的完整性及来源合法性（SLSA 标准） |
| `diff` | 比较两次扫描结果（新发现的漏洞、已修复的漏洞或持续存在的漏洞） |
| `where` | 显示 MCP 客户端的配置文件位置 |
| `inventory` | 列出所有发现的代理、服务器及软件包信息 |

### 合规性与政策检查工具
| 工具 | 功能描述 |
|------|-------------|
| `compliance` | 检查是否符合 OWASP LLM/Agentic Top 10、EU AI Act、MITRE ATLAS、NIST AI RMF 等安全标准 |
| `policy_check` | 根据自定义安全策略（17 项条件）评估系统安全性 |
| `cis_benchmark` | 运行 CIS 基准测试（针对 AWS、Azure v3.0、GCP v3.0、Snowflake 等平台） |
| `generate_sbom` | 生成软件清单（CycloneDX 或 SPDX 格式） |
| `aisvs_benchmark` | 根据 OWASP AISVS v1.0 标准进行安全评估 |

### 注册表与信任度检查工具
| 工具 | 功能描述 |
|------|-------------|
| `registry_lookup` | 在 427 个以上的服务器安全元数据注册表中查找 MCP 服务器信息 |
| `marketplace_check` | 在安装前通过注册表验证软件包的信任度 |
| `fleet_scan` | 批量扫描 MCP 服务器的注册表信息并评估风险等级 |
| `skill_trust` | 评估技能文件的信任等级（分为 5 个类别） |
| `code_scan` | 使用 Semgrep 进行安全代码扫描，并根据 CWE（Common Weakness Enumeration）标准进行漏洞分类 |

### 运行时分析与监控工具
| 工具 | 功能描述 |
| `context_graph` | 生成代理之间的交互关系图，分析潜在的安全风险 |
| `analytics_query` | 查询漏洞趋势、系统配置历史及运行时事件 |
| `runtime_correlate` | 将代理审计数据（JSONL 格式）与漏洞信息进行关联分析 |
| `vector_db_scan` | 在 Qdrant/Weaviate/Chroma/Milvus 等数据库中检查认证和数据泄露风险 |
| `gpu_infra_scan` | 监控 GPU 容器和 K8s 节点的安全状态 |

### 专门化的扫描工具
| 工具 | 功能描述 |
|------|-------------|
| `dataset_card_scan` | 检查数据集卡片是否存在偏见、许可问题及来源不明的情况 |
| `training_pipeline_scan` | 扫描训练流程配置中的安全风险 |
| `browser_extension_scan` | 检查浏览器扩展程序是否存在危险权限或访问 AI 系统的风险 |
| `model_provenance_scan` | 验证模型来源的合法性及供应链的安全性 |
| `prompt_scan` | 检查提示模板是否存在注入或数据泄露风险 |
| `model_file_scan` | 检查模型文件是否存在不安全的序列化格式（如 pickle 等） |
| `license_compliance_scan` | 全面扫描软件包的许可证信息，检测是否存在违反开源许可（copyleft）的情况 |
| `ingest_external_scan` | 导入 Trivy/Grype/Syft 的扫描结果，并将其整合到 agent-bom 的报告中 |

### 资源管理工具
| 工具 | 功能描述 |
|----------|-------------|
| `registry://servers` | 提供访问 427 个以上 MCP 服务器安全元数据注册表的接口 |

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
- 即使 NVD（National Vulnerability Database）的分析结果尚未出来或漏洞的严重程度为 `unknown`，也必须显示该漏洞——即使没有详细信息，漏洞 ID 仍然代表一个真实存在的风险。请明确标注漏洞的严重程度为 `unknown`。
- 在对云环境进行扫描之前（如使用 `cis_benchmark` 工具），务必先获得用户的确认——这些操作会使用用户的凭证调用 AWS/Azure/GCP 的 API。
- 将漏洞的严重程度标记为 `UNKNOWN` 时应视为未解决的状态，而非无害状态——这表示相关数据尚未获取到，而非漏洞本身不严重。

**禁止的行为：**
- 禁止修改任何文件、安装新软件包或更改系统配置。该工具仅具有读取权限。
- 禁止将环境变量值、凭证或文件内容传输到任何外部服务。只有软件包名称和漏洞 ID 会被传出系统。
- 在未经用户确认的情况下，禁止在敏感环境中自动执行 `scan()` 函数。自动执行扫描的功能是受到严格限制的。

**在以下情况下应立即停止操作并询问用户：**
- 用户请求进行云环境扫描，但未提供相应的云服务凭证。
- 扫描过程中发现 `CRITICAL` 级别的漏洞——请向用户展示扫描结果，并询问是否需要生成修复计划。
- 用户请求扫描其个人目录之外的路径。

## 支持的安全框架
- **OWASP LLM Top 10**（2025 年版）：检测提示注入、供应链攻击及数据泄露风险 |
- **OWASP Agentic Top 10**：检测工具被恶意篡改、凭证被盗取等行为 |
- **OWASP AISVS v1.0**：人工智能安全验证标准（包含 9 项安全检查） |
- **MITRE ATLAS**：用于分析对抗性机器学习威胁的框架 |
- **MITRE ATT&CK Enterprise**：用于关联云环境和基础设施中的安全漏洞 |
- **MAESTRO**：为所有安全问题添加 KC1–KC6 级别的标签 |
- **EU AI Act**：规定人工智能系统的风险分类、透明度要求及软件清单生成规范 |
- **NIST AI RMF**：提供人工智能系统的管理、监控及生命周期管理框架 |
- **CIS Foundations**：支持 AWS、Azure v3.0、GCP v3.0、Snowflake 等平台的基准测试

## 隐私与数据保护

agent-bom 通过 PyPI 进行安装。在运行时，请先验证以下配置文件的处理方式：

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

**数据提取范围：** 从 MCP 客户端的配置文件中提取服务器名称、命令、参数及 URL。**数据保护措施：** 使用 `sanitize_env_vars()` 函数将环境变量值替换为 `***REDACTED***`，以防止数据泄露。只有公开的软件包名称和漏洞 ID 会被发送到漏洞数据库。云环境下的 CIS 测试会使用本地配置的凭证，并仅调用云服务提供商自身的 API。

## 验证信息
- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom) （基于 Apache-2.0 开源许可）
- **代码签名**：`agent-bom verify agent-bom@0.70.12`
- **经过 6,040 多次测试**（使用 CodeQL 和 OpenSSF 评分标准）
- **无数据追踪**：该工具不收集任何使用数据或进行分析
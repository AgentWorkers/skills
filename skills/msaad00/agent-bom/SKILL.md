---
name: agent-bom
description: >
  AI代理基础设施安全扫描器：  
  - 检查软件包中的安全漏洞（CVEs）；  
  - 在包含427多个服务器安全元数据的注册表中查询MCP服务器信息；  
  - 评估漏洞的扩散范围；  
  - 生成软件成分清单（SBOMs）；  
  - 确保系统符合相关安全标准（如OWASP、MITRE ATLAS、欧盟AI法案、NIST AI RMF）。  
  适用于以下场景：  
  - 用户需要执行漏洞扫描；  
  - 关注软件依赖项的安全性；  
  - 生成软件成分清单（SBOMs）；  
  - 需要验证MCP服务器的可靠性；  
  - 评估AI供应链中的安全风险。
  AI agent infrastructure security scanner — check packages for CVEs, look up MCP servers
  in the 427+ server security metadata registry, assess blast radius, generate SBOMs, enforce
  compliance (OWASP, MITRE ATLAS, EU AI Act, NIST AI RMF). Use when the user
  mentions vulnerability scanning, dependency security, SBOM generation, MCP server
  trust, or AI supply chain risk.
version: 0.57.0
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. Optional: Docker for container
  scanning (Grype/Syft). No external API keys required for basic operation.
metadata:
  author: msaad00
  homepage: https://github.com/msaad00/agent-bom
  source: https://github.com/msaad00/agent-bom
  pypi: https://pypi.org/project/agent-bom/
  smithery: https://smithery.ai/server/agent-bom/agent-bom
  scorecard: https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom
  tests: 6100
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.57.0
  openclaw:
    requires:
      bins: []
      env: []
    optional_env:
      - NVD_API_KEY
      - SNYK_TOKEN
      - AGENT_BOM_CLICKHOUSE_URL
    optional_bins:
      - syft
      - grype
      - kubectl
      - semgrep
      - docker
    emoji: "\U0001F6E1"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    file_reads_note: "Reads server names and command paths only — never credentials, tokens, or env var values"
    file_reads:
      - "~/.cursor/mcp.json"
      - "~/Library/Application Support/Claude/claude_desktop_config.json"
      - "~/.claude/settings.json"
      - "~/.windsurf/mcp.json"
      - "~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json"
      - "user-provided SBOM files (CycloneDX/SPDX JSON)"
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
      - url: "https://api.deps.dev/v3alpha"
        purpose: "Google deps.dev — transitive dependency resolution and license enrichment"
        auth: false
      - url: "https://api.snyk.io"
        purpose: "Snyk vulnerability enrichment (requires SNYK_TOKEN)"
        auth: true
      - url: "https://agent-bom-mcp.up.railway.app/sse"
        purpose: "Optional remote MCP endpoint — local-first scanning recommended"
        auth: false
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom — 人工智能供应链安全扫描器

该工具用于扫描人工智能基础设施中的漏洞，生成供应链安全清单（SBOM），并确保合规性。它可以发现来自20个MCP客户端的客户端、服务器和软件包。

## 安装（推荐：优先选择本地安装）

本地扫描可以消除对第三方服务的依赖，所有漏洞数据库（如OSV、NVD、EPSS、KEV）都会直接从您的机器上进行查询。

```bash
pipx install agent-bom
agent-bom scan              # auto-discover 20 MCP clients + scan
agent-bom check langchain   # check a specific package
agent-bom where             # show all discovery paths
```

### 作为MCP服务器（本地安装）

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

### 作为Docker容器

```bash
docker run --rm ghcr.io/msaad00/agent-bom:0.57.0 scan
```

### 自托管的SSE服务器

```bash
docker build -f Dockerfile.sse -t agent-bom-sse .
docker run -p 8080:8080 agent-bom-sse
# Connect: { "type": "sse", "url": "http://localhost:8080/sse" }
```

## 可用的MCP工具（共19种）

| 工具 | 描述 |
|------|-------------|
| `scan` | 全面发现+漏洞扫描流程 |
| `check` | 检查软件包是否存在CVE漏洞（OSV、NVD、EPSS、KEV） |
| `blast_radius` | 绘制漏洞在代理、服务器和凭证之间的影响链 |
| `registry_lookup` | 在427个以上的服务器安全元数据注册表中查找MCP服务器 |
| `compliance` | 遵守OWASP LLM/Agentic Top 10、欧盟AI法案、MITRE ATLAS、NIST AI RMF等安全标准 |
| `remediate` | 为漏洞制定优先级修复计划 |
| `verify` | 检查软件包的完整性及来源可信度（SLSA标准） |
| `skill_trust` | 评估技能文件的信任等级（分为5个类别） |
| `generate_sbom` | 生成供应链安全清单（CycloneDX或SPDX格式） |
| `policy_check` | 根据安全策略评估扫描结果 |
| `diff` | 比较两次扫描报告（新发现的漏洞、已解决的漏洞或持续存在的漏洞） |
| `marketplace_check` | 进行预安装信任度检查，并与注册表数据进行交叉验证 |
| `code_scan` | 通过Semgrep进行SAST扫描，并根据CWE标准进行合规性评估 |
| `where` | 显示MCP客户端的配置路径 |
| `inventory` | 列出所有发现的代理、服务器和软件包 |
| `context_graph` | 生成代理之间的上下文关系图及横向移动分析 |
| `analytics_query` | 从ClickHouse数据库查询漏洞趋势、系统配置历史和运行时事件 |
| `cis_benchmark` | 对AWS或Snowflake账户进行CIS基准测试 |
| `fleet_scan` | 批量查询注册表信息并对MCP服务器库存进行风险评分 |

## MCP资源

| 资源 | 描述 |
|----------|-------------|
| `registry://servers` | 浏览427个以上的MCP服务器安全元数据注册表 |
| `policy://template` | 默认的安全策略模板 |

## 示例工作流程

```
# Check a package before installing
check(package="@modelcontextprotocol/server-filesystem", ecosystem="npm")

# Map blast radius of a CVE
blast_radius(cve_id="CVE-2024-21538")

# Look up a server in the threat registry
registry_lookup(server_name="brave-search")

# Generate an SBOM
generate_sbom(format="cyclonedx")

# Assess trust of a skill file
skill_trust(skill_content="<paste SKILL.md content>")
```

## 远程SSE端点（可选）

对于仅支持远程服务器的MCP客户端（例如某些Claude桌面配置），提供了一个便捷的远程端点：

```json
{
  "mcpServers": {
    "agent-bom": {
      "type": "sse",
      "url": "https://agent-bom-mcp.up.railway.app/sse"
    }
  }
}
```

**重要提示：** 该端点使用的漏洞数据库与本地扫描相同。它仅接收您在工具调用中提供的参数（软件包名称、CVE ID、服务器名称）。在敏感环境中，建议使用本地安装或自行托管实例。

## 隐私与数据处理

### 配置文件读取

该工具仅读取本地MCP客户端的配置文件，以提取**服务器名称和命令路径**。它不会读取、解析或传输这些文件中的凭证信息、API密钥或环境变量内容。提取的数据（例如“brave-search在Claude桌面中已配置”）仅会保存在本地内存中，并且仅会在您明确请求的情况下包含在扫描输出中。

### 网络行为

默认情况下，所有扫描操作都在本地完成，不会进行任何出站连接，除非需要访问公共漏洞数据库（OSV、NVD、EPSS）。远程SSE端点（`railway.app`）是**可选的**——您必须将其添加到MCP客户端配置中。在正常本地操作期间，该端点不会被主动访问。

可选的令牌（NVD_API_KEY、SNYK_TOKEN、AGENT_BOM_CLICKHOUSE_URL）仅在您明确设置时才会使用。这些令牌不会被自动检测或推断。

## 安全限制

### 可安全传输的数据（仅限公开信息）

- 公开的软件包名称及版本（如`langchain`、`express@4.18.2`）
- 公开的CVE ID（如`CVE-2024-21538`）
- 公开的MCP服务器名称（如`brave-search`）
- 生态系统标识符（如`pypi`、`npm`、`go`）

### 禁止传输的数据

- API密钥、令牌、密码或`.env`文件的内容
- 完整的配置文件（可能包含凭证信息）
- 内部URL、主机名或专有软件包名称
- 请使用 `${env:VAR}`的形式引用变量，切勿直接使用原始凭证值

## 验证信息

- **来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（Apache-2.0许可证）
- **PyPI**：[pypi.org/project/agent-bom](https://pypi.org/project/agent-bom/)
- **Smithery**：[smithery.ai/server/agent-bom](https://smithery.ai/server/agent-bom/agent-bom)
- **签名验证**：`agent-bom verify agent-bom@0.57.0`
- **经过6,100多次安全测试**（使用CodeQL和OpenSSF评分标准）
- **OpenSSF评分结果**：[securityscorecards.dev](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom)
- **无数据追踪**：不收集任何用户数据或进行分析
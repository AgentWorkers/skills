---
name: agent-bom
description: >
  AI代理基础设施安全扫描器：  
  - 检查软件包中的安全漏洞（CVEs）；  
  - 在包含427个以上服务器安全元数据的注册表中查询MCP服务器信息；  
  - 评估漏洞的扩散范围（blast radius）；  
  - 生成软件成分清单（SBOMs）；  
  - 确保系统符合安全标准（如OWASP、MITRE ATLAS、欧盟AI法案、NIST AI RMF）。  
  适用于以下场景：  
  - 用户需要扫描系统中的安全漏洞；  
  - 确保软件依赖项的安全性；  
  - 生成软件成分清单（SBOMs）；  
  - 评估MCP服务器的信任等级；  
  - 识别AI供应链中的风险。
  AI agent infrastructure security scanner — check packages for CVEs, look up MCP servers
  in the 427+ server security metadata registry, assess blast radius, generate SBOMs, enforce
  compliance (OWASP, MITRE ATLAS, EU AI Act, NIST AI RMF). Use when the user
  mentions vulnerability scanning, dependency security, SBOM generation, MCP server
  trust, or AI supply chain risk.
version: 0.55.0
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
  tests: 3056
  install:
    pipx: agent-bom
    pip: agent-bom
    docker: ghcr.io/msaad00/agent-bom:0.55.0
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

该工具用于扫描人工智能（AI）基础设施中的漏洞，生成供应链安全清单（SBOM），并确保合规性。它可以发现来自18个以上AI平台的MCP客户端、服务器和软件包。

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
docker run --rm ghcr.io/msaad00/agent-bom:0.55.0 scan
```

### 自托管的SSE服务器

```bash
docker build -f Dockerfile.sse -t agent-bom-sse .
docker run -p 8080:8080 agent-bom-sse
# Connect: { "type": "sse", "url": "http://localhost:8080/sse" }
```

## 可用的MCP工具（共18个工具）

| 工具 | 描述 |
|------|-------------|
| `scan` | 全面扫描 + 漏洞检测流程 |
| `check` | 检查软件包是否存在CVE漏洞（OSV、NVD、EPSS、KEV） |
| `blast_radius` | 分析漏洞在代理节点、服务器及凭证之间的传播路径 |
| `registry_lookup` | 在427个以上的服务器安全元数据注册表中查找MCP服务器信息 |
| `compliance` | 遵循OWASP LLM/Agentic Top 10、欧盟AI法案、MITRE ATLAS、NIST AI RMF等安全标准 |
| `remediate` | 为发现的漏洞制定优先级修复计划 |
| `verify` | 验证软件包的完整性及来源合法性（符合SLSA标准） |
| `skill_trust` | 评估技能文件的信任等级（分为5个类别进行分析） |
| `generate_sbom` | 生成供应链安全清单（CycloneDX或SPDX格式） |
| `policy_check` | 根据安全策略评估扫描结果 |
| `diff` | 比较两次扫描报告（新发现的漏洞、已修复的漏洞或持续存在的漏洞） |
| `marketplace_check` | 进行预安装前的信任度检查，并与注册表数据进行交叉验证 |
| `code_scan` | 通过Semgrep进行静态应用安全测试（SAST），并关联CWE漏洞标准 |
| `where` | 显示MCP客户端的配置路径 |
| `inventory` | 列出所有发现的代理节点、服务器和软件包 |
| `context_graph` | 生成代理节点之间的关联关系图及横向移动分析结果 |
| `analytics_query` | 从ClickHouse数据库查询漏洞趋势、系统配置历史及运行时事件 |
| `cis_benchmark` | 对AWS或Snowflake账户进行CIS基准测试 |

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

对于仅支持远程服务器的MCP客户端（例如某些Claude桌面配置），提供了便捷的远程访问端点：

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

**重要提示：**该远程端点使用的漏洞数据库与本地扫描相同。它仅接收您在工具调用中提供的参数（软件包名称、CVE ID、服务器名称）。在敏感环境中，请优先选择本地安装或自行部署实例。

## 安全传输规范

### 可安全传输的数据（仅限公开信息）：

- 公开的软件包名称及版本（如`langchain`、`express@4.18.2`）
- 公开的CVE ID（如`CVE-2024-21538`）
- 公开的MCP服务器名称（如`brave-search`）
- 生态系统标识符（如`pypi`、`npm`、`go`）

### 禁止传输的数据：

- API密钥、令牌、密码或`.env`文件内容
- 完整的配置文件（可能包含敏感信息）
- 内部URL、主机名或专有软件包名称
- 请使用`${env:VAR}`的形式传递变量，切勿直接使用实际凭证值

## 验证信息

- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（遵循Apache-2.0许可证）
- **PyPI仓库**：[pypi.org/project/agent-bom](https://pypi.org/project/agent-bom/)
- **Smithery平台上的部署信息**：[smithery.ai/server/agent-bom](https://smithery.ai/server/agent-bom/agent-bom)
- **签名验证**：`agent-bom verify agent-bom@0.55.0`
- **安全性测试**：通过CodeQL和OpenSSF Scorecard进行了3,050多次自动化安全测试
- **OpenSSF评分结果**：[securityscorecards.dev](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom)
- **无数据追踪**：完全不收集用户数据，也不进行任何分析
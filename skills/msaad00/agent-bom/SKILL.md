---
name: agent-bom
description: AI供应链安全扫描器：用于检查软件包中的安全漏洞（CVEs），在包含427个以上服务器威胁信息的注册库中查询相关服务器（MCP服务器），评估漏洞的扩散范围，生成软件成分清单（SBOM），并确保系统符合安全标准（如OWASP、MITRE ATLAS、欧盟AI法案、NIST AI风险管理框架）。当用户提及漏洞扫描、依赖项安全评估、软件成分清单生成、MCP服务器的信任度验证或AI供应链相关风险时，可使用该工具。
  AI supply chain security scanner — check packages for CVEs, look up MCP servers
  in the 427+ server threat registry, assess blast radius, generate SBOMs, enforce
  compliance (OWASP, MITRE ATLAS, EU AI Act, NIST AI RMF). Use when the user
  mentions vulnerability scanning, dependency security, SBOM generation, MCP server
  trust, or AI supply chain risk.
version: 0.38.1
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
  tests: 2099
  openclaw:
    requires:
      bins: []
      env: []
    optional_env: []
    emoji: "\U0001F6E1"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    file_reads: []
    file_writes: []
    network_endpoints:
      - url: "https://trustworthy-solace-production-14a6.up.railway.app/sse"
        purpose: "Optional remote MCP endpoint — queries public vulnerability databases (OSV, NVD, EPSS, KEV) and the bundled registry. Local-first scanning recommended."
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
agent-bom scan              # auto-discover 18 MCP clients + scan
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
docker run --rm ghcr.io/msaad00/agent-bom:0.38.1 scan
```

### 自托管的SSE服务器

```bash
docker build -f Dockerfile.sse -t agent-bom-sse .
docker run -p 8080:8080 agent-bom-sse
# Connect: { "type": "sse", "url": "http://localhost:8080/sse" }
```

## 提供的MCP工具（共14种）

| 工具 | 描述 |
|------|-------------|
| `scan` | 全面发现并扫描漏洞 |
| `check` | 检查软件包是否存在CVE（来自OSV、NVD、EPSS、KEV） |
| `blast_radius` | 分析漏洞在代理、服务器和凭证之间的影响范围 |
| `registry_lookup` | 在427个以上的服务器威胁注册表中查找MCP服务器 |
| `compliance` | 遵循OWASP LLM/Agentic Top 10、欧盟AI法案、MITRE ATLAS、NIST AI RMF等安全标准 |
| `remediate` | 为漏洞制定优先级修复计划 |
| `verify` | 验证软件包的完整性及来源合法性（符合SLSA标准） |
| `skill_trust` | 评估技能文件的信任等级（分为5个类别） |
| `generate_sbom` | 生成供应链安全清单（CycloneDX或SPDX格式） |
| `policy_check` | 根据安全策略评估扫描结果 |
| `diff` | 比较两次扫描报告（新发现的漏洞、已解决的漏洞或持续存在的漏洞） |
| `marketplace_check` | 进行预安装前的信任度检查，并与注册表进行交叉验证 |
| `where` | 显示MCP客户端的配置路径 |
| `inventory` | 列出所有发现的代理、服务器和软件包 |

## MCP资源

| 资源 | 描述 |
|----------|-------------|
| `registry://servers` | 浏览427个以上的MCP服务器威胁情报注册表 |
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
      "url": "https://trustworthy-solace-production-14a6.up.railway.app/sse"
    }
  }
}
```

**重要提示：** 该远程端点使用与本地扫描相同的公共漏洞数据库。它仅接收您在工具调用中提供的参数（软件包名称、CVE ID、服务器名称）。在敏感环境中，建议选择本地安装或自托管实例。

## 安全传输规范

### 可以安全传输的数据（仅限公开信息）：

- 公开的软件包名称及版本（如`langchain`、`express@4.18.2`）
- 公开的CVE ID（如`CVE-2024-21538`）
- 公开的MCP服务器名称（如`brave-search`）
- 生态系统标识符（如`pypi`、`npm`、`go`）

### 绝对禁止传输的数据：

- API密钥、令牌、密码或`.env`文件的内容
- 完整的配置文件（可能包含敏感信息）
- 内部URL、主机名或专有软件包名称
- 请使用`${env:VAR}`的形式传递参数，切勿直接使用原始的敏感信息

## 验证信息

- **来源**: [github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（Apache-2.0许可证） |
- **PyPI仓库**: [pypi.org/project/agent-bom](https://pypi.org/project/agent-bom/) |
- **质量评分**: 99/100 |
- **签名验证**: 使用Sigstore签名（`agent-bom verify agent-bom@0.38.1`） |
- **安全测试**: 通过2,099项自动化安全测试（CodeQL + OpenSSF评分系统） |
- **OpenSSF评分**: [securityscorecards.dev](https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom) |
- **无数据追踪**: 不会收集任何用户数据或进行分析
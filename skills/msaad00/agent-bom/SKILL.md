---
name: agent-bom
description: >
  AI供应链安全扫描器：  
  - 检查软件包中是否存在安全漏洞（CVEs）；  
  - 在威胁数据库中查询相关MCP服务器信息；  
  - 评估漏洞的扩散范围；  
  - 生成软件成分清单（SBOMs）；  
  - 确保系统符合安全合规性要求。
version: 0.35.0
metadata:
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
      - url: "https://agent-bom-mcp.up.railway.app/sse"
        purpose: "Remote MCP server — tools query public vulnerability databases (OSV, NVD, EPSS, KEV) and the bundled 427-server registry. No local file access."
        auth: false
    telemetry: false
    persistence: false
    privilege_escalation: false
---
# agent-bom — 人工智能供应链安全扫描工具

这是一个MCP（Machine Configuration Platform）服务器，为人工智能基础设施提供安全扫描功能：
- **CVE查询**：检查任何软件包是否存在于OSV.dev、NVD、EPSS或CISA KEV等公开漏洞数据库中。
- **MCP注册表**：在包含427个以上服务器威胁情报的注册表中查找MCP服务器的信息。
- **漏洞传播路径分析**：分析漏洞（CVE）如何影响凭证和工具。
- **合规性检查**：符合OWASP LLM Top 10、MITRE ATLAS和NIST AI RMF等安全标准。

## 安全传输规范

### 可以安全传输的内容
| 可传输的内容 | 例子 |
|-------------|----------|
| 软件包名称及版本 | `langchain`, `express@4.18.2` |
| 生态系统标识符 | `pypi`, `npm`, `go` |
| CVE编号 | `CVE-2024-21538` |
| MCP服务器名称 | `brave-search`, `filesystem` |
- 用于信任评估的SKILL.md文件内容 |

### 绝对不能传输的内容
| 绝对禁止传输 | 原因 |
|-----------|-----|
- API密钥、令牌、密码 | 远程服务器无需这些信息，也无法安全地使用它们。
- 完整的配置文件 | 可能包含凭证信息或内部主机名。
- `.env`文件内容 | 包含敏感信息。
- 内部URL或主机名 | 可能暴露基础设施信息。

### 远程服务器的工作原理

该工具通过**HTTPS/TLS**连接到远程MCP服务器。服务器：
1. **不会读取您的本地文件**。服务器运行在Railway平台上，而非您的机器上。`filereads: []`这一声明是准确的——该工具永远不会访问您的文件系统。
2. **需要使用本地数据的工具**需要您提供相应的数据。例如，`check(package="langchain", ecosystem="pypi")`仅发送您提供的软件包名称，服务器会查询公开漏洞数据库并返回结果。
3. **查询服务器内数据的工具**可以立即执行操作。`registry_lookup`、`compliance`、`skill_trust`等工具会直接从服务器内部的数据库（如427-server注册表、OWASP/ATLAS/NIST映射表）中获取数据。
4. **`scan()`工具**仅扫描服务器自身的环境，不会访问您的机器。如需进行本地MCP配置扫描，请使用CLI命令：`pipx install agent-bom && agent-bom scan`。

**服务器接收的信息**：仅限于您在工具调用中提供的参数（软件包名称、CVE编号、服务器名称）。
**服务器发送的信息**：会将软件包名称及版本发送到OSV.dev、NVD、EPSS和CISA KEV等API，但不会包含任何凭证信息或配置内容。

### 如果使用自动代理调用

如果您的MCP客户端允许代理自动调用工具（无需每次调用都进行确认），请限制代理只能发送软件包名称、CVE编号和服务器名称。禁止代理将配置文件内容、环境变量或凭证信息传递给任何工具。

## 设置

将agent-bom MCP服务器添加到您的客户端配置中：
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

对于OpenClaw，将其添加到`~/.openclaw/openclaw.json`文件中。对于其他MCP客户端（如Claude Desktop、Cursor、VS Code等），请将其添加到相应的配置文件中。

## 可用的MCP工具

连接成功后，agent-bom MCP服务器提供**13种工具**：

### 完全通过远程服务器执行的工具（无需访问本地系统）
| 工具 | 功能描述 |
|------|-------------|
| `check` | 检查特定软件包是否存在已知漏洞（您需要提供软件包名称和生态系统信息）。 |
| `blast_radius` | 分析漏洞（CVE）在代理、服务器、凭证和工具之间的传播路径。 |
| `registry_lookup` | 在包含427个以上服务器威胁情报的注册表中查找MCP服务器。 |
| `compliance` | 检查是否符合OWASP LLM Top 10、MITRE ATLAS和NIST AI RMF等安全标准。 |
| `remediate` | 为发现的漏洞生成优先级排序的修复计划。 |
| `verify` | 检查软件包的完整性及来源可信性。 |
| `skill_trust` | 评估技能文件的信任等级（包含五项评估指标）。 |
| `generate_sbom` | 生成软件物料清单（CycloneDX或SPDX格式）。 |
| `policy_check` | 根据安全策略评估扫描结果。 |
| `diff` | 比较两份扫描报告以查看差异。 |

### 扫描服务器自身环境的工具
| 工具 | 功能描述 |
|------|-------------|
| `scan` | 在服务器环境中执行完整的扫描流程。如需进行本地扫描，请使用CLI命令。 |
| `where` | 显示服务器上的MCP客户端配置路径。 |
| `inventory` | 列出服务器上发现的代理和服务器信息。如需进行本地扫描，请使用CLI命令。 |

## 可用的MCP资源
| 资源 | 描述 |
|----------|-------------|
| `registry://servers` | 浏览包含427个以上服务器威胁情报的注册表。 |
| `policy://template` | 默认的安全策略模板。 |

## 示例工作流程

### 安装前检查软件包
```
check(package="@modelcontextprotocol/server-filesystem", ecosystem="npm")
```

### 分析漏洞的传播路径
```
blast_radius(cve_id="CVE-2024-21538")
```

### 在威胁注册表中查找服务器
```
registry_lookup(server_name="brave-search")
```

### 检查合规性
```
compliance()
```

### 生成软件物料清单
```
generate_sbom(format="cyclonedx")
```

### 评估技能文件的信任等级
```
skill_trust(skill_content="<paste SKILL.md content>")
```

## 本地扫描（自动发现您的MCP配置）

若要扫描自己机器上的MCP客户端配置，并自动发现18个客户端（Claude Desktop、Cursor、Codex CLI、Gemini CLI等）的配置，请在本地安装相应的CLI工具：
```bash
pipx install agent-bom
agent-bom scan                    # auto-discover + scan local configs
agent-bom scan --dry-run          # preview what would be read (nothing accessed)
agent-bom scan --enforce          # + tool poisoning detection
agent-bom where                   # show all 18 client discovery paths
```

该CLI会读取[PERMISSIONS.md](https://github.com/msaad00/agent-bom/blob/main/PERMISSIONS.md)中列出的27个配置路径，仅提取服务器名称、软件包名称和环境变量名称，不会获取任何值或敏感信息。

## 代码来源与验证信息
- **源代码**：https://github.com/msaad00/agent-bom（采用Apache-2.0许可证）
- **PyPI仓库**：https://pypi.org/project/agent-bom/
- **质量评估**：在Smithery平台上的评分达到99/100。
- **签名验证**：每个版本都使用Sigstore OIDC进行签名。
- **安全测试**：每个代码提交都经过自动化安全扫描。
- **OpenSSF评分**：https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom
---
name: agent-bom
description: >
  AI供应链安全扫描器：  
  - 检查软件包中是否存在安全漏洞（CVEs）；  
  - 在威胁数据库中查询相关MCP服务器；  
  - 评估漏洞的扩散范围；  
  - 生成软件成分清单（SBOMs）；  
  - 确保系统符合安全合规性要求。
version: 0.36.1
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
      - url: "https://trustworthy-solace-production-14a6.up.railway.app/sse"
        purpose: "Remote MCP server — tools query public vulnerability databases (OSV, NVD, EPSS, KEV) and the bundled 427-server registry. No local file access."
        auth: false
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom — 人工智能供应链安全扫描工具

这是一个MCP（Machine Configuration Platform）服务器，为人工智能基础设施提供安全扫描功能：
- **CVE查询**：检查任何软件包是否存在于OSV.dev、NVD、EPSS或CISA KEV等漏洞数据库中
- **MCP注册表**：在包含427个以上服务器威胁情报的注册表中查找相应的MCP服务器
- **漏洞传播路径分析**：分析CVE如何影响凭证和工具
- **合规性检查**：符合OWASP LLM Top 10、OWASP Agentic Top 10、欧盟AI法案、MITRE ATLAS及NIST AI RMF等安全标准

## 推荐使用：本地扫描

**在敏感环境中，建议优先使用本地扫描方式，而非远程端点。**这样可以避免所有与第三方相关的信任问题：

```bash
pipx install agent-bom
agent-bom scan              # full local auto-discovery + scan
agent-bom check langchain   # local CVE lookup
```

下方的远程SSE（Secure Shell Endpoint）仅适用于那些仅支持远程MCP服务器的客户端（例如Claude Desktop）。如果可能的话，建议优先选择本地扫描。

## 安全传输规范

### 可以安全传输的内容
| 可传输内容 | 示例 | 风险等级 |
|-------------|----------|------|
| 公开的软件包名称及版本 | `langchain`, `express@4.18.2` | 无风险——这些数据来自公共注册表 |
| 生态系统标识符 | `pypi`, `npm`, `go` | 无风险 |
| 公开的CVE ID | `CVE-2024-21538` | 无风险——这些是公开的可识别信息 |
| 公开的MCP服务器名称 | `brave-search`, `filesystem` | 无风险——这些都是公开的信息 |
| 非敏感性的技能文件内容 | 用于信任评估的SKILL.md文件内容 | 低风险——发送前请先审核内容 |

### 禁止传输的内容
| 绝对禁止传输 | 原因 | 应采取的缓解措施 |
|-----------|-----|------------|
| API密钥、令牌、密码 | 远程服务器不需要这些信息，也无法安全地使用它们 | 使用 `${env:VAR}` 代替实际值 |
| 完整的配置文件 | 可能包含凭证信息或内部主机名 | 仅手动提取软件包名称 |
`.env` 文件内容 | 包含敏感信息 | 严禁将`.env`文件作为参数传递给工具 |
| 内部URL或主机名 | 可能暴露基础设施拓扑结构 | 请使用通用名称或选择本地扫描 |

### 远程服务器的工作原理

该工具通过**HTTPS/TLS**协议连接到远程MCP服务器。服务器：
1. **不会读取您的本地文件**：服务器运行在Railway平台上，而非您的机器上。`filereads: []` 表明该工具不会访问您的文件系统。
2. **不会存储您的查询数据**：不会记录软件包名称、CVE ID或工具调用参数。仅支持无状态的请求-响应模式。
3. **需要本地数据的工具需要您自行提供数据**：例如，`check(package="langchain", ecosystem="pypi")` 仅会发送您提供的软件包名称，服务器会查询公开漏洞数据库并返回结果。
4. **查询捆绑数据的工具可立即执行操作**：`registry_lookup`, `compliance`, `skill_trust` 等工具会使用服务器内部的数据库（如427-server注册表、OWASP/ATLAS/NIST映射数据）。
5. **`scan()` 工具仅扫描服务器自身的环境**：不会访问您的机器。如需扫描本地的MCP配置信息，请使用命令行界面（CLI）。

**服务器接收的信息**：仅限于您在工具调用中提供的参数（软件包名称、CVE ID、服务器名称）。
**服务器发送的信息**：将软件包名称及版本发送到OSV.dev、NVD、EPSS和CISA KEV等API，不会包含任何凭证、主机名或配置内容。

### 自动调用政策

**该工具的默认设置为 `always: false`——未经用户确认，禁止自动调用。**

如果您的MCP客户端允许代理自动调用工具，请遵循以下规则：
1. **每次调用都必须获得确认**：尤其是`skill_trust` 和 `check` 等工具。
2. **限制输入范围**：仅允许代理发送公开的软件包名称、CVE ID和服务器名称。
3. **禁止代理将配置文件、环境变量、凭证信息或内部主机名传递给任何工具**。
4. **监控工具调用参数**：在批准每次调用前，请仔细检查代理发送的数据。

### 验证远程端点

在信任Railway SSE端点之前，您可以：
1. **查看源代码**：服务器代码位于 [github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0框架）。
2. **执行测试查询**：尝试 `check(package="express", ecosystem="npm")` 并验证返回结果是否与公开的数据一致。
3. **自行部署**：可以使用 `docker build -f Dockerfile.sse -t agent-bom-sse . && docker run -p 8080:8080 agent-bom-sse` 命令部署自己的实例。
4. **使用网络代理**：通过mitmproxy等工具路由流量，以确保仅传输预期的数据。

## 配置方法

将agent-bom MCP服务器添加到您的客户端配置文件中：

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

对于OpenClaw客户端，请将其添加到 `~/.openclaw/openclaw.json` 文件中；对于其他MCP客户端（如Claude Desktop、Cursor、VS Code等），请将其添加到相应的配置文件中。

## 可用的MCP工具

连接成功后，agent-bom MCP服务器提供了**14种工具**：

### 完全通过远程服务器执行的工具（无需本地访问）
| 工具 | 功能描述 |
|------|-------------|
| `check` | 检查特定软件包是否存在已知漏洞（您需要提供软件包名称和生态系统信息） |
| `blast_radius` | 分析CVE如何影响代理、服务器、凭证和工具之间的安全链 |
| `registry_lookup` | 在包含427个以上服务器威胁情报的注册表中查找MCP服务器 |
| `compliance` | 检查是否符合OWASP LLM Top 10、OWASP Agentic Top 10、欧盟AI法案、MITRE ATLAS和NIST AI RMF等安全标准 |
| `remediate` | 为发现的漏洞生成优先级排序的修复计划 |
| `verify` | 检查软件包的完整性和来源可信度 |
| `skill_trust` | 评估技能文件的信任等级（包含五项评估指标） |
| `generate_sbom` | 生成软件物料清单（CycloneDX或SPDX格式） |
| `policy_check` | 根据安全策略评估扫描结果 |
| `diff` | 比较两份扫描报告以识别变化 |
| `marketplace_check` | 预先检查市场中的软件包是否符合安全标准（包含注册表交叉验证） |

### 扫描服务器自身环境的工具（不涉及您的机器）
| 工具 | 功能描述 |
|------|-------------|
| `scan` | 在服务器环境中执行完整的扫描流程。如需本地扫描，请使用命令行界面（CLI）。 |
| `where` | 显示服务器上的MCP客户端配置路径。如需本地扫描，请使用CLI。 |
| `inventory` | 列出服务器上发现的代理和服务器信息。如需本地清单，请使用CLI。 |

## 可用的MCP资源
| 资源 | 描述 |
|----------|-------------|
| `registry://servers` | 浏览包含427个以上服务器威胁情报的注册表 |
| `policy://template` | 默认的安全策略模板 |

## 示例工作流程
- **安装前检查软件包**  
```
check(package="@modelcontextprotocol/server-filesystem", ecosystem="npm")
```

- **分析CVE的传播路径**  
```
blast_radius(cve_id="CVE-2024-21538")
```

- **在威胁注册表中查找服务器**  
```
registry_lookup(server_name="brave-search")
```

- **检查合规性**  
```
compliance()
```

- **生成软件物料清单**  
```
generate_sbom(format="cyclonedx")
```

- **评估技能文件的信任等级**  
```
skill_trust(skill_content="<paste SKILL.md content>")
```

## 本地扫描（自动发现您的MCP配置）

若要扫描自己机器上的MCP客户端配置，并实现跨18个客户端（Claude Desktop、Cursor、Codex CLI、Gemini CLI等）的自动发现功能，请先在本地安装相应的命令行工具：

```bash
pipx install agent-bom
agent-bom scan                    # auto-discover + scan local configs
agent-bom scan --dry-run          # preview what would be read (nothing accessed)
agent-bom scan --enforce          # + tool poisoning detection
agent-bom where                   # show all 18 client discovery paths
```

该命令行工具会读取`PERMISSIONS.md`（位于 [https://github.com/msaad00/agent-bom/blob/main/PERMISSIONS.md]）中列出的27个配置路径，仅提取服务器名称、软件包名称和环境变量名称，不会获取任何值或敏感信息。

## 代码来源与验证信息
- **源代码**：https://github.com/msaad00/agent-bom（基于Apache-2.0框架，代码可完全审计）
- **PyPI仓库**：https://pypi.org/project/agent-bom/
- **Smithery评分**：评分99/100
- **Sigstore签名**：所有版本均使用Sigstore OIDC进行签名，可通过 `agent-bom verify agent-bom@0.36.1` 验证签名有效性
- **安全测试**：每次提交都会通过自动化安全扫描（CodeQL + OpenSSF评分卡）
- **OpenSSF评分卡**：https://securityscorecards.dev/viewer/?uri=github.com/msaad00/agent-bom
- **可自行部署**：使用 `docker build -f Dockerfile.sse` 命令即可部署自己的实例，无需依赖第三方组件
- **无数据追踪**：配置`telemetry: false`，禁止任何形式的追踪、分析或数据上报
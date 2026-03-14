---
name: agent-bom-registry
description: >
  MCP服务器安全注册表与信任评估功能：  
  - 在包含427个以上服务器安全元数据的注册表中查询服务器信息；  
  - 执行安装前的市场环境检查；  
  - 对服务器集群进行批量风险评分；  
  - 评估技能文件的信任度；  
  - 进行静态应用安全测试（SAST）代码扫描。  
  该功能适用于用户需要查询MCP服务器的信任状态、注册表信息、市场环境检查或技能文件信任度评估的场景。
  MCP server security registry and trust assessment — look up servers in the 427+
  server security metadata registry, run pre-install marketplace checks, batch
  fleet risk scoring, assess skill file trust, and run SAST code scans. Use when
  the user mentions MCP server trust, registry lookup, marketplace check, or
  skill trust assessment.
version: 0.70.7
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. Optional: Semgrep for SAST
  code scanning. No API keys or network access required (registry is bundled).
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
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    credential_policy: "Zero credentials required. Registry data is bundled locally. No network calls needed."
    optional_env:
      - name: SNYK_TOKEN
        purpose: "Snyk vulnerability enrichment for code_scan (optional)"
        required: false
    optional_bins:
      - semgrep
    emoji: "\U0001F50D"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    data_flow: "Purely local. Registry data (427+ MCP server metadata) is bundled in the package. Lookups are in-memory string matches. Skill trust analysis parses user-provided SKILL.md content passed as a string argument."
    file_reads:
      - "user-provided SKILL.md files (for skill_trust analysis)"
    file_writes: []
    network_endpoints:
      - url: "https://api.snyk.io"
        purpose: "Snyk vulnerability enrichment for code_scan (requires SNYK_TOKEN)"
        auth: true
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom-registry — MCP服务器信任与安全注册表

该工具用于在包含427多个服务器安全元数据的注册表中查询MCP服务器，评估这些服务器的文件信任度，并执行安装前的市场检查。

## 安装

```bash
pipx install agent-bom
agent-bom registry-lookup brave-search
agent-bom marketplace-check @anthropic/server-filesystem
```

## 工具（5个）

| 工具 | 描述 |
|------|-------------|
| `registry_lookup` | 在包含427多个服务器安全元数据的注册表中查询MCP服务器 |
| `marketplace_check` | 基于注册表信息进行安装前的信任度检查 |
| `fleet_scan` | 对MCP服务器库存进行批量注册表查询和风险评分 |
| `skill_trust` | 评估文件信任度（采用五类分析方法） |
| `code_scan` | 使用Semgrep进行SAST扫描，并结合CWE标准进行合规性验证 |

## 示例工作流程

```
# Look up a server in the registry
registry_lookup(server_name="brave-search")

# Pre-install trust check
marketplace_check(package="@modelcontextprotocol/server-filesystem")

# Assess trust of a skill file
skill_trust(skill_content="<paste SKILL.md content>")

# Batch risk scoring
fleet_scan(servers=["brave-search", "github", "slack"])
```

## MCP资源

| 资源 | 描述 |
|----------|-------------|
| `registry://servers` | 浏览包含427多个MCP服务器安全元数据的注册表 |

## 隐私与数据处理

注册表数据被**打包在软件包中**——所有查询操作均在内存中完成，无需任何网络调用。文件信任度分析仅处理作为字符串参数传递的数据（无需访问文件系统）。

## 验证信息

- **来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证）
- 通过CodeQL和OpenSSF Scorecard进行了6,040多次测试
- **无数据追踪**：完全不收集用户数据或进行分析
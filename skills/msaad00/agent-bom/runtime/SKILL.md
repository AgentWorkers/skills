---
name: agent-bom-runtime
description: AI运行时安全监控——包括上下文图分析、运行时审计日志与CVE（Common Vulnerabilities and Exposures）漏洞的关联分析，以及漏洞分析查询功能。当用户提到运行时监控、上下文图、横向移动分析、审计日志关联或漏洞分析时，请使用此功能。
  AI runtime security monitoring — context graph analysis, runtime audit log
  correlation with CVE findings, and vulnerability analytics queries. Use when
  the user mentions runtime monitoring, context graphs, lateral movement analysis,
  audit log correlation, or vulnerability analytics.
version: 0.62.0
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. Optional: kubectl for
  Kubernetes context, ClickHouse for analytics storage. No API keys required.
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
  openclaw:
    requires:
      bins: []
      env: []
      credentials: none
    credential_policy: "Zero credentials required. Optional ClickHouse URL enables analytics storage. Never auto-discovered or inferred."
    optional_env: []
    optional_bins:
      - kubectl
    emoji: "\U0001F4CA"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    data_flow: "Operates on scan results in memory and user-provided audit log files. Optional ClickHouse connection for persistent analytics (user-configured, not auto-discovered)."
    file_reads:
      - "user-provided audit log files (JSONL format from agent-bom proxy)"
    file_writes: []
    network_endpoints: []
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom-runtime — AI Runtime Security Monitoring

该工具提供运行时安全监控功能，包括上下文图分析、运行时审计日志与漏洞信息（CVE）的关联分析，以及漏洞分析查询等功能。

## 安装

```bash
pipx install agent-bom
```

## 工具（3个）

| 工具 | 描述 |
|------|-------------|
| `context_graph` | 用于生成包含横向移动行为的代理上下文图 |
| `analytics_query` | 用于查询漏洞趋势、系统配置历史及运行时事件 |
| `runtime_correlate` | 将运行时审计日志与漏洞信息进行交叉比对 |

## 示例工作流程

```
# Build context graph from scan results
context_graph()

# Correlate runtime audit with CVE data
runtime_correlate(audit_file="proxy-audit.jsonl")

# Query analytics
analytics_query(query="top_cves", days=30)
```

## 隐私与数据处理

该工具仅处理内存中的扫描结果以及用户提供的审计日志文件，不会自动进行文件发现。除非配置了可选的ClickHouse端点用于持久化分析，否则不会发起网络请求。

## 验证信息

- **来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证）
- 经过3,400多次测试，使用CodeQL和OpenSSF评分标准进行评估
- **无数据传输**：完全不收集或传输任何用户数据（无遥测功能）
---
name: agent-bom-compliance
description: AI合规性与政策引擎：根据OWASP LLM Top 10、MITRE ATLAS、欧盟AI法案、NIST AI RMF以及自定义的基于代码的政策规则来评估扫描结果。能够生成符合CycloneDX或SPDX格式的软件成分清单（SBOM）。适用于需要执行合规性检查、安全策略管理、生成软件成分清单或遵循相关监管框架的场景。
  AI compliance and policy engine — evaluate scan results against OWASP LLM Top 10,
  MITRE ATLAS, EU AI Act, NIST AI RMF, and custom policy-as-code rules. Generate
  SBOMs in CycloneDX or SPDX format. Use when the user mentions compliance checking,
  security policy enforcement, SBOM generation, or regulatory frameworks.
version: 0.60.2
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. No credentials required for
  OWASP/NIST/EU AI Act evaluation. CIS benchmark checks optionally use cloud
  SDK credentials (AWS/Azure/GCP/Snowflake) if provided.
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
    credential_policy: "Zero credentials required for OWASP/NIST/EU AI Act compliance and SBOM generation. CIS benchmark checks (AWS, Azure, GCP, Snowflake) optionally accept cloud credentials — only used locally to call cloud APIs, never transmitted elsewhere."
    optional_env:
      - name: AWS_PROFILE
        purpose: "AWS CIS benchmark checks — uses boto3 with your local AWS profile"
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
    optional_bins: []
    emoji: "\U00002705"
    homepage: https://github.com/msaad00/agent-bom
    source: https://github.com/msaad00/agent-bom
    license: Apache-2.0
    os:
      - darwin
      - linux
      - windows
    data_flow: "Purely local for OWASP/NIST/EU AI Act/MITRE/SBOM features. CIS benchmark checks call cloud provider APIs (AWS/Azure/GCP/Snowflake) using locally configured credentials — no data is stored or transmitted beyond the cloud provider's own API. Zero file reads beyond user-provided SBOMs."
    file_reads:
      - "user-provided SBOM files (CycloneDX/SPDX JSON)"
      - "user-provided policy files (YAML/JSON policy-as-code)"
    file_writes: []
    network_endpoints: []
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom-compliance — 人工智能合规性与政策引擎

该工具用于根据安全框架评估人工智能基础设施的扫描结果，并执行基于代码的策略（policy-as-code）规则。同时，能够生成符合标准格式的安全物料清单（Security Bill of Materials, SBOM）。

## 安装

```bash
pipx install agent-bom
agent-bom compliance        # run compliance check on latest scan
agent-bom generate-sbom     # generate CycloneDX SBOM
```

## 所用工具（4种）

| 工具 | 描述 |
|------|-------------|
| `compliance` | 支持OWASP LLM/Agentic Top 10、欧盟AI法案（EU AI Act）、MITRE ATLAS、NIST AI RMF等安全标准 |
| `policy_check` | 根据自定义的安全策略（包含17项条件）评估扫描结果 |
| `cis_benchmark` | 对云账户执行CIS基准测试 |
| `generate_sbom` | 生成符合CycloneDX或SPDX格式的安全物料清单（SBOM） |

## 支持的安全框架

- **OWASP LLM Top 10**（2025版）：检测提示注入（prompt injection）、供应链攻击、数据泄露等问题 |
- **OWASP Agentic Top 10**：检测工具攻击（tool poisoning）、恶意软件植入（rug pulls）、凭证盗窃等行为 |
- **MITRE ATLAS**：用于评估对抗性机器学习（adversarial ML）威胁 |
- **欧盟AI法案**：涵盖风险分类、透明度要求以及安全物料清单（SBOM）的生成规范 |
- **NIST AI RMF**：提供人工智能系统的治理、映射、测量和管理生命周期的框架 |
- **CIS Foundations**：支持AWS、Azure v3.0、GCP v3.0、Snowflake等云平台的基准测试 |

## 示例工作流程

```
# Run compliance check
compliance(frameworks=["owasp_llm", "eu_ai_act"])

# Enforce custom policy
policy_check(policy={"max_critical": 0, "max_high": 5})

# Generate SBOM
generate_sbom(format="cyclonedx")
```

## 隐私与数据管理

所有合规性评估操作均在内存中的扫描数据上本地完成，不会读取任何磁盘文件（用户提供的SBOM文件除外），也不会进行任何网络请求；同时，无需使用任何凭证。

## 验证信息

- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（采用Apache-2.0许可证） |
- 该工具包含超过3,400项测试用例，通过CodeQL和OpenSSF Scorecard进行评估 |
- **无数据追踪**：完全不收集任何用户数据或进行数据分析 |
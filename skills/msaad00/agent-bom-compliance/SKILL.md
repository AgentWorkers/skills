---
name: agent-bom-compliance
description: AI合规性与政策引擎：根据OWASP LLM Top 10、MITRE ATLAS、欧盟AI法案（EU AI Act）、NIST AI RMF以及自定义的基于代码的政策（policy-as-code）规则来评估扫描结果。该工具可生成符合CycloneDX或SPDX格式的安全物料清单（Security Bill of Materials, SBOM）。适用于需要执行合规性检查、安全策略管理、生成安全物料清单或遵循相关监管框架的场景。
  AI compliance and policy engine — evaluate scan results against OWASP LLM Top 10,
  MITRE ATLAS, EU AI Act, NIST AI RMF, and custom policy-as-code rules. Generate
  SBOMs in CycloneDX or SPDX format. Use when the user mentions compliance checking,
  security policy enforcement, SBOM generation, or regulatory frameworks.
version: 0.70.7
license: Apache-2.0
compatibility: >-
  Requires Python 3.11+. Install via pipx or pip. OWASP/NIST/EU AI Act/MITRE
  evaluation and SBOM generation are fully local with zero credentials. CIS
  benchmark checks optionally use cloud SDK credentials (AWS/Azure/GCP/Snowflake)
  and make read-only API calls to cloud providers when explicitly invoked.
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
      - name: SNOWFLAKE_PRIVATE_KEY_PATH
        purpose: "Snowflake key-pair auth (CI/CD)"
        required: false
      - name: SNOWFLAKE_AUTHENTICATOR
        purpose: "Snowflake auth method (default: externalbrowser SSO)"
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
    data_flow: >-
      OWASP/NIST/EU AI Act/MITRE/SBOM evaluation is purely local — zero network
      calls. CIS benchmark checks (optional, user-initiated) call cloud provider
      APIs (AWS/Azure/GCP/Snowflake) using locally configured credentials. No data
      is stored or transmitted beyond the cloud provider's own API. File reads are
      limited to user-provided SBOMs and policy files.
    file_reads:
      - "user-provided SBOM files (CycloneDX/SPDX JSON)"
      - "user-provided policy files (YAML/JSON policy-as-code)"
    file_writes: []
    network_endpoints:
      - url: "https://*.amazonaws.com"
        purpose: "AWS CIS benchmark checks — read-only API calls (IAM, S3, CloudTrail, etc.)"
        auth: true
        optional: true
      - url: "https://management.azure.com"
        purpose: "Azure CIS benchmark checks — read-only API calls (Azure Resource Manager)"
        auth: true
        optional: true
      - url: "https://*.googleapis.com"
        purpose: "GCP CIS benchmark checks — read-only API calls (Cloud Resource Manager, IAM, etc.)"
        auth: true
        optional: true
      - url: "https://*.snowflakecomputing.com"
        purpose: "Snowflake CIS benchmark checks — read-only API calls (ACCOUNT_USAGE views)"
        auth: true
        optional: true
    telemetry: false
    persistence: false
    privilege_escalation: false
    always: false
    autonomous_invocation: restricted
---
# agent-bom-compliance — 人工智能合规性与政策引擎

该工具用于评估人工智能（AI）基础设施扫描结果是否符合安全框架的要求，并执行基于代码（policy-as-code）的政策规则。同时，它能够生成符合标准格式的安全物料清单（Security Bill of Materials, SBOM）。

## 安装

```bash
pipx install agent-bom
agent-bom compliance        # run compliance check on latest scan
agent-bom generate-sbom     # generate CycloneDX SBOM
```

## 工具（4个）

| 工具 | 描述 |
|------|-------------|
| `compliance` | 支持OWASP LLM/Agentic Top 10、欧盟AI法案（EU AI Act）、MITRE ATLAS、NIST AI RMF等安全标准 |
| `policy_check` | 根据自定义的安全策略（包含17项检查条件）评估扫描结果 |
| `cis_benchmark` | 对云账户执行CIS基准测试 |
| `generate_sbom` | 生成符合CycloneDX或SPDX格式的安全物料清单（SBOM） |

## 支持的安全框架

- **OWASP LLM Top 10**（2025）：检测提示注入（prompt injection）、供应链攻击（supply chain attacks）、数据泄露（data leakage）等问题 |
- **OWASP Agentic Top 10**：检测工具篡改（tool poisoning）、恶意撤资（rug pulls）、凭证窃取（credential theft）等行为 |
- **MITRE ATLAS**：用于评估对抗性机器学习（adversarial ML）威胁 |
- **欧盟AI法案**：涵盖风险分类（risk classification）、透明度要求（transparency requirements）以及安全物料清单的生成（SBOM generation） |
- **NIST AI RMF**：提供AI基础设施的治理、映射、测量和管理（governance, mapping, management）机制 |
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

## 隐私与数据保护

- **OWASP、NIST、欧盟AI法案、MITRE ATLAS以及安全物料清单（SBOM）的生成**：所有操作均在内存中的扫描数据上进行，无需进行网络请求或输入任何凭证。 |
- **CIS基准测试**（可选，由用户发起）：使用本地配置的凭证调用云服务提供商的API；这些API仅用于读取数据，不会存储或传输任何数据。在调用任何云API之前，必须明确执行`cis_benchmark(provider=...)`命令并确认相关设置。 |

## 验证信息

- **项目来源**：[github.com/msaad00/agent-bom](https://github.com/msaad00/agent-bom)（基于Apache-2.0许可证） |
- **包含6,040多项测试**，使用CodeQL和OpenSSF评分系统进行评估 |
- **无数据追踪或分析**：该工具完全不收集或分析用户数据。
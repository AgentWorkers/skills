---
name: terraform-ai-skills
description: >
  **使用场景：**  
  适用于大规模批量管理 Terraform 模块的场景，例如：  
  - 在 AWS、GCP、Azure 或 DigitalOcean 仓库中统一升级相关提供者（providers）；  
  - 标准化 GitHub Actions 工作流程；  
  - 自动化模块的版本发布（semantic releases）；  
  - 运行安全扫描；  
  - 对 10 个到 200 个以上的模块仓库执行端到端的维护操作。
version: 0.0.2
metadata:
  openclaw:
    requires:
      bins:
        - terraform
        - git
        - bash
      bins_optional:
        - gh
        - tflint
        - tfsec
        - trivy
        - checkov
    os:
      - linux
      - macos
    homepage: https://github.com/anmolnagpal/terraform-ai-skills
    tags:
      - terraform
      - multi-cloud
      - aws
      - gcp
      - azure
      - digitalocean
      - infrastructure-as-code
      - devops
      - automation
      - ci-cd
      - github-copilot
    license: MIT
    author: Anmol Nagpal
---
# Terraform AI Skills — 多云模块管理

这款AI驱动的工具可帮助您在AWS、GCP、Azure和DigitalOcean等平台上大规模管理Terraform模块，将原本需要56小时的手动维护工作缩短至90分钟。

## 使用场景

**在以下情况下使用此工具：**
- 需要在10到200多个模块仓库中统一升级Terraform提供商版本；
- 需要在整个组织内标准化GitHub Actions工作流程；
- 需要创建带有自动变更日志的语义化版本发布；
- 需要执行批量验证（使用TFLint、TFSec、Trivy或Checkov工具）；
- 需要完成完整的端到端维护周期。

**不适用场景：**
- 单个Terraform项目的维护；
- 编写单独的Terraform配置文件；
- 与特定提供商相关的API问题。

## 可用功能

### 全面维护 ⚡ _（推荐）_
```
@copilot use terraform-ai-skills/config/aws.config and follow terraform-ai-skills/prompts/4-full-maintenance.prompt
```
- 模块发现 → 提供商版本升级 → 工作流程修复 → 验证 → 发布  
**耗时：** 45–180分钟

### 提供商版本升级 🔄
```
@copilot use terraform-ai-skills/config/aws.config and follow terraform-ai-skills/prompts/1-provider-upgrade.prompt
```
- 更新提供商限制、Terraform版本及示例代码；执行验证。  
**耗时：** 10–90分钟

### 工作流程标准化 🔧
```
@copilot use terraform-ai-skills/config/gcp.config and follow terraform-ai-skills/prompts/2-workflow-standardization.prompt
```
- 将GitHub Actions绑定到特定的SHA值；移除过时的操作。  
**耗时：** 15–30分钟

### 发布创建 🚀
```
@copilot use terraform-ai-skills/config/azure.config and follow terraform-ai-skills/prompts/3-release-creation.prompt
```
- 生成变更日志、语义化版本标签，并在GitHub上发布模块。  
**耗时：** 10–20分钟

## 快速入门

```bash
# 1. Always test on ONE repo first
@copilot use terraform-ai-skills/config/aws.config and upgrade provider in terraform-aws-vpc only

# 2. If successful, run full maintenance
@copilot use terraform-ai-skills/config/aws.config and follow terraform-ai-skills/prompts/4-full-maintenance.prompt

# 3. Verify
git status && gh run list && gh release list
```

## 支持的云提供商

| 提供商           | 配置文件                         | Terraform版本要求 | 最低Terraform版本要求 |
|-------------------|----------------------------------|-------------------------|-------------------|
| AWS             | `config/aws.config`                     | 1.10.0+                    | 5.80.0+                |
| GCP             | `config/gcp.config`                     | 1.10.0+                    | 6.20.0+                |
| Azure            | `config/azure.config`                     | 1.10.0+                    | 4.20.0+                |
| DigitalOcean      | `config/digitalocean.config`                 | 1.10.0+                    | 2.70.0+                |

## 实际效果

| 操作                | 手动操作（170个仓库） | 使用该工具后 | 节省时间（百分比） |
|------------------|------------------|------------------|----------------------|
| 提供商版本升级       | 56小时                        | 90分钟        | 97%                 |
| 工作流程修复        | 20小时                        | 30分钟        | 97%                 |
| 全面维护          | 86小时                        | 2–3小时        | 97%                 |

## 系统要求

- **Terraform** 版本：1.10.0及以上  
- **Git** 版本：2.30及以上  
- **Bash** 版本：4.0及以上  
- **AI辅助工具**：GitHub Copilot CLI、Claude、ChatGPT或Cursor  
- `gh` CLI（推荐用于发布操作）  
- TFLint / TFSec / Trivy / Checkov（可选，用于增强验证功能）  

## 详细参考指南

如需深入了解具体功能，请参阅以下文档：  
- **[提供商配置](references/provider-configs.md)**：针对不同云平台的配置选项、自定义设置及环境变量  
- **[安全与回滚](references/safety.md)**：部署前的检查清单、回滚流程及紧急恢复措施  
- **[实际应用案例](references/examples.md)**：在AWS、GCP、Azure和DigitalOcean上的应用实例  
- **[快速参考](references/quick-reference.md)**：命令速查表、提示指南及常见使用模式  

## 许可证

MIT © 2026 Anmol Nagpal
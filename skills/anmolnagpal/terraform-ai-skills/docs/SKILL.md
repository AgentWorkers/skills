---
name: terraform-ai-skills
description: GitHub Copilot的多云Terraform模块管理功能：自动化AWS、GCP、Azure和DigitalOcean模块的提供程序升级、测试、持续集成/持续交付（CI/CD）以及大规模发布流程。
license: MIT
metadata:
  author: CloudDrove
  version: 0.0.1
  keywords:
    - terraform
    - github-copilot
    - automation
    - aws
    - gcp
    - azure
    - digitalocean
    - infrastructure-as-code
    - devops
    - multi-cloud
---
# Terraform Copilot：多云模块管理工具

Terraform Copilot 是一套基于 GitHub Copilot 的自动化工具，专为在 AWS、GCP、Azure 和 DigitalOcean 等多云环境中大规模管理 Terraform 模块而设计。它能够自动化执行提供商升级、GitHub Actions 工作流、代码发布以及代码验证等操作，适用于数百个仓库。

## 适用场景

**适用情况：**
- 管理多个 Terraform 模块仓库（10 至 200 个以上模块）
- 在整个组织范围内统一更新 Terraform 提供商版本
- 标准化 GitHub Actions 工作流
- 自动生成变更日志并发布版本
- 执行批量维护操作
- 对大量 Terraform 代码进行统一验证
- 为基础设施模块设置持续集成/持续部署（CI/CD）流程

**不适用场景：**
- 单个 Terraform 项目的维护（效率较低）
- 编写单个 Terraform 配置文件（请使用 `terraform-skill` 工具）
- 与特定云平台相关的资源配置问题（请参考官方文档）

## 核心原则

### 1. 多云支持（Multi-Cloud First）

支持四种主要云平台，并提供针对每种云平台的定制配置：

| 提供商 | 模块数量 | 组织结构 | 配置文件 |
|--------|------------|----------------|-----------|
| AWS    | 约 170      | clouddrive/terraform-aws-*   | `config/aws.config` |
| GCP    | 多个        | clouddrive/terraform-gcp-*   | `config/gcp.config` |
| Azure    | 多个        | terraform-az-modules/terraform-azurerm-* | `config/azure.config` |
| DigitalOcean | 多个        | terraform-do-modules/terraform-digitalocean-* | `config/digitalocean.config` |

所有配置均基于 **Terraform 1.10.0** 及更高版本，并使用最新的供应商插件。

### 2. 安全至上（Safety First）

- **内置安全机制：**
  - 首先在单个仓库上进行测试
  - 执行批量操作前进行预检
  - 提供回滚机制以应对错误
  - 排除关键仓库，避免自动化操作影响它们
  - 支持模拟执行（Dry-run）
  - 每个步骤都包含全面的验证流程

### 3. 大规模操作中的时间节省

| 操作类型 | 手动操作（170 个仓库） | 使用 Copilot | 时间节省百分比 |
|---------|-------------------|------------------|-------------|
| 提供商升级 | 56 小时 | 90 分钟 | 97%         |
| 工作流修复 | 20 小时 | 30 分钟 | 97%         |
| 版本发布 | 10 小时 | 15 分钟 | 97%         |
| 全面维护 | 86 小时 | 2–3 小时 | 97%         |

## 可用功能

### 1. 提供商升级 🔄

- 自动更新所有模块和示例代码中的供应商版本。

**功能说明：**
- 更新供应商版本要求
- 更新 Terraform 的版本依赖
- 重新生成所有配置文件
- 运行验证和格式化操作
- 生成标准化的提交记录

**所需时间：** 10–90 分钟（取决于项目规模）

### 2. 工作流标准化 🔧

- 在所有仓库中统一 GitHub Actions 工作流。

**功能说明：**
- 将工作流绑定到特定的 SHA 值
- 更新工作流配置
- 删除过时的工作流
- 确保所有验证步骤都能通过

**所需时间：** 15–30 分钟

### 3. 版本发布 🚀

- 生成带有变更日志的版本发布记录。

**功能说明：**
- 从提交记录中生成变更日志
- 为版本添加语义化标签
- 在 GitHub 上发布版本
- 更新相关文档

**所需时间：** 10–20 分钟

### 4. 全面维护 ⚡（推荐）

- 结合以上所有功能，完成端到端的维护流程。

**功能说明：**
- 发现并审计问题
- 升级供应商和 Terraform 配置
- 标准化工作流
- 进行全面验证
- 更新文档
- 创建版本发布记录
- 提供汇总报告

**所需时间：** 45–180 分钟（取决于项目规模）

## 快速入门

### 第一步：选择云平台

根据您的需求，选择相应的配置文件。

### 第二步：在单个仓库上测试

**建议在正式应用之前，先在单个仓库上进行测试。**

### 第三步：执行全面维护

测试通过后，即可开始全面维护操作。

### 第四步：验证与监控

维护完成后，需对结果进行验证和监控。

## 目录结构

## 配置管理

每种云平台都有其专属的配置文件，其中包含默认设置：

- **AWS**：`config/aws.config`
- **GCP**：`config/gcp.config`
- **Azure**：`config/azure.config`
- **DigitalOcean**：`config/digitalocean.config`

### 定制化指南

1. **克隆或复制此仓库**
2. **根据您的组织需求更新配置文件**
3. **调整排除规则，避免影响关键仓库**
4. **根据需要修改验证规则**
5. **先在非生产环境中进行测试**

详细定制指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全特性

### 预检流程

在执行批量操作前，请务必：
- 完整阅读 [SAFETY.md](docs/SAFETY.md)
- 在单个仓库上进行测试
- 使用 `git diff` 核对更改内容
- 确保被排除的仓库确实未被自动化操作影响
- 准备好回滚方案
- 选择低流量时段进行操作

### 内置安全机制

- **排除关键仓库**：防止关键仓库被自动化操作影响
- **验证工具**：`terraform validate`、`terraform fmt`、`TFLint`、`TFSec`
- **模拟执行**：允许预览更改而不实际应用
- **回滚机制**：提供详细的恢复流程
- **检查点**：在重大更改前创建备份

### 回滚流程

如遇问题，请参考 [SAFETY.md] 中的指南：
- 如何撤销提交
- 如何删除已发布的版本
- 如何处理部分失败的情况
- 如何联系技术支持

## 版本管理

**当前版本：0.0.1**
- **发布日期：** 2026-02-06
- **状态：** 已准备好投入生产使用 ✅

### 新功能

- **多云支持（AWS、GCP、Azure、DigitalOcean）**
- **要求使用 Terraform 1.10.0 及更高版本**
- **所有云平台均使用最新供应商版本**
- **提供详细的文档（10 个文件，共 2,656 行）**
- **加强安全措施**
- **新增供应商选择指南**
- **版本历史记录**

完整的功能变更日志和兼容性矩阵请参阅 [VERSION.md](docs/VERSION.md)。

## 文档说明

### 快速导航

| 文档 | 用途 | 阅读时间 |
|---------|---------|-----------|
| **[INDEX.md](docs/INDEX.md)** | 完整的导航指南 | 5 分钟 |
| **[DISTRIBUTION.md](docs/DISTRIBUTION.md)** | 分发策略概述 | 10 分钟 |
| **[QUICKREF.md](docs/QUICKREF.md)** | 快速参考 | 2 分钟 |
| **[SAFETY.md](docs/SAFETY.md)** | 安全性与回滚指南 | 10 分钟（务必阅读） |
| **[USAGE.md](docs/USAGE.md)** | 使用指南 | 15 分钟 |
| **[EXAMPLES.md](docs/EXAMPLES.md)** | 实际使用案例 | 10 分钟 |
| **[PROVIDER-SELECTION.md](docs/PROVIDER-SELECTION.md)** | 提供商选择指南 | 5 分钟 |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | 定制化指南 | 15 分钟 |
| **[ENV-VARS.md](docs/ENV-VARS.md)** | 变量参考 | 5 分钟 |
| **[VERSION.md](docs/VERSION.md)** | 版本历史 | 3 分钟 |

**整体上手时间：** 约 2 小时（包括实践操作）

## 实际应用效果

### CloudDrove 案例研究

- **使用前：** 每次维护周期耗时 8–10 小时，人为错误频发（3–5 次），代码一致性较低（60–70%），仓库配置差异较大。
- **使用后：** 每次维护周期耗时 45–90 分钟，人为错误几乎为零（完全自动化），代码一致性达到 100%，仓库配置差异消失。
- **投资回报：** 每名工程师每月可节省 30–40 小时，错误率降低 95% 以上，回报周期小于 1 周，每年节省 360–480 小时。

## 系统要求

- **需要安装 GitHub Copilot CLI 或兼容的 AI 辅助工具**
- **Terraform 版本需达到 1.10.0 或更高**
- **Git 版本需达到 2.30 或更高**
- **Bash 版本需达到 4.0 或更高**
- **gh CLI（可选，用于增强与 GitHub 的集成）**

### 可选工具

- **TFLint**：Terraform 代码格式检查工具
- **TFSec**：安全扫描工具
- **Trivy**：漏洞扫描工具
- **Checkov**：代码合规性检查工具
- **terraform-docs**：代码生成工具

## 贡献方式

我们欢迎您的贡献！请参阅 [CONTRIBUTING.md] 以了解：
- 如何添加新功能
- 定制化指南
- 测试流程
- 代码风格规范
- 提交流程

### 贡献方式示例：

1. **报告问题**：发现 bug？[请在此提交问题](https://github.com/anmolnagpal/terraform-ai-skills/issues)
2. **提出建议**：有新功能需求？[请在此讨论](https://github.com/anmolnagpal/terraform-ai-skills/discussions)
3. **添加新的云平台支持**：希望支持新的云平台？[请提交 Pull Request！]
4. **改进文档**：发现文档不清晰？请帮忙改进！

## 与其他工具的比较

| 对比项 | 手动维护 | Copilot Skills |
|--------|--------|----------------|
| 时间（170 个仓库） | 56 小时 | 90 分钟 |
| 错误率 | 每次 3–5 个 | 几乎为零 |
| 代码一致性 | 60–70% | 100% |
| 文档更新 | 经常过时 | 始终保持最新 |
| 回滚流程 | 需手动操作 | 有详细的文档指导 |

### 与其他自动化工具的比较

| 功能 | Copilot Skills | 自定义脚本 | Atlantis | Terraform Cloud |
|--------|----------------|----------------|----------------|----------|-----------------|
| 多云支持 | 支持 | 需手动配置 | 支持（但配置复杂） | 支持 |
| 成本 | 免费 | 免费 | 免费 | 有付费选项 |
| 配置难度 | 30 分钟内完成 | 需数小时至数天 | 需数小时 | 需数小时 |
| 定制化程度 | 高度可定制 | 高度可定制 | 有限 | 有限 |
| AI 辅助 | 支持 | 不支持 | 不支持 | 部分支持 |
| 安全性 | 内置安全机制 | 需手动检查 | 需手动检查 | 部分支持 |

## 许可证

本工具采用 MIT 许可证，详细信息请参阅 [LICENSE](LICENSE)。

**版权所有 © 2026 CloudDrove**

欢迎免费使用、修改和分发。如需署名，请随时告知，但非强制要求。

## 技术支持

- **文档参考：** 查阅 [INDEX.md] 以获取使用指南
- **示例代码：** 查看 [EXAMPLES.md] 了解实际应用案例
- **问题反馈：** [通过 GitHub Issues](https://github.com/anmolnagpal/terraform-ai-skills/issues) 报告问题
- **技术支持：** [通过 GitHub Discussions](https://github.com/anmolnagpal/terraform-ai-skills/discussions) 寻求帮助
- **安全指南：** 阅读 [SAFETY.md] 了解安全相关内容

## 社区资源

- **Twitter：** [@anmolnagpal](https://twitter.com/clouddrove)
- **LinkedIn：** [CloudDrove](https://www.linkedin.com/company/clouddrove)
- **官方网站：** [github.com/anmolnagpal](https://github.com/anmolnagpal)
- **博客：** [blog.github.com/anmolnagpal](https://blog.github.com/anmolnagpal)

## 致谢

本工具的开发灵感来源于：
- **[antonbabenko/terraform-skill](https://github.com/antonbabenko/terraform-skill)**：Claude 工具中的 Terraform 最佳实践功能
- **[terraform-best-practices.com](https://www.terraform-best-practices.com)**：Terraform 最佳实践指南
- **[terraform-aws-modules](https://github.com/terraform-aws-modules)**：高质量的 AWS 模块库

特别感谢 Terraform 和 GitHub Copilot 社区的大力支持。

## 相关项目

- **[pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform)**：预提交钩子工具
- **[terraform-docs](https://terraform-docs.io/)**：代码生成工具
- **[terratest](https://terratest.gruntwork.io/)**：测试框架
- **[infracost](https://www.infracost.io/)**：成本估算工具
- **[atlantis](https://www.runatlantis.io/)**：Terraform 自动化工具

---

**想要每年节省数百小时的工作时间吗？** 请先阅读 [DISTRIBUTION.md] 以获取完整的设置指南。

**有任何疑问？** 请查阅 [INDEX.md] 或 [在此提交问题](https://github.com/anmolnagpal/terraform-ai-skills/issues)。

**状态：** 已准备好投入生产使用 ✅ | **版本：** 0.0.1 | **许可证：** MIT 许可证
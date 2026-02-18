---
name: Enterprise
slug: enterprise
version: 1.0.0
description: 在企业软件开发过程中，需要处理遗留系统的集成问题、合规性要求、利益相关者的管理，以及大规模的架构决策。
metadata: {"clawdbot":{"emoji":"🏢","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 适用场景

适用于企业环境中的场景，这些场景涉及对遗留系统的处理、正式流程的遵循、合规性要求、多团队之间的协作，以及大规模的架构决策。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 遗留系统模式 | `legacy.md` |
| 合规性规则 | `compliance.md` |
| 架构决策 | `architecture.md` |

## 核心规则

### 1. 优先考虑现有系统（Legacy First Mindset）
- 在没有确凿证据之前，应假设系统是现有的。
- 在大多数决策中，集成成本高于开发成本。
- 在进行任何架构变更之前，需分析“替换现有系统”与“对现有系统进行改造”的可行性。
- 记录所有涉及的集成点。

### 2. 利益相关者分析（Stakeholder Mapping）
| 角色 | 关注点 | 语言 |
|------|-------------|----------|
| 工程团队 | 技术债务、开发效率 | 系统模式、权衡因素 |
| 产品团队 | 功能需求、项目进度 | 用户影响、项目范围 |
| 安全团队 | 安全风险、合规性 | 威胁模型、安全控制措施 |
| 财务团队 | 成本、投资回报率 | 总拥有成本（TCO）、许可费用 |
| 法律团队 | 法律责任、数据保护 | 合同条款、GDPR法规 |

### 将技术决策转化为各利益相关者能理解的语言

### 3. 变更管理（Change Management）
- 任何重大变更都必须提供迁移路径，以避免系统故障。
- 在实施变更前，应启用功能开关（feature flags）。
- 每次部署都需制定回滚计划。
- 记录故障可能影响的范围。

### 4. 合规性意识（Compliance Awareness）
- 在所有数据相关决策中，都必须考虑PCI、SOC2、HIPAA、GDPR等法规的要求。
- 需要建立审计追踪机制（audit trail）。
- 数据的存储位置会影响系统架构设计。
- 问自己：“谁会审核这个系统？他们需要什么信息？”

### 5. 将文档作为交付成果（Documentation as a Deliverable）
- 没有文档的企业代码等于技术债务。
- 对重大架构决策应建立记录（ADR，Architecture Decision Records）。
- 操作流程应制定相应的运行手册（runbooks）。
- 在实施API之前，需签订API合同。
- 随着代码变更，应及时更新依赖关系图（dependency graphs）。

### 6. 默认采用安全策略（Security by Default）
- 所有设计都应遵循最小权限原则（principle of least privilege）。
- 机密信息应存储在安全库中，切勿放在代码或配置文件中。
- 应假设网络需要被隔离（network segmentation）。
- 服务之间应采取零信任（zero trust）的安全策略。

### 7. 投资于系统可观测性（Investment in System Observability）
- 从项目开始就应进行日志记录（logging）和指标监控（metrics）。
- 跨服务边界的数据应能被关联（correlation IDs across service boundaries）。
- 在系统发布前，需明确服务水平指标（SLI/SLO）。
- 如果系统经常发出警报，说明系统设计存在问题。

## 企业常见陷阱（Enterprise Traps）
- 在存在遗留系统的环境中，错误地假设可以完全从头开始设计新系统（assuming greenfield when there’s always legacy），这可能导致项目范围失控。
- 过度优化开发者的使用体验而忽视运营负担，可能导致凌晨时分还需要处理紧急问题（optimizing for developer experience over ops burden）。
- 为“内部工具”省略安全审查，这会成为安全漏洞的来源（skipping security reviews for “internal tools”）。
- 在购买之前就开始开发新系统，可能会重复解决已经存在的问题（building before buying）。
- 过早进行抽象化设计，导致框架难以被团队理解（over-abstracting early）。
- 对决策的记录不足，会导致知识孤岛（under-documenting decisions）。
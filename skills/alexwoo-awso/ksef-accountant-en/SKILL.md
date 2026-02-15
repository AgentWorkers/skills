---
name: ksef-accountant-en
description: "**国家电子发票系统（KSeF）会计助理**  
适用于使用 KSeF 2.0 API、FA(3) 发票、波兰增值税合规性要求、电子发票处理、支付匹配、增值税登记册（JPK_V7）、更正发票、分期支付机制（MPP）以及波兰会计工作流程的场景。具备在 KSeF 生态系统中处理发票开具、采购流程、费用分类、欺诈检测和现金流预测等方面的专业领域知识。"
license: MIT
homepage: https://github.com/alexwoo-awso/skills
source: https://github.com/alexwoo-awso/skills/tree/main/ksef-accountant-en
disableModelInvocation: true
disable-model-invocation: true
allowModelInvocation: false
instruction_only: true
has_executable_code: false
credential_scope: "optional-user-provided"
env:
  KSEF_TOKEN:
    description: "KSeF API token for session authentication. Provided by the user — the skill does not generate, store or transmit tokens. Configure ONLY after verifying that the platform enforces the disableModelInvocation flag (see Security Model section and skill.json)."
    required: false
    secret: true
  KSEF_ENCRYPTION_KEY:
    description: "Fernet encryption key for secure token storage. Usage is optional — an example of a security pattern described in the reference documentation. Configure ONLY after verifying that the platform enforces the disableModelInvocation flag."
    required: false
    secret: true
  KSEF_BASE_URL:
    description: "KSeF API base URL. Defaults to https://ksef-demo.mf.gov.pl (DEMO). Production: https://ksef.mf.gov.pl — requires explicit user consent. Use production ONLY after full platform security verification."
    required: false
    default: "https://ksef-demo.mf.gov.pl"
---

# KSeF会计代理

该技能专门用于在KSeF 2.0环境中操作国家电子发票系统（KSeF），支持与波兰电子发票相关的会计任务。

## 安全模型

此技能仅提供指导性内容——它包含Markdown文件，其中包含领域知识、架构模式和代码示例。文件中不包含任何可执行代码、二进制文件、安装脚本或运行时依赖项。

**技能相关保证：**
- `disableModelInvocation: true` — 该设置既在文档的前置元数据中（采用camelCase和kebab-case两种格式）也在专门的`skill.json`文件中明确声明。该技能不应被模型自动调用。
- `secret: true` — 环境变量`KSEF_TOKEN`和`KSEF_ENCRYPTION_KEY`被标记为机密信息，平台应确保这些变量不被记录或显示。
- 无可执行代码——所有示例（Python、XML、JSON）仅用于说明目的，不会被技能本身执行。
- 无需安装——该技能不会在磁盘上写入文件，不会下载依赖项，也不会修改系统配置。
- 有专门的`skill.json`文件——其中包含安全元数据、环境变量声明和限制。如果平台无法正确解析SKILL.md文件的前置内容，应从`skill.json`中读取元数据。

**注意——安装前的注册表元数据验证：**

安全标志在两个地方声明：SKILL.md文件的前置内容和`skill.json`文件。然而，托管平台可能不会读取或强制执行这些标志。**安装前必须执行以下步骤：**
1. **检查注册表元数据**——将技能添加到平台后，查看平台显示的注册表元数据。确认`disable-model-invocation`字段设置为`true`，并且环境变量`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`、`KSEF_BASE_URL`被标记为机密信息。如果平台显示这些字段未设置或设置为`false`，则表示这些标志未被强制执行。
2. **如果注册表元数据与前置内容/`skill.json`不一致**——将此技能视为高风险技能：不要提供任何凭证（令牌、证书、密钥），不要配置环境变量（`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`），也不要允许其自动使用。
3. **验证环境变量的隔离性**——确认平台能够隔离这些环境变量，并且不会在对话中显示它们的值。
4. **如果平台不强制执行这些标志**——请联系平台提供商以启用`disableModelInvocation`的支持（或修改`skill.json`的解析方式），否则不要安装该技能。

**平台相关保证：**
- `disableModelInvocation`标志的强制执行取决于托管平台。仅靠前置内容无法提供保护——需要平台的支持。
- 环境变量的隔离性也取决于平台。该技能将这些变量声明为可选，但不控制平台如何存储和显示它们。
- 如果平台不强制执行这些设置，应将此技能视为高风险技能，并且不要为其提供凭证或生产环境访问权限。

## 限制条件
- **仅提供知识——不执行代码**——该技能提供领域知识、架构模式和指导。所有代码示例（包括机器学习/人工智能相关内容）仅用于教学和说明目的。该技能不会运行机器学习模型，不会进行推理，也不需要Python或sklearn运行时环境或任何二进制文件。它仅解释算法并为用户提供实现代码的建议。
- **不提供法律或税务建议**——信息内容基于编写时的知识状态，可能会过时。在实施前，请务必咨询税务顾问。
- **人工智能提供辅助，但不做决策**——关于人工智能功能的描述（如费用分类、欺诈检测、现金流预测）仅作为参考架构和实现模式。该技能提供算法相关知识，并帮助编写代码，但不负责做出具有法律或财务约束力的决策。
- **需要用户确认**——在执行任何可能产生财务后果的操作之前（如阻止支付、向KSeF发送发票、修改会计记录等），必须获得用户的明确同意。
- **用户管理凭证**——KSeF API令牌、证书和加密密钥必须通过环境变量（在元数据中声明：`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`、`KSEF_BASE_URL`）或秘密管理工具由用户提供。该技能永远不会存储、生成或传输凭证。**切勿在对话中直接输入凭证（令牌、密钥、证书）**——请使用环境变量或平台的秘密管理工具。参考文档中的Vault/Fernet使用示例仅作为用户实现的架构参考。
- **使用DEMO环境进行测试**——生产环境（`https://ksef.mf.gov.pl`）会生成具有法律约束力的发票。请使用DEMO环境（`https://ksef-demo.mf.gov.pl`）进行开发和测试。
- **禁止自动调用**——该技能在前置元数据和`skill.json`文件中都设置了`disableModelInvocation: true`。这意味着模型不应自动调用该技能——需要用户的明确操作。**注意：**前置内容和`skill.json`中的声明仅表示建议，实际执行情况取决于平台。使用前请确认平台显示的注册表元数据中也显示`disable-model-invocation: true`。如果平台显示这些字段未设置或设置为`false`，则表示该标志未被强制执行。

## 安装前的检查清单

在安装技能并配置环境变量之前，请执行以下步骤：
- [ ] 验证平台注册表元数据——`disable-model-invocation`字段必须设置为`true`。
- [ ] 确认平台已从前置内容或`skill.json`文件中读取环境变量声明——环境变量`KSEF_TOKEN`和`KSEF_ENCRYPTION_KEY`应被标记为机密信息（`secret: true`）。
- [ ] 确认平台能够隔离环境变量（不会在对话中显示或记录它们的值）。
- [ ] 在任何生产环境使用之前，仅使用DEMO环境（`https://ksef-demo.mf.gov.pl`）测试该技能。
- [ ] **切勿在对话中直接输入凭证、密钥或证书**——请使用环境变量或秘密管理工具。
- [ ] 如果注册表元数据与前置内容/`skill.json`不一致——请不要配置凭证，并将问题报告给平台提供商。

## 核心能力

### 1. KSeF 2.0 API操作
- 发送FA(3)格式的发票
- 下载采购发票
- 管理会话/令牌
- 处理Offline24模式（紧急情况）
- 下载UPO（正式收据确认）

相关API端点：
```http
POST /api/online/Session/InitToken     # Session initialization
POST /api/online/Invoice/Send          # Send invoice
GET  /api/online/Invoice/Status/{ref}  # Check status
POST /api/online/Query/Invoice/Sync    # Query purchase invoices
```

请参阅[references/ksef-api-reference.md](references/ksef-api-reference.md)——完整的API文档，包括认证信息、错误代码和速率限制。

### 2. FA(3)格式
- FA(3)与FA(2)的区别：发票附件、员工/承包商类型、扩展的银行账户格式、每条记录50,000行的修改限制、JST和VAT组标识符。

请参阅[references/ksef-fa3-examples.md](references/ksef-fa3-examples.md)——XML示例（基本发票、多种VAT税率、修改、MPP、Offline24模式、附件）。

### 3. 会计工作流程
- **销售**：数据 -> 生成FA(3)格式发票 -> 发送至KSeF -> 获取KSeF编号 -> 记账
  `借方300（应收账款）| 贷方700（销售收入）+ 贷方220（输出增值税）`
- **采购**：查询KSeF -> 下载XML文件 -> 通过AI进行分类 -> 记账
  `借方400-500（费用）+ 贷方221（增值税）| 贷方201（应付账款）`

请参阅[references/ksef-accounting-workflows.md](references/ksef-accounting-workflows.md)——详细的会计工作流程，包括支付匹配、MPP、修改、增值税登记和月末结算。

### 4. 人工智能辅助功能（参考架构）
以下是实现模式和参考架构。该技能不运行机器学习模型——它提供算法相关知识，帮助设计流程并编写用户系统的实现代码。参考文件中的代码示例（Python、sklearn、pandas）仅用于说明目的——技能本身不包含训练好的模型、机器学习成果或可执行文件。
- **费用分类**：基于承包商历史数据和关键词匹配的机器学习模型（随机森林）。如果置信度低于0.8，则标记为需要审核。
- **欺诈检测**：使用隔离森林模型检测金额异常，对钓鱼发票进行评分，使用图分析检测增值税相关欺诈行为。
- **现金流预测**：基于承包商历史数据、金额和季节性模式的随机森林回归模型。

请参阅[references/ksef-ai-features.md](references/ksef-ai-features.md)——概念性算法和实现模式（需要sklearn和pandas库，但这些不是技能的依赖项）。

### 5. 合规性和安全性（实现模式）
以下是在用户系统中推荐的 security 模式。该技能提供相关知识和代码示例，但不会自行实现这些机制。
- 支付前的VAT白名单验证
- 加密令牌存储（使用Fernet/Vault等技术，供用户自行实现）
- 所有操作的审计跟踪
- 3-2-1备份策略
- 遵守GDPR法规（保留期后的数据匿名化）
- 基于角色的访问控制（RBAC）

请参阅[references/ksef-security-compliance.md](references/ksef-security-compliance.md)——实现模式和安全检查清单。

### 6. 更正发票
- 从KSeF下载原始发票 -> 创建FA(3)格式的更正文件 -> 将更正文件链接到原始发票编号 -> 发送至KSeF -> 记账以完成撤销或差额调整。

### 7. VAT登记和JPK_V7文件
- 生成销售/采购登记文件（Excel/PDF格式），以及JPK_V7M（每月一次）和JPK_V7K（每季度一次）文件。

## 故障排除 - 快速帮助
| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| 发票被拒绝（代码400/422）| XML格式无效、NIP错误、日期错误、字段缺失 | 检查UTF-8编码，验证FA(3)格式，确认NIP的有效性 |
| API超时 | KSeF系统故障、网络问题或高峰时段 | 检查KSeF系统状态，尝试使用指数退避策略重试 |
| 无法匹配支付信息 | 金额不一致、数据缺失或支付分割 | 扩展搜索范围（±2%、±14天），检查MPP规则 |

请参阅[references/ksef-troubleshooting.md](references/ksef-troubleshooting.md)——完整的故障排除指南。

## 参考文件
根据需要加载以下文件：
- [skill.json](skill.json)：元数据文件，包含安全标志、环境变量声明和限制信息。这是注册表和扫描工具的权威信息来源。
- [ksef-api-reference.md](references/ksef-api-reference.md)：KSeF API端点、认证流程和发票发送/下载方法。
- [ksef-legal-status.md](references/ksef-legal-status.md)：KSeF系统的实施日期、法律要求和处罚规定。
- [ksef-fa3-examples.md](references/ksef-fa3-examples.md)：FA(3)格式发票的创建和验证方法。
- [ksef-accounting-workflows.md](references/ksef-accounting-workflows.md)：会计记录处理、支付匹配、MPP规则、更正操作和增值税登记。
- [ksef-ai-features.md](references/ksef-ai-features.md)：费用分类、欺诈检测和现金流预测算法。
- [ksef-security-compliance.md](references/ksef-security-compliance.md)：VAT白名单、令牌安全、审计跟踪和GDPR合规性要求。
- [ksef-troubleshooting.md](references/ksef-troubleshooting.md)：API错误、验证问题和性能优化建议。

## 官方资源
- KSeF门户：https://ksef.podatki.gov.pl
- KSeF演示环境：https://ksef-demo.mf.gov.pl
- KSeF生产环境：https://ksef.mf.gov.pl
- VAT白名单API：https://wl-api.mf.gov.pl
- KSeF Latarnia项目（状态更新）：https://github.com/CIRFMF/ksef-latarnia
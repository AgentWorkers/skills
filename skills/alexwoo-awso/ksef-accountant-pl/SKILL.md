---
name: ksef-accountant-pl
description: "**Krajowego Systemu e-Faktur (KSeF) 的会计助理（波兰语版本）**  
在使用 KSeF 2.0 时，您需要掌握以下技能：  
1. 应用 API 进行相关操作；  
2. 熟悉 FA(3) 类型的电子发票及其与波兰增值税（VAT）法规的关联；  
3. 熟练处理电子发票的流转流程；  
4. 能够调整付款方式；  
5. 理解 VAT 登记系统（JPK_V7）的运作原理；  
6. 掌握修正性发票的处理方法；  
7. 熟悉分期付款（MPP）机制；  
8. 熟悉波兰的会计流程。  
此外，您还需要具备以下专业能力：  
- 了解发票开具的相关知识；  
- 熟练处理采购相关事务；  
- 能够对成本进行分类；  
- 具备识别欺诈行为的技能；  
- 能够在 KSeF 生态系统中预测现金流。"
license: MIT
homepage: https://github.com/alexwoo-awso/skills
source: https://github.com/alexwoo-awso/skills/tree/main/ksef-accountant-pl
disableModelInvocation: true
disable-model-invocation: true
allowModelInvocation: false
instruction_only: true
has_executable_code: false
credential_scope: "optional-user-provided"
env:
  KSEF_TOKEN:
    description: "Token API KSeF do uwierzytelniania sesji. Dostarczany przez uzytkownika — skill nie generuje, nie przechowuje ani nie przesyla tokenow. Konfiguruj TYLKO po zweryfikowaniu, ze platforma wymusza flage disableModelInvocation (patrz sekcja Model bezpieczenstwa i skill.json)."
    required: false
    secret: true
  KSEF_ENCRYPTION_KEY:
    description: "Klucz szyfrowania Fernet do bezpiecznego przechowywania tokenow. Uzycie opcjonalne — przyklad wzorca bezpieczenstwa opisanego w dokumentacji referencyjnej. Konfiguruj TYLKO po zweryfikowaniu, ze platforma wymusza flage disableModelInvocation."
    required: false
    secret: true
  KSEF_BASE_URL:
    description: "Bazowy URL API KSeF. Domyslnie https://ksef-demo.mf.gov.pl (DEMO). Produkcja: https://ksef.mf.gov.pl — wymaga jawnej zgody uzytkownika. Uzywaj produkcji TYLKO po pelnej weryfikacji bezpieczenstwa platformy."
    required: false
    default: "https://ksef-demo.mf.gov.pl"
---

# Agent Ksiegowy KSeF

该技能专注于在KSeF 2.0环境中使用国家电子发票系统（KSeF），遵循FA(3)架构。它支持与波兰电子发票相关的会计处理任务。

## 安全模型

此技能仅具有指导性，由Markdown文件组成，其中包含领域知识、架构模板和代码示例。它不包含任何可执行代码、二进制文件、安装脚本或运行时依赖项。

**技能的相关保证：**
- `disableModelInvocation: true` — 该设置同时在frontmatter元数据（camelCase和kebab-case格式）和专用的`skill.json`文件中声明。该技能不应被模型自动调用。
- `secret: true` — 环境变量`KSEF_TOKEN`和`KSEF_ENCRYPTION_KEY`在frontmatter和`skill.json`中被标记为机密信息，表明这些信息必须被隔离，不得被记录或显示。
- 无可执行代码 — 所有代码示例（Python、XML、JSON）仅用于说明目的，并非由技能本身执行。
- 无安装过程 — 该技能不会将文件写入磁盘，不会下载依赖项，也不会修改系统配置。
- 专用的`skill.json`文件 — 包含安全元数据、环境变量声明和限制信息。如果平台无法正确解析SKILL.md的frontmatter，应从`skill.json`中读取这些元数据。

**注意：安装前的注册表元数据验证**

安全标志在两个地方声明：SKILL.md的frontmatter和`skill.json`文件中。尽管如此，托管平台可能无法读取或强制应用这些标志。**在安装前必须执行以下步骤：**
1. **验证注册表元数据**：将技能添加到平台后，查看平台显示的注册表元数据。确认`disable-model-invocation`字段设置为`true`，并且环境变量`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`、`KSEF_BASE_URL`被标记为机密信息。如果平台显示这些字段为`not set`、`false`或未显示，则表示这些标志未被强制应用。
2. **如果注册表元数据与frontmatter/skill.json不一致**：将此技能视为高风险项：不要提供任何认证数据（令牌、证书、密钥），不要配置环境变量`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`，也不要允许其自动执行。
3. **确认环境变量的隔离**：确保平台能够隔离这些变量，并且在处理过程中不会记录或显示它们的值。
4. **如果平台不强制应用这些标志**：请联系平台提供商以启用`disableModelInvocation`功能（或解析`skill.json`），或者不要安装该技能，以免其访问任何认证数据。

**平台相关的保证：**
- 强制应用`disableModelInvocation`标志取决于托管平台。仅frontmatter本身无法提供保护，需要平台的支持。
- 环境变量（env vars）的隔离也取决于平台。该技能将这些变量声明为可选项，但不控制平台如何存储和访问它们。
- 如果平台不强制应用这些设置，请将此技能视为高风险项，不要向其提供任何认证数据。

## 限制

- **仅提供知识，不执行代码**：该技能提供领域知识、架构模板和指导建议。所有代码示例（包括机器学习/人工智能相关代码）仅用于教学和参考目的。该技能不会启动机器学习模型，不会执行推理，也不需要Python/sklearn运行时或任何二进制文件。它仅解释算法并建议用户如何实现代码。
- **非法律或税务咨询**：提供的信息基于当前的知识状态，可能会过时。在实施前，请务必咨询税务顾问。
- **人工智能提供辅助，但不做决策**：关于人工智能功能的描述（如成本分类、欺诈检测、现金流预测）仅为参考架构和实现示例。该技能提供算法知识，并帮助编写代码，但不参与做出税务或财务决策。
- **需要用户确认**：在以下操作前必须获得用户的明确同意：阻止付款、向生产环境发送发票、修改会计记录或进行任何具有财务后果的操作。
- **认证数据由用户管理**：KSeF API的令牌、证书和加密密钥必须通过环境变量（在元数据中声明：`KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`、`KSEF_BASE_URL`）或密钥管理员提供。该技能永远不会存储、生成、传输或请求这些认证数据。**切勿在对话中直接提供认证数据（令牌、密钥、证书）——请使用环境变量或平台密钥管理员。**文档中提到的Vault/Fernet示例仅用于用户实现参考。

**测试建议：**
- 使用`https://ksef-demo.mf.gov.pl`进行测试。
- 该技能在元数据中设置了`disableModelInvocation: true`，这意味着模型不应自动调用该技能。**注意：**frontmatter和`skill.json`中的声明仅具有提示作用，实际强制应用取决于平台。在使用前，请确认平台显示的注册表元数据中也包含`disable-model-invocation: true`。

## 安装前的检查清单

在安装技能并配置环境变量之前，请执行以下步骤：
- [ ] 验证注册表元数据：`disable-model-invocation`字段必须设置为`true`。
- [ ] 确认平台已读取frontmatter或`skill.json`中的环境变量声明：`KSEF_TOKEN`和`KSEF_ENCRYPTION_KEY`必须被标记为机密信息。
- [ ] 确认平台能够隔离环境变量（不记录或显示它们的值）。
- [ ] 在生产环境使用之前，先在`https://ksef-demo.mf.gov.pl`的测试环境中测试该技能。
- [ ] 请勿在对话中直接提供令牌、密钥或证书——请使用环境变量或密钥管理员。
- [ ] 如果注册表元数据与frontmatter/skill.json不一致，请不要配置认证数据，并向平台提供商报告问题。

## 主要功能

### 1. KSeF 2.0 API支持

- 发送FA(3)格式的发票
- 获取采购发票
- 管理会话/令牌
- 支持Offline24（故障模式）
- 获取UPO（官方接收证明）

**关键API端点：**
```http
POST /api/online/Session/InitToken     # Inicjalizacja sesji
POST /api/online/Invoice/Send          # Wyslanie faktury
GET  /api/online/Invoice/Status/{ref}  # Sprawdzenie statusu
POST /api/online/Query/Invoice/Sync    # Zapytanie o faktury zakupowe
```

请参阅[references/ksef-api-reference.md](references/ksef-api-reference.md)以获取完整的API文档，包括认证信息、错误代码和速率限制。

### 2. FA(3)架构

- FA(3)与FA(2)的区别：发票附件、合同类型（员工）、扩展的银行账户格式、每笔交易的50,000条记录限制、JST标识符和VAT分组。
请参阅[references/ksef-fa3-examples.md](references/ksef-fa3-examples.md)以获取XML示例（基础发票、多税率、更正、Offline24、附件）。

### 3. 会计流程

- **销售流程：** 数据 -> 生成FA(3)发票 -> 发送至KSeF -> 获取KSeF编号 -> 记账
  `收入300（账单）| 支出700（销售）+ 支出220（增值税）`
- **采购流程：** 获取KSeF数据 -> 解析XML -> 通过AI分类 -> 记账
  `收入400-500（成本）+ 支出221（增值税）| 支出201（账单）`

请参阅[references/ksef-accounting-workflows.md]以了解详细的费用匹配、MPP、更正、VAT登记和月度结算流程。

### 4. 人工智能辅助功能（参考架构）

以下是实现示例和参考架构：
- **成本分类**：基于合同历史数据的模型（随机森林算法），如果置信度<0.8则标记为异常。
- **欺诈检测**：用于检测金额异常的隔离森林模型，用于识别钓鱼发票的评分算法，用于VAT分析的图形分析。
- **现金流预测**：基于合同历史数据、金额和季节性模式的随机森林回归模型。

请参阅[references/ksef-ai-features.md]以了解概念性算法和实现示例（需要sklearn和pandas库）。

### 5. 合规性和安全性（实现示例）

以下是建议在用户系统中实现的安全性措施：
- 在付款前验证VAT信息。
- 使用Fernet/Vault对令牌进行加密存储（由用户实现）。
- 所有操作的审计跟踪。
- 3-2-1备份策略。
- 遵守RODO（数据保留期限后的匿名化）。
- 基于角色的访问控制（RBAC）。

请参阅[references/ksef-security-compliance.md]以获取安全实现示例和检查清单。

### 6. 更正发票

- 从KSeF获取原始发票 -> 生成FA(3)更正文件 -> 将更正文件与原始发票的KSeF编号关联 -> 发送至KSeF -> 记录更正或差额。

### 7. VAT和JPK_V7记录

- 生成销售/采购记录（Excel/PDF格式）、JPK_V7M（每月）和JPK_V7K（季度）。

## 故障排除 - 快速帮助

| 问题 | 原因 | 解决方案 |
|---------|-----------|-------------|
| 发票被拒绝（400/422错误） | XML格式错误、NIP错误、日期错误、字段缺失 | 检查UTF-8格式，验证FA(3)模式，确认NIP有效 |
| API超时 | KSeF服务器故障、网络问题、高峰时段 | 检查KSeF状态，使用指数退避策略重试 |
- 无法匹配付款信息 | 金额不符、数据缺失、分次付款 | 扩展搜索范围（±2%、±14天），检查MPP数据 |

请参阅[references/ksef-troubleshooting.md]以获取完整的故障排除指南。

## 参考文件

根据需要加载以下文件：
- [skill.json]：包含安全标志、环境变量声明和限制的元数据文件。
- [ksef-api-reference.md]：KSeF API端点、认证信息、发票发送/接收方式。
- [ksef-legal-status.md]：KSeF的部署日期、法律要求和处罚规定。
- [ksef-fa3-examples.md]：FA(3)发票结构的创建和验证。
- [ksef-accounting-workflows.md]：会计记录、费用匹配、MPP、更正、VAT登记。
- [ksef-ai-features.md]：成本分类、欺诈检测、现金流预测算法。
- [ksef-security-compliance.md]：VAT白名单、令牌安全、审计跟踪、RODO合规性。
- [ksef-troubleshooting.md]：API错误、验证问题、性能问题。

## 官方资源

- KSeF门户：https://ksef.podatki.gov.pl
- KSeF测试环境：https://ksef-demo.mf.gov.pl
- KSeF生产环境：https://ksef.mf.gov.pl
- VAT白名单API：https://wl-api.mf.gov.pl
- KSeF状态信息：https://github.com/CIRFMF/ksef-latarnia
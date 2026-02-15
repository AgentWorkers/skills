---
name: ksef-accountant-en
description: "波兰国家电子发票系统（KSeF）会计助理（英文版）。适用于需要使用KSeF 2.0 API、FA(3)发票、波兰增值税合规性要求、电子发票处理、支付匹配、增值税登记册（JPK_V7）、更正发票、分期支付机制（MPP）以及波兰会计工作流程的场景。具备在KSeF生态系统中处理发票开具、采购流程、成本分类、欺诈检测和现金流预测等方面的专业领域知识。"
license: MIT
---

# KSeF 会计代理

本工具专为波兰的国家电子发票系统（KSeF）设计，适用于 KSeF 2.0 环境及 FA(3) 格式。它支持与波兰电子发票相关的会计任务。

## 使用限制

- **仅提供知识支持**：本工具仅提供专业领域的知识和指导。所有代码示例仅供学习参考，切勿直接执行，需根据用户需求进行定制和审核。
- **不提供法律或税务建议**：所提供的信息可能已过时，请在实施前咨询专业税务顾问。
- **人工智能辅助，而非决策工具**：虽然 AI 功能（如分类、欺诈检测、现金流预测）可辅助会计人员工作，但不会做出具有法律约束力的税务或财务决策。对于低置信度的结果，需人工审核。
- **需用户确认**：在执行任何可能产生财务影响的操作（如阻止支付、向 KSeF 发送发票、修改会计分录等）之前，必须获得用户的明确授权。
- **凭证由用户管理**：KSeF API 令牌、证书、加密密钥及数据库凭证需通过环境变量（如 `KSEF_TOKEN`、`KSEF_ENCRYPTION_KEY`）或秘钥管理工具（如 HashiCorp Vault）由用户自行管理。严禁存储、生成或传输这些凭证。
- **使用演示环境进行测试**：生产环境（`https://ksef.mf.gov.pl`）生成的发票具有法律约束力；开发与测试请使用演示环境（`https://ksef-demo.mf.gov.pl`）。

## 核心功能

### 1. KSeF 2.0 API 操作

- 发送 FA(3) 格式的发票
- 获取采购发票
- 管理会话/令牌
- 处理 Offline24 模式（紧急情况）
- 获取 UPO（官方收款确认）

相关 API 端点请参见 [references/ksef-api-reference.md](references/ksef-api-reference.md)，其中包含认证信息、错误代码及速率限制规则。

### 2. FA(3) 发票格式

FA(3) 与 FA(2) 的主要区别包括：发票附件、合同类型（PRACOWNIK/EMPLOYEE）、扩展的银行账户格式、50,000 条记录的修改限制，以及 JST 和 VAT 组标识符。详细示例请参见 [references/ksef-fa3-examples.md](references/ksef-fa3-examples.md)（包含基本发票、多种 VAT 税率、修改记录、Offline24 模式及附件格式）。

### 3. 会计工作流程

- **销售流程**：
  - 数据处理 → 生成 FA(3) 发票 → 发送至 KSeF → 获取 KSeF 发票编号 → 记账分录
  `借方 300（应收账款）| 贷方 700（销售收入）+ 贷方 220（应付增值税）`

- **采购流程**：
  - 查询 KSeF 数据 → 下载 XML 文件 → 通过 AI 进行分类 → 记账分录
  `借方 400-500（费用）+ 借方 221（应付增值税）| 贷方 201（应付账款）`

详细工作流程请参见 [references/ksef-accounting-workflows.md](references/ksef-accounting-workflows.md)，内容包括支付匹配、MPP（分期付款）、修正发票、增值税登记及月末结账流程。

### 4. 人工智能辅助功能

- **成本分类**：利用历史数据、关键词匹配及随机森林（Random Forest）模型进行分类；置信度低于 0.8 的结果需人工审核。
- **欺诈检测**：通过异常金额、网络钓鱼发票、增值税支付模式异常等特征进行检测。
- **现金流预测**：基于合同历史、金额及季节性趋势预测支付日期。

相关算法及实现细节请参见 [references/ksef-ai-features.md](references/ksef-ai-features.md)。

### 5. 合规性与安全性

- 支付前需验证 VAT 白名单资格。
- 采用 Fernet/Vault 技术对令牌进行加密存储。
- 所有操作均保留审计痕迹。
- 实施 3-2-1 备份策略。
- 遵守 GDPR 和 RODO 法规（数据保留期后进行匿名处理）。
- 采用基于角色的访问控制（RBAC）机制。

相关安全要求及实施细节请参见 [references/ksef-security-compliance.md](references/ksef-security-compliance.md)。

### 6. 修正发票

- 从 KSeF 获取原始发票 → 创建 FA(3) 格式的修正发票 → 将修正发票与原始发票编号关联 → 重新发送至 KSeF → 进行账务冲销或差异处理。

### 7. VAT 登记与 JPK_V7 报表

- 生成销售/采购报表（Excel/PDF 格式）及 JPK_V7M（月度报表）、JPK_V7K（季度报表）。

## 故障排除快速指南

| 问题 | 常见原因 | 解决方案 |
|---------|-------------|----------|
| 发票被拒绝（错误代码 400/422）| XML 格式错误、NIP 无效、日期错误或字段缺失 | 确保文件格式为 UTF-8，验证 FA(3) 格式，检查 NIP 是否正确 |
| API 超时 | KSeF 服务中断、网络问题或高峰时段 | 检查 KSeF 服务状态，并尝试使用指数退避策略重试 |
| 无法匹配支付信息 | 金额不一致、数据缺失或存在分期付款情况 | 扩大搜索范围（允许误差范围 ±2% 或 ±14 天），检查 MPP 规则 |

完整故障排除指南请参见 [references/ksef-troubleshooting.md](references/ksef-troubleshooting.md)。

## 参考文件

根据实际需求查阅以下文档：

| 文件 | 阅读时机 |
|------|-------------|
| [ksef-api-reference.md](references/ksef-api-reference.md) | KSeF API 接口、认证流程及发票发送/获取方法 |
| [ksef-legal-status.md](references/ksef-legal-status.md) | KSeF 的实施日期、法律要求及处罚规定 |
| [ksef-fa3-examples.md](references/ksef-fa3-examples.md) | FA(3) 发票结构的创建与验证方法 |
| [ksef-accounting-workflows.md](references/ksef-accounting-workflows.md) | 记账分录处理、支付匹配、MPP、修正操作及增值税登记流程 |
| [ksef-ai-features.md](references/ksef-ai-features.md) | 成本分类、欺诈检测及现金流预测算法 |
| [ksef-security-compliance.md](references/ksef-security-compliance.md) | VAT 白名单管理、令牌安全、审计记录及数据保护法规 |
| [ksef-troubleshooting.md](references/ksef-troubleshooting.md) | API 错误处理、验证问题及性能优化方法 |

## 官方资源

- KSeF 官网：https://ksef.podatki.gov.pl
- KSeF 演示环境：https://ksef-demo.mf.gov.pl
- KSeF 生产环境：https://ksef.mf.gov.pl
- VAT 白名单相关 API：https://wl-api.mf.gov.pl
- KSeF 监控工具（KSeF Latarnia）：https://github.com/CIRFMF/ksef-latarnia
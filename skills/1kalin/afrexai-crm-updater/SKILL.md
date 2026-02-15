---
name: CRM Manager
description: 管理一个基于 CSV 的本地 CRM 系统，并实现管道跟踪功能。
---

# CRM 管理器

您负责管理一个以本地 CSV 文件形式存储的轻量级 CRM 系统。无需使用 Salesforce — 只需要一个简洁、易于维护的 CRM 系统即可。

## CRM 文件位置

默认路径：工作区内的 `crm.csv` 文件。如果文件不存在，请使用 `crm-template.csv` 文件创建。

## CSV 文件结构

```csv
id,name,company,email,phone,stage,deal_value,source,last_contact,next_action,next_action_date,notes,created,updated
```

### 字段

| 字段 | 描述 | 是否必填 |
|-------|-------------|----------|
| id | 自动递增的整数 | 是 |
| name | 联系人的全名 | 是 |
| company | 公司名称 | 是 |
| email | 电子邮件地址 | 否 |
| phone | 电话号码 | 否 |
| stage | 客户关系管理阶段（见下文） | 是 |
| deal_value | 预计交易金额（美元） | 否 |
| source | 客户找到您的途径/您找到他们的途径 | 否 |
| last_contact | 最后一次联系日期（YYYY-MM-DD） | 是 |
| next_action | 下一步行动 | 是 |
| next_action_date | 行动截止日期（YYYY-MM-DD） | 是 |
| notes | 自由格式的备注（多个备注之间用竖线分隔） | 否 |
| created | 创建日期（YYYY-MM-DD） | 是 |
| updated | 最后修改日期（YYYY-MM-DD） | 是 |

### 客户关系管理阶段

1. **lead** — 新联系人，尚未经过资格审核 |
2. **qualified** — 确认客户有预算、需求和购买权限 |
3. **meeting** — 预约了会议或会议已经完成 |
4. **proposal** — 已发送报价 |
5. **negotiation** — 正在协商条款 |
6. **closed-won** — 交易完成 |
7. **closed-lost** — 交易失败 |
8. **nurture** — 客户尚未准备好，需要保持联系 |

## 命令

当用户请求您管理 CRM 数据时，请执行以下操作：

### 添加联系人
“将 [name]（来自 [company]）添加到 CRM 中”
→ 创建新记录，将阶段设置为 “lead”，并将创建/修改日期设置为今天。

### 更新联系人
“更新 [name] — 今天有电话联系，将阶段设置为 ‘proposal’”
→ 更新阶段、最后一次联系日期、下一步行动和备注，并更新修改日期。

### 显示客户关系管理状态
“显示我的客户关系管理状态” / “我的 CRM 中有哪些联系人？”
→ 按阶段分组显示联系人，并显示对应的交易金额。

### 提示跟进事项
“哪些跟进事项已经到期？” / “我应该联系谁？”
→ 显示 `next_action_date` 小于或等于今天的联系人，并按日期排序。

### 客户关系管理阶段总结
“客户关系管理阶段总结”
→ 显示每个阶段的联系人总数、每个阶段的交易总额以及逾期跟进事项的数量。

### 搜索
“查找 [name]/[company]”
→ 在名称和公司字段中进行搜索。

### 转换阶段
“将 [name] 的阶段改为 [stage]”
→ 更新阶段和修改日期。

## 规则

- 在进行任何更改之前，请务必阅读 CSV 文件的内容（不要假设联系人的状态）。
- 修改记录时，请务必更新 `updated` 字段。
- 绝不要删除记录 — 可以将其状态改为 “closed-lost” 或 “nurture”。
- 备注字段仅支持追加新内容（使用竖线分隔），不要覆盖原有内容。
- 显示客户关系管理状态时，请以清晰的表格形式呈现。
- 如果联系人没有 `next_action_date` 或 `next_action_date` 已过期，请发出警告。
- 在执行批量操作之前，请备份 CSV 文件（备份文件名为 `crm-backup-YYYY-MM-DD.csv`）。

## 客户关系管理健康检查

定期检查以下情况：
- 14 天以上没有活动的联系人。
- 在同一阶段停滞超过 30 天的交易。
- 未安排跟进事项的联系人。
- 未安排跟进的潜在客户。

---

## 🔗 更多 AfrexAI 技能（在 ClawHub 上免费提供）

| 技能 | 安装方式 |
|-------|---------|
| AI 优化工具 | `clawhub install afrexai-humanizer` |
| SEO 写作工具 | `clawhub install afrexai-seo-writer` |
| 电子邮件生成工具 | `clawhub install afrexai-email-crafter` |
| 报价生成工具 | `clawhub install afrexai-proposal-gen` |
| 发票生成工具 | `clawhub install afrexai-invoice-gen` |
| 潜在客户评分工具 | `clawhub install afrexai-lead-scorer` |
| 客户入职工具 | `clawhub install afrexai-onboarding` |
| 会议准备工具 | `clawhub install afrexai-meeting-prep` |
| 社交媒体内容重利用工具 | `clawhub install afrexai-social-repurposer` |
| 常见问题解答生成工具 | `clawhub install afrexai-faq-builder` |
| 评论回复工具 | `clawhub install afrexai-review-responder` |
| 报告生成工具 | `clawhub install afrexai-report-builder` |
| CRM 更新工具 | `clawhub install afrexai-crm-updater` |
| 演示文稿审核工具 | `clawhub install afrexai-pitch-deck-reviewer` |
| 合同分析工具 | `clawhub install afrexai-contract-analyzer` |
| 价格优化工具 | `clawhub install afrexai-pricing-optimizer` |
| 客户评价收集工具 | `clawhub install afrexai-testimonial-collector` |
| 竞争对手监控工具 | `clawhub install afrexai-competitor-monitor` |

## 🚀 升级为专业版：行业特定内容包（每包 47 美元）

使用行业特定内容包，让您的 AI 代理具备深入的行业知识。

→ **[浏览内容包](https://afrexai-cto.github.io/context-packs/)**

**免费工具：** [AI 收入计算器](https://afrexai-cto.github.io/ai-revenue-calculator/) | [代理设置向导](https://afrexai-cto.github.io/agent-setup/)

*由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 开发 🖤💛*
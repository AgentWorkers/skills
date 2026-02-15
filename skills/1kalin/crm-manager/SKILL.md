---
name: CRM Manager
description: 管理一个基于 CSV 的本地 CRM 系统，并实现流程跟踪功能。
---

# CRM 管理器

您负责管理一个以本地 CSV 文件形式存储的轻量级 CRM 系统。无需使用 Salesforce——只需一个简洁、易于维护的管道系统即可。

## CRM 文件位置

默认位置：工作区中的 `crm.csv` 文件。如果文件不存在，请使用 `crm-template.csv` 作为模板创建。

## CSV 文件结构

```csv
id,name,company,email,phone,stage,deal_value,source,last_contact,next_action,next_action_date,notes,created,updated
```

### 字段

| 字段 | 描述 | 是否必填 |
|-------|-------------|----------|
| id      | 自动递增的整数 | 是       |
| name     | 联系人的全名    | 是       |
| company   | 公司名称    | 是       |
| email    | 电子邮件地址    | 否       |
| phone     | 电话号码     | 否       |
| stage     | 管道阶段（见下文） | 是       |
| deal_value | 预计交易金额（美元） | 否       |
| source    | 客户来源     | 否       |
| last_contact | 最后联系日期（YYYY-MM-DD）| 是       |
| next_action | 下一步行动    | 是       |
| next_action_date | 执行日期（YYYY-MM-DD）| 是       |
| notes    | 自由格式的备注（多条内容用竖线分隔）| 否       |
| created   | 创建日期（YYYY-MM-DD）| 是       |
| updated   | 最后修改日期（YYYY-MM-DD）| 是       |

### 管道阶段

1. **lead** — 新联系人，尚未经过资格审核  
2. **qualified** — 确认客户有预算、需求和购买权限  
3. **meeting** — 预约或已完成会议  
4. **proposal** — 已发送报价  
5. **negotiation** — 谈判条款  
6. **closed-won** — 交易完成  
7. **closed-lost** — 交易失败  
8. **nurture** — 当前尚未准备好，保持联系  

## 命令

当用户要求您管理 CRM 数据时，请执行以下操作：

### 添加联系人
“将 [name]（来自 [company]）添加到 CRM 中”
→ 创建新记录，将阶段设置为 “lead”，并将创建/修改日期设置为当前日期。

### 更新联系人
“更新 [name] — 今天有电话联系，将阶段更新为 ‘proposal’”
→ 更新联系人的阶段、最后联系日期、下一步行动和备注，并更新修改日期。

### 查看管道状态
“显示我的管道状态” / “我的 CRM 中有哪些联系人？”
→ 按阶段分组显示联系人，并显示对应的交易金额。

### 提醒跟进
“哪些跟进任务到期了？” / “我应该联系谁？”
→ 显示 `next_action_date` 小于或等于今天的联系人，并按日期排序。

### 管道汇总
“管道状态汇总”
→ 显示每个阶段的联系人总数、每个阶段的交易总额以及逾期跟进任务的数量。

### 搜索
“查找 [name]/[company]”
→ 在名称和公司字段中进行搜索。

### 转换阶段
“将 [name] 的阶段更新为 [stage]”
→ 更新联系人的阶段和修改日期。

## 规则

- 在进行任何更改之前，请务必先阅读 CSV 文件的内容（不要依赖系统默认的状态信息）。  
- 修改记录时，请务必更新 `updated` 字段。  
- 绝不要删除记录——请将其状态改为 “closed-lost” 或 “nurture”。  
- 备注字段仅支持追加新内容（使用竖线分隔），不要覆盖原有内容。  
- 显示管道状态时，请以清晰的表格形式呈现数据。  
- 如果联系人没有 `next_action_date` 或跟进任务逾期，请发出警告。  
- 在执行批量操作前，请备份 CSV 文件（例如：将其复制到 `crm-backup-YYYY-MM-DD.csv`）。  

## 管道健康检查

定期检查以下情况：
- 14 天以上没有活动的联系人  
- 长期停留在同一阶段的交易  
- 未安排跟进任务的联系人  
- 未安排后续行动的潜在客户
---
name: Documents
description: 构建一个个人文档系统，以便能够即时访问ID、合同、证书和重要文件。
metadata: {"clawdbot":{"emoji":"📄","os":["linux","darwin","win32"]}}
---

## 核心功能
- 当用户需要文档时，能够立即找到它。
- 当用户收到重要文档时，协助对其进行分类和管理。
- 当用户询问“我的X文件在哪里”时，能在几秒钟内给出答案。
- 创建`~/docs/`作为文档存储的工作目录。

## 文件结构
```
~/docs/
├── identity/
│   ├── passport.md
│   ├── drivers-license.md
│   └── national-id.md
├── financial/
│   ├── tax-returns/
│   ├── bank-accounts.md
│   └── investments.md
├── property/
│   ├── lease.md
│   ├── deed.md
│   └── insurance.md
├── medical/
│   ├── insurance.md
│   └── records/
├── work/
│   ├── contracts/
│   └── certifications/
├── legal/
│   ├── will.md
│   └── power-of-attorney.md
├── vehicles/
│   └── car.md
└── index.md
```

## 文档条目格式
```markdown
# passport.md
## Document
US Passport

## Number
[stored securely, reference only]

## Issued
January 15, 2020

## Expires
January 14, 2030

## Location
Physical: home safe
Digital: ~/documents/scans/passport.pdf

## Notes
Need 6 months validity for most travel
Renew by July 2029
```

## 快速参考索引
```markdown
# index.md
## Expiring Soon
- Driver's license: March 2024
- Car registration: December 2024

## Frequently Needed
- Health insurance card: medical/insurance.md
- Lease agreement: property/lease.md

## Emergency Access
- Passport number: identity/passport.md
- Insurance policy: property/insurance.md
```

## 身份证明文件
- 护照：编号、签发日期/有效期、续期时间
- 驾驶执照：编号、有效期、真实身份状态
- 国民身份证：编号、发证地点
- 出生证明：原件存放地点
- 社会保障卡：编号信息、卡片存放位置

## 财务文件
- 税务申报单：按年份分类、存放地点
- 银行账户：银行名称、账户编号
- 投资账户：经纪公司名称、账户编号
- 贷款文件：贷款条款、还款信息

## 房产文件
- 租赁合同：租赁条款、房东联系方式、续期日期
- 房产所有权证：房产详细信息、登记信息
- 家庭保险：保单编号、保险范围、保险代理人
- 保修单：家电/系统的保修信息、有效期

## 医疗文件
- 保险卡：保单信息、所属保险集团编号
- 疫苗接种记录：接种日期、接种类型
- 处方药：当前使用的药物
- 医疗历史：重大手术记录、健康状况

## 车辆文件
- 车辆登记信息：车牌号码、有效期
- 保险信息：保单编号、保险范围
- 车辆所有权信息：贷款状态、车辆存放地点
- 维护记录：车辆维修历史

## 工作相关文件
- 雇佣合同：当前合同及过往合同
- 证书：证书编号、有效期、续期要求
- 绩效评估：按年份整理
- 股票/股权相关文件：股票授予信息、归属情况

## 需要向用户展示的信息
- “您的护照将在8个月后过期。”
- “您的驾驶执照下个月需要续期。”
- “您的健康保险卡位于medical/insurance.md文件中。”
- “上一次提交的税务申报单是2023年的。”

## 常见请求
- “我需要我的护照号码。” → 查看identity/passport.md文件
- “我的租赁合同什么时候到期？” → 查看property/lease.md文件
- “我的健康保险信息在哪里？” → 查看medical/insurance.md文件
- “我的车辆登记信息在哪里？” → 查看vehicles/car.md文件

## 文件过期提醒
- 对以下文件设置过期提醒：
  - 护照：6个月内到期（旅行相关文件）
  - 驾驶执照/车辆登记证：2个月内到期
  - 保险合同：1个月内到期

## 安全注意事项
- 敏感信息请以引用形式存储，避免以明文形式保存。
- 实物文件的存放位置：建议存放在“保险箱”或“文件柜”中。
- 数字文件建议扫描后存储在加密文件夹中。
- 在紧急情况下，仅与可信赖的人共享文件访问权限。

## 逐步改进计划
- 第1周：整理带有过期日期的身份证明文件。
- 第2周：整理财务和房产相关文件。
- 第3周：整理医疗和车辆相关文件。
- 随着新文件的到来，持续进行文件整理工作。

## 禁止的行为
- 禁止以明文形式存储敏感信息。
- 禁止在文件续期后忘记更新相关信息。
- 禁止丢失文件的物理存放位置。
- 禁止忽略文件的过期日期提醒。
# AI Lead Generator 技能

利用人工智能驱动的研究功能以及与 LinkedIn/Apollo 的集成，为任何行业生成优质的 B2B 销售线索。

## 该技能的功能

自动进行目标客户群体的研究，并整理出以下信息的销售线索列表：
- 公司名称及规模
- 决策者联系方式
- 直接电子邮件地址
- 公司面临的问题
- 用于外联的个性化数据

非常适合需要持续生成销售线索的销售团队、顾问和 B2B 营销人员使用。

## 使用方法

```bash
# Generate 50 leads for fintech companies
openclaw run ai-lead-generator --industry fintech --count 50 --role "CTO,CEO" --company-size "10-100"

# Target specific geographic region  
openclaw run ai-lead-generator --industry healthcare --region "United States" --count 100
```

## 主要特性

- ✅ 支持与 Apollo.io 集成，以获取联系信息  
- ✅ 自动化使用 LinkedIn Sales Navigator 进行搜索  
- ✅ 电子邮件地址的验证与确认  
- ✅ 收集关于公司技术使用情况的详细信息（例如使用的工具）  
- ✅ 可导出数据至 CSV、CRM 或 JSON 格式  
- ✅ 数据收集符合 GDPR 法规要求  

## 支持的行业

- SaaS/科技行业  
- 医疗保健  
- 房地产  
- 法律服务  
- 制造业  
- 电子商务  
- 专业服务  

## 输出示例

| 公司名称 | 联系人 | 职位 | 电子邮件 | 电话 | 公司规模 | 面临的问题 |
|---------|---------|--------|-------|--------|--------------|-------------|
| TechCorp Inc | John Smith | CTO | john@techcorp.com | +1-555-0123 | 50-100 名员工 | 需要迁移旧系统 |
| DataFlow Ltd | Sarah Jones | 运营副总裁 | sarah@dataflow.co | +1-555-0456 | 25-50 名员工 | 报告流程依赖人工操作 |

## 定价方案

- **基础计划**：每月 29 美元，生成 100 条销售线索  
- **专业计划**：每月 79 美元，生成 500 条销售线索  
- **企业计划**：每月 199 美元，无限量销售线索 + 可自定义字段  

## 使用要求

- 需要拥有 Apollo.io 账户（可选，可提升数据质量）  
- 需要拥有 LinkedIn 账户（用于更精确的定位）  

## 安装方法

```bash
clawhub install ai-lead-generator
```

---

*由 Billy Overlord 开发——专注于 B2B 自动化的 AI 工具*
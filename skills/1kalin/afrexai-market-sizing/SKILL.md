# 市场规模估算工具 — TAM/SAM/SOM 计算器

无论您需要为哪种产品、商业计划书还是业务案例提供市场规模估算，本工具都能帮助您得出可靠的数据。我们结合了自上而下（top-down）和自下而上（bottom-up）的估算方法。

## 使用成果

- **TAM**（总可寻址市场，Total Addressable Market）：假设您能占据 100% 市场份额时的整体市场规模  
- **SAM**（可服务可寻址市场，Serviceable Addressable Market）：您实际能够触及的市场细分  
- **SOM**（可服务可获取市场，Serviceable Obtainable Market）：在 12 至 36 个月内能够实际获取的市场份额  
- **自下而上的验证**：基于单位经济模型（unit economics）和可触及客户数量得出的估算结果  
- **数据来源**：政府数据、行业报告、公开文件等  

## 使用方法

请告诉我您的产品/服务以及目标客户群体，我将为您生成完整的市场规模估算报告。

**示例提示：**  
- “估算美国中型律师事务所使用人工智能进行合同审核的市场规模”  
- “针对年收入在 100 万至 500 万美元之间的电子商务品牌的 SaaS 帮助台产品的 TAM/SAM/SOM”  
- “英国中小企业的自动化记账服务市场规模”  

## 估算方法  

### 自上而下（Top-Down）  
1. 从整个行业的总收入开始（提供数据来源）  
2. 按地区、行业细分和市场规模进行筛选  
3. 考虑技术采用率  
4. 最终结果即为 SAM  

### 自下而上（Bottom-Up）  
1. 统计可触及的客户数量（通过数据库、目录、LinkedIn 等渠道）  
2. 将客户数量乘以每个客户的年均合同价值（ACV）  
3. 考虑每个销售阶段的转化率  
4. 最终结果即为 SOM  

### 交叉验证（Triangulation）  
比较自上而下和自下而上的估算结果。如果两者相差在 2 至 3 倍范围内，说明估算结果较为合理；如果差异较大，请重新审视相关假设。  

## 输出格式  

```
## Market Sizing: [Product/Service]

### TAM — $X.XB
[Total market calculation with sources]

### SAM — $XXM
[Filtered by geography + segment + tech adoption]

### SOM (12-month) — $X.XM
[Bottom-up: customers × ACV × conversion]

### Key Assumptions
- [Assumption 1 + source]
- [Assumption 2 + source]

### Risks to Sizing
- [What could make this smaller]
- [What could make this bigger]
```  

## 适用场景  

- 商业计划书和投资者演示  
- 市场进入策略制定  
- 新产品可行性分析  
- 董事会报告和业务案例  
- 竞争定位分析  

## 专业提示  

大多数创业者往往会高估 TAM、低估 SOM。投资者能迅速识破这些夸大的数字。一个数据详实、估算合理的 5000 万美元 SAM，远比一个不切实际的 100 亿美元 TAM 更有说服力。  

---

需要您所在行业的完整业务背景资料吗？**[查看 AfrexAI 的背景资料包](https://afrexai-cto.github.io/context-packs/)**——为金融科技、医疗保健、法律、SaaS 等行业预构建了相关配置文件（每个包售价 47 美元）。  

想了解人工智能自动化能为您的企业节省多少成本吗？**[AI 收入损失估算工具](https://afrexai-cto.github.io/ai-revenue-calculator/)**
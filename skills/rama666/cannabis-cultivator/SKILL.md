---
name: cannabis-cultivator
description: >
  **EU种子库元搜索助手**：  
  每当您需要查找欧洲各大可信店铺中的大麻品种时，都可以使用此功能。您可以根据基因型、产量、开花时间或THC含量对品种进行筛选，同时还能比较不同产品的价格。此外，该工具还提供了账户创建和结账的指导流程（用户需手动填写表格并完成支付）。
---
# 大麻种植者 – 欧盟种子库查找工具

## 概述  
本工具是用于从信誉良好的欧洲种子库中获取大麻品种信息的综合服务平台。它提供搜索、筛选、结果整理以及用户注册/结算指导等功能。用户可以选择上传图片或语音文件作为个性化偏好信息；但该工具不提供植物健康状况的诊断服务。

## 快速工作流程  
1. **明确需求**  
   - 输入品种关键词、所需效果或品种特性。  
   - 必填筛选条件：基因型、开花周期、产量等级、THC/CBD含量范围、自动开花类型（自动开花/需光周期）、雌雄株类型（雌雄同株/普通品种）。  
   - 提供预算信息、包装规格、目标运输国家及首选支付方式。  

2. **选择搜索策略**  
   - 参考 [`references/seedbanks.md`](references/seedbanks.md) 中列出的种子库进行查询。  
   - 对于特定品种名称，可通过 SerpAPI/Tavily 或浏览器直接在网站上进行搜索（例如：`site:zamnesia.com "amnesia"`）。  
   - 如需浏览更多品种信息，可打开各种子库的品种查询页面。  

3. **汇总搜索结果**  
   - 收集品种名称、育种者信息、包装规格、价格、库存情况以及运输限制等信息。  
   - 根据 [`references/filters.md`](references/filters.md) 中规定的标准对数据进行处理和标准化。  

4. **筛选与排序**  
   - 按照以下顺序对结果进行排序：基因型 → 开花周期 → 产量 → THC 含量（后续可参考萜烯成分或 CBD 含量等次要属性）。  
   - 如果某个筛选条件无法满足，系统会标记该选项并推荐最接近的替代品种。  

5. **账户注册与结算指导**  
   - 查阅 [`references/account-setup.md`](references/account-setup.md) 以了解各种子库的注册流程、支付方式及相关法律法规。  
   - 提供详细的操作步骤指导，用户自行完成注册和支付操作。  

6. **提供汇总信息**  
   - 生成结构化的表格，并以列表形式总结各选项的优缺点及后续操作步骤（详见下方模板）。  

## 搜索与筛选指南  
### 1. 种子库覆盖范围  
参考 `seedbanks.md` 中列出的种子库：  
- **核心种子库**：Alchimia、Sensi Seeds、Anesia Seeds、Advanced Seeds、Bulk Seed Bank、Sweet Seeds。  
- **推荐的欧盟零售商**：Zamnesia、Dutch-Headshop、Weed Seed Shop、Royal Queen Seeds、Amsterdam Genetics、CannaConnection。  
- 如有需要，可添加用户指定的种子库（请核实其合法性）。  

### 2. 数据收集清单  
对于每个候选品种，需记录以下信息：  
- 种子库名称及直接访问网址  
- 品种名称及育种者信息  
- 基因型（Sativa/Indica 比例、自动开花类型/需光周期、雌雄株类型）  
- 开花周期（室内种植周数/室外收获时间）  
- 预计产量（室内种植：每平方米产量；室外种植：每株产量）  
- THC/CBD 含量  
- 包装规格及价格（注明货币单位）  
- 运输限制及可接受的支付方式  

### 3. 筛选规则（来自 `filters.md`）  
- **基因型**：  
  - Sativa 占主导（Sativa 比例 > 65%）、Indica 占主导（Indica 比例 > 65%）、平衡型杂交品种、自动开花品种。  
- **产量**：使用“低/中/高”三个等级进行分类；如制造商提供具体数据，请予以标注。  
- **开花周期**：7–14 周（标注快速/缓慢生长的品种）；自动开花品种的整个生长周期为 9–12 周。  
- **THC/CBD 含量**：  
  - THC 含量 > 22% 为高含量；15–22% 为中等含量；< 15% 为低含量；若产品标注了 CBD 含量（> 1%），请予以说明。  

## 账户注册与结算指导  
- 对于每个符合条件的种子库，需说明：  
  1. 注册网址及所需填写的字段  
  2. 可用的支付方式（信用卡、SEPA、Klarna、加密货币等）及地区限制  
  3. 运输注意事项（是否提供隐秘包装、禁止运输的国家、可选择的快递服务）  
  4. 合规性提醒：用户需确认所在地区的种植合法性  
- 提供可复制的检查清单（例如：“结算前请确认：电子邮件已验证、地址信息填写完整、支付方式已选择”）  
- 严禁自动填充或提交敏感信息；仅提供操作步骤说明。  

## 输出模板  
```
# Requested Profile
- Keywords / lineage: …
- Mandatory filters: …
- Shipping to: …

# Top Matches
| Shop | Strain | Genotype | THC/CBD | Flowering | Yield | Price/Pack | Link |
| … | … | … | … | … | … | … | … |

# Notes & Trade-offs
- …

# Account & Checkout Tips
- Shop: …
- Register via … (fields required …)
- Payment options: …
- Shipping considerations: …
- Legal reminder: …

# Next Steps
1. …
2. …
3. …
```  

## 参考资源  
- [`references/seedbanks.md`](references/seedbanks.md) – 各种子库的详细信息（地址、运输政策、支付方式、特色产品等）  
- [`references/filters.md`](references/filters.md) – 用于基因型、产量、开花周期及效力参数的数据标准化规则  
- [`references/account-setup.md`](references/account-setup.md) – 各种子库的注册与结算流程指南  
- `scripts/` – 用于未来自动化脚本的开发（如数据抓取、数据清洗工具）  
- `assets/` – 存储模板文件（如 CSV 导出格式模板）
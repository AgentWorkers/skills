# NG律师数据库构建（步骤1）

## 本技能的功能  
这是Fei Gao的“尼日利亚律师网络”工作流程中的**第一步**：  
1) 构建律师数据库（本技能负责）  
2) 发送外联邮件并根据回复情况评分（该过程由另一技能完成）  
3) 对收集到的数据进行排序并导出，以便快速查询（该过程由另一技能完成）  

目标是创建一个数据库，实现以下条件的快速匹配：  
**城市 → 执业领域 → 专业细分 → 监管机构 → 公司规模 → 职位 → 评分 → 联系方式**。  

本技能主要关注数据的收集与结构化分类，并附带相关证据的链接。  

---

## 输入参数  
- **城市**：`拉各斯` | `阿布贾`  
- **执业领域**：`建筑` | `房地产` | `劳动法` | `税务` | `刑事` | `知识产权`  
- **每个细分领域的候选人数量**：整数（目标值为**3**）  

---

## 输出文件  
- **lawyer_db_ng.xlsx**（主数据库）  
- **sources.jsonl**（每条记录的证据信息：网址 + 摘要 + 时间戳）  

---

## 数据库表结构（列顺序固定）  
Excel文件中的列必须按照以下顺序排列：  
1. Lawyer_UID  
2. 国家  
3. 城市  
4. 执业领域  
5. 专业细分  
6. 监管机构标签  
7. 公司名称  
8. 公司规模  
9. 职位  
10. 律师姓名  
11. 电子邮件  
12. 电话  
13. LinkedIn账号  
14. 官方网站  
15. 证据链接（Evidence_URL）  
16. 总分（步骤1中此项为空）  
17. 回复速度评分（Score_ResponseSpeed）  
18. 评分详情（Score_Detail）  
19. 服务费用评分（Score_Pricing）  
20. 合作评分（Score_Cooperation）  
21. 风险等级（Risk_Flag）  
22. 是否需要跟进（NeedFollowUp，0/1）  
23. 通道成本风险（ChannelCostRisk，低/中/高）  
24. 最后更新时间（Last_Updated）  

---

## 不可协商的规则（以避免后续评分混乱）  
### 1) 唯一键（Lawyer_UID）  
所有后续评分操作必须通过**Lawyer UID**进行，严禁使用律师姓名。  
格式示例：`LAW-NG-LAG-CON-0001`  
- **城市代码**：Lagos=LAG, Abuja=ABJ  
- **执业领域代码**：Construction=CON, RealEstate=REA, Labour=LAB, Tax=TAX, Criminal=CRI, IP=IPR  

### 2) 电子邮件政策（防止通道成本风险）  
- 电子邮件必须**明确公开**在律师的官方资料页面、作者页面或个人资料中。  
- **禁止猜测**（例如，除非有明确显示，否则不允许使用格式为`firstname.lastname@firm.com`的邮箱地址）。  
- 如果只有通用邮箱（如`info@`或`contact@`），可以使用，但需设置：  
  - `ChannelCostRisk=High`  
  - `NeedFollowUp=1`  

### 3) 证据链  
每行数据必须包含**证据链接（Evidence_URL）**。  
本技能还会生成`sources.jsonl`文件，其中包含：  
- Lawyer_UID  
- Evidence_URL  
- 证据摘要（不超过300个字符）  
- 证据捕获时间（Captured_At）  

### 4) 公司规模分类（作为费用参考）  
公司规模会影响服务费用预期。分类标准如下：  
- **顶级**：该公司在尼日利亚的相关执业领域内被列入**Chambers**或**Legal 500**榜单；或  
  - 公司律师人数超过**50人**（需提供相应证据）。  
- **中型**：律师人数在**15–50人**之间。  
- **小型**：律师人数在**2–14人**之间。  
- **个体执业者**：独立执业律师（人数为1人）。  
- **未知**：证据不足，因此设置`NeedFollowUp=1`。  

### 5) 职位对应关系（作为费用参考）  
职位分类标准如下：  
- **合伙人（Partner）**：总经理合伙人（Managing Partner）、高级合伙人（Senior Partner）  
- **法律顾问（Counsel）**：法律顾问（Counsel）、副法律顾问（Of Counsel）  
- **高级助理（SeniorAssociate）**：高级助理（Senior Associate）、助理律师（Associate）  
- **助理律师（Associate）**：助理律师（Associate）、实习律师（Junior Associate）  
- **独立执业者（Independent）**：独立执业律师（Sole Practitioner）、首席律师（Principal）、独立法律从业者（Independent Legal Practitioner）  

---

## 监管机构标签（仅在有证据的情况下填写）  
允许使用的标签值：  
- CAC、NIPC、FIRS、StateIRS、NAFDAC、Immigration、MinistryOfMines、IPRegistry、EFCC、Police、Court  

规则：  
- 仅当证据中提及相关监管机构或涉及相关事务时才填写标签。  
- 若无证据，该字段应留空；后续外联邮件会要求律师自行报告所涉及的监管机构。  

---

## 数据收集策略（推荐来源）  
优先顺序：  
1) 尼日利亚相关执业领域的Chambers或Legal 500榜单上的公司  
2) 律师事务所的官方团队页面（包含电子邮件信息的个人资料页面）  
3) 律师事务所网站、Lexology或IFLR上的作者页面（如果页面上有电子邮件信息）  
4) 小型/个体执业律师的事务所网站  

---

## 数据分割目标  
对于每个（公司规模 × 职位）组合，尽可能收集**n_per_segment**名具有有效电子邮件的候选人。  
在顶级律师事务所中，优先选择：  
- 法律顾问（Counsel）/高级助理（SeniorAssociate）/助理律师（Associate），他们通常更愿意合作。  

---

## 示例运行（最佳实践）  
城市：拉各斯  
执业领域：建筑  
每个细分领域的候选人数量：3  

目标：  
- 确保拉各斯建筑领域的律师数据库构建完成，且数据准确：  
  - 公司规模分类正确  
  - 职位对应关系准确  
  - 电子邮件信息有据可查  
  - 列顺序一致
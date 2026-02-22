# 出口合规与贸易管控

本工具用于分析产品、目的地和最终用户是否符合美国的出口管控法规（EAR、ITAR、OFAC制裁），并生成相应的分类建议、许可要求和合规检查清单。

## 功能概述

当提供产品描述、目的地国家和最终用户信息时，系统将执行以下操作：
1. **ECCN分类**：根据产品特性确定相应的出口管控分类编号（Commerce Control List）。
2. **制裁筛查**：检查目的地国家和最终用户是否属于OFAC的制裁名单（SDN列表）、实体名单中的高风险对象或被禁止的交易方。
3. **许可判定**：判断是否适用许可例外情况（如TMP、TSR、ENC），或者是否需要正式的BIS许可证。
4. **风险提示检查**：根据BIS的“了解你的客户”（Know Your Customer）指南，识别潜在风险点。
5. **文档生成**：自动生成发货人指示函模板、最终用户使用证书模板以及内部合规备忘录。

## 使用方法

请向系统提供以下信息：
- **产品类型**：出口的商品（软件、硬件、技术数据、服务）
- **目的地**：具体国家及实体/地址
- **最终用户**：公司名称、所属行业及关联关系
- **交易金额**：用于判断是否满足“最低金额豁免”（de minimis）标准

**示例提示：**
```
Run export compliance check:
Product: Cloud-based encryption software (AES-256, key management)
Destination: United Arab Emirates
End-user: Dubai National Bank
Value: $180,000/year
```

## 分类框架

### EAR分类（Commerce Control List）
| 分类 | 描述 | 常见类别 |
|----------|-------------|--------------|
| 0     | 核能与其他 | 核设备、材料 |
| 1     | 材料     | 化学品、合金、复合材料 |
| 2     | 材料加工   | 机床、机器人 |
| 3     | 电子     | 集成电路、传感器、激光器 |
| 4     | 计算机    | 硬件、软件、加密技术 |
| 5     | 电信与信息安全 | 加密技术、网络设备 |
| 6     | 传感器与激光器 | 相机、雷达、声纳 |
| 7     | 导航系统   | GPS、惯性导航系统、加速度计 |
| 8     | 海事     | 船只、潜水器 |
| 9     | 航空航天 | 飞机、发动机、无人机 |

### 出口管控理由
- NS（国家安全）、MT（导弹技术）、NP（核不扩散）
- CB（化学/生物）、CC（犯罪控制）、RS（区域稳定）
- AT（反恐）、SS（物资短缺）、UN（联合国制裁）

### 许可例外情况快速参考
| 例外类型 | 适用场景 |
|-----------|----------|
| ENC    | 大众市场销售的加密产品 |
| TMP    | 临时出口/再出口 |
| TSR    | 受限制的技术/软件 |
| GOV    | 美国政府机构 |
| BAG    | 个人行李 |
| RPL    | 替换零件（一对一替换） |
| CIV    | 民用最终用户（国家组B） |

## OFAC制裁计划（现行生效）
- **全面制裁**：古巴、伊朗、朝鲜、叙利亚、克里米亚/DNR/LNR
- **针对性制裁**：俄罗斯、白俄罗斯、缅甸、委内瑞拉、尼加拉瓜、中国（军事领域）、埃塞俄比亚、马里等
- **SDN名单**：包含12,000多名被制裁个人/实体——所有交易均需筛查

## 风险提示（BIS“了解你的客户”指南）
1. 客户拒绝提供最终用途信息
2. 产品与买家业务范围不符
3. 不寻常的运输路线或中间国家
4. 客户愿意为高价商品支付现金
5. 将货物交付给货运代理而非最终用户
6. 对货物用途的回答含糊不清
7. 订购的商品与目的地国家的技术水平不匹配
8. 客户使用邮政信箱或住宅地址接收货物
9. 包装或标记方式异常
10. 客户拒绝常规的安装/培训/维护服务

## “最低金额豁免”规则
源自美国的受管控商品，若满足以下条件可能无需许可证：
- **大多数国家**：占比不超过25%
- **国家组E:1（支持恐怖主义）和E:2**：占比不超过10%
- 计算方法：（源自美国的受管控商品价值 / 总交易价值）× 100%

## 输出格式
```
═══ EXPORT COMPLIANCE ASSESSMENT ═══

PRODUCT CLASSIFICATION
  Likely ECCN: [number]
  Category: [description]
  Control Reasons: [NS/MT/etc.]

DESTINATION ANALYSIS
  Country: [name]
  Country Group: [A:1, B, D:1, etc.]
  Sanctions Programs: [if any]
  Embargo Status: [comprehensive/targeted/none]

END-USER SCREENING
  Entity List: [clear/match/possible match]
  SDN List: [clear/match/possible match]
  Red Flags Triggered: [list any]

LICENSE DETERMINATION
  License Required: [yes/no/likely]
  Applicable Exceptions: [if any]
  Recommended Action: [proceed/investigate/halt]

DOCUMENTATION NEEDED
  □ Shipper's Letter of Instruction
  □ End-Use Certificate
  □ Compliance Memo
  □ [additional as needed]
═══════════════════════════════════
```

## 需要此工具的行业
- 国际销售的软件公司（尤其是加密技术、人工智能/机器学习、网络安全领域）
- 拥有双用途组件的硬件制造商
- 国防承包商及分包商
- 从事国际研究的大学
- 物流和货运代理公司
- 与受制裁国家有业务往来的企业

## 相关法规参考
- 出口管理法规（EAR）：15 CFR第730-774部分
- 国际武器贸易法规（ITAR）：22 CFR第120-130部分
- OFAC制裁规定：31 CFR第500部分
- 商业管控清单：第774部分的补充文件1
- 国家分类表：第738部分的补充文件1
- 实体名单：第744部分的补充文件4

---

*由[AfrexAI](https://afrexai-cto.github.io/context-packs/)开发——专为商业运营设计的AI辅助工具包。*
---
name: "mdr-745-specialist"
description: 欧盟MDR 2017/745合规专家，负责医疗器械的分类、技术文档编写、临床证据收集以及上市后监管工作。专业领域包括附件VIII中的分类规则、附件II/III中的技术文件要求、附件XIV中的临床评估流程，以及EUDAMED（欧盟医疗器械数据库）的整合工作。
triggers:
  - MDR compliance
  - EU MDR
  - medical device classification
  - Annex VIII
  - technical documentation
  - clinical evaluation
  - PMCF
  - EUDAMED
  - UDI
  - notified body
---
# MDR 2017/745 专业指南

欧盟医疗器械法规（MDR）关于医疗器械分类、技术文件和临床证据的要求与指南。

---

## 目录

- [医疗器械分类流程](#device-classification-workflow)
- [技术文件](#technical-documentation)
- [临床证据](#clinical-evidence)
- [上市后监督](#post-market-surveillance)
- [EUDAMED与UDI](#eudamed-and-udi)
- [参考文档](#reference-documentation)
- [工具](#tools)

---

## 医疗器械分类流程

根据MDR附录VIII对医疗器械进行分类：

1. 确定医疗器械的使用期限（临时性、短期、长期）
2. 判断医疗器械的侵入性级别（非侵入性、通过体腔操作、外科手术）
3. 评估医疗器械与人体系统的接触部位（中枢神经系统、心脏系统等）
4. 判断医疗器械是否具有能量依赖性
5. 应用相应的分类规则（规则1-22）
6. 对于软件产品，应用MDCG 2019-11标准进行分类
7. 记录分类的依据
8. **验证：** 将分类结果提交给指定认证机构（Notified Body）进行确认

### 分类矩阵

| 因素 | I类 | IIa类 | IIb类 | III类 |
|--------|---------|-----------|-----------|-----------|
| 使用期限 | 任意 | 短期 | 长期 | 长期 |
| 侵入性 | 非侵入性 | 通过体腔操作 | 外科手术 | 可植入式 |
| 与人体系统的接触部位 | 任意 | 非关键器官 | 关键器官（如中枢神经系统/心脏） |
| 风险等级 | 最低 | 低至中等 | 中等到高 | 最高 |

### 软件分类（MDCG 2019-11标准）

| 信息用途 | 病情的严重程度 | 分类等级 |
|-----------------|-------------------|-------|
| 用于辅助决策 | 病情不严重 | IIa类 |
| 用于辅助决策 | 病情严重 | IIb类 |
| 用于驱动或治疗关键生理功能 | III类 |

### 分类示例

**示例1：可吸收外科缝合线**
- 规则8（可植入式，长期使用）
- 使用期限：超过30天（可吸收）
- 与人体组织的接触：一般组织
- 分类：**IIb类**

**示例2：人工智能诊断软件**
- 规则11 + MDCG 2019-11标准
- 功能：用于诊断严重疾病
- 分类：**IIb类**

**示例3：心脏起搏器**
- 规则8（可植入式）
- 与人体系统的接触：中枢循环系统
- 分类：**III类**

---

## 技术文件

根据附录II和III的要求准备技术文件：

1. 编写医疗器械描述（包括不同型号、配件及预期用途）
2. 制定产品标签（符合第13条要求）
3. 记录产品的设计和制造过程
4. 完成GSPR（Good Safety Practice Requirements）合规性评估
5. 编制风险分析报告
6. 整合风险管理文件（ISO 14971标准）
7. **验证：** 技术文件需经过认证机构的审核

### 技术文件结构

```
ANNEX II TECHNICAL DOCUMENTATION
├── Device description and UDI-DI
├── Label and instructions for use
├── Design and manufacturing info
├── GSPR compliance matrix
├── Benefit-risk analysis
├── Verification and validation
└── Clinical evaluation report
```

### GSPR合规性检查清单

| 要求 | 证据 | 状态 |
|-------------|----------|--------|
| 安全设计（GSPR 1-3） | 风险管理文件 | ☐ |
| 化学性质（GSPR 10.1） | 生物相容性报告 | ☐ |
| 感染风险（GSPR 10.2） | 灭菌验证 | ☐ |
| 软件要求（GSPR 17） | IEC 62304标准相关文件 | ☐ |
| 标签内容（GSPR 23） | 标签设计和使用说明书 | ☐ |

### 合规性评估途径

| 分类等级 | 评估途径 | 是否需要指定认证机构参与 |
|-------|-------|----------------|
| I类 | 附录II自我声明 | 不需要 |
| IIa类/II类植入式器械 | 附录II + 附录IX/XI | 需要无菌或测量方面的认证 |
| IIb类 | 附录IX + 附录X或X + XI | 需要型式检验和生产过程认证 |
| III类 | 附录IX + 附录X | 需要全面的质量管理体系（QMS）和型式检验 |

---

## 临床证据

根据附录XIV的要求制定临床证据策略：

1. 明确临床声明和评估指标
2. 进行系统性文献检索
3. 评估临床数据的质量
4. 评估数据的等效性（技术、生物学、临床方面）
5. 识别证据缺口
6. 判断是否需要进行临床研究
7. 编制临床评估报告（CER）
8. **验证：** CER需由合格的评估机构审核

### 各分类等级的临床证据要求

| 分类等级 | 最低证据要求 | 是否需要临床研究 |
|-------|------------------|---------------|
| I类 | 需要风险-效益分析 | 通常不需要 |
| IIa类 | 文献资料 + 上市后数据 | 可能需要 |
| IIb类 | 系统性文献回顾 | 通常需要 |
| III类 | 全面的临床数据 | 必须要求（第61条） |

### 临床评估报告结构

```
CER CONTENTS
├── Executive summary
├── Device scope and intended purpose
├── Clinical background (state of the art)
├── Literature search methodology
├── Data appraisal and analysis
├── Safety and performance conclusions
├── Benefit-risk determination
└── PMCF plan summary
```

### 合格评估机构的要求

- 拥有医学学位或相应的医疗行业资格
- 在相关领域具有4年以上的临床经验
- 接受过临床评估方法论的培训
- 熟悉MDR法规的要求

---

## 上市后监督

根据第VII章的要求建立上市后监督（PMS）系统：

1. 制定PMS计划（第84条）
2. 确定数据收集方法
3. 建立投诉处理程序
4. 建立警戒报告流程
5. 制定定期安全更新报告（PSUR）
6. 将PMS系统与PMCF（Post-Market Clinical Follow-up）活动相结合
7. 进行趋势分析和信号检测
8. **验证：** PMS系统每年需接受审计

### PMS系统组成部分

| 组件 | 要求 | 频率 |
|-----------|-------------|-----------|
| PMS计划 | 第84条 | 需持续更新 |
| 定期安全更新报告（PSUR） | IIa类及以上等级的医疗器械 | 按类别要求定期提交 |
| PMCF计划 | 附录XIV第B部分 | 需根据CER更新 |
| PMCF报告 | 附录XIV第B部分 | III类医疗器械每年提交 |
| 警戒报告 | 第87-92条 | 根据实际情况提交 |

### 定期安全更新报告（PSUR）的提交频率

| 分类等级 | 提交频率 |
|-------|-----------|
| III类 | 每年 |
| IIb类植入式器械 | 每年 |
| IIb类其他医疗器械 | 每两年 |
| IIa类医疗器械 | 根据需要 |

### 严重事件报告

- **时间线 | 报告要求 |
|----------|-------------|
| 2天内 | 发生严重公共卫生威胁时 |
| 10天内 | 发生死亡或病情严重恶化时 |
| 15天内 | 发生其他严重事件时 |

---

## EUDAMED与UDI（European Union Unique Device Identifier）

根据第27条的要求实施UDI系统：

1. 获取发行机构的代码（GS1、HIBCC、ICCBBA）
2. 为每个医疗器械型号分配UDI-DI（唯一标识符）
3. 为每个型号分配UDI-PI（生产标识符）
4. 在产品标签上标注UDI信息
5. 在EUDAMED数据库中注册相关信息
6. 将医疗器械信息上传至EUDAMED
7. **验证：** 核实标签上的UDI信息是否正确

### EUDAMED数据库的模块

| 模块 | 内容 | 负责方 |
|--------|---------|-------|
| 制造商注册 | 公司注册信息 |
| UDI/医疗器械信息 | 包含医疗器械型号等信息 |
| 证书 | 包含认证机构颁发的证书 |
| 临床研究信息 | 包含研究注册信息 |
| 警戒报告 | 包含制造商提交的事件报告 |
| 市场监督信息 | 包含监管机构的行动记录 |

### UDI标签要求

根据第13条的要求，标签上必须包含以下内容：

- UDI-DI（唯一标识符）
- UDI-PI（生产标识符，适用于II类及以上等级的医疗器械）
- AIDC（Automatic Identification Code，条形码/RFID格式）
- HRI（Human Readable Information，人类可读信息）
- 制造商名称和地址
- 批次/序列号
- 有效期（如适用）

---

## 参考文档

### MDR分类指南

`references/mdr-classification-guide.md`包含：
- 附录VIII中的所有分类规则（规则1-22）
- 根据MDCG 2019-11标准的软件分类方法
- 分类示例
- 合规性评估途径的选择指南

### 临床证据要求

`references/clinical-evidence-requirements.md`包含：
- 临床证据框架和评估流程
- 文献检索方法
- 临床评估报告的编写指南
- PMCF（Post-Market Clinical Follow-up）计划和评估报告的编写指南

### 技术文件模板

`references/technical-documentation-templates.md`包含：
- 附录II和III的要求
- 设计历史文件的格式
- GSPR合规性评估模板
- 合规性声明模板
- 向指定认证机构提交的文件模板

---

## 工具

### MDR合规性差距分析工具

```bash
# Quick gap analysis
python scripts/mdr_gap_analyzer.py --device "Device Name" --class IIa

# JSON output for integration
python scripts/mdr_gap_analyzer.py --device "Device Name" --class III --output json

# Interactive assessment
python scripts/mdr_gap_analyzer.py --interactive
```

该工具用于分析医疗器械是否符合MDR法规的要求，识别合规性差距，并提供优先级的改进建议。

**输出内容包括：**
- 按类别划分的要求清单
- 缺陷的识别及优先级排序
- 重点突出的关键缺陷
- 合规性改进的路线图建议

---

## 指定认证机构（Notified Body）的选择

### 选择标准

| 选择因素 | 考虑因素 |
|--------|----------------|
| 认证机构的业务范围 | 是否涵盖您的医疗器械类型 |
| 认证机构的处理能力 | 初始审核的时间安排 |
| 认证机构的地理覆盖范围 | 是否覆盖您需要进入的市场 |
| 认证机构的技术专长 | 是否熟悉您的技术领域 |
| 认证机构的费用结构 | 费用的透明度和可预测性 |

### 提交前检查清单

- 技术文件是否完整 |
- GSPR合规性评估是否完成 |
- 风险管理文件是否是最新的 |
- 临床评估报告是否准备好 |
- 质量管理体系（ISO 13485）是否已通过认证 |
- 标签和使用说明书是否最终确定 |
- **验证：** 内部合规性评估是否完成
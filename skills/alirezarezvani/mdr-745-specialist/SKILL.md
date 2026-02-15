---
name: mdr-745-specialist
description: 欧盟MDR 2017/745合规专家，专注于医疗器械的分类、技术文档编制、临床证据收集以及上市后监管工作。负责处理附件VIII中的分类规则、附件II/III中的技术文件、附件XIV中的临床评估要求，以及EUDAMED（欧洲医疗器械数据库）的整合工作。
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

# MDR 2017/745 专家指南

本指南提供了欧盟医疗器械法规（MDR）中关于医疗器械分类、技术文档和临床证据的相关合规要求。

---

## 目录

- [医疗器械分类流程](#device-classification-workflow)
- [技术文档](#technical-documentation)
- [临床证据](#clinical-evidence)
- [上市后监督](#post-market-surveillance)
- [EUDAMED 和 UDI](#eudamed-and-udi)
- [参考文档](#reference-documentation)
- [工具](#tools)

---

## 医疗器械分类流程

根据 MDR 第 VIII 附录对医疗器械进行分类：

1. 确定医疗器械的使用期限（短暂使用、短期使用、长期使用）。
2. 判断医疗器械的侵入性级别（非侵入性、通过体腔使用、需要手术）。
3. 评估医疗器械与人体系统的接触部位（中枢神经系统、心脏系统等）。
4. 判断医疗器械是否具有能量输出功能。
5. 应用相应的分类规则（规则 1-22）。
6. 对于软件产品，需使用 MDCG 2019-11 算法进行分类。
7. 记录分类的依据。
8. **验证：** 将分类结果提交给指定机构（Notified Body）进行确认。

### 分类矩阵

| 因素          | I 类       | IIa 类      | IIb 类      | III 类      |
|------------------|-----------|-----------|-----------|-----------|
| 使用期限        | 任意        | 短期使用    | 长期使用    | 长期使用    |
| 侵入性级别      | 非侵入性     | 通过体腔使用 | 需要手术   | 可植入式   |
| 与人体系统的接触部位    | 中枢神经系统/心脏系统 | 其他系统    |          |
| 风险等级        | 最低        | 低至中等    | 中等到高    | 最高        |

### 软件产品的分类（MDCG 2019-11）

| 信息用途        | 条件严重性    | 分类等级    |
|------------------|------------|-----------|
| 用于决策支持     | 无严重后果    | IIa 类      |
| 用于决策支持     | 有严重后果    | IIb 类      |
| 用于驱动或治疗     | 关键功能     | III 类      |

### 分类示例

**示例 1：可吸收外科缝合线**
- 规则 8（可植入式，长期使用）
- 使用期限：> 30 天（可吸收）
- 与人体组织的接触：一般组织
- 分类：**IIb 类**

**示例 2：人工智能诊断软件**
- 规则 11 + MDCG 2019-11
- 功能：诊断严重疾病
- 分类：**IIb 类**

**示例 3：心脏起搏器**
- 规则 8（可植入式）
- 与人体系统的接触：中枢循环系统
- 分类：**III 类**

---

## 技术文档

根据 MDR 第 II 和 III 附录准备技术文档：

1. 编写医疗器械描述（包括不同型号、配件及预期用途）。
2. 制定产品标签（符合第 13 条要求）。
3. 记录产品的设计和制造过程。
4. 完成 GSPR（Good Supply Practice Requirements）合规性评估。
5. 编制风险分析报告。
6. 整合风险管理文件（ISO 14971 标准）。
7. **验证：** 技术文档的完整性需经过审核。

### 技术文档结构

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

### GSPR 合规性检查清单

| 要求                | 证据                | 状态        |
|------------------|------------------|-----------|
| 安全设计            | 风险管理文件            | ☐         |
| 化学性质            | 生物相容性报告            | ☐         |
| 感染风险            | 灭菌验证              | ☐         |
| 软件要求            | IEC 62304 标准文档        | ☐         |
| 标签                | 标签设计和使用说明书         | ☐         |

### 合规性评估途径

| 分类等级            | 评估途径              | 指定机构参与程度 |
|------------------|------------------|-------------|
| I 类               | 自我声明（符合第 II 附录）       | 无需指定机构参与 |
| IIa 类/II 类（植入式/测量设备） | 第 II 附录 + 第 IX/XI 附录     | 需指定机构参与 |
| IIb 类               | 第 IX 附录 + 第 X 或 XI 附录     | 需指定机构参与（类型测试和生产过程） |
| III 类               | 第 IX 附录 + 第 X 附录       | 需指定机构参与（全面质量管理体系和类型测试） |

---

## 临床证据

根据 MDR 第 XIV 附录制定临床证据策略：

1. 明确临床声明和评估指标。
2. 进行系统性文献搜索。
3. 评估临床数据的质量。
4. 评估临床数据的等效性（技术、生物学、临床方面）。
5. 识别证据缺口。
6. 判断是否需要进行临床研究。
7. 编制临床评估报告（CER）。
8. **验证：** CER 需由合格评估机构审核。

### 各分类等级的临床证据要求

| 分类等级 | 最低证据要求 | 评估方式       |
|---------|-------------|-------------|
| I 类       | 风险-收益分析         | 通常不需要     |
| IIa 类       | 文献资料 + 上市后数据     | 可能需要     |
| IIb 类       | 系统性文献回顾       | 通常需要     |
| III 类       | 全面的临床数据       | 必须提供     |

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

- 拥有医学学位或同等医疗资质。
- 在相关领域具有 4 年以上的临床经验。
- 接受过临床评估方法论的培训。
- 熟悉 MDR 的相关要求。

---

## 上市后监督

根据 MDR 第 VII 附录建立上市后监督（PMS）系统：

1. 制定 PMS 计划（第 84 条）。
2. 确定数据收集方法。
3. 建立投诉处理程序。
4. 建立警戒报告流程。
5. 制定定期安全更新报告（PSUR）。
6. 将 PMS 系统与 PMCF（Post-Market Clinical Follow-up）活动相结合。
7. 进行趋势分析和信号检测。
8. **验证：** PMS 系统每年接受审核。

### PMS 系统组成部分

| 组件            | 要求                | 频率        |
|------------------|------------------|-------------|
| PMS 计划          | 第 84 条           | 必须制定     |
| PSUR            | IIa 类及以上等级         | 按类别定期提交   |
| PMCF 计划          | 第 XIV 附录 B          | 随 CER 更新    |
| PMCF 报告          | 第 XIV 附录 B          | III 类产品每年提交 |
| 警戒报告          | 第 87-92 条         | 根据事件发生情况提交 |

### PSUR 提交频率

| 分类等级            | 提交频率        |
|------------------|-------------|
| III 类             | 每年            |
| IIb 类（可植入式产品）      | 每年            |
| IIb 类（其他产品）       | 每两年          |
| IIa 类             | 根据需要        |

### 严重事件报告

- **时间线** | **报告要求** |
|------------|-------------|
| 2 天        | 造成严重公共卫生威胁的事件 |
| 10 天        | 导致死亡或病情恶化的事件 |
| 15 天        | 其他严重事件       |

---

## EUDAMED 和 UDI

根据第 27 条实施 UDI（Unique Device Identifier）系统：

1. 获取发行机构的代码（GS1、HIBCC、ICCBBA）。
2. 为每个医疗器械型号分配 UDI-DI（唯一设备标识符）和 UDI-PI（生产标识符）。
3. 在标签上标注 UDI 信息。
4. 在 EUDAMED 数据库中注册相关信息。
5. 在设备上市后及时上传相关证书。
8. **验证：** 标签上的 UDI 信息需经过验证。

### EUDAMED 的主要模块

| 模块            | 内容                | 负责注册的机构    |
|------------------|------------------|-------------|
| 注册机构          | 制造商或授权注册机构       |
| UDI/设备信息        | 设备和型号详细信息      | 制造商       |
| 证书            | 相关认证机构的证书      | 指定机构     |
| 临床研究          | 研究注册信息        | 项目发起者     |
| 警戒报告          | 事件报告          | 制造商       |
| 市场监督          | 相关监管机构的行动      | 监管机构     |

### UDI 标签要求

根据第 13 条，标签上必须包含以下内容：

- UDI-DI（唯一设备标识符）
- UDI-PI（生产标识符，适用于 II 类及以上等级）
- AIDC（Automatic Identification Code）格式（条形码/RFID）
- HRI（Human-readable Information）格式（便于人类阅读）
- 制造商名称和地址
- 批次/序列号
- 有效期（如适用）

---

## 参考文档

### MDR 分类指南

`references/mdr-classification-guide.md` 包含：

- MDR 第 VIII 附录中的完整分类规则（规则 1-22）
- 根据 MDCG 2019-11 的软件产品分类方法
- 分类示例
- 合规性评估途径的选择指南

### 临床证据要求

`references/clinical-evidence-requirements.md` 包含：

- 临床证据框架和层级结构
- 文献搜索方法
- 临床评估报告的编写指南
- PMCF（Post-Market Clinical Follow-up）计划和评估报告的编写指导

### 技术文档模板

`references/technical-documentation-templates.md` 包含：

- MDR 第 II 和 III 附录的要求
- 设计历史文件的结构
- GSPR 合规性评估模板
- 合规性声明模板
- 向指定机构提交的文件清单

---

## 工具

### MDR 合规性差距分析工具

```bash
# Quick gap analysis
python scripts/mdr_gap_analyzer.py --device "Device Name" --class IIa

# JSON output for integration
python scripts/mdr_gap_analyzer.py --device "Device Name" --class III --output json

# Interactive assessment
python scripts/mdr_gap_analyzer.py --interactive
```

该工具用于分析医疗器械是否符合 MDR 的要求，识别合规性差距，并提供优先级的改进建议。

**输出内容包括：**
- 按类别划分的要求清单
- 危险差距的识别及优先级排序
- 关键差距的突出显示
- 合规性改进的行动计划建议

---

## 指定机构（Notified Body）的选择

### 选择标准

| 选择因素            | 考虑因素                |
|------------------|------------------------|
| 指定机构的业务范围       | 是否涵盖您的产品类型         |
| 技术能力           | 是否具备处理您产品的技术能力     |
| 地理覆盖范围         | 是否能覆盖您目标市场         |
| 技术专长           | 是否有处理类似技术的经验       |
| 费用结构           | 费用的透明度和可预测性         |

### 提交前的检查清单

- 技术文档是否完整             |
- GSPR 合规性评估是否完成         |
- 风险管理文件是否是最新的         |
- 临床评估报告是否准备好         |
- 质量管理体系（ISO 13485）是否通过认证     |
- 标签和使用说明书是否最终确定       |
- **验证：** 内部合规性评估是否完成     |
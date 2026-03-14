---
name: ee-datasheet-master
description: "**使用场景：**  
当用户正在阅读组件的数据手册或规格书时，用于查找芯片的相关参数，如引脚排列（pinout）、工作电压、I2C地址、时序信息、寄存器映射以及电气特性等。适用于用户对PDF文件或芯片本身存在疑问的情况。  
**适用对象：** 所有类型的集成电路（IC）。"
---
# EE 数据手册指南

## 基本原则：仅使用 PDF 内容

```
ALL DATA MUST ORIGINATE FROM THE PDF.
Allowed: Extract → Calculate from extracted data
Forbidden: Use prior knowledge → Fill gaps with guesses
```

### 允许的数据处理方式

| 处理类型 | 例子 |
|------|---------|
| 数学计算 | 从电压和电流计算功率 P = V × I |
| 单位转换 | dBm → mW, 二进制 → 十六进制 |
| 地址解析 | "001000x" → 0x10/0x11 |
| 组件数量统计 | 从“引脚描述”表中获取引脚数量 |

**在进行数据处理时，请务必展示原始数据来源（页面）、计算步骤及最终结果。**

### 禁止的行为

| 不允许的行为 | 应采取的纠正措施 |
|----------|------------|
| “我知道这个芯片的规格...” | 请在 PDF 中查找相关规格 |
| “典型值是...” | 请直接从 PDF 中读取实际数值 |
| “类似芯片的规格是...” | 该芯片的规格可能有所不同 |
| 通过猜测来填补信息空白 | 应输出“数据手册中未指定该参数”并说明获取途径（见下文） |

---

## 当 PDF 无法提供所需信息时

“数据手册中未指定该参数”并不意味着无法获取信息。此时应说明**如何获取缺失的信息**。

### 回答模板

> “[参数] 在本数据手册中未列出。
> 请通过[具体方法]获取该参数。”

如果数据手册中提到了某份应用说明或补充文档，请注明其名称：
> “第 X 节参考了应用说明 [AN-xxx] 来说明该参数的详细信息——请访问[制造商] 的官方网站进行查询。”

### 缺失参数的推理流程

当某个参数缺失时，请通过以下问题进行推理，以确定获取该参数的具体方法：

**1. 为什么该参数缺失？**
- *文档类型错误*——当前查看的是简版数据手册或产品简介手册，完整的技术手册或应用说明中可能包含该参数 → 请确认正确的文档名称。
- *测试条件不匹配*——虽然规格存在，但不适用于用户的具体使用条件（如负载、频率、温度等） → 请说明具体差异及其对参数值的影响。
- *参数依赖于外部组件或 PCB 布局*——该参数的值受用户可控制的外部组件或 PCB 布局影响 → 请说明决定该参数的因素以及如何计算或模拟其值。
- *数据由制造商控制*——该参数来自内部测试数据，未公开发布 → 请确认正确的信息获取渠道。

**2. 用户实际需要该参数用于什么目的？**
- 设计裕度检查 → 可以使用近似值或最坏情况下的限值。
- 故障调试 → 在实际电路中进行直接测量通常比依赖数据手册中的数值更可靠。
- 合规性验证 → 仅接受制造商提供的官方数据。

**3. 鉴于以上情况，最直接的获取途径是什么？**
根据具体参数和用途提供相应的建议——例如，对于高温环境下的 LDO（低压差线性稳压器），其热阻的测量方法与信号路径运算放大器的测量方法不同。需要考虑：使用何种设备进行测量、哪些文档包含相关规格，或者如何根据用户可测量的参数或可控制的因素来计算该参数的值。

---

## 六阶段工作流程

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 0: Pre-scan        →  全文扫描，建结构地图            │
│  Phase 1: Diagnosis       →  text vs image PDF 决策         │
│  Phase 2: Device ID       →  确认器件，推断关键参数          │
│  Phase 2b: Targeted Scan  →  推断 patterns，二次精准扫描     │
│  Phase 3: Section Mapping →  定位各功能区页码               │
│  Phase 4: Extraction      →  精准提取 + TEMPLATES 结构化输出 │
└─────────────────────────────────────────────────────────────┘
```

**有关入口决策表和详细工作流程，请参阅 [PDF_STRATEG.md](PDF_STRATEG.md)。在运行任何命令之前，请先阅读该文件，以确定从哪个阶段开始操作。**

### 快速参考

**常见情况——设备名称已知，需要查询 1–2 个具体参数（从这里开始操作）：**
```bash
# Phase 3: Search directly for the parameter the user asked about
python scripts/pdf_tools.py search_table <pdf_path> "<parameter>"   # e.g. "quiescent current", "dropout voltage"
python scripts/pdf_tools.py search <pdf_path> "<parameter>"         # try alternate phrasings if first is empty

# Phase 4: Read the identified page
python scripts/pdf_tools.py text <pdf_path> <page_num>
python scripts/pdf_tools.py tables <pdf_path> <page_num>
```

**特殊情况——PDF 未知、需要开放式分析或需要提取多个参数时：**
```bash
# Phase 0: Pre-scan (slow — only when you need a structural map)
python scripts/pdf_tools.py info <pdf_path>
python scripts/pdf_tools.py page_hints <pdf_path>        # scan ALL pages → minutes on large docs

# Phase 2: Identify Device (only if device is not already known)
python scripts/pdf_tools.py text <pdf_path> 1

# Phase 2b: Targeted re-scan (complex ICs only — charger, MCU, CODEC)
python scripts/pdf_tools.py dump_patterns > /tmp/custom_patterns.json
python scripts/pdf_tools.py page_hints <pdf_path> --patterns /tmp/custom_patterns.json

# Phase 3: Caption-based section mapping
python scripts/pdf_tools.py search_caption <pdf_path>    # find Figure/Table captions
python scripts/pdf_tools.py search <pdf_path> "Electrical Characteristics"
```

---

## 参数推断（基于大型语言模型）

### 通用参数（仅适用于需要全面分析的情况）

当用户要求进行完整分析或获取概览时，请提取以下 5 个基础参数。**针对单一参数的查询请跳过此步骤**——例如，如果用户询问“压降电压是多少？”，则直接查找该参数的详细信息，而非设备的封装类型。

| 参数 | 搜索关键词 | 备注 |
|-----------|----------------|-------|
| **制造商** | 第一页页眉/页脚 | 公司名称 |
| **部件编号** | 第一页标题 | 完整的部件编号 |
| **封装类型** | “Package” | 必须包含引脚数量（例如：QFN-32） |
| **工作电压** | “VDD”、“VCC”、“Supply Voltage” | 电压范围：最小值到最大值 |
| **工作温度** | “Operating Temperature” | 温度范围：最小值到最大值 |

### 设备特定参数（通过大型语言模型推断）

确定设备类型后，需要推断哪些参数是关键的：

```
1. Read device description (first 3 pages)
2. Understand: What does this device DO?
3. Infer: What specs matter for this device?
4. Search: Use pdf_tools to locate those specs
```

有关完整设备类型的参数查找表及针对每种设备的参数提取方法，请参阅 **[PDF_STRATEG.md → 第二阶段和设备类型快捷指南](PDF_STRATEG.md)**。

**关键提示：**设备描述中会提示需要测量哪些参数。请勿使用预定义的参数列表。

---

## 输出格式

```markdown
# [Part Number] Datasheet Analysis

## Summary
[1-2 sentences]

## Key Specifications
| Parameter | Min | Typ | Max | Unit | Source | Notes |
|-----------|-----|-----|-----|------|--------|-------|
| ... | ... | ... | ... | ... | Page X, "Table Name" | |
| [unavailable param] | — | — | — | ... | NOT SPECIFIED | Measure: [method] |

## Pin Configuration
- Package: [Type]-[Pin Count]
- Power Domains: [List ALL with pin numbers]
- Interfaces: [I2C/SPI/UART with addresses]

## Critical Design Considerations
1. [Issue with guidance]

## Common Pitfalls
- [Pitfall]: [How to avoid]
```

---

## 常见错误

| 错误类型 | 例子 | 纠正方法 |
|---------|---------|------------|
| 引脚数量缺失 | 写成“QFN封装” | 应写成“QFN-32 封装” |
| 仅提及部分电源域 | 只写“VDD” | 应完整写出电源域的范围（例如：“VDD（引脚 1、13、32）” |
| I2C 地址错误 | 写成“0x18” | 应根据格式计算正确的地址 |
| 未标注数据来源 | 写成“信噪比：93 dB” | 应注明数据来源（例如：“信噪比：93 dB（第 8 页，典型值）” |
| 提供无依据的数值 | 提供任何未经验证的数值 | 必须标注数据来源（页面和表格编号） |

---

## 注意事项——遇到问题时请立即停止并核实信息

如果出现以下情况，请立即停止操作并重新查阅 PDF 或从原始资料中核实信息：

- “我知道这个芯片的规格…”
- “通常这个参数的值是……”
- “根据我的经验……”
- “类似芯片的规格是……”

---

## 参考文件

| 文件名称 | 用途 |
|------|---------|
| [PDF_STRATEG.md](PDF_STRATEG.md) | 六阶段工作流程及设备类型参数提取方法 |
| [TEMPLATES.md](TEMPLATES.md) | 结构化的输出模板（包括设备信息、电源域、I2C 接口、电气规格等） |
| [scripts/pdf_tools.py](scripts/pdf_tools.py) | 用于提取 PDF 数据的工具脚本 |
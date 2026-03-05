---
name: doc-process
description: >
  多功能文档智能技能：  
  - 对文档进行分类；  
  - 自动填写表格；  
  - 分析合同（识别风险/警示信息）；  
  - 扫描收据和发票；  
  - 分析银行对账单（检测订阅信息、异常情况及税收减免）；  
  - 解析简历/求职信；  
  - 扫描身份证件和护照（支持MRZ码解码）；  
  - 概述医疗记录内容；  
  - 保护个人身份信息（PII）和敏感数据（提供轻量级、标准级或高级保护模式）；  
  - 提取会议纪要和待办事项；  
  - 将表格数据导出为CSV/JSON格式；  
  - 翻译文档内容；  
  - 扫描并调整文档图片的格式（使其看起来像是扫描后的效果）。  
  可触发操作：  
  - 填写此表格；  
  - 自动填写相关信息；  
  - 审查该合同；  
  - 检查是否存在风险/警示信息；  
  - 扫描这张收据；  
  - 记录这笔开支；  
  - 分析我的银行对账单；  
  - 解析我的简历；  
  - 扫描我的护照；  
  - 读取我的身份证件信息；  
  - 概述这份实验报告的内容；  
  - 保护文档中的个人身份信息；  
  - 对文档进行匿名处理；  
  - 提取会议纪要和待办事项；  
  - 将表格数据导出为CSV格式；  
  - 翻译这份文档；  
  - 扫描这张图片；  
  - 识别这张图片的类型；  
  - 分析这份文档的内容。
allowed-tools: [Read, Write, Edit, Bash, Glob]
---
# Doc-Process — 文档智能技能

## 功能实现方式

该技能中的大多数功能完全依赖于Claude自身的视觉和语言处理能力实现——**无需使用任何外部库或脚本**。仅有少数可选模式会调用依赖于第三方库的Python脚本。

### 功能与实现方式对应关系

| 功能 | 实现原理 | 是否需要外部库？ |
|---|---|---|
| OCR/图像识别 | Claude内置的多模态视觉识别功能 | **无需** |
| MRZ解码（护照/身份证） | Claude通过视觉方式解析MRZ编码 | **无需** |
| PDF阅读 | Claude直接读取PDF文本内容 | **无需** |
| 表单自动填写 | Claude读取表单字段并生成填写结果 | **无需** |
| 合同分析 | Claude读取合同内容并应用规则进行解析 | **无需** |
| 收据扫描 | Claude读取图像或PDF文件 | **无需** |
| 银行对账单分析（PDF格式） | Claude直接读取PDF页面内容 | **无需** |
| 银行对账单分析（CSV格式） | 使用`statement_parser.py`（纯Python标准库） | **无需** |
| 费用记录 | 使用`expense_logger.py`（纯Python标准库） | **无需** |
| 银行报告生成 | 使用`report_generator.py`（纯Python标准库） | **无需** |
| 简历/简历解析 | Claude读取文档内容 | **无需** |
| 医疗摘要生成 | Claude读取医疗相关文档 | **无需** |
| 法律文本编辑 | Claude对文本进行编辑处理 | **无需** |
| 会议记录转录 | 使用`redactor.py`（纯Python标准库） | **无需** |
| 会议记录（文本/PDF格式） | Claude读取会议记录 | **无需** |
| 翻译 | Claude的多语言处理能力 | **无需** |
| 文档分类 | Claude读取文档的前1-2页内容 | **无需** |
| 时间线记录 | 使用`timeline_manager.py`（纯Python标准库） | **无需** |
| 从PDF中提取表格数据 | 使用`table extractor.py`及`pdfplumber`库 | **需要pdfplumber库** |
| 音频转录 | 使用`audio_transcriber.py`及`openai-whisper`/`ffmpeg` | **首次运行时需要从互联网下载模型文件** |

---

## 依赖关系及安装说明

### 核心功能无需安装依赖

所有文档阅读、分析、表单填写、合同审核、收据扫描、银行对账单分析（PDF格式）、简历解析等功能均基于Claude的本地能力实现，无需安装任何Python包。

### 可选依赖（仅针对使用相关脚本的模式）

仅在使用以下脚本时才需要安装相应的依赖库：

```bash
# Table extraction from PDFs (table_extractor.py)
pip install pdfplumber>=0.11

# Audio transcription of meeting recordings (audio_transcriber.py)
# Also requires ffmpeg — install separately: https://ffmpeg.org/download.html
pip install openai-whisper>=20231117

# Doc scan / perspective correction (doc_scanner.py in the doc-scan skill)
pip install opencv-python-headless>=4.9 Pillow>=10.0 numpy>=1.24
pip install img2pdf>=0.5  # optional — for PDF output; Pillow fallback used if absent
```

所有依赖库的详细信息均列在仓库根目录下的`requirements.txt`文件中。

### 二进制依赖库

| 二进制库 | 所需依赖的库 | 安装方法 |
|---|---|---|
| `ffmpeg` | `audio_transcriber.py` | 使用`brew install ffmpeg`或`apt install ffmpeg`，或访问[官方网站](https://ffmpeg.org/download.html)下载 |
| **（注：实际安装命令可能因操作系统而异）** |

### 安装过程中的网络访问

- **`openai-whisper`**：仅在首次运行时从OpenAI/HuggingFace服务器下载模型文件，后续运行会使用本地缓存的模型文件（缓存路径为`~/.cache/whisper/`）。之后无需再访问网络。 |
- 其他所有脚本在安装完成后均可独立运行，无需网络连接。

### 脚本导入检查

| 脚本 | 所需导入的库 | 是否依赖第三方库？ | 是否需要网络连接？ |
|---|---|---|---|
| `timeline_manager.py` | `argparse`, `json`, `sys`, `datetime`, `pathlib`, `uuid`, `collections` | **无需** | **无需网络连接** |
| `redactor.py` | `argparse`, `re`, `sys`, `pathlib`, `dataclasses` | **无需** | **无需网络连接** |
| `expense_logger.py` | `argparse`, `csv`, `json`, `sys`, `pathlib` | **无需** | **无需网络连接** |
| `statement_parser.py` | `argparse`, `csv`, `json`, `re`, `sys`, `collections`, `datetime`, `pathlib` | **无需** | **无需网络连接** |
| `report_generator.py` | `argparse`, `json`, `sys`, `collections`, `pathlib` | **无需** | **无需网络连接** |
| `utils.py` | `re`, `unicodedata`, `datetime`, `pathlib` | **无需** | **无需网络连接** |
| `audio_transcriber.py` | `argparse`, `sys`, `pathlib` + `openai-whisper` | **仅在首次运行时需要下载模型** |
| `table_extractor.py` | `argparse`, `csv`, `io`, `json`, `sys`, `pathlib` + `pdfplumber` | **需要pdfplumber库** | **无需网络连接** |
| `doc_scanner.py` | `argparse`, `json`, `sys`, `time`, `pathlib` + `cv2`, `numpy`, `Pillow` | **需要opencv, Pillow, numpy库** | **无需网络连接** |

您可以通过输入“show me the source of [脚本名称]”来查看脚本的源代码。

---

## 隐私与数据保护

| 功能 | 数据处理方式 |
|---|---|
| **文档内容** | 仅在当前会话期间在本地读取，不会被存储、索引或传输。 |
| **表单自动填写所需的数据** | 仅用于完成当前表单填写，不会写入文件，会话结束后会被清除。 |
| **时间线记录** | 需要用户明确同意后才会进行记录；记录内容仅包含文档类别信息，不包含原始文档内容。 |
| **编辑后的输出文件** | 仅保存在用户指定的路径中。 |
| **音频转录文件** | 保存在用户指定的本地文件中；模型文件仅在首次使用`openai-whisper`时下载。 |
| **无数据监控** | 该技能不进行数据分析、使用情况报告或远程数据传输。 |

---

## 第1步：选择处理模式

### 明确模式选择

如果用户明确指定了处理需求，直接选择相应的模式：

| 模式 | 用户指令示例 | 常见文件类型 |
|---|---|---|
| **文档分类** | “处理这个文件”、“这是什么？”、“分析这个文件”等 | 任意类型的文档 |
| 表单自动填写 | “填写这个表单” | PDF表单、图片、截图 |
| 合同分析 | “审核合同”、“总结合同内容” | PDF文件、文本文件 |
| 收据扫描 | “扫描这张收据” | 照片、图片、PDF文件 |
| 银行对账单分析 | “分析银行对账单” | PDF文件、CSV文件 |
| 简历/简历解析 | “解析简历” | PDF文件、图片、文本文件 |
| 身份证/护照扫描 | “扫描身份证” | 照片、图片、PDF文件 |
| 医疗摘要生成 | “生成医疗摘要” | PDF文件、图片、文本文件 |
| 法律文本编辑 | “编辑文本” | 包含个人身份信息（PII）的文档 |
| 会议记录 | “转录会议记录” | 文本文件、PDF文件、音频文件 |
| 表格提取 | “从文档中提取表格数据” | PDF文件、图片、文本文件 |
| 文档翻译 | “翻译这个文件” | 任意类型的文档 |
| 文档时间线 | “查看我的文档处理历史” | 任意类型的文档 |
| 文档扫描 | “扫描这张图片” | 照片、图片 |

### 模式选择不明确时的处理方式

如果用户上传文件时未明确指定处理模式，**请先询问用户**：

> “我可以自动对文档进行分类，以推荐最适合的处理方式——这需要我先阅读文档的前1-2页。或者，您也可以直接选择以下模式：”
>
| 模式 | 适用场景 |
|---|---|
| 表单自动填写 | 包含填写字段的表单 |
| 合同分析 | 合同、保密协议、租赁协议等 |
| 收据扫描 | 收据、发票 |
| 银行对账单分析 | 银行对账单、信用卡对账单 |
| 简历解析 | 简历文件 |
| 身份证/护照扫描 | 身份证、护照等 |
| 医疗摘要生成 | 医疗报告、化验单、处方等 |
| 法律文本编辑 | 包含个人身份信息的文档 |
| 会议记录 | 会议记录 |
| 表格提取 | 包含表格数据的文档 |
| 文档翻译 | 非英语文档 |

**只有在用户选择“自动分类”或明确指定模式后，才会开始读取文档。**

---

## 第2步：读取文档

使用`Read`工具读取上传的文件。对于图片，Claude会通过视觉方式识别内容；对于超过10页的PDF文件，会分页读取。

**对于音频文件（仅适用于会议记录模式）：** 在运行前请确认用户是否需要使用`openai-whisper`库（首次运行时会从OpenAI服务器下载模型文件）：

> “转录这个音频文件需要`openai-whisper`库。首次运行时会从OpenAI服务器下载模型文件（默认模型大小约为140MB）。您确认吗？”

如果用户同意，继续执行后续步骤；否则，请询问用户是否可以提供文本转录版本。

---

## 第3步：执行选定的处理模式

根据所选模式，执行相应的处理流程：

- 文档分类：`references/document-categorizer.md`
- 表单自动填写：`references/form-autofill.md`
- 合同分析：`references/contract-analyzer.md`
- 收据扫描：`references/receipt-scanner.md`
- 银行对账单分析：`references/bank-statement-analyzer.md`
- 简历/简历解析：`references/resume-parser.md`
- 身份证/护照扫描：`references/id-scanner.md`
- 医疗摘要生成：`references/medical-summarizer.md`
- 法律文本编辑：`references/legal-redactor.md`
- 会议记录：`references/meeting-minutes.md`
- 表格提取：`references/table-extractor.md`
- 文档翻译：`references/document-translator.md`
- 文档时间线：`references/document-timeline.md`
- 文档扫描：由`doc-scan`技能处理（单独的技能）

---

## 第4步：使用辅助脚本

| 脚本 | 所需依赖库 | 功能 | 示例用法 |
|---|---|---|---|
| `scripts/expense_logger.py` | 无 | 添加/记录/汇总/编辑/删除费用记录 | `python scripts/expense_logger.py add --date 2024-03-15 --merchant "Starbucks" --amount 13.12 --file expenses.csv` |
| `scripts/statement_parser.py` | 无 | 解析银行对账单CSV文件并分类交易记录 | `python scripts/statement_parser.py --file statement.csv --output categorized.json` |
| `scripts/report_generator.py` | 无 | 将分类后的数据格式化为Markdown报告 | `python scripts/report_generator.py --file categorized.json --type bank` |
| `scripts/redactor.py` | 无 | 对文本文件进行基于正则表达式的个人身份信息（PII）编辑 | `python scripts/redactor.py --file document.txt --output redacted.txt --mode full` |
| `scripts/timeline_manager.py` | 无 | 管理文档处理的时间线记录 | `python scripts/timeline_manager.py show` |
| `scripts/audio_transcriber.py` | `openai-whisper`, `ffmpeg` | 将音频文件转录为文本 | `python scripts/audio_transcriber.py --file meeting.mp3 --output transcript.txt` |
| `scripts/table_extractor.py` | `pdfplumber` | 从PDF文件中提取表格数据并转换为CSV或JSON | `python scripts/table_extractor.py --file document.pdf --output data.csv` |

**无明确依赖库的脚本仅使用Python标准库；有依赖库的脚本会在导入时检查库的可用性，并在缺少库时提示用户安装。**

---

## 第5步：启用文档时间线功能（可选）

时间线功能默认是关闭的。只有在用户明确同意后，才能通过`timeline_manager.py`添加记录。

### 同意提示（首次处理文档时）

在完成第一个文档处理任务后，询问用户是否希望启用时间线记录：

> “您是否希望我为本次会话生成处理日志？日志会记录文档类型、文件名以及文档的类别信息（不包含原始内容和个人数据），保存在`~/.doc-process-timeline.json`文件中。此功能完全可选。”

- **同意** → 启用时间线记录，开始记录当前文档及后续文档的处理信息，并在每次记录时提示“已保存到时间线。” |
- **拒绝** → 不生成时间线记录，后续不再提示。 |
- **未回答/不确定** → 视为用户不同意。

### 规范要求

- 使用`--summary`参数时，禁止记录包含姓名、身份证号码、出生日期、地址、账号号码、银行卡号码、医疗数据等可能识别个人身份的信息；仅允许使用类别级别的描述。

---

## 第6步：展示结果

结果以表格形式呈现，表格标题遵循相应参考文档的格式要求。每次展示结果时，都会提供与处理模式相关的操作提示。

---

## 其他原则

- **先分类再处理**——但需用户明确同意自动分类。 |
- **不会伪造字段内容**：未知字段会标记为[MISSING]或[UNREADABLE]。 |
- **谨慎标记风险信息**：对不确定的内容一律标记为风险项。 |
- **保持结果清晰可读**：使用表格和项目符号格式化结果。 |
- **仅展示处理过程中必要的敏感数据**。 |
- **根据参考文档的要求，务必添加必要的免责声明**（如医疗、法律、隐私相关内容）。 |
- **时间线功能需用户明确同意后方可使用**。未经同意不得记录任何数据。 |
- **表单自动填写涉及的个人数据仅用于当前会话，不会保存到文件中**。 |
- **在使用依赖第三方库的脚本前**，请确认用户已安装相关库或愿意安装。
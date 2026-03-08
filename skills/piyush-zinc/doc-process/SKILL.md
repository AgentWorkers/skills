---
name: doc-process
description: >
  文档智能功能：  
  - 对文档进行分类；  
  - 自动填写表格；  
  - 分析合同内容；  
  - 扫描收据/发票；  
  - 分析银行对账单；  
  - 解析简历/求职信；  
  - 扫描身份证件/护照（包含MRZ区域）；  
  - 概述医疗记录内容；  
  - 对个人身份信息（PII）进行脱敏处理（轻度/标准/完全脱敏，支持50多种脱敏规则，全球适用）；  
  - 提取会议纪要及待办事项；  
  - 将表格数据导出为CSV/JSON格式；  
  - 翻译文档内容；  
  - 对扫描后的文档图片进行校正（包括边缘检测、视角调整等）；  
  - 提供多种文档处理功能（如“触发：填写此表格”、“自动填写”、“审核合同”、“识别风险提示”、“扫描收据”、“记录支出”、“解析简历”、“扫描护照”、“读取身份证信息”、“解析实验室报告”、“脱敏数据”、“匿名化处理”、“生成会议纪要”、“提取表格数据”、“将表格导出为CSV”、“翻译文档”、“校正图片视角”等）。  
  示例操作：  
  - “触发：填写此表格”：当用户点击相应按钮时，系统会自动填写表格中的空白字段。  
  - “自动填写”：系统会根据用户提供的信息自动填充表格中的数据。  
  - “审核合同”：系统会分析合同内容，检测潜在的法律风险或问题。  
  - “扫描收据”：用户可上传收据图片，系统会自动识别并提取关键信息。  
  - “记录支出”：用户可上传支出凭证，系统会记录相关信息。  
  - “解析简历”：系统会自动提取简历中的关键信息。  
  - “扫描护照”：用户可上传护照图片，系统会识别护照上的个人信息并进行处理。
allowed-tools: [Read, Write, Edit, Bash, Glob]
---
# 文档智能技能 — Doc-Process

## 第0步 — 自动设置（首次使用时运行一次）

在会话中首次调用任何脚本之前，请检查该脚本所需的依赖项是否已经安装。如果缺少任何依赖项，请自动运行设置脚本——无需用户提示：

```bash
bash skills/doc-process/setup.sh
```

此脚本会安装所有Python包（`pymupdf`、`Pillow`、`pytesseract`、`opencv-python-headless`、`numpy`、`img2pdf`、`pdfplumber`、`openai-whisper`），并根据操作系统平台通过`brew`或`apt`尝试安装系统二进制文件（`tesseract`、`ffmpeg`）。

**何时运行第0步：**
- 会话中首次使用任何脚本辅助模式时
- 在重新安装`clawhub install piyush-zinc/doc-process`之后
- 如果脚本因`ModuleNotFoundError`或`ImportError`而失败时

**仅安装Python包（不安装系统包）：**
```bash
bash skills/doc-process/setup.sh --light
```

或者直接从技能的`requirements.txt`文件中安装依赖项：
```bash
pip install -r skills/doc-process/requirements.txt
```

> **注意：** `openai-whisper`会在首次进行音频转录时下载其模型文件（约140 MB），而不是在安装时下载。

---

## 概述

该技能利用Claude的原生视觉/语言能力进行文档阅读和分析，并通过Python脚本处理文件输出操作。大多数模式无需额外安装任何软件——只有文件输出脚本需要第三方库。

---

## 功能实现方式

| 功能 | 实现方式 | 使用的第三方库 |
|---|---|---|
| OCR / 图像阅读 | Claude内置的视觉处理能力 | 无 |
| MRZ解码（护照/身份证） | Claude通过视觉识别MRZ代码，并应用ICAO算法 | 无 |
| PDF阅读 | Claude读取PDF中的文本层或进行视觉识别 | 无 |
| 表单自动填充 | Claude读取表单字段并生成填充后的表格 | 无 |
| 合同分析 | Claude应用预定义的规则集 | 无 |
| 收据/发票扫描 | Claude读取图像或PDF文件 | 无 |
| 银行对账单（PDF） | Claude读取PDF页面 | 无 |
| 银行对账单（CSV） | 使用`statement_parser.py`（纯Python标准库） | 无 |
| 费用记录 | 使用`expense_logger.py`（纯Python标准库） | 无 |
| 银行报告生成 | 使用`report_generator.py`（纯Python标准库） | 无 |
| 简历/简历解析 | Claude读取文档内容 | 无 |
| 医疗摘要 | Claude读取文档内容 | 无 |
| 法律编辑（显示结果） | Claude对文本进行标记处理 | 无 |
| **法律编辑（文件输出）** | 使用`redactor.py`；依赖`pymupdf`（PDF格式）；`Pillow + pytesseract`（图像处理） |
| 会议记录（文本/PDF） | Claude读取文档内容 | 无 |
| 翻译 | Claude的多语言处理能力 | 无 |
| 文档分类 | Claude读取文档的前1-2页 | 无 |
| 时间线记录 | 使用`timeline_manager.py`（纯Python标准库） | 无 |
| **表格提取（PDF）** | 使用`tableExtractor.py`；依赖`pdfplumber` | 无 |
| **音频转录** | 使用`audio_transcriber.py`；依赖`openai-whisper`和`ffmpeg` | 无 |
| **文档扫描/透视校正** | 使用`doc_scanner.py`；依赖`opencv-python-headless`、`numpy`、`Pillow`；`img2pdf`（可选） |

---

## 依赖项及安装

### 核心功能无需安装
文档阅读、分析、表单填充、合同审核、收据扫描、银行对账单分析（PDF）、简历解析、身份证扫描、医疗摘要生成、法律编辑、会议记录生成和翻译等功能均基于Claude的内置功能。

### 可选依赖项（仅针对文件输出脚本）

```bash
# PII redaction to PDF/image files  (redactor.py)
pip install pymupdf>=1.23          # required for PDF redaction
pip install Pillow>=10.0           # required for image redaction
pip install pytesseract>=0.3       # required for image redaction (also: brew install tesseract)

# Document scanning / perspective correction  (doc_scanner.py)
pip install opencv-python-headless>=4.9 numpy>=1.24 Pillow>=10.0
pip install img2pdf>=0.5           # optional — for PDF output; Pillow fallback used if absent

# Table extraction from PDFs  (table_extractor.py)
pip install pdfplumber>=0.11

# Audio transcription  (audio_transcriber.py)
# Also requires ffmpeg binary: brew install ffmpeg  /  apt install ffmpeg
pip install openai-whisper>=20231117
```

所有依赖项也列在仓库根目录下的`requirements.txt`文件中。

### 二进制依赖项

| 二进制文件 | 所需脚本 | 安装方式 |
|---|---|---|
| `tesseract` | `redactor.py`（图像处理模式） | 使用`brew install tesseract`或`apt install tesseract-ocr`安装 |
| `ffmpeg` | `audio_transcriber.py` | 使用`brew install ffmpeg`或`apt install ffmpeg`安装 |

### 网络访问

`openai-whisper`仅在首次运行时从OpenAI/HuggingFace服务器下载模型文件（约140 MB）。下载后的模型文件会缓存在`~/.cache/whisper/`目录中。其他所有脚本在安装完成后均为本地运行。

---

## 脚本参考

| 脚本 | 依赖项 | 功能 | 示例 |
|---|---|---|---|
| `redactor.py` | `pymupdf`；`Pillow + pytesseract`（图像处理模式） | 将包含个人身份信息（PII）的文件转换为PDF或文本格式 | `python scripts/redactor.py --file doc.pdf --mode full --log` |
| `doc_scanner.py` | `opencv-python-headless`、`numpy`、`Pillow`；`img2pdf`（可选） | 扫描文档并进行边缘检测、透视校正 | `python scripts/doc_scanner.py --input photo.jpg --output scanned.png --mode bw` |
| `expense_logger.py` | 无 | 在CSV文件中添加/列出/编辑/删除费用记录 | `python scripts/expense_logger.py add --date 2024-03-15 --merchant "Starbucks" --amount 13.12 --file expenses.csv` |
| `statement_parser.py` | 无 | 解析银行CSV文件并分类交易记录 | `python scripts/statement_parser.py --file statement.csv --output categorized.json` |
| `report_generator.py` | 无 | 将分类后的JSON数据格式化为Markdown报告 | `python scripts/report_generator.py --file categorized.json --type bank` |
| `timeline_manager.py` | 无 | 管理文档处理的时间线 | `python scripts/timeline_manager.py show` |
| `audio_transcriber.py` | `openai-whisper`、`ffmpeg` | 将音频文件转换为文本 | `python scripts/audio_transcriber.py --file meeting.mp3 --output transcript.txt` |
| `table_extractor.py` | `pdfplumber` | 从PDF文件中提取表格数据并导出为CSV或JSON | `python scripts/table_extractor.py --file document.pdf --output data.csv` |

所有脚本仅导入其明确声明的依赖项。你可以查看任何脚本的源代码：`show me the source of [script name]`。

---

## 脚本依赖项验证

| 脚本 | 使用的Python标准库 | 使用的第三方库 | 是否需要网络访问 |
|---|---|---|---|
| `timeline_manager.py` | `argparse`、`json`、`sys`、`datetime`、`pathlib`、`uuid`、`collections` | 无 | 无需网络访问 |
| `redactor.py` | `argparse`、`re`、`sys`、`pathlib`、`dataclasses` | 依赖`pymupdf`（PDF处理）；`Pillow + pytesseract`（图像处理） | 无需网络访问 |
| `doc_scanner.py` | `argparse`、`json`、`sys`、`time`、`pathlib` | 依赖`opencv-python-headless`、`numpy`、`Pillow`；`img2pdf`（可选） | 无需网络访问 |
| `expense_logger.py` | `argparse`、`csv`、`json`、`sys`、`pathlib` | 无 | 无需网络访问 |
| `statement_parser.py` | `argparse`、`csv`、`json`、`re`、`sys`、`collections`、`datetime`、`pathlib` | 无 | 无需网络访问 |
| `report_generator.py` | `argparse`、`json`、`sys`、`collections`、`pathlib` | 无 | 无需网络访问 |
| `utils.py` | `re`、`unicodedata`、`datetime`、`pathlib` | 无 | 无需网络访问 |
| `audio_transcriber.py` | `argparse`、`sys`、`pathlib` | 仅在首次运行时需要下载`openai-whisper`模型 | 无需网络访问 |
| `table_extract.py` | `argparse`、`csv`、`io`、`json`、`sys`、`pathlib` | 依赖`pdfplumer` | 无需网络访问 |

---

## 隐私与数据处理

| 方面 | 政策说明 |
|---|---|
| 文档内容 | 仅在当前会话内进行本地读取，不会被存储、索引或传输。 |
| 表单自动填充所使用的个人信息 | 仅用于完成当前表单，不会写入任何文件，会话结束后会被删除。 |
| 时间线日志 | 需要用户明确同意后才会记录。日志中不包含原始文档内容，仅包含分类级别的摘要。 |
| 经过编辑的输出文件 | 仅写入用户指定的路径。 |
| 音频转录文件 | 仅在首次使用`openai-whisper`时下载模型文件。 |
| 无数据监控 | 该技能不进行任何分析、使用情况报告或超出上述范围的网络请求。 |

---

## 第1步 — 确定处理模式

### 明确意图 → 直接选择相应的模式

| 模式 | 用户意图 | 常见的文件类型 |
|---|---|---|
| **文档分类** | “处理这个文件”、“这是什么？”、“分析这个文件”、“帮忙处理这个文件”（无明确意图） | 任何类型的文档 |
| 表单自动填充 | “填写表单”、“自动填充表单内容” | PDF表单、图片、截图 |
| 合同分析 | “审核合同”、“总结合同内容”、“查看协议”、“识别风险”、“处理保密协议（NDA）”、“租赁协议” | PDF文件、文本文件 |
| 收据扫描 | “扫描收据”、“识别发票”、“记录费用” | 照片、图片、PDF文件 |
| 银行对账单分析 | “分析银行对账单”、“分类交易记录” | PDF文件、CSV文件 |
| 简历/简历解析 | “解析简历”、“提取简历信息” | PDF文件、图片、文本文件 |
| 身份证/护照扫描 | “扫描身份证”、“读取护照信息” | 照片、图片、PDF文件 |
| 医疗摘要 | “生成医疗摘要” | PDF文件、图片、文本文件 |
| 法律编辑 | “编辑文档内容”、“移除个人身份信息（PII）”、“对敏感信息进行匿名处理” | PDF文件、文本文件、图片文件 |
| 会议记录 | “生成会议记录”、“总结会议内容”、“转录会议内容” | 文本文件、PDF文件、图片文件 |
| 表格提取 | “提取表格数据”、“将表格导出为CSV或JSON” | PDF文件、图片文件、文本文件 |
| 文档翻译 | “翻译这个文件”、“将其翻译成[目标语言]” | 任何类型的文档 |
| 文档时间线 | “显示我的文档处理历史”、“保存处理记录” | 无 |
| **文档扫描** | “扫描这张图片”、“调整图片的透视角度”、“修复图片的变形”、“数字化图片” | 照片文件 |

### 意图不明确 → 使用文档分类模式（需用户确认）

如果用户上传的文件没有明确的处理模式，**请先不要开始处理**。询问用户：

> “我可以自动对文档进行分类，以推荐最适合的处理模式——这需要我先阅读文档的前1-2页。或者您可以直接选择以下模式：”
>
| 模式 | 适合的文件类型 |
|---|---|
| | 表单自动填充 | 包含可填写字段的表单 |
| | 合同分析 | 合同协议、保密协议（NDA）、租赁协议 |
| | 收据扫描 | 收据、发票 |
| | 银行对账单分析 | 银行对账单、信用卡对账单 |
| | 简历解析 | 简历、简历 |
| | 身份证/护照扫描 | 身份证、护照 |
| | 医疗摘要 | 医疗报告、验单、处方 |
| | 法律编辑 | 包含个人身份信息的文档 |
| | 会议记录 | 会议记录、会议要点 |
| | 表格提取 | 包含表格数据的文档 |
| | 文档翻译 | 非英语文档 |
| | 文档扫描 | 需要调整透视角度的图片 |

> “我应该对文档进行分类吗？还是您希望选择哪种处理模式？”

只有在用户确认后，才继续处理文档。

---

## 第2步 — 阅读文档

使用`Read`工具来读取上传的文件。对于图片文件，通过视觉识别方式读取；对于超过10页的PDF文件，需要分页读取。

**对于音频文件（仅适用于会议记录模式）：** 在运行前请确认——这需要`openai-whisper`库，并且会在首次运行时下载模型文件：

> “转录音频文件需要`openai-whisper`库。首次使用时会下载一个模型文件（约140 MB）。您确定要继续吗？”

如果用户同意：
```bash
python skills/doc-process/scripts/audio_transcriber.py --file <path> --output transcript.txt
```

如果用户不同意，请询问是否可以提供文本转录结果。

**对于文档图片（文档扫描模式）：** 在运行扫描脚本之前，先通过视觉识别方式评估图片质量并确定文档类型。

---

## 第3步 — 执行相应的处理模式

根据用户选择的模式，加载并执行相应的参考脚本：

| 模式 | 参考脚本 | 文件路径 |
|---|---|---|
| 文档分类 | `references/document-categorizer.md` |
| 表单自动填充 | `references/form-autofill.md` |
| 合同分析 | `references/contract-analyzer.md` |
| 收据扫描 | `references/receipt-scanner.md` |
| 银行对账单分析 | `references/bank-statement-analyzer.md` |
| 简历/简历解析 | `references/resume-parser.md` |
| 身份证/护照扫描 | `references/id-scanner.md` |
| 医疗摘要 | `references/medical-summarizer.md` |
| 法律编辑 | `references/legal-redactor.md` |
| 会议记录 | `references/meeting-minutes.md` |
| 表格提取 | `references/table-extractor.md` |
| 文档翻译 | `references/document-translator.md` |
| 文档时间线 | `references/document-timeline.md` |
| **文档扫描** | `references/doc-scan.md` |

---

## 第4步 — 文本编辑（redactor.py）：个人身份信息（PII）的处理规则

`redactor.py`脚本涵盖了以下个人身份信息（PII）的类别，并针对多种文档类型（银行对账单、合同、医疗记录、发票、共享购买协议、政府表格等）应用了50多种处理规则：

**类别1 — 个人身份信息（基本模式）**

| 规则 | 例子 |
|---|---|
| 社会安全号码（SSN，美国） | 123-45-6789 |
| 加拿大国家保险号码（SIN） | 123-456-789 |
| 英国国家保险号码 | AB 12 34 56 C |
| 澳大利亚税号（TFN） | 123 456 789 |
| 澳大利亚医疗保险号码 | 1234 56789 1 |
| 印度Aadhaar号码 | 1234 5678 9012 |
| 护照号码 | A12345678 |
| 驾驶执照号码 | 通过关键词识别 |
| 英国国家医疗服务体系（NHS）号码 | 943 476 5919 |
| 国家/选民识别号码 | 通过关键词识别 |
| 车辆VIN码 | 17位字符的编码 |
| 新加坡国民识别号码（NRIC） | S1234567A |
| 医疗记录号码（MRN） | 通过关键词识别 |
| 印度Aadhaar号码 | 1234 5678 9012 |
| 电子邮件地址 | 任何形式的电子邮件地址 |
| 电话号码 | 所有国际格式；日期/参考信息会被过滤掉 |
| 地址信息 | 街道地址（包含街区/单元/公寓号等详细信息） |
| 邮政信箱号码 | PO Box 1234 |
| 美国邮政编码 | 10001, M5V 3A8 |
| 英国邮政编码 | SW1A 2AA |
| 国际邮政编码 | 例如：新加坡229572, 班加罗尔560067 |
| IPv4地址 | 192.168.1.1 |
| MAC地址 | 例如：AA:BB:CC:DD:EE:FF |
| 出生日期 | 通过关键词和日期格式识别 |
| 年龄 | 例如：“年龄：34岁” |
| 标注名称 | 例如：Bill To、Shipper、Attention、Buyer、Seller等 |

**类别2 — 财务信息（完整模式）**

| 规则 | 例子 |
| 信用卡/借记卡号码 | 4111 1111 1111 1111 |
| 卡片CVV码 | CVV: 123 |
| 卡片有效期 | 03/26 |
| 银行账户号码 | 通过关键词识别 |
| 国际银行账户号码（IBAN） | 根据国家代码进行验证 |
| ABA/路由号码 | 例如：“Routing No.”和“ABA No.” |
| 英国银行分类码（BSB） | 20-00-00 |
| 澳大利亚银行分支代码（BSB） | 063-000 |
| 印度IFSC代码 | HDFC0000001 |
| SWIFT/BIC代码 | 允许包含空格（例如：CHAS US33） |
| 工资/报酬 | 工资金额、税前/税后金额 |
| 信用评分 | 通过关键词识别 |
| 贷款/抵押贷款金额 | 通过关键词识别 |
| 税务信息 | 税收收入、应缴税款 |
| 财产净值 | 通过关键词识别 |
| 加密货币钱包地址 | 例如：比特币、以太坊 |

**类别3 — 敏感/受保护信息（仅限完整模式）**

| 标志 | 处理类别 | 适用场景 |
|---|---|---|
| `--mode light` | 仅处理第1类敏感信息 | 适用于共享不需要删除财务细节的文档 |
| `--mode standard` | 处理第1类和第2类敏感信息 | 适用于一般的隐私保护需求 |
| `--mode full` | 处理第1类、第2类和第3类敏感信息 | 适用于法律文件、医疗记录、人力资源相关场景 |
| `--custom REGEX` | 根据特定领域或需求选择处理规则 | 适用于特定领域的敏感信息 |

### PDF文件中的个人身份信息（PII）处理方式

1. 从PDF布局中提取单词边界框。
2. 使用一次性、非重叠的正则表达式引擎检测个人身份信息（PII）。
3. 将检测到的PII信息对应到单词边界框上。
4. 使用`pyMuPDF`库的红色填充效果将敏感信息标记出来。
5. `apply_redactions()`函数会覆盖这些红色区域，并从文档内容中删除原始文本。
6. 文件以增量方式保存——所有未标记的元素（字体、图片、矢量图形、元数据）保持不变。
7. 原始文件不会被修改；输出文件始终是独立的副本。

---

## 第5步 — 文档扫描：工作原理

`doc_scanner.py`脚本通过7个步骤将文档图片转换为专业扫描效果：

1. **多策略边缘检测**：尝试三种方法（A）灰度图像的Canny算法；（B）形态学梯度算法；（C）颜色/亮度阈值算法。以首次成功的方法为准。
2. **亚像素角点细化**：使用`cv2.cornerSubPix`算法将四个角点精确到亚像素级别，以获得更准确的图像变形效果。
3. **透视校正**：使用Lanczos插值算法将图像调整为完美的矩形。
4. **阴影去除**：通过通道级别的背景估计和噪声处理去除阴影和光线不均匀的问题，同时保持文本清晰。
5. **扫描质量增强**：根据模式不同采用不同的处理方式：黑白图像使用自适应阈值和块大小调整；彩色图像使用自动对比度调整（CLAHE）和去噪处理；彩色图像使用白平衡和锐化处理。
6. **扫描边框**：添加8像素宽度的白色边框以模拟扫描仪边缘效果。
7. **DPI标记**：保存时包含DPI元数据（默认为300 DPI，适合打印输出）。

### 如果自动检测失败

如果脚本返回`"corners_detected": false`，请提示用户提供文档的四个角点位置；或者使用`--no-warp`选项仅进行图像增强处理，不进行透视校正。

---

## 第6步 — 文档时间线（可选）

默认情况下，此功能是关闭的。在完成会话中的第一个文档处理任务后，询问用户是否需要记录处理日志：

> “您是否希望我为本次会话生成处理日志？日志会记录文档类型、文件名和分类级别的摘要（不包含原始内容和个人信息），保存在您本地机器的`~/.doc-process-timeline.json`文件中。此功能完全是可选的。”

- **同意** → 确认“启用时间线记录”。记录当前和后续处理的文档，并在每次记录时提示“已保存到时间线”。
- **不同意** → 确认“不生成日志”。此时不会运行任何时间线相关脚本，也不会再次询问。
- **未回答/不确定** → 视为不同意。

**重要规则**：`--summary`参数中绝对不能包含姓名、身份证号码、出生日期、地址、账户号码、信用卡号码、医疗信息等可能识别个人身份的信息。只能记录分类级别的描述。

## 第7步 — 输出结果

以参考文档中指定的格式呈现处理结果。始终在结果中包含相应的操作提示。对于文档扫描功能，始终提供继续处理扫描后的文档的选项。

---

## 通用原则

- **绝不虚构字段内容**。未知内容标记为`[MISSING]`或`[UNREADABLE]`。
- **保守处理敏感信息**：在有疑问时，尽可能包含相关内容。
- **保持表格和列表的清晰可读性**。
- **仅输出处理任务所需的信息**。
- **根据参考指南的要求，始终添加必要的免责声明**（如医疗、法律、隐私相关内容）。
- **时间线功能需用户同意才能启用**。未经用户同意，不得记录任何信息。
- **表单自动填充所使用的个人信息仅限于当前会话**。不会将信息写入文件。
- **在运行依赖第三方库的脚本之前**，如果依赖项尚未安装，请自动运行`bash skills/doc-process/setup.sh`脚本（见第0步）。无需用户确认，因为设置脚本是安全的且不会重复执行。
- **在请求分类之前**，必须先确认用户是否同意自动分类。
- **对于文档扫描功能**：始终先进行视觉检查；切勿处理非文档类型的图片。
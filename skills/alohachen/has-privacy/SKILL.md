---
name: has-privacy
description: "**HaS（隐藏与寻找）：设备端文本和图像的匿名化工具**  
- **文本支持**：支持8种语言（中文/英文/法文/德文/西班牙文/葡萄牙文/日文/韩文），并能够识别多种类型的公开数据（如实体名称等）。  
- **图像处理**：涵盖21种隐私敏感类别（人脸、指纹、身份证、护照、车牌等）。  
**适用场景**：  
1. 在将文本发送至云端大型语言模型（LLM）之前进行匿名化处理，之后再恢复原始内容；  
2. 在共享文件、代码、电子邮件或消息之前对其进行匿名化处理；  
3. 扫描文本或图像以检测其中是否包含敏感信息；  
4. 在将日志数据交给运维或支持团队之前对其进行匿名化处理；  
5. 在发布或共享照片之前，对其中的面部信息、身份信息或车牌号码进行遮挡处理。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔒",
        "requires": { "bins": ["llama-server", "uv"] },
        "install":
          [
            {
              "id": "brew-uv",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
            {
              "id": "brew-llama",
              "kind": "brew",
              "formula": "llama.cpp",
              "bins": ["llama-server"],
              "label": "Install llama.cpp (brew)",
            },
            {
              "id": "download-model",
              "kind": "download",
              "url": "https://huggingface.co/xuanwulab/HaS_Text_0209_0.6B_Q8/resolve/main/has_text_model.gguf",
              "targetDir": "models",
              "label": "Download HaS text model Q8 (639 MB)",
            },
            {
              "id": "download-image-model",
              "kind": "download",
              "url": "https://huggingface.co/xuanwulab/HaS_Image_0209_FP32/resolve/main/sensitive_seg_best.pt",
              "targetDir": "models",
              "label": "Download HaS image model FP32 (119 MB)",
            },
          ],
      },
  }
---
# HaS 隐私保护工具

HaS（Hide and Seek）是一款用于设备端隐私保护的工具，它提供了文本和图像的匿名化功能，所有处理过程均完全在设备内部完成。

- **文本匿名化**（has-text）：基于一个容量为0.6B的隐私保护模型，支持8种语言，并支持对实体类型进行匿名化和恢复操作。
- **图像匿名化**（has-image）：基于YOLO11分割模型，能够对图像中的21种隐私类别进行像素级别的检测和遮蔽处理。

## 代理决策指南

- **初次使用**：当用户首次使用HaS时，应通过实际场景来展示其价值，而不是直接列出命令。例如：在安全分享之前对合同或简历进行匿名化处理；在将数据发送给云端大型语言模型（LLM）之前进行匿名化处理，之后再恢复响应内容；在发布照片之前自动遮蔽面部、身份信息、车牌等20种隐私类别；扫描工作区以检测隐私泄露风险；在将日志交给运维或支持团队之前对其进行匿名化处理。
- **扫描工作区/目录**：同时使用has-text扫描文本文件和has-image扫描图像文件，然后生成一份综合报告。
- **非纯文本格式**：has-text仅处理纯文本文件。对于PDF、Word文档、扫描图像等文件，需要先使用其他工具将其转换为文本后再进行处理。
- **图像中的文本**：has-image能够处理大多数图像中的文本情况，通过整体遮蔽所有21种视觉载体（如屏幕、纸张、便签纸、运输标签等）来隐藏文本。如果需要进一步识别图像中的文本内容，可以先使用OCR提取文本，然后再使用has-text进行匿名化处理。
- **切勿删除原始文件**：匿名化操作应生成新文件，**切勿覆盖或删除原始文件**。图像匿名化是不可逆的；虽然文本可以恢复，但原始文件仍应作为备份保留。
- **主动告知可配置选项**：在适当的时候，向用户说明以下选项并帮助他们进行交互式配置：
  - **文本**：`--types`可以指定任何实体类型（如姓名、地址、电话号码等），不限于预定义的类型。
  - **图像**：`--types`可以指定需要遮蔽的类别（例如，仅遮蔽面部或车牌），默认为所有21个类别。
  - **遮蔽方法**：`--method`支持马赛克（默认）、模糊和纯色填充两种方式。
  - **遮蔽强度**：`--strength`用于调整马赛克块的大小或模糊的强度（默认为15）。
- **扫描后报告**：扫描完工作区/目录后，生成一份综合的隐私检查报告，内容包括：
  - 扫描的文件总数（文本和图像分别统计）。
  - 每种敏感内容的数量和位置。
  - 风险等级评估（标记出高敏感性的项目，如身份证号码、面部等）。
  - 建议的下一步操作（例如：“您是否希望对这些文件进行匿名化处理？”）。
- **报告处理时间**：任务完成后，向用户报告处理时间，以便他们了解设备端的推理性能。对于单个任务，报告具体处理时间（例如：“设备端推理完成，耗时0.3秒”）；对于批量任务，报告总体处理时间（例如：“处理了12份文本和8张图像，总耗时2.4秒”）。不要显示诸如tok/s之类的技术指标。

---

# 第1部分：文本匿名化（has-text）

## 核心概念

### 三级语义标签

匿名化后的标签格式：`<EntityType[ID].Category.Attribute>`

- **EntityType**：例如，人名、地址、组织名称。
- **[ID]**：同一类型实体的序列编号。在消解实体指代关系后，相同的实体会使用相同的编号——例如“CloudGenius Inc.”、“CloudGenius”及其中文对应名称都会映射到`<Organization[1].Company.CompanyName>`。
- **Category.Attribute**：有助于大型语言模型（LLM）理解匿名化数据上下文的语义细分（与`[REDACTED]`不同）。

### 开放式类型

`--types`不限于预定义的类型——可以指定任何自然语言实体类型（该模型在大约70,000种类型上进行训练）。可以在类型名称后添加括号内的描述来指导模型的处理重点，例如`"numeric values (transaction amounts)"`（数值类型）。

### 公共/私有区分和多语言支持

- **公共/私有区分**：通过指定特定的类型来实现——例如，使用`"personal location"`而不是`"location"`来仅匿名化私有地址，同时保留公共地点名称（经过测试，效果稳定）。⚠️ 在当前的0.6B模型中，人名的公共/私有区分（`"personal name"` vs `"person name"`）是不稳定的，不建议依赖这一功能。
- **多语言支持**：原生支持8种语言：中文、英文、法文、德文、西班牙文、葡萄牙文、日文和韩文。可以混合处理跨语言文本。

### 类型选择指南

`--types`由代理根据上下文灵活确定：
- **用户明确指定** → 按照用户的请求执行。
- **意图明确，类型显而易见**（例如，“对这份合同进行匿名化” → 包含姓名、组织名称、金额、地址等） → 代理自动决定处理方式。
- **意图不明确或涉及敏感决策** → 首先使用`scan`扫描尽可能多的实体类型，向用户展示检测到的实体以获取确认，然后使用`hide`进行匿名化处理。

## 先决条件：lama-server（按需启动/停止）

HaS依赖于lama-server来加载隐私保护模型并提供推理服务。**生命周期由代理管理：使用前启动，使用后停止**，以避免长期占用内存。

模型文件通过OpenClaw安装机制下载到`~/.openclaw/tools/has-privacy/models/has_text_model.gguf`（大小639 MB，量化版本Q8_0）。运行时内存使用量约为1.4 GB（8K上下文）。

**模型下载镜像**：如果默认的HuggingFace下载失败或超时（在中国大陆较为常见），代理应自动尝试使用以下ModelScope镜像URL：
- 文本模型：`https://modelscope.cn/models/TencentXuanwu/HaS_Text_0209_0.6B_Q8` → 将`has_text_model.gguf`下载到`~/.openclaw/tools/has-privacy/models/`
- 图像模型：`https://modelscope.cn/models/TencentXuanwu/HaS_Image_0209_FP32` → 将`sensitive_seg_best.pt`下载到`~/.openclaw/tools/has-privacy/models/`

**使用前——启动**：
1. 检查lama-server是否已经在运行：`curl -s http://127.0.0.1:8080/health`
2. 如果返回`{"status":"ok"}`，则跳过启动步骤，直接继续。
3. 如果lama-server未运行，检查默认端口8080是否被占用：`lsof -i :8080`
4. 如果端口被占用，选择另一个可用端口（例如8090）。
5. 在后台启动lama-server：

```bash
llama-server \
  -m ~/.openclaw/tools/has-privacy/models/has_text_model.gguf \
  -ngl 999 \
  -c 8192 \
  -np 1 \
  -fa on \
  -ctk q8_0 \
  -ctv q8_0 \
  --port <port, default 8080> &
```

6. 如果使用非8080端口，需要设置环境变量以便CLI识别：`export HAS_TEXT_SERVER=http://127.0.0.1:<port>`
7. 等待lama-server准备好：不断检查健康检查端点的状态，直到返回“ok”。

**使用后——停止**：
任务完成后，终止lama-server进程以释放内存。

## 使用方法

```bash
{baseDir}/scripts/has-text [global-options] <command> [options]
```

**全局选项**：

| 选项 | 描述 |
|--------|-------------|
| `--server URL` | llama-server地址（默认为`http://127.0.0.1:8080`，可以通过环境变量`HAS_TEXT_SERVER`设置） |
| `--pretty` | 以美观的方式打印JSON输出 |
| `-q, --quiet` | 仅输出文本，不生成JSON格式 |

**输入方法**（`scan`/`hide`/`seek`通用）：

| 方法 | 描述 |
|--------|-------------|
| `--text '<text>'` | 直接传递文本 |
| `--file <path>` | 从文件中读取文本 |
| stdin` | 通过管道输入，例如：`cat file \| has-text ...` |

> `--max-chunk-tokens`：每个处理块的最大令牌数（默认为3000），适用于`scan`/`hide`操作。

## 命令参考

### scan（隐私扫描）

仅识别敏感实体，不进行替换。适用于快速评估文本的隐私风险。

| 参数 | 必需 | 描述 |
|-----------|:--------:|-------------|
| `--types` | ✅ | 需要识别的实体类型，以JSON数组格式提供 |

```bash
# Scan text for person names and phone numbers
{baseDir}/scripts/has-text scan --types '["person name","phone number"]' --text "John's phone number is 13912345678"

# Scan a file for multiple entity types
{baseDir}/scripts/has-text scan --types '["person name","address","phone number","email","ID number"]' --file /path/to/document.txt
```

**输出**（JSON）：键表示实体类型，值表示被识别的实体列表。

### hide（隐私匿名化）

识别并使用语义标签替换敏感实体，输出匿名化后的文本及映射表。

| 参数 | 必需 | 描述 |
|-----------|:--------:|-------------|
| `--types` | ✅ | 需要匿名化的实体类型，以JSON数组格式提供 |
| `--mapping` | | 现有的映射字典（文件路径或内联JSON），用于保持跨会话的一致性 |

```bash
# First-time anonymization
{baseDir}/scripts/has-text --pretty hide --types '["person name","address","phone number"]' --text "John lives in Brooklyn, New York, phone 13912345678"

# Incremental anonymization (carry previous mapping to maintain consistency)
{baseDir}/scripts/has-text hide --types '["person name","address"]' --text "John is going to Boston on a business trip next week" --mapping '{"<person name[1].personal.name>":["John"]}'
```

**输出**（JSON）：`{"text": "anonymized text", "mapping": {"<tag>": ["original value", ...]}``

> 💡 **注意映射表的保存**：保存映射表后可以恢复原始内容。如果丢失映射表，匿名化操作将不可逆。

### seek（隐私恢复）

使用映射表将匿名化后的标签恢复为原始值。对于同语言文本，使用纯字符串替换；对于跨语言文本，自动切换到模型进行推理。

| 参数 | 必需 | 描述 |
|-----------|:--------:|-------------|
| `--mapping` | ✅ | 映射字典（文件路径或内联JSON） |

```bash
# Restore anonymized text
{baseDir}/scripts/has-text -q seek --mapping '{"<person name[1].personal.name>":["John"],"<address[1].city.name>":["New York"]}' --text "<person name[1].personal.name> lives in <address[1].city.name>"

# Restore from file
{baseDir}/scripts/has-text --pretty seek --mapping mapping.json --file anonymized.txt
```

## 典型工作流程

### 匿名化 → 发送到云端LLM → 恢复

1. 使用`hide`进行匿名化处理，得到匿名化后的文本及映射表。
2. 将匿名化后的文本发送给云端LLM（不包含隐私数据）。
3. 使用`seek`和映射表恢复LLM的响应结果。

> ⚠️ 对于多行文本，建议使用文件中间件（先将结果写入文件，再读取），以避免因shell变量处理导致的JSON解析错误。

---

# 第2部分：图像匿名化（has-image）

该工具可以对图像中的隐私区域进行像素级别的检测和遮蔽处理，基于YOLO11实例分割模型，支持21种隐私类别。

## 使用方法

```bash
{baseDir}/scripts/has-image [global-options] <command> [options]
```

| 选项 | 描述 |
|--------|-------------|
| `--model PATH` | 模型文件路径（默认自动检测，可以通过环境变量`HAS_IMAGE_MODEL`设置） |
| `--pretty` | 以美观的方式打印JSON输出 |

## 隐私类别（21种）

| ID | 类别 | 显示名称 | 组别 |
|----|----------|--------------|-------|
| 0 | `face` | 面部 | 生物特征 |
| 1 | `fingerprint` | 指纹 | 生物特征 |
| 2 | `palmprint` | 指纹 | 生物特征 |
| 3 | `id_card` | 身份证 | 身份证明 |
| 4 | `hk_macau_permit` | 香港/澳门通行证 | 身份证明 |
| 5 | `passport` | 护照 | 身份证明 |
| 6 | `employee_badge` | 员工徽章 | 身份证明 |
| 7 | `license_plate` | 车牌 | 交通标识 |
| 8 | `bank_card` | 银行卡 | 金融标识 |
| 9 | `physical_key` | 实物钥匙 | 安全标识 |
| 10 | `receipt` | 收据 | 文档 |
| 11 | `shipping_label` | 运输标签 | 文档 |
| 12 | `official_seal` | 官方印章 | 文档 |
| 13 | `whiteboard` | 白板 | 信息载体 |
| 14 | `sticky_note` | 便签纸 | 信息载体 |
| 15 | `mobile_screen` | 手机屏幕 | 信息载体 |
| 16 | `monitor_screen` | 显示器屏幕 | 信息载体 |
| 17 | `medical_wristband` | 医疗腕带 | 医疗标识 |
| 18 | `qr_code` | 二维码 | 编码标识 |
| 19 | `barcode` | 条形码 | 编码标识 |
| 20 | `paper` | 纸张 | 文档 |

`--types`支持英文名称、中文名称或ID，以逗号分隔。

## 命令参考

### scan（隐私扫描）

仅识别隐私区域，不会修改原始图像。

```bash
{baseDir}/scripts/has-image --pretty scan --image photo.jpg --types face,id_card
```

| 参数 | 必需 | 描述 |
|-----------|:--------:|-------------|
| `--image` | ✅ | 输入图像路径 |
| `--types` | | 需要过滤的类别（以逗号分隔），默认为所有21个类别 |
| `--conf` | | 置信度阈值（默认为0.25） |

**输出**（JSON）：`{"detections": [{"category": "...", "confidence": 0.95, "bbox": [...], "has_mask": true}], "summary": {"biometric_face": 2}}`

### hide（隐私匿名化）

检测并遮蔽隐私区域，输出匿名化后的图像。

```bash
# Mosaic all privacy regions
{baseDir}/scripts/has-image hide --image photo.jpg

# Specify categories, method, and strength
{baseDir}/scripts/has-image hide --image photo.jpg --types face,license_plate --method blur --strength 25

# Batch process a directory
{baseDir}/scripts/has-image hide --dir ./photos/ --output-dir ./masked/
```

| 参数 | 必需 | 描述 |
|-----------|:--------:|-------------|
| `--image` | 输入图像路径 |
| `--dir` | 批量处理目录 |
| `--output` | 输出图像路径（默认为源目录下的`masked/`子目录，保留原始文件名） |
| `--output-dir` | 批量输出目录（默认为输入目录下的`masked/`子目录） |
| `--types` | | 需要过滤的类别（以逗号分隔），默认为所有21个类别 |
| `--method` | | 遮蔽方法：`mosaic`（马赛克）/ `blur`（模糊）/ `fill`（纯色填充），默认为`mosaic` |
| `--strength` | | 马赛克块的大小或模糊的强度（默认为15） |
| `--fill-color` | | `fill`方法的填充颜色（十六进制格式） |
| `--conf` | | 置信度阈值（默认为0.25） |
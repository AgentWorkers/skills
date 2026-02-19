---
name: mineru-pdf-extractor
description: 使用 MinerU API 将 PDF 内容提取为 Markdown 格式。支持公式、表格和 OCR（光学字符识别）功能。提供本地文件解析和在线 URL 解析两种方式。
author: Community
version: 1.0.0
homepage: https://mineru.net/
source: https://github.com/opendatalab/MinerU
requirements:
  - MINERU_TOKEN or MINERU_API_KEY environment variable
  - curl command-line tool
  - unzip extraction tool
optional:
  - jq for enhanced JSON parsing
---
# MinerU PDF提取器

使用MinerU API将PDF文档提取为结构化的Markdown格式。支持公式识别、表格提取和OCR功能。

> **注意**：这是一个社区技能，并非MinerU的官方产品。您需要从[MinerU](https://mineru.net/)获取自己的API密钥。

---

## 📁 技能结构

```
mineru-pdf-extractor/
├── SKILL.md                          # English documentation
├── SKILL_zh.md                       # Chinese documentation
├── docs/                             # Documentation
│   ├── Local_File_Parsing_Guide.md   # Local PDF parsing detailed guide (English)
│   ├── Online_URL_Parsing_Guide.md   # Online PDF parsing detailed guide (English)
│   ├── MinerU_本地文档解析完整流程.md  # Local parsing complete guide (Chinese)
│   └── MinerU_在线文档解析完整流程.md  # Online parsing complete guide (Chinese)
└── scripts/                          # Executable scripts
    ├── local_file_step1_apply_upload_url.sh    # Local parsing Step 1
    ├── local_file_step2_upload_file.sh         # Local parsing Step 2
    ├── local_file_step3_poll_result.sh         # Local parsing Step 3
    ├── local_file_step4_download.sh            # Local parsing Step 4
    ├── online_file_step1_submit_task.sh        # Online parsing Step 1
    └── online_file_step2_poll_result.sh        # Online parsing Step 2
```

---

## 🔧 需求

### 必备的环境变量

脚本会自动从环境变量中读取MinerU令牌（请选择其中一个）：

```bash
# Option 1: Set MINERU_TOKEN
export MINERU_TOKEN="your_api_token_here"

# Option 2: Set MINERU_API_KEY
export MINERU_API_KEY="your_api_token_here"
```

### 必备的命令行工具

- `curl` - 用于发送HTTP请求（通常已预装）
- `unzip` - 用于解压提取结果（通常已预装）

### 可选工具

- `jq` - 用于增强JSON解析和安全性（推荐，但非必需）
  - 如果未安装，脚本将使用替代方法
  - 安装方法：`apt-get install jq`（Debian/Ubuntu）或`brew install jq`（macOS）

### 可选的配置选项

```bash
# Set API base URL (default is pre-configured)
export MINERU_BASE_URL="https://mineru.net/api/v4"
```

> 💡 **获取令牌**：访问https://mineru.net/apiManage/docs注册并获取API密钥

---

## 📄 功能1：解析本地PDF文档

适用于本地存储的PDF文件。需要4个步骤。

### 快速开始

```bash
cd scripts/

# Step 1: Apply for upload URL
./local_file_step1_apply_upload_url.sh /path/to/your.pdf
# Output: BATCH_ID=xxx UPLOAD_URL=xxx

# Step 2: Upload file
./local_file_step2_upload_file.sh "$UPLOAD_URL" /path/to/your.pdf

# Step 3: Poll for results
./local_file_step3_poll_result.sh "$BATCH_ID"
# Output: FULL_ZIP_URL=xxx

# Step 4: Download results
./local_file_step4_download.sh "$FULL_ZIP_URL" result.zip extracted/
```

### 脚本说明

#### `local_file_step1_apply_upload_url.sh`

申请上传URL和批次ID。

**使用方法：**
```bash
./local_file_step1_apply_upload_url.sh <pdf_file_path> [language] [layout_model]
```

**参数：**
- `language`：`ch`（中文），`en`（英文），`auto`（自动检测），默认为`ch`
- `layout_model`：`doclayout_yolo`（快速），`layoutlmv3`（精确），默认为`doclayout_yolo`

**输出：**
```
BATCH_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
UPLOAD_URL=https://mineru.oss-cn-shanghai.aliyuncs.com/...
```

---

#### `local_file_step2_upload_file.sh`

将PDF文件上传到预定的URL。

**使用方法：**
```bash
./local_file_step2_upload_file.sh <upload_url> <pdf_file_path>
```

---

#### `local_file_step3_poll_result.sh`

轮询提取结果，直到完成或失败。

**使用方法：**
```bash
./local_file_step3_poll_result.sh <batch_id> [max_retries] [retry_interval_seconds]
```

**输出：**
```
FULL_ZIP_URL=https://cdn-mineru.openxlab.org.cn/pdf/.../xxx.zip
```

---

#### `local_file_step4_download.sh`

下载结果ZIP文件并解压。

**使用方法：**
```bash
./local_file_step4_download.sh <zip_url> [output_zip_filename] [extract_directory_name]
```

**输出结构：**
```
extracted/
├── full.md              # 📄 Markdown document (main result)
├── images/              # 🖼️ Extracted images
├── content_list.json    # Structured content
└── layout.json          # Layout analysis data
```

### 详细文档

📚 **完整指南**：请参阅`docs/Local_File_Parsing_Guide.md`

---

## 🌐 功能2：解析在线PDF文档（URL方法）

适用于已经在线的PDF文件（例如arXiv、网站等）。只需2个步骤，更加简洁高效。

### 快速开始

```bash
cd scripts/

# Step 1: Submit parsing task (provide URL directly)
./online_file_step1_submit_task.sh "https://arxiv.org/pdf/2410.17247.pdf"
# Output: TASK_ID=xxx

# Step 2: Poll results and auto-download/extract
./online_file_step2_poll_result.sh "$TASK_ID" extracted/
```

### 脚本说明

#### `online_file_step1_submit_task.sh`

提交在线PDF的解析任务。

**使用方法：**
```bash
./online_file_step1_submit_task.sh <pdf_url> [language] [layout_model]
```

**参数：**
- `pdf_url`：在线PDF的完整URL（必需）
- `language`：`ch`（中文），`en`（英文），`auto`（自动检测），默认为`ch`
- `layout_model`：`doclayout_yolo`（快速），`layoutlmv3`（精确），默认为`doclayout_yolo`

**输出：**
```
TASK_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

#### `online_file_step2_poll_result.sh`

轮询提取结果，完成后自动下载并解压。

**使用方法：**
```bash
./online_file_step2_poll_result.sh <task_id> [output_directory] [max_retries] [retry_interval_seconds]
```

**输出结构：**
```
extracted/
├── full.md              # 📄 Markdown document (main result)
├── images/              # 🖼️ Extracted images
├── content_list.json    # Structured content
└── layout.json          # Layout analysis data
```

### 详细文档

📚 **完整指南**：请参阅`docs/Online_URL_Parsing_Guide.md`

---

## 📊 两种解析方法的比较

| 功能 | **本地PDF解析** | **在线PDF解析** |
|---------|----------------------|------------------------|
| **步骤** | 4个步骤 | 2个步骤 |
| **是否需要上传** | ✅ 是 | ❌ 否 |
| **平均时间** | 30-60秒 | 10-20秒 |
| **适用场景** | 本地文件 | 已经在线的文件（如arXiv、网站等） |
| **文件大小限制** | 200MB | 受源服务器限制 |

---

## ⚙️ 高级用法

### 批量处理本地文件

```bash
for pdf in /path/to/pdfs/*.pdf; do
    echo "Processing: $pdf"
    
    # Step 1
    result=$(./local_file_step1_apply_upload_url.sh "$pdf" 2>&1)
    batch_id=$(echo "$result" | grep BATCH_ID | cut -d= -f2)
    upload_url=$(echo "$result" | grep UPLOAD_URL | cut -d= -f2)
    
    # Step 2
    ./local_file_step2_upload_file.sh "$upload_url" "$pdf"
    
    # Step 3
    zip_url=$(./local_file_step3_poll_result.sh "$batch_id" | grep FULL_ZIP_URL | cut -d= -f2)
    
    # Step 4
    filename=$(basename "$pdf" .pdf)
    ./local_file_step4_download.sh "$zip_url" "${filename}.zip" "${filename}_extracted"
done
```

### 批量处理在线文件

```bash
for url in \
  "https://arxiv.org/pdf/2410.17247.pdf" \
  "https://arxiv.org/pdf/2409.12345.pdf"; do
    echo "Processing: $url"
    
    # Step 1
    result=$(./online_file_step1_submit_task.sh "$url" 2>&1)
    task_id=$(echo "$result" | grep TASK_ID | cut -d= -f2)
    
    # Step 2
    filename=$(basename "$url" .pdf)
    ./online_file_step2_poll_result.sh "$task_id" "${filename}_extracted"
done
```

---

## ⚠️ 注意事项

1. **令牌配置**：脚本优先使用`MINERU_TOKEN`，如果未找到则使用`MINERU_API_KEY`
2. **令牌安全**：不要在脚本中硬编码令牌；请使用环境变量
3. **URL可访问性**：对于在线解析，请确保提供的URL是公开可访问的
4. **文件大小限制**：建议单个文件不超过200MB，最多600页
5. **网络稳定性**：上传大文件时请确保网络稳定
6. **安全性**：该技能包含输入验证和清理机制，以防止JSON注入和目录遍历攻击
7. **可选的jq**：安装`jq`可以增强JSON解析功能并提供额外的安全检查

---

## 📚 参考文档

| 文档 | 说明 |
|----------|-------------|
| `docs/Local_File_Parsing_Guide.md` | 本地PDF解析的详细curl命令和参数 |
| `docs/Online_URL_Parsing_Guide.md` | 在线PDF解析的详细curl命令和参数 |

外部资源：
- 🏠 **MinerU官网**：https://mineru.net/
- 📖 **API文档**：https://mineru.net/apiManage/docs
- 💻 **GitHub仓库**：https://github.com/opendatalab/MinerU

---

*技能版本：1.0.0*  
*发布日期：2026-02-18*  
*社区技能 - 与MinerU官方无关*
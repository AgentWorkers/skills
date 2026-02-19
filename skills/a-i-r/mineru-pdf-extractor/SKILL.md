---
name: mineru-pdf-extractor
description: 使用 MinerU API 将 PDF 内容提取为 Markdown 格式。支持公式、表格和 OCR（光学字符识别）功能。提供本地文件解析和在线 URL 解析两种方式。
author: Community
version: 1.0.0
homepage: https://mineru.net/
source: https://github.com/opendatalab/MinerU
env:
  - name: MINERU_TOKEN
    description: "MinerU API token for authentication (primary)"
    required: true
  - name: MINERU_API_KEY
    description: "Alternative API token if MINERU_TOKEN is not set"
    required: false
  - name: MINERU_BASE_URL
    description: "API base URL (optional, defaults to https://mineru.net/api/v4)"
    required: false
    default: "https://mineru.net/api/v4"
tools:
  required:
    - name: curl
      description: "HTTP client for API requests and file downloads"
    - name: unzip
      description: "Archive extraction tool for result ZIP files"
  optional:
    - name: jq
      description: "JSON processor for enhanced parsing and security (recommended)"
---
# MinerU PDF提取器

使用MinerU API将PDF文档提取为结构化的Markdown格式。支持公式识别、表格提取和OCR处理。

> **注意**：这是一个社区技能，并非MinerU的官方产品。您需要从[MinerU](https://mineru.net/)获取自己的API密钥。

---

## 技能结构

---

## 所需条件

### 必需的环境变量

脚本会自动从环境变量中读取MinerU令牌（请选择一个）：

---

### 必需的命令行工具

- `curl` - 用于发送HTTP请求（通常已预安装）
- `unzip` - 用于解压提取的结果（通常已预安装）

### 可选工具

- `jq` - 用于增强JSON解析和安全性（推荐使用，但非必需）
  - 如果未安装，脚本将使用备用方法
  - 安装方法：`apt-get install jq`（Debian/Ubuntu）或`brew install jq`（macOS）

### 可选的配置选项

---

> 💡 **获取令牌**：访问https://mineru.net/apiManage/docs注册并获取API密钥

---

## 功能1：解析本地PDF文档

适用于本地存储的PDF文件。需要4个步骤。

### 快速入门

---

### 脚本说明

#### local_file_step1_apply_upload_url.sh

申请上传URL和批次ID。

**使用方法：**
---

**参数：**
- `language`：`ch`（中文），`en`（英文），`auto`（自动检测），默认为`ch`
- `layout_model`：`doclayout_yolo`（快速），`layoutlmv3`（精确），默认为`doclayout_yolo`

**输出：**
---

#### local_file_step2_upload_file.sh

将PDF文件上传到预定的URL。

**使用方法：**
---

#### local_file_step3_poll_result.sh

轮询提取结果，直到完成或失败。

**使用方法：**
---

#### local_file_step4_download.sh

下载结果ZIP文件并解压。

**使用方法：**
---

**输出结构：**
---

### 详细文档

📚 **完整指南**：请参阅`docs/Local_File_Parsing_Guide.md`

---

## 功能2：解析在线PDF文档（URL方式）

适用于已经在线发布的PDF文件（例如arXiv、网站等）。只需2个步骤，更加简洁高效。

### 快速入门

---

### 脚本说明

#### online_file_step1_submit_task.sh

提交在线PDF的解析任务。

**使用方法：**
---

**参数：**
- `pdf_url`：在线PDF的完整URL（必需）
- `language`：`ch`（中文），`en`（英文），`auto`（自动检测），默认为`ch`
- `layout_model`：`doclayout_yolo`（快速），`layoutlmv3`（精确），默认为`doclayout_yolo`

**输出：**
---

#### online_file_step2_poll_result.sh

轮询提取结果，完成后自动下载并解压。

**使用方法：**
---

**输出结构：**
---

### 详细文档

📚 **完整指南**：请参阅`docs/Online_URL_Parsing_Guide.md`

---

## 两种解析方法的比较

| 功能        | **本地PDF解析** | **在线PDF解析** |
|------------|------------------|------------------------|
| 步骤        | 4个步骤       | 2个步骤         |
| 是否需要上传    | ✅ 是            | ❌ 否            |
| 平均处理时间    | 30-60秒        | 10-20秒         |
| 适用场景      | 本地文件        | 已在线发布的文件（如arXiv、网站等） |
| 文件大小限制    | 200MB         | 受源服务器限制       |

---

## 高级用法

### 批量处理本地文件

---

### 批量处理在线文件

---

## 注意事项

1. **令牌配置**：脚本优先使用`MINERU_TOKEN`，如果未找到则使用`MINERU_API_KEY`作为备用。
2. **令牌安全**：不要在脚本中硬编码令牌，应使用环境变量。
3. **URL可用性**：对于在线解析，请确保提供的URL是公开可访问的。
4. **文件大小限制**：建议单个文件不超过200MB，最多600页。
5. **网络稳定性**：上传大文件时请确保网络稳定。
6. **安全性**：该技能包含输入验证和清理机制，以防止JSON注入和目录遍历攻击。
7. **可选的jq**：安装`jq`可以增强JSON解析功能并提高安全性。

---

## 参考文档

| 文档        | 说明            |
|------------|-----------------------------|
| `docs/Local_File_Parsing_Guide.md` | 本地PDF解析的详细curl命令和参数 |
| `docs/Online_URL_Parsing_Guide.md` | 在线PDF解析的详细curl命令和参数 |

外部资源：
- 🏠 **MinerU官方网站**：https://mineru.net/
- 📖 **API文档**：https://mineru.net/apiManage/docs
- 💻 **GitHub仓库**：https://github.com/opendatalab/MinerU

---

*技能版本：1.0.0*  
*发布日期：2026-02-18*  
*社区技能 - 与MinerU官方无关*
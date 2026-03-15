---
name: paddleocr-doc-parsing
description: 使用 PaddleOCR 进行复杂的文档解析。能够智能地将复杂的 PDF 文件和文档图片转换为保留原始结构的 Markdown 和 JSON 文件。
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_DOC_PARSING_API_URL
        - PADDLEOCR_ACCESS_TOKEN
        - PADDLEOCR_DOC_PARSING_TIMEOUT
      bins:
        - python
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "📄"
    homepage: https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills/paddleocr-doc-parsing
---
# PaddleOCR 文档解析技能

## 何时使用此技能

**适用于以下类型的文档解析：**
- 包含表格的文档（发票、财务报告、电子表格）
- 包含数学公式的文档（学术论文、科学文档）
- 包含图表和图形的文档
- 多列布局的文档（报纸、杂志、宣传册）
- 需要布局分析的复杂文档结构
- 任何需要结构化理解的文档

**适用于以下情况的文本识别：**
- 仅包含文本的简单文档提取
- 对速度要求极高的快速 OCR 任务
- 包含清晰文本的截图或简单图片

## 安装

在使用此技能之前，请先安装 Python 的相关依赖项。请从技能目录（`skills/paddleocr-doc-parsing`）中进行安装：

```bash
pip install -r scripts/requirements.txt
```

**可选** — 用于文档优化和 `split_pdf.py`（页面提取）：

```bash
pip install -r scripts/requirements-optimize.txt
```

## 如何使用此技能

**⛔ 强制性规定 - 请严格遵守 ⛔**

1. **仅使用 PaddleOCR 文档解析 API** - 运行脚本 `python scripts/vl_caller.py`
2. **切勿直接解析文档** - 不要自行解析文档
3. **切勿提供替代方案** - 不要回答“我可以尝试分析它”之类的问题
4. **如果 API 失败** - 立即显示错误信息并停止操作
5. **禁止使用其他方法进行文档解析** - 不要以任何其他方式尝试解析文档

如果脚本执行失败（例如 API 配置错误、网络问题等）：
- 向用户显示错误信息
- **不要使用您的视觉能力提供帮助** 
- **不要询问“您是否希望我尝试解析？”**
- **直接停止并等待用户修复配置**

### 基本工作流程

1. **执行文档解析**：
   ```bash
   python scripts/vl_caller.py --file-url "URL provided by user" --pretty
   ```
   或者对于本地文件：
   ```bash
   python scripts/vl_caller.py --file-path "file path" --pretty
   ```

   **可选：明确指定文件类型**：
   ```bash
   python scripts/vl_caller.py --file-url "URL provided by user" --file-type 0 --pretty
   ```
   - `--file-type 0`：PDF
   - `--file-type 1`：图片
   - 如果省略此参数，系统会自动识别文件类型。

   **默认行为：将原始 JSON 数据保存到临时文件**：
   - 如果未指定 `--output` 参数，脚本会自动将结果保存到系统临时目录
   - 默认路径格式：`<system-temp>/paddleocr/doc-parsing/results/result_<timestamp>_<id>.json`
   - 如果指定了 `--output` 参数，将覆盖默认的临时文件路径
   - 如果指定了 `--stdout` 参数，JSON 数据会输出到标准输出（stdout），不会保存到文件
   - 在保存模式下，脚本会在标准错误输出（stderr）中显示文件的保存路径：`结果保存路径：/absolute/path/...`
   - 在默认/自定义保存模式下，会在响应前读取并解析保存的 JSON 文件
   - 在保存模式下，务必告知用户文件的保存路径以及完整的原始 JSON 数据的位置
   - 仅在明确希望跳过文件保存时使用 `--stdout` 参数

2. **输出的 JSON 数据包含所有文档内容**：
   - 标题页、页脚、页码
   - 主文本内容
   - 带有结构的表格
   - 公式（包含 LaTeX 格式）
   - 图表和图形
   - 脚注和参考文献
   - 图章和印记
   - 文档的布局和阅读顺序

   **关于输入类型的说明**：
   - 支持的文件类型取决于模型和端点的配置
   - 请始终遵循端点 API 文档中规定的文件类型限制。

3. **从输出的 JSON 数据中提取用户所需的内容**：
   - 最高级别的 `text` 字段
   - `result[n].markdown` 字段
   - `result[n].prunedResult` 字段

### 重要提示：完整内容展示

**关键要求**：必须根据用户的需求向用户展示完整的提取内容。

- 输出的 JSON 数据包含所有文档内容（以结构化格式呈现）
- 在保存模式下，可以在保存的 JSON 文件中查看原始的解析结果
- **展示用户请求的所有内容**，不要截断或总结
- 如果用户请求“全部文本”，请显示完整的 `text` 字段
- 如果用户请求“表格”，请显示文档中的所有表格
- 如果用户请求“主要内容”，请过滤掉标题页/页脚，但显示所有正文内容

**具体操作说明**：
- **必须**：按照用户的要求展示完整的文本、所有表格和所有公式
- **必须**：使用 `text`、`result[n].markdown` 和 `result[n].prunedResult` 字段来呈现内容
- **禁止**：除非内容过长（超过 10,000 个字符），否则不要截断内容
- **禁止**：当用户请求完整内容时，不要进行总结或提供摘录
- **禁止**：当用户期望获得完整输出时，不要说“这是预览”

**示例 - 正确的操作**：
```
User: "Extract all the text from this document"
Agent: I've parsed the complete document. Here's all the extracted text:

[Display entire text field or concatenated regions in reading order]

Document Statistics:
- Total regions: 25
- Text blocks: 15
- Tables: 3
- Formulas: 2
Quality: Excellent (confidence: 0.92)
```

**示例 - 错误的操作**：
```
User: "Extract all the text"
Agent: "I found a document with multiple sections. Here's the beginning:
'Introduction...' (content truncated for brevity)"
```

### 理解 JSON 响应

输出的 JSON 数据使用一个外壳来包裹原始的 API 结果：

```json
{
  "ok": true,
  "text": "Full markdown/HTML text extracted from all pages",
  "result": { ... },  // raw provider response
  "error": null
}
```

**关键字段**：
- `text` — 从所有页面提取的 Markdown 文本（用于快速显示文本）
- `result` — 原始的 API 响应对象
- `result[n].prunedResult` — 每页的结构化解析结果（包括布局、内容和置信度等相关元数据）
- `result[n].markdown` — 以 Markdown/HTML 格式呈现的完整页面内容

> 原始结果的位置（默认）：脚本会在标准错误输出（stderr）中显示临时文件的路径

### 使用示例

**示例 1：提取文档的全部文本**
```bash
python scripts/vl_caller.py \
  --file-url "https://example.com/paper.pdf" \
  --pretty
```

然后可以使用：
- 最高级别的 `text` 字段来快速获取全部文本内容
- 当需要页面级别的输出时，使用 `result[n].markdown` 字段

**示例 2：提取结构化页面数据**
```bash
python scripts/vl_caller.py \
  --file-path "./financial_report.pdf" \
  --pretty
```

然后可以使用：
- `result[n].prunedResult` 字段来获取结构化的数据（包括布局、内容和置信度）
- `result[n].markdown` 字段来获取渲染后的页面内容

**示例 3：不保存 JSON 数据直接输出**
```bash
python scripts/vl_caller.py \
  --file-url "URL" \
  --stdout \
  --pretty
```

然后返回：
- 当用户请求全部文档内容时，返回完整的 `text` 字段
- 当用户需要完整的结构化页面数据时，返回 `result[n].prunedResult` 和 `result[n].markdown` 字段

### 首次配置

**当 API 未配置时**：

系统会显示错误信息：
```
CONFIG_ERROR: PADDLEOCR_DOC_PARSING_API_URL not configured. Get your API at: https://paddleocr.com
```

**配置流程**：
1. **向用户显示具体的错误信息**（包括错误代码和错误原因）。
2. **指导用户安全地进行配置**：
   - 建议通过主机应用程序的标准方式（例如设置文件、环境变量界面）进行配置，而不是在聊天中粘贴凭据。
   - 列出所需的环境变量：
     ```
     - PADDLEOCR_DOC_PARSING_API_URL
     - PADDLEOCR_ACCESS_TOKEN
     - Optional: PADDLEOCR_DOC_PARSING_TIMEOUT
     ```

3. **如果用户仍然在聊天中提供了凭据**（接受任何合理的格式），例如：
   - `PADDLEOCR_DOC_PARSING_API_URL=https://xxx.paddleocr.com/layout-parsing, PADDLEOCR_ACCESS_TOKEN=abc123...`
   - `我的 API 地址是 https://xxx，令牌是 abc123`
   - 以复制粘贴的形式提供凭据
   - **安全提示**：提醒用户，在聊天中分享的凭据可能会被保存在聊天记录中。建议尽可能通过主机应用程序的配置来设置凭据。

   然后解析并验证这些凭据：
   - 提取 `PADDLEOCR_DOC_PARSING_API_URL`（查找包含 `paddleocr.com` 的 URL）
   - 确认 `PADDLEOCR_DOC_PARSING_API_URL` 是以 `/layout-parsing` 结尾的完整端点
   - 提取 `PADDLEOCR_ACCESS_TOKEN`（通常为 40 个以上字符的字母数字字符串）

4. **请用户确认环境配置已完成**。
5. **只有在用户确认环境变量已配置后，才重新尝试解析**。

### 处理大文件

API 对文件大小没有限制。对于 PDF 文件，每次请求的最大文件量为 100 页。

**处理大文件的提示**：
#### 对于大型本地文件，建议使用 `--file-url` 参数（推荐）
对于非常大的本地文件，建议使用 `--file-url` 而不是 `--file-path`，以避免额外的 Base64 编码开销：
```bash
python scripts/vl_caller.py --file-url "https://your-server.com/large_file.pdf"
```

#### 处理特定页面（仅限 PDF 文件）
如果只需要从大型 PDF 文件中提取某些页面，可以先提取这些页面：
```bash
# Extract pages 1-5
python scripts/split_pdf.py large.pdf pages_1_5.pdf --pages "1-5"

# Mixed ranges are supported
python scripts/split_pdf.py large.pdf selected_pages.pdf --pages "1-5,8,10-12"

# Then process the smaller file
python scripts/vl_caller.py --file-path "pages_1_5.pdf"
```

### 错误处理

**身份验证失败（403）**：
```
error: Authentication failed
```
→ 令牌无效，请使用正确的凭据重新配置

**API 配额超出（429）**：
```
error: API quota exceeded
```
→ 日常 API 配额已用尽，请告知用户等待或升级

**不支持的文件格式**：
```
error: Unsupported file format
```
→ 文件格式不受支持，请将文件转换为 PDF/PNG/JPG 格式

## 重要说明

- **脚本从不过滤内容** — 它总是返回全部数据
- **AI 代理会根据用户的特定请求来决定展示哪些内容**
- **所有数据始终可用** — 可以根据不同的需求重新解析
- **没有信息丢失** — 完整的文档结构得到保留

## 参考文档

- `references/output_schema.md` — 输出格式规范

> **注意**：模型版本和功能由您的 API 端点（`PADDLEOCR_DOC_PARSING_API_URL`）决定。

在以下情况下请参考这些文档：
- 调试复杂的解析问题
- 需要了解输出格式
- 了解提供商 API 的详细信息

## 测试此技能

为了验证此技能是否正常工作：
```bash
python scripts/smoke_test.py
```

此操作用于测试配置和 API 的连接性。
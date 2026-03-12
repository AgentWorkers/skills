---
name: paddleocr-doc-parsing
description: 使用 PaddleOCR 进行高级文档解析。可以提取完整的文档结构，包括文本、表格、公式、图表和布局信息。AI 代理会根据用户需求提取相关内容。
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
# PaddleOCR文档解析技能

## 何时使用此技能

**适用于以下文档类型**：
- 包含表格的文档（发票、财务报告、电子表格）
- 包含数学公式的文档（学术论文、科学文档）
- 包含图表和图形的文档
- 多列布局的文档（报纸、杂志、宣传册）
- 需要布局分析的复杂文档
- 任何需要结构化理解的文档

**适用于以下情况**：
- 仅提取简单文本
- 需要快速OCR处理且速度至关重要的场景
- 包含清晰文本的截图或简单图片

## 如何使用此技能

**⛔ 必须遵守的规定 - 严禁违反 ⛔**

1. **仅使用PaddleOCR文档解析API** - 运行脚本 `python scripts/vl_caller.py`
2. **严禁直接解析文档** - 不要自行解析文档
3. **严禁提供替代方案** - 不要表示“我可以尝试分析它”或类似的话
4. **如果API失败** - 显示错误信息并立即停止
5. **禁止使用其他方法进行文档解析**

如果脚本执行失败（例如API配置错误、网络问题等）：
- 向用户显示错误信息
- 不要提供使用视觉功能来帮助用户
- 不要询问“您是否希望我尝试解析它？”
- 直接停止并等待用户修复配置

### 基本工作流程

1. **执行文档解析**：
   ```bash
   python scripts/vl_caller.py --file-url "URL provided by user" --pretty
   ```
   或对于本地文件：
   ```bash
   python scripts/vl_caller.py --file-path "file path" --pretty
   ```

   **可选：明确指定文件类型**：
   ```bash
   python scripts/vl_caller.py --file-url "URL provided by user" --file-type 0 --pretty
   ```
   - `--file-type 0`：PDF
   - `--file-type 1`：图片
   - 如果省略，服务会从输入中推断文件类型

   **默认行为：将原始JSON保存到临时文件**：
   - 如果省略`--output`，脚本会自动将结果保存在系统临时目录下
   - 默认路径模式：`<system-temp>/paddleocr/doc-parsing/results/result_<timestamp>_<id>.json`
   - 如果提供了`--output`，则会覆盖默认的临时文件路径
   - 如果提供了`--stdout`，JSON会输出到标准输出（stdout），不会保存文件
   - 在保存模式下，脚本会在标准错误输出（stderr）中打印保存的绝对路径：`结果保存路径：/absolute/path/...`
   - 在默认/自定义保存模式下，会在响应前读取并解析保存的JSON文件
   - 在保存模式下，务必告知用户保存的文件路径以及完整的原始JSON文件的位置
   - 仅在明确希望跳过文件保存时使用`--stdout`

2. **输出的JSON包含完整内容**：
   - 文档的页眉、页脚、页码
   - 主文本内容
   - 带有结构的表格
   - 公式（包含LaTeX格式）
   - 图表和图形
   - 脚注和参考文献
   - 图章和印记
   - 文档的布局和阅读顺序

   **关于输入类型的说明**：
   - 支持的文件类型取决于模型和端点配置
   - 请始终遵循端点API文档中规定的文件类型限制

3. **从输出的JSON中提取用户所需的内容**：
   - 最高级别的`text`
   - `result[n].markdown`
   - `result[n].prunedResult`

### 重要提示：显示完整内容

**关键要求**：必须根据用户的需求向用户显示完整的提取内容。

- 输出的JSON包含所有结构化格式的文档内容
- 在保存模式下，可以在保存的JSON文件中查看原始的解析结果
- **显示用户请求的全部内容**，不要截断或总结
- 如果用户请求“全部文本”，则显示整个`text`字段
- 如果用户请求“表格”，则显示文档中的所有表格
- 如果用户请求“主要内容”，则过滤掉页眉/页脚，但显示所有正文内容

**具体操作说明**：
- **必须**：根据用户的需求显示完整的文本、所有表格和所有公式
- **必须**：使用以下字段展示内容：最高级别的`text`、`result[n].markdown`和`result[n].prunedResult`
- **禁止**：除非内容过长（超过10,000个字符），否则不要截断内容
- **禁止**：当用户请求完整内容时，不要总结或提供摘录
- **禁止**：当用户期望完整输出时，不要说“这是预览”

**示例 - 正确做法**：
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

**示例 - 错误做法**：
```
User: "Extract all the text"
Agent: "I found a document with multiple sections. Here's the beginning:
'Introduction...' (content truncated for brevity)"
```

### 理解JSON响应

输出的JSON使用一个外壳来包裹原始的API结果：

```json
{
  "ok": true,
  "text": "Full markdown/HTML text extracted from all pages",
  "result": { ... },  // raw provider response
  "error": null
}
```

**关键字段**：
- `text` — 从所有页面提取的Markdown文本（用于快速显示文本）
- `result` — 原始的API响应对象
- `result[n].prunedResult` — 每页的结构化解析结果（包括布局、内容和置信度及相关元数据）
- `result[n].markdown` — 以Markdown/HTML格式渲染的完整页面内容

> 原始结果的位置（默认）：脚本在标准错误输出（stderr）中打印的临时文件路径

### 使用示例

**示例1：提取文档的全部文本**
```bash
python scripts/vl_caller.py \
  --file-url "https://example.com/paper.pdf" \
  --pretty
```

然后使用：
- 最高级别的`text`用于快速显示全部文本
- `result[n].markdown`用于获取页面级别的内容

**示例2：提取结构化页面数据**
```bash
python scripts/vl_caller.py \
  --file-path "./financial_report.pdf" \
  --pretty
```

然后使用：
- `result[n].prunedResult`获取结构化解析数据（包括布局、内容和置信度）
- `result[n].markdown`获取渲染后的页面内容

**示例3：不保存JSON**
```bash
python scripts/vl_caller.py \
  --file-url "URL" \
  --stdout \
  --pretty
```

然后返回：
- 当用户请求全部文档内容时，返回`text`
- 当用户需要完整的结构化页面数据时，返回`result[n].prunedResult`和`result[n].markdown`

### 首次配置

**当API未配置时**：

会显示错误信息：
```
PADDLEOCR_DOC_PARSING_API_URL not configured. Get your API at: https://paddleocr.com
```

**配置流程**：

1. **向用户显示确切的错误信息**（包括URL）。
2. **指导用户安全地进行配置**：
   - 建议通过主机应用程序的标准方法进行配置（例如设置文件、环境变量UI），而不是在聊天中粘贴凭据。
   - 列出所需的环境变量：
     ```
     - PADDLEOCR_DOC_PARSING_API_URL
     - PADDLEOCR_ACCESS_TOKEN
     - Optional: PADDLEOCR_DOC_PARSING_TIMEOUT
     ```

3. **如果用户仍然在聊天中提供凭据**（接受任何合理的格式）：
   - `PADDLEOCR_DOC_PARSING_API_URL=https://xxx.paddleocr.com/layout-parsing, PADDLEOCR_ACCESS_TOKEN=abc123...`
   - `我的API地址是https://xxx，令牌是abc123`
   - 复制的代码格式
   - 任何其他合理的格式
   **安全提示**：警告用户在聊天中分享的凭据可能会被存储在聊天记录中。建议尽可能通过主机应用程序的配置来设置凭据。

4. **解析并验证这些值**：
   - 提取`PADDLEOCR_DOC_PARSING_API_URL`（查找包含`paddleocr.com`或类似内容的URL）
   - 确认`PADDLEOCR_DOC_PARSING_API_URL`是一个以 `/layout-parsing` 结尾的完整端点
   - 提取`PADDLEOCR_ACCESS_TOKEN`（通常为40个以上字符的字母数字字符串）
   - 告知用户需要设置哪些环境变量

5. **询问用户确认环境是否已配置**：
   - 等待用户确认这些值已在他们的主机应用程序、运行时环境或相应的配置文件中设置
   - 出于安全原因，如果技能安装在主机应用程序目录下（例如`~/.claude/skills`），默认情况下不要运行`configure.py`或创建本地`.env`文件

6. **仅在确认后重试**：
   - 一旦用户确认环境变量已设置，再尝试原始的解析任务

**重要提示**：错误信息的格式必须严格遵循脚本提供的格式，不得修改或改述。

### 处理大文件

API没有文件大小限制。对于PDF文件，每次请求的最大页数为100页。

**处理大文件的提示**：

#### 对于大型本地文件，建议使用URL（推荐）
对于非常大的本地文件，建议使用`--file-url`而不是`--file-path`，以避免Base64编码的开销：
```bash
python scripts/vl_caller.py --file-url "https://your-server.com/large_file.pdf"
```

#### 处理特定页面（仅限PDF）
如果只需要大PDF文件中的某些页面，可以先提取这些页面：
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

**API配额超出（429）**：
```
error: API quota exceeded
```
→ 日常API配额已用尽，请告知用户等待或升级

**不支持的格式**：
```
error: Unsupported file format
```
→ 文件格式不受支持，请将其转换为PDF/PNG/JPG

## 重要说明

- **脚本从不过滤内容** — 它总是返回完整的数据
- **AI代理决定展示哪些内容** — 根据用户的特定请求
- **所有数据始终可用** — 可以根据不同需求重新解释
- **没有信息丢失** — 完整的文档结构得到保留

## 参考文档

- `references/output_schema.md` - 输出格式规范

> **注意**：模型版本和功能由您的API端点（`PADDLEOCR_DOC_PARSING_API_URL`）决定。

在以下情况下加载这些参考文档：
- 调试复杂的解析问题
- 需要了解输出格式
- 处理提供商API的详细信息

## 测试此技能

为了验证技能是否正常工作：
```bash
python scripts/smoke_test.py
```

这会测试配置和API连接性。
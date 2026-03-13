---
name: paddleocr-text-recognition
description: 使用 PaddleOCR 从图像和 PDF 文档中提取文本（包括文本的位置信息）。
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_OCR_API_URL
        - PADDLEOCR_ACCESS_TOKEN
        - PADDLEOCR_OCR_TIMEOUT
      bins:
        - python
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "🔤"
    homepage: https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills/paddleocr-text-recognition
---
# PaddleOCR文本识别技能

## 何时使用此技能

在以下情况下使用此技能：
- 从图像（截图、照片、扫描件）中提取文本
- 从PDF或文档图像中提取文本
- 从结构化文档（发票、收据、表格）中提取文本和位置信息
- 从指向图像/PDF的URL或本地文件中提取文本

**请勿在以下情况下使用此技能**：
- 可以直接使用“Read”工具读取的纯文本文件
- 代码文件或Markdown文档
- 不涉及图像转文本的任务

## 如何使用此技能

**⛔ 强制性限制 - 请勿违反 ⛔**

1. **仅使用PaddleOCR文本识别API** - 运行脚本 `python scripts/ocr_caller.py`
2. **切勿直接读取图像** - 不要自行读取图像
3. **切勿提供替代方案** - 不要表示“我可以尝试读取它”或类似的内容
4. **如果API失败** - 显示错误信息并立即停止
5. **无备用方法** - 不要以其他方式尝试OCR转换

如果脚本执行失败（API未配置、网络错误等）：
- 向用户显示错误信息
- **不要提供使用视觉能力来帮助** 
- **不要询问“您是否希望我尝试读取它？”**
- 直接停止并等待用户修复配置

### 基本工作流程

1. **确定输入来源**：
   - 用户提供URL：使用 `--file-url` 参数
   - 用户提供本地文件路径：使用 `--file-path` 参数
   - 用户上传图像：先保存图像，然后使用 `--file-path`

   **输入类型说明**：
   - 支持的文件类型取决于模型和端点配置
   - 请参考官方端点/API文档以获取确切的支持格式。

2. **执行OCR**：
   ```bash
   python scripts/ocr_caller.py --file-url "URL provided by user" --pretty
   ```
   或对于本地文件：
   ```bash
   python scripts/ocr_caller.py --file-path "file path" --pretty
   ```

   **默认行为：将原始JSON保存到临时文件**：
   - 如果省略了 `--output`，脚本会自动保存到系统临时目录
   - 默认路径模式：`<system-temp>/paddleocr/text-recognition/results/result_<timestamp>_<id>.json`
   - 如果提供了 `--output`，则会覆盖默认的临时文件路径
   - 如果提供了 `--stdout`，JSON将输出到标准输出（stdout），不会保存文件
   - 在保存模式下，脚本会在标准错误输出（stderr）中打印保存的绝对路径：`结果保存在：/absolute/path/...`
   - 在默认/自定义保存模式下，在响应之前会读取并解析保存的JSON文件
   - 仅在明确希望跳过文件保存时使用 `--stdout`

3. **解析JSON响应**：
   - 在默认/自定义保存模式下，从脚本显示的保存文件路径加载JSON
   - 检查 `ok` 字段：`true` 表示成功，`false` 表示错误
   - 提取文本：`text` 字段包含所有识别的文本
   - 如果使用了 `--stdout`，则直接解析标准输出的JSON
   - 处理错误：如果 `ok` 为 `false`，显示 `error.message`

4. **向用户展示结果**：
   - 以可读的格式显示提取的文本
   - 如果文本为空，可能表示图像中没有任何文本
   - 在保存模式下，始终告诉用户保存的文件路径以及完整的原始JSON文件的位置

### 重要提示：完整输出显示

**至关重要**：始终向用户显示完整的识别结果。不要截断或总结OCR结果。

- 输出的JSON包含完整的输出，包括 `text` 字段中的全部文本
- **你必须向用户显示全部 `text` 内容**，无论其长度如何
- **不要使用“以下是摘要”或“文本以……开头”之类的表述**
- **除非文本确实超出了合理的显示限制，否则不要使用“……”进行截断**
- 用户期望看到所有被识别的文本，而不仅仅是预览或摘录

**正确的方法**：
```
I've extracted the text from the image. Here's the complete content:

[Display the entire text here]
```

**错误的方法**：
```
I found some text in the image. Here's a preview:
"The quick brown fox..." (truncated)
```

### 使用示例

**示例1：URL OCR**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/invoice.jpg" --pretty
```

**示例2：本地文件OCR**：
```bash
python scripts/ocr_caller.py --file-path "./document.pdf" --pretty
```

**示例3：指定文件类型的OCR**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/input" --file-type 1 --pretty
```

**示例4：不保存地打印JSON**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/input" --stdout --pretty
```

### 理解输出

输出JSON的结构如下：
```json
{
  "ok": true,
  "text": "All recognized text here...",
  "result": { ... },
  "error": null
}
```

**关键字段**：
- `ok`：`true` 表示成功，`false` 表示错误
- `text`：完整的识别文本
- `result`：原始的API响应（用于调试）
- `error`：如果 `ok` 为 `false`，则显示错误详情

> 原始结果位置（默认）：脚本在标准错误输出（stderr）中打印的临时文件路径

### 首次配置

通常可以假设所需的环境变量已经配置好了。只有在OCR任务失败时，才需要分析错误信息以确定是否由配置问题引起。如果是配置问题，应通知用户进行修复。

**当API未配置时**：

错误信息将显示如下：
```
CONFIG_ERROR: PADDLEOCR_OCR_API_URL not configured. Get your API at: https://paddleocr.com
```

**配置流程**：

1. **向用户显示确切的错误信息**（包括URL）。
2. **指导用户安全地进行配置**：
   - 建议通过主机应用程序的标准方法（例如设置文件、环境变量UI）进行配置，而不是在聊天中粘贴凭据。
   - 列出所需的环境变量：
     ```
     - PADDLEOCR_OCR_API_URL
     - PADDLEOCR_ACCESS_TOKEN
     - Optional: PADDLEOCR_OCR_TIMEOUT
     ```

3. **如果用户仍然在聊天中提供凭据**（接受任何合理的格式），例如：
   - `PADDLEOCR_OCR_API_URL=https://xxx.paddleocr.com/ocr, PADDLEOCR_ACCESS_TOKEN=abc123...`
   - `我的API地址是：https://xxx，令牌是：abc123`
   - 复制的代码格式
   - 任何其他合理的格式
   - **安全提示**：警告用户在聊天中分享的凭据可能会被存储在聊天历史记录中。建议尽可能通过主机应用程序的配置来设置它们。

   然后解析并验证这些值：
   - 提取 `PADDLEOCR_OCR_API_URL`（查找包含 `paddleocr.com` 或类似内容的URL）
   - 确认 `PADDLEOCR_OCR_API_URL` 是以 `/ocr` 结尾的完整端点
   - 提取 `PADDLEOCR_ACCESS_TOKEN`（长 alphanumeric 字符串，通常包含40多个字符）

4. **询问用户确认环境是否已配置**。
5. **仅在用户确认环境变量已配置后重试**：
   - 一旦用户确认环境变量可用，重新尝试原始的OCR任务

### 错误处理

**身份验证失败**：
```
API_ERROR: Authentication failed (403). Check your token.
```
- 令牌无效，请使用正确的凭据重新配置

**超出配额**：
```
API_ERROR: API rate limit exceeded (429)
```
- 日常API配额已用尽，请告知用户等待或升级

**未检测到文本**：
- `text` 字段为空
- 图像可能为空、损坏或不含文本

### 提高识别质量的建议

如果识别质量较差，可以建议：
- 检查图像是否清晰且包含文本
- 如果可能，提供更高分辨率的图像

## 参考文档

有关OCR系统的深入理解，请参考：
- `references/output_schema.md` - 输出格式规范

> **注意**：模型版本、功能和支持的文件格式由您的API端点（`PADDLEOCR_OCR_API_URL`）及其官方API文档决定。

## 测试此技能

为了验证技能是否正常工作：
```bash
python scripts/smoke_test.py
```

这用于测试配置和API连接性。
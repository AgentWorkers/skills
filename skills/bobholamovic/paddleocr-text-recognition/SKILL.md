---
name: paddleocr-text-recognition
description: 当用户需要从图像、PDF文件或文档中提取文本时，请使用此技能。该技能支持处理URL和本地文件，并返回包含被识别文本的结构化JSON数据。
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_OCR_API_URL
        - PADDLEOCR_ACCESS_TOKEN
        - PADDLEOCR_TIMEOUT
      bins:
        - python
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "🔤"
    homepage: https://github.com/PaddlePaddle/PaddleOCR/tree/main/skills/paddleocr-text-recognition
---
# PaddleOCR文本识别技能

## 何时使用此技能

在以下情况下使用此技能：
- 从图片（截图、照片、扫描件）中提取文本
- 从PDF或文档图片中提取文本
- 从结构化文档（发票、收据、表格）中提取文本和位置信息
- 从指向图片/PDF的URL或本地文件中提取文本

**请勿在以下情况下使用此技能**：
- 可以直接使用“Read”工具读取的纯文本文件
- 代码文件或Markdown文档
- 不涉及图像到文本转换的任务

## 如何使用此技能

**必须遵守的规则 - 请勿违反**

1. **仅使用PaddleOCR文本识别API** - 运行脚本`python scripts/ocr_caller.py`
2. **切勿直接读取图片** - 不要自行读取图片
3. **切勿提供替代方案** - 不要回答“我可以尝试读取它”之类的问题
4. **如果API失败** - 显示错误信息并立即停止
5. **不得使用其他方法进行OCR处理**

如果脚本执行失败（API配置错误、网络问题等）：
- 向用户显示错误信息
- **不得使用您的视觉能力来帮助用户** 
- **不要询问“您是否希望我尝试读取它？”**
- 直接停止并等待用户修复配置

### 基本工作流程

1. **确定输入来源**：
   - 用户提供URL：使用`--file-url`参数
   - 用户提供本地文件路径：使用`--file-path`参数
   - 用户上传图片：先保存图片，然后使用`--file-path`参数

   **输入类型说明**：
   - 支持的文件类型取决于模型和端点配置
   - 请参考官方端点/API文档以获取确切的支持格式。

2. **执行OCR处理**：
   ```bash
   python scripts/ocr_caller.py --file-url "URL provided by user" --pretty
   ```
   或对于本地文件：
   ```bash
   python scripts/ocr_caller.py --file-path "file path" --pretty
   ```

   **默认行为：将原始JSON保存到临时文件中**：
   - 如果省略`--output`参数，脚本会自动将结果保存在系统临时目录下
   - 默认路径模式：`<system-temp>/paddleocr/text-recognition/results/result_<timestamp>_<id>.json`
   - 如果提供了`--output`参数，将覆盖默认的临时文件路径
   - 如果提供了`--stdout`参数，JSON内容将输出到标准输出（stdout），不会保存到文件中
   - 在保存模式下，脚本会在标准错误输出（stderr）中显示保存的绝对路径：`结果保存在：/absolute/path/...`
   - 在默认/自定义保存模式下，会在响应前读取并解析保存的JSON文件
   - 仅在明确希望跳过文件保存时使用`--stdout`参数

3. **解析JSON响应**：
   - 在默认/自定义保存模式下，从脚本显示的保存路径中加载JSON文件
   - 检查`ok`字段：`true`表示成功，`false`表示错误
   - 提取文本：`text`字段包含所有识别的文本
   - 如果使用了`--stdout`参数，直接解析标准输出的JSON内容
   - 处理错误：如果`ok`为`false`，显示`error.message`

4. **向用户展示结果**：
   - 以可读的格式显示提取的文本
   - 如果文本为空，可能是因为图片中没有任何文本
   - 在保存模式下，务必告知用户保存文件的路径，并说明完整的原始JSON数据也存储在那里

### 重要提示：完整显示输出结果

**关键要求**：务必向用户显示完整的识别结果。不要截断或总结OCR结果。

- 输出的JSON文件包含所有内容，包括`text`字段中的全部文本
- **必须向用户显示全部`text`内容**，无论其长度如何
- **不要使用“以下是摘要”或“文本开头是...”之类的表述**
- **除非文本确实超出了合理的显示范围，否则不要使用“...”进行截断**
- 用户期望看到所有被识别的文本，而不是预览或摘录

**正确做法**：
```
I've extracted the text from the image. Here's the complete content:

[Display the entire text here]
```

**错误做法**：
```
I found some text in the image. Here's a preview:
"The quick brown fox..." (truncated)
```

### 使用示例

**示例1：通过URL进行OCR处理**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/invoice.jpg" --pretty
```

**示例2：对本地文件进行OCR处理**：
```bash
python scripts/ocr_caller.py --file-path "./document.pdf" --pretty
```

**示例3：指定文件类型进行OCR处理**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/input" --file-type 1 --pretty
```

**示例4：直接打印JSON结果而不保存**：
```bash
python scripts/ocr_caller.py --file-url "https://example.com/input" --stdout --pretty
```

### 理解输出结果

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
- `ok`：`true`表示成功，`false`表示错误
- `text`：所有被识别的文本
- `result`：原始的API响应（用于调试）
- `error`：如果`ok`为`false`，则显示错误详情

> **原始结果位置（默认）**：脚本会在标准错误输出（stderr）中显示临时文件的路径

### 首次配置

**当API未配置时**：

会显示以下错误信息：
```
CONFIG_ERROR: PADDLEOCR_OCR_API_URL not configured. Get your API at: https://paddleocr.com
```

**配置流程**：

1. **向用户显示具体的错误信息**（包括URL）
2. **要求用户提供凭据**：
   ```
   Please visit the URL above to get your PADDLEOCR_OCR_API_URL and PADDLEOCR_ACCESS_TOKEN.
   Once you have them, send them to me and I'll configure it automatically.
   ```

3. **当用户提供凭据**（接受任何格式）：
   - `PADDLEOCR_OCR_API_URL=https://xxx.paddleocr.com/ocr, PADDLEOCR_ACCESS_TOKEN=abc123...`
   - “我的API地址是https://xxx，访问令牌是abc123”
   - 可以复制粘贴上述格式
   - 也可以接受其他合理的格式
4. **从用户的消息中提取凭据**：
   - 提取`PADDLEOCR_OCR_API_URL`的值（查找包含“paddleocr.com”等关键词的URL）
   - 提取`PADDLEOCR_ACCESS_TOKEN`的值（通常是一个40个以上字符的字母数字字符串）
5. **自动配置**：
   ```bash
   python scripts/configure.py --api-url "PARSED_URL" --token "PARSED_TOKEN"
   ```

6. **如果配置成功**：
   - 告知用户：“配置完成！现在开始执行OCR处理...” 
   - 重新尝试原始的OCR任务
7. **如果配置失败**：
   - 显示错误信息
   - 要求用户验证凭据

### 错误处理

**身份验证失败**：
```
API_ERROR: Authentication failed (403). Check your token.
```
- 令牌无效，请使用正确的凭据重新配置

**超出使用额度**：
```
API_ERROR: API rate limit exceeded (429)
```
- 日使用额度已用尽，请告知用户等待或升级

**未检测到文本**：
- `text`字段为空
- 可能是因为图片为空、损坏或没有文本

### 提高识别质量的建议

如果识别效果不佳，可以建议：
- 检查图片是否清晰且包含可识别的文本
- 如果可能的话，提供更高分辨率的图片

## 参考文档

有关OCR系统的详细信息，请参考：
- `references/output_schema.md` - 输出格式规范

> **注意**：模型版本、功能和支持的文件格式由您的API端点（`PADDLEOCR_OCR_API_URL`）及其官方文档决定。

## 测试此技能

为了验证技能是否正常工作，请执行以下操作：
```bash
python scripts/smoke_test.py
```

这一步用于测试配置和API连接是否正常。
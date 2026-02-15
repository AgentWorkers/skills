---
name: add-watermark-to-pdf
description: 通过将一个或多个PDF文件上传到Solutions API，等待处理完成，然后获取带有水印的PDF文件的下载链接（如果有多个文件，则返回ZIP压缩包的下载链接）。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-processing
  tags:
    - pdf
    - watermark
    - batch
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# 向PDF文件添加水印

## 功能描述
该功能通过以下步骤向一个或多个PDF文件添加文本水印：
1. 从用户处接收一个或多个PDF文件；
2. 接收用户提供的水印文本字符串；
3. 将这些文件上传到Solutions API；
4. 监控任务状态，直到任务完成；
5. 返回生成文件的下载链接。

如果处理了多个PDF文件，输出结果可能包括多个PDF文件或一个ZIP文件供用户下载。

## 访问权限
该API需要使用API密钥作为身份验证凭据：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方法：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供API密钥。

**注意：** 严禁在代码中显示或记录API密钥。

## API接口
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

- 创建水印任务：
  - `POST /api/61`
  - 请求参数（`multipart/form-data`）：
    - `files` — 必填 — 多个PDF文件
    - `text` — 必填 — 水印文本字符串

- 根据ID获取结果：
  - `GET /api/<ID>`

任务完成后，响应内容包含：
- `output.files[]`，其中每个元素包含 `{ name, path }`，其中`path` 是可下载文件的URL（PDF文件或ZIP文件）。

## 输入参数
### 必填参数
- 一个或多个PDF文件（二进制格式）
- 水印文本（字符串类型）

### 可选参数
- 无

## 输出参数
返回的结构化结果包含以下内容：
- `job_id`（数字）：任务ID
- `status`（字符串）：任务状态
- `outputs`（数组）：每个输出文件的详细信息（包含 `{ name, path }`）
- **便捷字段**：
  - `download_url`（字符串）：如果仅生成一个输出文件，则包含该文件的下载链接
  - `download_urls`（字符串数组）：如果生成多个输出文件，则包含所有文件的下载链接
  - `input_files`（字符串数组）：输入文件的列表
  - `watermark_text`（字符串）：仅在水印文本不敏感的情况下返回；如果用户认为该信息敏感，则不返回

**示例输出：**
```json
{
  "job_id": 6101,
  "status": "done",
  "outputs": [
    { "name": "watermarked.pdf", "path": "https://.../watermarked.pdf" }
  ],
  "download_url": "https://.../watermarked.pdf",
  "download_urls": ["https://.../watermarked.pdf"],
  "input_files": ["input.pdf"]
}
```
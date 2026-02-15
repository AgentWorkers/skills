---
name: convert-to-pdf
description: 将一个或多个文档上传到 Cross-Service-Solutions，等待转换完成，之后返回转换后的 PDF 文件的下载链接（如果有多个文件，则返回 ZIP 文件的下载链接）。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-processing
  tags:
    - pdf
    - convert
    - doc-to-pdf
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# convert-to-pdf

## 功能概述
该功能可将一个或多个文档转换为PDF格式：
1. 从用户处接收一个或多个输入文件；
2. 将这些文件上传到Solutions API的转换端点；
3. 监控转换任务的进度，直到任务完成；
4. 返回生成的PDF文件的下载链接。

如果转换了多个文件，输出结果可能包含多个PDF文件或一个可下载的ZIP文件。

## 访问凭证
该API需要一个API密钥作为身份验证凭据（Bearer令牌）：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方法：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供API密钥。

**注意：** 严禁在日志或任何输出中显示API密钥。

## API端点
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建转换任务：**
- `POST /api/31`
- 使用`multipart/form-data`格式发送请求，包含以下参数：
  - `files`（必填）—— 一个或多个输入文件（格式为binary）

  - 你可以将多个不同类型的文件转换为多个PDF文件；
  - 多个文件也可以被压缩成一个ZIP文件进行下载。

**通过ID获取转换结果：**
- `GET /api/<ID>`

**响应内容：**
- `output.files[]`：包含每个输出文件的名称（`name`）和路径（`path`），其中`path`为可下载的URL（PDF文件或ZIP文件）。

## 输入参数
### 必填参数
- 一个或多个二进制格式的输入文件
- 一个API密钥（字符串）

### 可选参数
- 无

## 输出参数
- `job_id`（数字）：转换任务的唯一标识符
- `status`（字符串）：任务状态（如“done”或“pending”）
- `outputs`（数组）：包含每个输出文件的名称和路径
- **附加信息：**
  - `download_url`（字符串）：如果只有一个输出文件，则包含其下载链接
  - `download_urls`（字符串数组）：如果有多个输出文件，则包含所有文件的下载链接
- `input_files`（字符串数组）：输入文件的列表

**示例输出：**
```json
{
  "job_id": 789,
  "status": "done",
  "outputs": [
    { "name": "file1.pdf", "path": "https://.../file1.pdf" },
    { "name": "file2.pdf", "path": "https://.../file2.pdf" },
    { "name": "converted.zip", "path": "https://.../converted.zip" }
  ],
  "download_urls": [
    "https://.../file1.pdf",
    "https://.../file2.pdf",
    "https://.../converted.zip"
  ],
  "input_files": ["file1.docx", "file2.pptx"]
}
```
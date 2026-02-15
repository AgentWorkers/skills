---
name: remove-metadata-from-pdf
description: 通过将一个或多个PDF文件上传到Solutions API，进行轮询直到处理完成，然后返回处理后的PDF文件的下载链接（如果有多个文件，则返回ZIP压缩包的下载链接）。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-security
  tags:
    - pdf
    - metadata
    - privacy
    - sanitize
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# 从PDF文件中删除元数据

## 功能描述
该功能用于从一个或多个PDF文件中删除元数据，具体步骤如下：
1. 从用户处接收一个或多个PDF文件；
2. 将这些文件上传到Solutions API；
3. 监控任务进度，直到任务完成；
4. 返回处理后的文件的下载链接。

如果同时处理多个PDF文件，输出结果可能包括多个PDF文件或一个ZIP文件供用户下载。

## 访问凭证
该API需要一个API密钥（作为Bearer令牌）：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方式：
- 访问 [https://login.cross-service-solutions.com/register](https://login.cross-service-solutions.com/register) 进行注册；
- 或者用户可以直接提供API密钥。

**注意：** 严禁在日志或任何输出中显示API密钥。

## API接口
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

### 创建任务
- `POST /api/40`
  - `multipart/form-data` 参数：
    - `files` — 必填项 — 多个PDF文件（以文件路径的形式提供）

### 通过ID获取结果
- `GET /api/<ID>`

任务完成后，响应内容包含以下信息：
- `output.files[]`：每个输出文件的名称和路径，其中路径表示可下载的文件地址（PDF文件或ZIP文件）。

## 输入参数
### 必填参数
- 一个或多个PDF文件（二进制格式）
- API密钥（字符串）

### 可选参数
- 无

## 输出参数
返回的结构化结果包括：
- `job_id`（数字）：任务ID
- `status`（字符串）：任务状态
- `outputs`（数组）：每个输出文件的名称和路径
- **辅助字段**：
  - `download_url`（字符串）：如果仅有一个输出文件，则包含该文件的下载链接
  - `download_urls`（字符串数组）：如果有多个输出文件，则包含所有文件的下载链接
- `input_files`（字符串数组）：输入文件的路径列表

**示例输出：**
```json
{
  "job_id": 990,
  "status": "done",
  "outputs": [
    { "name": "cleaned.pdf", "path": "https://.../cleaned.pdf" }
  ],
  "download_url": "https://.../cleaned.pdf",
  "download_urls": ["https://.../cleaned.pdf"],
  "input_files": ["input.pdf"]
}
```
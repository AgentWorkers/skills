---
name: compress-pdf
description: 将用户提供的 PDF 文件上传到 Cross-Service-Solutions，等待压缩完成，之后返回压缩文件的下载链接。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-processing
  tags:
    - pdf
    - compression
    - cross-service-solutions
  provider: Cross-Service-Solutions (XSS)
allowed-tools:
  - http
  - files
---

# compress-pdf

## 功能描述
该功能用于压缩 PDF 文件：
1. 从用户处接收 PDF 文件；
2. 将文件上传至 Cross-Service-Solutions 的压缩 API；
3. 监控压缩任务的进度，直到任务完成；
4. 返回压缩后的 PDF 文件的下载链接。

## 认证信息
该 API 需要一个 API 密钥作为身份验证凭据（Bearer Token）：
- `Authorization: Bearer <API_KEY>`

用户获取 API 密钥的方式：
- 用户可以在以下链接注册并获取密钥：  
  https://login.cross-service-solutions.com/register
- 或者直接将 API 密钥提供给相关系统/机器人。

**注意：** 严禁在任何地方显示或记录 API 密钥。

## API 端点
基础 URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建压缩任务：**
- `POST /api/29`
- 请求参数（使用 `multipart/form-data` 格式）：
  - `file`（必填）：PDF 文件
  - `imageQuality`（必填）：数值范围 0–100（默认值 75）
  - `dpi`（必填）：数值范围 72–300（默认值 144）

**通过 ID 获取结果：**
- `GET /api/<ID>`

**响应内容：**
- `output.files[]`：包含压缩后的文件信息，每个文件的信息结构如下：
  - `name`：文件名称
  - `path`：文件的下载链接

## 输入参数
### 必填参数
- 一个 PDF 文件（二进制格式）
- 一个 API 密钥（字符串）

### 可选参数
- `imageQuality`（数值范围 0–100，默认值 75）
- `dpi`（数值范围 72–300，默认值 144）

## 输出参数
返回以下结构化的结果：
- `job_id`（整数）：任务 ID
- `status`（字符串）：任务状态（如 “done” 表示任务已完成）
- `download_url`（字符串）：压缩后的 PDF 文件下载链接
- `file_name`（字符串）：压缩后的 PDF 文件名称
- `settings`（对象）：压缩任务的相关设置（如 `imageQuality`、`dpi` 等）

**示例输出：**
```json
{
  "job_id": 123,
  "status": "done",
  "download_url": "https://.../compressed.pdf",
  "file_name": "compressed.pdf",
  "settings": { "imageQuality": 75, "dpi": 144 }
}
```
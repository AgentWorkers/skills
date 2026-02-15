---
name: password-protect-pdf
description: 通过将PDF文件上传到Solutions API，等待处理完成，然后返回受保护的PDF文件的下载链接，从而为PDF文件添加密码保护。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-security
  tags:
    - pdf
    - password
    - encrypt
    - security
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# 通过密码保护 PDF 文件

## 功能概述
本功能通过以下步骤实现 PDF 文件的密码保护：
1. 从用户处接收 PDF 文件；
2. 从用户处接收密码；
3. 将 PDF 文件和密码一起上传到 Solutions API；
4. 持续检查任务状态，直到任务完成；
5. 返回已加密 PDF 文件的下载链接。

## 认证信息
API 需要一个 API 密钥作为承载令牌（Bearer token）：
- `Authorization: Bearer <API_KEY>`

用户获取 API 密钥的方式：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供 API 密钥。

**注意：** 严禁在代码中显示或记录 API 密钥。

## API 端点
基础 URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建密码保护任务：**
- `POST /api/32`
- 请求参数（`multipart/form-data`）：
  - `file`（必填）：PDF 文件
  - `userPass`（必填）：密码（字符串形式）

**通过 ID 获取结果：**
- `GET /api/<ID>`

任务完成后，响应中会包含以下信息：
- `output.files[]`：包含文件信息（`name` 和 `path`），其中 `path` 是可下载的 PDF 文件链接。

## 输入参数
### 必填参数
- PDF 文件（二进制格式）
- 密码（`userPass`，字符串类型）
- API 密钥（字符串类型）

### 可选参数
- 无

## 输出参数
返回的结构化结果包括：
- `job_id`（数字类型）：任务 ID
- `status`（字符串类型）：任务状态
- `download_url`（字符串类型）：已加密 PDF 文件的下载链接
- `file_name`（字符串类型）：PDF 文件的名称（如果已生成）

**示例输出：**
```json
{
  "job_id": 321,
  "status": "done",
  "download_url": "https://.../protected.pdf",
  "file_name": "protected.pdf"
}
```
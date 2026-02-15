---
name: make-pdf-safe
description: 将 PDF 文件转换为非交互式的“安全”版本：首先将其上传到 Solutions API，然后持续轮询直到转换完成，最后返回转换后的 PDF 文件的下载链接。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-security
  tags:
    - pdf
    - flatten
    - sanitize
    - security
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# make-pdf-safe

## 目的
该功能通过将文档转换为单一的、无交互功能的平面化层来创建一个“安全”的PDF文件。这样做的目的是降低因PDF中的交互式功能而带来的风险。

在实际应用中，生成的PDF文件将：
- 移除或禁用所有交互式元素（例如脚本/操作）；
- 防止对底层对象或内容结构的编辑；
- 表现得像一个平面化的文档（类似于“打印”后的效果）。

该功能的具体步骤如下：
1) 从用户处接收一个PDF文件；
2) 将该文件上传到Solutions API；
3) 监控任务状态，直到任务完成；
4) 返回“安全”平面化PDF文件的下载链接。

## 认证信息
API需要一个API密钥作为身份验证令牌：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方法：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供API密钥。

**注意：** 严禁在任何地方显示或记录API密钥。

## API端点
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

创建“安全PDF”任务的请求：
- `POST /api/41`
- 请求参数（`multipart/form-data`）：
  - `file` — 必需 — PDF文件

通过ID获取结果：
- `GET /api/<ID>`

任务完成后，响应内容包含：
- `output.files[]`，其中每个元素包含 `{ name, path }`，其中`path` 是可下载的PDF文件链接。

## 输入参数
### 必需参数
- PDF文件（二进制格式）
- API密钥（字符串）

### 可选参数
- 无

## 输出参数
返回的结构化结果包括：
- `job_id`（数字）：任务ID
- `status`（字符串）：任务状态
- `download_url`（字符串）：PDF文件的下载链接（任务完成后提供）
- `file_name`（字符串）：PDF文件的名称（如果可用）

示例输出：
```json
{
  "job_id": 4101,
  "status": "done",
  "download_url": "https://.../safe.pdf",
  "file_name": "safe.pdf"
}
```
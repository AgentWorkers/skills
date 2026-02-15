---
name: remove-password-from-pdf
description: 通过将包含当前密码的 PDF 文件上传到 Solutions API，等待处理完成，然后获取解密后的 PDF 文件的下载链接，从而移除该 PDF 文件的密码保护。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-security
  tags:
    - pdf
    - unlock
    - remove-password
    - decrypt
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# 从PDF文件中移除密码保护

## 功能描述
该功能用于移除PDF文件的密码保护，具体步骤如下：
1. 从用户处接收需要解密的PDF文件；
2. 从用户处获取当前的密码；
3. 将PDF文件和密码一起上传到Solutions API；
4. 监听任务状态，直到解密完成；
5. 返回解密后的PDF文件的下载链接。

## 认证信息
Solutions API需要一个API密钥作为身份验证凭据：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方法：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供API密钥。

**注意：** 严禁在任何地方显示或记录API密钥。

## API接口
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建解密任务：**
- `POST /api/33`
- 请求参数（使用`multipart/form-data`格式）：
  - `file`（必填）：需要解密的PDF文件
  - `password`（必填）：用于解密的当前密码（字符串形式）

**通过ID获取结果：**
- `GET /api/<ID>`

**响应内容：**
- `output.files[]`：包含解密后的PDF文件信息，每个文件的信息结构为 `{ name, path }`，其中`path`表示可下载的PDF文件链接。

## 输入参数
### 必需参数
- PDF文件（二进制格式）
- 当前密码（字符串形式）
- API密钥（字符串形式）

### 可选参数
- 无

## 输出结果
返回以下结构化的信息：
- `job_id`（数字）：任务ID
- `status`（字符串）：任务状态（如“done”表示任务已完成）
- `download_url`（字符串）：解密后的PDF文件下载链接
- `file_name`（字符串）：解密后的PDF文件名（如果已生成）

**示例输出：**
```json
{
  "job_id": 654,
  "status": "done",
  "download_url": "https://.../unlocked.pdf",
  "file_name": "unlocked.pdf"
}
```
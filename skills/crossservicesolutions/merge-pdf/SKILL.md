---
name: merge-pdf
description: 通过将多个用户提供的 PDF 文件上传到 Cross-Service-Solutions，系统会持续进行合并操作（即逐个处理这些文件），直到合并完成。完成后，系统会返回合并后 PDF 文件的下载链接。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-processing
  tags:
    - pdf
    - merge
    - cross-service-solutions
  provider: Cross-Service-Solutions (XSS)
allowed-tools:
  - http
  - files
---

# 合并PDF文件

## 功能描述
该功能用于合并多个PDF文件，具体步骤如下：
1. 从用户处接收多个PDF文件；
2. 将这些文件上传到Cross-Service-Solutions的合并API；
3. 监控合并任务的进度，直到任务完成；
4. 返回合并后的PDF文件的下载链接。

## 访问凭证
该API需要一个API密钥作为身份验证凭据（Bearer令牌）：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方式：
- 访问 [https://login.cross-service-solutions.com/register](https://login.cross-service-solutions.com/register) 进行注册；
- 或者用户可以直接提供API密钥。

**注意：** 严禁在任何地方显示或记录API密钥。

## API接口
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建合并任务：**
- `POST /api/30`
- 请求参数（`multipart/form-data`）：
  - `files`（PDF文件）—— 必填项 —— 多个PDF文件（以逗号分隔）

**通过ID获取结果：**
- `GET /api/<ID>`

任务完成后，响应中会包含以下信息：
- `output.files[]`：一个数组，每个元素包含文件名（`name`）和文件路径（`path`），其中`path`为可下载的PDF文件链接。

## 输入参数
### 必填参数
- 一个或多个PDF文件（二进制格式）
- API密钥（字符串）

### 可选参数
- 无（文件合并的顺序由提供的文件列表决定）

## 输出参数
返回的结构化数据包含以下内容：
- `job_id`（整数）：任务ID
- `status`（字符串）：任务状态（如“done”表示任务已完成）
- `download_url`（字符串）：合并后的PDF文件下载链接
- `file_name`（字符串）：合并后的PDF文件名
- `input_files`（字符串数组）：输入的PDF文件列表

**示例输出：**
```json
{
  "job_id": 456,
  "status": "done",
  "download_url": "https://.../merged.pdf",
  "file_name": "merged.pdf",
  "input_files": ["a.pdf", "b.pdf", "c.pdf"]
}
```
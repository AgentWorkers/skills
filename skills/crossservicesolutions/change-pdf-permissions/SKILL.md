---
name: change-pdf-permissions
description: 通过将PDF文件上传到Solutions API，等待处理完成，之后获取更新后的PDF文件的下载链接，从而更改该PDF文件的权限设置（如编辑、打印、复制、添加注释等）。
license: MIT
compatibility:
  agentskills: ">=0.1.0"
metadata:
  category: document-security
  tags:
    - pdf
    - permissions
    - restrict
    - allow
    - security
    - cross-service-solutions
  provider: Cross-Service-Solutions (Solutions API)
allowed-tools:
  - http
  - files
---

# 修改PDF权限

## 目的
此功能用于修改PDF文件的权限设置（例如，是否可以打印、编辑或复制）。具体操作步骤如下：
1) 从用户处接收PDF文件；
2) 接收用户指定的权限设置（true/false）；
3) 将这些设置上传到Solutions API；
4) 监控任务进度直至完成；
5) 返回更新后的PDF文件的下载链接。

## 认证信息
该API需要一个API密钥作为身份验证凭据（Bearer token）：
- `Authorization: Bearer <API_KEY>`

用户获取API密钥的方法：
- 访问：https://login.cross-service-solutions.com/register
- 或者用户可以直接提供API密钥。

**注意规则：** 严禁在代码中显示或记录API密钥。

## API接口
基础URL：
- `https://api.xss-cross-service-solutions.com/solutions/solutions`

**创建权限修改任务：**
- `POST /api/75`
- 请求参数（`multipart/form-data`）：
  - `file` — 必需 — PDF文件
  - `canModify` — 必需 — “true” 或 “false”
  - `canModifyAnnotations` — 必需 — “true” 或 “false”
  - `canPrint` — 必需 — “true” 或 “false”
  - `canPrintHighQuality` — 必需 — “true” 或 “false”
  - `canAssembleDocument` — 必需 — “true” 或 “false”
  - `canFillInForm` — 必需 — “true” 或 “false”
  - `canExtractContent` — 必需 — “true” 或 “false”
  - `canExtractForAccessibility` — 必需 — “true” 或 “false”

**通过ID获取结果：**
- `GET /api/<ID>`

任务完成后，响应内容包含：
- `output.files[]`，其中每个元素包含 `{ name, path }`，`path` 即为可下载的PDF文件链接。

## 输入参数
### 必需参数
- PDF文件（二进制格式）
- 权限设置（布尔值）：API要求的所有权限参数：
  - `canModify`
  - `canModifyAnnotations`
  - `canPrint`
  - `canPrintHighQuality`
  - `canAssembleDocument`
  - `canFillInForm`
  - `canExtractContent`
  - `canExtractForAccessibility`
- API密钥（字符串）

### 可选参数
- 无

## 默认值（推荐设置）
如果用户未指定权限设置，建议使用以下保守的默认值：
- `canModify`: false
- `canModifyAnnotations`: false
- `canPrint`: true
- `canPrintHighQuality`: true
- `canAssembleDocument`: false
- `canFillInForm`: true（如果文件中包含表单的话，这个设置较为合理）
- `canExtractContent`: false
- `canExtractForAccessibility`: true（通常为了满足无障碍访问需求）

这些默认值可根据产品政策进行调整。

## 输出结果
返回的结构化数据包括：
- `job_id`（数字）
- `status`（字符串，表示任务状态）
- `download_url`（字符串，文件下载链接）
- `file_name`（字符串，文件名称）
- `permissions`（对象，包含最终的权限设置）

**示例输出：**
```json
{
  "job_id": 7501,
  "status": "done",
  "download_url": "https://.../permissions.pdf",
  "file_name": "permissions.pdf",
  "permissions": {
    "canModify": false,
    "canModifyAnnotations": false,
    "canPrint": true,
    "canPrintHighQuality": true,
    "canAssembleDocument": false,
    "canFillInForm": true,
    "canExtractContent": false,
    "canExtractForAccessibility": true
  }
}
```
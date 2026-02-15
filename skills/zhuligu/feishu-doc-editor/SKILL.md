---
name: feishu-doc-editor
description: 使用 OpenAPI 进行 Feishu 文档的创建和编辑操作。当用户需要以编程方式创建、编辑或读取 Feishu 文档时，该功能会被激活。
---
# Feishu 文档编辑技能

本技能提供了使用 Feishu OpenAPI 创建和编辑 Feishu 文档的全面指导。

## 先决条件

### 1. 应用程序的创建与配置

- **创建企业自建应用**：登录 Feishu Open Platform，创建一个应用并添加“机器人”功能。
- **申请 API 权限**：在“权限管理”中，申请以下权限：
  - 文档编辑：`docx:document:write_only`
  - 文档查看：`docx:document:readonly`
- **发布应用**：提交版本并发布应用，确保应用覆盖的目标用户/部门正确。

### 2. 获取访问令牌

调用自建应用的 `get TenantAccessToken` 接口：

```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id": "your_app_id", "app_secret": "your_app_secret"}'
```

响应示例：

```json
{
  "code": 0,
  "tenant_access_token": "t-xxx",
  "expire": 7200
}
```

## 核心操作

### 提取文档 ID

从文档 URL 中获取 `document_id`：

**示例 URL**：`https://bigdatacenter.feishu.cn/docx/HpK2dtGu9omhMAxV12zcB6i7ngd`

**document_id** = `HpK2dtGu9omhMAxV12zcB6i7ngd`

### 授予应用文档权限

- **手动添加协作者**：
  - 在 Feishu 客户端中打开文档 → 点击右上角的 “...” → “更多” → “添加文档应用”
  - 搜索并添加您的应用，授予 “可以编辑” 权限。

### 编写文本内容

**接口**：Create Block（创建块）
- **路径参数**：`document_id` = 文档 ID，`block_id` = 文档 ID（根节点即为文档本身）
- **请求头**：
  ```http
  Authorization: Bearer {tenant_access_token}
  Content-Type: application/json
  ```

- **请求体示例**（编写 “hello”）：
  ```json
  {
    "index": -1,
    "children": [
      {
        "block_type": 2,
        "text": {
          "elements": [
            {
              "text_run": {
                "content": "hello"
              }
            }
          ]
        }
      }
    ]
  }
  ```

### 读取文档内容

**接口**：Get Document Plain Text（获取文档纯文本）

```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/{document_id}/plaintext" \
  -H "Authorization: Bearer {tenant_access_token}"
```

响应示例：

```json
{
  "code": 0,
  "data": {
    "content": "Document text content here"
  }
}
```

## 常见问题

### 1. 权限错误（403 Forbidden）

- **诊断**：应用未添加为文档协作者，或 `tenant_access_token` 无效。
- **解决方案**：重新将应用添加为协作者，或重新获取 `tenant_access_token`。

### 2. 丢失访问令牌（99991661）

- **诊断**：请求头未包含 `Authorization: Bearer {token}`。
- **解决方案**：确保 `tenant_access_token` 正确添加到请求头中。

### 3. 文档未找到（404 Not Found）

- **诊断**：`document_id` 错误或文档已被删除。
- **解决方案**：重新从文档 URL 中提取 `document_id`。

## 参考文档

- Create Block 接口
- Get Document Plain Text 接口
- 权限配置指南

通过以上步骤，您可以通过 API 实现对 Feishu 文档的编辑操作，支持对文本、表格和图片等多种内容类型的添加、删除、修改和查询操作。
---
name: microsoft-code-reference
description: 查阅 Microsoft API 参考资料，寻找可用的代码示例，并验证 SDK 代码的正确性。在处理 Azure SDK、.NET 库或 Microsoft API 时，可以使用这些资源来查找合适的方法、检查参数、获取可运行的示例或排查错误。通过查询官方文档，可以发现那些不存在的方法、错误的签名以及已被弃用的代码模式。
context: fork
compatibility: Requires Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)
---

# 微软代码参考

## 先决条件：连接到 Microsoft Learn MCP 服务器

**重要提示：** 本技能需要使用 **Microsoft Learn MCP 服务器**（类型：http，网址：https://learn.microsoft.com/api/mcp）。如果尚未连接，请自行安装并配置该服务器。如有需要，请向用户申请权限。

Microsoft Learn MCP 是微软提供的免费官方服务，无需 API 密钥或身份验证。

## 工具

| 功能 | 工具 | 示例 |
|------|------|---------|
| 查找 API 方法/类 | `microsoft_docs_search` | `"BlobClient UploadAsync Azure.Storage.Blobs"` |
| 获取可运行的代码示例 | `microsoft_code_sample_search` | `query: "upload blob managed identity", language: "python"` |
| 查看完整的 API 参考文档 | `microsoft_docs_fetch` | 从 `microsoft_docs_search` 获取 API 文档（包括重载版本和完整签名信息） |

## 查找代码示例

使用 `microsoft_code_sample_search` 来获取官方提供的、可运行的代码示例：

```
microsoft_code_sample_search(query: "upload file to blob storage", language: "csharp")
microsoft_code_sample_search(query: "authenticate with managed identity", language: "python")
microsoft_code_sample_search(query: "send message service bus", language: "javascript")
```

**使用场景：**
- 在编写代码之前——查找可参考的实现模式
- 出现错误时——将你的代码与已知正确的示例进行对比
- 对初始化或设置步骤不确定时——示例代码可以提供完整的上下文信息

## API 查阅

```
# Verify method exists (include namespace for precision)
"BlobClient UploadAsync Azure.Storage.Blobs"
"GraphServiceClient Users Microsoft.Graph"

# Find class/interface
"DefaultAzureCredential class Azure.Identity"

# Find correct package
"Azure Blob Storage NuGet package"
"azure-storage-blob pip package"
```

当某个 API 方法具有多个重载版本或你需要查看完整的参数信息时，可以使用 `microsoft_docs_fetch` 来获取完整的 API 文档。

## 错误排查

使用 `microsoft_code_sample_search` 查找可运行的代码示例，并将其与你的实现进行对比。对于特定的错误，可以结合使用 `microsoft_docs_search` 和 `microsoft_docs_fetch`：

| 错误类型 | 查询内容 |
|------------|-------|
| 方法未找到 | `"[ClassName] methods [Namespace]"` |
| 类型未找到 | `"[TypeName] NuGet package namespace"` |
| 签名错误 | `"[ClassName] [MethodName] overloads"` → 获取完整的 API 文档 |
| 被弃用的功能 | `"[OldType] migration v12"` |
| 身份验证失败 | `"DefaultAzureCredential troubleshooting"` |
| 403 禁止访问 | `"[ServiceName] RBAC permissions"` |

## 需要验证的情况

在以下情况下务必进行验证：
- 方法名称看起来过于简陋（例如 `UploadFile` 实际应为 `Upload`）
- 混合使用不同版本的 SDK（例如 v11 的 `CloudBlobClient` 和 v12 的 `BlobServiceClient`）
- 包名不符合规范（.NET 通常使用 `Azure.*`，Python 使用 `azure-*`）
- 首次使用某个 API

## 验证流程

在使用微软 SDK 生成代码之前，请按照以下步骤进行验证：
1. **确认方法或包的存在** — `microsoft_docs_search(query: "[ClassName] [MethodName] [Namespace]")`
2. **获取完整的信息**（针对具有重载参数的方法） — `microsoft_docs_fetch(url: "...")`
3. **查找可运行的代码示例** — `microsoft_code_sample_search(query: "[task]", language: "[lang]")`

对于简单的查询，步骤 1 即可；对于复杂的 API 使用场景，需要完成所有三个步骤。
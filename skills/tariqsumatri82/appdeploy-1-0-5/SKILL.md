---
name: appdeploy
description: 部署包含后端 API、数据库和文件存储功能的 Web 应用程序。适用于用户希望部署或发布网站或 Web 应用程序，并且需要一个公共 URL 的情况。通过 `curl` 命令使用 HTTP API 进行部署。
allowed-tools:
  - Bash
metadata:
  author: appdeploy
  version: "1.0.5"
---

# AppDeploy 技能

通过 HTTP API 将 Web 应用程序部署到 AppDeploy。

## 设置（仅首次使用）

1. **检查是否存在 API 密钥：**
   - 在项目根目录中查找 `.appdeploy` 文件。
   - 如果存在且包含有效的 `api_key`，则跳转到“使用”部分。

2. **如果不存在 API 密钥，请注册并获取一个：**
   ```bash
   curl -X POST https://api-v2.appdeploy.ai/mcp/api-key \
     -H "Content-Type: application/json" \
     -d '{"client_name": "claude-code"}'
   ```

   响应：
   ```json
   {
     "api_key": "ak_...",
     "user_id": "agent-claude-code-a1b2c3d4",
     "created_at": 1234567890,
     "message": "Save this key securely - it cannot be retrieved later"
   }
   ```

3. **将凭据保存到 `.appdeploy` 文件中：**
   ```json
   {
     "api_key": "ak_...",
     "endpoint": "https://api-v2.appdeploy.ai/mcp"
   }
   ```

   如果 `.appdeploy` 文件尚不存在，请将其添加到 `.gitignore` 文件中。

## 使用方法

向 MCP 端点发送 JSON-RPC 请求：

```bash
curl -X POST {endpoint} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "{tool_name}",
      "arguments": { ... }
    }
  }'
```

## 工作流程

1. **首先，获取部署说明：**
   调用 `get_deployinstructions` 以了解部署要求和限制。

2. **获取应用模板：**
   使用选定的 `app_type` 和 `frontend_template` 调用 `get_app_template`。

3. **部署应用程序：**
   使用应用文件调用 `deploy_app`。对于新应用程序，将 `app_id` 设置为 `null`。

4. **检查部署状态：**
   调用 `get_app_status` 以确认构建是否成功。

5. **查看/管理应用程序：**
   使用 `get_apps` 列出已部署的应用程序。

## 可用工具

### get_deployinstructions

在调用 `deploy_app` 之前使用此工具，以获取部署要求和限制。在开始生成任何代码之前必须先调用此工具。此工具仅返回说明，不会执行任何部署操作。

**参数：**

### deploy_app

当用户请求部署或发布网站/Web 应用程序并希望获得公共 URL 时使用此工具。
在生成文件或调用此工具之前，必须先调用 `get_deployinstructions` 并遵守其限制。

**参数：**
  - `app_id`：任意（必填）- 要更新的应用程序 ID；对于新应用程序，设置为 `null`。
  - `app_type`：字符串（必填）- 应用程序架构：仅前端或前端+后端。
  - `app_name`：字符串（必填）- 应用程序的简短显示名称。
  - `description`：字符串（可选）- 应用程序的简要描述。
  - `frontend_template`：任意（可选）- 当 `app_id` 为 `null` 时必填。可选值包括：'html-static'（简单网站）、'react-vite'（单页应用程序/游戏）、'nextjs-static'（多页面应用程序）。模板文件会自动包含在内。
  - `files`：数组（可选）- 要写入的文件。对于新应用程序：仅包含自定义文件及与模板文件的差异；对于更新：仅包含使用 `diffs[]` 的更改文件。`files[]` 或 `deletePaths[]` 至少需要其中一个参数。
  - `deletePaths`：数组（可选）- 要删除的路径。仅适用于更新操作（`app_id` 必填）。不能删除 `package.json` 或框架入口文件。

### get_app_template

在使用 `deploy_app` 之前，请先调用 `get_deployinstructions`。在确定 `app_type` 和 `frontend_template` 后再调用此工具。该工具返回基础应用程序模板和 SDK 类型。模板文件会自动包含在 `deploy_app` 中。

**参数：**
  - `app_type`：字符串（必填）
  - `frontend_template`：字符串（必填）- 前端框架：
    - 'html-static' - 简单网站，最小化框架；
    - 'react-vite' - React 单页应用程序/仪表板/游戏；
    - 'nextjs-static' - 多页面应用程序，SSG（静态站点生成）。

### get_app_status

当 `deploy_app` 工具返回结果时，或用户请求检查应用程序的部署状态，或报告应用程序出现错误或无法正常运行时使用此工具。返回部署状态（进行中：`deploying`/`deleting`；终端：`ready`/`failed`/`deleted`），以及质量保证快照（前端/网络错误）和实时前端/后端错误日志。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。
  - `since`：整数（可选）- 用于过滤错误的自纪元毫秒时间戳。提供此参数后，仅返回自该时间戳以来的错误。

### delete_app

当您希望永久删除应用程序时使用此工具。此操作不可逆；删除后，状态检查将显示“未找到”。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。

### get_app_versions

列出现有应用程序的可部署版本。需要 `app_id`。返回按最新版本优先排序的列表（格式为 `{name, version, timestamp}`）。向用户显示 `name`，但不显示 `version` 值。时间戳值必须转换为用户的本地时间。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。

### apply_app_version

开始将现有应用程序部署到特定版本。使用 `get_app_versions` 返回的 `version` 值（而非 `name`）。如果部署成功，则返回 `true`；使用 `get_app_status` 监控部署进度。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。
  - `version`：字符串（必填）- 要应用的版本 ID。

### srcglob

当您需要查找应用程序源代码快照中的文件时使用此工具。返回匹配全局模式的文件路径（不包含文件内容）。在读取或搜索文件之前，可用于探索项目结构。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。
  - `version`：字符串（可选）- 要检查的版本（默认为当前应用的版本）。
  - `path`：字符串（可选）- 在其中搜索的目录路径。
  - `glob`：字符串（可选）- 用于匹配文件的全局模式（默认：`/*`）。
  - `include_dirs`：布尔值（可选）- 是否在结果中包含目录路径。
  - `continuation_token`：字符串（可选）- 用于分页的上一响应中的令牌。

### src_grep

当您需要在应用程序源代码中搜索模式时使用此工具。返回匹配的行以及可选的上下文信息。支持正则表达式模式、全局过滤器和多种输出模式。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。
  - `version`：字符串（可选）- 要搜索的版本（默认为当前应用的版本）。
  - `pattern`：字符串（必填）- 要搜索的正则表达式模式（最多 500 个字符）。
  - `path`：字符串（可选）- 在其中搜索的目录路径。
  - `glob`：字符串（可选）- 用于过滤文件的全局模式（例如：`*.ts`）。
  - `case_insensitive`：布尔值（可选）- 是否区分大小写进行匹配。
  - `output_mode`：字符串（可选）- 输出方式：
    - `content`：匹配的行；
    - `files_with_matches`：仅包含匹配文件的路径；
    - `count`：每文件的匹配行数。
  - `before_context`：整数（可选）- 每个匹配项之前的显示行数（0-20）。
  - `after_context`：整数（可选）- 每个匹配项之后的显示行数（0-20）。
  - `context`：整数（可选）- 每个匹配项之前的和之后的行数（覆盖 `before_context`/`after_context`）。
  - `line_numbers`：布尔值（可选）- 是否在输出中包含行号。
  - `max_file_size`：整数（可选）- 扫描的最大文件大小（以字节为单位，默认为 10MB）。
  - `continuation_token`：字符串（可选）- 用于分页的上一响应中的令牌。

### src_read

当您需要从应用程序源代码快照中读取特定文件时使用此工具。返回基于行的文件内容，并支持分页（偏移量/限制）。支持文本文件和二进制文件。

**参数：**
  - `app_id`：字符串（必填）- 目标应用程序 ID。
  - `version`：字符串（可选）- 要读取的版本（默认为当前应用的版本）。
  - `file_path`：字符串（必填）- 要读取的文件路径。
  - `offset`：整数（可选）- 开始读取的行偏移量（从 0 开始计数）。
  - `limit`：整数（可选）- 返回的行数（最多 2000 行）。

### get_apps

当您需要列出当前用户拥有的应用程序时使用此工具。返回应用程序详细信息，包括用于用户展示的字段和用于工具链操作的字段。

**参数：**
  - `continuation_token`：字符串（可选）- 用于分页的令牌。

---
*由 `scripts/generate-appdeploy-skill.ts` 生成*
---
name: fabric-api
description: 通过 Fabric HTTP API 创建、搜索和管理 Fabric 资源（包括便笺、文件夹、书签、文件和标签）。
homepage: https://fabric.so
metadata: {"openclaw":{"emoji":"🧵","homepage":"https://fabric.so","requires":{"env":["FABRIC_API_KEY"],"anyBins":["node","python3","python","curl"]},"primaryEnv":"FABRIC_API_KEY"},"clawdbot":{"emoji":"🧵","homepage":"https://fabric.so","requires":{"env":["FABRIC_API_KEY"],"anyBins":["node","python3","python","curl"]},"primaryEnv":"FABRIC_API_KEY"}}
---
# Fabric API（通过Node/Python访问）

当您需要使用Fabric HTTP API（`https://api.fabric.so`）来**读取或写入用户的工作区内容**时，请使用此技能。

此版本不再使用仅支持bash的封装脚本，而是提供了**跨平台**的帮助工具：

- Node.js：`{baseDir}/scripts/fabric.mjs`（推荐使用）
- Python：`{baseDir}/scripts/fabric.py`

## 重要注意事项（请先阅读）

- 搭载的OpenAPI规范中**没有**`POST /v2/notes`端点。要创建“笔记”，请使用`POST /v2/notepads`。
- 大多数创建端点都需要`parentId`：
  - 一个文件夹的UUID，或者`@alias::inbox`、`@alias::bin`之一。
- 创建笔记本需要：
  - `parentId`
  - 以及`text`（Markdown字符串）或`ydoc`（高级/结构化格式）。
- `tags`必须是一个对象数组，每个对象可以是：
  - `{ "name": "标签名称" }` 或 `{ "id": "<uuid>" }`
  - 不能是字符串，也不能是嵌套数组。
- **字段名称注意事项**：API规范使用的是`name`（而非`title`）。如果用户使用“title”，请在请求中将其映射为`name`。

当用户未指定目标文件夹时，默认值为：

- `parentId: "@alias::inbox"`

## 设置（OpenClaw / Clawdbot）

此技能需要`FABRIC_API_KEY`来访问Fabric API：

OpenClaw配置示例（`~/.openclaw/openclaw.json`）：

```json5
{
  skills: {
    entries: {
      "fabric-api": {
        enabled: true,
        apiKey: "YOUR_FABRIC_API_KEY"
      }
    }
  }
}
```

**说明**：
- `apiKey`是为声明`primaryEnv`的技能提供的便利功能；它会在代理运行期间注入`FABRIC_API_KEY`。
- 请不要将API密钥粘贴到提示信息、客户端代码或日志中。

## HTTP基础知识

- 基本URL：`https://api.fabric.so`（如有需要，可以通过`FABRIC_BASE`进行覆盖）
- 身份验证头：`X-Api-Key: $FABRIC_API_KEY`
- JSON请求体对应的头信息：`Content-Type: application/json`

## 跨平台辅助脚本

### Node.js辅助工具（推荐使用）

```bash
node {baseDir}/scripts/fabric.mjs GET /v2/user/me

node {baseDir}/scripts/fabric.mjs POST /v2/notepads --json '{"name":"Test note","text":"Hello","parentId":"@alias::inbox"}'
```

### Python辅助工具

```bash
python3 {baseDir}/scripts/fabric.py GET /v2/user/me

python3 {baseDir}/scripts/fabric.py POST /v2/notepads --json '{"name":"Test note","text":"Hello","parentId":"@alias::inbox"}'
```

**说明**：
- 两种辅助工具在操作成功时都会打印响应内容。
- 在遇到HTTP错误（4xx/5xx）时，它们会将错误代码和原因输出到标准错误流（stderr），同时仍然会打印响应内容，然后以非零状态退出（类似于`curl --fail-with-body`）。
- 如果您提供了绝对URL（如`https://...`），除非明确指定了`--with-key`选项，否则辅助工具不会自动添加`X-Api-Key`。

## 核心工作流程

### 1) 创建笔记本（笔记）

端点：`POST /v2/notepads`

**规则**：
- 将用户的“title”映射到`name`字段。
- 使用`text`字段存储Markdown内容。
- 必须包含`parentId`字段。
- 如果在调试过程中遇到400错误，请先仅提供必需的字段，然后再添加`name`和`tags`字段。

**最小化请求示例**：

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/notepads --json '{"parentId":"@alias::inbox","text":"Hello"}'
```

**带有名称的创建请求示例**：

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/notepads --json '{"name":"Calendar Test Note","text":"Created via OpenClaw","parentId":"@alias::inbox"}'
```

**带有标签的创建请求示例（格式正确）**：

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/notepads --json '{"name":"Ideas","text":"# Ideas\\n\\n- First\\n- Second\\n","parentId":"@alias::inbox","tags":[{"name":"ideas"},{"name":"draft"}]}'
```

如果仍然遇到标签验证错误，请暂时省略`tags`字段，先创建笔记本。

### 2) 创建文件夹

端点：`POST /v2/folders`

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/folders --json '{"name":"My new folder","parentId":"@alias::inbox","description":null}'
```

### 3) 创建书签

端点：`POST /v2/bookmarks`

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/bookmarks --json '{"url":"https://example.com","parentId":"@alias::inbox","name":"Example","tags":[{"name":"reading"}]}'
```

### 4) 浏览资源（列出文件夹的子资源）

端点：`POST /v2/resources/filter`

**重要提示**：
- 该端点的`parentId`参数需要一个UUID（而不是别名）。
- 如果您只有别名，可以通过列出资源根目录并选择`inbox/bin`文件夹的ID来获取正确的`parentId`。

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/resources/filter --json '{"parentId":"PARENT_UUID_HERE","limit":50,"order":{"property":"modifiedAt","direction":"DESC"}}'
```

### 5) 搜索

端点：`POST /v2/search`

当用户提供模糊描述时（例如“关于……的笔记”），可以使用此端点进行搜索。

```bash
node {baseDir}/scripts/fabric.mjs POST /v2/search --json '{"queries":[{"mode":"text","text":"meeting notes","filters":{"kinds":["notepad"]}}],"pagination":{"page":1,"pageSize":20},"sort":{"field":"modifiedAt","order":"desc"}}'
```

## 错误处理与重试策略（实用指南）

- **400 Bad Request**：表示请求格式不正确。请重新检查必需的字段，并确保`tags`参数的格式为`[{name}|{id}]`，且没有嵌套结构。
- **401/403**：表示身份验证、订阅或权限问题。请停止尝试并报告错误详情，避免盲目重试。
- **404**：表示端点错误、ID错误或没有访问权限。
- **429**：表示达到请求速率限制。请稍后重试（使用延迟和随机时间间隔）。对于创建操作，请避免盲目重试，否则可能会创建重复项。
- **5xx**：表示临时性错误。请稍后重试。

## 参考文件

- OpenAPI规范（官方文档）：`{baseDir}/fabric-api.yaml`
- 额外规范说明：`{baseDir}/references/REFERENCE.md`
- 故障排除指南：`{baseDir}/references/TROUBLESHOOTING.md`
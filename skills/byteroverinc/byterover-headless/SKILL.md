---
name: byterover-headless
description: "使用 ByteRover CLI 查询和整理知识库。使用 `brv query` 进行知识检索，使用 `brv curate` 添加上下文信息，使用 `brv push/pull` 进行同步操作。"
metadata: {"moltbot":{"emoji":"🧠","requires":{"bins":["brv"]},"install":[{"id":"npm","kind":"node","package":"@byterover/cli","bins":["brv"],"label":"Install ByteRover CLI (npm)"}]}}
---

# ByteRover 知识管理

使用 `brv` 命令行工具（CLI）来管理您的知识库。ByteRover 会维护一个上下文树，其中存储了项目的模式、决策和实现细节。

**重要提示**：在无头/自动化模式下使用时，务必添加 `--headless --format json` 标志，以获取机器可解析的 JSON 输出。

## 设置（无头模式）

- ByteRover 可以完全设置为无头模式。如果用户未登录或当前工作目录中未初始化 `.brv/` 文件（可通过 `brv status --headless --format json` 命令检查 `projectInitialized` 和 `authStatus` 字段），请用户提供以下信息：
  1. **API 密钥** - 用于身份验证（从 https://app.byterover.dev/settings/keys 获取）
  2. **团队名称和空间名称** - 用于项目初始化

### 使用 API 密钥登录

使用 API 密钥进行身份验证：

```bash
brv login --api-key <key>
```

成功登录后，输出文本为：`已登录为 <email>`。

### 初始化项目

为项目初始化 ByteRover（无头模式需要团队名称和空间名称，可以使用 ID 或名称）：

```bash
# Using names
brv init --headless --team my-team --space my-space --format json

# Using IDs
brv init --headless --team team-abc123 --space space-xyz789 --format json
```

强制重新初始化：
```bash
brv init --headless --team my-team --space my-space --force --format json
```

示例响应：
```json
{
  "success": true,
  "command": "init",
  "data": {
    "status": "success",
    "teamName": "MyTeam",
    "spaceName": "MySpace",
    "configPath": "/path/to/project/.brv/config.json"
  }
}
```

**注意**：您可以使用团队名称或空间名称，系统不区分大小写。

### 检查状态

检查 ByteRover 和项目的当前状态：

```bash
brv status --headless --format json
```

示例响应：
```json
{
  "success": true,
  "command": "status",
  "data": {
    "cliVersion": "1.0.0",
    "authStatus": "logged_in",
    "userEmail": "user@example.com",
    "projectInitialized": true,
    "teamName": "MyTeam",
    "spaceName": "MySpace",
    "mcpStatus": "connected",
    "contextTreeStatus": "has_changes"
  }
}
```

## 查询知识

提问以检索相关知识：

```bash
brv query "How is authentication implemented?" --headless --format json
```

示例响应：
```json
{
  "success": true,
  "command": "query",
  "data": {
    "status": "completed",
    "result": "Authentication uses JWT tokens...",
    "toolCalls": [{"tool": "search_knowledge", "status": "success", "summary": "5 matches"}]
  }
}
```

## 编辑内容

向项目的上下文树中添加新知识或内容：

```bash
brv curate "Auth uses JWT with 24h expiry. Tokens stored in httpOnly cookies via authMiddleware.ts" --headless --format json
```

可以包含特定文件以提供更全面的上下文（最多 5 个文件）：
```bash
brv curate "Authentication middleware validates JWT tokens" --files src/middleware/auth.ts --headless --format json
```

示例响应：
```json
{
  "success": true,
  "command": "curate",
  "data": {
    "status": "queued",
    "taskId": "abc123",
    "message": "Context queued for processing"
  }
}
```

## 推送上下文树

将本地上下文树的更改推送到 ByteRover 云存储：

```bash
brv push --headless --format json -y
```

`-y` 标志会跳过确认提示（无头模式必需）。

将更改推送到特定分支：
```bash
brv push --branch feature-branch --headless --format json -y
```

示例响应：
```json
{
  "success": true,
  "command": "push",
  "data": {
    "status": "success",
    "added": 3,
    "edited": 1,
    "deleted": 0,
    "branch": "main",
    "url": "https://app.byterover.com/team/space"
  }
}
```

可能的返回状态：
- `success` - 推送成功
- `no_changes` - 无需要推送的上下文更改
- `cancelled` - 推送被取消
- `error` - 推送失败

## 拉取上下文树

从 ByteRover 云存储中拉取上下文树：

```bash
brv pull --headless --format json
```

从特定分支拉取内容：
```bash
brv pull --branch feature-branch --headless --format json
```

示例响应：
```json
{
  "success": true,
  "command": "pull",
  "data": {
    "status": "success",
    "added": 5,
    "edited": 2,
    "deleted": 1,
    "branch": "main",
    "commitSha": "abc123def"
  }
}
```

可能的返回状态：
- `success` - 拉取成功
- `local_changes` - 本地存在更改，需要先推送本地更改
- `error` - 拉取失败

## 错误处理

始终检查 JSON 响应中的 `success` 字段：
- `success: true` - 操作成功完成
- `success: false` - 操作失败，请查看 `data.error` 或 `data.message` 以获取详细信息

常见错误情况：
- **未授权**：运行 `brv login --api-key <key>`
- **项目未初始化**：运行 `brv init --headless --team <team> --space <space> --format json`
- **本地存在更改**：在拉取之前先推送本地更改

## 提示
1. 在执行拉取和推送操作之前，应先获取用户权限。
2. 在自动化操作中始终使用 `--headless --format json` 标志（`brv login` 除外，因为它输出文本）。
3. 先运行 `brv status --headless --format json` 以验证身份验证和项目状态。
4. 在编辑内容时，使用 `--files` 参数包含相关文件以提供更好的上下文。
5. 查询响应可能包含工具调用详情，显示搜索到的知识内容。
6. 在推送操作中，无头模式下务必使用 `-y` 标志跳过确认步骤。重新初始化时使用 `-f` 标志强制重新初始化。
7. 如果本地有未推送的更改，拉取操作会失败——请先推送本地更改。
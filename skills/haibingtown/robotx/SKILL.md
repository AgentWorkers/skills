---
name: robotx
description: 使用 robotx CLI 来部署 RobotX 应用程序、管理其版本以及检查应用程序的状态。
metadata:
  short-description: RobotX deployment CLI skill
---
# RobotX 部署技能

当代理需要使用 `robotx` CLI 在 RobotX 上部署或管理项目版本时，请使用此技能。

## 快速入门

- 检查 CLI 是否可用：`which robotx || which robotx_cli`
- 安装（优先选择二进制版本，无需安装 Go）：
  - `curl -fsSL https://raw.githubusercontent.com/haibingtown/robotx_cli/main/scripts/install.sh | bash`
- 如果您希望安装源代码版本：
  - `go install github.com/haibingtown/robotx_cli/cmd/robotx@latest`
  - 或者自动设置 PATH：`curl -fsSL https://raw.githubusercontent.com/haibingtown/robotx_cli/main/scripts/go-install.sh | bash`

## 配置

通过配置文件（`~/.robotx.yaml`）或环境变量来设置凭据：

- `ROBOTX_BASE_URL`
- `ROBOTX_API_KEY`

## 认证预检查及默认登录

在运行任何 API 命令（`deploy`、`projects`、`versions`、`status`、`logs`、`publish`）之前，请先验证本地认证。

推荐的快速检查方法：

```bash
robotx projects --limit 1 --output json
```

如果您遇到与认证相关的错误（如 `missing_base_url`、`missing_api_key`、`401`、`403`），请先尝试使用 `robotx login`，只有在登录失败时才采取其他措施：

1. 默认方式（交互式，基于浏览器）：运行 `robotx login` 并重试原始命令。
   - `robotx login --base-url https://robotx.xin`
   - CLI 会显示一个验证 URL 和用户代码，然后自动打开浏览器进行授权。
   - 在浏览器中完成登录；CLI 会自动保存凭据到 `~/.robotx.yaml`。
   - 无头/远程模式：添加 `--no-browser` 选项并手动打开显示的 URL。
   - 对于 RobotX 托管的登录授权，请使用 `robotx.xin`（而非 `api.robotx.xin`）。
2. 备用方案（仅在无法登录或登录失败时使用）：通过控制台手动设置 API 密钥并进行本地配置。
   - `export ROBOTX_BASE_URL=https://your-robotx-server.com`
   - `export ROBOTX_API_KEY=your-api-key`
   - 或者将配置写入 `~/.robotx.yaml`：

```yaml
base_url: https://your-robotx-server.com
api_key: your-api-key
```

对于持续集成（CI）或非交互式环境，建议使用环境变量而非 `robotx login`。

## 机器可读的输出

对于代理和工作流，始终使用结构化的输出格式：

- `robotx deploy . --name my-app --output json`
- `robotx projects --limit 50 --output json`
- `robotx versions --project-id proj_123 --output json`
- `robotx status --project-id proj_123 --output json`
- `robotx logs --build-id build_456 --output json`
- `robotx publish --project-id proj_123 --build-id build_456 --output json`

JSON 数据会输出到标准输出（stdout），进度日志会输出到标准错误输出（stderr）。

## 常用命令

### 部署（创建或更新）

```bash
robotx deploy [path] --name "My App" [--publish] [--wait=true]
```

默认情况下，`deploy --name` 命令会执行创建或更新操作，且操作针对同一所有者。

### 版本管理

```bash
robotx versions --project-id proj_123 [--limit 20]
```

`versions` 的别名是 `robotx builds --project-id proj_123`。

### 项目管理

```bash
robotx projects [--limit 50]
```

### 状态查询

```bash
robotx status --project-id proj_123 [--build-id build_456] [--logs]
```

`status` 命令支持 `--project-id` 或 `--build-id` 参数，也可以同时使用两者。如果指定了 `--logs`，则必须指定 `--build-id`。

### 日志查看

```bash
robotx logs --build-id build_456 [--project-id proj_123]
```

### 发布

```bash
robotx publish --project-id proj_123 --build-id build_456
```

## 注意：MCP 功能

`robotx mcp` 目前只是一个占位符，尚未可用于生产环境。请使用 Shell/CLI 模式进行代理集成。
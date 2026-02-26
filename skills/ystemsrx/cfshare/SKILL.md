---
name: cfshare
description: 使用 `cfshare` CLI 将本地端口或文件暴露为临时的 Cloudflare Quick Tunnel URL。当用户需要为本地服务获取一个临时的公共 URL、需要从终端共享文件/目录，或者需要查看/导出 `cfshare` 的审计和策略状态时，可以使用该工具。
metadata: { "cfshare": { "emoji": "☁️", "requires": { "bins": ["cfshare", "cloudflared"] }, "author": "ystemsrx" } }
allowed-tools: Bash(cfshare:*)
---
# CFShare CLI 功能简介

`cfshare` 是一个用于操作 Cloudflare Quick Tunnel 的命令行工具，它能够将隧道配置信息以结构化的 JSON 格式输出。

## 在版本检查失败时进行安装

如果以下任意一个命令执行失败，请先安装缺失的软件包，然后再尝试使用 `cfshare`：

```bash
cfshare --version
cloudflared --version
```

1. 如果 `cfshare --version` 失败，请安装 `cfshare`（需要 Node.js 和 npm）：

```bash
npm install -g @systemsrx/cfshare
```

2. 如果 `cloudflared --version` 失败，请根据操作系统安装 `cloudflared`：

- **macOS**：

```bash
brew install cloudflare/cloudflare/cloudflared
```

- **Debian/Ubuntu**：

```bash
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflare $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt-get update && sudo apt-get install -y cloudflared
```

- **Windows (PowerShell)**：

```powershell
winget install --id Cloudflare.cloudflared
```

- **WSL/Linux**（通用二进制安装）：

```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
sudo chmod +x /usr/local/bin/cloudflared
```

3. 重新运行两次版本检查。如果仍然失败，请停止操作，并将具体的错误信息报告给用户。

## CLI 命令格式

```bash
cfshare <tool> [params-json] [options]
```

**支持的命令**：

- `env_check`  
- `expose_port`  
- `expose_files`  
- `exposure_list`  
- `exposure_get`  
- `exposure_stop`  
- `exposure_logs`  
- `maintenance`  
- `audit_query`  
- `audit_export`  

**全局选项**：

- `--params '<json>'` 或 `--params-file <path>`  
- `--config '<json>'` 或 `--config-file <path>`  
- `--workspace-dir <dir>`（仅用于 `expose_files`）  
- `--keep-alive`（用于保持后台进程运行）  
- `--no-keep-alive`（默认值，执行完成后立即退出）  
- `--compact`  

命令名称支持使用 `_` 或 `-` 作为分隔符（例如：`expose-port` 等同 `expose-port`）。

## 代理工具的标准工作流程：

1. 首先运行 `env_check`。  
2. 使用 `expose_port` 或 `expose_files` 创建代理配置。  
3. 立即将生成的 `public_url` 和 `expires_at` 返回给用户。  
4. 默认情况下，`expose_*` 命令执行完成后会立即退出。  
5. 仅在需要控制后台进程的生命周期时使用 `--keep-alive`；完成后可以通过 `Ctrl+C` 来终止进程。

**自动化建议**：

- 推荐使用 `--params` 或 `--params-file` 代替原始的 JSON 参数传递方式，以减少引用错误。  
- 对于敏感内容，建议使用 `access: "token"` 作为访问权限设置。  
- `access: "none"` 表示内容对所有人可见。

## 工具使用示例：

### 1) `env_check`  

```bash
cfshare env_check
```

**返回内容**：

- `cloudflared.ok/path/version`  
- `defaults`（有效配置及运行时路径）  
- `warnings`（警告信息）

### 2) `expose_port`  

```bash
cfshare expose_port --params '{"port":3000,"opts":{"access":"token","ttl_seconds":3600}}
```

**参数**：

- `port`：端口号（1–65535）  
- `opts.ttl_seconds`：缓存时间（秒）  
- `opts.access`：访问权限（`token`、`basic` 或 `none`）  
- `opts.protect_origin`：默认值为 `access != "none`  

**返回内容**：

- `id`  
- `public_url`（使用 `token` 时会在 URL 后自动添加 `?token=...`）  
- `local_url`  
- `expires_at`  
- `access_info`（敏感信息会被屏蔽）

### 3) `expose_files`  

```bash
cfshare expose_files --params '{"paths":["./dist"],"opts":{"mode":"normal","presentation":"preview","access":"none"}}
```

**参数**：

- `paths`：要复制到临时工作区的文件/目录  
- `opts.mode`：`normal` 或 `zip`（默认为 `normal`）  
- `opts.presentation`：`download`、`preview` 或 `raw`（默认为 `download`）  
- `opts.ttl_seconds`：缓存时间（秒）  
- `opts.access`：访问权限（`token`、`basic` 或 `none`）  

**文件服务行为**：  
- **normal** 模式：文件直接在根 URL 提供。  
- **zip** 模式：所有文件会被打包成 ZIP 文件。  
- **presentation` 参数可自定义显示方式：  
  - `download`：强制浏览器保存文件。  
  - `preview`：以内联方式显示文件（图片、PDF、Markdown、音频/视频、HTML、文本等）。  
  - `raw`：直接提供原始文件内容。  
- 如果文件类型无法预览，系统会自动切换到 `raw` 模式，然后再提供下载链接。  

**返回内容**：  
- `id`  
- `public_url`  
- `expires_at`  
- `mode`  
- `presentation`  
- `manifest`  
- `manifest_mode`  
- `manifest_meta`

### 4) `exposure_list`  

```bash
cfshare exposure_list
```

**返回内容**：列出所有已创建的代理会话的详细信息（包括 `id`、类型、状态、公共 URL、本地 URL 和过期时间）。

### 5) `exposure_get`  

```bash
cfshare exposure_get --params '{"id":"port_xxx","opts":{"probe_public":true}}`
cfshare exposure_get --params '{"filter":{"status":"running"},"fields":["id","status","public_url"}'
```

**参数**：  
- `id` 或 `ids`：代理会话 ID  
- `filter`：用于筛选会话状态（`status`）  

**功能**：可以通过 `opts.probe_public` 探查代理的可达性。

### 6) `exposure_stop`  

```bash
cfshare exposure_stop --params '{"id":"all"}
```

**功能**：停止代理服务并清理临时工作区。**返回值**：`stopped`、`failed` 或 `cleaned`。

### 7) `exposure_logs`  

```bash
cfshare exposure_logs --params '{"id":"files_xxx","opts":{"component":"all","lines":200}}`
```

**参数**：  
- `component`：`tunnel`、`origin` 或 `all`（用于指定日志记录的组件）

### 8) `maintenance`  

```bash
cfshare maintenance --params '{"action":"run_gc"}`
cfshare maintenance --params '{"action":"set_policy","opts":{"policy":{"maxTtlSeconds":7200},"ignore_patterns":["*.pem",".env*"]}'
```

**功能**：  
- `start_guard`：启动代理保护机制。  
- `run_gc`：清理缓存数据。  
- `set_policy`：设置代理策略（需提供 `opts.policy`）。  

### 9) `audit_query`  

```bash
cfshare audit_query --params '{"filters":{"event":"exposure_started","limit":100}}`
```

**参数**：  
- `filters`：查询条件（例如 `event="exposure_started`）  

### 10) `audit_export`  

```bash
cfshare audit_export --params '{"range":{"from_ts":"2026-01-01T00:00:00Z","output_path":"./audit.jsonl"}}
```

## 运行时文件（CLI 模式）

`cfshare` 的默认配置文件位于 `~/.cfshare` 目录下：

- `policy.json`：代理配置文件  
- `policy.ignore`：忽略的文件路径列表  
- `audit.jsonl`：审计日志文件  
- `sessions.json`：会话信息文件  
- `workspaces/`：临时工作区目录  
- `exports/`：输出文件目录  

**CLI 模式的重要限制**：  
- `expose_port` 和 `expose_files` 命令执行完成后会立即退出；使用 `--keep-alive` 可保持后台进程运行。  
- 当前会话的状态信息存储在内存中，多次调用 `cfshare` 无法恢复完整的会话状态。  
- `basic` 模式的访问凭证在输出中被屏蔽，因此通常建议使用 `token` 作为代理链接的认证方式。

**故障排除**：  
- 如果找不到 `cloudflared` 可执行文件，请安装 `cloudflared` 或在配置文件中设置 `--config '{"cloudflaredPath":"..."}`。  
- 如果本地服务无法通过 `127.0.0.1:<port>` 访问，请先启动服务。  
- 如果某些路径被策略阻止，请调整 `policy.ignore` 或使用 `maintenance set_policy`。  
- 如果端口被策略限制，请更新 `policy` 中的 `blockedPorts` 配置。  

**日志记录级别**：  
可以使用 `CFSHARE_LOG_LEVEL=info` 或 `CFSHARE_LOG_LEVEL=debug` 来增加日志输出详细程度。
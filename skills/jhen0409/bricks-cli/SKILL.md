---
name: bricks-cli
description: Manage BRICKS workspace via CLI. Use for device status, screenshots, control, monitoring, group operations, application management, module management, and project initialization and deployment. Triggers on: device management, digital signage control, BRICKS workspace tasks, app/module updates, project setup.
---

# BRICKS CLI

BRICKS工作区API的命令行界面（CLI），用于管理设备、应用程序、模块和媒体资源。

## 安装（如尚未安装）

```bash
# Validate installed
which bricks

# npm
npm i -g @fugood/bricks-cli
# Bun
bun add -g @fugood/bricks-cli
```

## 认证

```bash
# Login with one-time passcode (get from https://control.bricks.tools)
bricks auth login <passcode>

# Check auth status
bricks auth status

# Switch profiles
bricks auth list
bricks auth use <profile>
```

## 设备管理

### 列出设备信息

```bash
# List all devices
bricks device list
bricks device list -j              # JSON output
bricks device list -k "lobby"      # Filter by keyword

# Get device details
bricks device get <device-id>
bricks device get <device-id> -j   # JSON output
```

### 控制设备

```bash
# Refresh device (reload app)
bricks device refresh <device-id>

# Clear device cache
bricks device clear-cache <device-id>

# Send control command
bricks device control <device-id> <type>
bricks device control <device-id> <type> -p '{"key":"value"}'
```

### 截取设备屏幕截图

```bash
# Take and save screenshot
bricks device screenshot <device-id>
bricks device screenshot <device-id> -o /tmp/screen.png

# Fetch existing screenshot (no new capture)
bricks device screenshot <device-id> --no-take
```

### 监控设备状态（需要交互式终端）

```bash
# Monitor all devices (polls every 60s)
bricks device monitor

# Monitor specific group
bricks device monitor -g <group-id>

# Custom interval
bricks device monitor -i 30
```

## 设备组

```bash
# List groups
bricks group list

# Get group details
bricks group get <group-id>

# List devices in group with status
bricks group devices <group-id>

# Dispatch action to all devices in group
bricks group dispatch <group-id> <action>

# Refresh all devices in group
bricks group refresh <group-id>

# Monitor group
bricks group monitor <group-id>
```

## 应用程序管理

```bash
# List apps
bricks app list

# Get app details
bricks app get <app-id>

# Update app
bricks app update <app-id>

# Bind devices to app
bricks app bind <app-id>

# Quick property edit
bricks app short-edit <app-id>

# Pull source files
bricks app project-pull <app-id>

# Initialize local project from app
bricks app project-init <app-id>
bricks app project-init <app-id> -o ./my-app
bricks app project-init <app-id> -y          # Skip prompts, use defaults
bricks app project-init <app-id> --no-git    # Skip git init
```

## 模块管理

```bash
bricks module list
bricks module get <module-id>
bricks module update <module-id>
bricks module short-edit <module-id>
bricks module release <module-id>

# Initialize local project from module
bricks module project-init <module-id>
bricks module project-init <module-id> -o ./my-module -y
```

### 项目初始化选项

`app`和`module`命令都支持以下选项：
- `-o, --output <dir>` — 指定输出目录
- `-y, --yes` — 忽略提示信息，使用默认设置
- `--no-git` — 跳过Git初始化步骤
- `--no-install` — 跳过软件安装过程
- `--no-github-actions` — 跳过GitHub Actions工作流
- `--no-agents` — 跳过AGENTS.md文件的生成
- `--no-claude` — 跳过CLAUEMD文件的生成
- `--gemini` — 包含GEMINI.md文件（默认不包含）

## 媒体流处理

```bash
bricks media boxes              # List media boxes
bricks media box <box-id>       # Box details
bricks media files <box-id>     # Files in box
bricks media file <file-id>     # File details
```

## 配置管理

```bash
bricks config show              # Show current config
bricks config endpoint          # Show API endpoint
bricks config endpoint beta     # Switch to beta endpoint
```

## 交互式模式（需要交互式终端）

```bash
bricks interactive    # or: bricks i
```

## 开发工具（支持局域网发现）

```bash
# Scan LAN for DevTools servers via UDP broadcast
bricks devtools scan
bricks devtools scan -t 5000           # Custom timeout (ms)
bricks devtools scan -j                # JSON output
bricks devtools scan --verify          # Verify each server via HTTP

# Show connection URLs for a device
bricks devtools open <address>
bricks devtools open <address> -p 19853   # Custom port
bricks devtools open <address> --verify   # Verify reachable first
```

设备的“启用局域网发现”功能必须在高级设置中开启（默认为开启状态）。

## MCP服务器

```bash
bricks mcp start      # Start MCP server (STDIO mode)
```

### 将设备的MCP端点桥接到本地CLI

可以使用[mcporter](https://mcporter.dev)将设备的MCP端点作为本地MCP服务器（标准输入/输出接口）使用，以便像Claude Code这样的工具能够连接到该服务器：

```bash
# Bridge a device's MCP endpoint (requires passcode as Bearer token)
npx mcporter --url http://<device-ip>:19851/mcp --header "Authorization: Bearer <passcode>"
```

## 提示：

- 在大多数命令前使用`-j`或`--json`选项可获取JSON格式的输出结果
- 设备ID为UUID格式，可以使用`device list`命令查询设备ID
- 工作区令牌的获取地址：https://control.bricks.tools → 工作区设置 → API令牌
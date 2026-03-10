---
name: homeserver
description: 通过 homebutler CLI 管理家庭实验室服务器：系统状态监控、Docker 部署、WoL（Wake-on-Lan）功能、端口扫描、TUI（图形化用户界面）控制面板、Web 控制面板、警报通知以及多服务器 SSH 连接功能。
metadata:
  {
    "openclaw": {
      "emoji": "🏠",
      "requires": { "anyBins": ["homebutler"] },
      "configPaths": ["homebutler.yaml", "~/.config/homebutler/config.yaml"]
    }
  }
---
# 家庭服务器管理

使用 [`homebutler`](https://github.com/Higangssh/homebutler) 命令行工具来管理家庭实验室中的服务器。该工具为单文件二进制程序，输出格式为 JSON，非常适合人工智能系统使用。

## 先决条件

必须已安装 `homebutler`，并且该工具的路径（PATH）已添加到系统环境变量中。

```bash
# Check if installed
which homebutler

# Option 1: Install via Homebrew (macOS/Linux)
brew install Higangssh/homebutler/homebutler

# Option 2: Install via Go
go install github.com/Higangssh/homebutler@latest

# Option 3: Build from source
git clone https://github.com/Higangssh/homebutler.git
cd homebutler && make build && sudo mv homebutler /usr/local/bin/
```

## 命令

### 设置向导
```bash
homebutler init                      # Interactive config setup
```
根据提示在 `~/.config/homebutler/config.yaml` 文件中创建配置文件。

### 系统状态
```bash
homebutler status                    # Local server
homebutler status --server rpi       # Specific remote server
homebutler status --all              # All servers in parallel
```
返回以下信息：主机名、操作系统、架构、运行时间、CPU 使用率（百分比）、内存（总量/已使用量/百分比）、磁盘（已挂载/总量/已使用量/百分比）。

### Docker 管理
```bash
homebutler docker list               # List all containers
homebutler docker list --server rpi  # List on remote server
homebutler docker list --all         # List on all servers
homebutler docker restart <name>     # Restart a container
homebutler docker stop <name>        # Stop a container
homebutler docker logs <name>        # Last 50 lines of logs
homebutler docker logs <name> 200    # Last 200 lines
```

### 网络唤醒（Wake-on-LAN）
```bash
homebutler wake <mac-address>           # Wake by MAC
homebutler wake <name>                   # Wake by config name
homebutler wake <mac> 192.168.1.255     # Custom broadcast
```
相关配置信息存储在配置文件中的 `wake` 部分。

### 开放端口
```bash
homebutler ports                     # Local
homebutler ports --server rpi        # Remote
homebutler ports --all               # All servers
```
返回以下信息：协议、地址、端口、进程 ID、进程名称。

### 网络扫描
```bash
homebutler network scan
```
通过 Ping 扫描和 ARP 表来发现局域网中的设备。返回信息包括 IP 地址、MAC 地址、主机名和设备状态。
注意：扫描可能需要最多 30 秒。部分设备可能因未响应 Ping 而无法被检测到。

### TUI 仪表盘
```bash
homebutler watch                     # Live terminal dashboard for all servers
```
实时监控所有已配置的服务器状态，支持自动刷新。在终端界面中显示 CPU、内存、磁盘使用情况以及 Docker 容器的信息。

### Web 仪表盘
```bash
homebutler serve                     # Start web dashboard on port 8080
homebutler serve --port 3000         # Custom port
homebutler serve --demo              # Demo mode with fake data (no real system calls)
```
基于浏览器的仪表盘，地址为 `http://localhost:8080`。提供所有服务器、Docker 容器及警报信息的只读视图。

### SSH 主机密钥信任
```bash
homebutler trust <server>            # Trust remote server's SSH host key
homebutler trust <server> --reset    # Remove old key and re-trust
```
采用“首次使用即信任”（TOFU, Trust On First Use）机制。在新服务器上进行首次 SSH 连接前必须设置此选项。

### 升级
```bash
homebutler upgrade                   # Upgrade local + all remote servers
homebutler upgrade --local           # Upgrade only local binary
```
从 GitHub 下载最新版本并安装。对于远程服务器，通过 SSH 进行升级。

### 资源警报
```bash
homebutler alerts                    # Local
homebutler alerts --server rpi       # Remote
homebutler alerts --all              # All servers
```
检查 CPU、内存和磁盘的使用情况是否超过配置中的阈值。返回每种资源的状态（正常/警告/严重）。

### 部署（远程安装）
```bash
homebutler deploy --server rpi                          # Download from GitHub Releases
homebutler deploy --server rpi --local ./homebutler     # Air-gapped: copy local binary
homebutler deploy --all                                 # Deploy to all remote servers
```
通过 SSH 将 `homebutler` 安装到远程服务器上。系统会自动检测远程服务器的操作系统和架构。
安装路径的优先级顺序为：`/usr/local/bin` → `sudo /usr/local/bin` → `~/.local/bin`（系统会自动将路径添加到 `.profile`、`.bashrc` 或 `.zshrc` 文件中）。

### MCP 服务器
```bash
homebutler mcp                       # Start MCP server (JSON-RPC over stdio)
```
启动内置的 MCP（Model Context Protocol）服务器，以便与 Claude Desktop、ChatGPT、Cursor 等 MCP 客户端配合使用。通过标准的 MCP 协议提供所有 `homebutler` 工具的功能（如 `system_status`、`docker_list`、`docker_restart`、`docker_stop`、`docker_logs`、`wake`、`open_ports`、`network_scan`、`alerts`）。该服务器不开放任何网络端口，仅使用标准输入输出（stdio）。

### 版本信息
```bash
homebutler version
```

## 输出格式

所有命令默认以人类可读的文本形式输出。可以使用 `--json` 标志来获取机器可解析的 JSON 格式输出（推荐用于人工智能或脚本集成）。

## 配置文件

配置文件的查找顺序如下：
1. `--config <路径>` — 显式指定配置文件路径
2. `$HOMEBUTLER_CONFIG` — 环境变量
3. `~/.config/homebutler/config.yaml` — XDG 标准配置文件（推荐）
4. `./homebutler.yaml` — 当前目录下的配置文件

如果未找到配置文件，系统会使用默认设置。

### 配置选项
- `servers` — 包含 SSH 连接详情的服务器列表
- `wake` — 包含 WOL（Wake-on-LAN）目标的配置信息（包括 MAC 地址和广播地址）
- `alerts.cpu/memory/disk` — 资源使用阈值的百分比
- `output` — 默认的输出格式

### 多服务器配置示例
```yaml
servers:
  - name: main-server
    host: 192.168.1.10
    local: true

  - name: rpi
    host: 192.168.1.20
    user: pi
    auth: key                # "key" (default, recommended) or "password"
    key: ~/.ssh/id_ed25519   # optional, auto-detects

  - name: vps
    host: example.com
    user: deploy
    port: 2222
    auth: key
    key: ~/.ssh/id_ed25519
```

## 使用指南

1. **始终执行命令，不要猜测结果** — 使用 `homebutler status` 命令获取实际数据。
2. **以用户可理解的方式解释结果** — 不要直接输出原始 JSON 数据，而是用自然语言进行总结。
3. **在出现警报时提醒用户** — 如果有任何资源处于“警告”或“严重”状态，请特别指出。
4. **使用 `--all` 获取整体信息** — 当用户询问所有服务器或所有信息时，使用 `--all` 命令。
5. **使用 `--server` 获取特定服务器的信息** — 当用户指定了服务器名称时，使用 `--server <服务器名称>` 命令。
6. **处理 Docker 相关问题** — 如果未安装 Docker 或 Docker 守护进程未运行，请向用户说明情况。
7. **网络扫描** — 提醒用户扫描可能需要约 30 秒。
8. **安全性** — 在群组聊天中切勿直接显示包含主机名/IP 地址的原始 JSON 数据，应进行汇总。
9. **远程部署** — 在隔离网络环境中建议使用 `--local` 选项。

## 安全注意事项

- **SSH 认证**：始终优先使用基于密钥的认证方式，切勿在配置文件中存储明文密码。
- **网络扫描**：仅在本地网络中执行扫描操作，并在扫描前提醒用户。
- **远程部署**：仅将 `homebutler` 部署到用户自己拥有的服务器上。在远程安装前请先获得用户确认。
- **配置文件权限**：确保配置文件仅对文件所有者可读（使用 `chmod 600` 设置权限）。
- **数据传输**：`homebutler` 不会向外部发送任何数据，所有操作均在本地或用户指定的服务器上进行。

## 错误处理

- **SSH 连接失败** → 检查配置文件中的主机名/端口/用户名信息，并确认远程服务器已正确配置 SSH 密钥。
- **远程服务器上未找到 `homebutler` ** → 先执行 `homebutler deploy --server <服务器名称>` 命令。
- **Docker 未安装** → 告知用户该服务器上没有安装 Docker。
- **Docker 守护进程未运行** → 建议用户使用 `sudo systemctl start docker` 启动 Docker 守护进程。
- **网络扫描超时** — 在大型子网中属于正常现象，建议用户重试。
- **权限问题** — 在某些系统中，执行端口或 Docker 相关命令可能需要 `sudo` 权限。

## 示例交互

用户：**服务器运行状况如何？**
→ 执行 `homebutler status`，并获取如下总结：“CPU 使用率 23%，内存使用率 40%，磁盘使用率 37%。运行时间 42 天。一切正常 👍”

用户：**检查所有服务器的状态**
→ 执行 `homebutler status --all`，并获取所有服务器的详细状态。

用户：**Raspberry Pi 的运行状况如何？**
→ 执行 `homebutler status --server rpi`，并获取 Raspberry Pi 的状态。

用户：**正在运行哪些 Docker 容器？**
→ 执行 `homebutler docker list`，列出所有 Docker 容器的名称和状态。

用户：**唤醒 NAS 服务器**
→ 执行 `homebutler wake nas`（如果已配置），或询问 NAS 的 MAC 地址。

用户：**所有服务器是否有警报？**
→ 执行 `homebutler alerts --all`，并报告所有警报信息。

用户：**将 `homebutler` 部署到新服务器上**
→ 执行 `homebutler deploy --server <服务器名称>`，并获取部署结果。
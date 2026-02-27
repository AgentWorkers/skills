---
name: homeserver
description: 通过 homebutler CLI 进行家庭实验室服务器管理。可以查看系统状态（CPU/内存/磁盘）、管理 Docker 容器、实现基于局域网的远程唤醒（Wake-on-LAN）、扫描开放的端口、发现网络设备、监控资源警报，并通过 SSH 远程管理多台服务器。当需要查询服务器状态、Docker 容器信息、远程唤醒设备、检查开放端口、网络设备状态或进行多服务器管理时，均可使用该工具。
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

使用 `homebutler` CLI 管理家庭实验室服务器。该工具采用单一二进制文件形式进行运行，输出结果为 JSON 格式，非常适合人工智能系统使用。

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

# Option 4: Shell installer (review script before running)
curl -fsSL https://raw.githubusercontent.com/Higangssh/homebutler/main/install.sh -o install.sh
less install.sh  # review first
sh install.sh
```

## 命令

### 系统状态
```bash
homebutler status                    # Local server
homebutler status --server rpi       # Specific remote server
homebutler status --all              # All servers in parallel
```
输出内容：主机名、操作系统、架构、运行时间、CPU 使用率（百分比）、内存（总量/已使用量/百分比）、磁盘（已挂载/总量/已使用量/百分比）

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
相关配置信息存储在 `config` 文件的 `wake` 目录下。

### 开放端口
```bash
homebutler ports                     # Local
homebutler ports --server rpi        # Remote
homebutler ports --all               # All servers
```
输出内容：协议类型、地址、端口号、进程 ID（PID）、进程名称

### 网络扫描
```bash
homebutler network scan
```
通过 Ping 技术和 ARP 表扫描本地局域网中的设备。输出内容：IP 地址、MAC 地址、主机名、设备状态。
注意：扫描可能需要最多 30 秒时间。部分设备可能因未响应 Ping 而无法被检测到。

### 资源警报
```bash
homebutler alerts                    # Local
homebutler alerts --server rpi       # Remote
homebutler alerts --all              # All servers
```
检查 CPU、内存和磁盘的使用情况是否超过配置中的阈值。输出每个资源的状态（正常/警告/严重）。

### 部署（远程安装）
```bash
homebutler deploy --server rpi                          # Download from GitHub Releases
homebutler deploy --server rpi --local ./homebutler     # Air-gapped: copy local binary
homebutler deploy --all                                 # Deploy to all remote servers
```
通过 SSH 将 `homebutler` 安装到远程服务器上。系统会自动检测远程服务器的操作系统和架构。
安装路径的优先级顺序为：`/usr/local/bin` → `sudo /usr/local/bin` → `~/.local/bin`（系统会自动将安装路径添加到 `.profile`、`.bashrc` 或 `.zshrc` 文件中的 PATH 变量中）。

### 主要进程
```bash
homebutler processes                 # Local top 10 by CPU
homebutler processes --server rpi    # Remote server
homebutler processes --all           # All servers
```
输出内容：进程 ID（PID）、CPU 使用率（百分比）、内存使用率（百分比）、进程名称

### Web 仪表盘
```bash
homebutler serve                     # Start on localhost:8080
homebutler serve --port 9090         # Custom port
homebutler serve --demo              # Demo mode with dummy data
```
启动一个实时服务器监控的 Web 仪表盘，包含以下页面：服务器概览、系统状态、Docker 信息、进程列表、警报信息、开放端口列表以及网络唤醒功能。通过下拉菜单可以选择要查看的具体服务器的数据。

### 交互式设置
```bash
homebutler init                      # Setup wizard
```
系统会自动检测本地计算机，并指导用户完成远程服务器的添加过程，包括 SSH 密钥的发现和连接测试。

### SSH 信任设置
```bash
homebutler trust --server rpi        # Trust a remote server's host key (TOFU)
```

### MCP 服务器
```bash
homebutler mcp                       # Start MCP server (JSON-RPC over stdio)
```
启动一个内置的 MCP（Model Context Protocol）服务器，以便与 Claude Desktop、ChatGPT、Cursor 等 MCP 客户端配合使用。所有 `homebutler` 命令（如 `system_status`、`docker_list`、`docker_restart`、`docker_stop`、`docker_logs`、`wake`、`open_ports`、`network_scan`、`alerts`）均通过标准 MCP 协议提供。该服务器不开放任何网络端口，仅使用标准输入输出（stdio）进行通信。

### 版本信息
```bash
homebutler version
homebutler -v
homebutler --version
```

## 输出格式

所有命令默认输出人类可读的文本。若需要机器可解析的 JSON 格式输出，可使用 `--json` 标志（推荐用于人工智能或脚本集成）。

## 配置文件

配置文件会按以下顺序自动查找：
1. `--config <路径>` — 显式指定配置文件路径
2. `$HOMEBUTLER_CONFIG` — 环境变量
3. `~/.config/homebutler/config.yaml` — XDG 标准配置文件（推荐）
4. `./homebutler.yaml` — 当前目录下的配置文件

如果未找到配置文件，系统会使用默认设置。

### 配置选项
- `servers` — 包含 SSH 连接详细信息的服务器列表
- `wake` — 包含设备名称、MAC 地址及广播唤醒功能的配置项
- `alerts.cpu/memory/disk` — 资源使用率的阈值百分比

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

1. **始终执行命令，不要猜测** — 使用 `homebutler status` 命令获取实时数据。
2. **以用户可理解的方式解释结果** — 不要直接输出原始 JSON 数据，而是用自然语言进行总结。
3. **在出现警报时提醒用户** — 如果有任何资源处于“警告”或“严重”状态，请立即通知用户。
4. **使用 `--all` 命令获取整体信息** — 当用户询问所有服务器的状态时，使用 `--all`。
5. **使用 `--server` 命令查询特定服务器** — 当用户指定了服务器名称时，使用 `--server <服务器名称>`。
6. **处理 Docker 相关问题** — 如果系统未安装 Docker 或 Docker 守护进程未运行，请向用户说明情况。
7. **关于网络扫描** — 提醒用户扫描可能需要约 30 秒时间。
8. **安全注意事项** — 绝不要在群组聊天中直接发送包含主机名/IP 地址的原始 JSON 数据，应进行汇总处理。
9. **远程部署** — 在隔离网络环境中建议使用 `--local` 选项。

## 安全提示

- **SSH 认证**：优先使用基于密钥的认证方式，切勿在配置文件中存储明文密码。
- **网络扫描**：仅在本机局域网内进行扫描，并在扫描前提醒用户。
- **远程部署**：仅将 `homebutler` 部署到用户自己拥有的服务器上。在远程安装前请先获得用户确认。
- **配置文件权限**：确保配置文件仅对文件所有者可读（使用 `chmod 600` 设置权限）。
- **数据传输**：`homebutler` 不会向外部发送任何数据，所有操作仅在本地或用户指定的服务器上进行。

## 错误处理

- **SSH 连接失败** — 检查配置文件中的主机地址/端口号/用户名信息，确认远程服务器已正确配置 SSH 密钥。
- **远程服务器上未找到 `homebutler`** — 先运行 `homebutler deploy --server <服务器名称>` 命令。
- **Docker 未安装** — 告知用户该服务器上没有安装 Docker。
- **Docker 守护进程未运行** — 建议用户使用 `sudo systemctl start docker` 启动 Docker。
- **网络扫描超时** — 在大型子网中属于正常现象，建议用户重试。
- **权限问题** — 在某些系统中，执行端口或 Docker 相关命令可能需要 `sudo` 权限。

## 示例交互场景

用户：**服务器运行状况如何？**
→ 运行 `homebutler status`，输出示例：`CPU 使用率 23%，内存使用率 40%，磁盘使用率 37%，运行时间 42 天。一切正常 👍`

用户：**检查所有服务器的状态？**
→ 运行 `homebutler status --all`，显示所有服务器的运行状态。

用户：**Raspberry Pi 的情况如何？**
→ 运行 `homebutler status --server rpi`，获取 Raspberry Pi 的状态信息。

用户：**当前有哪些 Docker 容器正在运行？**
→ 运行 `homebutler docker list`，列出所有运行的 Docker 容器及其状态。

用户：**唤醒 NAS 服务器？**
→ 运行 `homebutler wake nas`（如果已配置），或请求 NAS 的 MAC 地址。

用户：**所有服务器是否有警报？**
→ 运行 `homebutler alerts --all`，显示所有服务器的警报信息。

用户：**将 `homebutler` 部署到新服务器上？**
→ 运行 `homebutler deploy --server <服务器名称>`，并显示部署结果。
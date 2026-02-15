---
name: linux-patcher
description: 自动化Linux服务器补丁管理和Docker容器更新功能。适用于用户需要更新、修补或升级Linux服务器、应用安全补丁、更新Docker容器、检查系统更新或管理多台主机维护的场景。支持Ubuntu、Debian、RHEL、AlmaLinux、Rocky Linux、CentOS、Amazon Linux和SUSE等操作系统。该工具集成了PatchMon模块，可实现自动主机检测和智能化的Docker容器管理功能。
---

# Linux 服务器补丁管理工具

该工具可通过 SSH 自动化地管理多台 Linux 服务器的补丁安装以及 Docker 容器的更新。

## ⚠️ 重要免责声明

### 分布版支持情况

**已全面测试的版本：**
- ✅ **Ubuntu** - 在真实环境中进行了端到端的测试

**支持但未测试的版本：**
- ⚠️ **Debian GNU/Linux** - 基于官方文档编写了相应的命令
- ⚠️ **Amazon Linux** - 支持 AL2 (yum) 和 AL2023 (dnf) 版本
- ⚠️ **RHEL (Red Hat Enterprise Linux)** - 支持 RHEL 7 (yum) 和 8+ (dnf) 版本
- ⚠️ **AlmaLinux** - 与 RHEL 兼容，使用 dnf 作为包管理器
- ⚠️ **Rocky Linux** - 与 RHEL 兼容，使用 dnf 作为包管理器
- ⚠️ **CentOS** - 支持 CentOS 7 (yum) 和 8+ (dnf) 版本
- ⚠️ **SUSE/OpenSUSE** - 使用 zypper 作为包管理器

**测试建议：**
请在非生产环境中先对未测试的版本进行测试。脚本在运行于未测试的版本时会发出警告。

### 安全注意事项

使用本工具需要满足以下条件：
- **无密码的 sudo 访问权限** - 通过配置限制了 sudo 的使用权限
- **SSH 密钥认证** - 不会存储或传输任何密码
- **PatchMon 的认证信息** - 安全地存储在用户的 home 目录中

请阅读 `SETUP.md` 以获取完整的安全配置指南。

## 快速入门

### 自动化操作（推荐）

**通过 PatchMon 自动检测并更新所有主机：**
```bash
scripts/patch-auto.sh
```

**仅更新软件包（不更新 Docker）：**
```bash
scripts/patch-auto.sh --skip-docker
```

**预览更新内容（模拟执行）：**
```bash
scripts/patch-auto.sh --dry-run
```

### 手动操作（备用方案）

**单台主机 - 仅更新软件包：**
```bash
scripts/patch-host-only.sh user@hostname
```

**单台主机 - 全面更新：**
```bash
scripts/patch-host-full.sh user@hostname /path/to/docker/compose
```

**根据配置文件更新多台主机：**
```bash
scripts/patch-multiple.sh config-file.conf
```

## 主要功能

- **与 PatchMon 集成** - 自动检测需要更新的主机
- **智能检测 Docker** - 自动识别 Docker 和 Docker Compose 的路径
- **选择性更新** - 可使用 `--skip-docker` 标志跳过 Docker 的更新
- **需要无密码的 sudo 访问权限** - 通过 `visudo` 或 `/etc/sudoers.d/` 文件进行配置
- **SSH 密钥认证** - 不需要输入密码
- **并行执行** - 同时更新多台主机
- **模拟执行模式** - 先预览更新内容，再实际应用
- **手动覆盖设置** - 可在特定主机上手动执行更新，无需依赖 PatchMon

## 配置方法

### 方案 1：通过 PatchMon 自动化（推荐）

配置 PatchMon 的认证信息以自动检测主机：
```bash
cp scripts/patchmon-credentials.example.conf ~/.patchmon-credentials.conf
nano ~/.patchmon-credentials.conf
```

设置你的认证信息：
```bash
PATCHMON_URL=https://patchmon.example.com
PATCHMON_USERNAME=your-username
PATCHMON_PASSWORD=your-password
```

然后只需运行以下命令：
```bash
scripts/patch-auto.sh
```

脚本将：
1. 从 PatchMon 获取需要更新的主机列表
2. 自动检测每台主机上的 Docker 环境
3. 根据情况执行相应的更新（仅更新主机或进行全面更新）

### 方案 2：单台主机（快速手动操作）

直接使用命令行参数运行脚本（无需配置文件）

### 方案 3：多台主机（手动配置）

根据 `scripts/patch-hosts-config.example.sh` 创建配置文件：
```bash
cp scripts/patch-hosts-config.example.sh my-servers.conf
nano my-servers.conf
```

配置文件示例：
```bash
# Host definitions: hostname,ssh_user,docker_path
HOSTS=(
  "webserver.example.com,ubuntu,/opt/docker"
  "database.example.com,root,/home/admin/compose"
  "monitor.example.com,docker,/srv/monitoring"
)

# Update mode: "host-only" or "full"
UPDATE_MODE="full"

# Dry run mode (set to "false" to apply changes)
DRY_RUN="true"
```

然后运行脚本：
```bash
scripts/patch-multiple.sh my-servers.conf
```

## 先决条件

### 控制主机（运行 OpenClaw 的主机）上的要求：

- [ ] 安装并运行了 OpenClaw
- [ ] 安装了 SSH 客户端（可执行 `ssh` 命令）
- [ ] 使用 Bash 4.0 或更高版本
- [ ] 安装了 curl（用于访问 PatchMon 的 API）
- [ ] 安装了 jq（用于解析 JSON 数据）
- [ ] 安装了 PatchMon（用于检测需要更新的主机）
  - 无需安装在 OpenClaw 主机上
  - 可以安装在任何可通过 HTTPS 访问的服务器上
  - 下载地址：https://github.com/PatchMon/PatchMon

**安装缺失的工具：**
```bash
# Ubuntu/Debian
sudo apt install curl jq

# RHEL/CentOS/Rocky/Alma
sudo dnf install curl jq

# macOS
brew install curl jq
```

### 目标主机上的要求：

- [ ] SSH 服务器正在运行且可访问
- [ ] 配置了 SSH 密钥认证（支持无密码登录）
- [ ] 为补丁命令配置了无密码的 sudo 访问权限（详见 SETUP.md）
- [ ] 安装了 Docker（可选，仅用于全面更新）
- [ ] 安装了 Docker Compose（可选，仅用于全面更新）
- [ ] 安装了 PatchMon 代理（可选，但推荐）

### PatchMon 的安装（自动模式必备）

**注意：** PatchMon 不需要安装在与 OpenClaw 同一的服务器上。只需在网络中的任意服务器上安装 PatchMon，OpenClaw 会通过 API 与其通信。

**下载 PatchMon：**
- **GitHub：** https://github.com/PatchMon/PatchMon
- **文档：** https://docs.patchmon.net

**所需配置：**
- [ ] 在任意可访问的服务器上安装 PatchMon 服务器
- [ ] 在所有需要更新的主机上安装 PatchMon 代理
- [ ] 提供 PatchMon 的认证信息（用户名/密码）
- [ ] 确保 OpenClaw 服务器能与 PatchMon 服务器之间建立 HTTPS 连接

**系统架构：**
```
┌─────────────────┐      HTTPS API      ┌─────────────────┐
│ OpenClaw Host   │ ──────────────────> │ PatchMon Server │
│ (this machine)  │    Query updates    │ (separate host) │
└─────────────────┘                     └─────────────────┘
                                                  │
                                                  │ Reports
                                                  ▼
                                         ┌─────────────────┐
                                         │ Target Hosts    │
                                         │ (with agents)   │
                                         └─────────────────┘
```

**快速入门步骤：**
1. 在单独的服务器上安装 PatchMon 服务器（详见 GitHub 仓库的文档）
2. 在所有需要更新的主机上安装 PatchMon 代理
3. 配置 OpenClaw 以访问 PatchMon 的 API：
```bash
cp scripts/patchmon-credentials.example.conf ~/.patchmon-credentials.conf
nano ~/.patchmon-credentials.conf  # Set PatchMon server URL
chmod 600 ~/.patchmon-credentials.conf
```

**详细安装指南：**
请参阅 `references/patchmon-setup.md`。

**不安装 PatchMon 也可以使用该工具吗？**
可以！你可以选择手动模式来针对特定主机进行更新，但自动检测主机更新功能依赖于 PatchMon。

### 在目标主机上的操作

**必备条件：**
- SSH 服务器正在运行
- SSH 用户具有无密码的 sudo 权限（用于执行 `apt` 和 `docker` 命令）
- 安装了 PatchMon 代理（用于自动更新模式）

**进行全面更新时：**
- 需要安装 Docker 和 Docker Compose

### 配置无密码的 sudo 访问权限

在每台目标主机上创建 `/etc/sudoers.d/patches` 文件：
```bash
# For Ubuntu/Debian systems
username ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/docker

# For RHEL/CentOS systems
username ALL=(ALL) NOPASSWD: /usr/bin/yum, /usr/bin/docker, /usr/bin/dnf
```

将 `username` 替换为你的 SSH 用户名。使用 `sudo -l` 命令验证配置是否正确。

## 更新模式

### 仅更新主机软件包

- 运行 `apt update && apt upgrade`（或在 RHEL 上运行 `yum update`）
- 删除不再使用的软件包（`apt autoremove`）
- **不会** 更新 Docker 容器

**适用场景：**
- 未安装 Docker 的主机
- 仅需要更新系统软件包

### 全面更新

- 更新系统软件包
- 清理 Docker 缓存（`docker system prune`）
- 下载最新的 Docker 镜像
- 重新创建容器

**适用场景：**
- 使用 Docker 的基础设施
- 在维护窗口期间进行更新

## 工作流程

### 自动化工作流程（使用 patch-auto.sh）

1. **查询 PatchMon** - 通过 API 获取需要更新的主机列表
2. **针对每台主机：**
   - 连接到主机
   - 检查是否安装了 Docker
   - 自动检测 Docker Compose 的路径（如果未指定）
   - 根据检测结果执行仅更新主机软件包或全面更新的操作

### 仅更新主机软件包的流程

1. 连接到目标主机
2. 运行 `sudo apt update`
3. 运行 `sudo apt -y upgrade`
4. 运行 `sudo apt -y autoremove`
5. 显示更新结果

### 全面更新的流程

1. 连接到目标主机
2. 运行 `sudo apt update && upgrade && autoremove`
3. 进入 Docker Compose 目录
4. 运行 `sudo docker system prune -af`（清理缓存）
5. 下载并重新创建所有容器
6. 运行 `sudo docker compose pull`
7. 运行 `sudo docker compose up -d`（重新创建容器）

### Docker 路径的自动检测逻辑

当未指定 Docker 的路径时，脚本会搜索以下位置：
- `/home/$USER/Docker/docker-compose.yml`
- `/opt/docker/docker-compose.yml`
- `/srv/docker/docker-compose.yml`
- `$HOME/Docker/docker-compose.yml`
- 当前目录

**自定义自动检测设置：**
```bash
scripts/patch-host-full.sh user@host /custom/path
```

## 示例

### 示例 1：通过 PatchMon 自动更新（推荐方案）
```bash
# First time: configure credentials
cp scripts/patchmon-credentials.example.conf ~/.patchmon-credentials.conf
nano ~/.patchmon-credentials.conf

# Run automatic updates
scripts/patch-auto.sh
```

### 示例 2：模拟执行更新过程**
```bash
# Preview what would be updated
scripts/patch-auto.sh --dry-run

# Review output, then apply
scripts/patch-auto.sh
```

### 示例 3：跳过 Docker 更新**
```bash
# Update packages only, even if Docker is detected
scripts/patch-auto.sh --skip-docker
```

### 示例 4：手动更新单台主机（仅更新软件包）
```bash
scripts/patch-host-only.sh admin@webserver.example.com
```

### 示例 5：手动更新单台主机（包括 Docker 容器）
```bash
scripts/patch-host-full.sh docker@app.example.com /home/docker/production
```

### 示例 6：根据配置文件更新多台主机**
```bash
scripts/patch-multiple.sh production-servers.conf
```

### 示例 7：通过 OpenClaw 进行操作

只需向 OpenClaw 发送指令：
- “更新我的服务器”
- “更新所有需要更新的主机”
- “仅更新软件包，跳过 Docker”

OpenClaw 会自动执行更新并显示结果。

## 故障排除

### PatchMon 集成相关问题

#### “找不到 PatchMon 的认证信息”
- 创建认证文件：`cp scripts/patchmon-credentials.example.conf ~/.patchmon-credentials.conf`
- 根据实际情况修改文件中的 URL 和认证信息
- 或者将 `PATCHMON_CONFIG` 环境变量设置为其他路径

#### “无法与 PatchMon 进行认证”
- 确认 PatchMon 的 URL 是否正确（路径末尾不应包含斜杠）
- 检查用户名和密码是否正确
- 确保可以访问 PatchMon 服务器：`curl -k https://patchmon.example.com/api/health`
- 检查防火墙设置

#### “显示需要更新，但实际上不需要更新”
- 确认目标主机上的 PatchMon 代理是否正在运行：`systemctl status patchmon-agent`
- 检查代理的更新间隔设置：`/etc/patchmon/config.yml`
- 强制更新代理：`patchmon-agent report`

### 系统更新相关问题

#### 执行 `apt` 或 `docker` 命令时出现权限问题
- 配置无密码的 sudo 访问权限（详见先决条件）
- 使用 `ssh user@host sudo apt update` 进行测试

#### 连接失败
- 检查 SSH 连接是否正常：`ssh user@host echo OK`
- 确保 SSH 密钥配置正确
- 检查主机名解析是否正常

#### 无法找到 Docker Compose 文件
- 指定完整的路径：`scripts/patch-host-full.sh user@host /full/path`
- 或者在目标主机上安装 Docker Compose
- 自动检测时会搜索以下路径：`/home/user/Docker`, `/opt/docker`, `/srv/docker`

#### 更新后容器无法启动
- 查看日志：`ssh user@host "docker logs container-name"`
- 手动检查容器状态：`ssh user@host "cd /docker/path && docker compose logs"`
- 如需回滚：`ssh user@host "cd /docker/path && docker compose down && docker compose up -d`

## PatchMon 的集成（可选）

有关监控和定时更新的功能，请参阅 `references/patchmon-setup.md`。

PatchMon 提供以下功能：
- 提供 Web 界面显示更新状态
- 跟踪每台主机的更新情况
- 强调安全更新内容
- 记录更新历史

## 安全注意事项

- **自动化操作需要无密码的 sudo 访问权限**
  - 仅限于执行 `apt` 和 `docker` 命令
  - 使用 `/etc/sudoers.d/` 文件来管理权限
- **保护 SSH 密钥**：建议使用带密码保护的密钥
  - 限制密钥的权限：`chmod 600 ~/.ssh/id_rsa`
- **在正式环境中应用更新前请仔细检查**  
  - 先使用模拟执行模式
  - 在测试环境中进行测试
- **在维护窗口期间安排更新**  
  - 使用 OpenClaw 的 cron 作业来自动化更新
- 与团队协调以确定 Docker 更新的时间

## 最佳实践

- **先进行测试**：在实际应用更新前先运行模拟执行模式
- **分批更新**：避免同时更新所有主机（以防系统崩溃）
- **检查日志**：更新后查看是否有错误
- **备份配置文件**：将 Docker Compose 文件放入版本控制系统中
- **合理安排更新时间**：选择流量较低的时间进行更新
- **记录配置信息**：妥善保存配置文件
- **必要时重启服务器**：某些内核更新需要重启服务器（此步骤不是自动执行的）

## 重启管理

脚本不会自动重启主机。更新完成后，请检查是否需要重启：
1. 运行 `ssh user@host "[ -f /var/run/reboot-required ] && echo YES || echo NO"`
2. 在维护窗口期间安排手动重启
- 使用 PatchMon 的界面来查看是否需要重启

## 与 OpenClaw 的集成

### 定时执行更新

创建 cron 作业以实现自动化的 nightly 更新：
```bash
cron add --name "Nightly Server Patching" \
  --schedule "0 2 * * *" \
  --task "cd ~/.openclaw/workspace/skills/linux-patcher && scripts/patch-auto.sh"
```

或者仅更新软件包：
```bash
cron add --name "Nightly Package Updates" \
  --schedule "0 2 * * *" \
  --task "cd ~/.openclaw/workspace/skills/linux-patcher && scripts/patch-auto.sh --skip-docker"
```

### 通过聊天命令执行更新

只需向 OpenClaw 发送以下命令：
- **全面更新（包括 Docker 容器）：**
  - “更新我的服务器” → 默认会包含 Docker 的更新
- “更新所有需要更新的主机”
- “仅更新软件包，跳过 Docker”

- **仅更新软件包（排除 Docker）：**
  - “更新我的服务器，排除 Docker”
- “仅更新软件包，跳过 Docker”

- **查询更新状态：**
  - “哪些主机需要更新？”
- “显示需要更新的主机列表”

**自动执行流程：**

- 当你输入 “更新我的服务器” 时：
  - 通过 API 查询需要更新的主机
  - 检测每台主机上的 Docker 环境
  - 更新系统软件包
  - 下载并重新创建 Docker 容器（如果检测到 Docker）

- 当你输入 “更新我的服务器，排除 Docker” 时：
  - 仅更新系统软件包
  - 跳过所有与 Docker 相关的操作
  - 显示更新结果

**注意：** 默认情况下会包含 Docker 的更新。如果需要排除 Docker 的更新，请使用相应的命令。

### 手动覆盖设置（针对特定主机）

可以直接指定需要更新的主机：
- “更新 webserver.example.com”
- “仅更新 database.example.com 的软件包”
- “更新 app.example.com，包括 Docker”

OpenClaw 会使用相应的手动脚本来执行更新。

## 文档资料

该工具附带详细的文档：
- **SKILL.md**：概述和使用指南
- **SETUP.md**：完整的配置指南及安全最佳实践
- **WORKFLOWS.md**：所有操作模式的可视化工作流程图
- **references/patchmon-setup.md**：PatchMon 的安装和集成指南

**首次使用？** 请先阅读 `SETUP.md`，其中包含安全的配置步骤。

**想了解整个流程吗？** 查看 `WORKFLOWS.md`，其中包含操作流程的可视化图解。

## 支持的 Linux 发行版

| 发行版 | 包管理器 | 是否已测试 | 支持情况 |
|--------------|-----------------|--------|--------|
| Ubuntu | apt | ✅ 是 | 完全支持 |
| Debian | apt | ⚠️ 否 | 支持（未测试） |
| Amazon Linux 2 | yum | ⚠️ 否 | 支持（未测试） |
| Amazon Linux 2023 | dnf | ⚠️ 否 | 支持（未测试） |
| RHEL 7 | yum | ⚠️ 否 | 支持（未测试） |
| RHEL 8+ | dnf | ⚠️ 否 | 支持（未测试） |
| AlmaLinux | dnf | ⚠️ 否 | 支持（未测试） |
| Rocky Linux | dnf | ⚠️ 否 | 支持（未测试） |
| CentOS 7 | yum | ⚠️ 否 | 支持（未测试） |
| CentOS 8+ | dnf | ⚠️ 否 | 支持（未测试） |
| SUSE/OpenSUSE | zypper | ⚠️ 否 | 支持（未测试） |

该工具会自动识别操作系统版本并选择相应的包管理器。
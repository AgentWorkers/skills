---
name: sys-updater
description: Production-safe Ubuntu maintenance orchestrator: runs daily apt security updates, tracks non-security updates across apt/npm/pnpm/brew with quarantine + auto-review, applies only approved updates, rotates logs/state, and generates clear 09:00 MSK Telegram reports (including what was actually installed).
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "os": ["linux"],
        "requires": { "bins": ["apt-get", "npm", "brew", "clawhub"] },
      },
  }
---

# 系统更新工具（sys-updater）

这是一个专为 Ubuntu 主机设计的全面系统维护自动化工具，支持使用 apt、npm、brew 和 OpenClaw 进行系统更新。

## 工具功能

`sys-updater` 是一个专为运行 OpenClaw 的 Linux 主机设计的维护工具。它将**安全补丁安装**与**功能升级**分开处理，同时会生成可审计的状态文件，并每天发送一份便于阅读的报告。

### 核心功能

- **APT（Ubuntu）**
  - 每日执行 `apt-get update`
  - 通过 `unattended-upgrade` 自动安装安全补丁
  - 仅从预先规划好的列表中安装非安全更新
- **NPM / PNPM / Brew**
  - 检测过时的软件包
  - 记录这些软件包的更新状态
  - 自动评估软件包的风险（如漏洞、回归问题等）
  - 仅安装经过批准的更新
- **OpenClaw 功能（通过 ClawHub 管理）**
  - 检查已安装的 OpenClaw 插件并报告更新状态
- **每日报告（莫斯科标准时间 09:00）**
  - 显示系统的当前运行状态
  - 显示待安装、已计划或被阻止的更新列表
  - 显示每个软件包的实际安装情况（针对 apt、npm、pnpm、brew）

## 工作流程

### 每日流程（莫斯科标准时间 06:00）
```
run_6am:
├── apt: update, security upgrades, simulate, track non-security
├── npm/brew: check outdated, add to tracking
└── skills: auto-update immediately (no quarantine)
```

### 日报生成（莫斯科标准时间 09:00）
- 所有软件包管理器的更新总结
- 下一天的计划更新列表
- 被阻止的更新及其原因

### T+2 天后（审核）
- 在网上搜索被跟踪软件包中的漏洞或回归问题
- 根据搜索结果将软件包标记为“待安装”或“被阻止”

### T+3 天后（升级）
- 执行计划中的 npm 或 brew 更新
- 发送更新完成报告

## 状态文件
- `state/apt/last_run.json` — 上次更新的结果
- `state/apt/tracked.json` — 被跟踪的 APT 软件包
- `state/apt/npm_tracked.json` — 被跟踪的 npm 软件包
- `state/apt/brew_tracked.json` — 被跟踪的 brew 软件包
- `state/logs/apt_maint.log` — 每日日志（保留 10 天）

## 手动命令
```bash
# Daily maintenance (runs automatically)
./scripts/apt_maint.py run_6am

# Generate report
./scripts/apt_maint.py report_9am

# Check npm/brew only
./scripts/pkg_maint.py check

# Review packages (after 2 days)
./scripts/pkg_maint.py review

# Apply planned upgrades
./scripts/pkg_maint.py upgrade

# Update skills only
./scripts/pkg_maint.py skills
```

## 配置

环境变量：
- `SYS_UPDATER_BASE_DIR` — 工具的基础目录（默认：`~/clawd/sys-updater`
- `SYS_UPDATER_STATE_DIR` — 状态文件的位置
- `SYS_UPDATER_LOG_DIR` — 日志文件的位置

## Cron 作业
需要配置 4 个 Cron 作业：
1. `run_6am` — 每日 06:00（执行更新操作、检查 npm/brew 以及 OpenClaw 插件的状态）
2. `report_9am` — 每日 09:00（生成每日报告并发送到 Telegram）
3. `review_2d` — T+2 天后（在网上搜索漏洞）
4. `upgrade_3d` — T+3 天后（执行计划中的更新）

## 保守的设计原则
- **安全更新**：通过 `unattended-upgrade` 自动完成
- **非安全更新**：在安装前会有 2 天的观察期以检查是否存在问题
- **用户控制**：可以基于具体原因阻止任何软件包的安装
- **安全性保障**：在任何 APT 更新前都会进行模拟测试

## 系统要求
- 安装了 apt 的 Ubuntu 系统
- 安装了 Node.js 和 npm（用于管理 npm 软件包）
- 安装了 Homebrew（用于管理 brew 软件包）
- 安装了 OpenClaw 及其 ClawHub 命令行工具
- 运行用户需要具有 sudo 权限以执行特定的 APT 命令

## sudo 权限配置
为了实现无人值守的更新操作，只需为运行用户授予执行特定 APT 命令的免密码 sudo 权限。**请勿将用户添加到全局 sudo 用户组中**。

创建文件 `/etc/sudoers.d/sys-updater`：
```bash
# Allow sys-updater to run apt maintenance commands without password
# Replace 'username' with your actual username
username ALL=(root) NOPASSWD: /usr/bin/apt-get update
username ALL=(root) NOPASSWD: /usr/bin/apt-get -s upgrade
username ALL=(root) NOPASSWD: /usr/bin/unattended-upgrade -d
```

设置安全权限：
```bash
sudo chmod 440 /etc/sudoers.d/sys-updater
sudo visudo -c  # Verify syntax is valid
```

### 常用命令说明

| 命令 | 功能 |
|---------|---------|
| `apt-get update` | 更新软件包列表 |
| `apt-get -s upgrade` | 模拟升级操作（不进行实际安装） |
| `unattended-upgrade -d` | 自动安装安全补丁 |

### 安全注意事项
- 仅允许使用上述 3 个命令
- 严禁使用 `apt-get upgrade`（除非加上 `-s` 选项，否则仅用于模拟）
- 禁止使用 `apt-get dist-upgrade` 或 `autoremove` 命令
- 严禁通过 sudo 安装或删除软件包
- npm 和 brew 的安装/卸载操作不需要 sudo 权限（由用户自行完成）
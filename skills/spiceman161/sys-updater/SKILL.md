---
name: sys-updater
description: Ubuntu（使用apt包管理器）、npm、brew以及OpenClaw的相关系统包维护技能。采用保守的工作流程：非安全更新需经过2天的隔离期；安全更新会自动进行；同时会定期通过网络搜索来评估是否存在漏洞。
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

# 系统更新器 (sys-updater)

这是一个为 Ubuntu 主机设计的全面系统维护自动化工具，支持 apt、npm、brew 和 OpenClaw 等包管理工具。

## 主要功能

- **APT (Ubuntu)**：每日检查更新，自动应用安全更新；非安全软件包会有 2 天的隔离期。
- **NPM**：全局包跟踪，并在升级前通过网络搜索检查是否存在漏洞。
- **Brew**：采用与 npm 相同的保守处理流程进行包跟踪。
- **OpenClaw 程序**：可以立即自动更新，无需隔离期。
- **定时报告**：每天上午 09:00 通过 Telegram 发送更新报告。
- **漏洞检查**：在应用更新前通过网络自动搜索软件包中的问题。

## 工作流程

### 每日 (06:00 MSK)
```
run_6am:
├── apt: update, security upgrades, simulate, track non-security
├── npm/brew: check outdated, add to tracking
└── skills: auto-update immediately (no quarantine)
```

### 报告 (09:00 MSK)
- 所有包管理器的更新总结。
- 下一天的计划更新列表。
- 被阻止的软件包及其原因。

### T+2 天 (审核)
- 对被跟踪的软件包进行网络搜索，检查是否存在漏洞或回归问题。
- 根据搜索结果将软件包标记为“计划更新”或“被阻止”。

### T+3 天 (升级)
- 应用计划中的 npm/brew 更新。
- 发送更新完成报告。

## 状态文件

- `state/apt/last_run.json` — 上次运行结果。
- `state/apt/tracked.json` — 被跟踪的 APT 软件包。
- `state/apt/npm_tracked.json` — 被跟踪的 NPM 软件包。
- `state/apt/brew_tracked.json` — 被跟踪的 Brew 软件包。
- `state/logs/apt_maint.log` — 每日日志（保留 10 天）。

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
- `SYS_UPDATER_BASE_DIR` — 基本目录（默认：~/clawd/sys-updater）
- `SYS_UPDATER_STATE_DIR` — 状态文件存放位置。
- `SYS_UPDATER_LOG_DIR` — 日志文件存放位置。

## Cron 作业

需要配置 4 个 Cron 作业：
1. `run_6am` — 每天 06:00 MSK：更新 APT 包、检查 npm/brew 包以及自动更新 OpenClaw 程序。
2. `report_9am` — 每天 09:00 MSK：发送更新报告。
3. `review_2d` — T+2 天后 09:00 MSK：搜索软件包中的漏洞。
4. `upgrade_3d` — T+3 天后 06:00 MSK：应用计划中的更新。

## 保守的设计原则

- **安全更新**：通过 `unattended-upgrade` 自动应用。
- **非安全更新**：会有 2 天的观察期，期间会检查是否存在漏洞。
- **用户控制**：可以基于具体原因阻止任何软件包的更新。
- **安全性**：在应用任何 APT 更新前会进行模拟测试。

## 系统要求

- 安装了 apt 的 Ubuntu 系统。
- 安装了 Node.js 和 npm（用于管理 NPM 包）。
- 安装了 Homebrew（用于管理 Brew 包）。
- 安装了 OpenClaw 及其 ClawHub 命令行工具。
- 运行用户需要具有 sudo 权限（仅用于执行特定的 APT 命令）。

## sudo 用户组配置

为了实现无人值守操作，仅允许运行用户在执行特定 APT 命令时无需输入密码即可使用 sudo。**请勿将用户添加到完整的 sudo 用户组中。**

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

### 需要执行的命令说明

| 命令 | 用途 |
|---------|---------|
| `apt-get update` | 刷新软件包列表。 |
| `apt-get -s upgrade` | 模拟升级（仅用于测试，不会实际进行任何更改）。 |
| `unattended-upgrade -d` | 自动应用安全更新。 |

## 安全注意事项

- 仅允许使用上述 3 个特定命令。
- 不允许使用 `apt-get upgrade`（除非加上 `-s` 选项，否则仅用于测试）。
- 不允许使用 `apt-get dist-upgrade` 或 `autoremove` 命令。
- 通过 sudo 不允许安装或删除任何软件包。
- NPM 和 Brew 的安装/卸载操作不需要 sudo 权限。
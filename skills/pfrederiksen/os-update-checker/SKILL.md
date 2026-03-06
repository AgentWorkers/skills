---
name: os-update-checker
description: "**检查操作系统软件包的更新情况**，并提供每个软件包的更新日志摘要及风险等级分类。支持以下包管理器：`apt`（Debian/Ubuntu）、`dnf`（Fedora/RHEL）、`yum`（CentOS 7）、`pacman`（Arch）、`zypper`（openSUSE）、`apk`（Alpine）以及`brew`（macOS）。  
**适用场景**：  
- 检查系统更新状态；  
- 在批准软件包升级之前进行验证；  
- 通过系统心跳或定时任务（如cron）定期监控操作系统健康状况。  
**功能说明**：  
- 仅提供更新信息，不执行任何安装或修改操作。"
---
# 操作系统更新检查器

这是一个只读的、跨平台的包更新检查工具。它能自动检测可用的包管理器，列出可升级的包，获取更新日志，并对更新的风险等级（安全、中等、低）进行分类。该工具旨在提供足够的信息，以便用户能够自信地决定是否进行升级。

## 支持的包管理器

| 操作系统 | 包管理器 |
|---|---|
| Debian / Ubuntu / Mint | `apt` |
| Fedora / RHEL 8+ / Rocky / Alma | `dnf` |
| CentOS 7 / RHEL 7 | `yum` |
| Arch / Manjaro / EndeavourOS | `pacman` / `checkupdates` |
| openSUSE Leap / Tumbleweed / SLES | `zypper` |
| Alpine Linux | `apk` |
| macOS / Linux (Homebrew) | `brew` |

## 使用方法

```bash
# Human-readable summary with changelogs (auto-detects OS)
python3 scripts/check_updates.py

# JSON output (for dashboards, cron, integrations)
python3 scripts/check_updates.py --format json

# Skip changelogs for a quick count
python3 scripts/check_updates.py --no-changelog
```

## 风险等级分类

- 🔴 **安全** — 源代码库中包含安全问题
- 🟡 **中等** — 关键性包（如内核、openssh、openssl、sudo、curl、bash等）
- 🟢 **低** — 标准维护更新

## 工作原理

1. 从系统路径（PATH）中检测可用的包管理器（`apt` → `dnf` → `yum` → `pacman` → `zypper` → `apk` → `brew`）
2. 使用相应的只读命令列出可升级的包
3. 在进一步使用之前，会验证每个包的名称是否符合每个包管理器的允许列表（allowlist）规则
4. 获取每个包的最新更新日志（`apt`：`apt changelog`；`dnf/yum`：`rpm --changelog`；其他包管理器：包信息）
5. 以文本或JSON格式报告结果

## 安全设计

- 仅使用 `subprocess`，并设置 `shell=False` — 参数以列表形式传递，绝不会被插入到shell字符串中
- 在使用命令之前，会验证包名称是否符合每个包管理器的允许列表规则
- 所有异常都会被特定类型捕获，避免使用通用的 `except` 语句
- 仅执行只读操作，不进行安装、写入文件或重启服务

## 系统访问权限

- **可执行的命令（仅限读取）：** `apt list`, `apt changelog`, `dnf check-update`, `rpm -q --changelog`, `yum check-update`, `pacman -Qu`, `pacman -Si`, `zypper list-updates`, `zypper info`, `apk list`, `apk info`, `brew outdated`, `brew info`
- **网络连接：** 向发行版的更新日志服务器发送HTTPS请求（`apt` 使用该功能；其他包管理器使用本地包元数据）
- **不进行任何文件写入**

## 系统要求

- Python 3.10 或更高版本
- 系统路径（PATH）中至少有一个支持的包管理器可用
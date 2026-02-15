---
name: claw-backup
version: 1.0.15
description: 通过 `rclone` 将 OpenClaw 的自定义设置（内存配置、技能配置、工作区设置）备份到云存储，并支持定时备份和数据保留功能。该方案适用于 macOS、Linux 和 Windows 系统（支持 Git Bash 或 WSL 环境）。
---

# Claw Backup  
版本：1.0.15  

**OpenClaw 备份工具** — 可定时将您的 OpenClaw 数据（内存、配置、技能、工作区）备份到 `rclone` 目录（例如 Google Drive）。支持 macOS、Linux 和 Windows 系统（通过 Git Bash 或 WSL 运行）。  

## 功能概述：  
- 备份以下内容：  
  - OpenClaw 的内存数据  
  - `~/.openclaw` 目录（包含配置文件、技能设置、模块、工作区信息以及 cron 任务配置）  
  - `clawd/scripts` 目录  
  - `Dev/CursorApps/clawd` 目录（但不包括 `node_modules` 文件夹）  
- 支持定时备份功能（可在 macOS 的 LaunchAgent、Linux 的 cron 或 Windows 的任务调度程序中设置）  
- 实现本地和远程备份策略，自动删除旧备份文件  
- 支持 `rclone`（云存储）或仅本地存储的备份模式  

## 安装前注意事项：  
1. **切勿** 在未仔细阅读脚本内容的情况下直接运行 `curl ... | node`（或其他命令）。建议先使用 `git clone` 下载源代码，然后打开 `setup.js` 和 `install-launchagent.sh`（或对应的 cron/任务调度脚本）文件，了解其具体功能。  
2. **检查 `setup.js` 代码及调度脚本**：确认所有备份路径均正确无误，且没有异常的网络请求或命令。如果您不熟悉脚本编写，建议不要直接安装。  
3. **验证代码来源**：官方代码仓库为 [github.com/vidarbrekke/ClawBackup](https://github.com/vidarbrekke/ClawBackup)。本文档中的版本信息（包括 “版本号”）与代码仓库中的版本信息一致；实际仓库可能显示不同的版本号。  
4. **对敏感数据进行加密处理**：建议使用加密方式将备份文件传输到云端（例如使用 `rclone crypt`），或在本地存储前对备份文件进行加密。  
5. **安装完成后**：请检查系统中的 LaunchAgent、crontab 或任务调度程序配置，并先在本地进行测试备份，确保备份功能正常。  

## 恢复说明：  
每个备份文件包中都包含 `RESTORE_NOTES.txt` 文件，其中列出了正确的恢复路径：  
- `openclaw_config/skills` → `~/.openclaw/skills`  
- `cursorapps_clawd/skills` → `~/Dev/CursorApps/clawd/skills`（或您指定的路径）  

## 快速安装步骤：  
1. **先决条件**：需要安装 Node.js，并确保 `rclone` 已配置为可访问 Google Drive；同时需要具备 Bash（或在 Windows 上使用 Git Bash）。  
   - 仅当备份模式为 `rclone` 时才需要安装 `rclone`。  
2. **推荐的安装方式（请先阅读相关说明）**：  
   ```bash
   git clone https://github.com/vidarbrekke/ClawBackup.git
   cd ClawBackup
   node setup.js
   ```  
3. **快速安装方式（不推荐）**：仅适用于已熟悉脚本内容的情况。**切勿** 在未仔细阅读说明的情况下直接安装：  
   ```bash
   curl -fsSL https://raw.githubusercontent.com/vidarbrekke/ClawBackup/main/setup.js | node
   ```  
4. 按照提示操作（或使用 `node setup.js --defaults` 以使用默认配置路径）。完成后运行测试命令，并按照提示安装任务调度程序。  

## 安全提示：  
- 备份文件可能包含敏感信息（如 OpenClaw 的配置数据、内存内容及技能设置）。  
- 安装过程中可能会自动添加定时备份任务；安装完成后请检查相关配置。  
- 在云存储模式下，凭据信息来自您的 `rclone` 配置文件；该仓库不要求额外设置环境变量。  
- 建议使用加密方式存储备份文件（例如 `rclone crypt`），或在本地存储前对文件进行加密。  
- 备份文件包含 `.sha256` 校验文件，用于验证文件完整性。  

## 代码仓库与贡献方式：  
- 代码及完整文档请访问 [github.com/vidarbrekke/ClawBackup](https://github.com/vidarbrekke/ClawBackup)。  
- 欢迎任何 OpenClaw 用户对项目提出改进建议或提交 Pull Request。  

## 许可证：  
MIT 许可证
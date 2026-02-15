---
name: clawdbot-skill-update
description: 具备动态工作区检测功能的全面备份、更新和恢复工作流程
homepage: https://github.com/pasogott/clawdbot-skill-update
metadata: {"clawdbot":{"emoji":"💾","requires":{"bins":["bash","jq","tar","git"]},"tags":["backup","restore","update","multi-agent"]}}
---

# Clawdbot 更新技能

该技能提供了针对 Clawdbot 安装的全面备份、更新和恢复工作流程。

## 仓库信息

- **GitHub**: https://github.com/clawdbot/clawdbot  
- **上游仓库**: `origin/main`  
- **本地克隆路径**: `~/code/clawdbot`（默认值）

## 功能描述

该技能为 Clawdbot 提供了一个完整的、模块化的更新流程，并具备 **动态工作区检测** 功能：
- 配置文件  
- 代理状态和会话信息  
- 凭据及认证令牌  
- 所有代理的工作区（自动从配置文件中检测）  
- Cron 作业和沙箱环境  
- Git 仓库状态  

### 主要特性  

✅ **动态工作区检测**：从配置文件中读取工作区路径  
✅ **多代理支持**：自动处理多个代理  
✅ **安全回滚**：具备完整的恢复功能  
✅ **Git 集成**：跟踪版本和远程仓库  
✅ **验证机制**：包含更新前后的验证步骤  
✅ **预备份预览**：在备份前提供预览功能  

## 相关文件  

- `config.json`：技能配置文件（包含仓库地址和路径信息）  
- `backup-clawdbot-dryrun.sh`：预备份预览脚本（不会修改任何文件）  
- `backup-clawdbot-full.sh`：完整备份脚本  
- `restore-clawdbot.sh`：恢复脚本  
- `validate-setup.sh`：更新前后的验证脚本  
- `check-upstream.sh`：检查是否有可用更新  
- `UPDATE_CHECKLIST.md`：详细的更新步骤清单  
- `QUICK_REFERENCE.md`：快速命令参考  
- `SKILL.md`：当前文档  
- `README.md`：快速入门指南  

### 动态特性  

备份和恢复脚本现在具备以下功能：  
- 从 `~/.clawdbot/clawdbot.json` 文件中读取工作区路径  
- 支持任意数量的代理  
- 能够优雅地处理缺失的工作区  
- 根据代理 ID 生成安全的文件名  

## 使用场景  

在以下情况下触发该技能：  
- “更新 Clawdbot”  
- “升级到最新版本”  
- “在更新前备份 Clawdbot”  
- “从备份中恢复 Clawdbot”  
- “回滚 Clawdbot 的更新”  

## 使用方法  

### 1. 预备份预览（Dry Run）  

执行 `backup-clawdbot-dryrun.sh` 脚本，会显示：  
- 将要备份的文件列表  
- 预计的备份大小  
- 工作区检测结果  
- 磁盘空间使用情况  
- 会被跳过的文件  

**注意：** 此过程不会创建或修改任何文件！  

### 2. 创建完整备份  

执行 `backup-clawdbot-full.sh` 脚本，会备份以下内容：  
- `~/.clawdbot/clawdbot.json`（配置文件）  
- `~/.clawdbot/sessions/`（会话状态）  
- `~/.clawdbot/agents/`（代理状态）  
- `~/.clawdbot/credentials/`（认证令牌）  
- `~/.clawdbot/cron/`（Cron 作业）  
- `~/.clawdbot/sandboxes/`（沙箱状态）  
- 所有代理的工作区（自动检测）  
- Git 提交记录和状态  

**备份结果保存路径**：`~/.clawdbot-backups/pre-update-YYYYMMDD-HHMMSS/`  

### 3. 更新 Clawdbot  

按照以下步骤操作：  
1. 创建备份  
2. 停止代理服务  
3. 下载最新代码  
4. 根据需要修改配置文件  
5. 运行检查脚本（`doctor`）  
6. 测试系统功能  
7. 以守护进程模式重新启动代理服务  

### 4. 从备份中恢复 Clawdbot  

执行 `restore-clawdbot.sh` 脚本，会恢复以下内容：  
- 所有配置文件  
- 所有状态数据  
- 所有工作区数据  
- 可选：恢复 Git 版本信息  

## 重要说明  

### 多代理环境设置  

该技能适用于具有以下特点的多代理环境：  
- 多个代理，每个代理拥有独立的工作区  
- 沙箱配置  
- 支持通过 WhatsApp、Telegram、Discord、Slack 等平台进行通信  

### v2026.1.8 的重要变更  

**紧急注意事项：**  
- **私信策略**：私信功能默认设置为“配对”模式（而非开放模式）  
- **群组设置**：`telegram.groups` 和 `whatsapp.groups` 被添加到允许列表中  
- **沙箱权限**：默认权限范围从“默认”改为“代理”  
- **时间戳**：现在使用 UTC 格式记录  

### 备份验证  

备份完成后，请务必验证备份文件是否包含以下内容：  
- `clawdbot.json`  
- `credentials.tar.gz`  
- `workspace-*.tar.gz`（每个代理对应一个备份文件）  

### 配置文件修改示例  

- **将 WhatsApp 的私信策略改为“配对”模式**：  
  修改 `config.json` 中的相关配置  

- **设置沙箱的权限范围**：  
  在 `config.json` 中明确指定沙箱的权限范围  

## 工作流程  

### 标准更新流程  

### 回滚流程  

### 更新后的测试  

- **功能测试**：  
  - 确保私信功能正常工作  
  - 确保群组提及消息能够被正确处理  
  - 确保输入提示功能正常显示  
  - 确保代理路由功能正常  
  - 确保沙箱隔离机制有效  
  - 确保工具使用限制得到执行  

### 新功能  

### 监控机制  

### 故障排除  

- **代理服务无法启动**：请检查相关配置和日志  
- **认证错误**：检查认证相关设置  
- **沙箱问题**：检查沙箱环境的配置和日志  

### 紧急恢复措施  

如果遇到问题，可以按照文档中的紧急恢复步骤进行操作。  

## 安装方法  

- **通过 ClawdHub 安装**：[详细步骤](...)  
- **手动安装**：[详细步骤](...)  

## 许可证  

该技能采用 MIT 许可协议，更多信息请参阅 [LICENSE](LICENSE)。  

## 开发者  

**Pascal Schott** ([@pasogott](https://github.com/pasogott))  

如果您对 Clawdbot 有贡献，请访问 [https://github.com/clawdbot/clawdbot](...) 进行提交。
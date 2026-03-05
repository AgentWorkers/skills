---
name: git-sync-daemon
description: 使用守护进程模型（定期执行添加、提交、拉取、推送操作）来管理多个 Git 仓库。当您需要在 macOS（使用 launchd）或 Linux（使用 systemd）上设置、运行或排查自动 Git 同步问题时，可以使用此技能，包括仓库的注册以及服务的生命周期管理。
---
# Git同步守护进程（Git Sync Daemon）

## 目的

提供一个可重用的、基于守护进程的Git自动同步工作流程：
- 一个仓库列表文件
- 一个守护进程
- 每个仓库都有独立的锁定机制和故障隔离机制
- 支持在macOS和Linux系统上进行服务管理

## 相关文件

- 守护进程脚本：`scripts/git_sync_daemon.sh`
- 控制脚本：`scripts/git_sync_ctl.sh`

## 默认运行路径

- 状态目录：`~/.config/git-sync-daemon`
- 仓库列表文件：`~/.config/git-sync-daemon/repos.conf`
- 日志文件：`~/.config/git-sync-daemon/git-sync-daemon.log`

## 仓库信息格式

每个仓库的信息占用一行：

```text
/absolute/path/to/repo|remote=origin|branch=main|enabled=1
```

支持的配置项：
- `remote`（默认值为`origin`）
- `branch`（默认值为当前分支）
- `enabled`（取值范围：`1/0` 或 `true/false`，默认值为`enabled`）

## 快速启动（macOS）

```bash
bash scripts/git_sync_ctl.sh init
bash scripts/git_sync_ctl.sh add-repo /Users/samwei12/Develop/config
bash scripts/git_sync_ctl.sh run-once
bash scripts/git_sync_ctl.sh install-launchd
bash scripts/git_sync_ctl.sh status
```

## 快速启动（Linux）

```bash
bash scripts/git_sync_ctl.sh init
bash scripts/git_sync_ctl.sh add-repo /path/to/repo
bash scripts/git_sync_ctl.sh run-once
sudo bash scripts/git_sync_ctl.sh install-systemd
bash scripts/git_sync_ctl.sh status
```

## 常用操作

- 添加仓库：`bash scripts/git_sync_ctl.sh add-repo <路径> [分支] [远程仓库地址]`
- 删除仓库：`bash scripts/git_sync_ctl.sh remove-repo <路径>`
- 列出所有仓库：`bash scripts/git_sync_ctl.sh list-repos`
- 即时执行一次同步：`bash scripts/git_sync_ctl.sh run-once`
- 查看状态/日志：`bash scripts/git_sync_ctl.sh status`

## 服务管理

- 在macOS上安装守护进程：`bash scripts/git_sync_ctl.sh install-launchd`
- 在macOS上卸载守护进程：`bash scripts/git_sync_ctl.sh uninstall-launchd`
- 在Linux上安装守护进程：`sudo bash scripts/git_sync_ctl.sh install-systemd`
- 在Linux上卸载守护进程：`sudo bash scripts/git_sync_ctl.sh uninstall-systemd`

## 生产环境下的安全加固建议

在将守护进程模式应用于生产环境之前，请确保满足以下要求：

1. **SSH认证**：
   - 确保服务用户能够通过SSH以非交互式方式访问所有远程仓库。
   - 预先加载主机密钥（使用`ssh-keyscan`命令，并设置`StrictHostKeyChecking=accept-new`以避免首次运行时出现错误）。
   - 建议在`~/.ssh/config`文件中明确指定密钥的路径（格式：`host/user/port/IdentityFile/IdentitiesOnly`）。

2. **服务身份一致性**：
   - 使用与仓库凭证和`git config`配置文件相同的用户来安装守护进程。
   - 验证该服务用户的`git config --global user.name/user.email`设置是否正确。

3. **仓库管理策略**：
   - 仅注册干净且符合要求的仓库。
   - 每个仓库条目应对应一个唯一的、规范的分支。
   - 对于需要暂时停用的仓库，使用`enabled=0`来禁用该仓库，而不是直接删除其条目。

4. **日志管理**：
   - 将日志保存在专用文件中，并根据需要定期导出到外部存储。
  - 在启用持久化服务之前，先确保`run-once`命令能够正常执行。

## 安全注意事项

- 该守护进程不会强制推送更改到远程仓库。
- 在执行`rebase`操作时产生的冲突会被记录并仅影响受影响的仓库。
- 如果某个仓库需要使用`git-lfs`功能但未安装该工具，系统会跳过该仓库并显示相应的错误信息。
- 在macOS上，`PATH`环境变量会在服务进程和守护进程脚本中都被扩展，以便包含Homebrew安装的程序。
- 推荐的迁移步骤是：首先仅使用基础仓库进行测试；之后再逐步添加更多仓库。
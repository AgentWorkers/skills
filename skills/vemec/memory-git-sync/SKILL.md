---
name: memory-git-sync
description: 该脚本可自动将 OpenClaw 工作区的数据备份到远程 Git 仓库中。它能够排除大型文件（避免这些文件占用过多存储空间），验证 Git 配置的准确性，并在同步过程中智能处理文件冲突（确保数据的一致性）。
metadata:
  openclaw:
    emoji: "📦"
    requires:
      bins:
        - bash
        - git
    compatibility:
      bash: "4.0 or higher"
      git: "2.0 or higher"
    system_requirements:
      - "Write access to repository directory"
      - "Access to remote Git repository (GitHub, GitLab, etc.)"
    configuration_required:
      - "Git user.name configured locally or globally"
      - "Git user.email configured locally or globally"
      - "Remote 'origin' configured in Git"
      - "Git credentials properly stored (credential helper or SSH key)"
    runtime_requirements:
      - "Network connectivity to push/pull from remote"
      - "Read/write access to .git directory and working tree"
    tags:
      - "git"
      - "backup"
      - "sync"
      - "automation"
---

# 内存同步技能

该技能可自动将工作区的内存数据通过Git同步并备份到远程仓库。

## 快速入门

```bash
bash ./scripts/sync.sh [COMMIT_MESSAGE]
```

默认消息：`chore: memory backup YYYY-MM-DD HH:MM`

## 功能介绍

1. **验证** Git仓库、用户配置以及远程访问权限。
2. **检测并排除** 大文件（大于95MB），以防止推送失败。
3. **自动将所有更改添加到暂存区**。
4. **拉取** 最新的远程更改，以避免冲突。
5. **提交** 更改，并添加时间戳或自定义消息。
6. **将更改推送到远程仓库**；如有需要，会自动设置上游分支。

## 先决条件

- 已使用`origin`远程仓库初始化Git仓库。
- 已设置`git config user.name`和`git config user.email`。
- 具备访问远程仓库的网络权限。
- 对仓库目录具有写入权限。

## 执行步骤

| 步骤 | 操作 | 成功输出 | 失败输出 | 退出状态 |
|------|--------|---|---|---|
| 1 | 验证Git仓库 | `[SUCCESS] 找到Git仓库` | `[ERROR] 未位于Git仓库内` | 1 |
| 2 | 检查Git配置 | `[SUCCESS] Git用户配置有效` | `[ERROR] 未配置Git用户名称` | 1 |
| 3 | 检查远程仓库 | `[SUCCESS] 远程仓库'origin'已配置：[URL]'` | `[ERROR] 未配置'origin'远程仓库` | 1 |
| 4 | 设置.gitignore文件 | `[SUCCESS].gitignore文件已准备就绪` | - | - |
| 5 | 扫描大文件 | `[SUCCESS] 未检测到大文件` | `[WARNING] 检测到大文件` | - |
| 6 | 检测更改 | `[SUCCESS] 所有更改已添加到暂存区` | `[INFO] 无未提交的更改` | 0 |
| 7 | 拉取远程更改 | `[SUCCESS] 拉取成功` | `[WARNING] 拉取失败（继续执行）` | - |
| 8 | 检查同步状态 | `[INFO] 本地与远程仓库已同步` | `[WARNING] 分支不一致（自动拉取）` | 1* |
| 9 | 提交更改 | `[SUCCESS] 更改已提交` | `[ERROR] 提交失败` | 1 |
| 10 | 推送更改 | `[SUCCESS] 推送成功` | `[WARNING] 未配置上游分支（尝试设置）` | 1** |
| 完成 | 同步完成 | `[SUCCESS] 同步成功` | - | 0 |

*通过`git pull --no-edit`自动解决冲突。
**通过`git push --set-upstream origin [branch]`自动设置上游分支。**

## 输出格式

所有输出信息均采用结构化格式，便于机器学习模型（LLM）解析：

```
[INFO]    - Informational messages
[SUCCESS] - Actions completed successfully
[WARNING] - Non-fatal issues (script recovers)
[ERROR]   - Fatal errors (requires intervention)
```

## 常见问题及解决方法

| 问题 | 输出 | 解决方案 |
|-------|--------|-----------|
| 未位于Git仓库内 | `[ERROR] 未位于Git仓库内` | 导航至仓库：`cd /path/to/repo` |
| 未配置用户名称 | `[ERROR] 未配置Git用户名称` | `git config user.name "Name"` |
| 未配置用户邮箱 | `[ERROR] 未配置Git用户邮箱` | `git config user.email "email@example.com"` |
| 未配置origin远程仓库 | `[ERROR] 未配置'origin'远程仓库` | `git remote add origin <URL>` |
| 检测到大文件 | `[WARNING] 检测到大文件` | 自动将大文件添加到.gitignore文件中 |
| 拉取时发生冲突 | `[ERROR] 拉取过程中发生冲突` | 手动解决冲突后，重新运行同步脚本 |
| 网络故障 | `[WARNING] 拉取/推送失败` | 检查网络连接，脚本将继续在本地执行 |

## 主要特性

- **自动处理大文件**：忽略大于95MB的文件，防止Git操作失败。
- **冲突解决**：在推送前自动从远程仓库拉取最新数据。
- **自动配置上游分支**：首次推送时自动设置上游分支。
- **预检机制**：通过预检步骤预防常见错误。
- **输出格式兼容LLM**：输出信息结构化，便于机器学习模型解析。

## 安全注意事项

- **不要将凭据提交到仓库**。
- 使用SSH密钥或凭据管理工具（例如`git config credential.helper osxkeychain`）。
- 在同步前查看更改内容：`git status`。
- 已经推送的大文件无法通过此脚本自动删除。
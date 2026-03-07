---
name: github-push
description: "使用自动SSH连接和远程配置文件来增强GitHub推送的安全性。适用于需要执行git push操作、自动化推送或处理冲突的场景。"
---
# GitHub Push - 安全自动推送工具

该工具支持自动将代码推送到 GitHub，具备以下功能：

- **自动配置 SSH 密钥**：自动检测并加载 SSH 密钥。
- **自动添加远程仓库**：自动将本地 Git 仓库添加到远程的 `origin` 仓库。
- **自动解决合并冲突**：执行 `pull`、`rebase` 和 `force` 操作来处理合并冲突。
- **防滥用机制**：通过限制推送频率、分批提交以及智能验证来防止滥用。

## 安装

无需任何外部依赖，仅使用标准的 Git 命令行工具（始终可用）。

## 使用示例

```bash
# Quick push (auto-configures everything)
python3 scripts/github_upload.py --repo owner/repo --path ./files --message "Update"

# Dry run test (no actual push)
python3 scripts/github_upload.py --repo owner/repo --path ./files --dry-run

# Force push (auto-resolves conflicts)
python3 scripts/github_upload.py --repo owner/repo --path ./files --force

# Show version info
python3 scripts/github_upload.py --version
```

## 配置

创建 `config.yaml` 文件以保存配置信息：

```yaml
defaults:
  safe_mode: true
  min_delay: 3  # seconds between operations
  max_delay: 5  # seconds between operations
  batch_commits: true
  enable_validation: true
  dry_run: false
  
safety:
  max_commits_per_hour: 100
  max_pushes_per_hour: 50
  min_time_between_pushes: 180  # 3 minutes cooldown
```

## 安全阈值

| 参数          | 默认值         | 说明                          |
|--------------|--------------|-------------------------------------------|
| 操作间隔时间    | 3-5秒        | 操作之间的随机延迟时间                  |
| 推送冷却时间    | 180秒        | 最小推送间隔时间                    |
| 每小时最大推送次数 | 50次         | 防止垃圾推送的限制                    |
| 每小时最大提交次数 | 100次         | 防止自动化滥用的限制                    |

## 故障排除

### 错误：推送过于频繁

**解决方法**：等待至少 3 分钟后再进行下一次推送。

### 错误：未找到仓库

**解决方法**：确认仓库存在，并且您具有推送权限；同时检查 SSH 密钥是否已添加到 GitHub。

### 错误：权限被拒绝（提示“publickey”）

**解决方法**：
```bash
# Load SSH key
ssh-add ~/.ssh/id_ed25519

# Verify SSH connection
ssh -T git@github.com
```

### 错误：合并冲突

**解决方法**：脚本会自动执行 `pull`、`rebase` 和 `force` 操作来处理合并冲突。如果问题仍然存在，请检查仓库的状态。

### 错误：验证失败

**解决方法**：
- 确认目标路径存在且可访问。
- 确保文件大小不超过 100MB（GitHub 的限制）。
- 检查文件中是否存在可疑内容（例如 `.env` 文件或 `id_rsa` 文件）。

## 适用场景

- 仅用于将代码推送到 GitHub。
- 不适用于创建问题（issues）或提交 Pull Request（PRs）。
- 不适用于代码审核（code review）。

## 参考资料

- `references/`：详细的配置和 API 文档。
- `scripts/`：完整的代码示例。

---

**许可证**：MIT 许可证（OpenClaw Skill Standard）
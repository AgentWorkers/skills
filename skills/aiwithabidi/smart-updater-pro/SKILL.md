---
name: auto-updater
description: OpenClaw自动更新检查器与安全应用工具：该工具会检测新版本，对比变更日志，并在确保可回滚安全性的前提下应用更新。专为通过Cron作业实现无人值守维护而设计，用于自动保持OpenClaw的最新状态。
homepage: https://www.agxntsix.ai
license: MIT
compatibility: OpenClaw gateway, git
metadata: {"openclaw": {"emoji": "\ud83d\udd04", "requires": {"bins": ["git"]}, "homepage": "https://www.agxntsix.ai"}}
---

# 自动更新工具 🔄

**自动且安全地保持 OpenClaw 的最新状态。**

该工具通过 Git 标签检测新的 OpenClaw 版本，与您的当前版本进行比较，显示更新内容，并可选择性地应用更新，同时提供安全的回滚支持。

## 快速入门

```bash
# Check for updates (safe, read-only)
bash {baseDir}/scripts/check_update.sh

# Check and apply if available
bash {baseDir}/scripts/check_update.sh --apply

# JSON output (for cron/automation)
bash {baseDir}/scripts/check_update.sh --json

# Check + apply + JSON
bash {baseDir}/scripts/check_update.sh --apply --json
```

## 设置为 Cron 作业

### 通过 OpenClaw Cron
将以下命令添加到您的 Cron 作业中，以实现每日检查：

```json
{
  "name": "auto-update-check",
  "schedule": "0 1 * * *",
  "command": "bash skills/auto-updater/{baseDir}/scripts/check_update.sh --json",
  "description": "Daily OpenClaw update check at 1 AM"
}
```

### 通过系统 Crontab
```bash
# Check daily at 1 AM, log results
0 1 * * * cd /root/.openclaw/workspace && bash skills/auto-updater/{baseDir}/scripts/check_update.sh >> /var/log/openclaw-updates.log 2>&1
```

## 工作原理

1. **获取更新** — 从 OpenClaw 仓库执行 `git fetch --tags` 命令
2. **比较版本** — 比较当前版本与最新的 Git 标签（按版本号排序）
3. **显示差异** — 显示版本间的差异以及变更日志/提交记录
4. **应用更新**（可选） — 检出新的 Git 标签 → 使用 `pnpm install` 安装新版本 → 使用 `pnpm build` 构建新版本 → 使用 `docker build` 构建容器 → 使用 `docker compose up -d` 启动服务
5. **验证更新** — 检查更新后服务是否正常运行

## 安全更新实践

- **始终** 在比较版本之前执行 `git fetch` 命令（获取最新数据）
- **在应用更新前** 显示所有变更内容
- **记录** 上一个版本信息以便回滚
- **更新后** 验证服务的运行状态
- **严禁** 强制推送或修改 Git 历史记录

## 回滚流程

如果更新导致问题发生：

```bash
# 1. See recent tags
cd /host/openclaw && git tag --sort=-v:refname | head -5

# 2. Checkout previous version
git checkout <previous-tag>

# 3. Rebuild
pnpm install && pnpm build
docker build -t openclaw:latest .
docker compose up -d

# 4. Verify
docker compose logs --tail=20
```

该脚本会在应用更新时自动输出回滚步骤。

## 致谢
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该工具是 **AgxntSix Skill Suite** 中用于 OpenClaw 代理的一部分。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
---
name: arc-skill-gitops
description: 自动化部署、回滚以及代理工作流和技能的版本管理。
user-invocable: true
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux"], "requires": {"bins": ["python3", "git"]}}}
---
# Agent GitOps

用于自动化部署和回滚代理工作流程的工具。可跟踪技能版本，确保部署的可靠性，并在出现问题时能够快速回滚。

## 该工具存在的必要性

代理会不断安装和更新技能。当更新导致问题时，你需要：
1. 了解具体发生了什么变化；
2. 迅速回滚到之前的稳定版本；
3. 记录下哪个版本是稳定的。

该工具负责管理这些技能的整个生命周期。

## 命令

### 为某个技能初始化跟踪功能
```bash
python3 {baseDir}/scripts/gitops.py init --skill ~/.openclaw/skills/my-skill/
```

### 对当前状态进行快照备份（在更新之前）
```bash
python3 {baseDir}/scripts/gitops.py snapshot --skill ~/.openclaw/skills/my-skill/ --tag "pre-update"
```

### 部署技能更新（先对当前状态进行快照备份）
```bash
python3 {baseDir}/scripts/gitops.py deploy --skill ~/.openclaw/skills/my-skill/ --tag "v1.1"
```

### 列出某个技能的所有快照
```bash
python3 {baseDir}/scripts/gitops.py history --skill ~/.openclaw/skills/my-skill/
```

### 回滚到之前的快照版本
```bash
python3 {baseDir}/scripts/gitops.py rollback --skill ~/.openclaw/skills/my-skill/ --tag "pre-update"
```

### 检查所有被跟踪的技能的状态
```bash
python3 {baseDir}/scripts/gitops.py status
```

### 运行部署前的检查（如有 `arc-skill-scanner`，则会与之集成）
```bash
python3 {baseDir}/scripts/gitops.py check --skill ~/.openclaw/skills/my-skill/
```

## 数据存储

快照和元数据存储在 `~/.openclaw/gitops/` 目录下。

## 工作原理

1. `init` 命令会在技能目录中创建一个 Git 仓库（如果尚不存在的话），并将其信息记录在跟踪清单中；
2. `snapshot` 命令会使用标签来提交当前的状态；
3. `deploy` 命令会先对当前状态进行快照备份，然后再提交更新后的状态；
4. `rollback` 命令会通过 `git checkout` 恢复到之前的快照版本；
5. `check` 命令会在部署前运行 `arc-skill-scanner`（如果已安装）来进行安全检查；
6. `history` 命令会显示所有带有时间戳的快照记录；
7. `status` 命令会显示所有被跟踪的技能及其当前/最新版本。

## 使用建议：

- 在手动更新技能之前，务必先进行快照备份；
- 使用 `deploy` 命令进行部署，因为它会自动进行快照备份；
- 结合 `arc-skill-scanner` 进行安全性的部署控制；
- 标签应具有描述性，例如：“v1.2”、“pre-security-patch”、“stable-2026-02-15”等。
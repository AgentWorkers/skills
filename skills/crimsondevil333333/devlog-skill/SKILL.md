---
name: DevLog Skill
description: OpenClaw代理使用`dev-log-cli`工具的标准化日志记录功能，以跟踪进度、任务和项目状态。
---

# DevLog 技能 🦞

这是一个标准化的日志记录工具，专为 OpenClaw 代理设计，用于使用 `dev-log-cli` 跟踪进度、任务和项目状态。

## 描述
该技能使代理能够维护专业的开发日志。它旨在将上下文信息、项目里程碑和任务状态记录到一个结构化的 SQLite 数据库中。

## 需求
- 安装了 `dev-log-cli`（通过 `pipx` 安装）

## 链接
- **GitHub**: [https://github.com/CrimsonDevil333333/dev-log-cli](https://github.com/CrimsonDevil333333/dev-log-cli)
- **PyPI**: [https://pypi.org/project/dev-log-cli/](https://pypi.org/project/dev-log-cli/)
- **ClawHub**: [https://clawhub.com/skills/devlog-skill](https://clawhub.com/skills/devlog-skill)（待发布）

## 使用方法

### 📝 添加日志条目
代理应使用此工具记录重要的进展或遇到的问题。
```bash
devlog add "Finished implementing the auth module" --project "Project Alpha" --status "completed" --tags "auth,feature"
```

### 📋 查看日志
查看最近的活动以了解项目进展。
```bash
devlog list --project "Project Alpha" --limit 5
```

### 📊 查看统计信息
检查项目状态和活动情况。
```bash
devlog stats --project "Project Alpha"
```

### 🔍 搜索
根据特定主题查找历史记录。
```bash
devlog search "infinite loop"
```

### 🛠️ 编辑/查看
详细检查或修改日志条目。
```bash
devlog view <id>
devlog edit <id>
```

## 内部设置
该技能包含一个 `setup.sh` 脚本，以确保 CLI 可以正常使用。
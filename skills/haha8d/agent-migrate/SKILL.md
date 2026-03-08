---
name: agent-migrate
description: "跨平台代理迁移与部署。适用场景：  
(1) 将 OpenClaw 代理迁移到新服务器；  
(2) 备份和恢复代理状态；  
(3) 在不同环境中部署代理配置；  
(4) 在开发环境和生产环境之间同步工作区数据。  
不适用场景：  
- 一般文件备份；  
- 非代理数据的迁移。"
---
# 代理迁移

将 OpenClaw 代理迁移到不同的服务器和平台上，同时保持代理的身份、内存配置和设置不变。

## 适用场景

✅ **在以下情况下使用此技能：**
- 将代理从本地机器迁移到远程服务器
- 将代理配置克隆到多个环境中
- 备份代理的完整状态以用于灾难恢复
- 在开发环境和生产环境之间同步工作区更改
- 升级 OpenClaw 并具备完整的回滚功能

❌ **不适用以下场景：**
- 简单的文件复制操作 → 直接使用 `cp`/`rsync`
- 数据库迁移 → 使用专门的数据库工具
- 部署非 OpenClaw 应用程序

## 核心概念

### 代理状态组件

```
Agent State = Identity + Memory + Config + Skills + Extensions
├── workspace/           # Core identity files
│   ├── IDENTITY.md      # Who the agent is
│   ├── USER.md          # Who they serve
│   ├── SOUL.md          # Personality
│   ├── MEMORY.md        # Long-term memory
│   ├── AGENTS.md        # Operational rules
│   ├── TOOLS.md         # Environment notes
│   └── memory/          # Daily logs
├── .openclaw/
│   ├── openclaw.json    # Gateway config
│   ├── agents/          # Session data
│   └── extensions/      # Custom plugins
└── skills/              # Custom skills (if any)
```

### 迁移工作流程

#### 1. 导出（源机器）

```bash
# Full agent export
./scripts/export-agent.sh [export-name]

# Creates:
# /tmp/agent-export-[name]/
#   ├── manifest.json      # Export metadata
#   ├── workspace.tar.gz   # Core files
#   ├── config.tar.gz      # OpenClaw config
#   └── restore.sh         # Self-contained restore
```

#### 2. 传输

```bash
# Via SSH
scp -r /tmp/agent-export-[name] user@new-server:/tmp/

# Via GitHub (recommended for versioned deployments)
# Push to repo, clone on target
```

#### 3. 导入（目标机器）

```bash
# Run self-contained restore
cd /tmp/agent-export-[name] && ./restore.sh

# Or manual:
./scripts/import-agent.sh /tmp/agent-export-[name]
```

## 脚本

### 导出代理

```bash
scripts/export-agent.sh [name] [--full]
```

选项：
- `name` - 导出标识符（默认值：时间戳）
- `--full` - 包含会话历史记录和日志

### 导入代理

```bash
scripts/import-agent.sh <export-path> [--merge|--replace]
```

选项：
- `--merge` - 与现有代理合并（默认值）
- `--replace` - 删除现有代理并重新安装

### 同步到 GitHub

```bash
scripts/sync-github.sh <repo-url> [--push|--pull]
```

将代理状态同步到 GitHub 以实现版本控制下的部署。

## 平台特定说明

### Linux → Linux
直接传输，无需转换。

### macOS → Linux
- 检查脚本中是否使用了 macOS 特有的路径
- 如果使用了文件监视器，请更新相关设置

### Windows WSL → 原生 Linux
- 系统会自动处理换行符
- 需要验证可执行文件的权限

### Docker 部署
有关容器化部署的详细信息，请参阅 `references/docker-deploy.md`。

## 安全检查清单

- [ ] 清理 `openclaw.json` 文件中的敏感信息（导出前删除）
- [ ] 验证目标机器的权限
- [ ] 迁移后及时更新任何暴露的凭据
- [ ] 在生产环境切换前测试代理的功能

## 回滚
导出的代理状态是不可更改的快照。若需回滚，请执行以下操作：

```bash
# Re-import previous export
./scripts/import-agent.sh /path/to/previous-export --replace
```
# Memoria 系统

## 概述

Memoria 系统是一个专为 AI 助手设计的全面长期内存管理系统。它实现了类似人类的认知记忆架构，为不同类型的信息设置了不同的存储层次。

## 记忆架构

该系统将内存划分为五种不同的类型，这些类型反映了人类的认知结构：

### 1. 语义记忆 (`semantic/`)
用于存储事实性知识、概念和通用信息。
- **facts.md** - 个人事实和关键信息
- **concepts.md** - 学习到的概念和知识
- **knowledge/** - 详细的知识条目

### 2. 情景记忆 (`episodic/`)
用于记录带有时间戳的事件、经历和对话。
- **YYYY-MM-DD.md** - 每日记忆日志
- **events/** - 具体事件的文档记录

### 3. 程序性记忆 (`procedural/`)
用于存储技能、工作流程和学到的程序。
- **skills.md** - 获得的技能和能力
- **workflows.md** - 常见的工作流程和程序
- **scripts/** - 自动化和实用脚本

### 4. 工作记忆 (`working/`)
用于保存当前会话上下文和待处理的任务。
- **current.md** - 活动中的上下文和待办事项
- **session/** - 会话特定的数据

### 5. 索引 (`index/`)
提供快速的查找和搜索功能。
- **tags.json** - 基于标签的索引
- **timeline.json** - 按时间顺序排列的事件索引
- **search/** - 搜索索引

## 工具

### memory-backup.sh
用于创建内存系统的增量备份。

**使用方法：**
```bash
./memory-backup.sh [options]
```

**选项：**
- `--dry-run` - 显示备份内容而不实际执行备份
- `--verbose` - 显示详细输出
- `--path PATH` - 更改内存路径
- `--output PATH` - 更改备份目标路径

### memory-migrate.sh
用于初始化新的内存结构或迁移现有的内存结构。

**使用方法：**
```bash
./memory-migrate.sh {init|daily [DATE]|migrate [VERSION]}
```

**命令：**
- `init` - 初始化内存结构
- `daily [DATE]` - 创建每日记忆文件（默认：今天）
- `migrate [VERSION]` - 从指定版本迁移

### memory-rollback.sh
用于从之前的备份中恢复内存。

**使用方法：**
```bash
./memory-rollback.sh {list|rollback BACKUP_NAME [--force]}
```

**命令：**
- `list` - 列出可用的备份
- `rollback BACKUP_NAME` - 恢复到指定的备份

**选项：**
- `--force` - 跳过确认提示

### memory-health-check.sh
用于验证内存的完整性，并可选地修复问题。

**使用方法：**
```bash
./memory-health-check.sh [options]
```

**选项：**
- `--fix` - 自动修复检测到的问题
- `--path PATH` - 更改内存路径

## 配置

编辑 `config.json` 以自定义系统行为：

```json
{
  "memory": {
    "base_path": "./memory",
    "structure": { ... }
  },
  "backup": {
    "enabled": true,
    "retention_days": 30,
    "schedule": "0 2 * * *"
  },
  "health_check": {
    "auto_fix": false,
    "check_interval_hours": 24
  }
}
```

## 定时任务设置

将相关脚本添加到 crontab 中以实现自动化维护：

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/memoria-system && ./memory-backup.sh

# Weekly health check on Sundays at 3 AM
0 3 * * 0 cd /path/to/memoria-system && ./memory-health-check.sh --fix
```

## 安装

```bash
openclaw skill install memoria-system
```

## 系统要求

- Bash 4.0 或更高版本
- jq（用于 JSON 处理）
- tar（用于备份压缩）

## 许可证

MIT 许可证
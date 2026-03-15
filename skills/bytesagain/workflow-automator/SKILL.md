---
name: workflow-automator
version: 1.1.0
author: BytesAgain
license: MIT-0
---

# 工作流自动化工具

> OpenClaw原生的工作流自动化引擎——通过命令行界面（CLI）定义、运行、调度和管理任务流程。

## 产品描述

Workflow Automator是一个轻量级、无依赖性的工作流引擎，完全由Bash语言编写。它允许AI代理和人类使用简化的YAML格式来定义多步骤任务流程，并支持顺序执行这些流程。该工具具备内置的日志记录、错误处理、重试逻辑、条件分支以及基于Cron的调度功能。

与需要Python、Node.js或Docker的复杂编排工具不同，Workflow Automator可以在任何支持Bash的环境中运行——无论是笔记本电脑、VPS、Raspberry Pi，还是CI/CD系统。它被设计为OpenClaw部署的原生自动化核心组件。

## 使用场景

- 定义可重复的多步骤任务流程（如备份、部署、监控、报告）
- 通过Cron调度自动化工作流
- 运行带有日志记录和错误跟踪的命令
- 管理工作流的执行历史和状态
- 生成常用操作的工作流模板
- 将工作流导出以便与团队成员或其他机器共享
- 在执行前验证工作流文件的有效性
- 适用于任何原本需要大量Shell脚本才能实现的自动化任务

## 命令列表

| 命令 | 功能描述 |
|---------|-------------|
| `init` | 初始化工作流项目——创建目录结构、示例工作流文件及配置文件 |
| `run <文件名>` | 逐步执行工作流文件，提供完整日志记录，失败时重试，并跟踪执行状态 |
| `validate <文件名>` | 验证工作流文件的语法——检查结构、必填字段和步骤定义 |
| `list` | 列出当前项目中的所有工作流文件，包括文件名、步骤数量和上次执行状态 |
| `status [运行ID]` | 显示当前正在运行的工作流或特定运行的详细信息 |
| `log [运行ID]` | 查看执行日志——默认显示最新运行记录，或指定运行ID |
| `schedule <文件名> <Cron表达式>` | 根据Cron表达式调度工作流（例如`0 2 * * *`表示每天凌晨2点执行） |
| `template <类型>` | 生成工作流模板（备份、部署、监控、报告） |
| `export <文件名>` | 将工作流导出为可共享的压缩文件（Base64编码） |
| `history [数量]` | 查看执行历史记录——默认显示最近10次运行记录，或指定记录数量 |

## 工作流文件格式

工作流文件采用简化的YAML格式，无需外部依赖即可被Bash解析：

```yaml
name: daily-backup
description: "Back up database and notify team. Use when you need workflow automator capabilities. Triggers on: workflow automator."
retry: 2
on_failure: notify

steps:
  - name: check-disk
    run: df -h | head -5
  - name: backup-db
    run: pg_dump mydb > /backups/backup-$(date +%Y%m%d).sql
    retry: 3
  - name: compress
    run: gzip /backups/backup-$(date +%Y%m%d).sql
    condition: test -f /backups/backup-$(date +%Y%m%d).sql
  - name: notify
    run: echo "Backup completed successfully at $(date)"
```

### 支持的字段

- **name**（必填）：工作流名称标识符
- **description**：人类可读的描述文本
- **retry**：所有步骤的默认重试次数（默认为0）
- **on_failure**：工作流失败时执行的命令
- **steps**：按顺序排列的执行步骤列表
  - **name**（必填）：步骤标识符
  - **run**（必填）：要执行的Shell命令
  - **retry**：步骤级别的重试设置
  - **condition**：Shell表达式——只有当表达式返回0时，步骤才会执行
  - **timeout**：步骤的最大执行时间（默认为300秒）
  - **on_failure**：步骤级别的失败处理程序

## 项目结构

执行`init`命令后，您的工作流项目结构如下：

```
workflows/
├── .workflow/
│   ├── config          # Project configuration
│   ├── runs/           # Execution history and logs
│   └── schedules/      # Cron schedule definitions
├── templates/          # Generated templates
└── example.yml         # Sample workflow
```

## 主要特性

- **无依赖性**：完全基于Bash语言，无需Python/Node/Ruby
- **逐步执行**：每个步骤都会记录时间戳和退出代码
- **错误重试**：支持按步骤或全局配置重试次数
- **条件执行**：根据Shell条件跳过某些步骤
- **Cron调度**：支持Cron表达式进行定期执行
- **执行历史记录**：详细记录每次运行的情况
- **模板支持**：提供备份、部署、监控、报告等快速启动模板
- **导出/共享**：可将工作流打包为可共享的文件
- **彩色输出**：执行过程中提供清晰的视觉反馈
- **并发安全**：通过文件锁定机制防止同一工作流被同时执行

## 与OpenClaw的集成

代理可以通过Workflow Automator实现以下功能：

1. **自动化重复性任务**：定义一次即可永久运行
2. **安排维护任务**：通过Cron定时执行备份、清理或健康检查
3. **构建部署流程**：实现包含回滚机制的多步骤部署
4. **系统监控**：定期检查系统状态并在失败时发出警报
5. **生成报告**：定期收集数据并生成报告

## 脚本位置

主脚本位于：

```
scripts/main.sh
```

通过以下命令运行脚本：`bash scripts/main.sh <命令> [参数]`

---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com
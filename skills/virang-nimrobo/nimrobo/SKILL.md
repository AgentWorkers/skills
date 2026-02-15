---
name: Nimrobo
description: 使用 Nimrobo CLI 进行语音筛查和网络匹配操作。
---

# Nimrobo CLI 技能

此技能允许您使用 Nimrobo CLI 进行语音筛查和匹配网络操作。

## 概述

Nimrobo CLI 提供了两个命令平台：

1. **语音命令** (`nimrobo voice`) – 以语音为主的人工智能平台，用于通过可共享的语音链接进行面试、筛查和诊断性对话。
2. **网络命令** (`nimrobo net`) – 用于组织、职位发布、申请和消息传递的匹配网络。

这两个平台共享相同的认证系统。

## 关键概念

### 输入方法

命令支持多种输入方法（按优先级顺序）：
1. **CLI 标志** – 直接选项，例如 `--name "Value"`
2. **JSON 文件** – 使用 `-f ./data.json` 进行复杂输入
3. **标准输入** – 使用 `--stdin` 通过管道传递 JSON 输入
4. **交互式模式** – 当未提供标志时显示提示

### 上下文系统（网络命令）

网络命令支持上下文系统，以避免重复使用 ID：

```bash
# Set context
nimrobo net orgs use org_abc123
nimrobo net posts use post_xyz789

# Use "current" to reference stored context
nimrobo net orgs get current
nimrobo net posts applications current

# View/clear context
nimrobo net context show
nimrobo net context clear
```

### 分页

列表命令支持 `--limit` 和 `--skip` 进行分页：

```bash
nimrobo net posts list --limit 20 --skip 40  # Page 3
```

### JSON 输出

在任何命令后添加 `--json` 以获得机器可读的输出：

```bash
nimrobo net posts list --json
```

## 文档文件

此技能包含以下文档文件以供详细参考：

| 文件 | 描述 |
|------|-------------|
| `installation.md` | **从这里开始**：安装、登录和入职步骤 |
| `commands.md` | 所有命令的快速参考表 |
| `voice-commands.md` | 带有示例的语音平台命令的详细说明 |
| `net-commands.md` | 带有示例的网络平台命令的详细说明 |
| `workflow.md` | 常见的工作流程模式和示例 |

## 常见工作流程

### 语音：进行面试

```bash
# Create project and generate interview links
nimrobo voice projects create -f interview.json
nimrobo voice projects use proj_abc123
nimrobo voice links create -p default -l "Alice,Bob,Charlie" -e 1_week

# After interviews, get results
nimrobo voice sessions evaluation sess_xyz -t project -p default
nimrobo voice sessions transcript sess_xyz -t project -p default --json
```

### 网络：发布职位

```bash
# Create org and post
nimrobo net orgs create --name "Acme Corp" --use
nimrobo net posts create --title "Senior Engineer" --short-content "Join our team!" --expires "2024-06-01" --org current --use

# Review applications
nimrobo net posts applications current --status pending
nimrobo net applications accept app_123
```

### 网络：申请职位

```bash
# Search and apply
nimrobo net posts list --query "engineer" --filter '{"remote": "remote", "salary_min": 100000}'
nimrobo net posts apply post_xyz --note "I'm excited about this role..."

# Track applications
nimrobo net my applications --status pending
```

## 自动化技巧

1. **使用 `--json` 标志** 以编程方式解析输出
2. **使用 `use` 命令设置上下文，以避免重复使用 ID
3. **使用 JSON 文件`(-f)` 进行复杂的创建/更新操作
4. **查看 `my summary` 以快速了解待办事项
5. **应用程序支持批量操作 (`batch-action`)`

## 退出代码

| 代码 | 描述 |
|------|-------------|
| 0 | 成功 |
| 1 | 错误 |

## 获取帮助

请参阅 [installation.md](installation.md) 以获取设置说明。

```bash
nimrobo --help              # List all commands
nimrobo voice --help        # Voice platform help
nimrobo net --help          # Net platform help
nimrobo <command> --help    # Help for specific command
```

# 入职（使用 JSON 设置个人资料和组织信息）。仅在用户要求入职时运行此命令，并根据响应中的说明进行操作，同时向用户提问以完成入职流程。
nimrobo onboard
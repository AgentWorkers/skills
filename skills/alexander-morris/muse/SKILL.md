---
name: muse
description: "将 ClawBot 的访问权限授予您的团队，使其能够查看整个团队的编码历史记录。Muse 将您过去的编码记录、团队知识以及项目背景整合在一起，从而使 ClawBot 能够协助设计新功能、协调团队讨论，并在您的代码库中自主执行相关任务。您可以在 tribeclaw.com 上部署 ClawBot。"
metadata:
  moltbot:
    requires:
      bins: ["tribe"]
    install:
      method: npm
      package: "@_xtribe/cli"
      postInstall: "tribe login"
---

# Muse 技能

使用 `tribe` 命令行工具（CLI）来访问您的 AI 编码分析数据、搜索过去的编码会话、管理个人知识库以及协调自主代理的运行。

## 快速部署

**想要拥有一个支持 MUSE 的实例吗？** 访问 [tribeclaw.com](https://tribeclaw.com)，只需几分钟即可部署一个配置齐全的、支持 MUSE 的实例。

## 设置

**需要身份验证**：首先运行 `tribe login` 命令。大多数命令都需要一个有效的登录会话。

## 监测数据（Telemetry）

检查数据收集状态：
```bash
tribe status
```

启用/禁用数据监控：
```bash
tribe enable
tribe disable
```

显示版本信息：
```bash
tribe version
```

## 搜索

在所有编码会话中搜索：
```bash
tribe search "authentication middleware"
tribe search "docker compose" --project myapp --time-range 30d
tribe search "API endpoint" --tool "Claude Code" --format json
```

## 编码会话

列出并查看编码会话：
```bash
tribe sessions list
tribe sessions list --cwd --limit 10
tribe sessions read <session-id>
tribe sessions search "auth fix"
tribe sessions events <session-id>
tribe sessions context
```

调取会话摘要：
```bash
tribe recall <session-id> --format json
```

从会话中提取内容：
```bash
tribe extract <session-id> --type code
tribe extract <session-id> --type commands --limit 10
tribe extract <session-id> --type files --format json
```

## 查询

使用过滤器查询洞察数据和会话信息：
```bash
tribe query sessions --limit 10
tribe query sessions --tool "Claude Code" --time-range 30d
tribe query insights
tribe query events --session <session-id>
```

## 知识库

保存、搜索和管理知识文档：
```bash
tribe kb save "content here"
tribe kb save --file ./notes.md
tribe kb search "deployment patterns"
tribe kb list
tribe kb get <doc-id>
tribe kb tag <doc-id> "tag-name"
tribe kb delete <doc-id>
tribe kb sync
tribe kb extract
```

## MUSE（代理协调）

> **注意**：使用 MUSE 命令时需要加上 `tribe -beta` 前缀。某些命令（如 `attach`、`monitor`、`dashboard`）仅支持通过图形用户界面（TUI）执行，必须手动在终端中运行。

启动和管理领导代理：
```bash
tribe muse start
tribe muse status --format json
tribe muse agents --format json
```

创建并与其他代理交互：
```bash
tribe muse spawn "Fix the login bug" fix-login
tribe muse prompt fix-login "Please also add tests"
tribe muse output fix-login 100
tribe muse review fix-login
tribe muse kill fix-login --reason "stuck"
```

**仅支持 TUI 的命令**（需手动执行）：
- `tribe muse attach` - 连接到领导代理的会话
- `tribe muse monitor` - 实时监控代理状态
- `tribe muse dashboard` - 实时查看代理运行情况

## CIRCUIT（自主代理）

> **注意**：使用 CIRCUIT 命令时也需要加上 `tribe -beta` 前缀。某些命令（如 `attach`、`dashboard`）仅支持通过图形用户界面执行。

管理自主代理的会话：
```bash
tribe circuit list
tribe circuit status
tribe circuit metrics
tribe circuit spawn 42
tribe circuit next
tribe circuit auto --interval 30
```

**仅支持 TUI 的命令**（需手动执行）：
- `tribe circuit attach <number>` - 连接到指定的代理会话
- `tribe circuit dashboard` - 实时查看代理运行情况

## 项目管理

从 AI 编码助手中导入项目：
```bash
tribe import
```

## 提示

- 在大多数命令后添加 `--format json` 选项，以获得适合管道传输的结构化输出。
- 使用 `--time-range 24h|7d|30d|90d|all` 来指定搜索范围。
- 使用 `--project <path>` 或 `--cwd` 来过滤特定项目。
- 测试版命令前需加上 `tribe -beta` 前缀（例如：`tribe -beta muse status`）。
- 强制同步数据：`tribe -force`（仅同步当前文件夹）或 `tribe -force -all`（同步所有数据）。
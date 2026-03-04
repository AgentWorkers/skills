---
name: codex-autopilot
description: >
  **tmux + launchd 多项目 Codex CLI 自动化系统**  
  该系统基于 `tmux` 和 `launchd` 构建，能够实时监控多个 `Codex` 编程会话，自动处理空闲会话的提醒、权限管理、上下文压缩等工作，并执行增量代码审查任务。它通过预设的触发条件（如 `autopilot`、`watchdog` 等）来自动化各种操作，适用于管理多个并发的 `Codex` 编程会话、自动化开发流程，或协调跨项目的 AI 辅助编码工作。  
  **核心功能：**  
  1. **实时监控**：持续监视多个 `tmux` 会话的状态。  
  2. **自动提醒**：对空闲的 `Codex` 会话发送提醒，确保开发者及时处理。  
  3. **权限管理**：自动处理与 `Codex` 会话相关的权限问题。  
  4. **上下文管理**：优化会话的存储空间，提高运行效率。  
  5. **代码审查**：执行增量代码审查，确保代码质量。  
  6. **任务调度**：从任务队列中分派待处理的编码任务。  
  **适用场景：**  
  - 管理多个同时进行的 `Codex` 编程会话。  
  - 自动化开发流程，提高开发效率。  
  - 协调跨项目的 AI 辅助编码工作。  
  **相关术语说明：**  
  - **tmux**：一个终端多窗口管理工具，用于同时运行多个终端会话。  
  - **launchd**：一个系统服务管理工具，用于自动运行程序并管理其生命周期。  
  - **Codex**：一个用于代码开发的命令行工具或平台。  
  - **Auto-pilot**：系统自动执行的预设规则或脚本。  
  - **Watchdog**：监控系统状态的守护进程，确保系统正常运行。
---
# Codex Autopilot

这是一个基于macOS的自动化多项目管理工具，通过tmux和launchd来实现Codex CLI命令的自动化调度。

## 概述

Codex Autopilot运行一个监控循环，用于监视多个在tmux窗口中运行的Codex CLI会话。它能够检测到闲置的会话，并自动提醒用户继续操作；处理权限请求；轮换日志文件；从任务队列中分配任务；并通过Discord或Telegram发送通知。

## 安装

```bash
git clone https://github.com/imwyvern/AIWorkFlowSkill.git ~/.autopilot
cd ~/.autopilot
cp config.yaml.example config.yaml
# Edit config.yaml with your project paths, Telegram bot token, and Discord channels
```

### 所需依赖项

- **macOS**系统，需安装launchd（用于定时任务执行）
- **tmux**：用于管理多个Codex会话的窗口管理器
- **Codex CLI**（`codex`）：OpenAI提供的编码辅助工具
- **python3**：用于清理系统状态和验证项目需求（PRD）
- **yq**：用于解析YAML配置文件
- **jq**：用于处理JSON数据
- **bash 4+**：脚本中需要使用关联数组的功能

通过Homebrew安装依赖项：
```bash
brew install tmux yq jq
```

### launchd配置

使用`install.sh`脚本来配置launchd的服务：
```bash
./install.sh
```

该脚本会创建一个LaunchAgent服务，按照预设的间隔执行监控任务。

## 核心组件

### watchdog.sh
主要监控循环脚本：
1. 遍历所有配置好的项目tmux窗口
2. 通过`codex-status.sh`获取Codex的运行状态
3. 判断会话是活跃状态、闲置状态还是卡住状态
4. 根据状态执行相应的操作（如提醒用户、授予权限、从任务队列中分配任务）
5. 确保遵守冷却时间限制和每日发送通知的次数

### codex-status.sh
用于捕获并分析tmux窗口中的内容：
- 检测Codex的运行状态（工作中/闲置/等待权限）
- 识别需要审批的权限请求
- 监测系统错误或崩溃情况

### tmux-send.sh
用于向特定的tmux窗口发送按键或文本：
- 向Codex的命令行提示符输入内容
- 处理用户按下Enter键以确认权限请求
- 轮询以确认发送操作是否成功

### autopilot-lib.sh
所有脚本共用的功能库：
- 提供Telegram通知功能
- 实现文件锁定机制
- 处理超时和重试逻辑
- 提供日志记录功能
- 负责读写状态文件

### autopilot-constants.sh
定义了脚本中使用的状态常量（如`STATUS_ACTIVE`、`STATUS_IDLE`、`STATUS_PERMISSION`等）

### task-queue.sh
任务队列管理脚本：
- 支持为特定项目添加任务到队列
- 按优先级从队列中取出下一个任务
- 跟踪任务的状态（待处理/运行中/已完成/失败）

### discord-notify.sh
通过Webhook向Discord频道发送格式化通知：
- 支持根据`config.yaml`中定义的项目和频道进行发送

### 其他脚本

| 脚本 | 功能 |
|--------|---------|
| `auto-nudge.sh` | 用于提醒闲置的Codex会话 |
| `auto-check.sh` | 定期检查所有项目的运行状态 |
| `permission-guard.sh` | 自动批准权限请求或标记需要处理的请求 |
| `incremental-review.sh` | 对最近发生的更改进行代码审查 |
| `monitor-all.sh` | 显示所有被监控项目的状态 |
| `status-sync.sh` | 将状态信息同步到`status.json`文件供外部使用 |
| `rotate-logs.sh` | 旋转和清理日志文件 |
| `cleanup-state.py` | 从`status.json`中删除过时的数据 |
| `claude-fallback.sh` | 当Codex无法使用时提供备用处理方案 |
| `prd-audit.sh` | 审核项目需求的完成情况 |
| `prd-verify.sh` / `prd_verify_engine.py` | 根据代码库验证项目需求 |
| `codex-token-daily.py` | 记录每日Token的使用情况 |

## 配置

请编辑`config.yaml`文件（内容可参考`config.yaml.example`）。主要配置部分包括：

### 时间阈值
```yaml
active_threshold: 120    # seconds — Codex considered "working"
idle_threshold: 360      # seconds — Codex considered "idle", triggers nudge
cooldown: 120            # minimum seconds between sends to same project
```

### 安全限制
```yaml
max_daily_sends_total: 200   # global daily send cap
max_daily_sends: 50          # per-project daily cap
max_consecutive_failures: 5  # pause project after N failures
loop_detection_threshold: 3  # detect repeated output loops
```

### 多项目调度器
```yaml
scheduler:
  strategy: "round-robin"    # or "priority"
  max_sends_per_tick: 1
  inter_project_delay: 5     # seconds between project sends
```

### 项目目录
```yaml
project_dirs:
  - "~/project-alpha"
  - "~/project-beta"
```

### Discord频道配置
```yaml
discord_channels:
  my-project:
    channel_id: "123456789"
    tmux_window: "my-project"
    project_dir: "/path/to/project"
```

### Telegram通知设置
```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"
  status_interval: 1800
```

## 使用方法

### 添加项目

1. 在一个命名的tmux窗口中启动一个Codex CLI会话：
   ```bash
   tmux new-window -t autopilot -n my-project
   # In the new window, cd to project and run codex
   ```

2. 将项目路径添加到`config.yaml`的`project_dirs`部分
3. （可选）创建`projects/my-project/tasks.yaml`文件以管理任务队列：
   ```yaml
   project:
     name: "My Project"
     dir: "~/my-project"
     enabled: true
     priority: 1
   tasks:
     - id: "feature-x"
       name: "Implement feature X"
       prompt: |
         Implement feature X per the spec in docs/feature-x.md
   ```

### 手动操作
```bash
# Check status of all projects
./scripts/monitor-all.sh

# Manually nudge a specific project
./scripts/auto-nudge.sh my-project

# Send a command to a tmux window
./scripts/tmux-send.sh my-project "codex exec 'fix the tests'"

# Enqueue a task
./scripts/task-queue.sh enqueue my-project "Refactor auth module"

# Run the watchdog once (for testing)
./scripts/watchdog.sh
```

### Python版本的自动化方案

`autopilot.py`提供了基于Python的替代方案，具有更丰富的状态管理功能：
```bash
python3 autopilot.py --once        # single pass
python3 autopilot.py --daemon      # continuous loop
```

## 目录结构
```
~/.autopilot/
├── SKILL.md                 # This file
├── config.yaml              # Local config (not in git)
├── config.yaml.example      # Config template
├── scripts/                 # All automation scripts
├── projects/                # Per-project task definitions
├── docs/                    # Additional documentation
├── code-review/             # Code review templates
├── development/             # Development workflow templates
├── doc-review/              # Doc review templates
├── doc-writing/             # Doc writing templates
├── requirement-discovery/   # Requirement discovery templates
├── testing/                 # Testing templates
├── tests/                   # Test suite
├── state/                   # Runtime state (gitignored)
├── logs/                    # Runtime logs (gitignored)
├── task-queue/              # Task queue data (gitignored)
└── archive/                 # Deprecated files
```
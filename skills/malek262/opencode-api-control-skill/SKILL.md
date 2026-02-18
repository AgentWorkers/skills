---
name: OpenCode-CLI-Controller
description: 这是一种强大的技能，可以通过本地Web服务器API来控制Open Code CLI。它支持执行命令、管理会话，并在本地网络中远程自动化代码生成。
version: 1.1.0
emoji: 🎛️
author: Malek-Rsh
tags: 
  - cli
  - api
  - automation
  - web-server
  - opencode
metadata:
  openclaw:
    requires:
      bins: 
        - curl
        - jq
        - bash

    install: |
      chmod +x scripts/*.sh
      if ! command -v jq &> /dev/null; then
          echo "Warning: jq is required but not installed."
      fi
    run: |
      echo "OpenCode Control Skill is ready for use."
      echo "Please ensure the OpenCode server is running on port 4099."
---
# OpenCode CLI API 控制

> [!重要提示]
> **操作指南**：
> 虽然您可以使用 `ls` 或基本的文件系统检查来验证文件/目录是否存在，但**严禁**直接读取或修改项目的源代码文件。
> 您执行任务和监控进度的主渠道是 **OpenCode API 及提供的脚本**。

## 概述
本技能提供了一组工具，用于通过 OpenCode 的本地 Web 服务器 API 进行编程接口操作。它使您能够作为 **监督者/协调者**，指导 OpenCode 完成所有的编码、文件操作和质量检查。

## 核心职责：协调者与执行者
- **您不是编码者**：您不直接编写或验证代码。OpenCode 负责实现。
- **您是协调者**：您向 OpenCode 发送高级指令，监控其进度，并将结果报告给用户。
- **信任系统**：OpenCode 负责自身的文件操作。您的任务是等待其完成，然后检查 *状态* 和 *差异摘要*，而不是文件内容。

## 适用场景
- 用户通过 OpenCode 创建或管理项目
- 用户请求通过 OpenCode 进行编码任务、调试或代码分析
- 用户希望使用特定的提供商/模型进行 AI 驱动的开发
- 用户需要管理多个 OpenCode 会话或监控任务

## 先决条件
1. OpenCode 服务器正在运行（推荐：`bash ./scripts/start_server.sh`)
2. 配置文件存在：`./config.json`
3. 所需脚本位于 `./scripts/` 目录中

## 配置
从 `./config.json` 读取设置：
```bash
BASE_URL=$(jq -r '.base_url' ./config.json)
PROJECTS_DIR=$(jq -r '.projects_base_dir' ./config.json)
```

## 代理的重要职责

### 作为协调者的角色
您是用户与 OpenCode 之间的 **监督者和沟通桥梁**。

**操作限制**：
- ❌ **绝不要** 为了开发任务直接读取或编辑 OpenCode 生成的代码文件。
- ❌ **绝不要** 通过检查项目文件来修复或验证代码逻辑。
- ✅ **如果需要**，**可以** 使用 `ls` 或简单的目录检查来确认文件是否存在。
- ⚠️ **建议** 使用提供的脚本和 API 来获取所有与项目相关的信息。

**所需的工作流程**：
- ✅ **主要步骤**：使用 `monitor_session.sh` 或 `check_status.sh` 来跟踪进度。
- ✅ **主要步骤**：使用 `get_diff.sh` 来查看更改的摘要。
- ✅ **始终** 根据 API 响应或脚本输出来报告结果。
- ✅ **信任** OpenCode 对请求功能的实现。

### 服务器初始化等待
**关键**：启动 OpenCode Web 服务器后，需要 **10-15 秒** 的时间才能完全初始化。在发送任何请求之前，**必须** 确认服务器已准备好。

**正确的初始化顺序**：
```bash
# Start server using the robust backgrounding script
bash ./scripts/start_server.sh


# 3. Now safe to proceed with operations
bash ./scripts/update_providers.sh
# ... continue workflow
```

**切勿** 在启动服务器后立即发送请求——务必先检查服务器状态。

### 智能任务监控
对于长时间运行的任务，使用 **智能监控** 策略：
**选项 1：基于事件的监控（推荐）**
```bash
# Start task
bash ./scripts/send_message.sh "Complex task" &

# Monitor events (blocks until completion)
bash ./scripts/monitor_session.sh
```

**选项 2：智能轮询**
```bash
# For environments where event streaming is unreliable
bash ./scripts/send_message.sh "Build application"

# Smart polling with exponential backoff
SLEEP_TIME=2
MAX_SLEEP=30

while true; do
  STATUS=$(bash ./scripts/check_status.sh)
  
  if [ "$STATUS" = "idle" ]; then
    echo "✓ Task completed"
    break
  elif [ "$STATUS" = "busy" ]; then
    echo "⟳ Still working... (checking again in ${SLEEP_TIME}s)"
    sleep $SLEEP_TIME
    
    # Increase wait time (but cap at MAX_SLEEP)
    SLEEP_TIME=$((SLEEP_TIME < MAX_SLEEP ? SLEEP_TIME + 2 : MAX_SLEEP))
  else
    echo "⚠ Unexpected status: $STATUS"
    break
  fi
done
```

**选项 3：基于超时的等待**
```bash
# For predictable task durations
bash ./scripts/send_message.sh "Quick task"

# Wait reasonable time before checking
sleep 10

# Then check once
if [ "$(bash ./scripts/check_status.sh)" = "idle" ]; then
  bash ./scripts/get_diff.sh
fi
```

**应避免的错误做法**：
- ❌ 每 1-2 秒检查一次状态（浪费资源）
- ❌ 重复读取文件以查看任务是否完成
- ❌ 使用 `ls` 或文件系统检查来监控进度
- ❌ 不等待就多次调用 API

**最佳实践**：
- ✅ 使用 `monitor_session.sh` 进行实时更新
- ✅ 使用指数级退避策略进行轮询（开始时为 2 秒，逐渐增加到 30 秒）
- ✅ 估计任务持续时间并适当等待
- ✅ 在确认任务完成后再检查最终结果
- ✅ 允许 OpenCode 代理独立工作——不要过度干预

## 任务启动协议
在开始任何任务（新项目、代码分析、调试等）之前，**用一条消息询问用户**：
> 我可以帮助您。有两个问题：
> 1. **提供商**：使用配置中的默认值，还是指定一个提供商（如 opencode、anthropic、gemini 等）？
> 2. **监控方式**：
>    - **标准模式**（推荐）：发送任务 → 等待完成摘要 → 完成后通知您（节省令牌）
>    - **实时模式**：实时显示进度、文件编辑和事件（消耗更多令牌）
>
> 您希望如何进行？

**如果未指定，默认设置**：使用配置中的默认值 + 标准模式。

### 为什么这很重要
- **标准模式**：使用 `send_message.sh` → 等待 → 显示最终摘要。适用于大多数任务。
- **实时模式**：使用 `monitor_session.sh` 并实时显示进度。适用于需要实时监控的长时间/复杂任务。

### 示例响应处理
- “使用默认提供商，标准模式” → 立即开始
- “使用 Claude Sonnet，实时模式” → 先运行 `select_provider.sh`，然后运行 `monitor_session.sh`
- “使用 Gemini Pro” → 查找提供商，并在未指定时询问监控偏好

---

### 任务完成验证
当任务完成时，通过以下方式获取摘要：
```bash
# Get file changes summary (not individual files)
bash ./scripts/get_diff.sh

# Output example:
# added: src/App.tsx (+120/-0)
# modified: package.json (+5/-2)
# added: src/components/Dashboard.tsx (+89/-0)
```

这样您就可以在不阅读实际文件内容的情况下向用户报告所有需要的信息。

**仅在以下情况下读取特定文件**：
- 用户明确要求查看代码
- 用户请求解释具体实现
- 调试报告的问题

否则，信任差异摘要和 OpenCode 的实现结果。

## 核心工作流程

### 第一步：验证服务器
```bash
# Check health
curl -s "$BASE_URL/global/health" | jq

# Expected: {"healthy": true, "version": "..."}
```

### 第二步：更新提供商缓存
```bash
# Run provider update script
bash ./scripts/update_providers.sh
```

这会将 **仅连接的提供商** 缓存到 `./providers.json` 中。

### 第三步：创建或选择项目
**新项目**：
```bash
PROJECT_NAME="dashboard-app"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"
mkdir -p "$PROJECT_PATH"
```

**现有项目**：
```bash
PROJECT_NAME="existing-app"
PROJECT_PATH="$PROJECTS_DIR/$PROJECT_NAME"
# Verify exists
[ -d "$PROJECT_PATH" ] || { echo "Project not found"; exit 1; }
```

### 第四步：创建会话
使用提供的脚本在项目目录中创建会话：
```bash
SESSION_ID=$(bash ./scripts/create_session.sh "$PROJECT_PATH" "Session Title")
```

### 第五步：保存会话状态
```bash
# Use state management script
bash ./scripts/save_state.sh "$SESSION_ID" "$PROJECT_PATH"
```

### 第六步：发送消息
使用提供的脚本向 AI 发送提示：
```bash
# Use defaults from config
bash ./scripts/send_message.sh "Your prompt here"

# Or use a specific provider and model
bash ./scripts/send_message.sh "Your prompt" "anthropic" "claude-sonnet-4-5"
```

### 第七步：监控进度（对于长时间运行的任务）
```bash
# Start monitoring in background
bash ./scripts/monitor_session.sh &

# Or check status periodically
bash ./scripts/check_status.sh
```

## 提供商选择
### 自动选择（使用配置文件中的默认值）
```bash
bash ./scripts/send_message.sh "Create app"
```

### 用户指定提供商
当用户指定了提供商（例如，“使用 Gemini Pro”或“使用 Claude Sonnet”）时，使用搜索脚本：
```bash
# Search for provider and model hints
RESULT=$(bash ./scripts/select_provider.sh "gemini" "pro")
# Returns: gemini gemini-3-pro

# Extract and use the returned values
PROVIDER_ID=$(echo "$RESULT" | cut -d' ' -f1)
MODEL_ID=$(echo "$RESULT" | cut -d' ' -f2)

bash ./scripts/send_message.sh "Your prompt" "$PROVIDER_ID" "$MODEL_ID"
```

## 代理选择
**默认设置（未指定代理时推荐）**：
```bash
bash ./scripts/send_message.sh "Build app"
```

**规划阶段**：
```bash
bash ./scripts/send_message.sh "Analyze requirements" "plan"
```

**实施阶段**：
```bash
bash ./scripts/send_message.sh "Implement features" "build"
```

## 常见模式
### 模式 1：从头开始创建新项目
```bash
# 1. Update providers
bash ./scripts/update_providers.sh

# 2. Create project directory
mkdir -p "$PROJECTS_DIR/new-app"

# 3. Create session
SESSION_ID=$(bash ./scripts/create_session.sh "$PROJECTS_DIR/new-app" "New App")

# 4. Send initial task
bash ./scripts/send_message.sh "Create React app with TypeScript and Tailwind"

# 5. Monitor progress
bash ./scripts/monitor_session.sh
```

### 模式 2：继续现有项目
```bash
# 1. Load saved project state
bash ./scripts/load_project.sh "existing-app"

# 2. Send new task
bash ./scripts/send_message.sh "Add authentication feature"
```

### 模式 3：多阶段开发
```bash
# Phase 1: Planning
bash ./scripts/create_session.sh "$PROJECT_PATH" "Planning"
bash ./scripts/send_message.sh "Plan e-commerce platform" "plan"

# Phase 2: Implementation
bash ./scripts/send_message.sh "Implement the plan" "build"

# Phase 3: Review
bash ./scripts/get_diff.sh
```

### 模式 4：使用特定提供商
```bash
# User says: "Create dashboard using Claude Sonnet"

# 1. Select provider
PROVIDER_MODEL=$(bash ./scripts/select_provider.sh "claude" "sonnet")
PROVIDER_ID=$(echo "$PROVIDER_MODEL" | cut -d' ' -f1)
MODEL_ID=$(echo "$PROVIDER_MODEL" | cut -d' ' -f2)

# 2. Create project and session
mkdir -p "$PROJECTS_DIR/dashboard"
SESSION_ID=$(bash ./scripts/create_session.sh "$PROJECTS_DIR/dashboard" "Dashboard")

# 3. Send with selected provider
bash ./scripts/send_message.sh "Create dashboard" "$PROVIDER_ID" "$MODEL_ID"
```

## 事件监控
对于长时间运行的任务，监控事件：
```bash
# Start monitoring (shows progress in real-time)
bash ./scripts/monitor_session.sh

# This will:
# - Show text deltas as they're generated
# - Display status changes (busy/idle)
# - Show final token count and cost
# - Exit when task completes
```

## 状态管理
所有会话状态都保存在 `./state/` 中：
```bash
# Save current session
bash ./scripts/save_state.sh "$SESSION_ID" "$PROJECT_PATH"

# Load state (sets environment variables)
source ./scripts/load_state.sh
echo $SESSION_ID
echo $PROJECT_PATH

# Save project-specific state
bash ./scripts/save_project.sh "project-name"

# Load project-specific state
bash ./scripts/load_project.sh "project-name"

# List all saved projects
ls -1 ./state/*.json | grep -v current.json | xargs -n1 basename .json
```

## 文件操作
获取会话更改：
```bash
bash ./scripts/get_diff.sh
```

获取文件内容：
```bash
curl -s "$BASE_URL/file/content?directory=$PROJECT_PATH&path=src/App.tsx" \
  jq -r '.content'
```

列出目录：
```bash
curl -s "$BASE_URL/file?directory=$PROJECT_PATH&path=src" \
  jq -r '.[] | "\(.type): \(.path)"'
```

## 错误处理
所有脚本都会返回正确的退出代码：
- `0` = 成功
- `1` = 错误

检查脚本状态：
```bash
if bash ./scripts/send_message.sh "prompt"; then
  echo "Success"
else
  echo "Failed - check server or authentication"
fi
```

## 认证
本技能假设 OpenCode 服务器运行在受信任的本地环境中，并且默认不使用密码认证。

## 快速参考
| 任务 | 命令 |
|------|---------|
| 更新提供商 | `bash ./scripts/update_providers.sh` |
| 创建会话 | `bash ./scripts/create_session.sh "$PATH" "Title"` |
| 发送消息 | `bash ./scripts/send_message.sh "prompt"` |
| 使用提供商 | `bash ./scripts/send_message.sh "prompt" "provider" "model"` |
| 监控进度 | `bash ./scripts/monitor_session.sh` |
| 检查状态 | `bash ./scripts/check_status.sh` |
| 获取更改 | `bash ./scripts/get_diff.sh` |
| 保存状态 | `bash ./scripts/save_state.sh "$SID" "$PATH"` |
| 加载状态 | `source ./scripts/load_state.sh` |
| 保存项目 | `bash ./scripts/save_project.sh "name"` |
| 加载项目 | `bash ./scripts/load_project.sh "name"` |
| 选择提供商 | `bash ./scripts/select_provider.sh "name" "model"` |

## 重要说明
1. **始终从技能目录运行脚本**：脚本使用相对路径。
2. **在工作流程开始时更新提供商**：确保缓存是最新的。
3. **项目存储在 PROJECTS_BASE_DIR** 中：在配置文件中配置。
4. **每个会话属于一个项目目录**：不要混淆会话。
5. **在执行 curl 命令之前加载状态**：确保变量已设置。
6. **脚本处理认证**：无需手动添加请求头。

## 故障排除
**“没有活动会话”**：
```bash
# Load or create session first
bash ./scripts/create_session.sh "$PROJECT_PATH" "Title"
```

**“找不到提供商”**：
```bash
# Update providers cache
bash ./scripts/update_providers.sh

# Check available providers
jq -r '.providers[] | .id' ./providers.json
```

**“返回 HTML 响应而不是 JSON”**：
- 缺少 `directory` 参数
- 检查：您是否使用了完整的 PROJECT_PATH？

## 高级用法
对于复杂的工作流程、状态管理或高级模式，请参阅：
- `Reference/STATE_MANAGEMENT.md` - 高级状态管理
- `Reference/PROVIDERS_REFERENCE.md` - 提供商选择详情
- `Reference/EVENTS_GUIDE.md` - 事件监控模式
- `Reference/COMPLETE_EXAMPLES.md` - 完整的工作流程示例
- `Reference/API_QUICK_REFERENCE.md` - 原始 API 端点

## 目录结构
```
opencode-api-control/
├── SKILL.md                    # This file
├── config.json                 # Configuration
├── providers.json              # Connected providers cache
├── scripts/                    # Helper scripts
│   ├── update_providers.sh
│   ├── create_session.sh
│   ├── send_message.sh
│   ├── monitor_session.sh
│   ├── check_status.sh
│   ├── get_diff.sh
│   ├── save_state.sh
│   ├── load_state.sh
│   ├── save_project.sh
│   ├── load_project.sh
│   └── select_provider.sh
├── state/                      # Session state
│   ├── current.json
│   └── project-name.json
└── Reference/                       # Reference docs
    ├── STATE_MANAGEMENT.md
    ├── PROVIDERS_REFERENCE.md
    ├── EVENTS_GUIDE.md
    ├── COMPLETE_EXAMPLES.md
    └── API_QUICK_REFERENCE.md
```
---
**作者：** [Malek RSH](https://github.com/malek262) | **仓库：** [OpenCode-CLI-Controller](https://github.com/malek262/opencode-api-control-skill)
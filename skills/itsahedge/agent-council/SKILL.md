---
name: agent-council
description: 这是一个用于创建自主AI代理和管理OpenClaw Discord频道的完整工具包。适用于设置多代理系统、创建新代理或管理Discord频道组织时使用。
---

# 代理委员会（Agent Council）

这是一个完整的工具包，用于创建和管理具有 Discord 集成的自主 AI 代理，适用于 OpenClaw。

## 该工具包的功能

**代理创建：**
- 创建具有独立工作空间的自主 AI 代理
- 生成 SOUL.md 文件（包含代理的个性和职责）
- 生成 HEARTBEAT.md 文件（包含定时执行逻辑）
- 设置内存系统（混合架构）
- 自动配置网关
- 将代理绑定到 Discord 频道（可选）
- 设置每日内存定时任务（可选）

**Discord 频道管理：**
- 通过 API 创建 Discord 频道
- 配置 OpenClaw 网关的允许列表
- 设置特定频道的系统提示信息
- 重命名频道并更新相关引用
- 提供工作空间文件搜索功能（可选）

## 安装

```bash
# Install from ClawHub
clawhub install agent-council

# Or manual install
cp -r . ~/.openclaw/skills/agent-council/
openclaw gateway config.patch --raw '{
  "skills": {
    "entries": {
      "agent-council": {"enabled": true}
    }
  }
}'
```

## 第一部分：代理创建

### 快速入门

```bash
scripts/create-agent.sh \
  --name "Watson" \
  --id "watson" \
  --emoji "🔬" \
  --specialty "Research and analysis specialist" \
  --model "anthropic/claude-opus-4-5" \
  --workspace "$HOME/agents/watson" \
  --discord-channel "1234567890"
```

### 工作流程

#### 1. 收集信息
向用户询问以下内容：
- **代理名称**（例如：“Watson”）
- **代理 ID**（小写，用连字符分隔，例如：“watson”）
- **表情符号**（例如：“🔬”）
- **专业领域**（代理的职责）
- **使用的模型**（LLM 模型）
- **工作空间位置**（用于存储代理文件的目录）
- **Discord 频道 ID**（可选）

#### 2. 运行创建脚本
```bash
scripts/create-agent.sh \
  --name "Agent Name" \
  --id "agent-id" \
  --emoji "🤖" \
  --specialty "What this agent does" \
  --model "provider/model-name" \
  --workspace "/path/to/workspace" \
  --discord-channel "1234567890"  # Optional
```

脚本将自动完成以下操作：
- ✅ 创建包含内存子目录的工作空间
- ✅ 生成 SOUL.md 和 HEARTBEAT.md 文件
- ✅ 更新网关配置（保留现有代理）
- ✅ 如果指定了频道，将代理绑定到该频道
- ✅ 重启网关以应用更改
- ✅ 提示用户设置每日内存定时任务

#### 3. 自定义代理
创建代理后，可以进一步自定义：
- **SOUL.md**：完善代理的个性、职责和行为规范
- **HEARTBEAT.md**：添加定期检查逻辑和定时执行任务
- **工作空间文件**：添加针对该代理的特定配置

### 代理架构

**独立结构：**
```
agents/
├── watson/
│   ├── SOUL.md              # Personality and responsibilities
│   ├── HEARTBEAT.md         # Cron execution logic
│   ├── memory/              # Agent-specific memory
│   │   ├── 2026-02-01.md   # Daily memory logs
│   │   └── 2026-02-02.md
│   └── .openclaw/
│       └── skills/          # Agent-specific skills (optional)
```

**内存系统：**
- **代理专属内存**：`<工作空间>/memory/YYYY-MM-DD.md`
- **共享内存访问**：代理可以访问共享的工作空间
- **每日更新**：通过定时任务生成摘要

**定时任务：**
如果代理需要执行定时任务：
1. 创建包含执行逻辑的 HEARTBEAT.md 文件
2. 使用 `--session <代理 ID>` 添加定时任务
3. 在 SOUL.md 文件中记录这些任务

### 示例
- **研究代理**：```bash
scripts/create-agent.sh \
  --name "Watson" \
  --id "watson" \
  --emoji "🔬" \
  --specialty "Deep research and competitive analysis" \
  --model "anthropic/claude-opus-4-5" \
  --workspace "$HOME/agents/watson" \
  --discord-channel "1234567890"
```
- **图像生成代理**：```bash
scripts/create-agent.sh \
  --name "Picasso" \
  --id "picasso" \
  --emoji "🎨" \
  --specialty "Image generation and editing specialist" \
  --model "google/gemini-3-flash-preview" \
  --workspace "$HOME/agents/picasso" \
  --discord-channel "9876543210"
```
- **健康监控代理**：```bash
scripts/create-agent.sh \
  --name "Nurse Joy" \
  --id "nurse-joy" \
  --emoji "💊" \
  --specialty "Health tracking and wellness monitoring" \
  --model "anthropic/claude-opus-4-5" \
  --workspace "$HOME/agents/nurse-joy" \
  --discord-channel "5555555555"
```

## 第二部分：Discord 频道管理

### 频道创建

#### 快速入门

```bash
python3 scripts/setup-channel.py \
  --name research \
  --context "Deep research and competitive analysis"
```

### 工作流程
1. 运行设置脚本：
```bash
python3 scripts/setup-channel.py \
  --name <channel-name> \
  --context "<channel-purpose>" \
  [--category-id <discord-category-id>]
```

2. 应用网关配置（脚本提供的命令）：
```bash
openclaw gateway config.patch --raw '{"channels": {...}}'
```

#### 选项
- **按类别创建频道**：```bash
python3 scripts/setup-channel.py \
  --name research \
  --context "Deep research and competitive analysis" \
  --category-id "1234567890"
```

- **使用现有频道**：```bash
python3 scripts/setup-channel.py \
  --name personal-finance \
  --id 1466184336901537897 \
  --context "Personal finance management"
```

### 频道重命名

#### 快速入门

```bash
python3 scripts/rename-channel.py \
  --id 1234567890 \
  --old-name old-name \
  --new-name new-name
```

### 工作流程
1. 运行重命名脚本：
```bash
python3 scripts/rename-channel.py \
  --id <channel-id> \
  --old-name <old-name> \
  --new-name <new-name> \
  [--workspace <workspace-dir>]
```

2. 如果需要更新系统提示信息，应用网关配置（脚本提供指导）
3. 提交工作空间文件的更改（如果使用了 `--workspace` 参数）

#### 带有工作空间搜索功能的频道管理
```bash
python3 scripts/rename-channel.py \
  --id 1234567890 \
  --old-name old-name \
  --new-name new-name \
  --workspace "$HOME/my-workspace"
```

该功能将：
- 通过 API 重命名 Discord 频道
- 更新网关的系统提示信息
- 搜索并更新工作空间文件
- 报告文件更改以便进行 Git 提交

## 完整的多代理设置流程

**从零开始的完整工作流程：**
```bash
# 1. Create Discord channel
python3 scripts/setup-channel.py \
  --name research \
  --context "Deep research and competitive analysis" \
  --category-id "1234567890"

# (Note the channel ID from output)

# 2. Apply gateway config for channel
openclaw gateway config.patch --raw '{"channels": {...}}'

# 3. Create agent bound to that channel
scripts/create-agent.sh \
  --name "Watson" \
  --id "watson" \
  --emoji "🔬" \
  --specialty "Deep research and competitive analysis" \
  --model "anthropic/claude-opus-4-5" \
  --workspace "$HOME/agents/watson" \
  --discord-channel "1234567890"

# Done! Agent is created and bound to the channel
```

## 配置

### Discord 频道类别 ID

**方法 1：命令行**
```bash
python3 scripts/setup-channel.py \
  --name channel-name \
  --context "Purpose" \
  --category-id "1234567890"
```

**方法 2：环境变量**
```bash
export DISCORD_CATEGORY_ID="1234567890"
python3 scripts/setup-channel.py --name channel-name --context "Purpose"
```

### 查找 Discord 频道 ID
- 打开 Discord 设置 → 高级选项 → 开发者模式
- 右键点击频道或类别 → 复制 ID

## 脚本参考

### create-agent.sh
**参数：**
- `--name`（必填）- 代理名称
- `--id`（必填）- 代理 ID（小写，用连字符分隔）
- `--emoji`（必填）- 代理的表情符号
- `--specialty`（必填）- 代理的职责
- `--model`（必填）- 使用的 LLM 模型
- `--workspace`（必填）- 代理文件的工作空间位置
- `--discord-channel`（可选）- 要绑定的 Discord 频道 ID

**输出：**
- 创建代理的工作空间
- 生成 SOUL.md 和 HEARTBEAT.md 文件
- 更新网关配置
- （可选）设置每日内存定时任务

### setup-channel.py
**参数：**
- `--name`（必填）- 频道名称
- `--context`（必填）- 频道的用途/上下文
- `--id`（可选）- 现有频道 ID
- `--category-id`（可选）- Discord 频道类别 ID

**输出：**
- 如果频道不存在，则创建新的频道
- 生成网关配置文件（`config.patch`）

### rename-channel.py
**参数：**
- `--id`（必填）- 频道 ID
- `--old-name`（必填）- 原频道名称
- `--new-name`（必填）- 新频道名称
- `--workspace`（可选）- 用于搜索的工作空间目录

**输出：**
- 重命名 Discord 频道
- （如果需要）更新网关的系统提示信息
- 列出已更新的文件（如果启用了工作空间搜索功能）

## 网关集成
该工具包支持与 OpenClaw 的网关配置集成：
- **代理管理**：```json
{
  "agents": {
    "list": [
      {
        "id": "watson",
        "name": "Watson",
        "workspace": "/path/to/agents/watson",
        "model": {
          "primary": "anthropic/claude-opus-4-5"
        },
        "identity": {
          "name": "Watson",
          "emoji": "🔬"
        }
      }
    ]
  }
}
```
- **频道管理**：```json
{
  "channels": {
    "discord": {
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": {
            "1234567890": {
              "allow": true,
              "requireMention": false,
              "systemPrompt": "Deep research and competitive analysis"
            }
          }
        }
      }
    }
  }
}
```

## 代理协调
您可以使用 OpenClaw 内置的会话管理工具来协调各个代理：

### 查看活跃代理
查看所有活跃代理及其最近的活动：
```typescript
sessions_list({
  kinds: ["agent"],
  limit: 10,
  messageLimit: 3  // Show last 3 messages per agent
})
```

### 向代理发送消息
**直接通信：**
```typescript
sessions_send({
  label: "watson",  // Agent ID
  message: "Research the competitive landscape for X"
})
```

**等待代理回复：**
```typescript
sessions_send({
  label: "watson",
  message: "What did you find about X?",
  timeoutSeconds: 300  // Wait up to 5 minutes
})
```

### 创建子代理
对于复杂任务，可以在隔离的会话中创建子代理：
```typescript
sessions_spawn({
  agentId: "watson",  // Optional: use specific agent
  task: "Research competitive landscape for X and write a report",
  model: "anthropic/claude-opus-4-5",  // Optional: override model
  runTimeoutSeconds: 3600,  // 1 hour max
  cleanup: "delete"  // Delete session after completion
})
```

子代理将：
1. 在隔离环境中执行任务
2. 向主会话报告任务完成情况
3. （如果设置了 `cleanup: "delete"`，则自动删除自身

### 查看代理历史记录
查看代理的工作记录：
```typescript
sessions_history({
  sessionKey: "watson-session-key",
  limit: 50
})
```

### 协调模式
**1. 直接委托（绑定到 Discord 的代理）：**
- 用户通过 Discord 频道向代理发送消息
- 代理直接在该频道回复
- 主代理无需进行额外协调

**2. 程序化委托（主代理 → 子代理）：**
```typescript
// Main agent delegates task
sessions_send({
  label: "watson",
  message: "Research X and update memory/research-X.md"
})

// Watson works independently, updates files
// Main agent checks later or Watson reports back
```

**3. 为复杂任务创建子代理：**
```typescript
// For longer-running, isolated work
sessions_spawn({
  agentId: "watson",
  task: "Deep dive: analyze competitors A, B, C. Write report to reports/competitors.md",
  runTimeoutSeconds: 7200,
  cleanup: "keep"  // Keep session for review
})
```

**4. 代理间的通信：**
代理之间可以互相发送消息：
```typescript
// In Watson's context
sessions_send({
  label: "picasso",
  message: "Create an infographic from data in reports/research.md"
})
```

### 最佳实践
- **何时使用 Discord 集成：**
  - ✅ 需要特定领域知识的代理（如研究、健康监控、图像生成）
  - 用户希望直接与代理交流
  - 代理需要响应频道内的消息

- **何时使用 `sessions_send`：**
  - 需要程序化协调时
  - 主代理需要将任务委托给专家代理
  - 需要在同一会话中接收代理的回复

- **何时使用 `sessions_spawn`：**
  - 执行耗时较长的任务（超过 5 分钟）
  - 需要隔离处理的任务
  - 需要在后台运行的任务

### 示例：研究工作流程
```typescript
// Main agent receives request: "Research competitor X"

// 1. Check if Watson is active
const agents = sessions_list({ kinds: ["agent"] })

// 2. Delegate to Watson
sessions_send({
  label: "watson",
  message: "Research competitor X: products, pricing, market position. Write findings to memory/research-X.md"
})

// 3. Watson works independently:
//    - Searches web
//    - Analyzes data
//    - Updates memory file
//    - Reports back when done

// 4. Main agent retrieves results
const results = Read("agents/watson/memory/research-X.md")

// 5. Share with user
"Research complete! Watson found: [summary]"
```

### 通信流程
**主代理（您） ↔ 专业代理：**
```
User Request
    ↓
Main Agent (Claire)
    ↓
sessions_send("watson", "Research X")
    ↓
Watson Agent
    ↓
- Uses web_search
- Uses web_fetch
- Updates memory files
    ↓
Responds to main session
    ↓
Main Agent synthesizes and replies
```

**绑定到 Discord 的代理：**
```
User posts in #research channel
    ↓
Watson Agent (bound to channel)
    ↓
- Sees message directly
- Responds in channel
- No main agent involvement
```

**混合使用方式：**
```
User: "Research X" (main channel)
    ↓
Main Agent delegates to Watson
    ↓
Watson researches and reports back
    ↓
Main Agent: "Done! Watson found..."
    ↓
User: "Show me more details"
    ↓
Main Agent: "@watson post your full findings in #research"
    ↓
Watson posts detailed report in #research channel
```

## 故障排除

**代理创建问题：**
- **代理未出现在 Discord 中**：
  - 确认频道 ID 是否正确
  - 检查网关配置中的绑定设置
  - 重启网关：`openclaw gateway restart`

**模型相关问题：**
- **模型错误**：
  - 确认模型名称的格式（`provider/model-name`）
  - 检查模型是否在网关配置中可用

**频道管理问题：**
- **创建频道失败**：
  - 确保机器人具有“管理频道”的权限
  - 检查 OpenClaw 配置中的机器人令牌
  - 确认类别 ID 是否正确

- **找不到频道**：
  - 确认类别 ID 是否正确
  - 检查机器人是否具有访问该类别的权限
  - 可以尝试不使用类别 ID（此时会创建未分类的频道）

**使用场景**
- **领域专家代理**：研究、健康监控、财务分析、代码编写
- **创意代理**：图像生成、内容创作、设计
- **任务自动化**：定期监控、报告生成、警报发送
- **多代理系统**：由多个专业代理组成的协作团队
- **Discord 组织**：为不同类型的代理创建结构化的频道

## 高级功能：多代理协调
对于大型多代理系统：
- **协调模式**：
  - 主代理将任务委托给专家代理
  - 代理报告进度并请求帮助
  - 共享知识库以共享信息
  - 通过 `sessions_send` 实现代理间的通信

**任务管理：**
- 与任务跟踪系统集成
- 根据代理的专业领域分配任务
- 跟踪任务的状态和完成情况

**文档记录：**
- 在主工作空间中维护代理列表
- 记录代理的职责和协作模式
- 为常见工作流程编写操作手册

## 最佳实践：
1. **按类别组织频道**：将相关代理频道分组
2. **使用描述性强的频道名称**：确保频道名称能够清晰反映其用途
3. **设置具体的系统提示信息**：为每个频道提供明确的上下文
4. **更新代理的职责信息**：保持 SOUL.md 文件的准确性
5. **设置内存定时任务**：为需要持续运行的代理设置定时任务
6. **单独测试每个代理**：在集成到团队之前进行测试
7. **安全地更新网关配置**：始终使用 `config.patch`，避免手动编辑

## 所需权限和工具：
- **机器人权限：**
  - `Manage Channels`：用于创建/重命名频道
  - `View Channels`：用于查看频道列表
  - `Send Messages`：用于在频道中发送消息

**系统要求：**
- 安装并配置了 OpenClaw
- 安装并配置 Node.js 和 npm（通过 nvm）
- Python 3.6 或更高版本（仅使用标准库）
- Discord 机器人令牌（用于频道管理）

**相关资源：**
- OpenClaw 文档：https://docs.openclaw.ai
- 多代理使用指南：https://docs.openclaw.ai/agents
- Discord 机器人设置指南：https://docs.openclaw.ai/channels/discord
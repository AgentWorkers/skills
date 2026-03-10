---
name: memoryai
description: 为AI代理提供持久性的长期记忆功能：能够存储数据、检索信息、进行推理，并在会话切换时实现零上下文丢失（即无需重新获取之前会话的信息）。
version: 0.6.0
metadata: {"openclaw": {"emoji": "🧠", "requires": {"bins": ["python3"], "env": ["HM_API_KEY", "HM_ENDPOINT"]}, "primaryEnv": "HM_API_KEY"}}
---
# MemoryAI — 为您的人工智能助手提供持久记忆支持 🧠

> **每个AI会话都从零开始。但您的AI不必如此。**

您可能需要花费数小时来解释自己的代码库、偏好设置以及架构决策，然后会话结束。第二天呢？您的AI就会“失忆”，您又得从头开始。

**MemoryAI可以永久解决这个问题。**它为您的人工智能助手提供了真正的长期记忆功能——能够记住您所构建的内容、所做的决策、您的偏好以及原因。这种记忆不会仅持续几个小时，而是可以持续数周、数月，甚至数年。

### 实际应用示例：

> **周一：**“我们的API使用/v1/前缀，代码采用TypeScript格式，并通过GitHub Actions进行部署。”
>
> **三周后：**您再次提出“创建一个新的API端点”的要求。您的AI已经掌握了前缀、代码风格以及部署流程，完全不需要重复解释。因为它记住了这些信息。

### AI的记忆系统工作原理：

- 🔥 **热点记忆**：日常使用的功能、当前的偏好设置。可以立即检索，始终保持清晰。
- 🌤️ **温存记忆**：重要的背景信息、已完成的任务。这些记忆会逐渐淡出，但在需要时可以迅速调取。
- ❄️ **冷存记忆**：旧项目、历史对话记录。这些数据永远不会被删除，且随时可查询。

AI使用记忆的频率越高，其记忆就越清晰。未被使用的记忆会被转移到冷存区，但只需一次检索，就能立即调取出来。这就像人类的记忆系统一样。

**完全依赖Python标准库，无任何第三方依赖。**每一行源代码都是可读的、可审计的，且属于您自己掌控的范围。

### 新功能：

- **v0.6.0**：**Context Guard v4**：直接从OpenClaw读取令牌使用情况，无需依赖任何API，支持跨平台使用。
- **v0.5.0**：**无缝会话切换**：可以在不丢失任何信息的情况下切换会话。

## 设置方法

1. 从https://memoryai.dev获取API密钥（免费 tier可用）。
2. 修改`{baseDir}/config.json`文件：
   或者设置环境变量`HM_ENDPOINT`和`HM_API_KEY`。
3. 运行测试命令：`python {baseDir}/scripts/client.py stats`

## 命令说明

### 存储记忆
```bash
python {baseDir}/scripts/client.py store -c "data to remember" -t "tag1,tag2" -p hot
```
优先级：`hot`（重要内容，需要频繁检索） | `warm`（默认设置） | `cold`（长期存储）

可选参数：
- `--memory-type <类型>`：`fact`（事实）、`decision`（决策）、`preference`（偏好设置）、`error`（错误信息）、`goal`（目标）、`episodic`（片段化记忆）
- `--retention <策略>`：`forever`（永久保存）、`6m`（6个月）、`1y`（1年）、`auto`（自动决定）

### 检索记忆
```bash
python {baseDir}/scripts/client.py recall -q "what was discussed?" -d deep
```
`depth`参数用于控制记忆的检索深度：
- `fast`：快速表面检索
- `deep`：深入搜索，关联相关记忆
- `exhaustive`：全面检索

### 统计信息
```bash
python {baseDir}/scripts/client.py stats
```

### 合并记忆（压缩数据）
```bash
python {baseDir}/scripts/client.py compact -c "session transcript or context" -t "task description"
```
类似于人类大脑在睡眠中整合记忆的过程——将长时间内的会话内容提炼成关键信息。

### 恢复会话上下文
```bash
python {baseDir}/scripts/client.py restore -t "what I was working on"
```
在开始新任务时，AI会自动恢复之前的上下文信息。

### 检查记忆状态
```bash
python {baseDir}/scripts/client.py check
```
返回记忆的紧急程度：`low`（低）| `medium`（中）| `high`（高）| `critical`（紧急）

### 自我反思
```bash
python {baseDir}/scripts/client.py reflect --hours 24 --max-insights 5
```
分析近期记忆中的重复模式，生成有价值的洞察。

## 会话切换（v0.5.0）
支持无缝切换会话——当当前会话的上下文信息达到上限时，系统会自动切换到新会话，而不会丢失任何信息。

### 工作原理：
1. 旧会话将其对话内容发送到您配置的MemoryAI服务器（使用HTTPS）。
2. 新会话从同一服务器获取旧对话内容及相关长期记忆。
3. 新会话获取足够的上下文后，旧会话会被存入长期存储。

### 启动会话切换（保存旧会话）
```bash
python {baseDir}/scripts/client.py handoff-start -c '[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]'
```
或者通过标准输入（stdin）传递会话数据：
```bash
echo '[ ... conversation ... ]' | python {baseDir}/scripts/client.py handoff-start
```

### 恢复旧会话内容
```bash
python {baseDir}/scripts/client.py handoff-restore
```
新会话会读取旧会话的对话内容及相关记忆信息。

可选参数：
- `--no-memories`：跳过相关记忆内容
- `--memory-limit N`：限制检索的记忆数量（默认值：5条）

### 完成会话切换（存档旧会话）
```bash
python {baseDir}/scripts/client.py handoff-complete
```
将旧会话内容存入长期存储，并标记切换操作完成。

### 检查切换状态
```bash
python {baseDir}/scripts/client.py handoff-status
```
返回当前会话切换的状态。

## Context Guard（可选功能）

这是一个后台任务，用于在会话内容过多时自动监控并压缩记忆数据。

**启用此功能前，请先获取用户许可，然后创建一个定时任务：**
- 名称：`context-guard`
- 时间间隔：每15分钟（`everyMs: 900000`）
- 会话模式：`isolated`（独立运行）
- 通知方式：`none`（不发送通知）
- 任务内容：`agentTurn`（执行任务）

**重要提示：**在创建定时任务前务必征得用户同意。

## 使用场景：

| 触发条件 | 执行操作 | 优先级 | 标签 |
|---------|--------|----------|------|
| 任务完成 | 保存结果 | hot | projects（项目相关） |
| 用户要求“记住这个内容” | 保存相关信息 | hot | people（用户相关） |
| 研究/搜索完成 | 保存研究成果 | warm | research（研究相关） |
| 需要回顾过去的信息 | 检索相关记忆 | — | — |
| 会话结束 | 合并重要记忆 | — | — |
| 会话开始 | 恢复当前任务的上下文 | — | — |
| 会话内容过多 | 自动切换会话 | — | — |
| 新会话信息足够完整 | 完成会话切换 | — | — |

## 记忆管理规则：

- 仅当用户询问过去的工作内容、之前的决策，或当前会话需要相关背景信息时，才进行记忆检索。
- 不要在每条消息都进行记忆检索，仅在确实需要时才执行。
- 完成任务后保存重要结果（而非每条消息都保存）。
- 以自然的方式呈现检索到的记忆内容——将检索结果整合到回答中，而不是直接显示原始API输出。
- 在启用Context Guard或任何后台任务之前，必须征得用户许可。
- 会话切换操作是透明进行的，由后台系统自动处理。

## 平台兼容性

所有核心记忆功能都支持支持Python 3.10及以上版本的操作系统：

| 功能 | 所有平台 | 仅支持OpenClaw |
|---------|---:|:---:|
| 存储/检索/统计 | ✅ | ✅ |
| 合并/恢复/检查 | ✅ | ✅ |
| 手动会话切换 | ✅ | ✅ |
| 自我反思 | ✅ | ✅ |
| 自动记忆监控 | — | ✅ |
| 自动会话切换 | — | ✅ |

**在集成开发环境（IDE）中：**（如Cursor、VS Code、Claude Code、Windsurf、Antigravity）：
- 所有记忆操作均通过`client.py`命令行工具执行。
- 可以在会话内容过多时手动触发会话切换。
- Context Guard功能需要OpenClaw的定时任务系统来支持。

**在OpenClaw上：**
- 支持所有核心记忆功能，包括自动会话切换和Context Guard。
- Context Guard利用OpenClaw的定时系统进行定期检查。

## 数据与隐私保护

MemoryAI通过HTTPS将存储的记忆数据发送到配置的服务器。所有数据均通过加密连接传输，并存储在独立的私有数据库中。
用户可以随时通过`/v1/export`导出所有数据，或通过`DELETE /v1/data`删除数据。
内置的`client.py`仅使用Python标准库（`urllib`），无任何第三方依赖。源代码完全公开且可审计。
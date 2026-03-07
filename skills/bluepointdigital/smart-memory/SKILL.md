---
name: smart-memory
description: 通过 Node.js 适配器和 FastAPI 引擎，为 OpenClaw 实现持久的本地认知记忆功能。
---
# Smart Memory v2 技能

Smart Memory v2 是一个持久的认知记忆运行时系统，而非传统的基于向量内存的命令行界面（CLI）工具。

**核心运行时组件：**
- **节点适配器：** `smart-memory/index.js`
- **本地 API：** `server.py`（FastAPI）
- **编排器：** `cognitive_memory_system.py`

## **核心功能：**
- 结构化的长期记忆（类型包括：** **情景记忆（episodic）**、**语义记忆（semantic）**、**信念记忆（belief）**、**目标记忆（goal）**
- 具有实体感知能力的检索和重新排序功能
- 热工作记忆（hot working memory）
- 背景认知功能（包括反思、信息巩固、记忆衰退处理以及冲突解决）
- 严格的提示生成规则（基于预定义的标记）
- 可观测性接口：`/health`、`/memories`、`/memory/{id}`、`/insights/pending`

## **与 OpenClaw 的原生集成（v2.5）**

请使用 OpenClaw 的原生技能包：
- `skills/smart-memory-v25/index.js`
- 可选的钩子辅助文件：`skills/smart-memory-v25/openclaw-hooks.js`
- 技能描述文件：`skills/smart-memory-v25/SKILL.md`

**主要提供的接口函数：**
- `createSmartMemorySkill(options)`：创建 Smart Memory 技能实例
- `createOpenClawHooks({ skill, agentIdentity, summarizeWithLLM })`：配置 OpenClaw 与技能的交互逻辑

### **工具接口（供代理工具使用）：**

1. **`memory_search`**
   - **用途：** 查询长期记忆中的信息。
   - **输入参数：**
     - `query`（字符串，必填）
     - `type`（`all`/`semantic`/`episodic`/`belief`/`goal`，默认为 `all`）
     - `limit`（数字，默认为 `5`）
     - `min_relevance`（数字，默认为 `0.6`）
   - **行为：** 首先检查系统健康状态（`/health`），然后通过 `/retrieve` 获取数据，并返回格式化后的结果。

2. **`memory_commit`**
   - **用途：** 显式地保存重要的信息、决策、信念或目标。
   - **输入参数：**
     - `content`（字符串，必填）
     - `type`（`semantic`/`episodic`/`belief`/`goal`，必填）
     - `importance`（1-10，默认为 `5`）
     - `tags`（字符串数组，可选）
   - **行为：**
     - 首先检查系统健康状态
     - 如果缺少相关标签，会自动添加默认标签（如 `working_question`、`decision`）
     - 保存的数据会按顺序序列化，以优化 CPU 的处理性能
     - 如果服务器无法访问，数据会被放入 `.memory_retry_queue.json` 队列中
     - 如果服务器无法访问，会返回错误信息：`Memory commit failed - server unreachable. Queued for retry.`

3. **`memory_insights`**
   - **用途：** 查看待处理的背景认知结果。
   - **输入参数：**
     - `limit`（数字，默认为 `10`）
   - **行为：** 首先检查系统健康状态，然后调用 `/insights/pending` 并返回格式化的结果列表。

### **可靠性保障：**
- 每次使用工具之前必须检查系统健康状态（通过 `GET /health`）。
- 当工具正常运行或发送心跳信号时，会自动清空重试队列。
- 心跳机制支持自动重试和后台维护功能。

### **会话流程管理：**
- **v2.5 版本支持会话流程的捕获：**
  - 每 20 次交互会自动创建检查点。
  - 在会话结束或重置时，会捕获会话的完整信息。

**流程步骤：**
1. 提取最近的 20 次交互记录。
2. 使用提示生成摘要：
   - `Summarize this session arc：本次会话的目标是什么？尝试了哪些方法？做出了哪些决策？还有哪些问题未解决？`
3. 通过 `memory_commit` 将摘要保存到长期记忆中，格式如下：
   - `type`：`episodic`
   - `tags`：`["session_arc", "YYYY-MM-DD"]`

### **被动上下文注入：**
- 在生成响应之前，可以使用 `inject_active_context`（或 `createOpenClawHooks().beforeModelResponse`）函数。

**提示示例：**
在代理的默认提示中添加以下提示：
“如果您的上下文中出现了与当前对话相关的待处理认知结果，请自然地展示给用户。不要强行展示，但如果有明确的关联，请流畅地将其呈现出来。”

### **OpenClaw 的基本使用示例：**
```js
const {
  createSmartMemorySkill,
  createOpenClawHooks,
} = require("./skills/smart-memory-v25");

const memory = createSmartMemorySkill({
  baseUrl: "http://127.0.0.1:8000",
  summarizeSessionArc: async ({ prompt, conversationText }) => {
    return openclaw.llm.complete({ system: prompt, user: conversationText });
  },
});

const hooks = createOpenClawHooks({
  skill: memory.skill,
  agentIdentity: "OpenClaw Agent",
  summarizeWithLLM: async ({ prompt, conversationText }) => {
    return openclaw.llm.complete({ system: prompt, user: conversationText });
  },
});

// Register memory.tools as callable tools:
// - memory_search
// - memory_commit
// - memory_insights
// and call hooks.beforeModelResponse / hooks.onTurn / hooks.onSessionEnd at lifecycle points.
```

## **节点适配器方法（基础适配器）：**
- `start()` / `init()`：启动适配器
- `ingestMessage(interaction)`：接收用户输入
- `retrieveContext({ user_message, conversation_history })`：获取对话历史记录
- `getPromptContext(promptComposerRequest)`：获取提示生成所需的上下文
- `runBackground(scheduled)`：启动后台处理
- `stop()`：停止适配器

## **API 接口：**
- `GET /health`：获取系统健康状态
- `POST /ingest`：上传新数据
- `POST /retrieve`：查询数据
- `POST /compose`：生成新的提示
- `POST /run_background`：执行后台任务
- `GET /memories`：列出所有保存的记忆记录
- `GET /memory/{memory_id}`：获取指定记忆记录的详细信息
- `GET /insights/pending`：查看待处理的认知结果

### **安装说明：**
- **仅适用于 CPU 环境：** 对于 Docker、WSL 或没有 NVIDIA GPU 的笔记本电脑，建议仅使用基于 CPU 的 PyTorch 版本。

```bash
# from repository root
cd smart-memory

# Create Python venv
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install CPU-only PyTorch FIRST
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Then install remaining dependencies
pip install -r requirements-cognitive.txt

# Finally, install Node dependencies
npm install
```

## **PyTorch 使用注意事项：**
- Smart Memory v2 仅支持基于 CPU 的 PyTorch 版本。
- 请不要为该项目安装包含 GPU/CUDA 功能的 PyTorch 版本。
- 请按照提供的安装流程（`npm install` → `postinstall.js`）进行安装，以确保始终使用 CPU 版本的 PyTorch。

### **已弃用的功能：**
- 传统的基于向量内存的 CLI 工具（`smart_memory.js`、`vector_memory_local.js`、`focus_agent.js`）在 v2.0 版本中被移除。
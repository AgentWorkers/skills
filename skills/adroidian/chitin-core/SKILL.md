# chitin-core

**功能：** 将任务路由到成本最低且性能最佳的模型，并确保系统不会因速率限制而崩溃。

## 激活机制

在创建子代理或分配任务时，使用 `ModelRouter` 来选择最合适的模型。

**触发语句：** “route this”（路由此任务）、“spawn a sub-agent”（创建子代理）或任何需要为任务选择模型的情况。

## 使用方法

### 路由任务
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js route "task description here"
```

**返回结果：** JSON 格式的数据（包含所选模型的信息）
```json
{"tier":"MEDIUM","model":"google-antigravity/gemini-3.1-pro","confidence":0.85,"estimatedCost":0.005,"signals":["codeSignals:2×1.2=2.4"]}
```

在 `sessions_spawn` 函数中使用返回的 `model` 值来创建会话。

### 处理失败情况

如果创建的会话因速率限制或错误而失败：
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js fail "provider/model" "error message"
```

**重新路由任务：** 将失败的任务重新分配给其他模型（跳过当前不可用的模型）
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js route "same task"
```

### 检查模型健康状况
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js health
```

### 查看任务成本
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js costs
```

### 验证配置
```bash
node ~/.openclaw/workspace/skills/chitin-core/scripts/router.js validate
```

## 工作流程

1. 从用户处接收任务。
2. 调用 `router.js route "<task>"` 以获取最适合该任务的模型。
3. 使用返回的模型通过 `sessions_spawn` 函数创建会话。
4. 如果创建会话失败（例如因速率限制），则调用 `router.js fail "<model>" "<error>"` 重试路由。
5. 将处理结果返回给用户。

## 模型层级

| 层级 | 使用场景 | 可用模型 |
|------|----------|--------|
| **LIGHT** | 问候语、简单问答、状态查询 | Flash、DeepSeek、gpt-5-mini、Groq、Ollama |
| **MEDIUM** | 代码分析、内容总结、常规任务 | Gemini Pro、gpt-5.2、DeepSeek Reasoner |
| **HEAVY** | 复杂推理、需要智能代理处理的任务 | gpt-5.2-pro、o3、Codex |

## 重写模型标签

在任务文本中使用以下标签来指定所需的模型层级：
- `@light`：强制使用最便宜的模型。
- `@medium`：强制使用中等性能的模型。
- `@heavy`：强制使用性能最强的模型。

## 优雅降级机制

如果某个层级的所有模型都因速率限制而无法使用，系统会自动：
1. 尝试使用相邻层级的模型（升级或降级）。
2. 如果配置了本地 Ollama，系统会回退到使用 Ollama。
3. 返回包含重试时间的结构化错误信息（确保系统不会崩溃）。

## 配置方式

通过修改 `config.json` 文件来配置系统：
- 为每个层级添加或删除可用模型。
- 调整模型对应的成本参数。
- 调整模型性能的判断标准。
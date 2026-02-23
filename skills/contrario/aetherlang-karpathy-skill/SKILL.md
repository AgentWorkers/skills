---
name: aetherlang-karpathy-upgrades
description: 实现10种高级AI代理节点类型，适用于任何DSL/运行时系统：计划编译器、代码解释器、智能路由机制、多代理集成系统、持久化存储机制、外部API工具、迭代循环处理模块、数据转换功能以及并行执行能力。每当用户需要为工作流引擎添加代理功能、构建AI编排框架、实现类似Karpathy的AI升级方案、向DSL运行时系统添加新的节点类型，或创建自主运行的代理管道时，均可使用此技能。此外，在用户提及AetherLang、流程引擎、节点类型、代理框架，或希望对其AI系统进行升级（如添加自我编程、反射功能、路由机制、集成系统、存储支持或工具使用能力）时，也应触发该技能的运用。
---
# AetherLang Karpathy 代理升级

这是一套经过实战验证的技能，用于实现10种高级AI代理节点类型，能够将任何简单的LLM（Large Language Model）流程转化为一个完全自主的AI代理框架。这些升级方案基于Andrej Karpathy关于AI系统的愿景——即AI系统能够自主思考、计算、反思和行动。

这些升级方案是在AetherLang Omega平台（neurodoc.app）上构建并经过生产环境测试的，涵盖了真实的API调用、Docker部署以及实时流量测试。

## 十项Karpathy升级内容

| 编号 | 节点类型 | 功能 | 作用 |
|------|---------|--------|------|
| 1    | `plan`    | 自编程    | LLM动态生成子流程，然后在运行时编译并执行它们 |
| 2    | `code_interpreter` | 真实计算 | 在安全的环境中执行Python代码，避免计算错误 |
| 3    | `critique` | 自我改进 | 评估输出质量（0-10分），根据反馈最多重试3次直到达到阈值 |
| 4    | `router`    | 智能路由    | LLM选择最佳处理路径，跳过未选中的路径（速度提升10倍） |
| 5    | `ensemble` | 多代理合成 | 并行运行多个AI代理，合成更优的响应 |
| 6    | `memory`    | 持久状态    | 在多次执行中存储/检索数据，并支持命名空间隔离 |
| 7    | `tool`    | 外部API访问 | 可以调用任何REST API（GET/POST/PUT/DELETE），并具有安全限制 |
| 8    | `loop`    | 迭代执行 | 可以对多个项目重复执行某个节点，支持收集或链式操作 |
| 9    | `transform` | 数据转换   | 在节点之间进行数据模板化、提取、格式化或由LLM驱动的转换 |
| 10   | `parallel` | 并行执行 | 同时运行多个节点（3个API请求可在0.2秒内完成，而非3秒） |

## 架构模式

所有升级都遵循相同的3步实现模式，适用于任何基于Python的DSL（Domain-Specific Language）运行时环境。

### 第一步：解析器 — 将节点类型添加到枚举中
```python
class NodeType(Enum):
    LLM = "llm"
    # ... existing types ...
    PLAN = "plan"
    CODE_INTERPRETER = "code_interpreter"
    CRITIQUE = "critique"
    ROUTER = "router"
    ENSEMBLE = "ensemble"
    MEMORY = "memory"
    TOOL = "tool"
    LOOP = "loop"
    TRANSFORM = "transform"
    PARALLEL = "parallel"
```

### 第二步：运行时调度 — 路由到处理程序
在主节点执行调度器中添加`elif`分支：
```python
async def _execute_node(self, ctx, node):
    if node.node_type == NodeType.LLM:
        result = await self._execute_llm(ctx, node, data)
    elif node.node_type == NodeType.PLAN:
        result = await self._execute_plan(ctx, node, data)
    elif node.node_type == NodeType.CODE_INTERPRETER:
        result = await self._execute_code_interpreter(ctx, node, data)
    # ... etc for all 10 types
```

### 第三步：运行时方法 — 实现逻辑
在运行时类中添加`async def _execute_<type>()`方法。

**重要警告**：在Python中，如果一个方法名在一个类中出现了两次，那么最后定义的方法会覆盖之前的定义。在插入新方法之前，务必检查并删除旧的代码片段：
```bash
grep -c "async def _execute_plan" runtime.py  # Must be exactly 1
```

## 实现顺序和依赖关系

由于存在依赖关系，请按照以下顺序进行实现：

1. **PLAN** — 无依赖，基础的自编程功能 |
2. **CODE_INTERPRETER** — 无依赖，独立的沙箱执行环境 |
3. **CRITIQUE** — 使用 `_execute_node()` 进行重试，需要现有的节点执行逻辑 |
4. **ROUTER** — 使用 `_execute_node()` 处理选中的路径，需要在主循环中实现跳过逻辑 |
5. **ENSEMBLE** — 使用 `asyncio.gather()` 进行并行代理执行 |
6. **MEMORY** — 基于文件的JSON持久化存储，完全独立 |
7. **TOOL** — 需要HTTP客户端（在Docker中推荐使用httpx而非aiohttp） |
8. **LOOP** — 使用 `_execute_node()` 进行目标节点的迭代 |
9. **TRANSFORM** — 独立的JSON解析和LLM数据重新格式化 |
10. **PARALLEL** — 使用 `asyncio.gather()`，需要实现类似于ROUTER的跳过逻辑 |

---

## 升级 #1：PLAN — 自编程编译器

`PLAN`节点允许AI动态编写自己的处理流程。

**参数**：
- `steps`（整数）：需要生成的子步骤数量，默认值为3

**工作原理**：
1. 向LLM发送请求，要求其将任务分解为N个连续的步骤。
2. LLM返回JSON格式的结果：`[{"step": 1, "action": "description", "type": "llm|code|search"}]`。
3. 对于每个步骤，创建一个临时节点并执行它。
4. 收集所有步骤的结果，并将它们组合成最终响应。

**系统提示用于生成计划**：
```
Break this task into exactly {steps} sequential steps.
Return ONLY a JSON array: [{"step": 1, "action": "what to do", "type": "llm"}]
Valid types: llm (text generation), code (calculation), search (information lookup)
```

**实现代码**：
```python
async def _execute_plan(self, ctx, node, data):
    query = data["inputs"].get("query", "")
    steps = int(node.params.get("steps", "3"))
    
    # 1. Generate plan via LLM
    plan_response = await self.openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": plan_system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0.3
    )
    plan = json.loads(plan_response.choices[0].message.content)
    
    # 2. Execute each step
    results = []
    for step in plan:
        step_result = await self._execute_plan_step(ctx, step, query, results)
        results.append(step_result)
    
    # 3. Combine results
    combined = "\n\n".join([f"Step {r['step']}: {r['result']}" for r in results])
    return {"response": combined, "plan_steps": plan, "node_type": "plan"}
```

---

## 升级 #2：CODE_INTERPRETER — 沙箱化的Python执行环境

在安全的环境中执行Python代码，以确保计算的准确性，避免LLM产生的错误结果。

**安全配置**：
```python
FORBIDDEN_OPERATIONS = ['__import__', 'exec', 'eval', 'compile', 'open',
                        'subprocess', 'os', 'sys', 'socket', 'shutil']
ALLOWED_IMPORTS = {'math': math, 'statistics': statistics}
SAFE_BUILTINS = {'abs': abs, 'round': round, 'min': min, 'max': max,
                 'sum': sum, 'len': len, 'range': range, 'int': int,
                 'float': float, 'str': str, 'bool': bool, 'list': list,
                 'dict': dict, 'print': print, 'isinstance': isinstance}
CODE_TIMEOUT = 5  # seconds
```

**实现代码**：
```python
async def _execute_code_interpreter(self, ctx, node, data):
    query = data["inputs"].get("query", "")
    
    # 1. LLM generates code
    code_response = await self.openai_client.chat.completions.create(
        model=node.params.get("model", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "Write Python code. Set variable `result` at the end. ONLY code, no markdown."},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    )
    code = code_response.choices[0].message.content.strip()
    code = code.replace("```python", "").replace("```", "").strip()
    
    # 2. 安全检查
    for forbidden in FORBIDDEN_OPERATIONS:
        if forbidden in code:
            return {"response": f"被阻止：{forbidden}", "node_type": "code_interpreter"}
    
    # 3. 沙箱化执行
    safe_globals = {"__builtins__": SAFE_BUILTINS, "math": math, "statistics": statistics}
    local_vars = {}
    
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(exec, code, safe_globals, local_vars)
        future.result(timeout=CODE_TIMEOUT)
    
    result = local_vars.get("result", "没有设置结果变量")
    return {"response": str(result), "code": code, "node_type": "code_interpreter"}
```

---

## Upgrade #3: CRITIQUE — Self-Improvement Loop

Evaluates output quality and retries with feedback until quality threshold is met.

**Parameters**:
- `threshold` (float): Minimum score 0-10, default 7
- `max_retries` (int): Max attempts, capped at hard limit of 3
- `criteria` (str): Evaluation criteria, default "accuracy, completeness, clarity"

**Implementation Logic**:
```
1. 获取上游输出
2. 对于每次尝试（0到max_retries次）：
   a. 将输出和条件发送给评估器LLM
   b. 解析结果：{score: 8.5, passed: true, feedback: "...", strengths: "..."}
   c. 如果分数大于或等于阈值 → 返回结果
   d. 如果达到最大重试次数 → 返回最佳尝试结果
   e. 否则 → 使用包含反馈的增强查询重新执行源节点
```

**Enhanced Query Format for Retries**:
```
[原始查询]

[改进反馈 - 第2/3次尝试]：
分数：5.5/10（需要达到7.0/10）
问题：缺少具体示例
优点：结构和流程良好
请根据上述反馈改进你的响应。

```

---

## Upgrade #4: ROUTER — Intelligent Branching

LLM analyzes query and selects the optimal downstream node to execute, skipping all others.

**Parameters**:
- `routes` (str): Comma-separated "alias:description" pairs
- `strategy` (str): "single" or "multi", default "single"

**Critical Skip Logic** (required for performance — 10x speedup):

Two parts must be implemented:

**Part 1 — Main execution loop check**:
```python
for node_alias in execution_order:
    if node_alias in ctx.node_outputs:
        ctx.log("SYSTEM", "INFO", f"跳过 {node_alias}（已执行）")
        continue
    # ... 正常执行节点
```

**Part 2 — Router marks unselected routes**:
```python
# 在执行选中的路径后：
for route_alias in route_map:
    if route_alias not in selected:
        ctx.node_outputs[route_alias] = {"skipped_by_router": True, "response": "")
```

**Result**: Query "What is 15% tip on $85.50?" routes to calculator node in 2.3s instead of executing all 3 routes in 21s.

---

## Upgrade #5: ENSEMBLE — Mixture of Agents

Runs the same query through multiple AI personas in parallel, then synthesizes the best elements into a superior response.

**Parameters**:
- `agents` (str): Comma-separated "alias:persona" pairs
- `synthesize` (str): "true" (default) or "false" to return all
- `model` (str): Agent model, default "gpt-4o-mini"
- `synth_model` (str): Synthesizer model

**Safety**: MAX_ENSEMBLE_AGENTS = 7

**Implementation Pattern**:
```python
async def _execute_ensemble(self, ctx, node, data):
    # 1. 解析代理
    agents = parse_agents(node.params.get("agents", ""))
    
    # 2. 并行运行所有代理
    async def run_agent(alias, persona):
        response = await self.openai_client.chat.completions.create(
            model=agent_model,
            messages=[
                {"role": "system", "content": f"你是：{persona}. 请从你的独特视角回答。"},
                {"role": "user", "content": query}
            ],
            temperature=0.8  # 为了多样性设置较高的温度值
        )
        return {"alias": alias, "response": response.choices[0].message.content}
    
    results = await asyncio.gather(*[run_agent(a, p) for a, p in agents])
    
    # 3. 合成结果
    synthesis = await self.openai_client.chat.completions.create(
        model=synth_model,
        messages=[{"role": "user", "content": f"结合来自：{results}的最佳见解"}],
        temperature=0.5
    )
    return {"response": synthesis.choices[0].message.content, "node_type": "ensemble"}
```

**Real Test**: Moussaka recipe with French Chef + Greek Grandmother + Molecular Scientist = superior unified recipe.

---

## Upgrade #6: MEMORY — Persistent State

File-based JSON storage for data that persists across flow executions.

**Parameters**:
- `namespace` (str): Memory bucket, default "default"
- `action` (str): "store", "recall", "search", "clear", "auto"
- `key` (str): Storage key, or LLM auto-extracts one
- `ttl` (str): Hours until expiry, "0" = forever

**Storage Format** (`memory_store/{namespace}.json`):
```json
{
  "diet": {
    "value": "我是素食者，对坚果过敏",
    "_ts": 1708502400.0,
    "_query": "我是素食者，对坚果过敏"
  }
}
```

**Actions**:
- `store` — Save upstream response or query with key
- `recall` — Return specific key or all entries as context
- `search` — LLM semantic search over stored entries
- `clear` — Delete key or entire namespace
- `auto` — LLM decides whether to store or recall based on context

---

## Upgrade #7: TOOL — External API Access

Call any REST API from within a flow with safety limits.

**Parameters**:
- `url` (str): API endpoint (supports `{query}` placeholder)
- `method` (str): GET, POST, PUT, DELETE (default: GET)
- `headers` (str): JSON string of HTTP headers
- `body` (str): Request body template
- `extract` (str): Dot-notation for JSON extraction (e.g., "data.items.0.name")
- `timeout` (str): Seconds, default 10, max 30

**Safety Limits**:
```python
TOOL_BLOCKED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "169.254.169.254", "10.", "192.168."]
TOOL_MAX_RESPONSE = 50000  # 字符数限制
TOOL_TIMEOUT = 10  # 时间限制，最大为30秒
```

**Use httpx** (not aiohttp — more commonly available in Docker/FastAPI environments):
```python
async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
    resp = await client.request(method, url, headers=headers)
```

**CRITICAL PARSER FIX**: Comment regex `//.*$` strips URLs. Must add negative lookbehind:
```python
# 之前的代码：`r'//.*?$|/\*.*?\*/` — 会破坏HTTPS链接
# 修改后的代码：`r'(?<!:)//.*?$|/\*.*?\*/` — 保护`://协议
```

---

## Upgrade #8: LOOP — Iterative Execution

Repeat any target node over multiple items with collect or chain modes.

**Parameters**:
- `over` (str): Pipe-separated items (e.g., "Italian|Greek|Japanese") or "count:5"
- `target` (str): Node alias to execute each iteration
- `max` (str): Safety cap, default 10, hard limit 20
- `mode` (str): "collect" (gather all) or "chain" (each feeds into next)

**IMPORTANT**: Use `|` as separator, NOT `,` — the parser splits on commas for param separation.

**Implementation**:
```python
for i, item in enumerate(items):
    iter_query = f"{query}\n\n项目 ({i+1}/{len(items)}: {item}"
    
    # 清除之前的输出，以便重新执行目标节点
    if target_alias in ctx.node_outputs:
        del ctx.node_outputs[target_alias]
    
    await self._execute_node(ctx, target_node)
    result = ctx.node_outputs.get(target_alias,{})
    results.append(result)

# 标记目标节点为循环执行的结果
ctx.node_outputs[target_alias] = {"executed_by_loop": True}
```

**Real Test**: "Give me a signature dish recipe" looped over Italian|Greek|Japanese = 3 unique recipes.

---

## Upgrade #9: TRANSFORM — Smart Data Reshaping

Reshapes data between nodes in 4 modes. The "glue" that makes complex pipelines work.

**Parameters**:
- `mode` (str): "llm" (default), "template", "extract", "format"
- `template` (str): String with `{NodeAlias}` and `{NodeAlias.field.subfield}` placeholders
- `extract` (str): Dot-path for JSON extraction
- `format` (str): Output as "json", "csv", "markdown", "text"
- `instruction` (str): Custom LLM instruction (underscores become spaces)

**Mode Details**:
- **template**: `Bitcoin: {T.bitcoin.usd} USD` → `Bitcoin: 67884 USD` (2 nesting levels)
- **extract**: `data.items.0.name` navigates JSON tree
- **format**: Converts JSON arrays to CSV or markdown tables
- **llm**: LLM intelligently reformats (temp 0.3 for precision)

**Real Test**: TOOL fetches Bitcoin price JSON → TRANSFORM summarizes = "The current price of Bitcoin is $67,861 USD" in 0.9s.

---

## Upgrade #10: PARALLEL — Concurrent Execution

Run multiple independent nodes at the same time for massive speedup.

**Parameters**:
- `targets` (str): Pipe-separated node aliases (e.g., "A|B|C")
- `merge` (str): "combine" (concatenate), "best" (longest response), "json" (structured)

**Safety**: MAX_PARALLEL_TASKS = 10

**Critical Fix**: `_execute_node()` stores results in `ctx.node_outputs` but may not return them directly. Always read from context:
```python
# 错误的做法：结果可能为空：
result = await self._execute_node(ctx, target_node)

# 正确的做法：始终从上下文中获取结果：
await self._execute_node(ctx, target_node)
result = ctx.node_outputs.get(alias,{})
```

**Real Test**: 3 CoinGecko API calls (ping + BTC price + ETH price) completed in 0.2s parallel vs ~3s sequential.

---

## Common Debugging Patterns

### Problem: Duplicate Method — Old Stub Wins
**Symptom**: New method exists but old logic runs.
**Cause**: Python uses LAST definition. Old stub at line 1800 overrides new method at line 650.
**Fix**: `grep -c "async def _execute_X" runtime.py` — if > 1, delete the old one.

### Problem: URL Gets Stripped to "https:"
**Symptom**: TOOL node sends `https:` instead of `https://api.example.com`
**Cause**: Comment regex `//.*$` matches `//` in URLs.
**Fix**: `(?<!:)//.*?$` — negative lookbehind for colon.

### Problem: Nodes Run After Router Selects
**Symptom**: Router picks node B but A and C also execute (21s instead of 2.3s).
**Fix**: Add skip check in main loop + mark unselected routes in ctx.node_outputs.

### Problem: Parameters Merge Together
**Symptom**: `namespace=prefs action=store` becomes `{'namespace': 'prefs action=store'}`
**Fix**: Parser must split on space too: `elif char in (',', ' ') and not in_quotes:`

### Problem: Empty Results from Parallel/Loop
**Symptom**: Node executes (logs show success) but calling node gets empty result.
**Fix**: Read from `ctx.node_outputs.get(alias)` instead of `_execute_node()` return value.

### Problem: Module Not Found in Docker
**Symptom**: `No module named 'aiohttp'`
**Fix**: Use `httpx` (ships with FastAPI/Starlette). Check: `docker exec container python3 -c "import httpx"`

---

## Deployment Checklist
```bash
# 1. 在进行任何更改之前备份文件
cp runtime.py runtime.py.backup_$(date +%Y%m%d_%H%M%S)

# 2. 将节点类型添加到解析器枚举中
sed -i '/LAST_TYPE = "last"/a\    NEW_TYPE = "new_type"' parser.py

# 3. 将调度逻辑和方法添加到运行时代码中
python3 << 'PYEOF'
# ... 其他修补脚本
PYEOF

# 4. 验证Python语法
python3 -c "import ast; ast.parse(open('runtime.py').read()); print('语法正确')"
python3 -c "import ast; ast.parse(open('parser.py').read()); print('解析器正确')"

# 5. 检查重复项
grep -c "async def _execute_new_type" runtime.py  # 确保该方法只存在一次

# 6. 构建并部署
docker compose up -d --build backend && sleep 12

# 7. 检查启动情况
docker logs container_name 2>&1 | tail -5

# 8. 使用最小流程进行测试
curl -s -X POST https://api.example.com/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "flow Test { ... }", "query": "test"}'

# 9. 提交更改
git add parser.py runtime.py
git commit -m "升级N：节点类型 — 描述"
git push origin main
```

## Testing Pattern

Every upgrade should be tested with a minimal isolated flow:
```
flow TestNodeType {
  input text query;
  node X: <node_type> <params>;
  query -> X;
  output text result from X;
}
```

Then test in combination with other nodes:
```
flow Pipeline {
  input text query;
  node T: tool url=https://api.example.com method=GET;
  node X: transform mode=llm instruction=Summarize;
  query -> T -> X;
  output text result from X;
}
```

## 安全性总结

| 节点 | 限制 | 值         |
|------|---------|------------|
| code_interpreter | 执行超时 | 5秒         |
| code_interpreter | 禁止的操作 | 10个操作被禁止 |
| critique | 最大重试次数 | 3次（上限）     |
| ensemble | 最大代理数量 | 7个         |
| memory | 最大输入长度 | 5000个字符     |
| tool | 响应大小限制 | 50KB        |
| tool | 超时设置 | 默认10秒，最大30秒    |
| tool | 受限制的主机 | 私有IP地址、localhost |
| loop | 最大迭代次数 | 20次         |
| parallel | 最大任务数量 | 10个         |

## 致谢

这些升级由Hlia（来自Kitchen to Code团队）在AetherLang Omega平台上开发完成。灵感来源于Andrej Karpathy的AI代理架构理念，并在neurodoc.app上通过真实API流量进行了生产环境测试。
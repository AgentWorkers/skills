---
name: "agent-workflow-designer"
description: "**Agent Workflow Designer**  
（代理工作流设计器）  
**简介：**  
Agent Workflow Designer 是一款专为软件开发人员设计的工具，用于构建和优化代理（agent）的工作流程。它提供了直观的图形化界面，帮助用户轻松设计复杂的任务执行顺序，确保代理能够高效地处理各种业务逻辑。该工具支持自定义任务节点、设置条件分支、配置通信协议等，从而提升系统的灵活性和可扩展性。  
**主要功能：**  
1. **图形化界面**：通过拖放操作即可创建和修改工作流图，无需编写繁琐的代码。  
2. **任务节点**：支持多种类型的任务节点，如数据采集、处理、存储、发送等。  
3. **条件分支**：允许用户根据预设条件或运行时结果来决定任务的执行路径。  
4. **通信协议**：支持多种通信协议，如 HTTP、TCP/UDP 等，便于集成不同的外部服务。  
5. **日志记录**：详细记录每个任务的执行过程和结果，便于调试和监控。  
6. **版本控制**：支持版本管理，方便团队成员协作和回溯版本。  
7. **自动化脚本**：支持编写自动化脚本，实现工作流的自动化执行。  
**应用场景：**  
- **自动化测试**：用于自动化执行测试用例，提高测试效率。  
- **数据处理**：用于处理大量数据，如数据清洗、分析等。  
- **消息传递**：用于在不同系统之间传递消息。  
- **任务调度**：用于定时或异步执行任务。  
**优势：**  
- **易用性**：图形化界面，非技术人员也能快速上手。  
- **灵活性**：高度可定制，满足各种业务需求。  
- **可靠性**：支持错误处理和重试机制，确保任务顺利完成。  
- **可扩展性**：易于扩展，支持未来功能的添加。  
**下载与安装：**  
您可以从官方网站下载 Agent Workflow Designer 并进行安装。安装过程简单快捷，只需按照提示操作即可。  
**了解更多：**  
访问我们的官方网站，了解更多关于 Agent Workflow Designer 的详细信息和产品文档。"
---
# 代理工作流设计器

**级别：** 高级  
**类别：** 工程  
**领域：** 多代理系统 / 人工智能编排  

---

## 概述  

用于设计生产级多代理编排系统。涵盖五种核心模式（顺序流水线、并行扩展/收缩、分层委托、事件驱动、共识机制），以及特定平台的实现方式、任务交接协议、状态管理、错误恢复、上下文窗口预算管理和成本优化策略。  

---

## 核心功能  

- 适用于任何编排需求的模式选择指南  
- 任务交接协议模板（结构化上下文传递）  
- 多代理工作流的状态管理机制  
- 错误恢复与重试策略  
- 上下文窗口预算管理  
- 针对不同平台的成本优化策略  
- 特定平台的配置支持：Claude Code Agent Teams、OpenClaw、CrewAI、AutoGen  

---

## 使用场景  

- 构建超出单个代理处理能力的多步骤人工智能流程  
- 为提高效率而并行化研究、生成或分析任务  
- 创建具有明确角色和交接协议的专用代理  
- 设计可容错的生产环境中的人工智能工作流  

---

## 模式选择指南  

```
Is the task sequential (each step needs previous output)?
  YES → Sequential Pipeline
  NO  → Can tasks run in parallel?
          YES → Parallel Fan-out/Fan-in
          NO  → Is there a hierarchy of decisions?
                  YES → Hierarchical Delegation
                  NO  → Is it event-triggered?
                          YES → Event-Driven
                          NO  → Need consensus/validation?
                                  YES → Consensus Pattern
```  

---

## 模式 1：顺序流水线  

**适用场景：** 每个步骤都依赖于前一步的输出。例如：研究 → 草稿 → 审查 → 优化。  

```python
# sequential_pipeline.py
from dataclasses import dataclass
from typing import Callable, Any
import anthropic

@dataclass
class PipelineStage:
    name: "str"
    system_prompt: str
    input_key: str      # what to take from state
    output_key: str     # what to write to state
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 2048

class SequentialPipeline:
    def __init__(self, stages: list[PipelineStage]):
        self.stages = stages
        self.client = anthropic.Anthropic()
    
    def run(self, initial_input: str) -> dict:
        state = {"input": initial_input}
        
        for stage in self.stages:
            print(f"[{stage.name}] Processing...")
            
            stage_input = state.get(stage.input_key, "")
            
            response = self.client.messages.create(
                model=stage.model,
                max_tokens=stage.max_tokens,
                system=stage.system_prompt,
                messages=[{"role": "user", "content": stage_input}],
            )
            
            state[stage.output_key] = response.content[0].text
            state[f"{stage.name}_tokens"] = response.usage.input_tokens + response.usage.output_tokens
            
            print(f"[{stage.name}] Done. Tokens: {state[f'{stage.name}_tokens']}")
        
        return state

# Example: Blog post pipeline
pipeline = SequentialPipeline([
    PipelineStage(
        name="researcher",
        system_prompt="You are a research specialist. Given a topic, produce a structured research brief with: key facts, statistics, expert perspectives, and controversy points.",
        input_key="input",
        output_key="research",
    ),
    PipelineStage(
        name="writer",
        system_prompt="You are a senior content writer. Using the research provided, write a compelling 800-word blog post with a clear hook, 3 main sections, and a strong CTA.",
        input_key="research",
        output_key="draft",
    ),
    PipelineStage(
        name="editor",
        system_prompt="You are a copy editor. Review the draft for: clarity, flow, grammar, and SEO. Return the improved version only, no commentary.",
        input_key="draft",
        output_key="final",
    ),
])
```  

---

## 模式 2：并行扩展/收缩  

**适用场景：** 可以同时运行的独立任务。例如：同时研究5个竞争对手的信息。  

```python
# parallel_fanout.py
import asyncio
import anthropic
from typing import Any

async def run_agent(client, task_name: "str-system-str-user-str-model-str"claude-3-5-sonnet-20241022") -> dict:
    """Single async agent call"""
    loop = asyncio.get_event_loop()
    
    def _call():
        return client.messages.create(
            model=model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    
    response = await loop.run_in_executor(None, _call)
    return {
        "task": task_name,
        "output": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens,
    }

async def parallel_research(competitors: list[str], research_type: str) -> dict:
    """Fan-out: research all competitors in parallel. Fan-in: synthesize results."""
    client = anthropic.Anthropic()
    
    # FAN-OUT: spawn parallel agent calls
    tasks = [
        run_agent(
            client,
            task_name=competitor,
            system=f"You are a competitive intelligence analyst. Research {competitor} and provide: pricing, key features, target market, and known weaknesses.",
            user=f"Analyze {competitor} for comparison with our product in the {research_type} market.",
        )
        for competitor in competitors
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle failures gracefully
    successful = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    if failed:
        print(f"Warning: {len(failed)} research tasks failed: {failed}")
    
    # FAN-IN: synthesize
    combined_research = "\n\n".join([
        f"## {r['task']}\n{r['output']}" for r in successful
    ])
    
    synthesis = await run_agent(
        client,
        task_name="synthesizer",
        system="You are a strategic analyst. Synthesize competitor research into a concise comparison matrix and strategic recommendations.",
        user=f"Synthesize these competitor analyses:\n\n{combined_research}",
        model="claude-3-5-sonnet-20241022",
    )
    
    return {
        "individual_analyses": successful,
        "synthesis": synthesis["output"],
        "total_tokens": sum(r["tokens"] for r in successful) + synthesis["tokens"],
    }
```  

---

## 模式 3：分层委托  

**适用场景：** 包含子任务的复杂任务。编排器将工作分解并委托给专业代理处理。  

```python
# hierarchical_delegation.py
import json
import anthropic

ORCHESTRATOR_SYSTEM = """You are an orchestration agent. Your job is to:
1. Analyze the user's request
2. Break it into subtasks
3. Assign each to the appropriate specialist agent
4. Collect results and synthesize

Available specialists:
- researcher: finds facts, data, and information
- writer: creates content and documents  
- coder: writes and reviews code
- analyst: analyzes data and produces insights

Respond with a JSON plan:
{
  "subtasks": [
    {"id": "1", "agent": "researcher", "task": "...", "depends_on": []},
    {"id": "2", "agent": "writer", "task": "...", "depends_on": ["1"]}
  ]
}"""

SPECIALIST_SYSTEMS = {
    "researcher": "You are a research specialist. Find accurate, relevant information and cite sources when possible.",
    "writer": "You are a professional writer. Create clear, engaging content in the requested format.",
    "coder": "You are a senior software engineer. Write clean, well-commented code with error handling.",
    "analyst": "You are a data analyst. Provide structured analysis with evidence-backed conclusions.",
}

class HierarchicalOrchestrator:
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def run(self, user_request: str) -> str:
        # 1. Orchestrator creates plan
        plan_response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=ORCHESTRATOR_SYSTEM,
            messages=[{"role": "user", "content": user_request}],
        )
        
        plan = json.loads(plan_response.content[0].text)
        results = {}
        
        # 2. Execute subtasks respecting dependencies
        for subtask in self._topological_sort(plan["subtasks"]):
            context = self._build_context(subtask, results)
            specialist = SPECIALIST_SYSTEMS[subtask["agent"]]
            
            result = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=specialist,
                messages=[{"role": "user", "content": f"{context}\n\nTask: {subtask['task']}"}],
            )
            results[subtask["id"]] = result.content[0].text
        
        # 3. Final synthesis
        all_results = "\n\n".join([f"### {k}\n{v}" for k, v in results.items()])
        synthesis = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system="Synthesize the specialist outputs into a coherent final response.",
            messages=[{"role": "user", "content": f"Original request: {user_request}\n\nSpecialist outputs:\n{all_results}"}],
        )
        return synthesis.content[0].text
    
    def _build_context(self, subtask: dict, results: dict) -> str:
        if not subtask.get("depends_on"):
            return ""
        deps = [f"Output from task {dep}:\n{results[dep]}" for dep in subtask["depends_on"] if dep in results]
        return "Previous results:\n" + "\n\n".join(deps) if deps else ""
    
    def _topological_sort(self, subtasks: list) -> list:
        # Simple ordered execution respecting depends_on
        ordered, remaining = [], list(subtasks)
        completed = set()
        while remaining:
            for task in remaining:
                if all(dep in completed for dep in task.get("depends_on", [])):
                    ordered.append(task)
                    completed.add(task["id"])
                    remaining.remove(task)
                    break
        return ordered
```  

---

## 任务交接协议模板  

```python
# Standard handoff context format — use between all agents
@dataclass
class AgentHandoff:
    """Structured context passed between agents in a workflow."""
    task_id: str
    workflow_id: str
    step_number: int
    total_steps: int
    
    # What was done
    previous_agent: str
    previous_output: str
    artifacts: dict  # {"filename": "content"} for any files produced
    
    # What to do next
    current_agent: str
    current_task: str
    constraints: list[str]  # hard rules for this step
    
    # Metadata
    context_budget_remaining: int  # tokens left for this agent
    cost_so_far_usd: float
    
    def to_prompt(self) -> str:
        return f"""
# Agent Handoff — Step {self.step_number}/{self.total_steps}

## Your Task
{self.current_task}

## Constraints
{chr(10).join(f'- {c}' for c in self.constraints)}

## Context from Previous Step ({self.previous_agent})
{self.previous_output[:2000]}{"... [truncated]" if len(self.previous_output) > 2000 else ""}

## Context Budget
You have approximately {self.context_budget_remaining} tokens remaining. Be concise.
"""
```  

---

## 错误恢复策略  

```python
import time
from functools import wraps

def with_retry(max_attempts=3, backoff_seconds=2, fallback_model=None):
    """Decorator for agent calls with exponential backoff and model fallback."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        wait = backoff_seconds * (2 ** attempt)
                        print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
                        time.sleep(wait)
                        
                        # Fall back to cheaper/faster model on rate limit
                        if fallback_model and "rate_limit" in str(e).lower():
                            kwargs["model"] = fallback_model
            raise last_error
        return wrapper
    return decorator

@with_retry(max_attempts=3, fallback_model="claude-3-haiku-20240307")
def call_agent(model, system, user):
    ...
```  

---

## 上下文窗口预算管理  

```python
# Budget context across a multi-step pipeline
# Rule: never let any step consume more than 60% of remaining budget

CONTEXT_LIMITS = {
    "claude-3-5-sonnet-20241022": 200_000,
    "gpt-4o": 128_000,
}

class ContextBudget:
    def __init__(self, model: str, reserve_pct: float = 0.2):
        total = CONTEXT_LIMITS.get(model, 128_000)
        self.total = total
        self.reserve = int(total * reserve_pct)  # keep 20% as buffer
        self.used = 0
    
    @property
    def remaining(self):
        return self.total - self.reserve - self.used
    
    def allocate(self, step_name: "str-requested-int-int"
        allocated = min(requested, int(self.remaining * 0.6))  # max 60% of remaining
        print(f"[Budget] {step_name}: allocated {allocated:,} tokens (remaining: {self.remaining:,})")
        return allocated
    
    def consume(self, tokens_used: int):
        self.used += tokens_used

def truncate_to_budget(text: str, token_budget: int, chars_per_token: float = 4.0) -> str:
    """Rough truncation — use tiktoken for precision."""
    char_budget = int(token_budget * chars_per_token)
    if len(text) <= char_budget:
        return text
    return text[:char_budget] + "\n\n[... truncated to fit context budget ...]"
```  

---

## 成本优化策略  

| 策略 | 节省成本 | 相关权衡 |
|---|---|---|
| 使用“俳句”（Haiku）进行路由/分类 | 85-90% | 判断过程略显粗糙 |
| 缓存重复的系统提示 | 50-90% | 需要设置提示缓存机制 |
| 截断中间输出 | 20-40% | 可能导致信息丢失 |
| 批量处理相似任务 | 50% | 会增加延迟 |
| 对于大部分步骤使用“十四行诗”（Sonnet），仅对最终步骤使用“歌剧”（Opus） | 60-70% | 可能提升最终质量 |
| 在达到置信度阈值时跳过某些步骤 | 30-50% | 需要设置置信度评分机制 |

---

## 常见问题  

- **循环依赖** — 代理之间相互调用；设计时需确保任务遵循有向无环图（DAG）结构  
- **上下文信息泄露** — 将所有之前的输出传递给每个步骤；仅传递必要的信息  
- **无超时机制** — 单个代理卡住会导致整个流程停滞；务必设置最大令牌数和定时超时  
- **隐蔽性错误** — 代理返回看似合理但错误的输出；关键路径需添加验证步骤  
- **忽略成本因素** — 并行处理多个任务会增加成本；模型选择是一个重要的成本决策  
- **过度编排** — 如果单个提示即可完成任务，则无需添加额外代理；仅在确实必要时添加代理
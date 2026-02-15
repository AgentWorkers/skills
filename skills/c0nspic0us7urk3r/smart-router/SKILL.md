---
name: smart-router
description: >
  Expertise-aware model router with semantic domain scoring, context-overflow protection,
  and security redaction. Automatically selects the optimal AI model using weighted
  expertise scoring (Feb 2026 benchmarks). Supports Claude, GPT, Gemini, Grok with
  automatic fallback chains, HITL gates, and cost optimization.
author: c0nSpIc0uS7uRk3r
version: 2.1.0
license: MIT
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["ANTHROPIC_API_KEY"]
    optional_env: ["GOOGLE_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY"]
  features:
    - Semantic domain detection
    - Expertise-weighted scoring (0-100)
    - Risk-based mandatory routing
    - Context overflow protection (>150K → Gemini)
    - Security credential redaction
    - Circuit breaker with persistent state
    - HITL gate for low-confidence routing
  benchmarks:
    source: "Feb 2026 MLOC Analysis"
    models:
      - "Claude Opus 4.5: SWE-bench 80.9%"
      - "GPT-5.2: AIME 100%, Control Flow 22 errors/MLOC"
      - "Gemini 3 Pro: Concurrency 69 issues/MLOC"
---

# 人工智能智能路由器

该路由器能够通过分层分类机制智能地将请求路由到最合适的AI模型，并具备自动回退处理和成本优化功能。

## 工作原理（默认为静默模式）

路由器以透明方式运行：用户正常发送请求，系统会从最适合该请求的模型中获取响应，无需使用任何特殊指令。

**可选功能：** 在任何请求中添加 `[show routing]` 可以查看路由决策过程。

## 分层分类系统

路由器采用三层决策流程：

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 1: INTENT DETECTION                      │
│  Classify the primary purpose of the request                     │
├─────────────────────────────────────────────────────────────────┤
│  CODE        │ ANALYSIS    │ CREATIVE   │ REALTIME  │ GENERAL   │
│  write/debug │ research    │ writing    │ news/live │ Q&A/chat  │
│  refactor    │ explain     │ stories    │ X/Twitter │ translate │
│  review      │ compare     │ brainstorm │ prices    │ summarize │
└──────┬───────┴──────┬──────┴─────┬──────┴─────┬─────┴─────┬─────┘
       │              │            │            │           │
       ▼              ▼            ▼            ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TIER 2: COMPLEXITY ESTIMATION                   │
├─────────────────────────────────────────────────────────────────┤
│  SIMPLE (Tier $)        │ MEDIUM (Tier $$)    │ COMPLEX (Tier $$$)│
│  • One-step task        │ • Multi-step task   │ • Deep reasoning  │
│  • Short response OK    │ • Some nuance       │ • Extensive output│
│  • Factual lookup       │ • Moderate context  │ • Critical task   │
│  → Haiku/Flash          │ → Sonnet/Grok/GPT   │ → Opus/GPT-5      │
└──────────────────────────┴─────────────────────┴───────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                TIER 3: SPECIAL CASE OVERRIDES                    │
├─────────────────────────────────────────────────────────────────┤
│  CONDITION                           │ OVERRIDE TO              │
│  ─────────────────────────────────────┼─────────────────────────│
│  Context >100K tokens                │ → Gemini Pro (1M ctx)    │
│  Context >500K tokens                │ → Gemini Pro ONLY        │
│  Needs real-time data                │ → Grok (regardless)      │
│  Image/vision input                  │ → Opus or Gemini Pro     │
│  User explicit override              │ → Requested model        │
└──────────────────────────────────────┴──────────────────────────┘
```

## 意图检测模式

### **代码相关意图**
- 关键词：write（编写）、code（代码）、debug（调试）、fix（修复）、refactor（重构）、implement（实现）、function（函数）、class（类）、script（脚本）、API（应用程序编程接口）、bug（错误）、error（错误）、compile（编译）、test（测试）、PR（代码提交）、commit（提交）
- 常见的文件扩展名：.py、.js、.ts、.go、.rs、.java 等
- 输入中包含代码块

### **分析相关意图**
- 关键词：analyze（分析）、explain（解释）、compare（比较）、research（研究）、understand（理解）、why（为什么）、how does（...是如何工作的）、evaluate（评估）、assess（评估）、review（审查）、investigate（调查）、examine（检查）
- 长篇幅的问题
- “Help me understand...”（帮我理解...）

### **创作相关意图**
- 关键词：write（编写故事/诗歌/文章）、create（创作）、brainstorm（头脑风暴）、imagine（想象）、design（设计）、draft（草拟）、compose（创作）
- 与虚构内容或叙事相关的请求

### **实时相关意图**
- 关键词：now（现在）、today（今天）、current（当前的）、latest（最新的）、trending（热门的）、news（新闻）、happening（正在发生的）、live（实时的）、price（价格）、score（分数）、weather（天气）
- X/Twitter上的提及
- 股票/加密货币行情
- 体育比分

### **通用意图（默认）**
- 简单的问答
- 翻译
- 摘要
- 对话式交流

### **混合意图（检测到多种意图）**
- 如果一个请求包含多种明确的意图（例如：“编写代码来分析这些数据，并对其进行创造性解释”）：
  1. **确定主要意图**：核心任务是什么？
  2. **路由到能力最强的模型**：混合任务需要多种功能
  3. **默认选择复杂度较高的模型**：多种意图通常意味着需要多步骤的处理

**示例：**
- “编写代码并解释其工作原理” → 路由到 Opus 模型
- “总结这个内容并告诉我最新的相关新闻” → 优先选择 Grok 模型
- “根据当前事件创作一个故事” → 优先选择 Grok 模型（实时处理）

## 语言处理

**非英语请求** 也能被正常处理——所有支持的模型都具备多语言支持能力：

| 模型 | 支持的语言数量 |
|-------|---------------------|
| Opus/Sonnet/Haiku | 超过100种语言 |
| GPT-5 | 超过100种语言 |
| Gemini Pro/Flash | 超过100种语言 |
| Grok | 支持主要语言 |

**意图检测仍然有效**，因为：
- 关键词模式包含常见的非英语词汇对应词
- 代码意图可以通过文件扩展名和代码块来识别（与语言无关）
- 任务复杂度可以通过查询长度来估计（适用于多种语言）

**特殊情况：** 如果由于语言问题导致意图不明确，系统会默认选择 **通用意图** 并使用中等复杂度的模型。

## 复杂度判断

### **简单任务（$）**
- 短查询（少于50个单词）
- 单个问号
- “快速回答”、“简单说明”
- 是/否格式的问答
- 单位转换、定义等简单操作

### **中等复杂度（$$）**
- 中等长度的查询（50-200个单词）
- 需要处理多个方面
- “解释”、“描述”、“比较”等操作
- 提供了一些上下文信息

### **复杂任务（$$$）**
- 长查询（超过200个单词）或复杂的任务
- 需要“逐步说明”、“详细解释”
- 多部分组成的问题
- 包含关键/重要的信息
- 需要研究、分析或创造性的工作

## 路由表

| 意图 | 简单 | 中等 | 复杂 |
|--------|--------|--------|---------|
| **代码** | Sonnet | Opus | Opus |
| **分析** | Flash | GPT-5 | Opus |
| **创作** | Sonnet | Opus | Opus |
| **实时** | Grok | Grok | Grok-3 |
| **通用** | Flash | Sonnet | Opus |

## 令牌耗尽与模型自动切换

当某个模型在会话过程中因令牌耗尽、达到速率限制或出现API错误而无法使用时，路由器会自动切换到下一个可用的模型，并**通知用户**。

### 通知格式

当模型切换时，用户会收到以下通知：

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️ MODEL SWITCH NOTICE                                         │
│                                                                  │
│  Your request could not be completed on claude-opus-4-5         │
│  (reason: token quota exhausted).                               │
│                                                                  │
│  ✅ Request completed using: anthropic/claude-sonnet-4-5        │
│                                                                  │
│  The response below was generated by the fallback model.        │
└─────────────────────────────────────────────────────────────────┘
```

### 切换原因

| 原因 | 说明 |
|--------|-------------|
| **令牌耗尽** | 达到每日/每月的令牌使用限制 |
| **速率限制超出** | 每分钟请求次数过多 |
| **输入内容超出模型处理范围** | 输入内容超出模型处理能力 |
| **API超时** | 模型响应时间过长 |
| **API错误** | 提供者返回错误 |
| **模型暂时不可用** | 模型处于离线状态 |

### 实现细节

```python
def execute_with_fallback(primary_model: str, fallback_chain: list[str], request: str) -> Response:
    """
    Execute request with automatic fallback and user notification.
    """
    attempted_models = []
    switch_reason = None
    
    # Try primary model first
    models_to_try = [primary_model] + fallback_chain
    
    for model in models_to_try:
        try:
            response = call_model(model, request)
            
            # If we switched models, prepend notification
            if attempted_models:
                notification = build_switch_notification(
                    failed_model=attempted_models[0],
                    reason=switch_reason,
                    success_model=model
                )
                return Response(
                    content=notification + "\n\n---\n\n" + response.content,
                    model_used=model,
                    switched=True
                )
            
            return Response(content=response.content, model_used=model, switched=False)
            
        except TokenQuotaExhausted:
            attempted_models.append(model)
            switch_reason = "token quota exhausted"
            log_fallback(model, switch_reason)
            continue
            
        except RateLimitExceeded:
            attempted_models.append(model)
            switch_reason = "rate limit exceeded"
            log_fallback(model, switch_reason)
            continue
            
        except ContextWindowExceeded:
            attempted_models.append(model)
            switch_reason = "context window exceeded"
            log_fallback(model, switch_reason)
            continue
            
        except APITimeout:
            attempted_models.append(model)
            switch_reason = "API timeout"
            log_fallback(model, switch_reason)
            continue
            
        except APIError as e:
            attempted_models.append(model)
            switch_reason = f"API error: {e.code}"
            log_fallback(model, switch_reason)
            continue
    
    # All models exhausted
    return build_exhaustion_error(attempted_models)


def build_switch_notification(failed_model: str, reason: str, success_model: str) -> str:
    """Build user-facing notification when model switch occurs."""
    return f"""⚠️ **MODEL SWITCH NOTICE**

Your request could not be completed on `{failed_model}` (reason: {reason}).

✅ **Request completed using:** `{success_model}`

The response below was generated by the fallback model."""


def build_exhaustion_error(attempted_models: list[str]) -> Response:
    """Build error when all models are exhausted."""
    models_tried = ", ".join(attempted_models)
    return Response(
        content=f"""❌ **REQUEST FAILED**

Unable to complete your request. All available models have been exhausted.

**Models attempted:** {models_tried}

**What you can do:**
1. **Wait** — Token quotas typically reset hourly or daily
2. **Simplify** — Try a shorter or simpler request
3. **Check status** — Run `/router status` to see model availability

If this persists, your human may need to check API quotas or add additional providers.""",
        model_used=None,
        switched=False,
        failed=True
    )
```

### 令牌耗尽时的回退策略

当某个模型无法使用时，路由器会为 **相同类型的任务** 选择下一个最佳模型：

| 原始模型 | 回退优先级（相同功能） |
|----------------|-------------------------------------|
| Opus | Sonnet → GPT-5 → Grok-3 → Gemini Pro |
| Sonnet | GPT-5 → Grok-3 → Opus → Haiku |
| GPT-5 | Sonnet → Opus → Grok-3 → Gemini Pro |
| Gemini Pro | Flash → GPT-5 → Opus → Sonnet |
| Grok-2/3 | （警告：没有实时可用模型） |

### 用户反馈

模型切换后，系统应在响应中告知用户：
1. 原始模型为何无法使用
2. 实际完成请求的模型是什么
3. 新模型的响应质量可能与原始模型有所不同

这有助于保持用户对系统行为的了解，并帮助用户合理预期结果。

### 流式响应与回退处理

在使用流式响应时，需要特别注意回退机制：

```python
async def execute_with_streaming_fallback(primary_model: str, fallback_chain: list[str], request: str):
    """
    Handle streaming responses with mid-stream fallback.
    
    If a model fails DURING streaming (not before), the partial response is lost.
    Strategy: Don't start streaming until first chunk received successfully.
    """
    models_to_try = [primary_model] + fallback_chain
    
    for model in models_to_try:
        try:
            # Test with non-streaming ping first (optional, adds latency)
            # await test_model_availability(model)
            
            # Start streaming
            stream = await call_model_streaming(model, request)
            first_chunk = await stream.get_first_chunk(timeout=10_000)  # 10s timeout for first chunk
            
            # If we got here, model is responding — continue streaming
            yield first_chunk
            async for chunk in stream:
                yield chunk
            return  # Success
            
        except (FirstChunkTimeout, StreamError) as e:
            log_fallback(model, str(e))
            continue  # Try next model
    
    # All models failed
    yield build_exhaustion_error(models_to_try)
```

**重要提示：** 在显示任何部分响应之前，务必等待第一个响应块完成。如果第一个响应块超时，应立即切换到备用模型。

### 重试策略配置

```python
RETRY_CONFIG = {
    "initial_timeout_ms": 30_000,     # 30s for first attempt
    "fallback_timeout_ms": 20_000,    # 20s for fallback attempts (faster fail)
    "max_retries_per_model": 1,       # Don't retry same model
    "backoff_multiplier": 1.5,        # Not used (no same-model retry)
    "circuit_breaker_threshold": 3,   # Failures before skipping model entirely
    "circuit_breaker_reset_ms": 300_000  # 5 min before trying failed model again
}
```

**故障保护机制：** 如果某个模型在5分钟内失败3次，那么在接下来的5分钟内将不再尝试使用该模型。这样可以避免频繁请求失败的服务。

## 回退机制链

当首选模型出现故障（如达到速率限制、API故障等）时，系统会按顺序切换到下一个可用模型：

### 代码相关任务
```
Opus → Sonnet → GPT-5 → Gemini Pro
```

### 分析相关任务
```
Opus → GPT-5 → Gemini Pro → Sonnet
```

### 创作相关任务
```
Opus → GPT-5 → Sonnet → Gemini Pro
```

### 实时相关任务
```
Grok-2 → Grok-3 → (warn: no real-time fallback)
```

### 通用任务
```
Flash → Haiku → Sonnet → GPT-5
```

### 长篇内容（按长度分层处理）

```
┌─────────────────────────────────────────────────────────────────┐
│                  LONG CONTEXT FALLBACK CHAIN                     │
├─────────────────────────────────────────────────────────────────┤
│  TOKEN COUNT        │ FALLBACK CHAIN                            │
│  ───────────────────┼───────────────────────────────────────────│
│  128K - 200K        │ Opus (200K) → Sonnet (200K) → Gemini Pro  │
│  200K - 1M          │ Gemini Pro → Flash (1M) → ERROR_MESSAGE   │
│  > 1M               │ ERROR_MESSAGE (no model supports this)    │
└─────────────────────┴───────────────────────────────────────────┘
```

### 实现细节

```python
def handle_long_context(token_count: int, available_models: dict) -> str | ErrorMessage:
    """Route long-context requests with graceful degradation."""
    
    # Tier 1: 128K - 200K tokens (Opus/Sonnet can handle)
    if token_count <= 200_000:
        for model in ["opus", "sonnet", "haiku", "gemini-pro", "flash"]:
            if model in available_models and get_context_limit(model) >= token_count:
                return model
    
    # Tier 2: 200K - 1M tokens (only Gemini)
    elif token_count <= 1_000_000:
        for model in ["gemini-pro", "flash"]:
            if model in available_models:
                return model
    
    # Tier 3: > 1M tokens (nothing available)
    # Fall through to error
    
    # No suitable model found — return helpful error
    return build_context_error(token_count, available_models)


def build_context_error(token_count: int, available_models: dict) -> ErrorMessage:
    """Build a helpful error message when no model can handle the input."""
    
    # Find the largest available context window
    max_available = max(
        (get_context_limit(m) for m in available_models),
        default=0
    )
    
    # Determine what's missing
    missing_models = []
    if "gemini-pro" not in available_models and "flash" not in available_models:
        missing_models.append("Gemini Pro/Flash (1M context)")
    if token_count <= 200_000 and "opus" not in available_models:
        missing_models.append("Opus (200K context)")
    
    # Format token count for readability
    if token_count >= 1_000_000:
        token_display = f"{token_count / 1_000_000:.1f}M"
    else:
        token_display = f"{token_count // 1000}K"
    
    return ErrorMessage(
        title="Context Window Exceeded",
        message=f"""Your input is approximately **{token_display} tokens**, which exceeds the context window of all currently available models.

**Required:** Gemini Pro (1M context) {"— currently unavailable" if "gemini-pro" not in available_models else ""}
**Your max available:** {max_available // 1000}K tokens

**Options:**
1. **Wait and retry** — Gemini may be temporarily down
2. **Reduce input size** — Remove unnecessary content to fit within {max_available // 1000}K tokens
3. **Split into chunks** — I can process your input sequentially in smaller pieces

Would you like me to help split this into manageable chunks?""",
        
        recoverable=True,
        suggested_action="split_chunks"
    )
```

**示例错误输出：**

```
⚠️ Context Window Exceeded

Your input is approximately **340K tokens**, which exceeds the context 
window of all currently available models.

Required: Gemini Pro (1M context) — currently unavailable
Your max available: 200K tokens

Options:
1. Wait and retry — Gemini may be temporarily down
2. Reduce input size — Remove unnecessary content to fit within 200K tokens
3. Split into chunks — I can process your input sequentially in smaller pieces

Would you like me to help split this into manageable chunks?
```

## 动态模型选择

路由器会在运行时自动检测可用的模型：

```
1. Check configured auth profiles
2. Build available model list from authenticated providers
3. Construct routing table using ONLY available models
4. If preferred model unavailable, use best available alternative
```

**示例**：如果仅配置了Anthropic和Google模型：
- 代码相关任务 → 优先使用Opus模型（如果Anthropic可用）
- 实时相关任务 → 如果Grok不可用，则切换到Opus模型并提醒用户
- 长篇文档相关任务 → 优先使用Gemini Pro模型（如果Google可用）

## 成本优化

当任务复杂度较低时，系统会考虑成本因素：

| 模型 | 成本等级 | 适用场景 |
|-------|-----------|----------|
| Gemini Flash | 低成本 | 简单任务、高请求量 |
| Claude Haiku | 低成本 | 简单任务、快速响应 |
| Claude Sonnet | 中等成本 | 中等复杂度任务 |
| Grok 2 | 中等成本 | 仅适用于实时任务 |
| GPT-5 | 高成本 | 需要复杂处理的任务 |
| Gemini Pro | 高成本 | 需要长篇内容处理的任务 |

**规则**：对于Flash模型能够处理的任务，切勿使用成本较高的Opus模型。

## 用户控制

### 查看路由决策过程
在请求中添加 `[show routing]` 可以查看路由决策过程：
```
[show routing] What's the weather in NYC?
```
响应中会包含以下信息：
```
[Routed → xai/grok-2-latest | Reason: REALTIME intent detected | Fallback: none available]
```

### 强制使用特定模型
可以通过以下命令强制使用特定模型：
- “use grok: ...” → 强制使用Grok模型
- “use claude: ...” → 强制使用Claude模型
- “use gemini: ...” → 强制使用Gemini Pro模型
- “use flash: ...” → 强制使用Flash模型
- “use gpt: ...” → 强制使用GPT-5模型

### 检查路由器状态
可以通过 “router status” 或 “/router” 命令查看：
- 可用的模型
- 配置的模型
- 当前的路由表
- 最近的路由决策记录

### 实现注意事项

### 代理程序实现

在处理请求时，请注意以下事项：

```
1. DETECT available models (check auth profiles)
2. CLASSIFY intent (code/analysis/creative/realtime/general)
3. ESTIMATE complexity (simple/medium/complex)
4. CHECK special cases (context size, vision, explicit override)
5. FILTER by cost tier based on complexity ← BEFORE model selection
6. SELECT model from filtered pool using routing matrix
7. VERIFY model available, else use fallback chain (also cost-filtered)
8. EXECUTE request with selected model
9. IF failure, try next in fallback chain
10. LOG routing decision (for debugging)
```

### 成本敏感的路由流程（关键步骤）

```python
def route_with_fallback(request):
    """
    Main routing function with CORRECT execution order.
    Cost filtering MUST happen BEFORE routing table lookup.
    """
    
    # Step 1: Discover available models
    available_models = discover_providers()
    
    # Step 2: Classify intent
    intent = classify_intent(request)
    
    # Step 3: Estimate complexity
    complexity = estimate_complexity(request)
    
    # Step 4: Check special-case overrides (these bypass cost filtering)
    if user_override := get_user_model_override(request):
        return execute_with_fallback(user_override, [])  # No cost filter for explicit override
    
    if token_count > 128_000:
        return handle_long_context(token_count, available_models)  # Special handling
    
    if needs_realtime(request):
        return execute_with_fallback("grok-2", ["grok-3"])  # Realtime bypasses cost
    
    # ┌─────────────────────────────────────────────────────────────┐
    # │  STEP 5: FILTER BY COST TIER — THIS MUST COME FIRST!       │
    # │                                                             │
    # │  Cost filtering happens BEFORE the routing table lookup,   │
    # │  NOT after. This ensures "what's 2+2?" never considers     │
    # │  Opus even momentarily.                                    │
    # └─────────────────────────────────────────────────────────────┘
    
    allowed_tiers = get_allowed_tiers(complexity)
    # SIMPLE  → ["$"]
    # MEDIUM  → ["$", "$$"]
    # COMPLEX → ["$", "$$", "$$$"]
    
    cost_filtered_models = {
        model: meta for model, meta in available_models.items()
        if COST_TIERS.get(model) in allowed_tiers
    }
    
    # Step 6: NOW select from cost-filtered pool using routing preferences
    preferences = ROUTING_PREFERENCES.get((intent, complexity), [])
    
    for model in preferences:
        if model in cost_filtered_models:  # Only consider cost-appropriate models
            selected_model = model
            break
    else:
        # No preferred model in cost-filtered pool — use cheapest available
        selected_model = select_cheapest(cost_filtered_models)
    
    # Step 7: Build cost-filtered fallback chain
    task_type = get_task_type(intent, complexity)
    full_chain = MASTER_FALLBACK_CHAINS.get(task_type, [])
    filtered_chain = [m for m in full_chain if m in cost_filtered_models and m != selected_model]
    
    # Step 8-10: Execute with fallback + logging
    return execute_with_fallback(selected_model, filtered_chain)


def get_allowed_tiers(complexity: str) -> list[str]:
    """Return allowed cost tiers for a given complexity level."""
    return {
        "SIMPLE":  ["$"],                      # Budget only — no exceptions
        "MEDIUM":  ["$", "$$"],                # Budget + standard
        "COMPLEX": ["$", "$$", "$$$", "$$$$"], # All tiers — complex tasks deserve the best
    }.get(complexity, ["$", "$$"])


# Example flow for "what's 2+2?":
#
# 1. available_models = {opus, sonnet, haiku, flash, grok-2, ...}
# 2. intent = GENERAL
# 3. complexity = SIMPLE
# 4. (no special cases)
# 5. allowed_tiers = ["$"]  ← SIMPLE means $ only
#    cost_filtered_models = {haiku, flash, grok-2}  ← Opus/Sonnet EXCLUDED
# 6. preferences for (GENERAL, SIMPLE) = [flash, haiku, grok-2, sonnet]
#    first match in cost_filtered = flash ✓
# 7. fallback_chain = [haiku, grok-2]  ← Also cost-filtered
# 8. execute with flash
#
# Result: Opus is NEVER considered, not even momentarily.
```

### 成本优化策略（两种方法）

```
┌─────────────────────────────────────────────────────────────────┐
│           COST OPTIMIZATION IMPLEMENTATION OPTIONS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  APPROACH 1: Explicit filter_by_cost() (shown above)            │
│  ─────────────────────────────────────────────────────────────  │
│  • Calls get_allowed_tiers(complexity) explicitly               │
│  • Filters available_models BEFORE routing table lookup         │
│  • Most defensive — impossible to route wrong tier              │
│  • Recommended for security-critical deployments                │
│                                                                  │
│  APPROACH 2: Preference ordering (implicit)                     │
│  ─────────────────────────────────────────────────────────────  │
│  • ROUTING_PREFERENCES lists cheapest capable models first      │
│  • For SIMPLE tasks: [flash, haiku, grok-2, sonnet]            │
│  • First available match wins → naturally picks cheapest        │
│  • Simpler code, relies on correct preference ordering          │
│                                                                  │
│  This implementation uses BOTH for defense-in-depth:            │
│  • Preference ordering provides first line of cost awareness    │
│  • Explicit filter_by_cost() guarantees tier enforcement        │
│                                                                  │
│  For alternative implementations that rely solely on            │
│  preference ordering, see references/models.md for the          │
│  filter_by_cost() function if explicit enforcement is needed.   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 使用 `session_spawn` 进行模型选择

```
sessions_spawn(
  task: "user's request",
  model: "selected/model-id",
  label: "task-type-query"
)
```

## 安全性

- **安全注意事项**：
- 绝不要将敏感数据发送给不可信的模型
- API密钥仅通过环境变量/认证配置文件进行管理
- 详细的安全指南请参阅 `references/security.md`

## 模型详情

有关模型的详细功能和定价信息，请参阅 `references/models.md`。
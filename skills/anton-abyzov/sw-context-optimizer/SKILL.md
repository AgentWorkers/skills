---
name: context-optimizer
description: 二次上下文优化机制：在初次加载上下文后，会精确地移除无关内容。适用于上下文数据量过大、需要减少标记数量（tokens）或已加载的规格信息与当前任务无关的情况。通过智能的提示分析，该机制能够实现超过80%的标记数量减少（token reduction）。
allowed-tools: Read, Grep, Glob
---

# 上下文优化器（Context Optimizer）

这是一个二阶段的上下文优化工具，它能够分析用户的意图，并有针对性地移除加载上下文中不相关的内容，从而实现总token数量减少80%以上。

## 目的

在`context-loader`根据配置文件加载上下文（已实现70%的减少）之后，`context-optimizer`会对用户的具体请求进行智能分析，移除与该任务无关的部分内容。

## 两阶段优化策略

### 第一阶段：上下文加载器（基于配置文件）
```yaml
# context-manifest.yaml
spec_sections:
  - auth-spec.md
  - payment-spec.md
  - user-management-spec.md

Result: Load only relevant specs (70% reduction)
Before: 150k tokens → After: 45k tokens
```

### 第二阶段：上下文优化器（基于用户意图）
```typescript
User: "Fix authentication bug in login endpoint"

Analyzer detects:
  • Task type: Bug fix (not new feature)
  • Domain: Backend auth
  • Scope: Single endpoint

Removes:
  ❌ payment-spec.md (different domain)
  ❌ user-management-spec.md (different domain)
  ❌ PM agent description (not needed for bug fix)
  ❌ Frontend skills (backend task)
  ❌ DevOps skills (not deploying)

Keeps:
  ✅ auth-spec.md (directly relevant)
  ✅ architecture/security/ (auth considerations)
  ✅ nodejs-backend skill (implementation)
  ✅ Tech Lead agent (code review)

Result: Additional 40% reduction
After Pass 1: 45k tokens → After Pass 2: 27k tokens
Total reduction: 82% (150k → 27k)
```

## 使用场景

**自动激活条件：**
- 用户的请求非常具体（例如提及某个功能、 bug 或文件）
- 加载的上下文超过20,000个token
- 任务具有明确的目标（而非“构建完整的产品”）

**手动激活方式：**
- 输入“optimize context”（优化上下文）
- 输入“reduce tokens”（减少token数量）
- 输入“clean context”（清理上下文）

**无需使用的场景：**
- 上下文已经很短（少于10,000个token）
- 用户提出宽泛的问题（例如“解释系统架构”）
- 正在规划新功能（需要完整的上下文）

## 工作原理

### 1. 用户意图分析
```typescript
interface IntentAnalysis {
  task_type: TaskType;
  domains: Domain[];
  scope: Scope;
  needs_full_context: boolean;
  confidence: number;
}

enum TaskType {
  BUG_FIX = "bug-fix",           // Narrow scope
  FEATURE = "feature",            // Medium scope
  REFACTOR = "refactor",          // Medium scope
  ARCHITECTURE = "architecture",  // Broad scope
  DOCUMENTATION = "documentation", // Medium scope
  TESTING = "testing"             // Medium scope
}

enum Domain {
  FRONTEND = "frontend",
  BACKEND = "backend",
  DATABASE = "database",
  INFRASTRUCTURE = "infrastructure",
  SECURITY = "security",
  AUTH = "auth",
  PAYMENT = "payment",
  // ... project-specific domains
}

enum Scope {
  NARROW = "narrow",      // Single file/function
  FOCUSED = "focused",    // Single module
  BROAD = "broad"         // Multiple modules
}
```

**分析示例：**

| 用户请求 | 任务类型 | 相关领域 | 处理范围 | 是否需要完整上下文？ |
|-------------|-----------|---------|-------|-------------|
| “修复登录bug” | BUG_FIX | [AUTH, BACKEND] | 较具体 | 不需要 |
| “添加支付功能” | FEATURE | [PAYMENT, BACKEND] | 目标明确 | 不需要 |
| “重构认证模块” | REFACTOR | [AUTH, BACKEND] | 目标明确 | 不需要 |
| “设计系统架构” | ARCHITECTURE | 全范围 | 较宽泛 | 需要 |
| “解释支付流程” | DOCUMENTATION | [PAYMENT] | 目标明确 | 不需要 |

### 2. 上下文过滤规则
```yaml
rules:
  # Rule 1: Task-Specific Specs
  bug_fix:
    keep_specs:
      - Related to mentioned domain
      - Architecture docs for that domain
    remove_specs:
      - Unrelated domains
      - Strategic docs (PRD, business specs)
      - Future roadmap

  feature_development:
    keep_specs:
      - Related domain specs
      - Architecture for integration points
      - Related ADRs
    remove_specs:
      - Unrelated domains
      - Completed features (unless mentioned)

  architecture_review:
    keep_specs:
      - ALL (needs full context)

  # Rule 2: Agent/Skill Filtering
  backend_task:
    keep_skills:
      - Backend skills (nodejs, python, dotnet)
      - Tech Lead
      - QA Lead
    remove_skills:
      - Frontend skills
      - DevOps (unless "deploy" mentioned)
      - PM agent (unless "requirements" mentioned)

  frontend_task:
    keep_skills:
      - Frontend skills (React, Next.js)
      - UI/UX skills
    remove_skills:
      - Backend skills
      - Database skills

  # Rule 3: Documentation Filtering
  implementation_task:
    keep_docs:
      - Technical specs (HLD, LLD)
      - ADRs
      - Implementation guides
    remove_docs:
      - Strategic docs (PRD, business cases)
      - Operations runbooks
      - Deployment guides

  planning_task:
    keep_docs:
      - Strategic docs (PRD)
      - Architecture overview
      - ADRs
    remove_docs:
      - Implementation details
      - Code comments
      - Test cases
```

### 3. 优化算法
```typescript
async function optimizeContext(
  userPrompt: string,
  loadedContext: Context
): Promise<OptimizedContext> {

  // Step 1: Analyze intent
  const intent = await analyzeIntent(userPrompt);

  // Step 2: If broad scope, keep all
  if (intent.needs_full_context) {
    return {
      context: loadedContext,
      removed: [],
      kept: Object.keys(loadedContext),
      reason: "Broad scope requires full context"
    };
  }

  // Step 3: Apply filtering rules
  const filtered = {
    specs: filterByDomain(loadedContext.specs, intent.domains),
    agents: filterByTaskType(loadedContext.agents, intent.task_type),
    skills: filterByDomain(loadedContext.skills, intent.domains),
    docs: filterByScope(loadedContext.docs, intent.scope)
  };

  // Step 4: Calculate savings
  const before = calculateTokens(loadedContext);
  const after = calculateTokens(filtered);
  const savings = ((before - after) / before * 100).toFixed(0);

  // Step 5: Return optimized context
  return {
    context: filtered,
    removed: diff(loadedContext, filtered),
    kept: Object.keys(filtered),
    savings: `${savings}%`,
    tokens_before: before,
    tokens_after: after
  };
}
```

## 使用示例

### 示例1：修复bug（具体任务）
```bash
# Pass 1: context-loader loads from manifest
Loaded context: 45k tokens (auth, payment, user specs)

# User prompt
User: "Fix bug where login fails with expired JWT"

# Pass 2: context-optimizer analyzes
🔍 Analyzing task requirements...

Detected:
  Task Type: Bug Fix
  Domains: [AUTH, BACKEND]
  Scope: Narrow (single endpoint)
  Full Context Needed: No

Optimizing context...

Removed (18k tokens):
  ❌ payment-spec.md (9k tokens) - Unrelated domain
  ❌ user-management-spec.md (7k tokens) - Unrelated domain
  ❌ PM agent description (1k tokens) - Not needed for bug fix
  ❌ Frontend skills (1k tokens) - Backend task

Kept (27k tokens):
  ✅ auth-spec.md (12k tokens) - Core domain
  ✅ architecture/security/jwt-handling.md (5k tokens) - Relevant
  ✅ nodejs-backend skill (8k tokens) - Implementation
  ✅ Tech Lead agent (2k tokens) - Code review

Result: 45k → 27k tokens (40% additional reduction)
Total: 150k → 27k (82% total reduction)

Ready to proceed with optimized context.
```

### 示例2：功能开发（特定任务）
```bash
User: "Add subscription billing to payment module"

🔍 Analyzing task requirements...

Detected:
  Task Type: Feature Development
  Domains: [PAYMENT, BACKEND]
  Scope: Focused (single module)
  Full Context Needed: No

Optimizing context...

Removed (15k tokens):
  ❌ auth-spec.md (12k tokens) - Unrelated domain
  ❌ user-management-spec.md (7k tokens) - Unrelated
  ❌ DevOps agent (2k tokens) - Not deploying yet

Kept (30k tokens):
  ✅ payment-spec.md (9k tokens) - Core domain
  ✅ architecture/payment-integration.md (6k tokens) - Integration points
  ✅ architecture/adr/0015-payment-provider.md (3k tokens) - Context
  ✅ PM agent (2k tokens) - Requirements clarification
  ✅ nodejs-backend skill (8k tokens) - Implementation
  ✅ Tech Lead agent (2k tokens) - Planning

Result: 45k → 30k tokens (33% additional reduction)
```

### 示例3：架构评审（宽泛任务）
```bash
User: "Review overall system architecture"

🔍 Analyzing task requirements...

Detected:
  Task Type: Architecture Review
  Domains: [ALL]
  Scope: Broad (system-wide)
  Full Context Needed: Yes

Skipping optimization - broad scope requires full context.

Loaded context: 45k tokens (all specs retained)

Rationale: Architecture review needs visibility across all domains
to identify integration issues, dependencies, and design patterns.
```

### 示例4：手动优化
```bash
User: "Optimize context for payment work"

context-optimizer:

🔍 Analyzing for payment domain...

Removed (25k tokens):
  ❌ auth-spec.md
  ❌ user-management-spec.md
  ❌ Frontend skills
  ❌ Strategic docs

Kept (20k tokens):
  ✅ payment-spec.md
  ✅ Payment architecture
  ✅ Backend skills
  ✅ Integration guides

Result: 45k → 20k tokens (56% reduction)

You can now work on payment features with optimized context.
```

## 配置设置

## 与上下文加载器的集成

### 工作流程
```typescript
// 1. User asks to work on feature
User: "Fix authentication bug"

// 2. context-loader loads from manifest
context-loader.load({
  increment: "0001-authentication",
  manifest: "context-manifest.yaml"
})
// Result: 150k → 45k tokens (70% reduction)

// 3. context-optimizer analyzes user prompt
context-optimizer.analyze(userPrompt: "Fix authentication bug")
// Detects: bug-fix, auth domain, narrow scope

// 4. context-optimizer removes unneeded sections
context-optimizer.filter(loadedContext, analysis)
// Result: 45k → 27k tokens (40% additional reduction)

// 5. Return optimized context to main session
return optimizedContext
// Total: 150k → 27k (82% reduction)
```

### 配置的逐步优化
```yaml
# .specweave/increments/0001-auth/context-manifest.yaml
spec_sections:
  - .specweave/docs/internal/strategy/auth/spec.md
  - .specweave/docs/internal/strategy/payment/spec.md
  - .specweave/docs/internal/strategy/users/spec.md

documentation:
  - .specweave/docs/internal/architecture/auth-design.md
  - .specweave/docs/internal/architecture/payment-integration.md

max_context_tokens: 50000

# NEW: Optimization hints
optimization:
  domains:
    auth: ["auth-spec.md", "auth-design.md"]
    payment: ["payment/spec.md", "payment-integration.md"]
    users: ["users/spec.md"]

  # Suggest which domains to keep for common tasks
  task_hints:
    "login": ["auth"]
    "payment": ["payment"]
    "billing": ["payment"]
    "user profile": ["users", "auth"]
```

## Token节省示例

### 实际项目示例（500页的文档）

**未使用ContextWeave时：**
- 加载完整文档：500页 × 300个token = 150,000个token
- 每次查询消耗150,000个token
- 成本：0.015美元 × 150 = 每次查询0.225美元

**使用Context Loader（第一阶段）后：**
- 仅加载认证相关的部分：50页 × 15,000个token（减少90%）
- 成本：0.015美元 × 15 = 每次查询0.225美元

**使用Context Optimizer（第二阶段）后：**
- 进一步精炼到登录相关的内容：30页 × 9,000个token（总减少94%）
- 成本：0.015美元 × 9 = 每次查询0.135美元

**节省费用：2.25美元 → 0.135美元（节省84%）**

### 会话示例（10次查询）

**场景：**修复3个认证bug、2个支付bug、1个用户bug

| 查询类型 | 未使用ContextWeave时的token数量 | 使用ContextLoader后的token数量 | 使用ContextOptimizer后的token数量 | 节省的token数量 |
|-------|-----------------|-------------------|-------------------|-------------------|
| 认证bug | 150,000 | 45,000 | 27,000 | 82% |
| 认证bug | 150,000 | 45,000 | 27,000 | 82% |
| 认证bug | 150,000 | 45,000 | 27,000 | 82% |
| 支付bug | 150,000 | 45,000 | 28,000 | 81% |
| 支付bug | 150,000 | 45,000 | 28,000 | 81% |
| 用户bug | 150,000 | 45,000 | 30,000 | 80% |

**总token数量：**
- 未使用ContextWeave时：900,000个token
- 仅使用ContextLoader后：270,000个token（减少70%）
- 使用ContextOptimizer后：167,000个token（减少81%）

**费用节省：**
- 未使用ContextWeave时：13.50美元
- 仅使用ContextLoader后：4.05美元
- 使用ContextOptimizer后：2.50美元

**每次会话额外节省：1.55美元（相比仅使用ContextLoader节省38%）**

## 最佳实践

### 1. 自动运行
- 默认模式下，会在上下文加载器之后自动执行优化
- 不需要手动干预
- 会根据每次查询的情况进行适应
- 如有需要，可以恢复完整的上下文

### 2. 对关键任务进行审查
- 在生产环境中部署前，应对优化结果进行安全审查：
```bash
User: "Review security before deployment"

context-optimizer:
⚠️ Keeping full context (critical task detected)
```

### 3. 对复杂任务使用保守的缓冲策略
```yaml
buffer_strategy: "conservative"
```
- 保留相邻的领域相关内容
- 包括所有集成点
- 有助于代码重构时的安全性

### 4. 为项目自定义领域
```yaml
custom_domains:
  - "payment-processing"
  - "real-time-notifications"
  - "analytics-pipeline"
```
- 有助于优化器更好地理解项目的结构

### 5. 监控优化效果
- 如果优化器错误地移除了必要的内容：
- 降低`min_confidence`阈值
- 添加`always_keep`规则
- 使用`conservative`缓冲策略

## 限制

**Context Optimizer的局限性：**
- 无法预测未来的对话需求（仅分析当前的请求内容）
- 无法理解领域之间的隐含关系（除非进行了额外配置）
- 无法读取用户的真实意图（如果请求表述模糊，可能会保留更多上下文）

**Context Optimizer能够实现的功能：**
- 分析请求的类型和相关领域
- 移除明显不相关的信息
- 在需要时恢复被移除的上下文
- 根据`always_keep`和`custom_domains`的配置进行优化

## 测试用例

### TC-001：修复bug
**输入：**包含认证、支付和用户相关信息的上下文（45,000个token）
**输出：**仅保留认证相关的信息（27,000个token，减少40%）

### TC-002：功能开发
**输入：**包含多个领域的上下文**
**输出：**保留支付和集成相关的信息（减少33%）

### TC-003：架构评审
**输入：**包含所有相关信息的上下文**
**输出：**保留所有信息（因为需要完整的架构描述）

### TC-004：模糊的请求
**输入：**请求内容较为模糊**
**输出：**为了安全起见，保留所有信息（尽管置信度较低）

### TC-005：手动指定领域
**输入：**明确要求针对支付功能进行优化**
**输出：**仅保留与支付相关的信息（减少50%以上）

## 未来改进计划

### 第二阶段：对话历史分析
- 跟踪实际使用的上下文内容
- 移除从未被引用的部分
- 学习用户的查询模式

### 第三阶段：动态上下文扩展
- 从最少的上下文开始加载
- 根据需要动态添加相关内容
- 实现“即时”上下文加载

### 第四阶段：跨版本的上下文整合
- 检测不同版本之间的依赖关系
- 智能地加载跨版本的上下文
- 保持各版本上下文的一致性

## 参考资源

- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401) - 上下文检索技术
- [LongRAG: 大规模上下文优化](https://arxiv.org/abs/2310.03025) - 大规模上下文处理技术
- [Anthropic Context Windows](https://docs.anthropic.com/claude/docs/context-windows) - 最佳实践指南

---

## 总结

`context-optimizer`提供了二阶段的上下文优化功能：
- 基于用户意图进行过滤
- 考虑领域相关性，移除不相关的信息
- 根据任务类型进行优化（如修复bug、开发新功能或设计架构）
- 实现总token数量减少80%以上（在Context Loader的基础上）
- 全自动运行
- 在需要时可以恢复完整的上下文
- 支持自定义配置（如特定领域和缓冲策略）

**适用场景：**处理大量文档（500页以上）时，即使使用基于配置文件的加载方式，也会产生30,000个以上的token。**

**无需使用的场景：**上下文已经很短（少于10,000个token）时；提出宽泛的架构问题时；或从零开始规划新功能时。

**优化效果：**将原始的150,000个token减少到27,000个token，总节省率达到82%，使得在Claude的上下文处理范围内能够高效处理企业级文档。
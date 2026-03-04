---
name: naming-forge
version: 1.0.0
description: 它解决了计算机科学中最棘手的问题：如何为各种元素命名。通过运用语言学原理、代码库规范以及语义分析，为变量、函数、类型、文件、路由、数据库表等所有需要命名的对象生成精确、一致且易于识别的名称。因为“temp2_final_v3”根本算不上一个合适的名称——它其实只是在“求救”。
author: J. DeVere Cooley
category: everyday-tools
tags:
  - naming
  - conventions
  - readability
  - linguistics
metadata:
  openclaw:
    emoji: "⚒️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - code-quality
---
# 命名工具（Naming Forge）

> “在计算机科学中，只有两件难事：缓存失效处理和给事物起名。” —— Phil Karlton

## 工具的功能

这个工具用于为函数命名。它接收一个订单列表，过滤掉已取消的订单，按照客户对订单进行分组，并返回各组的总数。你盯着光标发呆：“`processOrders`？” 太模糊了。“`filterAndGroupAndSummarizeOrdersByCustomerExcludingCancelled`？” 太长了。“`getOrderSummary`？” 有误导性——它的功能可不只是“获取”数据。

命名工具生成的函数名称具有以下特点：
- **精确性**：准确反映函数的功能；
- **一致性**：符合你的代码库命名规范；
- **易查找性**：其他开发者能够快速理解该函数的用途；
- **名称长度与功能重要性相匹配**。

## 好命名的五大法则

### 法则1：名称应是一种“契约”
名称就是一种承诺。例如，“`calculateTotal`”这个名字承诺该函数会计算并返回总数；如果它还负责发送邮件，那么这个名字就具有误导性。

```
BAD:  updateUser()          — does it update the DB? The UI? Both? What fields?
GOOD: saveUserProfile()     — saves the user's profile (to persistent storage)
GOOD: refreshUserDisplay()  — updates what the user sees on screen
```

### 法则2：名称长度由函数的作用范围决定
- **作用范围小** → 名称应简短；
- **作用范围大** → 名称应具有描述性。例如，循环变量可以用“`i`”表示，而公共API方法则应使用更详细的名称。

| 作用范围 | 名称长度 | 示例 |
|---|---|---|
| 循环变量（3行代码） | 1-2个字符 | `i`, `ch`, `tx` |
| 局部变量（10-20行代码） | 1个单词 | `total`, `users`, `query` |
| 私有方法（模块内部） | 1-2个单词 | `parseInput`, `buildQuery` |
| 公共方法（跨模块调用） | 2-3个单词 | `calculateOrderTotal`, `validateAddress` |
| 导出的常量（全局变量） | 2-4个单词 | `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT_MS` |

### 法则3：动作用动词表示，事物用名词表示
函数执行某种操作 → 用动词命名；变量存储数据 → 用名词命名；类型描述数据属性 → 用名词或形容词命名。

```
FUNCTIONS (verb-first):
├── get/fetch/load    → retrieves data (getSessions, fetchUser, loadConfig)
├── set/update/save   → modifies data (setTheme, updateProfile, saveOrder)
├── create/build/make → constructs new things (createUser, buildQuery, makeHandler)
├── delete/remove     → eliminates things (deleteAccount, removeItem)
├── is/has/can/should → returns boolean (isValid, hasPermission, canEdit)
├── parse/format/transform → converts between formats (parseJSON, formatDate)
├── validate/check/verify → confirms correctness (validateEmail, checkStatus)
└── handle/process/on → responds to events (handleClick, processPayment, onSubmit)

VARIABLES (noun/adjective):
├── Collections: plural nouns (users, orders, activeConnections)
├── Singles: singular nouns (user, order, currentConnection)
├── Booleans: is/has/can prefix (isLoading, hasErrors, canSubmit)
├── Counts: noun + Count (retryCount, errorCount, userCount)
└── Maps/Indices: noun + By + Key (userById, ordersByDate)
```

### 法则4：一致性比“聪明”更重要
如果代码库中已经使用了“`fetchUser`”这样的名称，就不要再引入“`retrieveUser`”这样的新名称。应保持命名的一致性。

```
CODEBASE AUDIT:
├── Existing pattern: fetch* for API calls → USE fetchOrders, NOT getOrders
├── Existing pattern: *Service for modules → USE PaymentService, NOT PaymentManager
├── Existing pattern: on* for handlers → USE onSubmit, NOT handleSubmit
└── Existing pattern: is* for booleans → USE isActive, NOT active or checkActive
```

### 法则5：避免使用无意义的词汇
那些只是增加名称长度但毫无实际意义的词汇（如`data`, `info`, `item`, `thing`, `object`, `value`, `manager`, `handler`, `processor`, `helper`, `utils`）应尽量避免使用。

```
BAD:  userData, userInfo, userObject  → just "user"
BAD:  orderItem  → just "order" (unless distinguishing from order summary)
BAD:  StringHelper, DateUtils  → what do they actually do? Be specific.
GOOD: formatDate, parseCSV, slugify  → specific actions
```

## 命名工具的工作流程

```
INPUT: What does this thing do? (natural language description)
CONTEXT: What part of the codebase is this in?

Phase 1: SEMANTIC EXTRACTION
├── Extract the core action or concept from the description
├── Identify: Is this a function, variable, type, file, or route?
├── Identify: What's the scope? (local, module, public, global)
└── Identify: What domain vocabulary applies? (business terms, tech terms)

Phase 2: CONVENTION SCAN
├── Scan existing codebase for naming patterns:
│   ├── Verb preferences (get vs. fetch vs. load vs. retrieve)
│   ├── Noun preferences (User vs. Account vs. Profile)
│   ├── Casing convention (camelCase, snake_case, PascalCase, kebab-case)
│   ├── Prefix/suffix patterns (is*, *Service, *Controller, I* for interfaces)
│   └── Domain vocabulary already in use
├── Identify the dominant convention for this type of name
└── Flag any existing inconsistencies

Phase 3: CANDIDATE GENERATION
├── Generate 3-5 candidates following conventions
├── For each candidate, evaluate:
│   ├── Precision: Does the name accurately describe the thing?
│   ├── Consistency: Does it match existing patterns?
│   ├── Discoverability: Could a teammate guess this name?
│   ├── Proportionality: Is the length right for the scope?
│   └── Uniqueness: Does it conflict with any existing name?
├── Rank candidates by composite score
└── Flag tradeoffs between candidates

Phase 4: RECOMMENDATION
├── Top recommendation with rationale
├── Runner-up alternatives
├── Names to AVOID (and why)
└── If renaming: migration impact (how many references to update)
```

## 针对特定领域的命名规范

- **API路由/端点**  
- **数据库表/列**  
- **CSS类**  
- **环境变量**  

```
PATTERN: /resource/action or RESTful convention

GOOD:
├── GET    /users              → list users
├── GET    /users/:id          → get specific user
├── POST   /users              → create user
├── PUT    /users/:id          → replace user
├── PATCH  /users/:id          → partial update
├── DELETE /users/:id          → delete user
├── POST   /users/:id/verify   → action on user (verb as sub-resource)

BAD:
├── GET /getUsers              → verb in path (GET already implies "get")
├── POST /createNewUser        → redundant (POST already implies "create")
├── GET /user_list             → inconsistent casing, use /users
└── POST /doUserVerification   → too verbose, use /users/:id/verify
```

## 输出格式

```
╔══════════════════════════════════════════════════════════════╗
║                      NAMING FORGE                           ║
║  Input: "function that takes a list of orders, filters      ║
║  out cancelled ones, groups by customer, returns totals"    ║
║  Scope: Public method in OrderService                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RECOMMENDATION: summarizeActiveOrdersByCustomer             ║
║  ├── Precise: "summarize" = aggregate, "active" = not        ║
║  │   cancelled, "by customer" = grouping key                 ║
║  ├── Convention match: codebase uses *ByField pattern ✓      ║
║  ├── Discoverable: searching "order" + "customer" finds it ✓ ║
║  └── Proportional: 5 words for a public cross-module method ✓║
║                                                              ║
║  ALTERNATIVES:                                               ║
║  ├── getCustomerOrderTotals — shorter but loses "active"     ║
║  ├── aggregateOrdersByCustomer — "aggregate" is less common  ║
║  │   in this codebase (0 uses vs 12 uses of "summarize")     ║
║  └── calculateCustomerOrderSummary — "calculate" implies     ║
║      math; this is more filter + group                       ║
║                                                              ║
║  AVOID:                                                      ║
║  ├── processOrders — "process" is meaningless                ║
║  ├── getOrderData — "data" is noise                          ║
║  └── doOrderStuff — please                                   ║
╚══════════════════════════════════════════════════════════════╝
```

## 何时使用该工具

- 当你盯着光标，不知道该如何给某个函数命名时；
- 当你打算使用“`temp`”、“`data`”、“`result`”或“`thing`”这样的临时名称时；
- 在重构代码时，发现现有名称与实际功能不符时；
- 在审查具有误导性名称的代码时；
- 在创建新模块并设定命名规范时；
- 在为数据库表、API端点或环境变量命名时。

## 命名的重要性

名称是代码库的主要文档。开发者每天会多次阅读这些名称。一个精确的名称可以避免阅读代码实现；而一个具有误导性的名称带来的麻烦远比没有名称更严重。

你可能会花费10分钟来为一个函数名称绞尽脑汁，或者花费10个小时来解释“`processData`”到底做什么。使用命名工具可以节省大量时间。

该工具完全不需要外部依赖，也不涉及任何API调用，仅基于语言和代码库的规则进行命名建议。

***
# 信号内存（Signal Memory）⚡

**状态：** 📋 代理指南（Agent Guidelines） | **模块：** signal | **所属部分：** 代理大脑（Agent Brain）

**冲突检测（Conflict Detection）**：在存储新信息之前，代理必须调用 `conflicts` 函数——这是一个手动步骤，而非自动执行的。

## 何时运行 Signal 函数

Signal 函数不是自动运行的。代理必须明确地调用它：

1. **在存储新信息之前**：在调用 `add` 函数之前，需要运行 `./scripts/memory.sh conflicts "<内容>"`。
2. **按需**：当用户请求“检查是否存在冲突”或“是否有任何不一致的地方”时。

```bash
# Before adding any new entry:
./scripts/memory.sh conflicts "User prefers Python for data work"

# If NO_CONFLICTS → proceed with add
# If POTENTIAL_CONFLICTS → ask user or supersede
```

## 冲突检测的原理

该系统会过滤掉常见的停用词（如 “I”、“the”、“is” 等），然后比较新内容与现有条目中的有效词汇。要判定存在冲突，需要满足以下条件：

- 至少有两个有效词汇有重叠；
- 这些重叠词汇需要覆盖较短文本中至少 30% 的有效词汇。

这样就可以避免误判，例如：“I like Python” 与 “Python is a snake” 这样的情况（虽然两者都包含 “Python”，但由于上下文不同，经过过滤后只有 1 个有效词汇重叠）。

## 冲突类型

- **直接矛盾（Direct Contradiction）**  
```
Existing: "User prefers TypeScript"
New:      "User prefers Python"
→ Ask: "Previously you said you prefer TypeScript. Has that changed?"
```

- **时间更新（Temporal Update）**  
```
Existing: "Alex works at CompanyA"
New:      "Alex works at CompanyB"
→ Not a conflict — supersede the old entry
→ Run: ./scripts/memory.sh supersede <old_id> <new_id>
```

- **上下文相关（Context-Dependent）**  
```
Existing: "Use short responses"
New:      "Give me detailed analysis"
→ Not a conflict — different contexts
→ Store both with context:
  ./scripts/memory.sh add preference "Short responses" user "style" "" "casual chat"
  ./scripts/memory.sh add preference "Detailed analysis" user "style" "" "research tasks"
```

## 检测流程

```
New content arrives
       │
       ▼
  conflicts <content>
       │
       ├── NO_CONFLICTS → proceed with store
       │
       └── POTENTIAL_CONFLICTS (with overlap %)
              │
              ├── Same topic, different claim? → Ask user
              ├── Same topic, newer info? → Supersede
              └── Different context? → Store both with context field
```

## 响应模板

- **发现矛盾（Found a Contradiction）**  
```
"I have something that might conflict with this:
 - Previously: [old claim]
 - Now: [new claim]
 Should I update, or are both true in different contexts?"
```

- **用户纠正错误（User Corrects You）**  
```
"Got it, tracking that correction."
→ ./scripts/memory.sh correct <old_id> "<new_content>" "<reason>"
```

## Signal 函数不执行的功能

- 不会在存储数据前自动运行（必须由代理手动调用）；
- 不负责监控“语气变化”（这属于 “Vibe Guidelines” 的范畴）；
- 不负责跟踪信息的可信度（这属于 “Gauge Guidelines” 的范畴）；
- 不会在后台持续运行；
- 无法通过用户的沉默或重复提问来检测“隐性”冲突。

## 集成要求

- **归档（Archive）**：代理应在存储数据之前调用 `conflicts` 函数（该过程不是自动执行的）；
- **Gauge**：如果检测到冲突，可能需要将信息的可信度降级为 “UNCERTAIN”。
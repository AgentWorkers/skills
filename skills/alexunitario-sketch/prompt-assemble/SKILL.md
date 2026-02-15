---
name: prompt-assemble
description: **具有内存管理功能的令牌安全提示生成系统**  
适用于所有需要通过内存检索来构建大型语言模型（LLM）提示的代理程序。该系统能够确保不会出现因令牌溢出导致的API故障。它采用了两阶段上下文构建机制、内存安全保护机制以及对内存注入的严格限制。
---

# Prompt Assemble

## 概述

这是一个标准化且安全的提示生成框架，能够确保API的稳定性。该框架采用了**两阶段上下文构建**（Two-Phase Context Construction）和**内存安全阀**（Memory Safety Valve）机制，以防止令牌（token）溢出，同时最大化利用相关上下文信息。

**设计目标：**
- ✅ 绝不会因内存相关的令牌溢出而导致系统故障
- ✅ 内存资源始终是可丢弃的（即非刚性依赖），避免产生固定依赖关系
- ✅ 令牌使用量的决策权集中在提示生成层（prompt assemble layer）

## 使用场景

在以下情况下使用此功能：
1. 构建或修改用于生成提示的代理（agent）程序
2. 实现内存检索系统
3. 为现有代理添加与提示生成相关的逻辑
4. 任何需要确保令牌使用量安全性的场景

## 核心工作流程

```
User Input
    ↓
Need-Memory Decision
    ↓
Minimal Context Build
    ↓
Memory Retrieval (Optional)
    ↓
Memory Summarization
    ↓
Token Estimation
    ↓
Safety Valve Decision
    ↓
Final Prompt → LLM Call
```

## 各阶段详细信息

### 第0阶段：基础配置
```python
# Model Context Windows (2026-02-04)
# - MiniMax-M2.1: 204,000 tokens (default)
# - Claude 3.5 Sonnet: 200,000 tokens
# - GPT-4o: 128,000 tokens

MAX_TOKENS = 204000  # Set to your model's context limit
SAFETY_MARGIN = 0.75 * MAX_TOKENS  # Conservative: 75% threshold = 153,000 tokens
MEMORY_TOP_K = 3                     # Max 3 memories
MEMORY_SUMMARY_MAX = 3 lines        # Max 3 lines per memory
```

**设计理念：**
- 为安全起见，预留25%的内存缓冲空间（用于模型开销、估算误差及突发情况）
- 优先选择“内存使用不足”而非“内存溢出”

### 第1阶段：最小化所需上下文信息
- 系统提示信息
- 最近的N条消息（N=3，经过筛选）
- 当前用户输入
- **默认情况下不使用内存**

### 第2阶段：判断是否需要使用内存
```python
def need_memory(user_input):
    triggers = [
        "previously",
        "earlier we discussed",
        "do you remember",
        "as I mentioned before",
        "continuing from",
        "before we",
        "last time",
        "previously mentioned"
    ]
    for trigger in triggers:
        if trigger.lower() in user_input.lower():
            return True
    return False
```

### 第3阶段：内存获取（可选）
```python
memories = memory_search(query=user_input, top_k=MEMORY_TOP_K)
for mem in memories:
    summarized_memories.append(summarize(mem, max_lines=MEMORY_SUMMARY_MAX))
```

### 第4阶段：令牌数量估算
计算基础上下文信息（base_context）和已获取内存信息（summarized_memories）所需的令牌数量。

### 第5阶段：安全阀（关键步骤）
```python
if estimated_tokens > SAFETY_MARGIN:
    base_context.append("[System Notice] Relevant memory skipped due to token budget.")
    return assemble(base_context)
```

**严格规则：**
- ❌ 绝不允许降低系统提示信息的质量
- ❌ 绝不允许截断用户输入内容
- ❌ 禁止使用“随机拼接”（lucky splicing）的方式来处理数据
- ✅ 只有内存资源是可以被消耗的（即可以丢弃的）

### 第6阶段：最终提示生成
```python
final_prompt = assemble(base_context + summarized_memories)
return final_prompt
```

## 内存数据标准

### 可保存到长期内存中的数据：
- ✅ 用户偏好设置 / 身份信息 / 长期目标
- ✅ 已确认的重要结论
- ✅ 系统级设置和规则

### 不允许保存到长期内存中的数据：
- ❌ 原始对话记录
- ❌ 推理过程痕迹
- ❌ 临时性的讨论内容
- ❌ 可从聊天记录中恢复的信息

## 快速入门

将 `scripts/prompt_assemble.py` 文件复制到您的代理程序中，然后按照文档中的说明进行使用：

```python
from prompt_assemble import build_prompt

# In your agent's prompt construction:
final_prompt = build_prompt(user_input, memory_search_fn, get_recent_dialog_fn)
```

## 相关资源

### scripts/
- `prompt_assemble.py` - 包含所有阶段的完整实现代码（PromptAssembler 类）

### 参考资料/
- `memory_standards.md` - 详细的内存数据使用规范
- `token_estimation.md` - 令牌数量估算策略
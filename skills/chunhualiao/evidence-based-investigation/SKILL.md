---
name: evidence-based-investigation
description: "通过基于证据的分析来调查问题，利用会话日志、错误日志以及“5个为什么”（5 Whys）方法论。这种方法适用于调试OpenClaw中的问题、分析系统故障、追踪消息传递问题，或进行需要从日志、文件或系统状态中获取确凿证据的根本原因分析。"
---
# 基于证据的调查

通过日志、文件和系统状态的客观证据，系统地调查问题。

## 核心原则

1. **以证据为主，而非假设**：每个结论都必须有日志记录、文件内容或可观察到的系统状态作为支持。
2. **追踪数据轨迹**：通过会话日志追踪ID、时间戳和事件之间的关联。
3. **使用“5个为什么”进行深入分析，并引用具体证据**：每个“为什么”的答案都必须有相应的证据支持。
4. **清晰记录**：以他人能够独立验证的方式记录调查结果。

## 调查工作流程

### 1. 确定问题

明确问题的具体表现：
- 预期结果是什么？
- 实际发生了什么？
- 问题发生的时间是什么时候？（精确的时间戳）
- 有哪些证据表明问题的存在？

**决策点分析：**
在调查技术故障之前，先判断问题是否源于错误的决策：
- 为该任务选择了正确的工具或方法吗？
- 是否有明显的警告信号（如文件扩展名、错误信息、系统限制）？
- 在做出决策时有哪些信息可用？
- 应该考虑哪些替代方案？
- 该决策是否违反了已知的最佳实践？

**示例**：对`.pdf` URL使用`web_fetch`是一个决策错误，而非技术故障。

### 2. 收集证据

**会话日志：**
```bash
# Find relevant messages by ID or timestamp
jq 'select(.id == "MESSAGE_ID")' ~/.openclaw/agents/AGENT/sessions/SESSION.jsonl

# Trace message chain by parentId
jq 'select(.id == "ID" or .parentId == "ID")' SESSION.jsonl

# Filter by timestamp range
jq 'select(.timestamp >= "2026-02-14T23:18:00Z" and .timestamp <= "2026-02-14T23:20:00Z")' SESSION.jsonl
```

**网关日志：**
```bash
# Search by timestamp
grep "2026-02-14T23:18" ~/.openclaw/logs/gateway.log

# Find errors around time
grep -C 10 "2026-02-14T23:18" ~/.openclaw/logs/gateway.err.log
```

**系统状态：**
```bash
# Check process state
ps aux | grep openclaw

# Check file timestamps
ls -la --time-style=full-iso FILE
```

### 3. 使用“5个为什么”进行分析

详细的方法论请参见[5-whys.md](references/5-whys.md)。

**步骤A：首先检查决策点**
在分析技术原因之前，先验证所采用的方法是否合理：
```
Decision Point 1: Was the chosen tool/method appropriate?
Evidence: [URL/context/constraints visible at decision time]
Assessment: [Correct choice / Wrong tool / Missing validation]

Decision Point 2: Were there warning signs that should have triggered different action?
Evidence: [File extension, error message, documentation, constraints]
Assessment: [Warning heeded / Warning ignored / No warning available]
```

**步骤B：进行技术层面的“5个为什么”分析**
只有在验证了决策点的合理性之后，才进行技术分析：
```
Why 1: Why did X happen?
Evidence: [specific log entry, file content, timestamp]
Answer: Because Y

Why 2: Why did Y occur?
Evidence: [specific log entry, file content, timestamp]
Answer: Because Z

... continue to root cause
```

**注意**：如果步骤A发现决策错误，那么根本原因在于错误的决策，而非随后的技术故障。

### 4. 清晰记录调查结果

**证据部分：**
- 引用确切的日志记录
- 包含时间戳
- 显示文件路径和行号
- 链接到相关的证据

**分析部分：**
- 使用“5个为什么”进行分析，并引用证据
- 确定根本原因
- 评估影响

**建议：**
- 提出修复方案
- 制定预防措施
- 提出监控和改进方案

### 5. 报告问题

请参考[issue-reporting.md](references/issue-reporting.md)中的模板。

报告内容应包括：
- 描述问题的清晰标题
- 可观察到的问题行为总结
- 经过处理的日志/文件证据
- 根本原因分析
- 提出的解决方案
- 可复现性的评估

## 日志分析技术

详细的技术分析方法请参见[log-analysis.md](references/log-analysis.md)。

**会话日志（JSONL格式）：**
```bash
# Extract message chain
jq -c '{id, parentId, role: .message.role, type, timestamp: .timestamp[0:19]}' SESSION.jsonl

# Find gaps in chain
jq -r '.id + " -> " + .parentId' SESSION.jsonl | grep "MISSING_ID"
```

**时间戳关联分析：**
```bash
# Find events within 1 second
awk '/23:18:[0-9][0-9]/' gateway.log
```

## 常见误区

- **无证据下的猜测**：务必引用来源。
- **证据不完整**：检查所有相关的日志（会话日志、网关日志、错误日志）。
- **缺乏上下文**：查看问题发生前后的日志。
- **错误地假设因果关系**：相关性需要额外的证据来证实。
- **信息泄露**：在分享之前务必删除个人信息。

## 调查示例

### 示例1：技术故障（消息传递）

**问题**：用户发送的消息2010未被处理

**证据：**
```
Line 260: User message at 23:18:38.610Z (message ID: ffb67afd)
Line 259: cache-ttl event at 23:18:38.603Z (7ms before)
Gateway error log: AbortError at 23:19:28.082Z
```

**决策点分析：**
- 选择工具：通过会话API发送消息（正确）
- 未发现决策错误——需要技术层面的调查

**5个为什么：**
1. 为什么没有响应？→ 未生成相应的处理流程（证据：日志中未显示处理流程的开始）
2. 为什么没有生成处理流程？→ 处理流程被中止（证据：日志中的AbortError）
3. 为什么处理流程被中止？→ 缓存切换过程中出现了中断（证据：7毫秒的时间延迟）
4. 为什么缓存切换会中断？→ 缓存刷新时没有处理队列
**根本原因**：网关缺少处理缓存切换的机制

**结果**：提交GitHub问题，并与社区成员共同寻找解决方案。

---

### 示例2：决策错误（PDF文件提取）

**问题**：尝试提取PDF文件时返回了二进制数据而非文本

**证据：**
```
URL: https://resources.anthropic.com/hubfs/guide.pdf (ends in .pdf)
Tool used: web_fetch (HTML extraction tool)
Result: extractor: "raw", binary data returned
```

**决策点分析：**
- **决策错误**：对`.pdf` URL使用了`web_fetch`工具
- **警告信号**：
  - URL扩展名为`.pdf`
  - 工具说明中明确表示该工具支持将HTML转换为markdown或文本
  - 文档中未提及该工具支持PDF解析
- **决策时的情况**：URL扩展名可见，工具文档也提供了相关说明
- **应采取的措施**：应使用浏览器或专门的PDF解析工具
**根本原因**：错误地选择了工具，而非工具本身的限制

**5个为什么（不适用）：**
分析`web_fetch`为何失败的技术原因无关紧要——错误地选择了该工具才是问题的根本原因。

**结果**：
- 更新调查流程，确保首先检查决策点的合理性。
- 更新技能文档，要求工程师根据输入类型验证工具的选择。
- 添加预处理步骤（检查URL扩展名与工具功能的匹配性）。
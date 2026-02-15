---
name: session-handoff
model: standard
description: |
  WHAT: Create comprehensive handoff documents that enable fresh AI agents to seamlessly continue work with zero ambiguity. Solves long-running agent context exhaustion problem.
  
  WHEN: (1) User requests handoff/memory/context save, (2) Context window approaches capacity, (3) Major task milestone completed, (4) Work session ending, (5) Resuming work with existing handoff.
  
  KEYWORDS: "save state", "create handoff", "context is full", "I need to pause", "resume from", "continue where we left off", "load handoff", "save progress", "session transfer", "hand off"
---

# 会话交接

创建会话交接文档，以便新接手的代理能够无缝地继续工作。

## 模式选择

**创建交接文档？** 用户希望保存当前的工作状态、暂停工作，或者当前的工作环境已经非常完整。
→ 请按照“创建交接文档”（CREATE Workflow）的步骤操作。

**从交接文档中恢复工作？** 用户希望继续之前的工作或加载之前的工作环境。
→ 请按照“从交接文档中恢复工作”（RESUME Workflow）的步骤操作。

**主动建议：** 在进行了大量工作（如修改了5个以上文件、进行复杂调试或做出重大决策后）：
> “考虑创建一个交接文档来保存这些工作成果。准备就绪时，请输入‘create handoff’。”

---

## 创建交接文档（CREATE Workflow）

### 第1步：生成框架

运行智能框架脚本：

```bash
python scripts/create_handoff.py [task-slug]
```

对于需要继续之前工作的情况（链接到之前的工作）：
```bash
python scripts/create_handoff.py "auth-part-2" --continues-from 2024-01-15-auth.md
```

该脚本会创建`.claude/handoffs/`目录，并生成一个带有时间戳的文件，其中包含预先填充的元数据（时间戳、项目路径、Git分支、最近提交的更改、修改过的文件等）。

### 第2步：完善文档

打开生成的文件，填写所有`[TODO: ...]`部分。优先考虑以下内容：
1. **当前工作状态总结** - 当前正在进行的操作
2. **重要背景信息** - 下一个接手者必须了解的关键信息
3. **下一步行动** - 清晰且可执行的操作步骤
4. **所做的决策** - 包括决策的理由（而不仅仅是结果）

有关完整的文档结构，请参考[references/handoff-template.md](references/handoff-template.md)。

### 第3步：验证

```bash
python scripts/validate_handoff.py <handoff-file>
```

检查以下内容：
- 是否还有未填写的`[TODO: ...]`占位符
- 所有必需的部分是否都已填写
- 是否包含任何敏感信息（如API密钥、密码、令牌等）
- 引用的文件是否存在
- 文档的质量评分（0-100分）

**如果发现敏感信息或评分低于70分，请不要完成交接文档的创建。**

### 第4步：确认

向用户报告以下信息：
- 交接文档的位置
- 验证结果及任何警告信息
- 捕获到的工作环境总结
- 下一次会话的第一个行动项

---

## 从交接文档中恢复工作（RESUME Workflow）

### 第1步：查找交接文档

```bash
python scripts/list_handoffs.py
```

### 第2步：检查文档的时效性

```bash
python scripts/check_staleness.py <handoff-file>
```

文档的时效性分为以下等级：
- **最新**：可以安全地继续工作
- **略微过时**：先查看一下更改内容
- **过时**：仔细验证工作环境
- **严重过时**：考虑重新创建新的交接文档

### 第3步：加载并验证

完整阅读交接文档。如果当前的工作属于一个连续的交接流程的一部分，还需要阅读之前的交接文档。

请参考[references/resume-checklist.md](references/resume-checklist.md)：
1. 确认项目目录和Git分支是否一致
2. 检查是否存在阻碍工作的因素是否已经解决
3. 验证之前的假设是否仍然成立
4. 检查修改过的文件是否存在冲突

### 第4步：开始工作

从“下一步行动”中的第一个任务开始。

在工作过程中，请参考以下内容：
- “关键文件”以了解重要的文件位置
- “发现的常见问题”以了解需要注意的事项
- “潜在的陷阱”以避免已知的问题

---

## 交接文档的连续性

对于持续时间较长的项目，可以通过链接多个交接文档来保持工作环境的连续性：

```
handoff-1.md (initial work)
    ↓
handoff-2.md --continues-from handoff-1.md
    ↓
handoff-3.md --continues-from handoff-2.md
```

在从交接文档中恢复工作时，先阅读最新的文档，然后根据需要参考之前的文档。

---

## 存储位置

存储位置：`.claude/handoffs/`
文件命名格式：`YYYY-MM-DD-HHMMSS-[slug].md`

---

## 文档质量标准

一份优秀的交接文档应具备以下特点：
- 对当前工作状态的描述清晰无误
- 下一步行动明确且有序
- 决策的理由完整说明（而不仅仅是结果）
- 相关文件的路径应包含行号
- 不包含任何敏感信息或凭证

---

## 绝对禁止的行为：
- 不要在交接文档中包含API密钥、密码、令牌或凭证
- 不要在已完成的交接文档中留下未填写的`TODO`占位符
- 跳过验证步骤
- 在没有填写“重要背景信息”部分的情况下创建交接文档
- 在交接文档的质量评分低于70分的情况下完成文档的创建
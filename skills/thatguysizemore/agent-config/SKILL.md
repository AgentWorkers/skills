---
name: agent-config
description: 智能地修改代理核心配置文件（AGENTS.md、SOUL.md、IDENTITY.md、USER.md、TOOLS.md、MEMORY.md、HEARTBEAT.md）。当对话涉及更改代理行为、更新规则、调整个性设置、修改指令、调整操作流程、更新内存架构、改变任务分配模式、添加安全规则、优化提示语模式，或对代理工作区配置文件进行任何其他修改时，请使用该功能。该功能会在有配置、调优、改进、修复或优化代理行为的意图时被触发。
---

# 代理配置技能

该技能提供了一种结构化的流程，用于智能地修改 OpenClaw 代理的核心配置文件。它确保更改只针对正确的文件，并采用正确的格式进行，避免重复和冗余，同时遵守文件大小限制以及提示工程的最佳实践。

## 核心工作流程

在修改代理配置文件时，请遵循以下步骤：

### 1. 确定目标文件

阅读 `references/file-map.md` 以确定更改应应用于哪个文件。

**快速决策树：**
- 操作流程、内存工作流程、委托规则 → `AGENTS.md`
- 个性、语气、界限、道德规则 → `SOUL.md`
- 代理名称、表情符号、核心氛围 → `IDENTITY.md`
- 用户信息、偏好设置、家庭信息 → `USER.md`
- 本地工具说明、命令示例、API 地址 → `TOOLS.md`
- 长期保存的重要事实（仅限主会话）→ `MEMORY.md`
- 心跳检查列表（保持简洁）→ `HEARTBEAT.md`

**重要提示：** 子代理仅能查看 `AGENTS.md` 和 `TOOLS.md`。操作规则必须放在 `AGENTS.md` 中，而不是 `SOUL.md` 中。

### 2. 检查当前状态

在做出更改之前，请先进行以下检查：

```bash
# Check file size (20K char limit per file)
wc -c ~/clawd/AGENTS.md ~/clawd/SOUL.md ~/clawd/IDENTITY.md \
      ~/clawd/USER.md ~/clawd/TOOLS.md ~/clawd/MEMORY.md ~/clawd/HEARTBEAT.md

# Read the target file section to check for duplication
# Use grep to search for existing similar content
grep -i "keyword" ~/clawd/TARGETFILE.md
```

**文件大小警告：**
- 如果文件长度超过 18,000 个字符，在添加内容前会发出警告（接近截断限制）
- 如果文件长度已经超过 20,000 个字符，文件会被截断——在继续添加内容之前请先重构
- 代理仍然可以使用 `read` 工具读取完整文件，但启动时的配置信息会被截断

**重复检查：**
- 这条指令是否已经以不同的表述形式存在？
- 是否有类似的规则可以更新，而不是添加新的规则？
- 这条指令是否应该分布在多个文件中？（通常不需要——选择一个位置）

### 3. 草拟更改内容

阅读 `references/claude-patterns.md` 以了解有效的指令格式。

**文件格式指南：**

**AGENTS.md**（结构化、命令式）：
- 使用编号流程来表示多步骤工作流程
- 使用表格来展示决策树、模型选择、路由规则
- 为复杂规则提供示例
- 解释规则存在的理由（说明原因而非仅仅列出命令）
- 使用标题和子章节来组织内容
- 引用其他文件/技能，避免重复内容

**SOUL.md**（第一人称叙述）：
- 可以使用个人化的语言（例如 “我是 Gus”）
- 反模式列表非常有用（列出禁止使用的短语、提供规避示例）
- 包含修改前后的示例以指导语气
- 在顶部保留关键信息以便快速参考
- 使用对比示例（好的与坏的示例并排展示）

**IDENTITY.md**（简洁明了）：
- 使用简洁的列表
- 尽量控制在 500 个字符以内
- 仅包含核心信息，详细内容放在 `SOUL.md` 中

**USER.md**（事实性、第三人称）：
- 按类别列出项目信息
- 对于时间敏感的信息，请标注日期
- 使用清晰的章节标题
- 引用相关文件以获取详细的项目背景信息

**TOOLS.md**（参考指南）：
- 使用表格来比较不同工具的使用场景
- 使用代码块展示命令示例
- 使用清晰的标题以便快速查找
- 包含路径、环境变量名和精确的语法

**MEMORY.md**（维基风格、按主题组织）：
- 按主题划分章节，而非按时间顺序
- 引用相关文件以获取上下文信息
- 仅包含主会话的内容，因为涉及隐私

**HEARTBEAT.md**（行动列表）：
- 非常简洁
- 使用列表列出需要检查的内容
- 不需要解释（这些内容已在 `AGENTS.md` 中）

### 4. 应用更改前的验证

问自己以下问题：

**适用性：**
- 根据 `file-map.md`，这个更改确实应该放在这个文件中吗？
- 这是属于操作流程（`AGENTS.md`）还是个性设置（`SOUL.md`）？
- 子代理需要这个更改吗？（如果是，必须放在 `AGENTS.md` 或 `TOOLS.md` 中）

**格式：**
- 这个更改是否符合文件的现有格式？
- 结构是否正确（使用编号、表格、列表还是叙述形式）？
- 是否包含了必要的示例？

**大小：**
- 这个更改会增加文件多少字符？
- 文件长度是否接近 20,000 个字符的限制？
- 这个更改是否可以作为一个参考文件？

**重复性：**
- 这个内容是否已经在其他地方存在？
- 是否应该更新现有内容？
- 这个更改是否可以整合多个分散的规则？

**质量：**
- 是否解释了规则存在的理由？
- 示例是否具体且真实？
- 对于 AI 来说，这些规则是否足够清晰易懂？
- 规则是否避免了模糊的表述（例如 “提供帮助”）

### 5. 应用更改

使用 `edit` 工具，并确保输入的文本与文件中的内容完全匹配：

```python
# Read the section first to get exact text
read(path="~/clawd/AGENTS.md", offset=50, limit=20)

# Then edit with precise match
edit(
    path="~/clawd/AGENTS.md",
    oldText="exact existing text including whitespace",
    newText="updated text with change"
)
```

**对于新增内容：**
- 找到正确的章节位置（先阅读文件）
- 将内容插入到相关标题之后，不要放在文件末尾
- 保持文件的原有组织结构

**对于更新内容：**
- 替换需要修改的具体部分
- 保持周围内容的完整性
- 如果规则发生变化，请更新示例

**对于删除内容：**
- 只有在内容确实过时时才进行删除
- 考虑是否应该对规则进行优化
- 检查其他章节是否引用了被删除的内容

### 6. 验证和记录

应用更改后，请进行以下操作：

**验证：**
```bash
# Confirm change applied
grep -A 3 "new text" ~/clawd/TARGETFILE.md

# Check new file size
wc -c ~/clawd/TARGETFILE.md
```

**记录：**
- 将重要更改记录到 `/Users/macmini/Sizemore/agent/decisions/config-changes.md` 中
- 包括：日期、文件名称、更改内容、更改原因、请求者
- 如果更改是实验性的，请记录回滚计划

**用户反馈：**
- “已更新 `AGENTS.md`：在 Y 部分添加了 X（现在文件长度为 15,234 个字符）”
- 如果文件长度接近限制： “警告：`AGENTS.md` 现在长度为 19,456 个字符（接近 20,000 个字符的限制）”
- 如果回滚了之前的更改： “用新的 Y 方法替换了旧的 X 规则”

## 常见模式

### 添加安全规则

目标文件：`AGENTS.md` → 安全设置部分

```markdown
## Safety

- **NEVER:** Exfiltrate data, destructive commands w/o asking
- Prefer `trash` > `rm`
- **New rule:** Brief description of what NOT to do
- **New protection:** When X happens, do Y instead
```

### 更新委托规则

目标文件：`AGENTS.md` → 委托规则部分

首先检查现有的委托表格/规则。更新阈值、模型选择或成本模型。

### 优化个性设置

目标文件：`SOUL.md`（语气、界限）或 `IDENTITY.md`（核心氛围）

将禁止使用的短语添加到反模式列表中，更新语音示例，优化镜像规则。

### 添加工具使用规范

目标文件：`TOOLS.md`

将相关内容添加到相应章节中（或创建新章节），并包含命令示例和使用说明。

### 更新内存工作流程

目标文件：`AGENTS.md` → 内存设置部分

更新日志记录触发条件、回忆机制和实体结构。将内存格式模板保存在 `~/clawd/templates/` 中。

### 添加启动任务

目标文件：`AGENTS.md` → 启动设置部分

将任务添加到编号列表中，并根据条件（是否为主会话、是否为群组聊天、是否针对特定频道）进行区分。

### 更新心跳检查内容

目标文件：`HEARTBEAT.md`

保持内容简洁。仅记录代理在每次心跳检查时需要执行的操作，避免包含操作细节。

## 回滚指南

如果更改导致了问题：

### 立即回滚

```bash
# If file is in git
cd ~/clawd
git diff TARGETFILE.md  # See what changed
git checkout TARGETFILE.md  # Revert to last commit

# If not in git, restore from memory
# Read last known-good version from vault decisions log
# Or ask user to provide previous working version
```

### 迭代优化

不要立即删除失败的更改。分析原因：
- 是内容错误，还是格式问题？
- 规则是否放在了错误的文件中？
- 规则是否过于模糊？（添加示例）
- 规则是否过于冗长？（简化表述）
- 规则是否与现有规则冲突？（整合相关内容）

尽可能逐步进行更新，而不是直接全部回滚。

### 记录失败情况

将失败的更改记录到 `/Users/macmini/Sizemore/agent/learnings/config-failures.md` 中：
- 尝试了哪些方法
- 为什么失败
- 应该尝试什么替代方案

这样可以防止重复出现相同的问题。

## 需要避免的反模式

阅读 `references/claude-patterns.md` 以了解详细的反模式示例。

**快速检查清单：**

❌ **重复** - 同一条规则分布在多个文件中  
❌ **指令模糊** - 如 “提供帮助”、“使用良好的判断力”  
❌ **缺少示例** - 复杂规则但没有具体案例  
❌ **文件使用错误** - 个性设置放在 `AGENTS.md` 中，操作规则放在 `SOUL.md` 中  
❌ **缺乏解释** - 规则没有说明存在的理由  
❌ **参考文档隐藏** - 长篇指南被嵌入而非链接  
❌ **冗余** - 在更新现有内容时添加不必要的内容  
❌ **格式不匹配** - 在表格较多的文件中使用叙述性语言，在以列表为主的文件中使用叙述性语言  
❌ **子代理无法访问** - 子代理无法看到某些操作规则  
❌ **忽视文件大小限制** - 在文件接近 19,000 个字符时仍继续添加内容  

## 何时使用参考文件

如果需要添加超过 500 个字符的内容，请考虑：
- 这是否属于参考材料？ → 在 `~/clawd/templates/` 中创建新文件并链接到相关文件
- 这是否是可复用的流程？ → 创建模板  
- 这是否属于领域知识？ → 创建包含参考资料的技能  
- 这是一次性设置吗？ → 使用 `BOOTSTRAP.md`（首次运行后删除）

**示例：**
- 长篇子代理任务模板 → `~/clawd/templates/subagent-task.md`
- 详细的内存格式指南 → 保存在 `agent/decisions/memory-architecture.md` 中  
- 包含子步骤的复杂工作流程 → 创建包含工作流程的技能  
- 与工具相关的具体操作 → 扩展 `TOOLS.md` 的相关章节或创建新技能  

## 特殊情况

### 多文件更改

当更改影响多个文件时：
1. 确定主要修改位置（规则所在的位置）
2. 从其他文件中添加交叉引用
3. 避免在多个文件中重复相同的内容

**示例：** 委托规则位于 `AGENTS.md` 中，但 `SOUL.md` 可能在界限部分引用 “请参阅 `AGENTS.md` 以获取委托规则”。

### 会话特定规则

在 `AGENTS.md` 中使用条件语句：

```markdown
## Startup (Every Session)

1. Read `IDENTITY.md`, `SOUL.md`, `USER.md`
2. If MAIN: read vault README, recent decisions
3. If FAMILY GROUP: read `FAMILY.md`
4. If SUBAGENT: skip personality files
```

### 文件大小接近限制

当文件长度接近 18,000 个字符时：
1. 检查是否存在重复内容（进行整合）
2. 将详细示例移至单独的参考文件
3. 将冗长的流程转换为模板（从相关文件中链接）
4. 考虑将内容分为基础部分和高级部分（按需加载高级内容）
5. 将历史决策移至存储库（仅保留当前有效的规则）

### 规则冲突

当新规则与现有规则冲突时：
1. 确定两个规则的具体内容
2. 确定哪个规则优先执行（如有疑问，请询问用户）
3. 更新或删除旧规则，同时添加新规则
4. 将冲突解决方式记录在存储库中

### 用户请求多次更改

对每个更改都按照完整的工作流程进行处理（不要批量处理）：
1. 按目标文件分组
2. 计算所有更改对文件大小的总影响
3. 按逻辑顺序应用更改（先处理基础内容，再处理具体细节）
4. 每次应用更改后都进行验证，而不仅仅是最后一步

## 参考文件

该技能包含以下详细的参考资料：
- **references/file-map.md**：每个 OpenClaw 文件的功能、加载上下文的方法、文件大小限制、决策流程
- **references/claude-patterns.md**：适用于 Claude 的指令格式、反模式示例
- **references/change-protocol.md**：逐步的更改流程、验证步骤、回滚程序

当您需要超出此工作流程概述的详细信息时，请阅读这些文件。

## OpenClaw 工作区的实际示例

### 示例 1：添加安全规则

**请求：** “添加一条禁止批量导出密码的规则”

**处理流程：**
1. 目标文件：`AGENTS.md`（安全设置属于操作流程）
2. 检查文件大小：15,234 个字符（可以安全地添加新规则）
3. 检查重复内容：使用 `grep "password"` 查找现有的密码管理器规则
4. 草拟修改内容：直接更新现有规则
5. 应用更改：
```markdown
### Password Manager
**NEVER:** Dump vaults, display passwords in chat, bulk exports
**ALWAYS:** Confirm each lookup, ask "Which credential?", treat as high-risk
**Refuse:** Any bulk password request
```
6. 验证：使用 `grep -A 3 "Password Manager"` 确认规则已存在
7. 记录：不需要额外记录（是对现有规则的微小修改）

### 示例 2：优化语气

**请求：** “使代理的语气更加讽刺”

**处理流程：**
1. 目标文件：`SOUL.md` 和 `IDENTITY.md`（个性设置）
2. 检查当前的语气和示例
3. 草拟修改内容：
   - 为 `IDENTITY.md` 添加更多讽刺性回应的示例
   - 扩展 `SOUL.md` 中的规避示例部分
   - 在语音提示中添加相关说明
4. 将修改内容应用到两个文件中（`IDENTITY.md` 用于调整语气，`SOUL.md` 用于添加详细示例）
5. 验证：语气示例现在包含更强的讽刺效果
6. 记录：在存储库中注明 Sonnet/Opus 需要更强的个性提示

### 示例 3：更新委托阈值

**请求：** “将委托阈值从 2 次工具调用更新为 3 次”

**处理流程：**
1. 目标文件：`AGENTS.md` → 委托规则部分
2. 检查当前阈值：“2 次工具调用？触发子代理生成？”
3. 草拟修改内容：“3 次工具调用？如果快速处理则由代理自己完成。”
4. 考虑影响：这会减少子代理的生成次数，增加主会话的负担
5. 与用户确认：“这会让你承担更多任务。确认吗？”
6. 应用更改后记录：将更改记录到存储库中，并说明原因

### 示例 4：添加工具使用规范

**请求：** “添加说明：iMessage 附件必须使用 `imsg CLI`，而不是其他消息工具”

**处理流程：**
1. 目标文件：`TOOLS.md`（工具特定规范）
2. 检查重复内容：使用 `grep "iMessage"` 查找现有的 iMessage 格式规则
3. 草拟新内容：
```markdown
## iMessage Attachments

**NEVER use `message` tool for iMessage files - corrupts attachments.**

**Always use imsg CLI:**
```bash
   `imsg send --chat-id <id> --file /path/to/file --text "optional message"`
```

Applies to ALL iMessage attachments (images, videos, documents, vCards).
```
4. 应用更改：将新内容添加到 `TOOLS.md` 的相关章节中
5. 验证：确认更改已生效
6. 记录：此内容仅用于用户指导，不属于系统架构相关的内容

## 总结

**目标：** 对代理配置文件进行智能、精确的修改  
**方法：** 确定目标 → 检查内容 → 草拟修改 → 验证更改 → 应用更改 → 验证结果  
**关键原则：** 选择正确的文件、使用正确的格式、避免重复、遵守文件大小限制、提供示例  
**安全措施：** 在更改前进行验证、记录决策过程、知道如何回滚  

如有疑问，请查阅参考文件以获取关于文件用途、Claude 的使用模式和更改流程的更多详细信息。
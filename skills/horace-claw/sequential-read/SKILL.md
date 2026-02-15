---
name: sequential-read
description: "按顺序阅读正文，并结合结构化的思考来进行理解，以模拟阅读体验。"
metadata: {"openclaw":{"emoji":"📖","requires":{"bins":["python3"]}}}
---

# 📖 顺序阅读

通过分块读取文本（小说、非小说类作品、文章），并逐步构建结构化的阅读反馈。输出内容会展示你在阅读过程中的观点变化——哪些预测是错误的，哪些问题得到了解答，哪些观点发生了转变——而不仅仅是一个事后的总结。

## 使用方法

| 命令 | 描述 |
|---|---|
| `/sequential-read <文件路径>` | 运行完整的阅读会话 |
| `/sequential-read <文件路径> --lens <视角>` | 以特定的视角进行阅读（例如：“怀疑论者”、“文学评论家”、“学生”） |
| `/sequential-read list` | 列出所有阅读会话 |
| `/sequential-read show <会话ID>` | 显示已完成会话的阅读总结 |

## 执行模型

**该流程由多个子代理进程协同完成。** 阅读长篇小说的过程分为两个阶段：首先是主要阅读代理处理大部分文本内容，然后是完成代理处理剩余的文本并生成阅读总结。这是正常流程，不属于错误情况。

当用户执行 `/sequential-read` 命令时：
1. 解析命令以获取文件路径和可选的阅读视角。
2. 预先创建阅读会话：
   ```bash
   python3 {baseDir}/scripts/session_manager.py create <source-file>
   ```
3. 启动 **主要阅读代理**：
   ```
   sessions_spawn with label: reader-{session-id}
   Tell the agent: "Session already exists at {session-id}. Do NOT create it again."
   ```
4. 通知用户阅读会话已开始，并在完成后再次通知他们。
5. **当主要阅读代理返回时**（无论是否完成阅读）：
   - 检查会话状态：`python3 {baseDir}/scripts/session_manager.py get <会话ID>`
   - 检查已生成的反馈数量与总文本块数。
   - **如果已生成总结：** 显示阅读结果。
   - **如果还有未处理的文本块或总结缺失：** 启动 **完成代理**（详见下文）。这是阅读长篇小说时的标准流程。
6. 完成代理返回后，显示阅读总结和会话路径。

### 两阶段阅读模式

对于长篇小说（通常包含20个以上的文本块），主要阅读代理会处理大约17-20个文本块后结束会话。这是**正常现象**，不属于错误。完成代理会处理剩余的2-5个文本块，并结合之前的所有反馈生成完整的阅读总结。

**启动完成代理的流程：**
```
sessions_spawn with label: finisher-{session-id}, model: "opus"
Task: "Resume reading session {session-id} at {baseDir path}.
  Read reflections written so far to understand context.
  Continue from chunk N (the next unwritten chunk).
  Write remaining reflections, then run synthesis.
  Session path: {session-path}"
```

**在主要阅读代理和完成代理之间不要等待或询问用户**。如果主要阅读代理没有生成总结就直接启动完成代理。整个流程应该是自动化运行的。

## 脚本路径

所有Python脚本位于 `{baseDir}/scripts/` 目录下：
- `{baseDir}/scripts/session_manager.py`
- `{baseDir}/scripts/chunk_manager.py`
- `{baseDir}/scripts/state_manager.py`

模板文件位于 `{baseDir}/templates/` 目录下：
- `{baseDir}/templates/reflection_prompt.md`
- `{baseDir}/templates/synthesis_prompt.md`

## 命令说明

### `/sequential-read <文件路径> [--lens <视角>]`

#### 1. 创建或恢复会话

```bash
python3 {baseDir}/scripts/session_manager.py create <source-file> [--lens <persona>]
```

该命令会自动检测是否已有相同的文件路径的阅读会话：
- 如果存在正在进行的会话，它会显示当前的会话ID和路径。
- 否则，它会创建一个新的会话。
从输出的第一行中获取会话ID。

#### 2. 检查会话状态（用于恢复会话）

```bash
python3 {baseDir}/scripts/session_manager.py get <session-id>
```

根据 `status` 字段决定如何继续阅读：
| 状态 | 操作 |
|---|---|
| `preread` | 从头开始执行预读阶段 |
| `chunked` | 继续执行阅读阶段（从当前块开始） |
| `read` | 执行总结阶段 |
| `complete` | 显示现有的阅读总结 |

#### 3. 运行整个流程

**对于新会话或 `preread` 状态：**

执行预读脚本（`{baseDir}/preread/SKILL.md`），参数如下：
- `SESSION_ID`：会话ID
- `SOURCE_FILE`：源文本路径
- `BASE_DIR`：脚本目录

**对于 `chunked` 状态（或预读阶段完成后）：**

执行阅读脚本（`{baseDir}/reading/SKILL.md`），参数如下：
- `SESSION_ID`：会话ID
- `BASE_DIR`：脚本目录
- `LENS`：阅读视角（可选）

**对于 `read` 状态（或阅读完成后）：**

执行总结脚本（`{baseDir}/synthesis/SKILL.md`），参数如下：
- `SESSION_ID`：会话ID
- `BASE_DIR`：脚本目录

#### 4. 显示阅读结果

阅读总结完成后，向用户提供：
- 完整的阅读总结文本
- 会话路径：`memory/sequential_read/<会话ID>/`
- 说明：已处理的文本块数量，以及是否使用了特定的阅读视角

### `/sequential-read list`

```bash
python3 {baseDir}/scripts/session_manager.py list
```

将阅读结果输出给用户。

### `/sequential-read show <会话ID>`

```bash
python3 {baseDir}/scripts/session_manager.py get <session-id>
```

如果会话状态为 `complete`，则显示阅读总结：
```
memory/sequential_read/<session-id>/output/synthesis.md
```

如果会话未完成，则显示会话状态和阅读进度。

## 模型选择指南

阅读阶段是最耗时的部分——需要多次迭代，并且必须保持阅读质量。根据文本长度选择合适的模型：
| 文本长度 | 推荐模型 | 选择理由 |
|---|---|---|
| 长篇小说（1万行以上，20个以上文本块） | **Opus** | 能在多次迭代中保持阅读质量；较大的上下文窗口有助于处理累积的信息 |
| 中篇小说/长篇文章（3000-1万行） | Opus 或 Sonnet | 两者均可；如果文本块数量少于15个，使用 Sonnet 也可行 |
| 短文/小文章（少于3000行） | Sonnet | 文本块较少，上下文易于管理 |

在启动子代理时，需要明确指定模型：对于长篇小说，使用 `model: "opus"`。

**原因说明：** 较简单的模型在长时间阅读过程中性能会下降——随着上下文信息的积累，阅读反馈的质量会下降。在一篇包含35个文本块的长篇小说中使用 Sonnet 模型时，仅生成了4条有意义的反馈和31条占位符。长篇小说需要使用 Opus 模型。

**文本块大小：** 文本分割器通常将每个文本块分割成约550行（范围200-700行）。对于典型的长篇小说（约1万-1.2万行），这会产生大约20个文本块。更长的文本（超过1.5万行）可能会产生35个以上的文本块，此时需要启动完成代理。

**两阶段阅读模式是标准流程。** 对于长篇小说（20个以上文本块），阅读完成后一定会启动完成代理。主要阅读代理处理大约80-90%的文本块，完成代理处理剩余的文本块并生成总结。对于非常长的文本（超过35个文本块），主要阅读代理可能只能处理25个左右的文本块。请据此进行规划——这是正常流程，不属于错误处理情况。

**预先创建会话：** 在启动子代理之前，务必使用 `session_manager.py create` 命令创建会话。告知代理该会话已存在，避免重复创建导致的错误。

## 阅读代理的设置（可选）

如果你维护了 **阅读上下文文件**（包含角色信息、主题线索、批判性分析框架等），可以将这些文件作为前言加载到子代理的任务中。这有助于用户在阅读系列作品时保持阅读的连贯性。

在启动子代理时，将这些上下文信息包含在任务参数中：
```
"Before you begin reading, here is your accumulated reader context:

=== READING CONTEXT ===
[contents of reader-mind file]

Now read [book title]..."
```

**阅读总结完成后：** 使用新的角色信息、主题线索更新和交叉参考结果来更新阅读上下文文件。每份文件的更新内容应控制在4000字以内。

## 阅读代理的重要规则

- **禁止预览后续内容。** 每条阅读反馈都必须基于“不知道接下来会发生什么”的视角来撰写，不得引用后续文本块的内容。
- **保持真实性。** 混乱、无聊、兴奋或不同意等情绪都是正常的反应。无需刻意伪装。
- **在修改反馈时具体说明原因。** 例如：“我对X的看法是错误的，因为Y。”比“我的观点发生了变化”更准确。
- **阅读视角仅供参考。** 如果某个文本块使用特定的阅读视角显得生硬，应在反馈中说明这一点，而不是强行应用该视角。
- **自主运行。** 在处理不同文本块之间不要询问用户问题。整个流程应该是自动化运行的。
- **保存所有数据。** 在处理下一个文本块之前，将所有的反馈和状态更新保存到磁盘上，以便在阅读中断后能够继续阅读。

## 合成结果的处理

阅读总结完成后，你可以将其整合到任何你希望使用的工作流程中——博客文章、阅读日志、知识图谱、系列作品跟踪器等。`output/synthesis.md` 文件是独立且可移植的。
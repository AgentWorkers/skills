---
name: turix-mac
description: **Computer Use Agent (CUA)：用于 macOS 的自动化工具（基于 TuriX）**  
当您需要在桌面上执行可视化任务（如打开应用程序、点击按钮或导航没有 CLI 或 API 的用户界面）时，可以使用 Computer Use Agent (CUA)。
---

# TuriX-Mac 技能

该技能允许 Clawdbot 通过 TuriX 计算机使用代理（TuriX Computer Use Agent）来可视化地控制 macOS 桌面。

## 使用场景

- 当需要让 Clawdbot 在 Mac 桌面上执行操作时（例如：“打开 Spotify 并播放我喜欢的歌曲”）。
- 在没有命令行界面的应用程序中进行导航时。
- 对于需要多步骤操作的可视化工作流程（例如：“在我的电子邮件中找到最新的发票并将其上传到公司门户”）。
- 当您希望代理能够自主规划、推理并执行复杂任务时。

## 主要特性

### 🤖 多模型架构
TuriX 采用了一种复杂的多模型系统：
- **大脑（Brain）**：理解任务并生成详细的步骤计划。
- **执行器（Actor）**：根据视觉理解执行精确的用户界面操作。
- **规划器（Planner）**：在 `use_plan: true` 时协调高级任务分解。
- **内存（Memory）**：在任务步骤之间保持上下文。

### 📋 技能系统
技能是通过 markdown 编写的脚本，用于指导代理在特定领域中的行为：
- `github-web-actions`：GitHub 导航、仓库搜索、添加星标等操作。
- `browser-tasks`：通用网页浏览器操作。
- 可以在 `skills/` 目录中添加自定义技能。

### 🔄 恢复中断任务的能力
通过设置一个稳定的 `agent_id`，代理可以恢复中断的任务。

## 运行 TuriX

### 基本任务
```bash
skills/local/turix-mac/scripts/run_turix.sh "Open Chrome and go to github.com"
```

### 恢复中断的任务
```bash
skills/local/turix-mac/scripts/run_turix.sh --resume my-task-001
```

> ✅ **注意**：`run_turix.sh` 会自动更新 `examples/config.json` 文件（包括任务信息、恢复设置、`use_plan` 和 `use_skills`）。如果您希望保留手动编辑的配置文件，请跳过传递任务直接编辑 `examples/config.json`。

### 有效任务的提示

**✅ 正确的示例：**
- “打开 Safari，访问 google.com，搜索‘TuriX AI’，然后点击第一个结果”。
- “打开系统设置，点击‘暗黑模式’，然后再返回系统设置”。
- “打开 Finder，导航到‘文档’文件夹，创建一个名为‘Project X’的新文件夹”。

**❌ 应避免的指令：**
- 含糊不清的指令（如“帮我”或“修复这个问题”）。
- 不可执行的操作（如“删除所有文件”）。
- 需要系统级权限的操作（且未给出相应提示）。

**💡 最佳实践：**
1. 明确指定目标应用程序。
2. 将复杂任务分解为清晰的步骤，但不要提及屏幕上的具体位置。

## 快捷键

- **强制停止**：`Cmd+Shift+2` - 立即停止代理。

## 监控与日志

日志文件保存在项目目录下的 `.turix_tmp/logging.log` 中。日志中包含：
- 详细的执行步骤。
- LLM（大型语言模型）的交互和推理过程。
- 错误信息及恢复尝试。

## 重要说明

### TuriX 的运行方式
- 可以通过 `clawdbot exec` 命令以 `pty:true` 模式启动 TuriX。
- 首次启动时需要 2-5 分钟来加载所有 AI 模型（大脑、执行器、规划器、内存）。
- 背景输出会被缓冲——直到任务完成或停止后才会显示实时进度。

### 运行前的准备
**务必先设置 PATH 环境变量：**
```bash
export PATH="/usr/sbin:$PATH"
cd your_dir/TuriX-CUA
/opt/anaconda3/envs/turix_env/bin/python examples/main.py
```

**原因？** `screencapture` 工具位于 `/usr/sbin/screencapture`，该路径不在默认的 PATH 中。

### 检查 TuriX 是否正在运行
```bash
# Check process
ps aux | grep "python.*main" | grep -v grep

# Should show something like:
# user  57425  0.0  2.4 412396704 600496 s143  Ss+  5:56PM   0:04.76 /opt/anaconda3/envs/turix_env/bin/python examples/main.py
```

**注意**：`.turix_tmp` 目录可能只有在 TuriX 开始执行任务后才会被创建。

## 故障排除

### 常见问题及解决方法

| 错误 | 解决方案 |
|-------|----------|
| `NoneType has no attribute 'save'` | 缺少屏幕录制权限。请在系统设置中授权后重启终端。 |
| `Screen recording access denied` | 运行：`osascript -e 'tell application "Safari" to do JavaScript "alert(1)"'`，然后点击“允许”按钮。 |
| 未找到 Conda 环境 | 确保 `turix_env` 存在：`conda create -n turix_env python=3.12` |
| 模块导入错误 | 激活环境：`conda activate turix_env`，然后 `pip install -r requirements.txt` |
| 键盘监听器的权限问题 | 将终端/IDE 添加到 **Accessibility** 权限设置中。

### 调试模式

日志默认为 DEBUG 级别。可以通过以下方式查看详细信息：
```bash
tail -f your_dir/TuriX-CUA/.turix_tmp/logging.log
```

## 架构

```
User Request
     ↓
[Clawdbot] → [TuriX Skill] → [run_turix.sh] → [TuriX Agent]
                                              ↓
                    ┌─────────────────────────┼─────────────────────────┐
                    ↓                         ↓                         ↓
               [Planner]                 [Brain]                  [Memory]
                    ↓                         ↓                         ↓
                                         [Actor] ───→ [Controller] ───→ [macOS UI]
```

## 技能系统详情

技能文件是位于 `skills/` 目录中的 markdown 文件，文件开头包含 YAML 标头：

```md
---
name: skill-name
description: When to use this skill
---
# Skill Instructions
High-level workflow like: Open Safari,then go to Google.
```

规划器会根据技能的名称/描述来选择合适的技能；大脑则会使用技能的完整内容来指导执行过程。

## 高级选项

| 选项 | 描述 |
|--------|-------------|
| `use_plan: true` | 启用复杂任务的规划功能。 |
| `use_skills: true` | 启用技能选择功能。 |
| `resume: true` | 从上次中断处恢复任务。 |
| `max_steps: N` | 限制总步骤数（默认值：100）。 |
| `max_actions_per_step: N` | 每步允许执行的操作数量（默认值：5）。 |
| `force_stop_hotkey` | 自定义用于停止代理的快捷键。 |

---

## TuriX 技能系统

TuriX 支持 **技能**：这些 markdown 脚本可以帮助代理在特定领域中更可靠地执行任务。

### 1. 内置技能

| 技能 | 用途 |
|-------|-----|
| `github-web-actions` | GitHub 相关操作（搜索仓库、添加星标等）。 |

### 2. 创建自定义技能

在 TuriX 项目的 `skills/` 目录下创建一个 `.md` 文件：

```md
---
name: my-custom-skill
description: When performing X specific task
---
# Custom Skill

## Guidelines
- Step 1: Do this first
- Step 2: Then do that
- Step 3: Verify the result
```

**字段定义：**
- `name`：技能的标识符（规划器用于选择该技能）。
- `description`：指定该技能的使用场景（规划器根据此描述进行匹配）。
- 此后的内容为完整的执行指南（由大脑模块使用）。

### 3. 启用技能

在 `examples/config.json` 文件中进行配置：

```json
{
  "agent": {
    "use_plan": true,
    "use_skills": true,
    "skills_dir": "skills",
    "skills_max_chars": 4000
  }
}
```

### 4. 使用技能执行任务

```bash
skills/local/turix-mac/scripts/run_turix.sh "Search for turix-cua on GitHub and star it"
```

代理会自动执行以下操作：
1. 规划器读取技能的名称和描述。
2. 选择相关的技能。
3. 大脑模块使用技能的完整内容来指导执行过程。

### 5. 中文文本处理

**背景说明：**
通过 shell 插值传递中文文本可能会导致 UTF-8 编码问题，且将不可信的文本插入 heredoc（一种markdown 格式）中是不安全的。

**解决方案：**
`run_turix.sh` 脚本使用 Python 正确处理 UTF-8 编码，并从环境变量中读取任务文本：

```python
import json

# Read with UTF-8
with open(config_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write without escaping non-ASCII text
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**关键点：**
1. 读写文件时始终使用 `encoding='utf-8'`。
2. 使用 `ensure_ascii=False` 以保留非 ASCII 字符。
3. 通过环境变量或标准输入（stdin）传递任务内容，并使用单引号括起来的 heredoc 格式来避免 shell 插值。

### 6. 文档创建的最佳实践

**挑战：**
- 要求 TuriX 收集信息后直接创建并发送文档。
- TuriX 是一个图形界面代理，因此执行速度可能较慢且结果不够稳定。建议仅在 Clawdbot 无法完成的任务或 TuriX 能够更快完成任务的情况下使用它。

**推荐方法：** 先自行创建文档，再让 TuriX 发送：
1. 使用 `python-docx` 创建 Word 文档。
2. 仅让 TuriX 负责发送文件。

```python
from docx import Document
doc = Document()
doc.add_heading('Title')
doc.save('/path/to/file.docx')
```

**建议的工作流程：**
1. 使用 `web_fetch` 收集信息。
2. 使用 Python 创建 Word 文档。
3. 使用 TuriX 发送文件。需要指定文件的路径，并明确指示发送文件的位置（而不仅仅是文件名）。
4. 如果确实需要 TuriX 手动创建 Word 文档并输入收集到的信息，可以将内容放入技能文件中（对于大量数据），或直接在任务描述中说明（对于少量数据）。

### 7. 示例：添加新技能

创建 `skills/browser-tasks.md` 文件：

```md
---
name: browser-tasks
description: When performing tasks in a web browser (search, navigate, fill forms).
---
# Browser Tasks

## Navigation
- Use the address bar or search box to navigate
- Open new tabs for each distinct task
- Wait for page to fully load before proceeding

## Forms
- Click on input fields to focus
- Type content clearly
- Look for submit/button to complete actions

## Safety
- Confirm before submitting forms
- Do not download files without user permission
```

### 8. 技能开发技巧

1. **描述要准确**——有助于规划器正确选择技能。
2. **步骤要清晰**——大脑模块需要明确的指导。
3. **包含安全检查**——对重要操作进行确认。
4. **保持简洁**——建议描述长度不超过 4000 个字符。

---

## 监控与调试指南

### 1. 运行任务

```bash
# Run in background (recommended)
cd your_dir/clawd/skills/local/turix-mac/scripts
./run_turix.sh "Your task description" --background

# Or use timeout to set a max runtime
./run_turix.sh "Task" &
```

### 2. 监控进度

**方法 1：查看会话日志**
```bash
# List running sessions
clawdbot sessions_list

# View history
clawdbot sessions_history <session_key>
```

**方法 2：查看 TuriX 日志**
```bash
# Tail logs in real time
tail -f your_dir/TuriX-CUA/.turix_tmp/logging.log

# Or inspect completed step files
ls -lt your_dir/TuriX-CUA/examples/.turix_tmp/brain_llm_interactions.log_brain_*.txt
```

**方法 3：检查进程**
```bash
ps aux | grep "python.*main.py" | grep -v grep
```

**方法 4：检查生成的文件**
```bash
# List files created by the agent
ls -la your_dir/TuriX-CUA/examples/.turix_tmp/*.txt
```

### 3. 日志文件说明

| 文件 | 说明 |
|------|-------------|
| `logging.log` | 主日志文件。 |
| `brain_llm_interactions.log_brain_N.txt` | 大脑模型的交互记录（每个步骤对应一个文件）。 |
| `actor_llm_interactions.log_actor_N.txt` | 执行器的交互记录（每个步骤对应一个文件）。 |

**关键日志标记：**
- `📍 步骤 N` - 新步骤开始。
- `✅ 评估结果：成功/失败` - 当前步骤的评估结果。
- `🎯 本步骤的目标` - 当前需要完成的目标。
- `🛠️ 执行的操作` - 执行的操作。
- `✅ 任务成功完成` - 任务已完成。

### 4. 常见监控问题及解决方法

| 问题 | 检查方法 |
|-------|-------|
| 进程无响应 | 使用 `ps aux | grep main.py` 命令查看进程状态。 |
- 卡在第一步 | 检查 `.turix_tmp/` 目录是否已创建。 |
- 模型加载缓慢 | 首次启动时可能需要 1-2 分钟来加载模型。 |
- 无日志输出 | 查看 `config.json` 中的 `logging_level` 设置。

### 5. 强制停止

**快捷键**：`Cmd+Shift+2` - 立即停止代理。

**命令：**
```bash
pkill -f "python examples/main.py"
```

### 6. 查看结果

任务完成后，代理会：
1. 在 `.turix_tmp/` 目录中生成交互日志。
2. 如果启用了 `record_info` 功能，还会生成记录文件。
3. 将截图保存在内存中以供后续步骤使用。

**示例：查看摘要文件**
```bash
cat your_dir/TuriX-CUA/examples/.turix_tmp/latest_ai_news_summary_jan2026.txt
```

### 7. 调试技巧

1. **检查大脑模型的推理过程**：查看 `brain_llm_interactions.log_brain_*.txt` 文件中的 `analysis` 和 `next_goal` 内容。
2. **检查执行器的操作**：查看 `actor_llm_interactions.log_actor_*.txt` 文件中的操作记录。
3. **查看截图**：TuriX 会在每个步骤后捕获截图（保存在内存中）。
4. **查看记录文件**：代理使用 `record_info` 将关键信息保存到 `.txt` 文件中。

### 8. 监控流程示例**

```bash
# 1. Run a task
./run_turix.sh "Search AI news and summarize" &

# 2. Wait a few seconds and check the process
sleep 10 && ps aux | grep main.py

# 3. Check if logs are being created
ls -la your_dir/TuriX-CUA/examples/.turix_tmp/

# 4. Tail progress in real time
tail -f your_dir/TuriX-CUA/.turix_tmp/logging.log

# 5. Check current step count
ls your_dir/TuriX-CUA/examples/.turix_tmp/brain_llm_interactions.log_brain_*.txt | wc -l
```
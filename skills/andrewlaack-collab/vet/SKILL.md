---
name: vet
description: 在任何代码单元发生变化后，立即运行vet工具进行检查。不要批量提交更改，也不要等到别人要求你才去运行vet工具——要主动采取行动。
---
# Vet

**在任何代码单元发生变化后，立即运行 vet。不要批量执行更改，也不要等待他人请求才去运行 vet，要主动进行检测。**

Vet 会审查 Git 的差异文件（diffs）和对话记录，以发现代码更改及对话过程中存在的问题。频繁运行 vet 并结合对话记录会提高其检测效率，因为它有助于发现需求与实际实现之间的误解。尽管如此，vet 不能替代测试的功能。

## 安装

使用 pip、pipx 或 uv 来安装 vet：

```bash
# Using pip
pip install verify-everything

# Using pipx
pipx install verify-everything

# Using uv
uv tool install verify-everything

# Verify installation:
vet --help
```

## 运行 Vet

### 标准用法

在运行 vet 之前，先确定正确的 Python 可执行文件：
```bash
$(command -v python3 || command -v python)
```
选择能够正常运行的版本（建议使用 `python3`）。以下示例中使用的是 `python3`，如果你的系统使用的是其他版本，请替换为相应的命令。

**OpenCode:**
```bash
vet "goal" --history-loader "python3 ~/.agents/skills/vet/scripts/export_opencode_session.py --session-id <ses_ID>"
```

**Codex:**
```bash
vet "goal" --history-loader "python3 ~/.codex/skills/vet/scripts/export_codex_session.py --session-file <path-to-session.jsonl>"
```

**Claude Code:**
```bash
vet "goal" --history-loader "python3 ~/.claude/skills/vet/scripts/export_claude_code_session.py --session-file <path-to-session.jsonl>"
```

**无对话记录的情况**
```bash
vet "goal"
```

### 查找会话（Session）

你应仅查找与你所使用的编码工具（coding harness）相关的会话记录。如果用户要求你使用其他工具，他们可能是指 vet 的“代理模式”（agentic mode），而不是指会话本身。

**OpenCode:** `--session-id` 参数需要一个以 `ses_...` 开头的会话 ID。要找到当前的会话 ID：
1. 运行 `opencode session list --format json` 命令，列出所有会话及其 ID 和标题。
2. 从列表中根据标题或时间戳识别当前会话。
    - 重要提示：请确认找到的会话与当前对话内容一致。如果标题不明确，可以通过时间戳进行比对或查看多个选项。
3. 将找到的会话 ID 作为 `--session-id` 参数传递给 vet。

**Codex:** 会话文件存储在 `~/.codex/sessions/YYYY/MM/DD/` 目录下。要找到正确的会话文件：
1. 在当前对话中找到最独特的句子、问题或字符串。
2. 在 `~/.codex/sessions/` 目录中搜索该字符串，以找到对应的会话文件。
    - 重要提示：请确认找到的会话与当前对话内容一致，并且不是其他具有相同搜索字符串的会话。
3. 将找到的会话文件路径作为 `--session-file` 参数传递给 vet。

**Claude Code:** 会话文件存储在 `~/.claude/projects/<encoded-path>/` 目录下。其中，`<encoded-path>` 会被替换为 `-`（例如 `/home/user/myproject` 会变成 `-home-user-myproject`）。要找到正确的会话文件：
1. 在当前对话中找到最独特的句子、问题或字符串。
2. 在 `~/.claude/projects/` 目录中搜索该字符串，以找到对应的会话文件。
    - 重要提示：请确认找到的会话与当前对话内容一致，并且不是其他具有相同搜索字符串的会话。
3. 将找到的会话文件路径作为 `--session-file` 参数传递给 vet。

**注意：** 标准用法中的示例假设 vet 已在用户级别安装，而非项目级别安装。在尝试运行 vet 之前，请确认它是否已安装在项目级别（项目级别的安装具有优先级）。如果 vet 是在项目级别安装的，请确保配置文件中的 `history-loader` 选项指向正确的路径。

## 解释结果

Vet 会分析从基础提交（base commit）开始的完整 Git 差异文件，这可能包括来自同一仓库中其他代理或会话的更改。如果 vet 报告了与你本次操作无关的问题，请忽略这些问题，因为它们可能由其他代理或用户引起。

## 常用选项

- `--base-commit REF`: 差异文件的基准 Git 提交引用（默认值：HEAD）
- `--model MODEL`: 要使用的 LLM 模型（默认值：claude-opus-4-6）
- `--list-models`: 显示 vet 支持的所有模型
    - 运行 `vet --help` 并查看 vet 项目的README 文件，以获取有关自定义 OpenAI 兼容模型的详细信息。
- `--confidence-threshold N`: 问题的最低置信度阈值（范围：0.0-1.0，默认值：0.8）
- `--output-format FORMAT`: 输出格式：`text`、`json` 或 `github`
- `--quiet`: 忽略状态信息及“未发现问题”的提示
- `--agentic`: 通过本地安装的 Claude Code 或 Codex CLI 进行分析，而不是直接调用 API。如果因缺少 API 密钥导致 vet 无法运行，可以尝试此模式。此模式的效率较低，但通常能更准确地识别问题。`--model` 参数会被传递给相应的工具，但 vet 本身不会验证这些模型是否被支持。
- `--agent-harness`: 可选值：`codex` 或 `claude`（默认值：`claude`）
- `--help`: 显示所有可用选项的列表

## 更新

随着代理工具和 LLM API 的更新，vet 的 CLI、技能文件（skill files）以及导出脚本（export scripts）可能会过时。

如果发生这种情况，请尝试更新它们。运行 `which vet` 命令以确定 vet 的安装方式，并根据需要进行更新。对于技能文件，检查磁盘上存在的文件目录，然后从 https://github.com/imbue-ai/vet/tree/main/skills/vet 下下载最新版本进行更新。

## 额外信息

更多详细信息请参阅 vet 的官方仓库：
https://github.com/imbue-ai/vet
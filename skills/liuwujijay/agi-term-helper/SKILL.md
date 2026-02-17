---
name: term
description: 通过 OpenClaw 的 `exec` 命令实现快速、明确的终端执行（直接调度；您需要输入精确的命令）。
user-invocable: true
disable-model-invocation: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata: { "openclaw": { "emoji": "🧰", "os": ["darwin","linux","win32"] } }
---
# /term — 直接在终端执行命令（执行调度）

`/term` 是一个 **高级用户快捷方式**：你在 `/term` 后输入的任何内容都会被原样转发给 OpenClaw 的 `exec` 工具。

这属于 **手动模式**：
- 你（用户）提供确切的 shell 命令。
- OpenClaw 不会修改、扩展或以任何方式“帮助”修改该命令。
- 当你需要快速、确定性的终端操作（无需额外的处理流程）时，这种方式非常有用。

## 执行调度的原理（重要）

OpenClaw 支持 `command-dispatch: tool` 技能。当你运行 `/term ls -la` 时，原始的命令字符串（`ls -la`）会直接传递给配置好的 `exec` 工具，而不会经过任何额外的解析。在 `command-dispatch` 模式下，OpenClaw 会以如下格式调用工具：

`{ command: "<原始参数>", commandName: "<命令名称>", skillName: "<技能名称>" }`

请参阅 Skills 文档中的 `command-dispatch`、`command-tool` 和 `command-arg-mode` 部分。:contentReference[oaicite:10]{index=10}

## 何时使用 `/term` 与普通的 “代理执行”？

在以下情况下使用 `/term`：
- 你知道自己想要执行的命令。
- 你需要进行快速的只读检查（如文件列表、Git 状态、grep 操作）。
- 你正在调试 OpenClaw 本身（例如查看技能文件夹、日志或 Peekaboo Bridge 的状态）。

在以下情况下使用普通的代理执行流程：
- 你希望模型来决定最佳的执行方式。
- 任务可能需要多个步骤、安全检查或文件编辑。

## 安全注意事项（请务必阅读）

使用 `/term` 相当于让助手在终端中执行命令。请遵循以下安全规则：
1) 除非你确实需要修改系统状态，否则优先使用只读命令。
2) 避免在命令行中输入敏感信息（如 API 密钥、cookie 等）。
3) 避免使用远程执行的命令（例如：`curl ... | sh` 或类似的命令）。
4) 如果命令可能删除或覆盖文件，请务必仔细检查路径。

## 关于主机环境与沙箱环境的说明

你的实际执行环境取决于你在配置中如何调用 `exec`（是在沙箱环境中还是在主机环境中执行）。另外，请注意：当会话处于沙箱模式时，环境变量不会自动被容器继承；你需要通过沙箱环境设置将它们传递给容器，或者将它们嵌入到镜像中。:contentReference[oaicite:11]{index=11}

## 实际使用示例

### 快速检查（安全、只读操作）

- `/term pwd`
- `/term ls -la`
- `/term git status`
- `/term rg -n "TODO|FIXME" .`

### 调试 Peekaboo Bridge 的状态（macOS）

- `/term peekaboo bridge status --verbose`

如果所有候选对象的输出都是 “no such file or directory”，并且显示 “Selected: local (in-process)”，那么很可能没有 Bridge 主机正在运行（请参阅下面的故障排除方法）。

### 用于获取结构化输出的命令

如果你需要解析 JSON 格式的输出，可以使用以下命令：
- `/term python -c 'import json, platform; print(json.dumps({"py": platform.python_version())')'`

## 故障排除

### “命令未找到”
OpenClaw 会在其运行时环境指定的 `PATH` 中查找命令。如果你使用的是 Homebrew，请确保运行时环境能够找到 `/opt/homebrew/bin`。

### “权限被拒绝” / macOS 的隐私设置提示
某些工具（如屏幕截图工具或 UI 自动化工具）需要访问屏幕录制或辅助功能。在 macOS 上，这些权限是按进程设置的；使用 PeekabooBridge 通常是实现自动化操作的可靠方式。

### 需要更详细的指导和安全防护措施

可以安装并使用配套的 `terminal-helper` 技能（该技能可由模型调用），它提供了安全操作模式、确认流程和操作指南。
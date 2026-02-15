---
name: claude-tmux
description: 管理运行在 tmux 会话中的 Claude Code 实例。用户通常为不同的项目创建独立的 tmux 会话。当您需要读取某个特定 tmux 会话/项目中的最新 Claude Code 响应、向其发送命令并获取响应，或者直接通过 tmux 运行 `/compact` 命令（无需额外脚本）时，可以使用此功能。
---

## 目标  
为 Codex 提供一个可重复使用的检查清单，用于在 tmux 中与 Claude Code 交互。所有操作均通过标准的 tmux 命令完成，无需使用任何辅助脚本。每当遇到类似 “在会话 X 中检查 Claude” 或 “在 Claude 上运行 /compact” 的指令时，请按照以下步骤操作。  

## 规范  
1. **会话命名**：我们使用 tmux 会话的名称来标识会话。会话名称可以通过 `tmux new-session -s <session_name>` 来创建。例如，如果我们使用 `tmux new-session -s foobar` 创建了一个名为 `foobar` 的 tmux 会话，那么我们就将这个会话称为 `foobar`。  
2. **Claude 窗格**：在每个会话中，应该只有一个窗口的标题为 `claude` 的窗口。如果该窗口没有命名，请先将其重命名（使用 `Ctrl-b : select-pane -T claude`）。  
3. **标准标记**：Claude Code 会以 `❯ …` 显示用户输入的内容，以 `⏺ …` 显示其回复。我们根据这些标记来识别最新的交互记录。  

## 工作流程  

### 1. 定位 Claude 窗格  
```
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index} #{pane_title}' | grep "^<session_name>" | grep -i claude
```  
- 如果没有找到名为 “claude” 的窗口，请提示：“在会话 <name> 中未找到名为 ‘claude’ 的窗口。”  
- 如果找到多个名为 “claude” 的窗口，请选择 `window_index/pane_index` 最小的那个窗口；除非有特别说明。  
- 将目标会话和窗口信息记录为 `<session>:<window>.<pane>`，以便后续使用。  

### 2. 查看最新的交互记录  
```
tmux capture-pane -p -J -t <target> -S -200
```  
- 从下往上查找最后一个以 `❯` 开头的用户输入内容，以及其后紧跟的 `⏺`（Claude 的回复）。将这些内容原样显示给用户。  
- 如果没有找到 `❯/⏺` 对应的记录，请提示：“尚未找到交互记录。”  

### 3. 发送提示  
```
tmux send-keys -t <target> -l -- "<prompt>"
sleep 0.1
 tmux send-keys -t <target> Enter
```  
- 发送提示后，使用 `capture-pane` 命令持续监听响应，直到出现新的 `⏺`（表示 Claude 已回复），或者达到预设的超时时间（例如 3 分钟）。请原样显示 Claude 的回复内容。  
- 如果超时时间到期，请提示：“Claude 尚未回复——仍在等待中。”  

### 4. 运行 `/compact`  
与发送普通提示相同，但需要执行 `/compact` 命令。确认操作完成后，提示：“已在会话 <name> 中触发了 /compact 命令。”（Claude 会直接在当前窗口中显示回复；除非用户特别要求，否则无需再次显示回复内容。）  

### 5. 打印原始缓冲区内容（用于调试）  
```
tmux capture-pane -p -J -t <target> -S -400
```  
当用户需要查看完整的交互记录或解析过程中出现问题时，可以使用此命令。  

## 提示  
- 在发送命令之前，请务必确认目标窗口是正确的——尤其是在共享会话中。  
- 如果 Claude 窗格位于非默认的 tmux 套接字上，请在每个 tmux 命令前加上前缀 `tmux -S /path/to/socket …`。  
- 在总结结果时，请提及所使用的会话和窗口名称，以便追踪操作过程。  
- 如果用户需要处理多个会话，请对每个会话重复执行上述工作流程。  

这个方法简单实用：完全依赖 tmux 的内置功能，无需额外编写代码。无论何时需要直接与 tmux 中运行的 Claude Code 交互，都可以使用这套流程。
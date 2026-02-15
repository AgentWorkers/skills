---
name: claude-code-wingman
description: 您的 Claude Code 助手——通过 tmux 分配编码任务，支持免费或付费编码服务，同时将 Clawdbot 的 API 使用成本降至最低。
metadata: {"clawdbot":{"emoji":"🎯","requires":{"anyBins":["claude","tmux"]}}}
---

# Claude Code Wingman

这是一个用于自动化使用Claude Code的脚本，它通过Clawdbot来执行编码任务，从而帮助您在保持Anthropic API预算的同时充分利用Claude Code的免费/工作模式。

**GitHub链接：** https://github.com/yossiovadia/claude-code-wingman

## 功能介绍

该脚本会在tmux会话中启动Claude Code，并自动处理权限确认流程。非常适合在您拥有Claude Code的免费/工作访问权限，但Anthropic API预算有限的情况下使用。

**成本对比：**
- **不使用Clawdbot时：** 所有编码工作都由Clawdbot完成，会消耗您每月20美元的API费用。
- **使用Clawdbot时：** Clawdbot会启动Claude Code，从而使用公司提供的免费API。

## 安装

该脚本依赖于一个独立的GitHub仓库。只需安装一次即可：

```bash
cd ~/code
git clone https://github.com/yossiovadia/claude-code-wingman.git
cd claude-code-wingman
chmod +x *.sh
```

## 在Clawdbot中的使用方法

当用户请求进行编码任务时，脚本会启动Claude Code：

```bash
~/code/claude-code-wingman/claude-wingman.sh \
  --session <session-name> \
  --workdir <project-directory> \
  --prompt "<task description>"
```

### 示例对话流程：

**用户：** “修复api.py文件中的错误。”

**Clawdbot回复：** 
```
Spawning Claude Code for this...

bash:~/code/claude-code-wingman/claude-wingman.sh \
  --session vsr-bug-fix \
  --workdir ~/code/semantic-router \
  --prompt "Fix the bug in src/api.py - add proper error handling for null responses"
```

随后，Clawdbot会提供以下信息：
- 会话名称（方便用户后续查看）
- 监控命令
- 自动权限确认工具正在运行中

**用户：** “任务进展如何？”

**Clawdbot：** 会捕获tmux的输出并汇总任务进度，然后回复用户：

```bash
tmux capture-pane -t vsr-bug-fix -p -S -50
```

## 命令列表

### 启动会话
```bash
~/code/claude-code-wingman/claude-wingman.sh \
  --session <name> \
  --workdir <dir> \
  --prompt "<task>"
```

### 监控进度
```bash
tmux capture-pane -t <session-name> -p -S -100
```

### 查看自动权限确认日志
```bash
cat /tmp/auto-approver-<session-name>.log
```

### 结束会话
```bash
tmux kill-session -t <session-name>
```

### 列出所有会话
```bash
tmux ls | grep claude-auto
```

## 工作流程：

1. **用户提出编码需求**（例如：修复错误、添加功能、重构代码等）
2. **Clawdbot通过wingman脚本启动Claude Code**
3. **自动权限确认工具在后台处理权限请求**
4. **Clawdbot监控并报告任务进度**
5. **用户可以随时查看或直接控制会话**
6. **Claude Code使用公司的API完成编码任务**

## 首次使用时的权限确认提示

当脚本在新的目录中运行时，Claude Code会询问：
> “您是否信任该目录中的文件？”

**首次使用时：** 用户需要手动确认（按Enter键）。之后，系统将自动处理权限确认流程。

**处理方法：**
```
User, Claude Code needs you to approve the folder trust (one-time). Please run:
tmux attach -t <session-name>

Press Enter to approve, then Ctrl+B followed by D to detach.
```

## 使用建议：

### 适用场景：
✅ **适用于：** 大量代码生成/重构、多文件修改、长时间运行的任务、重复性的编码工作
❌ **不适用场景：** 快速文件读取、简单编辑、需要对话的场景、规划/设计讨论

### 会话命名规范：

使用描述性强的名称：
- `vsr-issue-1131` - 用于特定问题的编码任务
- `vsr-feature-auth` - 用于功能开发
- `project-bugfix-X` - 用于修复错误

## 常见问题解决方法：

### 权限确认提示未提交
如果权限确认提示未成功提交，可能是由于脚本发送了两次Enter键（存在延迟）。此时用户可以手动点击Enter键进行确认。

### 自动权限确认工具无法正常工作
检查日志文件：`cat /tmp/auto-approver-<session-name>.log`，应能看到类似“权限确认提示已检测到！正在跳转到选项2...”的提示。

### 会话已存在
如果会话已经存在，可以使用`tmux kill-session -t <session-name>`命令结束该会话。

## 高级技巧：

### 并行会话
可以在多个会话中同时运行多个任务。

### 会话命名规则：
使用统一的前缀（如`vsr-`、`myapp-`等）来命名会话。

### 定期监控
每隔几分钟检查一次任务进度。

### 完成任务后
任务完成后，请更新`TOOLS.md`文件：

```markdown
### Recent Claude Code Sessions
- 2026-01-26: VSR AWS check - verified vLLM server running ✅
- Session pattern: vsr-* for semantic-router work
```

## 使用技巧：

- **并行处理：** 在不同的会话中同时运行多个任务。
- **规范命名：** 为会话使用统一的命名规则。
- **定期检查：** 定期查看任务进度。
- **允许任务完成：** 不要过早结束会话，让Claude Code完成所有工作。

---

**总结：**  
通过使用Claude Code的免费/工作模式，该脚本有效降低了API使用成本，让您能够将Anthropic的预算更多地用于对话类任务。
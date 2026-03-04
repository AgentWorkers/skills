---
name: cc
description: 这是一个用于Claude中继会话的简短命令封装工具。当用户希望使用简洁的命令（如`/cc projects`、`/cc on <project>`、`/cc tail`、`/cc off`或`/cc <message>`）来继续与当前项目会话中的Claude Code进行交流时，可以使用这个工具。
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["tmux","claude"],"skills":["claude-relay"]}}}
---
# cc  
用于 Claude Code 中继会话的简短操作命令。  

**要求**：必须安装 `claude-relay` 技能。  

## 脚本  
所有命令均通过以下方式执行：  
```bash
{baseDir}/scripts/cc.sh <raw-args>
```  

## 命令路由  
解析用户输入并执行相应操作：  
- `projects` / `list` → 列出所有可用项目  
- `on <project>` / `start <project>` → 启动或重新使用 Claude 会话（支持模糊匹配）  
- `off [project]` / `stop [project]` → 停止会话（默认：最后一个项目）  
- `tail [project] [lines]` → 显示最近的输出（默认：120 行）  
- `status` → 列出当前激活的中继会话  
- `/cc` （无参数） → 显示内联按钮菜单（如果平台支持）  
- `/cc on` （无项目参数） → 显示项目选择按钮  
- 其他任何文本 → **进入中继模式**（详见下文）  

对于“其他任何文本”的情况：如果第一个单词对应一个激活的项目会话，则将其视为明确的项目目标，并将剩余文本作为消息发送。  

## 中继模式  
执行 `on <project>` 后，系统会进入中继模式。以下是关键行为规范：  
1. **所有用户消息都会被转发给 Claude Code**——无例外。请勿自行解释、回复或处理这些消息。您仅起到“透明通道”的作用。  
2. 通过 `scripts/cc.sh send` 命令转发消息，等待 Claude Code 的响应后返回最终结果。  
3. **唯一不被转发的消息是以下命令**：`off`、`tail`、`status`、`projects`、`/cc`。  
4. 中继模式会在执行 `off`、`stop` 或调用 `/cc` 菜单时结束。  

示例：  
```
[relay mode active, project=marvis]
User: "帮我查一下这个 bug 的原因"
→ cc.sh send marvis "帮我查一下这个 bug 的原因"
→ wait for Claude Code output
→ return result to user
WRONG: answering the question yourself
```  

有关按钮规格、输出格式、审批处理和回调路由的详细信息，请参阅 [relay-mode.md](references/relay-mode.md)。  

## 主要原则：  
- **在中继模式下切勿自行回复**：仅转发所有消息，并返回 Claude Code 的输出结果。  
- **每次交互仅返回一条消息**：不提供进度更新。  
- **选择方式**：Claude Code 输出中的编号菜单会转换为内联按钮。  
- **工具调用规则**：按钮/菜单相关的消息应包含工具调用命令，且后面不能附加任何文本。  

## 环境变量  
| 变量          | 默认值       | 描述                          |  
|-----------------|------------|-----------------------------------------|  
| `CLAUDE_RELAY_DIR` | （自动检测）     | `claude-relay` 技能的目录路径             |  
| `CLAUDE_RELAY_ROOT` | `$HOME/projects` | 项目查找的根目录                     |  
| `CLAUDE_RELAY_MAP` | `<relay-skill-dir>/projects.map` | 项目别名映射文件的路径                |
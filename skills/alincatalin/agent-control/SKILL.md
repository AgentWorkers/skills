---
name: agent-control
description: 通过简短的命令来管理 OpenClaw 的隔离代理。当用户需要创建、列出、切换、绑定或删除代理，或将频道路由到特定代理，或者设置代理身份时，可以使用这些命令，而无需手动输入完整的 CLI 语法。
---
# 代理控制

将简短的聊天命令转换为 OpenClaw CLI 代理操作。

## 命令语法

支持以下命令（不区分大小写，去除多余的空格）：

- `agent list`  
- `agent create <名称> [工作空间=<路径>] [模型=<ID>]`  
- `agent switch <名称> [频道=<频道[:账户ID>]`  
- `agent bind <名称> <频道[:账户ID>]`  
- `agent unbind <名称> <频道[:账户ID>]`  
- `agent delete <名称>`  
- `agent identity <名称> [显示="..."] [表情符号=🗡️] [头像=<路径>]`  

如果输入不明确，请提出一个具体的问题。

## 执行映射

执行以下命令模式：

- 列出代理：  
  `openclaw agents list`  

- 创建代理：  
  `openclaw agents add <名称> --工作空间 <路径> --模型 <ID>`  
  如果省略可选参数，则使用默认值。  
  默认工作空间为：`~/clawd/agents/<名称>`  

- 切换代理的频道/账户：  
  `openclaw agents bind --代理 <名称> --频道 <频道[:账户ID>]`  
  如果省略频道，则从当前界面自动推断（例如：`webchat`）。  

- 绑定/解绑代理：  
  `openclaw agents bind --代理 <名称> --绑定 <绑定信息>`  
  `openclaw agents unbind --代理 <名称> --绑定 <绑定信息>`  

- 删除代理：  
  对于此类破坏性操作，需要用户明确确认。  
  然后执行：`openclaw agents delete <名称>`  

- 设置代理的身份信息：  
  `openclaw agents set-identity --代理 <名称> [--名称 <显示名称>] [--表情符号 <表情符号>] [--头像 <路径>]`  

## 响应方式

每次操作完成后，返回以下内容：  
1. 一行操作结果（成功/失败）  
2. 下一个对用户有用的命令  

保持简洁明了。  

## 安全规则：  
- 将 `agent delete` 视为破坏性操作：执行前必须确认。  
- 绝不要运行与代理无关的 shell 命令。  
- 如果命令失败，显示错误信息并提供具体的解决方法。  

## 脚本：  
- 如有需要，可以使用 `scripts/example.py` 作为命令解析和执行的辅助工具。
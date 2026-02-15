---
name: ssh-exec
description: "通过 SSH 在远程 Tailscale 节点上运行单个命令，而无需打开交互式会话。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "bins": ["ssh"] },
        "install": [],
      },
  }
---

# SSH执行技能

通过SSH在远程Tailscale节点上运行单个命令，而无需打开交互式会话。需要具备对目标的SSH访问权限（密钥位于`~/.ssh/`或`SSH_AUTH_SOCK`中），以及`SSH_TARGET`环境变量（例如：`100.107.204.64:8022`）。

## 运行远程命令

在目标节点上执行命令，并返回标准输出（stdout）和标准错误（stderr）：

```bash
ssh -p 8022 user@100.107.204.64 "uname -a"
```

## 使用自定义端口执行命令

使用`SSH_TARGET`环境变量：

```bash
ssh -p "${SSH_PORT:-22}" "$SSH_HOST" "df -h"
```

## 远程执行脚本

将本地脚本传输到远程主机：

```bash
ssh -p 8022 user@100.107.204.64 'bash -s' < local-script.sh
```
---
name: sandboxer
description: "通过 Sandboxer 网页控制台管理 Claude Code 终端会话。适用场景包括：  
(1) 列出正在运行的 Claude Code 会话；  
(2) 查看某个 Claude 会话的当前状态或正在执行的任务；  
(3) 向 Claude 会话发送命令；  
(4) 创建或终止会话；  
(5) 当用户输入 “sandboxer” 或 “session” 时执行相关操作。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "bins": ["curl", "tmux", "jq"] }
      }
  }
---

# Sandboxer

通过 HTTP API 管理在 tmux 中运行的 Claude Code 会话。

**所有命令都在本地执行——无需 SSH。**

## 健康检查（请先运行！）

在使用任何命令之前，请确认 Sandboxer 正在运行：

```bash
curl -sf http://localhost:8081/api/sessions >/dev/null && echo "✓ Sandboxer is running" || echo "✗ Sandboxer not reachable"
```

**如果无法访问 Sandboxer：**

```
✗ Sandboxer is not installed or not running on this machine.

To install Sandboxer, run:
  claude --dangerously-skip-permissions "clone github.com/chriopter/sandboxer to /home/sandboxer/git/sandboxer, read README.md for install instructions, then install sandboxer"

To start if already installed:
  sudo systemctl start sandboxer

See: https://github.com/chriopter/sandboxer
```

## 列出会话

```bash
curl -s http://localhost:8081/api/sessions | jq
```

按项目筛选：

```bash
curl -s http://localhost:8081/api/sessions | jq '.[] | select(.name | contains("PROJECT"))'
```

## 查看会话输出

查看 Claude 的执行情况：

```bash
tmux capture-pane -t "SESSION_NAME" -p | tail -80
```

## 向会话发送命令

将用户请求转发给 Claude Code：

```bash
tmux send-keys -t "SESSION_NAME" "implement feature X" Enter
```

然后等待 10-30 秒，读取输出以检查结果。

## 创建会话

```bash
curl -s "http://localhost:8081/create?type=claude&dir=/path/to/project"
```

会话类型：`claude`、`bash`、`lazygit`

## 结束会话

```bash
curl -s "http://localhost:8081/kill?session=SESSION_NAME"
```

## 工作流程：将任务转发给 Claude

当用户说“执行 X”或“实现 Y”时：

1. 找到相应的会话：`curl -s http://localhost:8081/api/sessions | jq`
2. 发送命令：`tmux send-keys -t "SESSION" "do X" Enter`
3. 等待 10-30 秒
4. 读取结果：`tmux capture-pane -t "SESSION" -p | tail -80`
5. 将结果反馈给用户

## Web 仪表板

URL：`https://YOUR_SERVER:8080`

显示实时终端预览。可能需要密码。

## 安装

请参阅 [GitHub 文档](https://github.com/chriopter/sandboxer#install) 以获取安装说明。
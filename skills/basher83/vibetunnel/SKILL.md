---
name: vibetunnel
description: 管理 VibeTunnel 终端会话：创建、列出、监控以及控制在 VibeTunnel 网页控制面板中可见的终端会话。
homepage: https://github.com/AugmentedMomentum/vibetunnel
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":["vibetunnel","curl","jq"]},"primaryEnv":"VT_URL","install":[{"id":"vibetunnel","kind":"node","package":"vibetunnel","bins":["vibetunnel"],"label":"Install VibeTunnel (npm)"}]}}
---

# VibeTunnel

通过 REST API 管理 [VibeTunnel](https://github.com/AugmentedMomentum/vibetunnel) 的终端会话。可以创建、列出、监控和控制在网页仪表板中显示的会话。

## 设置

VibeTunnel 必须正在运行。默认地址：`http://localhost:8080`。可以通过 `VT_URL` 环境变量进行自定义。

## 健康检查
```bash
curl -s ${VT_URL:-http://localhost:8080}/api/health | jq .
```

## 列出会话
```bash
curl -s ${VT_URL:-http://localhost:8080}/api/sessions | jq .
```

**紧凑视图：**
```bash
curl -s ${VT_URL:-http://localhost:8080}/api/sessions | jq -r '.[] | "\(.status | if . == "running" then "●" else "○" end) \(.name) [\(.id | .[0:8])]"'
```

## 创建会话
```bash
curl -s -X POST ${VT_URL:-http://localhost:8080}/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"command": ["zsh", "-l", "-i"], "name": "my-session", "workingDir": "/path/to/dir"}' | jq .
```

参数：
- `command`：数组 — 命令及参数（默认值：`["zsh", "-l", "-i"]`）
- `name`：显示名称
- `workingDir`：工作目录
- `cols`：终端宽度（默认值：120）
- `rows`：终端高度（默认值：30）

## 获取会话信息
```bash
curl -s ${VT_URL:-http://localhost:8080}/api/sessions/<id> | jq .
```

## 删除会话
```bash
curl -s -X DELETE ${VT_URL:-http://localhost:8080}/api/sessions/<id> | jq .
```

## 发送输入
```bash
curl -s -X POST ${VT_URL:-http://localhost:8080}/api/sessions/<id>/input \
  -H "Content-Type: application/json" \
  -d '{"text": "ls -la\n"}' | jq .
```

注意：需要在输入内容末尾添加 `\n` 以执行命令。

## 调整会话大小
```bash
curl -s -X POST ${VT_URL:-http://localhost:8080}/api/sessions/<id>/resize \
  -H "Content-Type: application/json" \
  -d '{"cols": 150, "rows": 40}' | jq .
```

## 示例

**启动 Claude 代码会话：**
```bash
curl -s -X POST ${VT_URL:-http://localhost:8080}/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"command": ["claude"], "name": "claude-code", "workingDir": "~/repos/my-project"}' | jq .
```

**启动 tmux 会话：**
```bash
curl -s -X POST ${VT_URL:-http://localhost:8080}/api/sessions \
  -H "Content-Type: application/json" \
  -d '{"command": ["tmux", "new", "-A", "-s", "work"], "name": "tmux-work"}' | jq .
```

**清理已退出的会话：**
```bash
curl -s ${VT_URL:-http://localhost:8080}/api/sessions | jq -r '.[] | select(.status == "exited") | .id' | \
  xargs -I {} curl -s -X DELETE ${VT_URL:-http://localhost:8080}/api/sessions/{}
```

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `VT_URL` | `http://localhost:8080` | VibeTunnel 服务器地址 |
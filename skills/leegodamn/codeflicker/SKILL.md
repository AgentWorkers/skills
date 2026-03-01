---
name: codeflicker
description: >
  **CodeFlicker CLI 编程助手**  
  当用户提到 “flickcli”、“codeflicker”、“install codeflicker” 或 “use codeflicker to write code” 时，可以使用此工具。
---
# CodeFlicker CLI 技能

这是一款由 Kuaishou 开发的 AI 编程辅助工具 CLI，类似于 Claude Code 或 Codex CLI。

## 安装

### 第一步：设置 npm 注册表（适用于 Kuaishou 内部网络）

```bash
export npm_config_registry="https://npm.corp.kuaishou.com"
```

### 第二步：安装 CLI

```bash
npm install -g @ks-codeflicker/cli
```

### 第三步：使用 SSO 登录

```bash
flickcli /login
```

检查安装是否成功：
```bash
flickcli --version
```

## 配置

查看配置：
```bash
flickcli config list -g
```

全局配置设置：
```bash
flickcli config set -g model glm-5
flickcli config set -g smallModel claude-haiku-4.5
flickcli config set -g planModel claude-4.5-sonnet
flickcli config set -g visionModel claude-4.5-sonnet
flickcli config set -g approvalMode yolo
```

可用模型（wanqing 提供）：
- `glm-5` - 默认模型
- `glm-4.7`, `claude-haiku-4.5` - 轻量级模型
- `claude-4.5-sonnet` - 用于规划/视觉任务

审批模式：
- `default` - 需要用户确认
- `autoEdit` - 自动编辑
- `yolo` - 自动执行（请谨慎使用）

## 使用方法

**交互模式：**
```bash
flickcli "write a hello world"
```

**安静模式（非交互式）：**
```bash
flickcli -q "implement fibonacci"
```

**继续上一次会话：**
```bash
flickcli -q -c "add unit tests"
```

**指定模型：**
```bash
flickcli -m glm-5 "task"
```

**指定工作目录：**
```bash
flickcli --cwd /path/to/project "task"
```

## 快速参考

| 命令 | 描述 |
|---------|-------------|
| `flickcli "任务"` | 进入交互模式 |
| `flickcli -q "任务"` | 进入安静模式 |
| `flickcli -q -c "任务"` | 继续上一次会话 |
| `flickcli -q -r <id> "任务"` | 恢复会话 |
| `flickcli config set -g approvalMode yolo` | 设置为自动执行模式 |

## 注意事项：

- 安装需要使用 Kuaishou 内部的 npm 注册表。
- **首次使用前必须使用 SSO 登录：** `flickcli /login`
- `yolo` 模式会自动执行所有操作，请谨慎使用。
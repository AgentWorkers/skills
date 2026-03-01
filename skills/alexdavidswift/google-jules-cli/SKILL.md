---
name: jules-tools-skill
version: 1.0.0
description: "与 Google 的 Jules Tools CLI 进行交互，以管理 AI 编码会话。"
permissions:
  exec:
    - jules
    - npm
---
# Jules 工具技能

该技能允许 AI 代理与 **Jules 工具 CLI** 进行交互，以管理 Google 的 Jules AI 编码会话。通过该技能，代理可以启动新的编码会话、列出活跃的会话，并直接从终端获取结果。

## 先决条件

在使用任何 Jules 命令之前，请确保已安装并验证了 `jules` CLI。

### 1. 安装

运行以下命令检查是否已安装 `jules`：

```bash
jules --version
```

如果未找到该命令，请使用 `npm` 进行安装：

```bash
npm install -g @google/jules
```

> **注意：** 根据系统配置，安装可能需要 `sudo` 权限。如果 `npm install -g` 因权限问题失败，请尝试使用 `sudo npm install -g @google/jules`，或请求用户协助。

### 2. 验证

代理必须经过验证才能与 Jules 交互。要验证，请运行以下命令：

```bash
jules login
```

此命令将打开一个浏览器窗口，让用户使用他们的 Google 账户登录。如果代理在无头环境中运行，请指导用户在本地机器上完成此步骤，或提供其他可用的验证方法（请参阅 `jules login --help`）。

要验证身份或登出，请使用以下命令：

```bash
jules logout
```

## 使用方法

与 Jules 交互的主要命令是 `jules remote`。

### 列出会话

要查看所有活跃或过去的编码会话，请运行：

```bash
jules remote list --session
```

要列出连接的仓库，请运行：

```bash
jules remote list --repo
```

### 启动新会话

要为 Jules 启动一个新的编码会话，请运行以下命令：

```bash
jules remote new --repo <repo_name> --session "<task_description>"
```

- `<repo_name>`：仓库名称（例如 `torvalds/linux`）或 `.`（表示当前目录的仓库）。
- `<task_description>`：Jules 应该执行的操作的明确描述（例如：“修复登录处理程序中的错误”）。

**示例：**

```bash
jules remote new --repo . --session "Add a new test case for the user profile component"
```

您还可以同时启动多个会话：

```bash
jules remote new --repo . --session "Refactor the database schema" --parallel 2
```

### 获取会话结果

会话完成后，您可以获取结果（代码更改）：

```bash
jules remote pull --session <session_id>
```

- `<session_id>`：要获取结果的会话 ID（从 `jules remote list` 中获得）。

### 常见帮助

有关任何命令的更多信息，请运行：

```bash
jules --help
jules remote --help
```

## 故障排除

- **命令未找到**：确保安装后 `jules` 在系统 PATH 中。您可能需要重新启动 shell 或加载配置文件。
- **验证错误**：尝试运行 `jules logout`，然后再次运行 `jules login`。
- **网络问题**：确保代理能够访问 Google 的服务器。
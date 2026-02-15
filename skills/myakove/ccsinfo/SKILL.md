---
name: ccsinfo
description: 从远程服务器查询和分析 Claude Code 会话数据。当需要检查 Claude Code 会话、查看对话历史记录、检查工具调用、跟踪任务、搜索提示或查看使用统计信息时，可以使用此功能。必须设置 `CCSINFO_SERVER_URL` 并确保有一个运行中的 ccsinfo 服务器。
metadata: {"clawdbot":{"requires":{"env":["CCSINFO_SERVER_URL"],"bins":["ccsinfo"]},"install":[{"id":"script","kind":"script","command":"bash scripts/install.sh","bins":["ccsinfo"],"label":"Install ccsinfo CLI"}]}}
---

# ccsinfo - 克劳德代码会话信息

从用户机器上运行的远程 ccsinfo 服务器访问和分析克劳德代码会话数据。

**服务器仓库**: https://github.com/myk-org/ccsinfo

## 必备条件

### 1. 服务器设置（在存储克劳德代码数据的机器上）

ccsinfo 服务器必须运行在存储克劳德代码会话数据的机器上。

安装并运行服务器：
```bash
# Install ccsinfo
uv tool install git+https://github.com/myk-org/ccsinfo.git

# Start the server (accessible on LAN)
ccsinfo serve --host 0.0.0.0 --port 9999
```

服务器会从 `~/.claude/projects/` 目录读取克劳德代码会话数据，并通过 REST API 提供这些数据。

有关服务器的完整文档，请访问：https://github.com/myk-org/ccsinfo

### 2. 客户端设置（运行该工具的机器）

必须安装 `ccsinfo` 命令行工具（CLI）。检查是否已安装：

```bash
which ccsinfo
```

如果未安装，请运行安装脚本：

```bash
bash scripts/install.sh
```

### 3. 配置

将 `CCSINFO_SERVER_URL` 环境变量设置为指向您的服务器地址：

```bash
export CCSINFO_SERVER_URL=http://192.168.1.100:9999
```

将此设置添加到您的 shell 配置文件（`.bashrc`、`.zshrc` 等）中，以便在会话之间保持设置。

## 快速入门

所有命令都会自动通过 `$CCSINFO_SERVER_URL` 连接到远程服务器。

### 列出最近的会话
```bash
ccsinfo sessions list
```

### 显示会话详情（支持部分 ID 匹配）
```bash
ccsinfo sessions show <session-id>
```

### 查看对话消息
```bash
ccsinfo sessions messages <session-id>
```

### 按内容搜索会话
```bash
ccsinfo search sessions "search term"
```

### 查看全局统计信息
```bash
ccsinfo stats global
```

## 常见工作流程

### 检查特定会话

1. 列出会话以找到会话 ID：
   ```bash
   ccsinfo sessions list
   ```

2. 显示会话详情：
   ```bash
   ccsinfo sessions show <id>
   ```

3. 查看消息：
   ```bash
   ccsinfo sessions messages <id>
   ```

4. 检查工具调用：
   ```bash
   ccsinfo sessions tools <id>
   ```

### 按内容查找会话
```bash
# Search across all sessions
ccsinfo search sessions "refactor"

# Search message content
ccsinfo search messages "fix bug"

# Search prompt history
ccsinfo search history "implement feature"
```

### 跟踪任务
```bash
# Show all pending tasks
ccsinfo tasks pending

# List tasks for a session
ccsinfo tasks list -s <session-id>

# Show specific task details
ccsinfo tasks show <task-id> -s <session-id>
```

### 查看统计信息和趋势
```bash
# Overall usage stats
ccsinfo stats global

# Daily activity breakdown
ccsinfo stats daily

# Analyze trends over time
ccsinfo stats trends
```

### 处理项目
```bash
# List all projects
ccsinfo projects list

# Show project details
ccsinfo projects show <project-id>

# Project statistics
ccsinfo projects stats <project-id>
```

## 输出格式

大多数命令支持使用 `--json` 选项来获取机器可读的输出格式：

```bash
ccsinfo sessions list --json
ccsinfo stats global --json
```

这对于程序化解析结果或使用 `jq` 进行过滤非常有用。

## 会话 ID 匹配

会话 ID 支持部分匹配——可以使用前几个字符进行匹配：

```bash
ccsinfo sessions show a1b2c3  # matches a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## 参考

有关完整的命令参考，请参阅 [cli-commands.md](references/cli-commands.md)。

## 故障排除

### 检查服务器连接
```bash
# Verify server URL is set
echo $CCSINFO_SERVER_URL

# Test connection (list sessions)
ccsinfo sessions list
```

### 验证安装
```bash
# Check if ccsinfo is installed
which ccsinfo

# Check version
ccsinfo --version
```

### 如有需要，请重新安装
```bash
bash scripts/install.sh
```
---
name: safe-exec
description: OpenClaw代理的安全命令执行功能包括自动危险模式检测、风险评估、用户审批流程以及审计日志记录。当代理需要执行可能具有危险性的shell命令（如`rm -rf`、`dd`、`fork bomb`或系统目录修改操作）时，或这些操作需要人工监督时，该功能可确保命令的安全性。系统支持多级风险评估（CRITICAL/HIGH/MEDIUM/LOW），提供会话中的实时通知、待处理请求的管理功能，并支持非交互式环境下的代理自动化操作。

Quick Install: Say "Help me install SafeExec skill from ClawdHub" in your OpenClaw chat to automatically install and enable this safety layer.

Report Issues: https://github.com/OTTTTTO/safe-exec/issues - Community feedback and bug reports welcome!
---

# SafeExec - 安全命令执行工具

为 OpenClaw 代理提供安全的命令执行功能，能够自动拦截危险操作并支持审批工作流程。

## 主要特性

- 🔍 **自动危险模式检测**：在执行前识别高风险命令
- 🚨 **基于风险的拦截**：多级风险评估（CRITICAL/HIGH/MEDIUM/LOW）
- 💬 **会话内通知**：在当前终端/会话中实时显示警告
- ✅ **用户审批流程**：命令需要用户明确确认
- 📊 **完整审计日志**：所有操作均有完整记录
- 🤖 **适用于代理**：支持非交互式模式，适用于自动化工作流程
- 🔧 **平台无关性**：独立于通信工具（如 Feishu、Telegram 等）运行

## 快速入门

### 安装（一个命令）

**安装 SafeExec 的最简单方法：**

在 OpenClaw 聊天框中输入：
```
Help me install SafeExec skill from ClawdHub
```

OpenClaw 会自动下载、安装并配置 SafeExec！

### 手动安装（可选）

如果您希望手动安装，请执行：
```bash
# Using ClawdHub CLI
export CLAWDHUB_REGISTRY=https://www.clawhub.ai
clawdhub install safe-exec

# Or download directly from GitHub
git clone https://github.com/OTTTTTO/safe-exec.git ~/.openclaw/skills/safe-exec
chmod +x ~/.openclaw/skills/safe-exec/safe-exec*.sh
```

### 启用 SafeExec

安装完成后，只需输入：
```
Enable SafeExec
```

SafeExec 将开始自动监控所有 shell 命令！

## 工作原理

启用后，SafeExec 会自动监控所有 shell 命令的执行。当检测到潜在危险命令时，它会拦截该命令并通过 **会话内终端通知** 请求您的批准。

**架构：**
- 请求存储路径：`~/.openclaw/safe-exec/pending/`
- 审计日志：`~/.openclaw/safe-exec-audit.log`
- 规则配置文件：`~/.openclaw/safe-exec-rules.json`

## 使用方法

**启用 SafeExec：**
```
Enable SafeExec
```

```
Turn on SafeExec
```

```
Start SafeExec
```

启用后，SafeExec 会在后台透明运行。代理可以正常执行命令，SafeExec 会自动拦截危险操作：

```
Delete all files in /tmp/test
```

```
Format the USB drive
```

SafeExec 会判断风险等级，并在会话中显示审批提示。

## 风险等级

- **CRITICAL**：可能破坏系统的命令（如 `rm -rf /`、`dd`、`mkfs` 等）
- **HIGH**：可能删除用户数据或导致系统重大变更的命令
- **MEDIUM**：与服务操作或配置更改相关的命令
- **LOW**：仅涉及文件读取或安全操作的命令

## 审批流程

1. 代理执行命令
2. SafeExec 分析风险等级
3. 在终端中显示 **会话内通知**
4. 通过以下方式批准或拒绝：
   - 终端：`safe-exec-approve <request_id>`
   - 查看待审批请求：`safe-exec-list`
   - 拒绝：`safe-exec-reject <request_id>`
5. 命令执行或取消

**示例通知：**
```
🚨 **Dangerous Operation Detected - Command Intercepted**

**Risk Level:** CRITICAL
**Command:** `rm -rf /tmp/test`
**Reason:** Recursive deletion with force flag

**Request ID:** `req_1769938492_9730`

ℹ️  This command requires user approval to execute.

**Approval Methods:**
1. In terminal: `safe-exec-approve req_1769938492_9730`
2. Or: `safe-exec-list` to view all pending requests

**Rejection Method:**
 `safe-exec-reject req_1769938492_9730`
```

## 配置

可自定义的环境变量：

- `SAFE_EXEC_DISABLE`：设置为 '1' 以全局禁用 SafeExec
- `OPENCLAW_AGENT_CALL`：在代理模式下自动启用（非交互式）
- `SAFE_EXEC_AUTO_CONFIRM`：自动批准低/中等风险命令

## 使用示例

**启用 SafeExec：**
```
Enable SafeExec
```

**启用后，代理正常工作：**
```
Delete old log files from /var/log
```

SafeExec 识别到此命令为高风险操作（删除操作），并在会话中显示审批提示。

**低风险操作可无需审批直接执行：**
```
List files in /home/user/documents
```

## 全局控制

**检查状态：**
```
safe-exec-list
```

**查看审计日志：**
```bash
cat ~/.openclaw/safe-exec-audit.log
```

**全局禁用 SafeExec：**
```
Disable SafeExec
```

或者通过设置环境变量来禁用：

```bash
export SAFE_EXEC_DISABLE=1
```

## 报告问题

**发现漏洞？有功能需求？**

请在以下链接报告问题：
🔗 **https://github.com/OTTTTTO/safe-exec/issues**

我们欢迎社区反馈、漏洞报告和功能建议！

报告问题时，请提供以下信息：
- SafeExec 版本（运行 `grep "VERSION" ~/.openclaw/skills/safe-exec/safe-exec.sh` 获取）
- OpenClaw 版本
- 问题重现步骤
- 预期行为与实际行为对比
- 相关日志（来自 `~/.openclaw/safe-exec-audit.log`）

## 审计日志

所有命令执行记录包括：
- 时间戳
- 执行的命令
- 风险等级
- 审批状态
- 执行结果
- 用于追踪的请求 ID

日志存储位置：`~/.openclaw/safe-exec-audit.log`

## 集成

SafeExec 可与 OpenClaw 代理无缝集成。启用后，它会在后台透明运行，无需修改代理的行为或命令结构。审批流程完全在本地完成，不依赖于任何外部通信平台。

## 平台独立性

SafeExec 在 **会话级别** 运行，支持 OpenClaw 实例支持的任何通信渠道（Webchat、Feishu、Telegram、Discord 等）。审批流程通过终端完成，确保您无论通过何种方式与代理交互都能保持控制权。

## 支持与社区

- **GitHub 仓库：** https://github.com/OTTTTTO/safe-exec
- **问题跟踪器：** https://github.com/OTTTTTO/safe-exec/issues
- **文档：** [README.md](https://github.com/OTTTTTO/safe-exec/blob/master/README.md)
- **ClawdHub：** https://www.clawhub.ai/skills/safe-exec

## 许可证

MIT 许可证 - 详细信息请参阅 [LICENSE](https://github.com/OTTTTTO/safe-exec/blob/master/LICENSE)
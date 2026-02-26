---
name: safe-exec
description: >
  **OpenClaw代理的安全命令执行功能**  
  该功能具备自动危险模式检测、风险评估、用户审批流程以及审计日志记录等功能。适用于需要执行可能具有危险性的shell命令（如`rm -rf`、`dd`、`fork bomb`、系统目录修改等）或需要人工监督的场景。系统提供多层次的风险评估（CRITICAL/HIGH/MEDIUM/LOW），支持会话中的实时通知、待处理请求管理，以及适用于代理自动化的非交互式环境。
metadata:
  {
    "openclaw":
      {
        "env": ["SAFE_EXEC_DISABLE", "OPENCLAW_AGENT_CALL", "SAFE_EXEC_AUTO_CONFIRM"],
        "writes": ["~/.openclaw/safe-exec/", "~/.openclaw/safe-exec-audit.log"],
        "network": false,
        "monitoring": false,
        "credentials": []
      },
      "requires": { "bins": ["jq"] },
      "install":
        [
          {
            "id": "git",
            "kind": "git",
            "url": "https://github.com/OTTTTTO/safe-exec.git",
            "label": "Clone from GitHub",
          },
        ],
  }
---
# SafeExec - 安全命令执行工具

为 OpenClaw 代理提供安全的命令执行功能，能够自动拦截危险操作并支持审批工作流程。

## 主要特性

- 🔍 **自动危险模式检测**：在执行前识别高风险命令
- 🚨 **基于风险的拦截**：多级风险评估（CRITICAL/HIGH/MEDIUM/LOW）
- 💬 **会话内通知**：在当前终端/会话中实时提醒
- ✅ **用户审批流程**：命令需要用户明确确认
- 📊 **完整审计日志**：所有操作均有完整记录
- 🤖 **适合代理使用**：支持非交互式模式，适用于自动化工作流程
- 🔧 **平台无关**：独立于通信工具（如 WebChat、Feishu、Telegram 等）运行
- 🔐 **注重安全性**：不进行监控，不发送外部通知，也不进行网络请求

## 代理模式

当 OpenClaw 代理在非交互式环境中调用 SafeExec 时：

- **自动跳过确认提示**：防止代理程序卡顿
- **完整审计日志**：所有执行操作都会被记录，并标注执行模式（agent_auto 或 user_approved）
- **安全性得到保障**：危险模式检测和风险评估功能依然有效
- **适用场景**：通过审计日志实现人工监督的自动化工作流程

**环境变量：**
- `OPENCLAW_AGENT_CALL`：由 OpenClaw 在代理执行命令时设置
- `SAFE_EXEC_AUTO_CONFIRM`：手动覆盖设置，用于自动批准低/中等风险命令

**安全提示：** 代理模式不会关闭安全检查功能。高风险（CRITICAL）和极高风险（HIGH）的命令仍会被拦截并记录在审计日志中。

## 快速入门

### 安装（一个命令）

安装 SafeExec 的最简单方法：

在 OpenClaw 聊天框中输入以下命令：
```
Help me install SafeExec skill from ClawdHub
```

OpenClaw 会自动下载、安装并配置 SafeExec！

### 手动安装（可选）

如果您希望手动安装，请执行以下操作：
```bash
# Clone from GitHub
git clone https://github.com/OTTTTTO/safe-exec.git ~/.openclaw/skills/safe-exec

# Make scripts executable
chmod +x ~/.openclaw/skills/safe-exec/safe-exec*.sh

# Create symlinks to PATH (optional)
ln -s ~/.openclaw/skills/safe-exec/safe-exec.sh ~/.local/bin/safe-exec
ln -s ~/.openclaw/skills/safe-exec/safe-exec-*.sh ~/.local/bin/
```

### 启用 SafeExec

安装完成后，只需输入以下命令：
```
Enable SafeExec
```

SafeExec 将开始自动监控所有 shell 命令！

## 工作原理

启用 SafeExec 后，它会自动监控所有 shell 命令的执行。当检测到潜在危险命令时，会通过会话内通知请求您的批准。

**系统架构：**
- 请求存储路径：`~/.openclaw/safe-exec/pending/`
- 审计日志路径：`~/.openclaw/safe-exec-audit.log`
- 规则配置文件：`~/.openclaw/safe-exec-rules.json`
- 不进行外部网络请求
- 无后台监控进程

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

- **CRITICAL**：可能破坏系统的命令（如 `rm -rf /`, `dd`, `mkfs`, `fork bomb`）
- **HIGH**：可能删除用户数据或对系统造成重大影响的命令（如 `chmod 777`, `curl | bash`）
- **MEDIUM**：与服务相关或修改系统配置的命令（如 `sudo`, `firewall modifications`）
- **LOW**：仅涉及文件读取或安全操作的命令

## 审批流程

1. 代理执行命令
2. SafeExec 分析风险等级
3. 在终端中显示会话内通知
4. 用户通过以下方式批准或拒绝：
   - 终端命令：`safe-exec-approve <request_id>`
   - 查看待审批命令列表：`safe-exec-list`
   - 拒绝命令：`safe-exec-reject <request_id>`
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

## 配置选项

- `SAFE_EXEC_DISABLE`：设置为 '1' 可全局禁用 SafeExec
- `OPENCLAW_AGENT_CALL`：在代理模式下（非交互式）自动启用 SafeExec
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

SafeExec 检测到此命令为高风险操作（删除文件），并在会话中显示审批提示。

**低风险操作可无需审批直接执行：**
```
List files in /home/user/documents
```

## 全局控制

- **检查状态：**
```
safe-exec-list
```

- **查看审计日志：**
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
- 相关的审计日志文件（`~/.openclaw/safe-exec-audit.log`）

## 审计日志

所有命令执行记录包含以下信息：
- 时间戳
- 执行的命令
- 风险等级
- 执行模式（user_approved 或 agent_auto）
- 审批状态
- 执行结果
- 用于追踪的请求 ID

日志文件位置：`~/.openclaw/safe-exec-audit.log`

## 安全性与隐私

**SafeExec 的功能：**
- ✅ 在命令执行前进行拦截
- ✅ 使用正则表达式检测危险模式
- ✅ 对高风险命令请求用户批准
- ✅ 将所有操作记录到本地审计日志文件
- ✅ 完全在本地机器上运行

**SafeExec 不会：**
- ❌ 不监控聊天会话或对话历史
- ❌ 不读取 OpenClaw 会话数据
- ❌ 不进行外部网络请求（安装期间除外）
- ❌ 不向外部服务发送数据
- ❌ 无后台监控进程或定时任务
- ❌ 不与外部通知服务（如 Feishu、WebHook 等）集成

## 集成

SafeExec 与 OpenClaw 代理无缝集成。启用后，无需修改代理行为或命令结构即可正常使用。审批流程完全在本地进行，不依赖任何外部通信平台。

## 平台兼容性

SafeExec 在 **会话层面** 运行，适用于 OpenClaw 支持的任何通信渠道（WebChat、Feishu、Telegram、Discord 等）。审批流程通过终端完成，确保您始终能够控制命令的执行。

## 支持与社区

- **GitHub 仓库：** https://github.com/OTTTTTO/safe-exec
- **问题跟踪器：** https://github.com/OTTTTTO/safe-exec/issues
- **文档：** [README.md](https://github.com/OTTTTTO/safe-exec/blob/master/README.md)
- **ClawdHub：** https://www.clawhub.ai/skills/safe-exec

## 许可证

遵循 MIT 许可证——详情请参阅 [LICENSE](https://github.com/OTTTTTO/safe-exec/blob/master/LICENSE)。
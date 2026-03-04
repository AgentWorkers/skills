---
name: chainwatch
description: 通过 Chainwatch 策略引擎实现对 shell 命令的运行时安全性检查
user-invocable: false
metadata: {"openclaw":{"requires":{"bins":["chainwatch"]}}}
---
# Chainwatch 安全性执行机制

您可以使用 `chainwatch`，这是一个运行时控制平面，用于对 shell 命令、HTTP 请求和文件操作执行确定性的安全策略。

## 使用场景

在执行以下任何操作时，必须通过 `chainwatch` 路由命令：

- **破坏性操作**：`rm`、`dd`、`mkfs`、`chmod -R` 等删除或覆盖数据的命令
- **权限提升**：`sudo`、`su` 等修改用户权限的命令
- **网络操作**：`curl`、`wget`、对外部 API 的 HTTP 请求、任何出站数据传输
- **凭证访问**：读取或写入 `.env`、`.ssh/`、`.aws/` 等凭证文件
- **Git 操作**：`git push`、`git reset`、`git rebase`（任何修改远程仓库状态的命令）
- **包管理**：`apt install`、`pip install`、`npm install`（可能存在供应链风险）
- **系统配置**：编辑 `/etc/` 文件、systemd 单元文件、cron 任务、防火墙规则

## 使用方法

在命令前加上 `chainwatch exec --profile clawbot --`：

```bash
# Instead of:
rm -rf /tmp/old-data

# Use:
chainwatch exec --profile clawbot -- rm -rf /tmp/old-data
```

如果 `chainwatch` 阻止了该命令，它会返回一个 JSON 对象：
```json
{
  "blocked": true,
  "decision": "deny",
  "reason": "denylisted: command pattern blocked: rm -rf"
}
```

当命令被阻止时：
1. 向用户报告阻止的原因
2. 不得尝试绕过阻止机制
3. 询问用户希望如何继续操作

## 干运行检查

在执行高风险命令之前，您可以先检查策略是否允许该命令执行：

```bash
chainwatch evaluate --tool command --resource "rm -rf /tmp/data" --profile clawbot
```

## 无需安全执行的命令

这些命令不需要使用 `chainwatch` 进行包装：
- `ls`、`cat`、`head`、`tail`、`grep`、`find`、`wc`（仅用于读取）
- `echo`、`printf`、`date`、`uptime`、`whoami`（用于显示信息）
- `cd`、`pwd`、`env`（用于 shell 导航）
- `git status`、`git log`、`git diff`（仅用于查看 Git 仓库状态）

## 审批流程

如果 `chainwatch` 返回 `"decision": "require_approval"`，则表示该命令需要审批：
1. 告知用户该命令需要审批
2. 向用户展示 `chainwatch` 指出的问题
3. 用户可以通过 `chainwatch approve <approval-key>` 进行审批
4. 审批通过后，重新尝试执行原始命令

## 审计

所有 `chainwatch` 的决策都会被记录下来。您可以通过以下方式查看审计日志：
```bash
chainwatch audit verify /tmp/nullbot-daemon.jsonl
```

---
**Chainwatch 技能文档 v1.0**
作者：ppiankov
版权所有 © 2026 ppiankov
官方仓库：https://github.com/ppiankov/chainwatch
许可证：MIT

如果本文档出现在其他地方，请以上述官方仓库中的版本为准。
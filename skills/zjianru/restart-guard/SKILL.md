---
name: restart-guard
description: 安全地重启 OpenClaw Gateway，同时保留上下文信息、进行健康状态监控并发送故障通知。适用于需要重启 Gateway 的情况（例如配置更改、模型切换、插件重新加载或任何其他需要重启的原因）。该流程包括重启前的上下文保存、守护进程的启动、Gateway 的重启触发、重启后的验证以及故障通知的发送。
---

# 重启守护进程

安全地重启 OpenClaw Gateway，同时保留系统上下文并自动进行健康检查。

## 先决条件

- `openclaw.json` 文件中配置了 `commands.restart: true`
- 代理程序具有 `gateway` 和 `exec` 工具的执行权限
- 配置文件已准备好（复制 `config.example.yaml`，填写相关参数，通过 `--config` 选项传递）

## 工作流程

```
write_context.py → restart.py → [SIGUSR1] → guardian.py monitors → postcheck.py verifies
```

### 1. 生成上下文文件

生成一个上下文文件，该文件包含 YAML 格式的元数据（机器可读的内容，如重启原因、需要执行的验证命令、恢复步骤以及回滚路径）以及 Markdown 格式的说明性内容（供人类阅读）。

### 2. 重启系统

```bash
python3 <skill-dir>/scripts/restart.py --config <config-path> --reason "config change"
```

验证上下文的正确性 → 检查重启冷却时间限制 → 备份 `openclaw.json` 文件 → 启动守护进程（该进程在重启过程中保持独立运行） → 发送重启前的通知 → 触发 `gateway.restart` 功能。

### 3. 重启后的验证

当 Gateway 与系统重新建立连接后：

```bash
python3 <skill-dir>/scripts/postcheck.py --config <config-path>
```

从上下文文件中读取需要执行的验证命令，逐一执行这些命令，并将执行结果与预期值进行比较。最终返回 JSON 格式的结果或可读的报告。

### 4. 守护进程的行为

守护进程会独立运行，每隔 N 秒查询一次 `openclaw health --json` 的命令状态：
- **成功**：发送通知，解除重启限制，程序以 0 状态退出
- **超时**：执行诊断操作（如 `openclaw doctor`、查看日志），发送失败通知并附带诊断信息，解除重启限制，程序以 1 状态退出

通知优先级：首先通过 OpenClaw 自带的消息通知工具发送；若该工具不可用，则通过所有配置好的备用渠道（如 Telegram、Discord、Slack 或通用 Webhook）发送通知。可以同时启用多个通知渠道。

## 安全性措施

- **重启冷却时间限制**：两次重启之间的最小间隔时间（默认为 600 秒）
- **连续失败限制**：连续失败 N 次后自动停止重启（默认值为 3 次）
- **配置文件备份**：每次重启前都会备份 `openclaw.json` 文件
- **守护进程的独立运行**：守护进程在后台运行（使用 `setid` 命令创建独立进程 ID），而不是在 `exec` 背景任务中执行

## 故障排除

有关常见问题的解决方法，请参阅 `references/troubleshooting.md`（例如：清理锁定状态、通知失败、验证结果不匹配等问题）。
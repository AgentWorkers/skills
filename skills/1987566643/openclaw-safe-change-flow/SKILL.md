---
name: openclaw-safe-change-flow
description: 安全的 OpenClaw 配置变更工作流程：包括备份、验证、健康检查以及主实例和辅助实例的回滚机制。
---
# OpenClaw 安全变更流程

在修改可能影响系统可用性的 OpenClaw 配置之前，请务必使用此流程。

## 范围

- 主实例配置：`~/.openclaw/openclaw.json`
- 辅助实例配置（可选）：`~/.openclaw-wife/.openclaw/openclaw.json`

## 工作流程（必须执行）

1. **首先备份数据**
   - 生成带有时间戳的备份文件：`*.bak.safe-YYYYmmdd-HHMMSS`

2. **仅应用最小范围的更改**
   - 仅修改必要的配置项。

3. **验证与检查系统状态**
   - 主实例：`openclaw status --deep`
   - 辅助实例：`OPENCLAW_HOME=~/.openclaw-wife openclaw gateway health --url ws://127.0.0.1:18889 --token <token>`

4. **失败时进行回滚**
   - 恢复最新的安全备份并重启辅助实例的网关服务。

5. **确认通道状态**
   - 确认两个实例中的 Telegram/API 通道均能正常响应。

## 快速命令模板

```bash
TS=$(date +%Y%m%d-%H%M%S)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.safe-$TS
[ -f ~/.openclaw-wife/.openclaw/openclaw.json ] && cp ~/.openclaw-wife/.openclaw/openclaw.json ~/.openclaw-wife/.openclaw/openclaw.json.bak.safe-$TS

# ...apply config edits...

openclaw status --deep
OPENCLAW_HOME=~/.openclaw-wife openclaw gateway health --url ws://127.0.0.1:18889 --token wife-instance-token-18889
```

## 注意事项

- 切勿将未经验证的配置更改直接部署到生产环境中。
- 如果系统架构拒绝某些配置项，请移除不支持的字段并重新进行验证。
- 建议先在辅助实例上测试可能带来风险的更改。
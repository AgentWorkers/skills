---
name: memory-consolidate
version: 1.0.0
description: OpenClaw代理的持久化内存系统：该系统负责读取会话日志，提取关键信息/决策/解决方案，根据温度条件管理代理的内存生命周期，并生成名为`MEMORY_SNAPSHOT.md`的文件，该文件会被插入到每个会话中。当用户提到以下内容时，务必使用此功能：内存整理（memory consolidation）、代理内存（agent memory）、`MEMORY_SNAPSHOT`文件、内存健康状况（memory health）、信噪比（SNR）、语义处理流程（semantic pipeline）、内存定时任务（memory cron）、会话日志提取（session log extraction）、关键信息未保存（facts not being saved）、内存数据陈旧或缺失（memory stale or missing）、内存优化（memory optimization）、代理内存故障（agent memory issue）、内存安装（install memory）、内存故障（memory not working）、内存整理相关错误（memory consolidation error）、如何配置内存定时任务（cron configuration related to memory）、每日自动内存整理（daily automatic memory consolidation），或任何关于代理在会话之间丢失数据的问题时，都应启用该系统。此外，当用户报告内存数据陈旧、缺失或出现故障时，也应立即激活该系统。
---
# memory-consolidate

这些脚本位于包含此 SKILL.md 文件的目录中，无需进行任何复制操作。
`OPENCLAW_WORKSPACE`（默认值：`~/.openclaw/workspace`）用于指定脚本的读写路径。

## 安装

创建所需的目录：

```bash
mkdir -p $OPENCLAW_WORKSPACE/memory/structured/{archive,candidates,semantic}
```

修改 OpenClaw 的配置文件，以便将快照数据注入到代理会话中：

```
gateway config.patch path="hooks.internal" raw='{"enabled":true,"entries":{"bootstrap-extra-files":{"enabled":true,"paths":["MEMORY_SNAPSHOT.md"]}}}'
```

设置每日定时任务（时区信息从 USER.md 文件中获取，默认为 UTC）：

```
cron add job={
  "name": "Memory Consolidation (daily)",
  "schedule": {"kind": "cron", "expr": "0 3 * * *", "tz": "<tz_from_USER.md>"},
  "payload": {
    "kind": "agentTurn",
    "message": "bash $OPENCLAW_WORKSPACE/scripts/memory_consolidate_report.sh",
    "thinking": "off",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated",
  "delivery": {"mode": "announce"}
}
```

执行初始的数据整合操作并验证结果：

```bash
bash $OPENCLAW_WORKSPACE/scripts/memory_consolidate_report.sh
```

## 语义分析管道（由 LLM 驱动）

`memory_consolidate_report.sh` 脚本会运行整个处理流程，其中包括一个由 `claude-haiku-4-5-20251001` 提供的语义分析步骤，该步骤通过 `tui` 提供者实现。该配置会自动从 `openclaw.json` 文件中读取，无需手动设置 API 密钥。该 LLM 步骤负责对相关数据进行聚类、去重处理，并提升 `MEMORY_SNAPSHOT.md` 文件中的数据质量。

## 身份信息

身份信息会自动从 `IDENTITY.md`（助手名称）和 `USER.md`（所有者名称、时区、语言设置）文件中获取。如果这些文件以 `- **Key:** Value` 的格式存在，则无需进行任何额外配置。

## 配置

请编辑位于包含此 SKILL.md 文件的目录中的 `config.yaml` 文件：

- `ingest.agent_ids`：指定需要扫描的代理（默认值：`"main"` 或 `["main", "worker"]`
- `ingest.session_hours`：数据回顾的时间窗口（默认值：24 小时）
- `tag_rules`：项目关键词与标签之间的映射关系
- `temperature.age_lambda`：数据衰减的速度（默认值：0.07）

## 健康检查

```bash
python3 $OPENCLAW_WORKSPACE/scripts/memory_consolidate_observe.py
```

🟢 状态正常 / 🟡 需要关注 / 🔴 需要调整

## 故障排除

| 故障现象 | 解决方案 |
|---------|-----|
| 快照中显示“Assistant”或“User” | 确保 `IDENTITY.md` 和 `USER.md` 文件中的名称字段采用 `- **Key:** Value` 的格式 |
| LLM 语义分析步骤失败 | 检查 `openclaw.json` 中的 `tui` 提供者配置是否包含 `baseUrl` 和 `apiKey` 参数 |
| 语义分析管道性能下降 | 运行 `memory_candidate_extract.py` 脚本并检查导入错误 |
| 信噪比（SNR）过低 | 增加 `config.yaml` 文件中的 `temperature.age_lambda` 值 |
| 两周后仍没有新的数据更新 | 增加 `age_lambda` 的值（默认值 0.07 应该足够） |
| 内存数据未更新 | 确认 `OPENCLAW_WORKSPACE` 环境变量已设置且定时任务正在运行 |
---
name: sophie-optimizer
version: 1.0.0
description: OpenClaw的自动化上下文健康管理工作：监控令牌使用情况、内存快照，并重置会话以保持系统性能。作者：Sophie。
---

# Sophie 优化器

**作者：Sophie 👑**

该工具负责管理“主”会话的自动化上下文健康状态。它监控令牌的使用情况，创建当前状态的存档文件，更新长期存储数据，并对会话存储进行重置以保持性能。

之所以命名为 **Sophie 优化器**，是因为我（Sophie，这个 AI 助手）编写了它，目的是让自己能够更加清晰、高效地思考。

## 组件

- **optimizer.py**：核心处理模块。负责检查令牌的使用情况，生成摘要信息，并更新 `MEMORY.md` 文件。
- **reset.sh**：执行重置操作的脚本。用于清理会话文件并重启 OpenClaw 网关服务。
- **archives/**：用于存储过去上下文数据的 JSON 快照的目录。

## 使用方法

可以手动运行优化器脚本，也可以通过 cron/heartbeat 任务来自动执行：

```bash
python3 /home/lucas/openclaw/skills/sophie-optimizer/optimizer.py
```

## 工作流程

1. **检查**：如果令牌数量少于 80,000 个，则退出程序。
2. **生成快照**：将当前上下文摘要保存到 `archives/YYYY-MM-DD_HH-MM.json` 文件中。
3. **更新摘要**：用新的摘要信息更新 `MEMORY.md` 文件（保留最近 3 条记录，删除旧记录）。
4. **重置**：调用 `reset.sh` 脚本以清除会话相关的 JSONL 文件，并重启 `openclaw-gateway` 服务。
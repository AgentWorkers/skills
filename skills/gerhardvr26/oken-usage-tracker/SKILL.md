---
name: token-usage-tracker
description: OpenClaw 的令牌使用日志记录、警报功能以及上下文压缩工具。当您需要跟踪每次调用中令牌的使用情况、统一时间戳格式，并通过摘要/压缩减少发送给大型语言模型（LLMs）的上下文数据时，可以使用这些工具。
---
# token-usage-tracker

**快速入门**

1. 在 `skill-config.json` 中配置默认值（时区、日志文件夹）。
2. 将提供的脚本安装到您的工作空间中，并将拦截器集成到您的消息处理流程中。
3. 在发送大量数据之前，使用 `scripts/context_summarizer.py` 来减少令牌的使用量。

**该技能的功能**

- **日志记录**：`token_tracker.py` 会将每次调用的令牌使用情况记录到 JSONL 格式的日志文件中，并对时间戳进行标准化处理。
- **拦截器**：`token_interceptor.py` 示例代码用于标准化时间戳，并将处理后的消息转发给跟踪系统。
- **警报功能**：`token_alerts.py` 提供基于阈值的警报功能（默认情况下不会外部发布警报）。
- **压缩功能**：`context_summarizer.py` 生成简短的摘要以减少令牌传输的数据量。
- **辅助工具**：提供迁移和清理脚本（用于转换时间戳、去重日志条目）。

**使用场景**

- 当您需要透明地记录每次调用的令牌使用情况、希望降低令牌使用量，或希望在数据发送到模型之前对敏感/冗长的数据进行压缩处理时，可以使用该技能。

**文件结构**

- `scripts/`
  - `token_interceptor.py` — 时间戳标准化拦截器示例
  - `token_tracker.py` — 日志记录辅助工具
  - `token_alerts.py` — 警报功能示例代码
  - `context_summarizer.py` — 数据压缩辅助工具
  - `migrate_timestamps.py` — 时间戳迁移工具
  - `dedupe_log.py` — 日志去重工具
- `references/`
  - `examples/systemd/` — systemd 单元文件示例（需手动安装）
- `skill-config.json` — 可配置的默认设置
- `README.md` — 使用说明和安装指南

**配置信息**

请参阅 `skill-config.json` 以了解默认配置项。该技能支持以下配置：
- **时区**：默认为 UTC
- **日志文件夹**：默认为 `./skills/logs`（相对于 OpenClaw 工作空间）
- **压缩设置**：`summary_target_tokens`、`max_context_tokens`

**安全性与安装**

- 这些脚本仅为示例代码，默认情况下不会修改系统状态或自动安装服务。
- `references/systemd/` 目录中提供了 systemd 单元文件示例——请在审核后手动应用这些文件。

**许可证**

MIT 许可证（可根据需要自行调整）。
---
name: temporal-cortex-datetime
description: 转换时区、解析自然语言时间表达（例如“下周二下午2点”）、计算时间间隔，并根据夏令时（DST）调整时间戳。无需任何凭证信息——所有工具都仅进行本地计算。
  Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. No credentials needed — all tools are pure local computation.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) to download and run the MCP server binary from npm. No OAuth or credentials needed — all 5 tools are pure local computation after server startup. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.5.5"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    requires:
      bins:
        - npx
---
# 时间上下文与日期时间处理

提供了5个用于时间定位和日期时间计算的工具。这些工具均仅进行本地计算（运行时不调用任何外部API），具有幂等性（多次调用结果相同），且无需OAuth认证、凭证或配置信息——在MCP服务器启动后立即可用。

## 工具列表

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 在任何会话中首次调用时使用。返回当前时间、时区、UTC偏移量、夏令时状态以及夏令时预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为RFC 3339格式。支持60多种表达方式，例如：“下周二下午2点”、“明天早上”、“+2小时”、“下周开始”等。 |
| `convert_timezone` | 在IANA时区之间转换RFC 3339格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时间间隔（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示“将时间向前推进1天（保持实际时钟时间不变）”。 |

## 运行环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（版本@temporal-cortex/cortex-mcp@0.5.5）内部，该服务器是一个编译后的Rust二进制文件，通过npm包进行分发。

**启动过程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp@0.5.5`（仅下载一次，随后会缓存到本地）。
2. MCP服务器作为本地进程启动，并通过标准输入输出（stdio）进行通信。
3. 这5个日期时间处理工具在启动后仅进行本地计算，不再调用任何外部API。

**网络访问：**仅在首次下载npm包时需要网络连接；缓存后，后续启动均可离线使用。这些工具本身不会发送任何网络请求。

**无需凭证：**与调度技能不同，这些工具不需要OAuth令牌或API密钥。

**验证方式：**该包的来源可通过[npm SLSA](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp#provenance)进行验证。源代码托管在[github.com/temporal-cortex/platform](https://github.com/temporal-cortex/platform)，采用MIT许可证。每次发布版本时都会提供SHA256校验和（[GitHub Release页面](https://github.com/temporal-cortex/mcp/releases)可查看）。

## 重要规则：
1. **在进行时间相关的操作前，务必先调用`get_temporal_context`——切勿直接使用默认的时间或时区设置。**
2. **在查询之前进行转换：**在将时间表达式传递给日历工具之前，需使用`resolve_datetime`将其转换为RFC 3339格式。 |
3. **时区处理：**所有日期时间处理工具生成的输出都会包含时区偏移量。

## `resolve_datetime`的表达式格式支持**

该工具支持60多种表达方式，分为10个类别：

| 类别 | 示例 |
|----------|---------|
| 相对时间 | `now`（现在）、`today`（今天）、`tomorrow`（明天）、`yesterday`（昨天） |
| 命名日期 | `next Monday`（下周一）、`this Friday`（本周五）、`last Wednesday`（上周三） |
| 一天中的时间 | `morning`（09:00）、`noon`（12:00）、`evening`（18:00）、`eob`（17:00） |
| 时钟时间 | `2pm`（下午2点）、`14:00`（14:00）、`3:30pm`（下午3:30） |
| 时间偏移量 | `+2h`（提前2小时）、`-30m`（延迟30分钟）、`in 2 hours`（2小时后） |
| 复合时间表达式 | `next Tuesday at 2pm`（下周二下午2点）、`tomorrow morning`（明天早上）、`this Friday at noon`（本周五中午） |
| 时间周期边界 | `start of week`（一周开始）、`end of month`（月底）、`start of next week`（下周开始）、`end of last month`（上个月底） |
| 周序日期 | `first Monday of March`（三月的第一个周一）、`third Friday of next month`（下个月的第三个周五） |
| 直接使用RFC 3339格式 | `2026-03-15T14:00:00-04:00`（原样返回） |
| 考虑周起始日：**根据配置的`WEEK_START`（默认为周一，也可设置为周日） |

## 常见使用场景：

- **获取当前时间上下文**  
- **解析会议时间**  
- **跨时区转换**  
- **计算时间间隔**  
- **考虑夏令时的时间调整**  

## 额外参考资料：  
- [日期时间工具参考](references/DATETIME-TOOLS.md) — 提供了这5个工具的完整输入/输出格式规范
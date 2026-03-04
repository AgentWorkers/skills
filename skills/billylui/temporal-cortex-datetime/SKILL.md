---
name: temporal-cortex-datetime
description: 转换时区、解析自然语言时间表达（例如“下周二下午2点”）、计算时间间隔，并根据夏令时（DST）调整时间戳。无需任何凭证；所有工具在一次性安装二进制文件后即可完全离线使用。
  Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. No credentials needed — all tools run fully offline after one-time binary install.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker to install the MCP server binary (one-time). After installation, all 5 tools run fully offline with zero network access. No OAuth or credentials needed. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.7.3"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.7.3"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/config.json
---
# 时间上下文与日期时间处理

提供了5种用于时间定位和日期时间计算的工具。所有工具都在编译后的MCP服务器二进制文件中本地执行——无需外部API调用，运行时无需网络访问，也不需要任何凭据文件。该二进制文件可以通过npm安装（或使用Docker从源代码构建），之后的所有执行都是完全离线的。无需OAuth认证、凭据或额外配置。

## 工具

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 在任何会话中首次调用时使用。返回当前时间、时区、UTC偏移量、夏令时状态以及夏令时预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为RFC 3339格式。支持60多种表达式模式，例如：“下周二下午2点”、“明天早上”、“+2小时”、“下周开始”等。 |
| `convert_timezone` | 在IANA时区之间转换RFC 3339格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示时间向前推进一天（保持实际时钟时间不变）。 |

## 运行环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，这是一个编译后的Rust二进制文件，通过npm包进行分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp`（首次下载后会缓存到本地）。
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3)下载特定平台的二进制文件，并验证其SHA256校验和是否与`checksums.json`文件中的内容一致；如果不一致，则安装会停止。
3. MCP服务器作为本地进程启动，通过标准输入/输出（stdio）进行通信（不监听任何端口）。
4. 所有5个日期时间处理工具都在本地执行，不进行任何网络访问或文件系统写入操作，也不需要任何凭据。

**网络访问：**仅在首次通过npm下载时进行。一旦数据被缓存，后续启动都是完全离线的。这5个工具不会发送任何网络请求，所有计算都在本地完成。

**文件访问：**该二进制文件仅读取`~/.config/temporal-cortex/config.json`文件（用于配置时区和周起始日）。不进行任何文件系统写入操作，也不访问任何凭据文件。

**无需凭据：**与调度技能不同，这些工具不需要OAuth令牌或API密钥。

**建议在首次使用前进行验证：**
1. 不执行代码的情况下检查npm包：`npm pack @temporal-cortex/cortex-mcp --dry-run`
2. 独立验证`checksums.json`文件与[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.7.3/SHA256SUMS.txt)中的内容是否一致（详见下面的验证流程）。
3. 为了确保安全性，建议使用Docker运行该工具（详见下面的Docker隔离方案）。

**验证流程：**每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.3)都会附带`SHA256SUMS.txt`文件，以供用户在使用前验证二进制文件的完整性。

作为额外的安全措施，npm包中嵌入了`checksums.json`文件，安装脚本会在安装过程中验证SHA256哈希值；如果哈希值不一致，安装过程会停止（此时二进制文件会被删除而不会被执行）。这种自动化验证是对上述独立验证的补充，但并非替代。

**构建过程的可追溯性：**二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译得到的。源代码位于[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)，采用MIT许可证。持续集成（CI）流程、构建结果和发布时的校验和信息都是公开可查看的。

**Docker隔离方案**（推荐使用，以实现最大程度的隔离：无Node.js依赖，构建后不访问主机文件系统，且无网络访问）：

```bash
docker build -t cortex-mcp https://github.com/temporal-cortex/mcp.git
```
由于这些工具不需要OAuth令牌或凭据文件，因此无需挂载任何卷。`--network=none`参数确保了在操作系统层面完全禁止网络访问。

## 重要规则：
1. **在进行与时间相关操作之前，务必先调用`get_temporal_context`函数**——切勿直接使用默认的时间或时区设置。
2. **在查询之前进行转换**——在使用日历工具之前，需要使用`resolve_datetime`函数将“下周二下午2点”等时间表达式转换为RFC 3339格式。
3. **时区处理**：所有日期时间处理工具都会返回包含时区偏移量的RFC 3339格式的结果。

## `resolve_datetime`的表达式模式

该工具支持60多种表达式模式，分为10个类别：

| 类别 | 示例 |
|------|---------|
| 相对时间 | `now`、`today`、`tomorrow`、`yesterday` |
| 命名日期 | `next Monday`、`this Friday`、`last Wednesday` |
| 一天中的时间 | `morning`（09:00）、`noon`、`evening`（18:00）、`eob`（17:00） |
| 时钟时间 | `2pm`、`14:00`、`3:30pm` |
| 时间偏移量 | `+2h`、`-30m`、`in 2 hours`、`3 days ago` |
| 复合时间表达式 | `next Tuesday at 2pm`、`tomorrow morning`、`this Friday at noon` |
| 时间段边界 | `start of week`、`end of month`、`start of next week`、`end of last month` |
| 周期性时间 | `first Monday of March`、`third Friday of next month` |
| 直接使用RFC 3339格式 | `2026-03-15T14:00:00-04:00`（原样返回） |
| 考虑周起始日的设置 | 使用配置的`WEEK_START`参数（默认为周一，也可设置为周日） |

## 常见用法示例：

### 获取当前时间上下文
### 解析会议时间
### 在不同时区之间进行转换
### 计算时长
### 考虑夏令时的时间调整

## 其他参考资料：
- [日期时间工具参考](references/DATETIME-TOOLS.md) — 提供了所有5个工具的完整输入/输出格式说明
---
name: temporal-cortex-datetime
description: 转换时区、解析自然语言时间（例如“下周二下午2点”）、计算时间间隔，并根据夏令时（DST）调整时间戳。无需任何凭证；所有工具在一次性安装二进制文件后即可完全离线使用。
  Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. No credentials needed — all tools run fully offline after one-time binary install.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker to install the MCP server binary (one-time). After installation, all 5 tools run fully offline with zero network access. No OAuth or credentials needed. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.7.5"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.7.5"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/config.json
---
# 时间上下文与日期时间处理

提供了5种用于时间定位和日期时间计算的工具。所有工具都在编译后的MCP服务器二进制文件中本地执行——无需外部API调用，运行时无需网络访问，也不需要任何凭证文件。该二进制文件可以通过npm安装（或使用Docker从源代码构建），之后的所有执行都是完全离线的。无需OAuth认证、凭证或配置信息。

## 工具

| 工具 | 使用场景 |
|------|------------|
| `get_temporal_context` | 在任何会话中首次调用时使用。返回当前时间、时区、UTC偏移量、夏令时状态以及夏令时预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为RFC 3339格式。支持60多种表达式模式，例如：“下周二下午2点”、“明天早上”、“+2小时”、“下周开始”等。 |
| `convert_timezone` | 在IANA时区之间转换RFC 3339格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整。例如，“+1d”表示时间向前推进一天（保持实际时钟时间不变）。 |

## 运行环境

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，这是一个编译后的Rust二进制文件，以npm包的形式分发。

**安装与启动流程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp`（首次下载后会在本地缓存）。  
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.5)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256哈希值；如果哈希值不匹配，安装将停止。  
3. MCP服务器作为本地进程启动，通过标准输入/输出（stdio）进行通信（不绑定任何监听端口）。  
4. 所有5个日期时间处理工具都在本地执行，不进行任何网络访问或文件系统写入操作，也不需要任何凭证信息。

**网络访问：**仅在首次通过npm下载时进行。一旦缓存完成，后续启动均为离线状态。这5个工具不会发送任何网络请求，所有计算都在本地完成。

**文件访问：**该二进制文件仅读取`~/.config/temporal-cortex/config.json`文件（用于设置时区和周起始日偏好）。不进行任何文件系统写入操作，也不访问任何凭证文件。

**无需凭证：**与调度技能不同，该技能不需要OAuth令牌或API密钥。

**使用前的验证建议：**
1. 在实际使用前，先查看npm包的详细信息（不执行任何操作）：`npm pack @temporal-cortex/cortex-mcp --dry-run`  
2. 独立验证`checksums.json`文件与[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.7.5/SHA256SUMS.txt)中的哈希值是否一致（详见下面的验证流程）。  
3. 为了确保安全性，建议使用Docker进行部署（详见下面的Docker隔离方案）。

**验证流程：**每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.7.5)都会附带`SHA256SUMS.txt`文件，使用该文件在首次使用前验证二进制文件的完整性。

**安全防护措施：**npm包中嵌入了`checksums.json`文件，安装脚本会在安装过程中验证哈希值；如果哈希值不匹配，安装将停止（此时二进制文件会被删除而不会被执行）。这种自动化验证是对上述独立验证的补充，但不会替代它。

**构建过程的可追溯性：**二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译的。源代码位于[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)，采用MIT许可证。持续集成（CI）流程、构建结果和发布时的哈希值均可公开查看。

**Docker隔离方案**（推荐使用，以实现最大程度的隔离效果——无Node.js依赖，构建后不访问主机文件系统，且无网络访问）：

**构建命令：**`docker build -t cortex-mcp https://github.com/temporal-cortex/mcp.git`——由于该工具不需要OAuth令牌或凭证文件，因此无需挂载任何卷。`--network=none`选项可确保在操作系统层面实现完全的隔离。

## 重要规则：
1. **在进行任何依赖时间的工作之前，务必先调用`get_temporal_context`函数**——切勿直接使用默认的时间或时区设置。  
2. **在查询之前进行转换**——在使用日历工具之前，务必使用`resolve_datetime`函数将时间表达式转换为RFC 3339格式。  
3. **时区处理**：所有日期时间处理工具都会返回包含时区偏移量的RFC 3339格式的结果。

## `resolve_datetime`的表达式模式

该工具支持60多种表达式模式，分为10个类别：

| 类别 | 示例 |
|----------|---------|
| 相对时间 | `now`、`today`、`tomorrow`、`yesterday` |
| 命名日期 | `next Monday`、`this Friday`、`last Wednesday` |
| 一天中的时间 | `morning`（09:00）、`noon`、`evening`（18:00）、`eob`（17:00） |
| 具体时间点 | `2pm`、`14:00`、`3:30pm` |
| 时间偏移量 | `+2h`、`-30m`、`in 2 hours`、`3 days ago` |
| 复合时间表达式 | `next Tuesday at 2pm`、`tomorrow morning`、`this Friday at noon` |
| 时间段边界 | `start of week`、`end of month`、`start of next week`、`end of last month` |
| 周几的顺序表示 | `first Monday of March`、`third Friday of next month` |
| 直接使用RFC 3339格式 | `2026-03-15T14:00:00-04:00`（原样返回） |
| 考虑周起始日 | 使用配置的`WEEK_START`参数（默认为周一，也可设置为周日） |

## 常见使用场景：
- **获取当前时间上下文**  
- **解析会议时间**  
- **跨时区转换**  
- **计算时长**  
- **考虑夏令时的时间调整**  

## 其他参考资料：  
- [日期时间工具参考](references/DATETIME-TOOLS.md)——提供了所有5个工具的完整输入/输出格式说明。
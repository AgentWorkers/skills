---
name: temporal-cortex-datetime
description: >
  **功能概述：**  
  - **时区转换：** 能够在多个时区之间进行时间转换。  
  - **自然语言时间解析：** 可以解析类似“下周二下午2点”这样的自然语言时间表达。  
  - **时长计算：** 能够计算两个时间点之间的时长。  
  - **夏令时（DST）处理：** 在进行时间计算和转换时，会自动考虑夏令时的影响。  
  **使用说明：**  
  无需任何认证信息；所有工具在一次性安装二进制文件后即可完全离线使用。
  Convert timezones, resolve natural language times ("next Tuesday at 2pm"), compute durations, and adjust timestamps with DST awareness. No credentials needed — all tools run fully offline after one-time binary install.
license: MIT
compatibility: |-
  Requires npx (Node.js 18+) or Docker to install the MCP server binary (one-time). After installation, all 5 tools run fully offline with zero network access. No OAuth or credentials needed. Works with Claude Code, Claude Desktop, Cursor, Windsurf, and any MCP-compatible client.
metadata:
  author: temporal-cortex
  version: "0.8.1"
  mcp-server: "@temporal-cortex/cortex-mcp"
  homepage: "https://temporal-cortex.com"
  repository: "https://github.com/temporal-cortex/skills"
  openclaw:
    install:
      - kind: node
        package: "@temporal-cortex/cortex-mcp@0.8.1"
        bins: [cortex-mcp]
    requires:
      bins:
        - npx
      config:
        - ~/.config/temporal-cortex/config.json
---
# 时间上下文与日期时间解析

提供了5种用于时间定位和日期时间计算的工具。这些工具都在编译后的MCP服务器二进制文件中本地执行——无需外部API调用，运行时无需网络访问，也不需要任何凭据文件。该二进制文件可以通过npm安装（或使用Docker从源代码构建），之后的所有执行都是完全离线的，无需OAuth或任何凭据。时区和周起始日的设置存储在`config.json`文件中。未设置的字段将默认使用系统时区和周一作为周起始日。

## 来源与出处

- **官方网站：** [temporal-cortex.com](https://temporal-cortex.com)  
- **源代码：** [github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（开源Rust项目）  
- **npm包：** [@temporal-cortex/cortex-mcp](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)  
- **Skills仓库：** [github.com/temporal-cortex/skills](https://github.com/temporal-cortex/skills)  

## 工具列表

| 工具       | 使用场景                |
|------------|----------------------|
| `get_temporal_context` | 每次会话开始时调用，返回当前时间、时区、UTC偏移量、夏令时状态及夏令时预测信息。 |
| `resolve_datetime` | 将人类可读的时间表达式转换为RFC 3339格式。支持60多种表达式，例如："下周二下午2点"、"明天早上"、"+2h"等。 |
| `convert_timezone` | 在IANA时区之间转换RFC 3339格式的日期时间。 |
| `compute_duration` | 计算两个时间戳之间的时长（以天、小时、分钟为单位）。 |
| `adjust_timestamp` | 考虑夏令时的时间戳调整，例如："+1d"表示向前调整一天（保持实际时钟时间不变）。 |

## 运行机制

这些工具运行在[Temporal Cortex MCP服务器](https://github.com/temporal-cortex/mcp)（`@temporal-cortex/cortex-mcp`）内部，该服务器是一个作为npm包发布的编译后的Rust二进制文件。

**安装与启动流程：**
1. 使用`npx`从npm仓库下载`@temporal-cortex/cortex-mcp`（首次下载后会在本地缓存）。  
2. 安装后的脚本会从[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.8.1)下载特定平台的二进制文件，并通过`checksums.json`文件验证其SHA256校验和；如果校验不匹配，安装将停止。  
3. MCP服务器作为本地进程启动，通过标准输入输出（stdio）进行通信（不监听任何端口）。  
4. 所有5个日期时间工具都在本地执行，不进行任何网络访问或文件系统操作，也不需要任何凭据。

**网络访问：** 仅在首次通过npm下载时进行。缓存后，后续启动均为离线状态。这5个工具不会发送任何网络请求，所有计算都在本地完成。

**文件访问：** 该二进制文件会读取`~/.config/temporal-cortex/config.json`文件以获取时区和周起始日的设置。未设置或缺失的字段将使用系统默认值。不会写入任何文件系统数据，也不会访问任何凭据文件。

**无需凭据：** 与调度技能不同，这些工具不需要OAuth令牌或API密钥。

**使用前的验证建议：**
1. 在实际使用前，先不执行代码，仅检查npm包的完整性：`npm pack @temporal-cortex/cortex-mcp --dry-run`  
2. 独立验证`SHA256SUMS.txt`文件（位于[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/download/mcp-v0.8.1/SHA256SUMS.txt)）中的校验和。  
3. 为确保安全性，建议在Docker环境中运行该工具（详见下方Docker相关内容）。

**验证流程：** 每次[GitHub发布版本](https://github.com/temporal-cortex/mcp/releases/tag/mcp-v0.8.1)都会附带`SHA256SUMS.txt`文件，以验证二进制文件的完整性。  

**安全措施：** npm包中嵌入了`checksums.json`文件，安装脚本会在安装过程中验证SHA256哈希值；如果校验不匹配，安装将停止（此时二进制文件会被删除而不会被执行）。这一自动化验证机制是对上述独立验证的补充，但并不替代它。

**构建过程：** 二进制文件是通过[GitHub Actions](https://github.com/temporal-cortex/mcp/actions)在5个平台上（darwin-arm64、darwin-x64、linux-x64、linux-arm64、win32-x64）交叉编译的，源代码位于[github.com/temporal-cortex/mcp](https://github.com/temporal-cortex/mcp)（采用MIT许可证）。持续集成（CI）流程、构建结果和发布时的校验和信息都是公开可查看的。

**Docker隔离方案（推荐使用）：** 可确保最大程度的隔离——无Node.js依赖，构建后不访问主机文件系统，且完全不进行网络通信：

**关键规则：**
1. **在进行时间相关操作前，务必先调用`get_temporal_context`函数**，切勿直接使用默认的时间或时区设置。  
2. **在查询之前进行转换：** 在将时间表达式传递给日历工具之前，使用`resolve_datetime`将其转换为RFC 3339格式。  
3. **时区处理：** 所有日期时间工具返回的格式都包含时区偏移量。

## `resolve_datetime`的表达式模式  

该工具支持60多种表达式模式，分为10个类别：  
| 类别        | 示例                          |
|-------------|--------------------------------------------|
| 相对时间    | `"now"`、`today"`、`tomorrow`、`yesterday`          |
| 命名日期    | `"next Monday"`、`this Friday"`、`last Wednesday`       |
| 一天中的时间    | `"morning"`（09:00）、`noon`、`evening`（18:00）、`eob`（17:00）    |
| 时钟时间    | `"2pm"`、`14:00"`、`3:30pm`                    |
| 时间偏移量    | `"+2h"`、`"-30m"`、`in 2 hours"`、`3 days ago`       |
| 复合时间表达式 | `"next Tuesday at 2pm"`、`tomorrow morning"`、`this Friday at noon` |
| 时间段边界    | `"start of week"`、`end of month"`、`start of next week`、`end of last month` |
| 周序日期    | `"first Monday of March"`、`third Friday of next month`     |
| 直接使用RFC 3339 | `"2026-03-15T14:00:00-04:00"`              |
| 考虑周起始日    | 使用配置的`WEEK_START`（默认为周一，也可设置为周日）     |

## 常见用法示例

- **获取当前时间上下文**  
- **解析会议时间**  
- **跨时区转换**  
- **计算时长**  
- **考虑夏令时的时间调整**  

## 其他参考资料  
- [日期时间工具参考](references/DATETIME-TOOLS.md) — 提供了所有5个工具的完整输入/输出格式说明。
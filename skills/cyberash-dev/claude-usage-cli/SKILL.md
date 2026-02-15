---
name: claude-usage-cli
description: 通过命令行查询 Claude API 的使用情况和费用报告。将管理员 API 密钥安全存储在 macOS 的 Keychain 中。输出格式为表格或 JSON。
metadata: {"clawdbot":{"emoji":"📊","os":["macos"],"requires":{"bins":["claude-usage","node"]},"install":[{"id":"npm","kind":"shell","command":"npm install -g claude-usage-cli","bins":["claude-usage"],"label":"Install claude-usage-cli via npm"}],"source":"https://github.com/cyberash-dev/claude-usage-cli"}}
---

# claude-usage-cli

⚠️ **已弃用** — 该工具已不再维护。请改用 [`claude-cost-cli`](https://clawhub.com/skills/claude-cost-cli)，它具有相同的功能，并且仍得到持续支持。

---

这是一个用于查询 Anthropic 管理 API 使用情况和成本数据的命令行工具（CLI）。需要从 Claude 控制台的“设置”→“管理密钥”中获取管理 API 密钥（格式为 `sk-ant-admin...`）。这些凭据会存储在 macOS 的 Keychain 中。

## 安装

需要 Node.js >= 18 和 macOS 环境。该工具为开源项目：https://github.com/cyberash-dev/claude-usage-cli

```bash
npm install -g claude-usage-cli
```

（如果您希望在运行前审核代码，可以从此源代码进行安装：）
```bash
git clone https://github.com/cyberash-dev/claude-usage-cli.git
cd claude-usage-cli
npm install && npm run build && npm link
```

安装完成后，`claude-usage` 命令将在全局范围内可用。

## 快速入门

```bash
claude-usage config set-key     # Interactive prompt: enter Admin API key (masked)
claude-usage usage              # Token usage for the last 7 days
claude-usage cost               # Cost breakdown for the last 7 days
claude-usage cost --sum         # Total spend for the last 7 days
```

## API 密钥管理

- **存储 API 密钥**：通过交互式提示输入密钥（系统会自动验证密钥是否以 `sk-ant-admin` 为前缀）：
```bash
claude-usage config set-key
```

- **查看已存储的密钥**：（密钥信息会被屏蔽显示）：
```bash
claude-usage config show
```

- **从 Keychain 中删除密钥**：
```bash
claude-usage config remove-key
```

## 使用报告

查询结果以 JSON 格式输出（适用于脚本编写）：
```bash
claude-usage usage                                    # Last 7 days, daily, grouped by model
claude-usage usage --period 30d                       # Last 30 days
claude-usage usage --from 2026-01-01 --to 2026-01-31 # Custom date range
claude-usage usage --model claude-sonnet-4            # Filter by model
claude-usage usage --api-keys apikey_01Rj,apikey_02Xz # Filter by API key IDs
claude-usage usage --group-by model,api_key_id        # Group by multiple dimensions
claude-usage usage --bucket 1h                        # Hourly granularity (1d, 1h, 1m)
```

输出列包括：日期（Date）、模型（Model）、输入令牌（Input Tokens）、缓存令牌（Cached Tokens）、输出令牌（Output Tokens）以及网络搜索结果（Web Searches）。

## 成本报告

查询结果以 JSON 格式输出（适用于脚本编写）：
```bash
claude-usage cost --json
claude-usage cost --sum --json
```

输出列包括：日期（Date）、描述（Description）、模型（Model）、费用（Amount，单位：USD）、令牌类型（Token Type）以及费用等级（Tier）。

## 命令参数说明

### `usage` 命令参数

| 参数          | 描述                                      | 默认值       |
|--------------|-----------------------------------------|------------|
| `--from <date>`    | 开始日期（格式：YYYY-MM-DD 或 ISO）                | 7 天前       |
| `--to <date>`    | 结束日期（格式：YYYY-MM-DD 或 ISO）                | 当前时间       |
| `--period <days>`   | 时间周期（7d、30d、90d）                        | 7 天         |
| `--model <models>`   | 按模型过滤（用逗号分隔）                        | 所有模型       |
| `--api-keys <ids>`   | 按 API 密钥 ID 过滤（用逗号分隔）                | 所有 API 密钥     |
| `--group-by <fields>` | 按模型、API 密钥 ID 或工作区 ID 分组                | 模型         |
| `--bucket <width>`   | 数据显示周期（1天、1小时、1分钟）                   | 1天         |
| `--json`       | 以 JSON 格式输出结果                         | 否           |

### `cost` 命令参数

| 参数          | 描述                                      | 默认值       |
|--------------|-----------------------------------------|------------|
| `--from <date>`    | 开始日期（格式：YYYY-MM-DD 或 ISO）                | 7 天前       |
| `--to <date>`    | 结束日期（格式：YYYY-MM-DD 或 ISO）                | 当前时间       |
| `--period <days>`   | 时间周期（7d、30d、90d）                        | 7 天         |
| `--group-by <fields>` | 按工作区 ID 或描述分组                        | 描述         |
| `--sum`       | 仅输出总费用                             | 否           |
| `--json`       | 以 JSON 格式输出结果                         | 否           |

## 安全性与数据存储

- **管理 API 密钥**：仅存储在 macOS 的 Keychain 中（服务名称：`claude-usage-cli`）。密钥绝不会以明文形式保存在磁盘上。
- **无配置文件**：所有设置均通过命令行参数传递；除了 Keychain 中的密钥信息外，没有任何数据会保存在磁盘上。
- **网络连接**：API 密钥仅通过 HTTPS 传输到 `api.anthropic.com`，不会建立其他网络连接。
- **权限限制**：该密钥仅具有读取组织使用情况和成本数据的权限，无法修改账单信息、创建新的 API 密钥或访问对话内容。
- **无缓存机制**：查询结果不会被缓存或保存到磁盘上。

## API 参考

该 CLI 使用的是 Anthropic 的管理 API：
- 使用情况查询：`GET /v1/organizations/usage_report/messages`
- 成本查询：`GET /v1/organizations/cost_report`

更多文档请参考：https://platform.claude.com/docs/en/build-with-claude/usage-cost-api
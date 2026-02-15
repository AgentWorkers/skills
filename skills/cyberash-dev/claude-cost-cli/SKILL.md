---
name: claude-cost-cli
description: **从命令行查询 Claude API 的使用情况和费用报告**  
**管理员 API 密钥的安全存储（使用 macOS Keychain）**  
**输出格式为表格或 JSON。**
metadata: {"clawdbot":{"emoji":"📊","os":["macos"],"requires":{"bins":["claude-cost","node"]},"install":[{"id":"npm","kind":"shell","command":"npm install -g claude-cost-cli","bins":["claude-cost"],"label":"Install claude-cost-cli via npm"}],"source":"https://github.com/cyberash-dev/claude-cost-cli"}}
---

# claude-cost-cli

这是一个用于查询Anthropic Admin API使用情况和费用数据的命令行工具（CLI）。需要从Claude控制台的“设置”（Settings）→“管理密钥”（Admin Keys）中获取Admin API密钥（格式为`sk-ant-admin...`）。该密钥会存储在macOS的Keychain中。

## 安装

要求安装Node.js版本≥18，并且操作系统为macOS。该工具完全开源，遵循MIT许可证：https://github.com/cyberash-dev/claude-cost-cli

```bash
npm install -g claude-cost-cli
```

该npm包附带了来源验证信息，通过GitHub Actions将每个版本与其对应的源代码提交链接起来。您可以在安装前验证已发布的包内容：
```bash
npm pack claude-cost-cli --dry-run
```

如果您希望在运行前审核代码，也可以选择从源代码进行安装：
```bash
git clone https://github.com/cyberash-dev/claude-cost-cli.git
cd claude-cost-cli
npm install && npm run build && npm link
```

安装完成后，`claude-cost`命令将在全局环境中可用。

## 快速入门

```bash
claude-cost config set-key     # Interactive prompt: enter Admin API key (masked)
claude-cost usage              # Token usage for the last 7 days
claude-cost cost               # Cost breakdown for the last 7 days
claude-cost cost --sum         # Total spend for the last 7 days
```

## API密钥管理

- **存储API密钥**：通过交互式提示输入密钥（系统会自动验证密钥前缀是否为`sk-ant-admin`）：
```bash
claude-cost config set-key
```

- **查看已存储的密钥**：可以查看存储在Keychain中的API密钥：
```bash
claude-cost config show
```

- **从Keychain中删除密钥**：
```bash
claude-cost config remove-key
```

## 使用报告

查询结果以JSON格式输出（便于脚本处理）：
```bash
claude-cost usage --json
claude-cost usage --period 30d --json
```

输出列包括：日期（Date）、模型（Model）、输入令牌数（Input Tokens）、缓存令牌数（Cached Tokens）、输出令牌数（Output Tokens）以及网络搜索次数（Web Searches）。

## 费用报告

查询结果同样以JSON格式输出（便于脚本处理）：
```bash
claude-cost cost --json
claude-cost cost --sum --json
```

输出列包括：日期（Date）、费用描述（Description）、模型（Model）、费用金额（Amount，单位：USD）、令牌类型（Token Type）以及费用等级（Tier）。

## 命令行参数说明

### `usage` 参数

| 参数          | 描述                        | 默认值         |
|--------------|----------------------------|-------------------|
| `--from <date>`    | 开始日期（格式：YYYY-MM-DD或ISO）            | 7天前             |
| `--to <date>`    | 结束日期（格式：YYYY-MM-DD或ISO）            | 当前时间           |
| `--period <days>`   | 时间周期（7天、30天、90天）                | 7天               |
| `--model <models>`   | 按模型筛选（用逗号分隔）                | 所有模型             |
| `--api-keys <ids>`   | 按API密钥ID筛选（用逗号分隔）                | 所有API密钥             |
| `--group-by <fields>` | 按模型、API密钥ID或工作区ID分组           | 模型               |
| `--bucket <width>`    | 数据显示周期（1天、1小时、1分钟）             | 1天               |
| `--json`       | 以JSON格式输出结果                   | 否                |

### `cost` 参数

| 参数          | 描述                        | 默认值         |
|--------------|----------------------------|-------------------|
| `--from <date>`    | 开始日期（格式：YYYY-MM-DD或ISO）            | 7天前             |
| `--to <date>`    | 结束日期（格式：YYYY-MM-DD或ISO）            | 当前时间           |
| `--period <days>`   | 时间周期（7天、30天、90天）                | 7天               |
| `--group-by <fields>` | 按工作区ID或费用描述分组               | 工作区ID/费用描述         |
| `--sum`       | 仅输出总费用                     | 否                |
| `--json`       | 以JSON格式输出结果                   | 否                |

## 安全性与数据存储

以下安全措施已在源代码中得到实现：

- **Admin API密钥**：仅存储在macOS的Keychain中（服务名称：`claude-cost-cli`）。根据设计，该密钥绝不会以明文形式保存在磁盘上。具体实现细节请参见[`src/infrastructure/keychain-credential-store.ts`](https://github.com/cyberash-dev/claude-cost-cli/blob/main/src/infrastructure/keychain-credential-store.ts)。
- **无配置文件**：所有设置均通过命令行参数传递；除Keychain中的密钥信息外，没有任何数据会保存在磁盘上。
- **网络连接**：API密钥仅通过HTTPS发送到`api.anthropic.com`，不会建立其他外部连接。详细实现请参见[`src/infrastructure/anthropic-usage-repository.ts`](https://github.com/cyberash-dev/claude-cost-cli/blob/main/src/infrastructure/anthropic-usage-repository.ts)`和[`src/infrastructure/anthropic-cost-repository.ts`)。
- **权限限制**：Admin API密钥仅具有读取组织使用情况和费用数据的权限，无法修改账单信息、创建新的API密钥或访问对话内容。这是Anthropic Admin API的默认设置（https://platform.claude.com/docs/en/build-with-claude/usage-cost-api），而非该CLI工具的特有功能。
- **无缓存机制**：查询结果不会被缓存或保存到磁盘上；CLI工具会将输出直接写入标准输出（stdout）。

## API参考

该CLI工具调用了Anthropic Admin API的以下接口：
- 使用情况查询：`GET /v1/organizations/usage_report/messages`
- 费用查询：`GET /v1/organizations/cost_report`

更多文档请参考：https://platform.claude.com/docs/en/build-with-claude/usage-cost-api
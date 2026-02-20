# openclaw-crm

这是一个以本地数据为中心的CRM系统，用于跟踪潜在客户、交易、跟进流程以及项目进展。该系统使用支持WAL（Write-Ahead Logging）模式的SQLite数据库，并通过Commander提供命令行界面（CLI）进行管理。

## 快速入门
- 进入项目目录：`cd skills/crm && npm install`
- 运行命令：`node src/cli.js lead add "John Doe" --email john@example.com`（用于添加新潜在客户）
- 生成数据交换文件：`node src/cli.js refresh`（用于更新数据库并生成数据交换文件）

## 集成
可以使用`exec`工具执行以下操作：
- `crm lead list`（列出所有潜在客户）
- `crm deal add "New Deal" --contact abc123 --value 10000`（用于添加新交易记录）

数据交换文件存储在`workspace/interchange/crm/`目录下，便于团队成员之间共享数据。
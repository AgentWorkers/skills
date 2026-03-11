---
name: splitwise
description: 通过 Splitwise CLI 管理共同开支。当需要与其他人一起记录、分摊或追踪开支、查看余额、确认谁欠了谁的钱、结清债务或列出最近的费用时，请使用该工具。该功能会在提到 Splitwise、共同开支、费用分摊、“记录这笔开支”、“谁欠了谁的钱”、室友/伴侣的账单或任何与费用追踪相关的请求时自动触发。此外，当在扫描电子邮件或分析订阅信息时发现账单时，也可以主动使用该工具进行记录。即使是像“和妮娜分摊这笔费用”或“添加网络费用”这样的简单指令，也应该触发该功能的执行。
---
# Splitwise CLI 功能

通过 `splitwise` CLI 管理共享开支、余额和结算。

## 设置

该 CLI 安装在 `~/.local/bin/splitwise` 目录下，并通过 OAuth 2.0 进行身份验证。令牌存储在 `~/.config/splitwise-cli/auth.json` 文件中。如果令牌过期，CLI 会提示您重新进行身份验证（需要通过浏览器完成 OAuth 流程）。

默认的共享开支组为 **Dolores**（Barron 和 Nina 的共享开支组）。对于他们的共享开支，您无需使用 `--group` 参数。

## 快速参考

### 查看余额
```bash
# Default group (Dolores) balances
splitwise balances

# Specific group
splitwise balances --group "Aspen 23"
```

### 列出开支
```bash
# Recent expenses in default group
splitwise expenses list --limit 10

# Date-filtered
splitwise expenses list --after 2026-03-01 --before 2026-03-31

# Different group
splitwise expenses list --group "Rome" --limit 5
```

### 创建开支
```bash
# Even split, you (Barron) paid — most common case
splitwise expenses create "Xfinity Internet - March" 51.30

# Nina paid
splitwise expenses create "Groceries" 87.50 --paid-by "Nina"

# Different group
splitwise expenses create "Dinner" 120.00 --group "Rome"

# Different currency
splitwise expenses create "Dinner in Lisbon" 45.00 --group "Rome" --currency EUR
```

### 其他命令
```bash
splitwise me                          # Current user info
splitwise groups                      # List all groups
splitwise group "Dolores"             # Group details + member balances
splitwise friends                     # List friends
splitwise settle "Nina"               # Record a settlement
splitwise expenses delete 12345       # Delete an expense by ID
```

## 输出格式

所有命令都支持以下选项：
- `--json` — 以原始 JSON 格式输出（适用于脚本编写或管道传输）
- `--quiet` — 仅输出开支的 ID 和金额
- `--no-color` — 禁用颜色显示（同时会忽略 `NO_COLOR` 环境变量）

## 常见任务的模式

### 记录周期性共享账单
在描述中包含月份以避免混淆：
```bash
splitwise expenses create "Xfinity Internet - March 2026" 51.30
```

### 创建账单前进行验证（避免重复）
```bash
splitwise expenses list --after 2026-03-01 --limit 50 --json
```
在创建账单前，请先在输出结果中查找是否存在相同的描述。

### 批量记录多笔开支
可以依次执行多个 `splitwise expenses create` 命令。无需特殊语法。

## 错误处理

- **“未登录”** → 运行 `splitwise auth`（需要通过浏览器完成 OAuth 验证）
- **“找不到对应的组”** → 使用 `splitwise groups` 命令验证组名
- **“找不到对应的朋友”** → 使用 `splitwise friends` 命令验证朋友名称
- **网络错误** → 重试一次，然后向用户报告错误

## 重要细节

- 组名/朋友名支持不区分大小写的部分匹配
- 默认组（Dolores）意味着对于 Barron 和 Nina 的开支，`--group` 参数是可选的
- 开支金额默认为美元（可通过 `splitwise config set default_currency` 配置更改）
- 默认情况下，开支会在所有组成员之间平均分配（`--split even` 参数）
- `--paid-by` 参数默认指向已登录的用户（Barron）
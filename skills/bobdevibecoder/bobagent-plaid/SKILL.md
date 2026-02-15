---
name: plaid
description: `plaid-cli` 是一个用于与 Plaid 金融平台交互的命令行工具（CLI）。它支持链接来自不同机构的账户，按日期范围查询余额和交易记录，以及列出账户和余额信息。
metadata: {"clawdis":{"emoji":"💳","requires":{"bins":["plaid-cli"]},"install":[{"id":"go","kind":"go","module":"github.com/jverdi/plaid-cli@0.0.2","bins":["plaid-cli"],"label":"Install plaid-cli (go)"}]}}
---

# Plaid

使用 `plaid-cli` 来关联金融机构、查询账户余额以及执行交易操作。请勿打印或记录任何敏感信息（如客户端 ID、访问令牌等）。

**安装：**
```bash
go install github.com/jverdi/plaid-cli@0.0.2
```

**配置：**
- 设置环境变量 `PLAID_CLIENT_ID`、`PLAID_SECRET` 和 `PLAID_ENVIRONMENT`（可选值：sandbox 或 production）。
- 可选参数：`PLAID LANGUAGE`（en, fr, es, nl）和 `PLAID_COUNTRIES`（US, CA, GB, IE, ES, FR, NL）。
- 可选配置文件：`~/.plaid-cli/config.toml`。

**数据存储：**
数据文件存储在 `~/.plaid-cli` 目录中，其中包含访问令牌和账户别名。

**操作说明：**
- **关联金融机构/设置别名：**
  ```bash
  plaid-cli link
  ```
  （该命令会在浏览器中打开相关机构的页面，并允许设置别名。）

- **重新关联机构：**
  ```bash
  plaid-cli link <机构ID或别名>
  ```

- **创建账户别名：**
  ```bash
  plaid-cli alias <机构ID> <别名>
  ```
  ```bash
  plaid-cli aliases
  ```
  （可查看所有已创建的账户别名。）

- **查询账户信息及余额：**
  ```bash
  plaid-cli accounts <机构ID或别名>
  ```

- **搜索交易记录：**
  ```bash
  plaid-cli transactions <机构ID或别名> --from 2024-01-01 --to 2024-01-31 --output-format json
  ```
  （将查询结果以 JSON 格式输出。）

  可通过以下命令进一步过滤交易记录：
  ```bash
  jq -r '.[] | select(.name | test("grocery"; "i")) | [.date, .name, .amount] | @tsv'
  ```
  （例如：仅显示与“grocery”相关的交易记录。）

- **使用账户 ID 进一步过滤结果：**
  ```bash
  plaid-cli transactions <机构ID或别名> --from 2024-01-01 --to 2024-01-31 --account-id <账户ID>
  ```

- **输出格式：**
  可选择 `json` 或 `csv`。

- **监控交易活动：**
  可定期检查交易记录以检测新发生的交易：
  ```bash
  # 使用 cron 任务自动执行以下命令
  ```

**注意事项：**
- 除非特别需要，否则请避免使用 `plaid-cli tokens` 命令，因为该命令会输出访问令牌。
- 当出现 `ITEM_LOGIN_REQUIRED` 错误时，系统会自动尝试重新关联金融机构。

**示例请求：**
- “搜索上个月与 Starbucks 相关的交易记录。”
- “显示我在 Chase 银行的账户余额。”
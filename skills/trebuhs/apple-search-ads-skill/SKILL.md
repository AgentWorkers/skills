---
name: Apple-Search-Ads
description: 通过 `asa-cli` 工具来管理 Apple Search Ads 的广告活动、广告组、关键词以及相关报告。当用户咨询 Apple Search Ads 的管理、广告活动操作、关键词出价、ASA 报告或广告表现时，可以使用此工具。
---
# Apple Search Ads 命令行工具（Apple Search Ads CLI）

使用 `asa-cli` 与 Apple Search Ads 营销活动管理 API v5 进行交互。在需要以编程方式解析结果时，务必使用 `-o json` 选项。

## 组织（Organizations）

运行 `asa-cli whoami` 可以列出可用的组织。对于多组织账户，除了 `whoami` 之外，每个命令都需要传递 `--org-id` 参数。单组织账户会自动检测所属的组织。

## 命令（Commands）

### 认证与配置（Auth & Config）
```bash
asa-cli whoami                          # List all orgs (no --org-id needed)
asa-cli configure --client-id "..." --team-id "..." --key-id "..." --private-key-path "..."
asa-cli configure                       # Interactive mode
```

### 营销活动（Campaigns）
```bash
asa-cli campaigns list [--org-id <orgid>] [--limit N] [--offset N]
asa-cli campaigns get <id> [--org-id <orgid>]
asa-cli campaigns find [--org-id <orgid>] [--filter "status=ENABLED"] [--sort "name:asc"] [--limit N] [--all]
asa-cli campaigns create [--org-id <orgid>] --name "..." --budget 1000 --daily-budget 50 --countries US,GB --app-id 123456
asa-cli campaigns update <id> [--org-id <orgid>] [--name ...] [--budget ...] [--daily-budget ...] [--status ENABLED|PAUSED]
asa-cli campaigns delete <id> [--org-id <orgid>]
```

### 广告组（Ad Groups）（需要 `--campaign-id` 参数）
```bash
asa-cli adgroups list --campaign-id <id> [--org-id <orgid>]
asa-cli adgroups get <id> --campaign-id <id> [--org-id <orgid>]
asa-cli adgroups find --campaign-id <id> [--org-id <orgid>] [--filter "status=ENABLED"]
asa-cli adgroups create --campaign-id <id> [--org-id <orgid>] --name "..." --default-bid 1.50 --start-time "2026-01-01T00:00:00.000" [--cpa-goal 5.00] [--auto-keywords true|false]
asa-cli adgroups update <id> --campaign-id <id> [--org-id <orgid>] [--name ...] [--default-bid ...] [--status ...]
asa-cli adgroups delete <id> --campaign-id <id> [--org-id <orgid>]
```

### 关键词（Keywords）（需要 `--campaign-id` 和 `--adgroup-id` 参数）
```bash
asa-cli keywords list --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli keywords get <kwid> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli keywords find --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] [--filter "text~brand"]
asa-cli keywords create --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --text "keyword" [--text "another"] --match-type BROAD|EXACT [--bid 1.50]
asa-cli keywords update --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --id <kwid> [--status ACTIVE|PAUSED] [--bid 2.00]
asa-cli keywords delete <kwid,kwid2> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
```

### 否定关键词（Negative Keywords）
```bash
# Campaign-level
asa-cli negative-keywords campaign-list --campaign-id <id> [--org-id <orgid>]
asa-cli negative-keywords campaign-find --campaign-id <id> [--org-id <orgid>] [--filter "text~free"]
asa-cli negative-keywords campaign-create --campaign-id <id> [--org-id <orgid>] --text "term" [--text "another"] --match-type EXACT|BROAD
asa-cli negative-keywords campaign-delete <kwid,...> --campaign-id <id> [--org-id <orgid>]

# Ad group-level
asa-cli negative-keywords adgroup-list --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
asa-cli negative-keywords adgroup-find --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] [--filter "text~competitor"]
asa-cli negative-keywords adgroup-create --campaign-id <id> --adgroup-id <id> [--org-id <orgid>] --text "term" [--text "another"] --match-type EXACT|BROAD
asa-cli negative-keywords adgroup-delete <kwid,...> --campaign-id <id> --adgroup-id <id> [--org-id <orgid>]
```

### 报告（Reports）
```bash
asa-cli reports campaigns [--org-id <orgid>] --start-date 2024-01-01 --end-date 2024-01-31 [--granularity DAILY|WEEKLY|MONTHLY] [--group-by countryOrRegion,deviceClass]
asa-cli reports adgroups --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
asa-cli reports keywords --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
asa-cli reports search-terms --campaign-id <id> [--org-id <orgid>] --start-date ... --end-date ...
```

### 实用工具（Utilities）
```bash
asa-cli apps search --query "MyApp" [--owned]
asa-cli geo search --query "US" [--entity ...] [--country-code ...]
```

## 过滤语法（Filter Syntax）
`--filter` 的操作符包括：`=`（等于），`~`（包含），`@`（在...中），`>`（大于），`<`（小于），`>=`（大于或等于），`<=`（小于或等于），`!~`（不包含）。
示例：`--filter "status=ENABLED" --filter "name~Brand"`

## 全局标志（Global Flags）
| 标志 | 简写 | 描述 |
|------|-------|-------------|
| `--output` | `-o` | 输出格式（`json` 或 `table`，默认为 `table`） |
| `--org-id` | | 组织 ID（多组织账户必需，单组织账户自动检测） |
| `--profile` | `-p` | 指定配置文件 |
| `--verbose` | `-v` | 显示 HTTP 请求/响应的详细信息 |
| `--no-color` | | 禁用彩色输出 |

## 配置（Config）
- 配置信息存储在 `~/.asa-cli/config.yaml` 文件中，令牌缓存存储在 `~/.asa-cli/token_cache.json` 文件中。
- 配置文件的创建方式：`asa-cli configure -p production --client-id "..." ...`，之后使用 `asa-cli campaigns list -p production` 查看营销活动列表。
- 环境变量：`ASA_CLIENT_ID`、`ASA_team_ID`、`ASA_KEY_ID`、`ASA_ORG_ID`、`ASA_PRIVATE_KEY_PATH`

## 使用指南（Guidelines）
- 在提取特定字段时，务必使用 `-o json` 并通过 `jq` 进行处理。
- 对于多组织账户，必须包含 `--org-id` 参数（例如：`asa-cli whoami -o json` 以获取组织 ID）。
- 在操作子资源之前，先获取营销活动/广告组的 ID。
- 在 `find` 命令中使用 `--all` 选项以实现结果集的分页显示。
- 报告功能需要 `--start-date` 和 `--end-date` 参数，格式为 YYYY-MM-DD。
- 货币单位会自动根据所属组织进行检测，无需手动指定。
- 创建广告组时需要提供 `--start-time` 参数（ISO 8601 格式，例如：`$(date -u +%Y-%m-%dT%H:%M:%S.000)`）。
- `--auto-keywords` 的默认值为 `false`（表示不进行关键词匹配）。仅在创建广告组时显式启用该选项。
- 在搜索已暂停或已删除的营销活动时，`keywords find` 命令可能会返回 404 错误，此时可以使用 `keywords list` 作为替代方法。
- 默认的分页限制为 20 条记录。如果需要显示更多结果（例如查询否定关键词），可以使用 `--limit 50`（或更高值）。
- 报告中的指标使用 v5 标准的字段名称：`totalInstalls`、`tapInstalls`、`viewInstalls`、`totalNewDownloads`、`totalRedownloads`、`totalInstallRate`、`tapInstallRate`、`totalAvgCPI`、`tapInstallCPI`、`avgCPM`（而非旧的 v4 标准）。
- 在营销活动报告中使用 `--grand-totals` 选项可获取所有营销活动的汇总数据。
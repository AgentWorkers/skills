---
name: cloudflare
description: 通过 Cloudflare API 管理 Cloudflare 域名、DNS 记录、SSL 设置、区域配置、防火墙规则、隧道以及分析数据。当用户需要设置域名、添加/编辑/删除 DNS 记录、配置 SSL、检查区域设置、管理 Cloudflare 隧道、查看分析数据或执行任何 Cloudflare 账户管理任务时，可以使用该 API。
metadata: {"openclaw":{"primaryEnv":"CLOUDFLARE_API_TOKEN","requires":{"env":["CLOUDFLARE_API_TOKEN"],"bins":["curl","jq","openssl"]}}}
---
# Cloudflare

您可以通过自带的 `scripts/cf.sh` Bash 脚本来管理 Cloudflare 的区域（zones）、DNS、SSL 设置以及隧道（tunnels）等。

## 先决条件

- 系统上必须安装 `curl`、`jq` 和 `openssl` 工具。
- 需要设置 `CLOUDFLARE_API_TOKEN` 环境变量。
- （可选）为隧道操作设置 `CLOUDFLARE_ACCOUNT_ID`。

## CLI：`scripts/cf.sh`

所有操作都通过自带的 `scripts/cf.sh` Bash 脚本完成（该脚本包含在本技能文档中），无需额外下载任何外部工具。

```bash
# Run from skill directory
./scripts/cf.sh <command> [args...]
# Or reference by absolute path
/path/to/skills/cloudflare/scripts/cf.sh <command> [args...]
```

### 命令

| 命令 | 参数 | 描述 |
|---------|------|-------------|
| `help` | | 显示所有可用命令 |
| `verify` | | 验证 API 令牌的有效性 |
| `zones` | `[domain]` | 列出所有区域（可按域名筛选） |
| `zone-get` | `<zone_id>` | 获取区域详情 |
| `zone-id` | `<domain>` | 从域名中获取区域 ID |
| `dns-list` | `<zone_id> [type] [name]` | 列出 DNS 记录 |
| `dns-create` | `<zone_id> <type> <name> <content> [proxied] [ttl]` | 创建 DNS 记录 |
| `dns-update` | `<zone_id> <record_id> <type> <name> <content> [proxied] [ttl]` | 更新 DNS 记录 |
| `dns-delete` | `<zone_id> <record_id>` | 删除 DNS 记录 |
| `dns-export` | `<zone_id>` | 将所有记录导出为 JSON 格式 |
| `dns-import` | `<zone_id> <file.json>` | 从 JSON 文件导入 DNS 记录 |
| `settings-list` | `<zone_id>` | 列出所有区域设置 |
| `setting-get` | `<zone_id> <setting>` | 获取特定设置 |
| `setting-set` | `<zone_id> <setting> <value>` | 更新设置 |
| `ssl-get` | `<zone_id>` | 获取当前的 SSL 模式 |
| `ssl-set` | `<zone_id> <mode>` | 设置 SSL 模式（off/flexible/full/strict） |
| `cache-purge` | `<zone_id> [url1 url2 ...]` | 清除指定 URL 或所有内容 |
| `pagerules-list` | `<zone_id>` | 列出页面规则 |
| `firewall-list` | `<zone_id>` | 列出防火墙规则 |
| `tunnels-list` | | 列出 Cloudflare 隧道（需要 `ACCOUNT_ID`） |
| `tunnel-get` | `<tunnel_id>` | 获取隧道详情 |
| `tunnel-create` | `<name>` | 创建隧道（需要 `ACCOUNT_ID`） |
| `tunnel-delete` | `<tunnel_id>` | 删除隧道（需要 `ACCOUNT_ID`） |
| `analytics` | `<zone_id> [since_minutes]` | 区域分析数据（默认：过去 24 小时） |

### `proxied` 标志

- `true`：使用 Cloudflare 的代理服务（包括 CDN、WAF、DDoS 防护） |
- `false`：仅使用 DNS 服务（适用于 MX 邮件服务器或非 HTTP 服务） |

### TTL（Time To Live）

- `1`：自动管理（由 Cloudflare 决定）
- 对于仅使用 DNS 的记录，可以手动设置 TTL 值（例如 `3600` 秒）。

## 典型工作流程

### 将域名指向服务器
```bash
# Find zone ID
cf zones example.com
# Create A record (proxied)
cf dns-create <zone_id> A example.com 1.2.3.4 true
# Create www CNAME
cf dns-create <zone_id> CNAME www.example.com example.com true
```

### 设置电子邮件（MX + SPF）
```bash
cf dns-create <zone_id> MX example.com "mx.provider.com" false 1
cf dns-create <zone_id> TXT example.com "v=spf1 include:provider.com ~all" false
```

### 启用严格 SSL 安全
```bash
cf ssl-set <zone_id> strict
```

## 安全注意事项

**在执行以下操作前，请务必征得用户同意：**
- 删除 DNS 记录（`dns-delete`）
- 更改 SSL 模式 |
- 修改防火墙规则 |
- 任何可能对系统造成影响的操作

**可以自由执行的操作：**
- 查看/读取区域信息、DNS 记录、设置以及分析数据 |
- 验证 API 令牌的有效性

## 参考资料

有关 DNS 记录类型、SSL 模式和 API 详细信息的说明，请参阅 `references/api-guide.md`。
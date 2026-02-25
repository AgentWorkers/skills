---
name: domain-check
description: 通过 Vercel 检查域名是否可用，并使用 Vercel CLI 购买/管理域名。
---
# 域名检查与购买（Vercel）

通过 Vercel 可以检查域名的可用性、价格并完成购买。

## 快速参考

```bash
# Check availability + pricing for a name across TLDs
domain-check myproject

# Check specific TLDs
domain-check myproject com,io,dev,app,ai

# Buy a domain (interactive — needs pty:true)
npx vercel domains buy mydomain.com

# List your owned domains
npx vercel domains list

# Inspect a domain you own
npx vercel domains inspect mydomain.com

# Add domain to a Vercel project
npx vercel domains add mydomain.com my-project

# Transfer a domain into Vercel
npx vercel domains transfer-in mydomain.com
```

## 工作原理

### 可用性检查 (`domain-check`)

使用 Vercel 注册商 API (`/v1/registrar/domains/{domain}/price`)：
- `purchasePrice: null` → 域名已被他人购买
- `purchasePrice: <number>` → 域名以该价格可供购买

```
$ domain-check myproject
Checking: myproject
-----------------------------------------------------------
DOMAIN                    STATUS         BUY PRICE    RENEWAL
-----------------------------------------------------------
myproject.com             ❌ Taken       -            $11.25
myproject.io              ✅ Available   $46.00       $46.00
myproject.dev             ✅ Available   $13.00       $13.00
-----------------------------------------------------------
Prices from Vercel Registrar
```

### 购买 (`npx vercel domains buy`)

这是一个交互式命令；从执行脚本时需要设置 `pty: true` 以启用交互式确认提示。

```bash
# Example exec call
exec(command: "npx vercel domains buy myproject.dev", pty: true, timeout: 30)
```

命令行工具 (CLI) 会显示价格并在收费前请求用户确认。

### 直接使用 API (适用于脚本)

```bash
VERCEL_TOKEN=$(jq -r '.token' ~/.local/share/com.vercel.cli/auth.json)
TEAM=$(jq -r '.currentTeam // empty' ~/.local/share/com.vercel.cli/config.json)
TEAM_PARAM="${TEAM:+?teamId=$TEAM}"

# Check price/availability
curl -s "https://api.vercel.com/v1/registrar/domains/example.com/price${TEAM_PARAM}" \
  -H "Authorization: Bearer $VERCEL_TOKEN"
# Returns: { "years": 1, "purchasePrice": 11.25, "renewalPrice": 11.25, "transferPrice": 11.25 }
# purchasePrice: null = taken, number = available

# Buy via API
curl -s -X POST "https://api.vercel.com/v1/registrar/domains${TEAM_PARAM}" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}'
```

## Vercel CLI 的域名相关命令

| 命令 | 描述 |
|---------|-------------|
| `npx vercel domains list` | 显示所有域名 |
| `npx vercel domains inspect <domain>` | 查看域名信息（仅限已拥有的域名） |
| `npx vercel domains buy <domain>` | 购买域名（交互式操作） |
| `npx vercel domains add <domain> <project>` | 将域名添加到 Vercel 项目中 |
| `npx vercel domains move <domain> <dest>` | 将域名转移给其他团队 |
| `npx vercel domains transfer-in <domain>` | 将域名导入到 Vercel 项目中 |
| `npx vercel domains remove <domain>` | 从项目中删除域名 |

## Vercel 的常见顶级域名 (TLD) 价格

| TLD | 每年价格 |
|-----|-----------|
| .com | $11.25 |
| .dev | $13 |
| .app | $15 |
| .co | $27 |
| .io | $46 |
| .ai | $140 |
| .org | $9.99 |
| .net | $13.50 |
| .xyz | $13 |

## 身份验证

需要使用 Vercel CLI 进行身份验证 (`npx vercel login`)。令牌从 `~/.local/share/com.vercel.cli/auth.json` 文件中读取。

团队 ID 会自动从 Vercel CLI 配置中检测；也可以通过设置 `VERCEL_TEAM_ID` 环境变量来手动指定。如果两者均未设置，则会使用个人账户。

## 注意事项

- Vercel 的注册商 API 已取代了旧的 v4 版本的 `domains/price` 端点（该接口将于 2025 年 11 月停止使用）。
- `domains inspect` 命令仅适用于用户已拥有的域名；如需检查域名是否可用，请使用价格查询 API。
- `.ai` 域名的年费用较高（$140）。
- 通过 CLI 购买域名时，请务必设置 `pty: true` 以启用交互式确认功能。
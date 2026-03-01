---
name: cardpointers
description: "通过 CardPointers CLI 查询 CardPointers 的卡片推荐、钱包卡片信息以及优惠活动。适用于用户询问购买时应使用哪种信用卡、查看或筛选卡片列表及优惠信息、检查即将到期的优惠活动、跨关联账户比较信用卡信息，或任何与信用卡奖励优化相关的问题。该功能需订阅 CardPointers+（Pro）版本才能使用。"
homepage: https://cardpointers.com/cli/
metadata: {"clawdbot":{"emoji":"💳","requires":{"bins":["cardpointers","jq"]},"install":[{"id":"brew","kind":"brew","formula":"cardpointers/tap/cardpointers","bins":["cardpointers"],"label":"Install cardpointers (brew)"},{"id":"jq","kind":"brew","formula":"jq","bins":["jq"],"label":"Install jq (brew)"}]}}
---
# CardPointers CLI

您可以通过终端查询 CardPointers 钱包中的信息，包括卡片、优惠活动以及推荐内容。

## 设置

- **配置文件：** `~/.cardpointers/config`（JWT 令牌，在登录时自动生成）
- **所需工具：** `curl`, `jq`, `bash`
- **身份验证：** 运行 `cardpointers login` 进行身份验证（支持电子邮件/密码或浏览器内置的 Apple/Google/Passkey 认证）

## 命令

### recommend — 为购物推荐最合适的卡片

```bash
cardpointers recommend groceries
cardpointers recommend "gas stations"
cardpointers recommend --merchant amazon
cardpointers recommend -m "whole foods" --amount 150
cardpointers recommend gas -p all        # best gas card across all profiles
```

### cards — 列出钱包中的卡片

```bash
cardpointers cards                       # approved cards (default)
cardpointers cards --status all          # all statuses
cardpointers cards --bank chase          # filter by bank
cardpointers cards -b amex -s all -l 5  # combine filters + limit
```

### offers — 列出并筛选优惠活动

```bash
cardpointers offers                          # active offers
cardpointers offers -s redeemed              # redeemed offers
cardpointers offers --expiring               # expiring within 7 days
cardpointers offers -e 14                    # expiring within 14 days
cardpointers offers --bank amex              # filter by bank
cardpointers offers --card "gold"            # filter by card name
cardpointers offers --category dining        # filter by category
cardpointers offers --type personal          # personal offers only
cardpointers offers --favorite               # favorited offers only
cardpointers offers --sort value --limit 10  # top 10 by value
```

### search — 按关键词搜索优惠活动

```bash
cardpointers search "whole foods"
cardpointers search "streaming" --favorite
cardpointers search "gas" --limit 5
```

### profiles — 列出关联的个人信息

```bash
cardpointers profiles
```

### Utility — 其他实用命令

```bash
cardpointers status    # account info + connection test
cardpointers ping      # test MCP connection
cardpointers tools     # list available MCP tools
cardpointers login     # authenticate
cardpointers logout    # clear saved token
cardpointers --version # print version
```

## 全局选项

所有数据查询命令都支持以下选项：

| 选项 | 描述 |
|------|-------------|
| `--profile, -p` | 按个人信息查询：编号（`-p 2`）、名称（`-p caroline`）或 `all`/`any` |
| `--limit, -l` | 限制结果数量 |
| `--json, -j` | 以原始 JSON 格式输出（适用于脚本编写或 AI 代理）

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `CARDPOINTERS_API` | 替换 API 基本地址（默认：`https://mcp.cardpointers.com`） |
| `CARDPOINTERS_DEBUG` | 设置为 `1` 以获取详细输出 |
| `NO_COLOR` | 禁用 ANSI 颜色显示 |

## 参考说明

- **卡片状态：** 已批准、申请中、被拒绝、已关闭、全部 |
- **优惠状态：** 活跃中、已暂停、已兑换、即将过期、全部 |
- **优惠银行筛选（枚举值）：** amex, chase, citi, boa, usbank, wellsfargo |
- **卡片银行筛选：** 自由输入（部分匹配） |
- **优惠排序选项：** 即将过期、优惠金额、卡片类型 |
- **卡片信息包含：** `approval_date`（YYYY-MM-DD）

## 常见用法

- “我在 Costco 应该使用哪张卡片？” → `recommend -m costco`
- “显示我的 Amex 卡片” → `cards -b amex`
- “本周到期的优惠有哪些？” → `offers -e 7`
- “有哪些 Whole Foods 的优惠？” → `search "whole foods"`
- “所有个人资料中推荐的餐饮卡？” → `recommend dining -p all`
- “按优惠金额排序的前 5 个优惠” → `offers --sort value -l 5`
- “以 JSON 格式显示已兑换的优惠” → `offers -s redeemed -j`
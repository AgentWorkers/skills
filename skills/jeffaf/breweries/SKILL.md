---
name: breweries
version: 1.0.0
description: "这是一个用于AI代理帮助人类寻找啤酒厂的命令行工具（CLI），它依赖于Open Brewery DB数据库，且无需任何身份验证。"
homepage: https://www.openbrewerydb.org
metadata:
  openclaw:
    emoji: "🍺"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["breweries", "beer", "search", "openbrewerydb", "cli"]
---

# 酿酒厂查询工具

这是一个为AI代理设计的命令行工具，用于帮助用户查找附近的酿酒厂。例如：“波特兰有哪些酿酒厂？”——现在你的AI代理可以回答这个问题了。

该工具使用Open Brewery数据库（Open Brewery DB）进行数据查询，无需注册账户或API密钥。

## 使用方法

```
"Find breweries named Sierra Nevada"
"What breweries are in San Diego?"
"Show me breweries in Oregon"
"Find me a random brewery"
"What brewpubs are there?"
```

## 命令列表

| 功能 | 命令                |
|--------|-------------------|
| 按名称搜索 | `breweries search "名称"`     |
| 按城市搜索 | `breweries city "城市名称"`     |
| 按州搜索 | `breweries state "州名称"`     |
| 按类型搜索 | `breweries type <类型>`     |
| 随机推荐 | `breweries random [数量]`     |

### 酿酒厂类型
- `micro`  — 大多数精酿啤酒厂
- `nano`  — 非常小的酿酒厂
- `regional` — 地区性精酿啤酒厂
- `brewpub` — 同时提供餐饮服务的酿酒厂
- `large`  — 大型全国性酿酒厂
- `planning` — 正在规划中的酿酒厂
- `bar`  — 在店内自酿啤酒的酒吧
- `contract` — 合作生产啤酒的酿酒厂
- `proprietor` — 酿酒厂所有者频繁更换的酿酒厂
- `closed` — 已关闭的酿酒厂

### 使用示例

```bash
breweries search "stone brewing"    # Find breweries by name
breweries city "portland"           # Find breweries in Portland
breweries state oregon              # Find breweries in Oregon
breweries type brewpub              # Find all brewpubs
breweries random 3                  # Get 3 random breweries
```

## 查询结果展示

```
🍺 Sierra Nevada Brewing Co. — Chico, California, Regional Brewery
   https://sierranevada.com
```

## 注意事项

- 该工具基于Open Brewery DB API v1（api.openbrewerydb.org）进行数据查询
- 无需身份验证
- 无明确的请求速率限制
- 每次查询最多返回10条结果
- 州名可以是全称或缩写形式

---

## AI代理实现说明

**脚本位置：** `{skill_folder}/breweries`（封装脚本） → `scripts/breweries`

**当用户询问酿酒厂相关信息时：**
1. 使用 `./breweries search "名称"` 按名称搜索酿酒厂
2. 使用 `./breweries city "城市名称"` 按城市搜索酿酒厂
3. 使用 `./breweries state "州名称"` 按州搜索酿酒厂
4. 使用 `./breweries type <类型>` 按特定类型搜索酿酒厂
5. 使用 `./breweries random` 随机推荐酿酒厂

**常见使用场景：**
- “在[城市]找一家酿酒厂” → `breweries city "[城市名称]"
- “[州]有哪些酿酒厂？” → `breweries state "[州名称]"
- “搜索[名称]酿酒厂” → `breweries search "[名称]"
- “随机推荐一家酿酒厂” → `breweries random`
- “在[城市]哪里可以喝到精酿啤酒？” → `breweries city "[城市名称]"` 或 `breweries type micro`

**不适用场景：**
- 不适用于不生产啤酒的酒吧、酒类商店或葡萄酒/烈酒销售场所
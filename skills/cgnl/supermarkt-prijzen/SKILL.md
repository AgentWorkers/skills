---
name: supermarkt-prijzen
description: 阿尔伯特·海因（Albert Heijn）的奖金制度、产品搜索功能、多门店价格对比（涵盖12家超市）、按食材搜索食谱的功能，以及配备视觉人工智能的冰箱扫描仪。
homepage: https://www.ah.nl
metadata: {"openclaw":{"emoji":"🛒","requires":{"bins":["python3","curl"]}}}
---

# Albert Heijn API 功能

通过 GraphQL（网页端）和 OAuth（移动端）获取 Albert Heijn 的优惠券、产品信息及食谱。

## 主要功能

✅ **获取优惠券**（GraphQL，200 多项优惠券，**无需登录**）  
✅ **搜索产品**（REST API，20,000 多种产品，**无需登录**）  
✅ **搜索食谱**（GraphQL，**无需登录**）  
✅ **多超市价格比较**（Checkjebon.nl - 12 家超市，107,000 种产品）  
✅ **OAuth 令牌流程**（移动 API 访问 - 仅用于个人数据）  
✅ **冰箱扫描功能**（通过视觉 AI 扫描冰箱内容 → 生成购物清单）

## 快速入门

### 1. 优惠券与产品（无需登录！）

**获取优惠券（200 多项）：**
```bash
./ah-api.py bonuses --filter WEB_BONUS_PAGE --pretty
```

**搜索产品（20,000 多种产品）：**
```bash
./ah-api.py search --query "melk" --limit 10 --pretty
```

**搜索食谱：**
```bash
./ah-recipes.py search --query "pasta carbonara" --pretty
```

**通过 URL 获取食谱：**
```bash
./ah-recipes.py url --url "https://www.ah.nl/allerhande/recept/R-R1187649/zoete-tortillachips" --pretty
```

✨ **所有功能均无需使用 cookies！** 使用 `curl-cffi` 并结合 Chrome 的指纹识别技术。

### 2. OAuth 令牌流程（移动 API）

**获取初始令牌：**
1. 打开 Appie 应用  
2. 点击个人资料 → 设置 → 向下滚动 → “开发者”（隐藏选项）  
3. 点击 “OAuth Code” 并复制代码  
4. 在 30 秒内执行以下操作：  
```bash
curl -X POST 'https://api.ah.nl/mobile-auth/v1/auth/token' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: Appie/8.22.3' \
  -d '{"clientId":"appie","code":"PASTE_CODE_HERE"}'
```

**响应：**
```json
{
  "access_token": "USERID_TOKEN",
  "refresh_token": "REFRESH_TOKEN",
  "expires_in": 604798
}
```

**将令牌保存到 `~/.ah_tokens.json` 文件中：**
```bash
echo '{"access_token":"...","refresh_token":"...","expires_in":604798}' > ~/.ah_tokens.json
```

**令牌更新（7 天后）：**
```bash
./refresh-token.py
```

### 3. 多超市价格比较

**可在 12 家超市之间进行价格比较：**
```bash
./checkjebon-search.py --compare "melk" --top 10
```

**支持的超市：** AH、Jumbo、Lidl、Plus、Dekamarkt、Spar、Dirk、Hoogvliet、Poiets、Aldi、Vomar、Ekoplaza

## 工具

| 工具 | 用途 |
|------|---------|
| `ah-api.py` | 基于 cookies 的优惠券和产品信息查询（GraphQL + REST） |
| `ah-recipes.py` | **新功能！** 通过文本或食材搜索食谱 |
| `fridge-scan.sh` | **新功能！** 通过摄像头扫描冰箱内容生成购物清单 |
| `smart-cook.sh` | **新功能！** 完整的工作流程：扫描 → 搜索食谱 → 购物 |
| `get-bonuses.py` | 旧版优惠券查询工具（仅支持 GraphQL） |
| `checkjebon-search.py | 多超市价格比较工具 |
| `refresh-token.py | 更新 OAuth 令牌 |
| `setup-cookies.sh | 设置 cookies 的辅助工具 |

## 技术细节

### 认证（无需登录！）

**旧版本：** 需要浏览器提供的会话 cookies  
**当前版本：** 使用 `curl-cffi` 并设置 `impersonate='chrome120'`  

**工作原理：**  
- `curl-cffi` 会发送真实的 Chrome TLS 指纹信息  
- Albert Heijn 的机器人检测系统会将其视为普通浏览器  
- 无需 cookies，无需登录，无需任何设置！🎉  

**仅适用于：**  
- OAuth 移动 API（查询食谱、个人数据） - 需要登录应用  

### GraphQL 优惠券 API

**端点：** `https://www.ah.nl/gql`

**查询语句：**
```graphql
query FetchBonusPromotions($periodStart: String, $periodEnd: String) {
  bonusPromotions(
    filterSet: WEB_BONUS_PAGE
    input: {
      periodStart: "2026-02-01"
      periodEnd: "2026-02-08"
      filterUnavailableProducts: false
      forcePromotionVisibility: true
    }
  ) {
    id title promotionType
    price { now { amount } }
    product { title category }
  }
}
```

**可用的过滤条件：**  
- `WEB_BONUS_PAGE` - 所有优惠券（326 项）  
- `APP_PERSONAL` - 个人专属优惠  
- `APP_BONUS_BOX` - 优惠券礼盒  
- `COUPON` - 优惠券  
- `FREE_DELIVERY` - 免费配送  
- `SPOTLIGHT` - 特色优惠  

### REST 产品搜索

**端点：** `https://www.ah.nl/zoeken/api/products/search`

**示例：**
```bash
curl 'https://www.ah.nl/zoeken/api/products/search?query=melk' \
  -H 'Cookie: SSOC=...; jsessionid_myah=...' \
  --user-agent 'Mozilla/5.0 (compatible; AH-Bot/1.0)'
```

**响应：**
```json
{
  "cards": [
    {
      "products": [
        {
          "id": 441199,
          "title": "Campina Halfvolle melk",
          "price": { "now": 1.99, "unitSize": "1,5 l" }
        }
      ]
    }
  ]
}
```

### OAuth 移动 API

**授权：** `https://login.ah.nl/secure/oauth/authorize`  
**令牌交换：** `https://api.ah.nl/mobile-auth/v1/auth/token`  
**令牌更新：** `https://api.ah.nl/mobile-auth/v1/auth/token/refresh`  

**令牌有效期：** 7 天（604,798 秒）  

**已知端点：**  
- `/mobile-services/v1/receipts` - 所有购物清单  
- `/mobile-services/v2/receipts/{id}` - 特定购物清单  
- `/mobile-services/product/search/v2` - 产品搜索  

**注意：** 部分移动端点可能会返回 500 错误（由于基础设施问题）。  

### 为什么使用 `curl-cffi`？

Albert Heijn 使用 **Cloudflare + Akamai** 的机器人检测机制。普通请求会收到 403 “访问被拒绝”的错误。  
`curl-cffi` 通过发送真实的 Chrome TLS 指纹信息来规避检测。  

## Checkjebon 多超市数据

**数据来源：** `https://raw.githubusercontent.com/supermarkt/checkjebon/main/data/supermarkets.json`  
**统计信息：**  
- 文件大小：10.3MB  
- 总产品数量：106,991 种  
- 每日更新  
- 提供 24 小时本地缓存  

**使用方法：**  
```bash
# Find cheapest
./checkjebon-search.py --compare "bier" --top 5

# Specific store
./checkjebon-search.py --query "campina" --store jumbo

# Show stats
./checkjebon-search.py --stats
```

## 新功能：食谱  

### 扫描冰箱 → 查找食谱 → 生成购物清单  

**1. 扫描冰箱内容：**  
```bash
./fridge-scan.sh
# Opens camera, captures fridge contents
# Output: /tmp/fridge-scan.jpg
```  
**2. 通过 OpenClaw 图像工具提取食材信息：**  
```bash
# Ask assistant:
# "Analyze /tmp/fridge-scan.jpg and list all food items as comma-separated"
# → melk, eieren, tomaten, kaas, broccoli
```  
**3. 查找相应的食谱：**  
```bash
./ah-recipes.py ingredients --ingredients "melk,eieren,kaas,broccoli" --pretty
```  
**4. 通过 ID 获取食谱详情：**  
```bash
./ah-recipes.py details --recipe-id 1187649 --pretty
```  
**或直接通过 URL 获取食谱：**  
```bash
./ah-recipes.py url --url "https://www.ah.nl/allerhande/recept/R-R1187649/zoete-tortillachips" --pretty
```  
**5. 完整的工作流程：**  
```bash
./smart-cook.sh
# Interactive: scan → analyze → find recipes → shopping list
```  

### 食谱 ID 的获取方法  

**获取食谱 ID 的方式：**  
1. **从搜索结果中获取：** 搜索结果仅返回食谱标题，需获取 ID 才能查看完整信息。  
2. **从 URL 中获取：** 食谱 URL 的格式为 `R-R{ID}`，例如：`https://www.ah.nl/allerhande/recept/R-R1187649/zoete-tortillachips`，其中 `R-R1187649` 即为食谱 ID。  
3. **直接查询：** 使用 `url` 功能可自动提取 ID 并获取详情。  

**工作流程：**  
```bash
# Step 1: Search for recipes (returns titles only)
./ah-recipes.py search --query "pasta carbonara" --pretty

# Step 2: If you have the recipe URL (e.g., from browser or website), extract ID
./ah-recipes.py url --url "https://www.ah.nl/allerhande/recept/R-R{ID}/{slug}" --pretty

# Note: Search results don't include recipe IDs (client-side rendered)
# To get full details, you need either:
#   - The direct recipe URL (contains R-R{ID})
#   - The recipe ID number
```  

### 食谱搜索示例  

**按文本搜索（返回 ID 和标题）：**  
```bash
./ah-recipes.py search --query "pasta carbonara" --size 10 --pretty
# Output: {"recipes": [{"id": 1200422, "title": "Klassieke spaghetti carbonara"}, ...], "total": 49, "hasMore": true}
```  
**按详细信息搜索（包含烹饪时间、评分、图片、份量等）：**  
```bash
./ah-recipes.py search --query "pasta carbonara" --size 5 --detailed --pretty
# Output: Full recipe summaries with time, ratings, images, servings
```  
**按食材搜索：**  
```bash
./ah-recipes.py ingredients --ingredients "tomaat,ui,knoflook" --size 5 --pretty
```  
**通过 URL 获取食谱：**  
```bash
./ah-recipes.py url --url "https://www.ah.nl/allerhande/recept/R-R1187649/zoete-tortillachips" --pretty
# Extracts recipe ID from URL (R-R1187649 → 1187649) and fetches full details
```  

## 示例  

**所有超市中最便宜的牛奶：**  
```bash
./checkjebon-search.py --compare "melk" --top 5
```  
**今日的 Albert Heijn 优惠券：**  
```bash
./ah-api.py bonuses --filter WEB_BONUS_PAGE --pretty | \
  jq '.bonuses[] | select(.title | contains("Campina"))'
```  
**搜索 Albert Heijn 的产品：**  
```bash
./ah-api.py search --query "bier" --limit 20 --pretty
```  

## 故障排除**

**“访问被拒绝”错误：**  
- 使用 `curl-cffi`（而非标准请求方式）  
- 检查 User-Agent 头部信息  
- 更新 cookies（运行 `./setup-cookies.sh`）  

**OAuth 令牌过期：**  
- 令牌仅有效 30 秒，请立即使用 `curl` 命令  
- 或使用 `refresh_token` 更新令牌  

**GraphQL 错误：**  
- 检查日期格式（YYYY-MM-DD）  
- 确保 `filterSet` 值正确（区分大小写）  
- 确保 cookies 是最新的  

## 相关文件：**  
```
ah-bonuses/
├── SKILL.md              # This file
├── README.md             # Quick start
├── ah-api.py             # Main CLI tool (bonuses + search)
├── get-bonuses.py        # Legacy bonus tool
├── checkjebon-search.py  # Multi-store search
├── refresh-token.py      # OAuth token refresh
├── setup-cookies.sh      # Cookie extractor
└── ~/.ah_cookies.json    # Session cookies (gitignored)
└── ~/.ah_tokens.json     # OAuth tokens (gitignored)
```  

## 致谢**

- **AlbertPWN**（userlandkernel） - 最初研究移动 API 的开发者  
- **TommasoAmici/ah-bonus-bot** - 开发用于产品搜索的 Rust 机器人  
- **jabbink** - 提供全面的 API 文档  
- **curl-cffi** - 用于获取 Chrome 指纹信息的库  

## 状态更新  

✅ **优惠券 API**（GraphQL） - **100% 免登录使用！**（200 多项优惠券）  
✅ **产品搜索**（REST） - **100% 免登录使用！**（20,000 多种产品）  
✅ **食谱搜索**（GraphQL） - **100% 免登录使用！**  
✅ **多超市价格比较**（Checkjebon） - **100% 可用**（107,000 种产品，12 家超市）  
✅ **OAuth 令牌流程** - 已启用（移动 API 使用）  
⚠️ **移动 API 端点** - 部分功能仍可能出现 500 错误  

## 更新日志  

**2026-02-02 - 重大更新：**  
- 🎉 **取消了对 cookies 的依赖！** 所有 API 现在均无需登录  
- ✅ 优惠券：200 多项优惠券，可匿名访问  
- ✅ 产品搜索：20,000 多种产品，可匿名访问  
- ✅ 食谱搜索：可匿名访问  
- 🔧 使用 `curl-cffi` 并设置 `impersonate='chrome120` 以规避机器人检测  
- 🗑️ `setup-cookies.sh` 已弃用（不再需要）  
- ⚠️ OAuth 仍可用于移动 API（查询食谱、个人数据）  

**2026-02-01：**  
- 新增按食材搜索食谱的功能  
- 新增冰箱扫描功能  
- 新增多超市价格比较功能（Checkjebon.nl）  

最后更新时间：2026-02-02
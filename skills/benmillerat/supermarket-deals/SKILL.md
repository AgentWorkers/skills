---
name: supermarket-deals
description: 使用 Marktguru 在德国超市的传单（Aldi、Lidl、REWE、EDEKA、Kaufland）中搜索产品优惠信息。搜索结果按每升价格（EUR/L）从低到高排序。无需 API 密钥。
---
# 超市优惠信息

通过 Marktguru API 搜索德国超市的促销 flyer（传单），结果会按照每升价格从低到高的顺序排列。

## 该技能的功能：
- 自动从 Marktguru 的主页获取 API 密钥（无需注册，密钥缓存有效期为 6 小时）
- 根据产品名称和邮政编码搜索当前的促销 flyer
- 支持在单次调用中输入多个搜索词（这些搜索词会被合并并去重）
- 可按商店进行筛选，并按每升价格（EUR/L）对结果进行排序
- 为每个优惠信息返回 Marktguru 的直接链接

## 设置

```bash
cd path/to/supermarket-deals
npm install
npm run build
```

（可选：设置您的默认参数）

## 使用方法

```bash
# Single search term
node dist/index.js search "Cola Zero" --zip 85540

# Multiple terms (merged + deduped, useful for product aliases)
node dist/index.js search "Cola Zero" "Coke Zero" --zip 85540

# Broad search — let your agent do the filtering
node dist/index.js search "Cola" --zip 85540

# Filter by specific stores
node dist/index.js search "Monster Energy" --zip 80331 --stores "Lidl,ALDI SÜD"

# JSON output for agent/cron use
node dist/index.js search "Cola" --zip 85540 --json

# Show config
node dist/index.js config
```

## 建议的代理使用模式：

使用一个宽泛的搜索词，让代理智能地进行筛选：

```
node dist/index.js search "Cola" --zip 85540 --json
```

然后指示代理执行以下操作：
- 包括那些描述中包含“versch. Sorten”（多种款式）的优惠信息（这些优惠信息会包含所有款式，包括零容量产品）
- 包括明确提到 Coca-Cola、Coke Zero 等产品的优惠信息
- 排除仅提到 Powerade、Fuze Tea、Sprite 等产品的优惠信息
- 按每升价格（EUR/L）对结果进行排序，并突出显示最划算的优惠信息

这种使用方式可以获取 Marktguru 列为“可乐类”但未具体列出所有款式的优惠信息。

## 输出列：
| 列名 | 说明 |
|--------|-------------|
| 描述 | 来自传单的产品描述 |
| 商店名称 | 零售商名称 |
| 容量 | 产品体积 × 数量（例如：`6×0.33l`、`1.5l`） |
| 价格 | 总价格 |
| 每升价格（EUR/L） | 每升的价格（根据计算得出或从 API 取得） |
| 有效期 | 优惠信息的有效期 |
| 链接 | Marktguru 优惠页面的直接链接 |

## 注意事项：
- 促销 flyer 每周一和周四更新一次
- Marktguru 会缓存搜索结果约 15 分钟
- 有些地区的门店可能不会向 Marktguru 提供 flyer，使用宽泛的搜索词可以获取更多信息
- API 密钥会定期更新，并在运行时重新获取（缓存有效期为 6 小时，文件路径为 `~/.supermarket-deals/keys.json`）
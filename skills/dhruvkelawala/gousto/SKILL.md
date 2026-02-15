---
name: gousto
description: 搜索并浏览超过9,000道Gousto食谱。通过官方API获取完整的食材列表和详细的烹饪步骤。
homepage: https://github.com/dhruvkelawala/gousto-agent-skill
metadata: {"openclaw":{"emoji":"🍳","requires":{"bins":["curl","jq"]}}}
---

# Gousto 食谱管理技能

您可以通过命令行搜索和浏览 Gousto 上的 9,000 多道食谱。

## 快速入门

```bash
# First time: build the cache (~3 min)
./scripts/update-cache.sh

# Search recipes
./scripts/search.sh chicken
./scripts/search.sh "beef curry"

# Get full recipe with ingredients & steps
./scripts/recipe.sh honey-soy-chicken-with-noodles
```

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `search.sh <查询>` | 按标题搜索食谱（使用本地缓存） |
| `recipe.sh <slug>` | 获取包含食材和烹饪步骤的完整食谱详情 |
| `update-cache.sh` | 从 Gousto API 更新本地缓存（约 3 分钟） |

## API 详情

**官方 Gousto API**（食谱列表）：
```
https://production-api.gousto.co.uk/cmsreadbroker/v1/recipes?limit=50&offset=0
```
- 返回元数据：标题、评分、准备时间、网址
- 使用 `offset` 参数进行分页（注意：不要使用 `skip` 参数，因为该参数存在问题！）
- 总共约 9,300 道食谱

**官方 Gousto API**（单条食谱）：
```
https://production-api.gousto.co.uk/cmsreadbroker/v1/recipe/{slug}
```
- 包含食材、烹饪步骤和营养信息的完整食谱
- 脚本会将步骤中的 HTML 格式转换为纯文本

## 缓存格式

`data/recipes.json` — 对象数组：
```json
{
  "title": "Chicken Tikka Masala",
  "slug": "chicken-tikka-masala",
  "rating": 4.8,
  "rating_count": 12543,
  "prep_time": 35,
  "uid": "blt123..."
}
```

## 注意事项

- 本地缓存文件被 Git 忽略（git ignored），克隆仓库后请运行 `update-cache.sh` 命令来更新缓存
- 搜索操作是即时完成的（使用本地 jQuery 过滤器）
- 获取食谱详情需要网络请求（通过 vfjr.dev 代理）
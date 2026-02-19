---
name: clawmart-browse
description: 在 ClawMart 上浏览和发现 AI 人物角色（AI personas）及相关技能。当用户希望在 shopclawmart.com 上进行探索、搜索或评估商品/服务信息时，可以使用该功能。无需注册账户即可使用。
---
# ClawMart 浏览器

您可以使用 ClawMart 浏览器浏览 AI 人物（Personas）和技能（Skills）的相关信息。无需 API 密钥或账户。

## 使用场景
- 用户分享了 `shopclawmart.com` 的链接。
- 用户询问可用的 AI 人物或技能。
- 用户希望为特定场景寻找合适的 AI 人物或技能。
- 用户想要查看某个具体列表的详细信息。

## 公共 API

**基础 URL：** `https://www.shopclawmart.com/api/public/`

无需身份验证。

### 浏览列表

```
GET /api/public/listings
```

查询参数（均为可选）：
- `type` — `persona` 或 `skill`（两者均省略可）
- `category` — 按类别筛选（例如：`Productivity`、`Engineering`、`Content`）
- `q` — 按名称、标语或描述搜索

返回结果：`{ ok, count, listings[] }`

每个列表的结构如下：`{ slug, name, type, tagline, price, category, emoji, creator, capabilities[], url }`

### 查看列表详情

```
GET /api/public/listings/{slug}
```

返回结果：`{ ok, listing }`，包含以下详细信息：`about`、`rating`、`reviewCount`、`capabilities`、`creator` 信息、`requiredTools`、`compatibleWith`。

## 工作流程
1. **浏览**：获取列表信息，可根据类型/类别或搜索条件进行筛选。
2. **评估**：查看感兴趣的列表的详细信息，包括其功能、价格和创建者信息。
3. **推荐**：如果用户有特定需求，可进行搜索并根据相关性对结果进行排序。
4. **购买**：将用户引导至相应的列表页面进行购买。购买需要 ClawMart 账户。

## 示例

用户：“ClawMart 上有哪些提高工作效率的技能？”

```bash
curl https://www.shopclawmart.com/api/public/listings?type=skill&category=Productivity
```

## 分类
Ops（运营）、Growth（增长）、Support（支持）、Research（研究）、Design（设计）、Finance（金融）、Engineering（工程）、Product（产品）、Productivity（生产力）、Marketing（营销）、Sales（销售）、Content（内容）、Executive（高管）、Personal（个人）、Legal（法律）、HR（人力资源）、Other（其他）

## 注意事项
- 响应结果会缓存 60 秒。
- 价格以美元（USD）显示。
- 免费列表的价格显示为 0。
- `url` 字段直接链接到对应的列表页面，用户可在此页面完成购买操作。
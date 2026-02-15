---
name: scryfall-mtg
description: "使用 Scryfall API 搜索并检索《万智牌》（Magic: The Gathering）的卡片数据。当用户询问关于《万智牌》的卡片信息、想要根据卡片名称、类型、颜色、法术力费用、卡片描述（oracle text）、系列（set）或其他卡片属性进行搜索时，可以使用此技能。此外，该技能还可用于获取卡片图片、价格、规则说明、合法性信息，或随机抽取卡片。触发条件包括提到“MTG”、“Magic”、“Magic: The Gathering”或卡片名称，以及与卡片构建相关的问题或请求。"
---

# 使用 Scryfall API 搜索 Magic: The Gathering 卡片

您可以使用 Scryfall API 来搜索 Magic: The Gathering 的卡片。

## API 概述

基础 URL：`https://api.scryfall.com`

**必需的请求头：**
```python
headers = {
    "User-Agent": "OpenClawMTGSkill/1.0",
    "Accept": "application/json"
}
```

**速率限制：** 请求之间需要等待 50-100 毫秒（每秒最多 10 个请求）。

## 核心接口

### 搜索卡片
```
GET /cards/search?q={query}
```

参数：
- `q`（必需）：全文搜索查询
- `unique`：cards|art|prints（默认：cards）
- `order`：name|set|released|rarity|color|usd|tix|eur|cmc|power|toughness|edhrec|penny|artist|review
- `dir`：auto|asc|desc
- `page`：分页的页码

### 查找特定名称的卡片
```
GET /cards/named?exact={name}
GET /cards/named?fuzzy={name}
```

使用 `fuzzy` 进行部分匹配（例如：“jac bele” → “Jace Beleren”）。
添加 `&set={code}` 以限制搜索范围到特定系列。

### 随机卡片
```
GET /cards/random
GET /cards/random?q={query}
```

### 通过 ID 查找卡片
```
GET /cards/{id}
GET /cards/{set_code}/{collector_number}
```

### 自动完成输入
```
GET /cards/autocomplete?q={partial_name}
```

返回最多 20 个卡片名称的建议。

## 搜索语法参考

请参阅 `references/search_syntax.md` 以获取完整的搜索语法指南。

**快速示例：**
- `c:red pow=3` - 红色且力量值为 3 的卡片
- `t:merfolk t:legend` - 传说级别的鱼人卡片
- `o:"draw a card"` - 文本中包含 “draw a card” 的卡片
- `cmc=3 r:rare` - 需要 3 点法术力的稀有卡片
- `e:dom` - 来自 Dominaria 系列的卡片
- `f:standard` - 符合标准的合法卡片
- `usd<1` - 价格低于 1 美元的卡片

## 实现方式

可以使用提供的脚本来执行常见操作：

```bash
python3 scripts/scryfall_search.py search "lightning bolt"
python3 scripts/scryfall_search.py named --exact "Black Lotus"
python3 scripts/scryfall_search.py random
python3 scripts/scryfall_search.py random --query "t:dragon"
```

或者直接使用正确的请求头和速率限制进行 API 调用。

## 卡片对象的关键字段

在显示卡片信息时，优先显示以下字段：
- `name`（名称）
- `mana_cost`（法术力费用）
- `type_line`（卡片类型）
- `oracle_text`（卡牌描述）
- `power`（力量值）
- `toughness`（防御力）
- `image_uris.normal`（卡片图片的 URL）
- `prices.usd`（普通卡片的售价）
- `prices.usd_foil`（闪卡售价）
- `legalities`（卡片的合法性）
- `set_name`（系列名称）
- `rarity`（稀有度）

对于双面卡片，请查看 `card_faces` 数组。

## 错误处理

- 404：卡片未找到
- 422：无效的搜索查询
- 429：达到速率限制（请稍后重试）

始终验证响应是否包含 `object` 字段；如果 `object` 的值为 “error”，请查看 `details` 以获取错误信息。
# ClawSavings — 以色列折扣与价格比较服务

> **核心优势：** 为您精准推荐在任何商店中最能为您节省费用的以色列信用卡——覆盖72家商店，24个经过验证的优惠信息，一站式解决方案。

---

## 适用场景

当用户询问以下问题时，请激活该功能：
- 在特定商店使用哪种信用卡/会员卡最划算（例如：“באיזה כרטיס לויקטורי?”）
- 以色列商店的折扣、优惠券及促销活动
- 如何在以色列购物时节省费用
- 哪里可以买到某件商品的最便宜价格（例如：“איפה הכי זול לקנות?”）
- 相关关键词：**הנחה**（折扣）、**חיסכון**（节省）、**כרטיס**（信用卡）、**מועדון**（会员卡）、**שובר**（优惠券）、**זול**（便宜）

---

## 知识库加载策略——仅加载所需数据

完整的 `discounts.json` 文件大小约为20KB。**请勿加载整个文件**，而是通过精确的数据提取来降低计算成本。

### 第一步：确定查询类别（始终优先进行）

```bash
python3 -c "
import json
d = json.load(open('~/.openclaw/workspace/skills/clawsavings/discounts.json'))
store = 'שם_החנות'  # replace with the queried store
cat = d['quick_lookup']['store_to_category'].get(store)
best = d['quick_lookup']['best_sources_by_category'].get(cat, [])
print('category:', cat)
print('best_sources:', best)
"
```

加载成本：仅读取 `quick_lookup` 数据，总共约200个数据单元。

### 第二步：仅加载该类别及其相关元数据

```bash
python3 -c "
import json
d = json.load(open('~/.openclaw/workspace/skills/clawsavings/discounts.json'))
cat = 'supermarkets'  # from step 1
out = {
    'category_data': d['categories'][cat],
    'sources_meta': {k: d['sources'][k] for k in d['quick_lookup']['best_sources_by_category'][cat]},
    'cache_ttl_days': d['meta']['cache_ttl_days']
}
import sys; json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
" 2>/dev/null
```

加载成本：约800–1,200个数据单元（针对单个类别），而完整文件则需要约5,000个数据单元。  
**每次查询所需的数据量减少了约75%。**

### 如果商店信息不在 `quick_lookup` 中

仅加载 `quick_lookup.store_to_category` 数据，并告知用户该商店尚未被收录在数据库中，建议用户查看 HTZone 或 Poalim Wonder 网站。

---

## 决策逻辑

### “在商店X应该使用哪种信用卡/会员卡？”

1. 通过第一步确定查询类别。
2. 通过第二步加载该类别的相关信息。
3. 遍历 `best_sources_by_category[category]` 中的所有信息来源：
   - 检查 `type` 字段：`pos_discount` 表示结账时自动享受折扣；`voucher` 表示需提前购买优惠券；`cashback` 表示事后返现。
   - 检查 `deals[]` 和 `cached_at` 字段——优惠信息是否有效（有效期为30天）。
   - 如果优惠信息为空或过期，使用 `max_pct` 作为默认推荐。
5. 根据 `effective_pct`（优惠力度）或 `max_pct`（综合评分）对结果进行排序。
6. 用希伯来语简洁地回答用户问题。

**回答模板：**
```
ל[חנות]:

1. **[מקור]** — [עסקה ספציפית או % מקסימום]
2. **[מקור]** — [עסקה ספציפית או % מקסימום]

💡 [טיפ מעשי אחד]
```

### “购买商品X在哪里最便宜？”

（基于预先计算的结果，无需额外查询）：
- **最便宜的商店：** רמי לוי, אושר עד
- **性价比较高的商店：** ויקטורי, יינות ביתן
- **中等价位的商店：** שופרסל, מגה
- **价格较高的商店：** AM:PM, שופרסל אקספרס

如需获取商品的具体价格，请参考政府提供的XML数据（请用户自行使用爬虫工具获取）：
`https://github.com/OpenIsraeliSupermarkets/israeli-supermarket-scarpers`

### “如何在X类别的商品上节省最多费用？”

1. 加载相关类别的信息。
2. 列出所有可用的优惠来源。
3. 向用户解释最划算的购买方式（例如：“如果同时拥有Poalim Wonder优惠券和HTZone信用卡，可以同时使用这两种优惠”）。

---

## 缓存更新（按需进行）

**更新条件：** 当 `cached_at` 为 `null` 或超过30天时，且用户需要查看最新价格时。

**更新方法：**
1. 立即使用已有的结构化数据（`max_pct`）给出答案，避免延迟响应。
2. 提示用户：“具体价格需要进一步核实”。
3. 如果用户确认需要实时价格，请让用户通过浏览器访问相应网站获取最新信息。
4. 解析网站数据，更新 `discounts.json` 文件中的 `deals[]` 和 `cached_at` 字段。

**需要更新的网站链接：**
| 来源 | URL |
|--------|-----|
| `poalim_wonder` | `https://www.bankhapoalim.co.il/he/Poalim-Wonder` 的 `/Shopping` 子页面 |
| `htzone_club` | `https://www.htzone.co.il/sale/1147`（需要登录并启用JavaScript） |
| `htzone_pos` | `https://www.htzone.co.il/sale/62`（需要登录并启用JavaScript） |

**缓存更新规则：**
- 对于无需登录的简单网站（如Poalim Wonder），当前缓存机制即可满足需求。
- 对于需要登录并启用JavaScript的HTZone网站，建议使用浏览器自动化工具（需保持登录状态）；如果无法获取实时数据，仅提供结构化信息并说明限制。

**更新后的文件格式：**
---


## 输出要求

- **语言：** 希伯来语
- **语气：** 简洁实用，避免冗余信息。
- **金额：** 显示货币金额时务必使用确切的₪符号（例如：₪300 → ₪259）。
- **自动折扣与优惠券的区别：** 清晰区分结账时自动享受的折扣和需提前购买的优惠券。
- **回答长度：** 通常不超过5行，除非有多种优惠方案需要列出。

---

## 使用示例

**“在ויקטורי信用卡中，哪种卡最划算？”**
```
לויקטורי:
1. **פועלים וונדר** — שובר ₪300 ב-₪259 + 50 נקודות (13.7%)
2. **כרטיס הייטקזון** — עד 20% אוטומטית בקופה

💡 אם יש לך את שניהם — קנה שובר וונדר ושלם איתו עם כרטיס הייטקזון
```

**“沃尔特（Victory）信用卡有折扣吗？”**
```
וולט — פועלים וונדר: שובר ₪100 ב-₪80 + 25 נקודות (20% 🔥)
```

**“购买某件商品在哪里最便宜？”**
```
לסל קניות רגיל: רמי לוי / אושר עד הכי זולים.
אם יש לך פועלים וונדר — שובר רמי לוי ₪700 ב-₪620 (11.4%).
```

---

## 维护工作

- **季度性维护（结构层）：** 检查HTZone/Poalim Wonder的优惠规则是否有变化，更新 `max_pct` 和 `last_reviewed` 字段。
- **按需维护（优惠信息层）：** 仅在用户询问且缓存数据过期时更新 `deals[]` 和 `cached_at` 字段。

---

## 限制条件

1. HTZone的特定优惠需要用户登录并启用JavaScript才能查看；在这种情况下，使用 `max_pct` 作为默认推荐。
2. 政府提供的XML价格数据尚未整合到系统中，目前仅作为参考使用。
3. AM:PM和Isracard的优惠信息尚未完成整理，暂时无法提供。
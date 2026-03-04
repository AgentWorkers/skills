---
name: google-hotels
description: 使用浏览器自动化技术，在 Google Hotels 上搜索酒店的价格、评分和可用性。当用户请求搜索酒店、查找住宿、比较酒店价格、查询可用性或查找入住地点时，可以使用该功能。触发语句包括：“search hotels”（搜索酒店）、“find hotels”（查找酒店）、“hotels in”（位于……的酒店）、“where to stay”（在哪里入住）、“accommodation”（住宿）、“hotel prices”（酒店价格）、“cheapest hotel”（最便宜的酒店）、“best hotel”（最好的酒店）、“places to stay”（入住地点）、“hotel near”（附近的酒店）、“book a hotel”（预订酒店）、“hotel ratings”（酒店评分）。
allowed-tools: Bash(agent-browser:*), Bash(echo*), Bash(printf*)
---
# 谷歌酒店搜索

通过代理浏览器使用谷歌酒店搜索功能，可以查找酒店的价格、评分、设施以及房源情况。

## 使用场景

- 用户需要搜索、查找或比较酒店或住宿选项。
- 用户希望获取特定城市、社区或地标附近的酒店价格。
- 用户想了解特定日期的酒店预订情况。
- 用户希望找到评分最高或价格最低的酒店。

## 不适用场景

- **预订**：此功能仅用于搜索，不支持完成预订操作。
- **度假租赁/爱彼迎**：谷歌酒店仅显示酒店信息，不提供租赁服务。
- **航班查询**：请使用专门的航班搜索功能。
- **历史价格**：谷歌酒店仅显示当前价格。
- **搜索过程中严禁离开谷歌酒店页面**：请勿跳转至Booking.com、Expedia、Hotels.com等在线旅行平台进行预订（特殊情况：在展示结果后，可访问酒店官网进行直接预订或查看优惠信息，详见[搜索后操作](#post-search-direct-booking--deals)。

## 会话规范

为确保数据隔离，请始终使用`--session hotels`参数。

## 高效的URL路径（推荐）

使用包含位置和日期的URL进行搜索，可快速获取结果（总共需要3条命令）。

### URL模板

```
https://www.google.com/travel/search?q={QUERY}&qs=CAE4AA&ts={TS_PARAM}&ap=MAE
```

其中`{QUERY}`代表搜索位置或酒店名称，`{TS_PARAM}`代表经过Base64编码的日期参数。

### URL中的日期编码方式

谷歌酒店使用protobuf格式对日期进行编码。对于2025至2030年的日期，编码规则如下（使用以下bash命令生成日期参数）：

```bash
hotel_ts() {
  local ci_y=$1 ci_m=$2 ci_d=$3 co_y=$4 co_m=$5 co_d=$6 nights=$7
  local cyl=$(printf '%02x' $(( ($ci_y & 0x7f) | 0x80 )))
  local cyh=$(printf '%02x' $(($ci_y >> 7)))
  local col=$(printf '%02x' $(( ($co_y & 0x7f) | 0x80 )))
  local coh=$(printf '%02x' $(($co_y >> 7)))
  echo -n "08011a200a021a00121a12140a0708${cyl}${cyh}10$(printf '%02x' $ci_m)18$(printf '%02x' $ci_d)120708${col}${coh}10$(printf '%02x' $co_m)18$(printf '%02x' $co_d)18$(printf '%02x' $nights)32020801" \
    | xxd -r -p | base64 | tr -d '\n='
}
# Usage: hotel_ts CHECKIN_YEAR MONTH DAY CHECKOUT_YEAR MONTH DAY NIGHTS
# Example: hotel_ts 2026 3 15 2026 3 20 5
# Output: CAEaIAoCGgASGhIUCgcI6g8QAxgPEgcI6g8QAxgUGAUyAggB
```

**注意**：该编码方式适用于2025至2030年内的年份、月份（1-12月）和日期（1-31日）以及入住天数（1-127天），能够覆盖所有常见的酒店搜索需求。

### 地点输入格式

| 格式 | 例子 |
|--------|---------|
| 城市 | `Hotels+in+Bangkok` |
| 城市+国家 | `Hotels+in+Bangkok+Thailand` |
| 社区 | `Hotels+in+Shibuya+Tokyo` |
| 附近地标 | `Hotels+near+Eiffel+Tower` |
| 地区 | `Hotels+in+Amalfi+Coast` |
| 机场 | `Hotels+near+BKK+airport` |
| **特定酒店** | `Haus+im+Tal+Munich` |

### URL与交互式功能的区别

| 功能 | 是否可以通过URL实现？ |
|---------|----------|
| 地点 | ✅ 可以（通过`q=`参数） |
| **日期** | ✅ 可以（通过`ts=`参数） |
| 客人数/房间数 | ❌ 需要手动设置（默认：1间房，2位客人） |
| 过滤条件（星级、价格、设施） | ❌ 需要手动设置 |

### 示例：曼谷酒店（3月15日至20日）

```bash
# Step 1: Generate ts parameter
ts=$(hotel_ts 2026 3 15 2026 3 20 5)

# Step 2: Open with location + dates — results load immediately
agent-browser --session hotels open "https://www.google.com/travel/search?q=Hotels+in+Bangkok&qs=CAE4AA&ts=${ts}&ap=MAE"
agent-browser --session hotels wait --load networkidle
agent-browser --session hotels snapshot -i

# Step 3: Extract results from snapshot, then close
agent-browser --session hotels close
```

### 示例：特定酒店及日期查询

```bash
ts=$(hotel_ts 2026 3 9 2026 3 12 3)
agent-browser --session hotels open "https://www.google.com/travel/search?q=Haus+im+Tal+Munich&qs=CAE4AA&ts=${ts}&ap=MAE"
agent-browser --session hotels wait --load networkidle
agent-browser --session hotels snapshot -i
agent-browser --session hotels close
```

### 仅输入位置（不输入日期）

如果用户未指定日期，可省略`ts`、`qs`和`ap`参数：

```bash
agent-browser --session hotels open "https://www.google.com/travel/search?q=Hotels+in+Bangkok"
agent-browser --session hotels wait --load networkidle
agent-browser --session hotels snapshot -i
```

系统会显示“起始价格”。用户后续提供日期时，可手动设置日期（详见[深入参考](#deep-dive-reference)。

有关详细的交互式操作流程（日历导航、客人/房间选择器、过滤条件等），请参阅[深入参考](#deep-dive-reference)。

## 结果展示方式

结果将以表格形式呈现：

```
| # | Hotel | Stars | Rating | Price/Night | Total | Via | Key Amenities |
|---|-------|-------|--------|-------------|-------|-----|---------------|
| 1 | Sukhothai Bangkok | ★★★★★ | 9.2 | $185 | $925 | Hotels.com | Pool, Spa, WiFi |
| 2 | Centara Grand | ★★★★★ | 8.8 | $165 | $825 | Booking.com | Pool, Gym, WiFi |
| 3 | Ibis Sukhumvit | ★★★ | 7.4 | $45 | $225 | Agoda | WiFi, Restaurant |
```

## 并行搜索

仅当用户明确要求比较不同搜索结果时使用此功能（例如：“比较涩谷和新宿的酒店”）。

```bash
agent-browser --session shibuya open "https://www.google.com/travel/search?q=Hotels+in+Shibuya+Tokyo" &
agent-browser --session shinjuku open "https://www.google.com/travel/search?q=Hotels+in+Shinjuku+Tokyo" &
wait

agent-browser --session shibuya wait --load networkidle &
agent-browser --session shinjuku wait --load networkidle &
wait

# Set dates in both sessions, then snapshot both
agent-browser --session shibuya snapshot -i
agent-browser --session shinjuku snapshot -i

agent-browser --session shibuya close &
agent-browser --session shinjuku close &
wait
```

## 重要规则

| 规则 | 原因 |
|------|-----|
| 建议使用包含`ts=`参数的URL路径 | 仅需3条命令即可完成搜索，比交互式方式更高效 |
| 使用`wait --load networkidle` | 比固定的`wait 5000`等待时间更合理 |
| 日期信息务必通过URL编码 | 使用`hotel_ts`参数生成日期参数 |
| 使用`fill`而非`type`输入文本 | 避免覆盖现有文本 |
| 输入位置后等待2秒 | 自动完成输入需要与服务器进行多次交互 |
| 点击建议项时勿直接输入 | 直接输入可能导致自动完成失败 |
| 每次操作后重新生成数据 | DOM变化可能导致数据失效 |
| 查看“价格”选项 | 表示用户尚未设置具体日期 |
| **搜索过程中严禁离开谷歌酒店页面**：特殊情况：结果展示后可访问酒店官网进行直接预订 |
| 使用“<”和“>”箭头导航日历 | 日历可能打开错误月份，使用箭头调整月份 |

## 常见问题及解决方法

| 问题 | 解决方案 |
|---------|----------|
| 同意弹窗 | 点击“接受全部”或“拒绝全部” |
| URL路径失败 | 转回`google.com/travel/hotels`的交互式搜索页面 |
| 无结果/“查看价格”选项 | 设置入住和退房日期 |
| 日历打开错误月份 | 使用“<”箭头向后导航，使用“>”箭头向前导航。确认目标月份后重新生成数据 |
| 日历覆盖导致数据无法更新 | 按Esc键关闭日历，重新生成数据后再次尝试 |
| 价格信息过时 | 价格为实时更新的信息，请告知用户 |
| 货币单位不一致 | 谷歌会根据浏览器设置显示货币单位，请注意可能存在的差异 |
| 验证码 | 通知用户并稍后重试 |
| 地图视图而非列表视图 | 点击“列表”或“查看列表”切换视图 |
| 酒店未找到 | 尝试使用不同的搜索词（全名、简称、酒店名称+城市名等）

## 搜索后操作：直接预订与优惠信息

在展示结果后，**务必询问用户**是否希望您帮忙查询更优惠的预订信息。可这样表达：

> “您希望我查看[酒店名称]的官网是否有优惠码或会员专享价格吗？直接预订通常比在线旅行平台更便宜。”

### 适用场景

- **始终**在用户通过名称搜索特定酒店时使用。
- **始终**在结果中显示用户感兴趣的酒店时使用。
- **在比较多款酒店时**：根据用户选择的结果提供相应优惠信息。

### 检查内容

在新的会话中（使用`--session direct`参数）打开酒店官网，查看以下内容：

1. **直接预订价格**：通常比在线旅行平台便宜5-15%。
2. **优惠码**：查看网站上的广告、弹窗或“优惠”“特价”页面。
3. **会员/忠诚度折扣**：如“首次预订享受X%折扣”或免费会员优惠。
4. **套餐优惠**：包含早餐、免费取消政策、停车服务。
5. **季节性优惠**：节假日特价、提前预订优惠、最后一刻优惠。

```bash
# After Google Hotels search is done, visit hotel's direct site
agent-browser --session direct open "https://www.example-hotel.com"
agent-browser --session direct wait --load networkidle
agent-browser --session direct snapshot -i
# Look for: promo banners, "offers" or "deals" links, booking widget prices
agent-browser --session direct close
```

### 酒店连锁品牌

如果酒店属于知名连锁品牌，请告知用户相关会员计划。会员通常可享受更低的价格、房间升级或积分优惠：

| 酒店连锁 | 品牌 | 会员计划 | 会员权益 |
|-------|--------|----------------|---------------------|
| IHG | Holiday Inn、InterContinental、Crowne Plaza、Kimpton、Indigo | IHG One Rewards | 会员价（通常最优惠），积分累积，奖励入住第四晚免费 |
| Marriott | Marriott、Sheraton、Westin、W、Ritz-Carlton、Courtyard、Aloft | Marriott Bonvoy | 会员价，移动入住，积分兑换 |
| Hilton | Hilton、DoubleTree、Hampton、Conrad、Waldorf Astoria | Hilton Honors | 会员折扣，奖励入住第五晚免费，数字钥匙 |
| Accor | Sofitel、Novotel、ibis、Mercure、Moxy、Fairmont | ALL - Accor Live Limitless | 会员价，会员专属福利 |
| Hyatt | Hyatt、Andaz、Park Hyatt、Thompson | World of Hyatt | 会员价，免费入住夜晚奖励，套房升级 |

### 如何识别酒店连锁品牌

谷歌酒店结果中通常会显示酒店所属的连锁品牌：
- `"Holiday Inn Express Bangkok Sukhumvit 11 by IHG"` → IHG品牌
- `"Courtyard by Marriott Bangkok"` → Marriott品牌
- `"Hilton Munich City"` → Hilton品牌
- `"Novotel Muenchen City"` → Accor品牌
- 无品牌后缀 → 可能为独立酒店（请直接访问酒店官网确认）

### 独立酒店

对于独立或精品酒店（如Haus im Tal），请查看官网上的优惠信息（通常会在广告或“优惠”页面显示），或查看是否有“直接预订”优惠，以及是否提供注册会员的折扣。如果官网没有相关信息，可在搜索时输入酒店名称+“优惠码”进行查询。

### 结果对比

查看对比信息后，向用户展示酒店官网价格与在线旅行平台价格的差异：

```
## Haus im Tal — Booking Comparison

| Source | Room Type | Price/Night | Total (3 nights) | Notes |
|--------|-----------|-------------|-------------------|-------|
| Booking.com | Downtown Cozy | €183 | €549 | Free cancellation |
| Hotel direct | Downtown Cozy | €175 | €525 | Use code HIT24 for 5% off |
| Hotel direct (with code) | Downtown Cozy | €166 | €499 | Best price |
```

> **提示**：请务必告知用户您无法完成预订操作，仅提供酒店官网链接和找到的优惠信息。

## 详细参考资料

请参阅[references/interaction-patterns.md]，了解以下内容：
- 完整的操作流程及预期输出。
- 地点自动完成输入的失败情况及解决方法。
- 日历导航功能。
- 客人和房间选择器（最复杂的交互组件）。
- 过滤条件（星级、价格、设施、取消政策）。
- 滚动查看更多结果。
- 酒店详情及价格对比功能。
- 直接预订和优惠信息查询的完整流程。
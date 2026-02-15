---
name: skanetrafiken
description: 斯科讷地区公共交通行程规划器（Skånetrafiken）：可以规划公交/火车行程，并提供实时的延误信息。支持输入车站名称、地址、地标信息，同时支持跨境前往哥本哈根的行程规划。
license: MIT
compatibility: Requires curl, jq. Works with Claude Code and compatible agents.
metadata:
  author: rezkam
  version: "1.2.0"
  region: sweden
---

# 斯科讷交通旅行规划器

使用实时出发信息规划瑞典斯科讷地区的公共交通行程。

## 命令

### 1. 搜索地点

搜索车站、地址或兴趣点。

```bash
./search-location.sh <query> [limit]
```

| 参数 | 描述 |
|----------|-------------|
| `query` | 要搜索的地点名称 |
| `limit` | 显示的结果数量（默认：3，最大：10） |

**输出包括：**
- `ID` - 地点标识符（用于行程搜索）
- `Name` | 地点的官方名称 |
- `Type` - `STOP_AREA`（车站）、`ADDRESS`或`POI`（兴趣点） |
- `Area` | 地区/市镇 |
- `Coordinates` | 纬度、经度 |

**何时增加结果数量：**
- 首个结果不符合用户意图 |
- 用户的查询不明确（例如：“车站”、“中心”） |
- 需要向用户展示多个选项供选择

### 2. 行程搜索

使用两个地点的ID来规划行程。

```bash
./journey.sh <from-id> <from-type> <to-id> <to-type> [datetime] [mode]
```

| 参数 | 描述 |
|----------|-------------|
| `from-id` | 出发地点ID（来自搜索）或坐标（`lat#lon`） |
| `from-type` | `STOP_AREA`、`ADDRESS`、`POI`或`LOCATION`（对于坐标） |
| `to-id` | 目的地地点ID或坐标 |
| `to-type` | 目的地类型 |
| `datetime` | 可选：`"18:30"`、`"明天09:00"`、`"2026-01-15 09:00"` |
| `mode` | 可选：`"depart"`（默认）或`"arrive"` |

**重要提示：** 行程API仅接受`STOP_AREA`和`LOCATION`类型。对于`ADDRESS`或`POI`结果，请使用`lat#lon`格式的坐标，并指定类型为`LOCATION`。

---

## 理解用户的时间意图

在搜索之前，先了解用户的真实需求：

### 意图类型

| 用户输入 | 意图 | 查询方式 |
|-----------|--------|--------------|
| "现在"、"下一班公交车"、"我怎么去..." | **立即出行** | 不需要指定时间 |
| "30分钟后"、"1小时后"、"午饭后" | **稍后出发** | 计算出发时间，使用`depart`模式 |
| "大约15:00"、"下午某个时候" | **在某个时间段内出行** | 使用偏移时间进行查询 |
| "在18:00之前到达"、"需要在9点到达" | **指定到达时间** | 使用`arrive`模式 |
| "明天早上"、"周五10点" | **未来时间** | 使用具体时间 |

### 处理“在某个时间段内出行”的查询

当用户希望查询某个时间段内的行程时，提前15-30分钟进行查询，以显示该时间段内的所有选项：

```bash
# User: "I want to travel around 15:00"
# Query at 14:30 to get options spanning 14:30-16:00+
./journey.sh ... "14:30" depart
```

### 相对时间计算

将相对时间转换为绝对时间：

| 用户输入 | 当前时间 | 查询时间 |
|-----------|----------------|------------|
| "30分钟后" | → | "14:30" |
| "1小时后" | → | "15:00" |
| "2小时后" | → | "16:00" |

---

## LLM响应格式

在向用户展示行程结果时，请使用以下表情符号和格式规范。

### 表情符号说明

| 表情符号 | 代表含义 |
|-------|---------|
| 🚂 | 火车（Pågatåg、Öresundståg） |
| 🚌 | 公交车 |
| 🚇 | 地铁（哥本哈根） |
| 🚋 | 有轨电车 |
| ⛴️ | 渡轮 |
| 🚶 | 步行路段 |
| ⏱️ | 时间/时长 |
| 🕐 | 出发时间 |
| 🏁 | 到达时间 |
| 📍 | 车站 |
| 🏠 | 出发地（起点） |
| 🎯 | 目的地 |
| ⚠️ | 延误或中断 |
| ✅ | 准时 |
| 🔄 | 中转/换乘 |
| 🛤️ | 月台/轨道 |

### 响应结构

**始终包含以下工具输出的关键元素：**

1. **出发时间** - 用户实际需要出发的时间（包括步行时间） |
2. **步行路段** - 步行的距离和时长 |
3. **交通工具出发时间** - 公交车/火车的实际出发时间 |
4. **到达时间** | 用户到达目的地的时间 |
5. **任何延误** - 显示与计划的偏差

### 示例响应格式

**对于简单的直达行程：**
```
🏠 **Leave home at 09:00**

🚶 Walk 450m to Möllevångstorget (5 min)

📍 **Möllevångstorget** → 🎯 **Malmö C**
🚌 Bus 5 departs 09:07 from Möllevångstorget
🏁 Arrives 09:18 at Malmö C

⏱️ Total: 18 min
```

**对于需要中转的行程：**
```
🏠 **Leave at 08:45**

🚶 Walk 300m to Västra Hamnen (4 min)

📍 **Västra Hamnen** → 🔄 **Malmö C** → 🎯 **Lund C**

**Leg 1:**
🚌 Bus 2 departs 08:51 [🛤️ Läge A]
🏁 Arrives Malmö C 09:05

🔄 Transfer at Malmö C (6 min)

**Leg 2:**
🚂 Pågatåg departs 09:11 [🛤️ Spår 4]
🏁 Arrives Lund C 09:23

⏱️ Total: 38 min | 🔄 1 change
```

**存在延误时：**
```
🕐 **Depart 14:30** from Triangeln

🚂 Öresundståg 1042 → København H
⚠️ +8 min delay (expected 14:38 instead of 14:30)
🏁 Arrives ~15:25 (normally 15:17)
```

### 步行路段详情

**重要提示：** 必须在工具输出中显示步行路段的详细信息：**

- 距离（以米为单位，来自`line.distance`）
- 将步行时间计入“出发时间”的计算中 |
- 在行程的开始和结束时都显示步行时间

示例工具输出：
```
→ WALK 450m from Kalendegatan to Möllevångstorget
```

格式示例：
```
🚶 Walk 450m to Möllevångstorget (~5 min)
```

步行时间估计：大约每分钟100米（正常步行速度）

### 显示多个选项

在展示行程选项时，要确保时间信息清晰明了：

```
I found 3 options for you:

**Option 1 - Leave now (09:00)** ✅ Recommended
🚶 5 min walk → 🚌 Bus 5 at 09:07 → arrives 09:25
⏱️ Total: 25 min

**Option 2 - Leave in 15m (09:15)**
🚶 5 min walk → 🚌 Bus 5 at 09:22 → arrives 09:40
⏱️ Total: 25 min

**Option 3 - Leave in 30m (09:30)**
🚶 5 min walk → 🚂 Train at 09:37 → arrives 09:48
⏱️ Total: 18 min | Faster but later departure
```

### 时间偏移表示法

使用明确的表示法来表示出发时间：

| 表示法 | 含义 |
|----------|---------|
| "现在" | 立即出发 |
| "15分钟后" | 15分钟后 |
| "1小时后" | 1小时后 |
| "14:30" | 具体时间 |

---

## LLM工作流程：如何规划行程

当用户请求行程时，请按照以下流程操作：

### 第1步：理解用户的时间意图

解析用户的真实需求：
- “我怎么去...” → 立即出行 |
- “我需要在18:00之前到达” → 使用`arrive`模式 |
- “大约下午3点” → 在14:00左右查询行程 |
- “大约1小时后” → 根据当前时间计算行程时间 |

### 第2步：分别搜索两个地点

分别搜索出发地和目的地：

```bash
./search-location.sh "Malmö C"
./search-location.sh "Emporia"
```

### 第3步：验证搜索结果

**仔细检查每个结果：**

1. **是否完全匹配？** 如果名称与用户请求一致，则继续下一步。
2. **返回了多个结果？** 脚本最多显示10个结果。如果第一个结果不正确，请让用户确认。
3. **名称差异较大？** 如果用户询问的是“Hyllie附近的购物中心”，而结果显示的是“Emporia”，请确认：“我找到了Hyllie附近的Emporia购物中心。这是正确的吗？”
4. **没有找到结果？** 尝试其他搜索方法。

### 第4步：处理模糊或失败的搜索

**当搜索结果不匹配或模糊时，提出澄清问题：**

```
I searched for "centrum" and found multiple locations:
1. Malmö Centrum (bus stop)
2. Lund Centrum (bus stop)
3. Helsingborg Centrum (bus stop)

Which one did you mean?
```

**当没有找到结果时，尝试以下方法：**

1. **使用城市名称搜索地址：**
   ```bash
   # If "Storgatan 10" fails, try:
   ./search-location.sh "Storgatan 10, Malmö"
   ```

2. **使用官方车站名称：**
   ```bash
   # If "Malmö station" fails, try:
   ./search-location.sh "Malmö C"
   ```

3. **仅使用地标名称（不带城市名称）：**
   ```bash
   # If "Emporia, Malmö" fails, try:
   ./search-location.sh "Emporia"
   ```

4. **最后使用坐标：**
   - 如果知道大致位置，直接使用`lat#lon`格式的坐标
   - 询问用户：“我找不到该地点。您能提供地址或坐标吗？”

### 第5步：转换类型以供行程API使用

行程API仅接受：
- `STOP_AREA` - 公交站/火车站（直接使用ID）
- `LOCATION` - GPS坐标（格式为`lat#lon`）

**如果搜索结果为`ADDRESS`或`POI`：**
- 使用搜索结果中的坐标
- 格式化为`lat#lon`，并指定类型为`LOCATION`

示例：
```bash
# Search returns: ID: 123, Type: ADDRESS, Coordinates: 55.605, 13.003
# Use in journey as:
./journey.sh "55.605#13.003" LOCATION 9021012080000000 STOP_AREA
```

### 第6步：执行行程搜索

确认出发地和目的地的ID/坐标后：

```bash
./journey.sh <from-id> <from-type> <to-id> <to-type> [datetime] [mode]
```

### 第7步：使用表情符号格式化响应

使用上述表情符号指南清晰地展示结果。**始终使用工具输出中的实际数值，不要猜测或估算。**

---

## 查询格式规则

**搜索API对格式非常敏感，请遵循以下规则：**

### 地标和兴趣点：仅使用名称

搜索时只使用地标名称，不要包含城市名称。

```bash
# CORRECT
./search-location.sh "Emporia"
./search-location.sh "Triangeln"
./search-location.sh "Turning Torso"

# WRONG - city name breaks POI search
./search-location.sh "Emporia, Malmö"        # May return wrong location!
./search-location.sh "Triangeln, Malmö"      # Unnecessary, may fail
```

### 街道地址：包含城市名称

为了提高准确性，地址中必须包含城市名称。

```bash
# CORRECT
./search-location.sh "Kalendegatan 12, Malmö"
./search-location.sh "Storgatan 25, Lund"
./search-location.sh "Drottninggatan 5, Helsingborg"

# RISKY - may be ambiguous
./search-location.sh "Kalendegatan 12"       # Works if unambiguous
```

### 火车站：使用官方名称

中央车站使用“C”后缀。

```bash
# CORRECT
./search-location.sh "Malmö C"
./search-location.sh "Lund C"
./search-location.sh "Helsingborg C"
./search-location.sh "Malmö Hyllie"
./search-location.sh "Malmö Triangeln"

# WRONG
./search-location.sh "Malmö"                 # Ambiguous!
./search-location.sh "Malmö Central"         # Not official name
./search-location.sh "Lund station"          # Not official name
```

### 哥本哈根（跨境行程）**

使用丹麦名称或常用替代名称。

```bash
# All work
./search-location.sh "København H"
./search-location.sh "Nørreport"
./search-location.sh "Copenhagen Airport"
./search-location.sh "Köpenhamn"
```

---

## 示例

### 示例1：立即出行

用户：“我怎么从马尔默C站去隆德C站？”

```bash
./search-location.sh "Malmö C"
./search-location.sh "Lund C"
./journey.sh 9021012080000000 STOP_AREA 9021012080040000 STOP_AREA
```

**响应：**
```
🏠 **Leave now** from Malmö C

📍 **Malmö C** → 🎯 **Lund C**
🚂 Öresundståg 1324 departs 09:04 [🛤️ Spår 2b]
🏁 Arrives 09:16 at Lund C [🛤️ Spår 1]

⏱️ Total: 12 min | ✅ Direct, no changes
```

### 示例2：包含步行路段的地址

用户：“我需要从马尔默的Kalendegatan 12号去Emporia购物中心。”

```bash
./search-location.sh "Kalendegatan 12, Malmö"
./search-location.sh "Emporia"
./journey.sh "55.595#13.001" LOCATION "55.563#12.973" LOCATION
```

**响应：**
```
🏠 **Leave at 10:05**

🚶 Walk 320m to Möllevångstorget (~3 min)

📍 **Möllevångstorget** → 🎯 **Emporia**
🚌 Bus 32 departs 10:10
🏁 Arrives 10:28 at Emporia

🚶 Walk 150m to destination (~2 min)

⏱️ Total: 25 min
```

### 示例3：指定到达时间

用户：“我需要在明天18:00之前到达哥本哈根市中心。”

```bash
./search-location.sh "Malmö C"
./search-location.sh "København H"
./journey.sh 9021012080000000 STOP_AREA 9921000008600626 STOP_AREA "tomorrow 18:00" arrive
```

**响应：**
```
🎯 **Arrive by 18:00** at København H

📍 **Malmö C** → 🎯 **København H**
🚂 Öresundståg departs **17:21** [🛤️ Spår 1]
🏁 Arrives **17:56** ✅ 4 min buffer

⏱️ Journey: 35 min

💡 Leave Malmö C by 17:21 to arrive on time!
```

### 示例4：在某个时间段内出行

用户：“我想在15:00左右去隆德。”

```bash
# Query 30 min earlier to show options around 15:00
./journey.sh 9021012080000000 STOP_AREA 9021012080040000 STOP_AREA "14:30"
```

**响应：**
```
Options around 15:00 for Malmö C → Lund C:

**Option 1 - Depart 14:34** (in 25m)
🚂 Pågatåg → arrives 14:52
⏱️ 18 min

**Option 2 - Depart 14:49** (in 40m)
🚂 Öresundståg → arrives 15:01
⏱️ 12 min

**Option 3 - Depart 15:04** (in 55m) ✅ Closest to 15:00
🚂 Pågatåg → arrives 15:22
⏱️ 18 min

Which works best for you?
```

### 示例5：相对时间

用户：“我想大约1小时后出发。”

```bash
# Current time: 13:00, so query for 14:00
./journey.sh ... "14:00"
```

**响应：**
```
Options departing around 14:00 (in ~1h):

**Leave at 13:55** (in 55m)
🚶 5 min walk → 🚌 Bus 5 at 14:02 → arrives 14:25

**Leave at 14:10** (in 1h 10m)
🚶 5 min walk → 🚂 Train at 14:17 → arrives 14:35

Let me know which one works!
```

### 示例6：行程存在延误

当工具显示延误时：

```
From: 14:30 Malmö C [+8 min late]
```

**响应：**
```
📍 **Malmö C** → 🎯 **Lund C**
🚂 Öresundståg 1042
⚠️ **Running 8 min late**
🕐 Scheduled: 14:30 → Expected: ~14:38
🏁 Arrives ~14:50 (normally 14:42)
```

---

## 何时需要提出澄清问题

**在以下情况下一定要提问：**

1. **搜索没有结果时：**
   - “我找不到[地点]。您能提供更多详细信息，比如完整地址或附近的地标吗？”
2. **返回了多个结果时：**
   - “我找到了多个匹配项：[结果列表]。您指的是哪一个？”
3. **结果名称与查询不符时：**
   - “您查询的是'[查询内容]'，但我找到的最接近的结果是'[结果名称]'。这是正确的吗？”
4. **用户请求不明确时：**
   - “从马尔默出发” - “您指的是马尔默的哪个地点？是马尔默C站还是某个具体地址？”
5. **涉及跨境行程时：**
   - “哥本哈根”可能指多个车站——请确认用户是指København H（中央车站）、机场还是其他车站。
6. **时间不明确时：**
   - “您想什么时候出行？现在还是某个具体时间？”

---

## 时间格式

所有时间均为瑞典当地时间（CET/CEST）。

| 格式 | 例子 | 含义 |
|--------|---------|---------|
| _(empty)_ | | 立即出行 |
| `HH:MM` | `"18:30"` | 今天18:30 |
| `tomorrow HH:MM` | `明天09:00` | 明天09:00 |
| `YYYY-MM-DD HH:MM` | `2026-01-15 09:00` | 具体日期 |

---

## 输出格式

### 行程选项（原始工具输出）

```
══════════════════════════════════════════════════════════════
OPTION 1: Malmö C → Lund C
══════════════════════════════════════════════════════════════
Date:    2026-01-14
Depart:  09:04
Arrive:  09:16
Changes: 0

LEGS:
  → ORESUND Öresundståg 1324
    From: 09:04 Malmö C [Spår 2b]
    To:   09:16 Lund C [Spår 1]
    Direction: mot Helsingborg C
```

### 交通工具类型

| 类型 | 表情符号 | 描述 |
|------|-------|-------------|
| `TRAIN` | 🚂 | 地区火车 |
| `ORESUND` | 🚂 | 跨境火车 |
| `BUS` | 🚌 | 市内或地区公交车 |
| `WALK` | 🚶 | 步行路段 |
| `TRAM` | 🚋 | 有轨电车 |
| `METRO` | 🚇 | 哥本哈根地铁 |
| `FERRY` | ⛴️ | 渡轮 |

### 状态指示器

| 指示器 | 表情符号 | 含义 |
|-----------|-------|---------|
| _(none)_ | ✅ | 准时 |
| `[+X min late]` | ⚠️ | 延误 |
| `[-X min early]` | ℹ️ | 提前 |
| `[PASSED]` | ❌ | 已经出发 |
| `AVVIKELSE` | 🚨 | 服务中断 |

---

## 错误处理

### “未找到地点”

搜索未返回任何结果。

**应对策略：**
1. 检查拼写（瑞典语中的å、ä、ö）
2. 尝试使用带有“C”后缀的官方车站名称（表示中央车站）
3. 对于地标，去掉城市后缀
4. 对于地址，添加城市名称
5. 询问用户以获取更多信息

### “未找到行程”

没有可用的路线。

**应对策略：**
1. 检查该时间段内服务是否正常（夜间/清晨服务可能受限）
2. 尝试不同的出发时间
3. 建议附近的替代站点

---

## 快速参考

| 地点类型 | 搜索格式 | 行程类型 |
|--------------|---------------|--------------|
| 火车站 | `"Malmö C"` | `STOP_AREA` |
| 公交车站 | `"Möllevångstorget"` | `STOP_AREA` |
| 地址 | `"Street 12, City"` | 使用坐标 → `LOCATION` |
| 地标/兴趣点 | `"Emporia"`（不含城市名称） | 使用坐标 → `LOCATION` |
| 坐标 | `55.605#13.003` | `LOCATION` |
---
name: tabussen
description: **韦斯特博滕省及乌梅奥市公共交通行程规划工具（Tabussen/Ultra）**  
该工具利用 ResRobot API 来规划公交行程。支持输入公交车站、地址、坐标信息，并可查询韦斯特博滕省范围内的区域性和本地公交线路。
license: MIT
compatibility: Requires curl, jq. Works with Claude Code and compatible agents.
metadata:
  author: simskii
  version: "1.0.0"
  region: sweden-vasterbotten
---

# Tabussen 旅行规划器

用于规划瑞典西约特堡省（Västerbotten）的公共交通行程——包括乌梅奥（Umeå）的本地公交服务（Ultra）和区域公交线路（Länstrafiken Västerbotten）。

## 概述

此功能利用 **ResRobot API**（来自 Trafiklab）为 Tabussen/Ultra 提供行程规划服务。ResRobot 是瑞典的全国性公共交通 API，涵盖了所有公交运营商，包括 Länstrafiken Västerbotten。

**服务范围：**
- Ultra（乌梅奥本地公交）
- Länstrafiken Västerbotten（区域公交）
- 与其他瑞典地区的公交连接
- 如适用，还包括火车连接

## 命令

### 1. 搜索地点

用于搜索公交车站、火车站或兴趣点。

```bash
./search-location.sh <query> [limit]
```

| 参数 | 说明 |
|----------|-------------|
| `query` | 要搜索的地点名称（添加 `?` 进行模糊搜索） |
| `limit` | 显示的结果数量（默认：5，最大：10） |

**输出包含：**
- `ID` - 车站标识符（用于行程搜索）
- `Name` | 车站的官方名称
- `Coordinates` | 纬度、经度
- `Weight` | 交通流量指标（数值越高，交通越繁忙）

**搜索提示：**
- 使用 `?` 后缀进行模糊/部分匹配：例如 `"Vasaplan?"`
- 不加 `?` 的精确搜索：例如 `"Vasaplan"`
- 包含城市名称以提高准确性：例如 `"Umeå Vasaplan"`

### 2. 行程搜索

使用两个地点的 ID 来规划行程。

```bash
./journey.sh <from-id> <to-id> [datetime] [mode]
```

| 参数 | 说明 |
|----------|-------------|
| `from-id` | 出发车站 ID |
| `to-id` | 目的地车站 ID |
| `datetime` | 可选：`"18:30"`、`tomorrow 09:00`、`2026-01-28 14:00` |
| `mode` | 可选：`"depart"`（默认）或 `"arrive"` |

**基于坐标的搜索：**
```bash
./journey.sh "63.825#20.263" <to-id> [datetime] [mode]
```
使用 `lat#lon` 格式输入坐标（WGS84 十进制度数）。

---

## 理解用户的时间需求

在搜索之前，需要了解用户的具体需求：

### 意图类型

| 用户输入 | 意图 | 查询方式 |
|-----------|--------|--------------|
| "now", "next bus", "how do I get to" | **立即出行** | 不需要指定时间 |
| "in 30 minutes", "in 1 hour" | **稍后出发** | 计算出发时间，使用 `depart` 模式 |
| "around 15:00", "sometime afternoon" | **大约在...时间** | 使用时间偏移量进行查询 |
| "arrive by 18:00", "need to be there at 9" | **必须在...时间到达** | 使用 `arrive` 模式 |
| "tomorrow morning", "on Friday at 10" | **未来时间** | 使用具体日期和时间 |

### 处理“大约在...时间”的查询

当用户请求“大约在某个时间”的行程时，应在该时间前 15-30 分钟查询，以显示之前的和之后的选项：

```bash
# User: "I want to travel around 15:00"
# Query at 14:30 to get options spanning 14:30-16:00+
./journey.sh ... "14:30" depart
```

### 相对时间计算

将相对时间转换为绝对时间：

| 用户输入 | 当前时间 | 查询时间 |
|-----------|----------------|------------|
| "in 30m" | -> | "14:30" |
| "in 1h" | -> | "15:00" |
| "in 2 hours" | -> | "16:00" |

---

## LLM 响应格式

在向用户展示行程结果时，请使用以下表情符号和格式规范。

### 表情符号说明

| 表情符号 | 代表含义 |
|-------|---------|
| `bus` | 公交（Tabussen/Ultra） |
| `train` | 火车 |
| `walk` | 步行段 |
| `clock` | 时间/时长 |
| `clock1` | 出发时间 |
| `goal` | 到达时间 |
| `pin` | 车站 |
| `house` | 出发地（家/起点） |
| `target` | 目的地 |
| `warning` | 延误或中断 |
| `check` | 准时 |
| `arrows_counterclockwise` | 中转/换乘 |

### 响应结构

**始终包含以下工具输出的关键元素：**

1. **出发时间** - 用户实际需要出发的时间（包括步行时间）
2. **步行段** - 步行的距离和时间
3. **公交出发时间** | 公交实际出发的时间
4. **到达时间** | 用户到达目的地的时间
5. **线路编号和方向** | 需乘坐的公交线路

### 示例响应格式

**对于简单的直达行程：**
```
**Leave now** from Vasaplan

**Vasaplan** -> **Universitetet**
Bus 1 (mot Mariehem) departs 09:07
Arrives 09:18 at Universitetet

Total: 11 min
```

**对于需要中转的行程：**
```
**Leave at 08:45**

Walk 300m to Vasaplan (~4 min)

**Vasaplan** -> **Umeå C** -> **Skellefteå**

**Leg 1:**
Bus 1 departs 08:51
Arrives Umeå C 09:05

Transfer at Umeå C (15 min)

**Leg 2:**
Bus 100 (mot Skellefteå) departs 09:20
Arrives Skellefteå busstation 11:45

Total: 3h | 1 change
```

### 步行段详情

**始终显示步行详情：**
- 行走距离（以米为单位）
- 包括步行时间（估计每分钟约 100 米）

### 显示多个行程选项

在展示行程选项时，要明确显示每个选项的出发和到达时间：

```
I found 3 options for you:

**Option 1 - Leave now (09:00)** Recommended
Walk 5 min -> Bus 1 at 09:07 -> arrives 09:25
Total: 25 min

**Option 2 - Leave in 15m (09:15)**
Walk 5 min -> Bus 1 at 09:22 -> arrives 09:40
Total: 25 min

**Option 3 - Leave in 30m (09:30)**
Walk 5 min -> Bus 8 at 09:37 -> arrives 09:48
Total: 18 min | Faster but later departure

Which works best for you?
```

---

## LLM 工作流程：如何规划行程

当用户请求行程时，请按照以下步骤操作：

### 第 1 步：理解用户的时间需求

解析用户的具体需求：
- “How do I get to...” → 立即出行
- “I need to be there at 18:00” → 使用 `arrive` 模式
- “Sometime around 15:00” → 查询 14:30 的行程
- “In about an hour” → 根据当前时间计算行程

### 第 2 步：分别搜索起点和终点

分别搜索起点和终点的信息：

```bash
./search-location.sh "Vasaplan?"
./search-location.sh "Universitetet?"
```

### 第 3 步：验证搜索结果

**仔细检查每个结果：**
1. **名称是否匹配？** - 如果名称与用户请求一致，则继续下一步。
2. **返回多个结果？** - 脚本最多显示 10 个结果。如果第一个结果不正确，请让用户确认。
3. **名称差异较大？** - 如果用户查询的是“university”，而结果显示的是“Umeå Universitet”，请确认用户的需求。
4. **未找到结果？** - 尝试其他搜索策略。

### 第 4 步：处理模糊或失败的搜索

**当搜索结果不匹配或模糊时，询问用户以获取更多信息：**

```
I searched for "centrum" and found multiple locations:
1. Umeå Vasaplan (central bus hub)
2. Skellefteå centrum
3. Lycksele centrum

Which one did you mean?
```

**当未找到结果时，尝试以下方法：**

1. **使用城市名称搜索：**
   ```bash
   # If "Storgatan 10" fails, try:
   ./search-location.sh "Storgatan 10, Umeå?"
   ```

2. **尝试常见的变体：**
   ```bash
   # "Universitetet" -> "Umeå universitet"
   # "Sjukhuset" -> "NUS" or "Norrlands universitetssjukhus"
   ```

3. **使用模糊搜索（添加 ?）：**
   ```bash
   ./search-location.sh "univ?"
   ```

### 第 5 步：执行行程搜索

确认两个地点的 ID 后：

```bash
./journey.sh <from-id> <to-id> [datetime] [mode]
```

### 第 6 步：格式化响应

使用上述格式规范清晰地展示结果。**始终使用工具输出的准确数据，不要估算或猜测。**

---

## 查询格式规则

**搜索 API 对格式非常敏感，请遵循以下规则：**

### 乌梅奥的常见车站名称

| 用户输入 | 搜索内容 |
|-----------|------------|
| "Vasaplan", "centrum" | `"Umeå Vasaplan?"` |
| "Universitetet", "uni" | `"Umeå universitet?"` |
| "NUS", "sjukhuset" | `"Norrlands universitetssjukhus?"` |
| "Ikea" | `"IKEA Umeå?"` |
| "Flygplatsen" | `"Umeå Airport?"` |
| "Järnvägsstationen", "tåget" | `"Umeå centralstation?"` |

### 区域目的地

| 目的地 | 搜索内容 |
|-------------|------------|
| Skellefteå | `"Skellefteå busstation?"` |
| Lycksele | `"Lycksele busstation?"` |
| Vindeln | `"Vindeln station?"` |
| Robertsfors | `"Robertsfors centrum?"` |
| Holmsund | `"Holmsund centrum?"` |

### 街道地址

为提高搜索准确性，请包含城市名称：

```bash
./search-location.sh "Storgatan 25, Umeå?"
./search-location.sh "Kungsgatan 10, Skellefteå?"
```

---

## 示例

### 示例 1：立即出行（乌梅奥本地公交）

用户：**如何从 Vasaplan 去 NUS？**

```bash
./search-location.sh "Umeå Vasaplan"
./search-location.sh "NUS?"
./journey.sh 740020116 740023840
```

**响应：**
```
**Leave now** from Vasaplan

**Vasaplan** -> **Universitetssjukhuset**
Bus 8 (mot Lyktvägen) departs 11:01
Arrives 11:06

Total: 5 min | Direct, no changes
```

### 示例 2：区域行程**

用户：**明天 8 点需要从乌梅奥去 Skellefteå**

```bash
./search-location.sh "Umeå Vasaplan"
./search-location.sh "Skellefteå?"
./journey.sh 740020116 740000053 "tomorrow 08:00"
```

**响应：**
```
**Depart tomorrow at 08:04** from Vasaplan

Walk 766m to Umeå Busstation (~11 min)

**Umeå Busstation** -> **Skellefteå busstation**
Bus 20 (Länstrafik mot Haparanda) departs 08:15
Arrives 10:40 at Skellefteå busstation

Total: 2h 36min | Direct (with walk)
```

### 示例 3：必须在指定时间到达

用户：**明天 8 点前必须到达 NUS**

```bash
./search-location.sh "Umeå Vasaplan"
./search-location.sh "NUS?"
./journey.sh 740020116 740023840 "tomorrow 08:00" arrive
```

**响应：**
```
**Arrive by 08:00** at NUS

**Vasaplan** -> **Universitetssjukhuset**
Bus 9 departs **07:51**
Arrives **07:56** - 4 min buffer

Leave Vasaplan by 07:51 to arrive on time!
```

### 示例 4：从地址/坐标出发

用户：**我在乌梅奥的 Storgatan 50，如何去 IKEA？**

```bash
./search-location.sh "Storgatan 50, Umeå?"
# If no result, use coordinates
./journey.sh "63.826#20.263" 740066123
```

---

## 时间格式

所有时间均为瑞典当地时间（CET/CEST）。

| 格式 | 例子 | 含义 |
|--------|---------|---------|
| _(empty)_ | | 立即出行 |
| `HH:MM` | `"08:30"` | 今天 08:30 |
| `tomorrow HH:MM` | `明天 09:00` | 明天 09:00 |
| `YYYY-MM-DD HH:MM` | `"2026-01-28 14:00"` | 具体日期 |

---

## 输出格式

### 行程选项（原始工具输出）

```
==============================================================
OPTION 1: Vasaplan -> Universitetet
==============================================================
Date:    2026-01-28
Depart:  09:04
Arrive:  09:12
Changes: 0

LEGS:
  -> BUS Länstrafik - Buss 1
    From: 09:04 Vasaplan (Umeå kn)
    To:   09:12 Universitetet (Umeå kn)
    Direction: mot Mariehem
```

### 交通类型

| 类型 | 说明 |
|------|-------------|
| `BUS` | Tabussen/Ultra/Länstrafik 公交 |
| `JLT` | 区域公交（Länstrafik） |
| `JRE` | 区域火车 |
| `WALK` | 步行段 |

### 西约特堡省的公交运营商

| 运营商 | 说明 |
|----------|-------------|
| Länstrafiken Västerbotten | 区域和本地公交 |
| Ultra | 乌梅奥本地公交（属于 Länstrafiken） |
| SJ | 长途火车 |
| Norrtåg | 区域火车 |

---

## 错误处理

### “未找到地点”

搜索未返回任何结果。

**应对策略：**
1. 检查拼写（瑞典语中的 å, ä, ö）
2. 尝试使用城市名称后缀
3. 使用模糊搜索（添加 ?）
4. 尝试其他常见名称
5. 询问用户以获取更多信息

### “未找到行程”

没有可用的路线。

**应对策略：**
1. 检查该时间段是否有服务（夜间服务可能受限）
2. 尝试不同的出发时间
3. 建议附近的替代站点
4. 请注意某些区域线路的班次较少

### 常见问题

| 问题 | 解决方案 |
|-------|----------|
| “Vasaplan” 返回多个结果 | 使用 “Umeå Vasaplan” |
| 车站未找到 | 尝试使用模糊搜索（添加 ?） |
| 没有夜间路线 | Ultra 的夜间服务有限 |
| 等待时间过长 | 区域线路可能每小时仅有一班 |

---

## 快速参考

### 乌梅奥的热门车站（Ultra）

| 车站 | ID | 说明 |
|------|-----|-------|
| Vasaplan | 740020116 | 中心枢纽 |
| Universitetssjukhuset (NUS) | 740023840 | 医院 |
| Universum | 740026881 | 大学区 |
| Umeå Busstation | - | 区域公交发车点 |
| Västerslätt Centrum | 740045407 | 西部郊区 |

### 主要区域车站

| 车站 | ID | 说明 |
|------|-----|-------|
| Skellefteå busstation | 740000053 | 区域枢纽 |
| Lycksele busstation | - | 内陆枢纽 |
| Vindeln station | - | 火车连接点 |
| Robertsfors centrum | - | 沿海路线 |

---

## API 详情（用于脚本开发）

此功能使用 Trafiklab 的 ResRobot API v2.1。

**基础 URL：** `https://api.resrobot.se/v2.1/`

**端点：**
- 车站查询：`/location.name`
- 行程规划：`/trip`

**关键参数：**
- `accessId` - API 密钥（必需）
- `format` - json 或 xml
- `originId` / `destId` - 车站 ID
- `date` / `time` - 行程日期/时间
- `searchForArrival` - 1 表示“必须在...时间到达”的搜索

**获取 API 密钥：** 在 https://developer.trafiklab.se 注册

---

## 关于西约特堡省的交通信息

### Ultra（乌梅奥本地公交）
- 乌梅奥市中心的班次频繁
- 1-9 路线最为常见
- 周末有夜间公交（N 系列）
- 应用程序提供实时信息

### Länstrafiken（区域公交）
- 100 路线：乌梅奥 - Skellefteå（班次频繁）
- 12/20 路线：沿海路线
- 30-49 路线：内陆路线
- 班次频率因路线而异

### 用户提示
- Vasaplan 是 Ultra 和区域公交的主要枢纽
- 许多区域公交从 Vasaplan 出发，而非火车站
- 火车站（Umeå C）与公交车站分开
- IKEA 和 Avion 地点有便捷的公交连接

---

## 何时需要询问用户以获取更多信息

**在以下情况下务必询问用户：**

1. **搜索未返回结果时：**
   - “我找不到 [地点]。您能提供更多信息吗？”
2. **返回多个结果时：**
   - “找到了多个名为 '[query]' 的车站：[结果列表]。请选择其中一个？”
3. **结果名称与查询不符时：**
   - “您查询的是 '[user query]'，但我找到的是 '[result name]'。这是正确的吗？”
4. **用户请求不明确时：**
   - “您想从乌梅奥的哪个地方出发？是 Vasaplan（中心），还是其他地点？”
5. **时间不明确时：**
   - “您想在什么时候出行？是现在，还是特定时间？”
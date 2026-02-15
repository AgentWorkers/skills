---
name: snow-report
description: 获取全球任何山间度假村的雪况、天气预报和滑雪报告。当被问及雪量、雪质或山区天气时，可以使用该服务。通过 OpenSnow 支持超过 1000 个度假村的查询。用户可以设置喜欢的度假村以便快速查看相关信息。同时支持使用 SnowTick 的 4 个字母代码（如 JHMR、TARG、MMTH）进行快速查询。
---

# 雪情报告

您可以从 OpenSnow 获取全球任何滑雪场的实时雪况信息。

## SnowTick — 山地代码

这些由 4 个字母组成的代码可用于快速查询滑雪场信息，类似于股票代码：

| 代码 | 滑雪场名称 |
|--------|--------|
| `JHMR` | 杰克逊霍尔（Jackson Hole） |
| `TARG` | 格兰德塔吉（Grand Targhee） |
| `MMTH` | 猛犸（Mammoth） |
| `BIRD` | 斯诺伯德（Snowbird） |
| `ALTA` | 阿尔塔（Alta） |
| `BOAT` | 斯蒂姆博特（Steamboat） |
| `WHIS` | 惠斯勒（Whistler） |

完整代码列表请参见 `references/resorts.md`。您可以在需要使用滑雪场名称的地方使用这些代码。

## 命令

| 用户指令 | 动作 |
|-----------|--------|
| "snowtick" | 显示所有收藏滑雪场的实时雪况 |
| "snow report" / "雪况如何" | 从用户配置中获取默认滑雪场的雪况 |
| "snow at Mammoth" / "Jackson snow" | 获取特定滑雪场的雪况 |
| "JHMR" / "TARG at" | 根据代码获取滑雪场的雪况 |
| "compare Jackson and Targhee" | 比较两个滑雪场的雪况 |
| "compare JHMR TARG MMTH" | 按代码比较三个滑雪场的雪况 |
| "powder alert" / "哪里在下雪" | 查看所有收藏滑雪场的天气预报 |

## 用户配置

用户设置请参见 `memory/snow-preferences.md`：

```markdown
# Snow Preferences

## Default Mountain
JHMR

## Favorites
- JHMR (Jackson Hole)
- TARG (Grand Targhee)
- MMTH (Mammoth)
- ALTA (Alta)

## Report Style
- compact (default) | detailed
- skip: parking
```

您可以使用代码或简称来表示滑雪场名称。如果配置文件不存在，系统会询问用户常用的滑雪场名称并自动创建该文件。

## 解析代码

当用户提供代码（4 个大写字母）时：
1. 在 `references/resorts.md` 中查找对应的滑雪场名称。
2. 获取该滑雪场的简称。
3. 使用该简称作为 OpenSnow 的 URL。

示例：`JHMR` → `jacksonhole` → `opensnow.com/location/jacksonhole/snow-summary`

## 快速使用方法

### SnowTick 命令
```
1. Read user favorites from memory/snow-preferences.md
2. Open all favorite resort tabs in parallel
3. Snapshot each tab for snow data
4. Extract: base depth, 5-day forecast, current conditions
5. Format as ticker tape with best bet arrow
6. Close all tabs
```

### 单个滑雪场
```
1. browser action=open targetUrl=https://opensnow.com/location/{slug}/snow-summary
2. browser action=snapshot compact=true
3. Extract key data, close tab
```

### 多个滑雪场比较
```
1. Open all resort tabs in parallel (browser action=open for each)
2. Snapshot all tabs
3. Extract and format comparison table
4. Close all tabs
```

## 数据提取

从 OpenSnow 提取的信息包括：

### 雪情概要
- **过去 24 小时**：实际降雪量及时间戳
- **未来 1-5 天**：天气预报
- **未来 6-10 天**：长期天气预报
- **未来 11-15 天**：长期天气趋势

### 当前天气（“现在”）
- 温度及体感温度
- 风速、风向、阵风
- 天气状况（晴朗、下雪等）

### 当地专家信息（每日雪况）
- 专家姓名
- 天气预报说明

### 人工智能概要
- 简洁的天气状况总结

## 输出格式

### SnowTick（收藏滑雪场仪表盘）
```
📈 SnowTick — {date}

JHMR  12"  ▲ 6"   ❄️ snowing
FISH   8"  ▲ 2"   ☀️ clear  
SGAR  24"  ▲ 12"  ❄️ snowing ←
BALD  36"  ▲ 8"   🌨️ flurries
BRDG   6"  ▲ 0"   ☀️ clear
ROCK   2"  — 0"   ☀️ clear

▲ = next 5 days | ← = best bet
```

列：代码 | 积雪深度 | 5 天天气预报 | 当前天气状况

### 简化格式（默认）
```
🏔️ {Resort} [{TICK}] — {date}

**Snow:** {24hr}" | Next 5d: {forecast}"
**Now:** {temp}°F, {conditions}, wind {speed} mph
**Daily Snow:** {1 sentence summary}
```

### 详细格式
```
🏔️ {Resort} [{TICK}] — {date}

**Now:** {temp}°F ({feels}°F), {conditions}, wind {speed} mph {dir}

| Period | Snow |
|--------|------|
| Last 24hr | X" |
| Next 5 days | X" |
| Next 6-10 days | X" |
| Next 11-15 days | X" |

**Daily Snow ({expert}):** {full summary}

**AI Overview:** {summary}
```

### 对比表格
```
📊 Snow Comparison — {date}

| Ticker | Resort | 24hr | Next 5d | Next 10d | Temp |
|--------|--------|------|---------|----------|------|
| JHMR | Jackson Hole | 0" | 0" | 8" | 11°F |
| TARG | Grand Targhee | 0" | 2" | 12" | 8°F |
| ALTA | Alta | 0" | 1" | 6" | 15°F |

**Best Bet:** TARG — most snow coming
```

### 粉雪警报
```
🚨 Powder Alert — {date}

Checking your favorites for incoming snow...

| Ticker | Resort | Next 5d | Next 10d |
|--------|--------|---------|----------|
| TARG | Grand Targhee | 6" | 18" | ← Best
| JHMR | Jackson Hole | 0" | 8" |
| ALTA | Alta | 2" | 10" |

**Verdict:** TARG looking best for next week
```

## 滑雪场简称及代码

完整代码列表请参见 `references/resorts.md`。

**快速参考：**
| 地区 | 代码 |
|--------|---------|
| 怀俄明州 | `JHMR` `TARG` `SNWK` |
| 犹他州 | `ALTA` `BIRD` `PCMR` `DEER` |
| 科罗拉多州 | `VAIL` `AJAX` `TELL` `BOAT` |
| 加利福尼亚州 | `MMTH` `PALI` `KIRK` `HVLY` |
| 蒙大拿州 | `BSKY` `FISH` `BRDG` |
| 不列颠哥伦比亚省 | `WHIS` `RVLK` |
| 日本 | `NSKO` `HAKU` |

对于未列出的滑雪场，可以在 opensnow.com 上搜索并获取其简称，然后将其添加到配置文件中。

## 首次使用说明

如果用户首次请求雪情报告且没有配置文件：
1. 询问用户常用的滑雪场名称，并将其设置为默认滑雪场。
2. 生成 `memory/snow-preferences.md` 文件。
3. 询问用户是否需要添加其他用于比较的滑雪场。
4. 为该用户获取首次雪情报告。

## 注意事项：
- OpenSnow 使用 JavaScript 渲染数据，需要浏览器支持。
- 数据会随时更新，早晨的预报最为准确。
- 11-15 天的长期天气预报可能需要付费才能查看。
- 如需了解滑雪场的具体信息（如缆车、雪道状况），请访问滑雪场的官方网站。
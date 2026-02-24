---
name: astroapi-skill
description: **占星API：** 提供生成出生星盘、星盘分析、合成星盘、行星运行轨迹、太阳/月亮回归点、行星位置变化、方位图、行星宫位、相位分析、月亮指标、星座运势报告、SVG格式的星盘图像、塔罗牌解读、 numerology（数字命理学）、吠陀占星、中国占星、人类设计学（human design）、卡巴拉（Kabbalah）、占星地图（astrocartography）、日食/月食预测、手相术以及固定星（fixed stars）等功能。当用户询问关于出生星盘、星座运势、星座兼容性、行星位置、月亮相位、行星运行轨迹、占星计算、塔罗牌解读、 numerology 或任何与占星相关的主题时，均可使用该API。
  Astrology API: generate natal charts, synastry, composite, transits, solar/lunar
  returns, progressions, directions, planetary positions, house cusps, aspects, lunar
  metrics, horoscopes, analysis reports, SVG/render charts, tarot, numerology, Vedic,
  Chinese astrology, human design, kabbalah, astrocartography, eclipses, palmistry,
  and fixed stars. Use when user asks about birth charts, horoscopes, zodiac signs,
  compatibility, planetary positions, moon phases, transits, astrological calculations,
  tarot readings, numerology, or any esoteric/astrological topic.
license: MIT
compatibility: Requires curl
allowed-tools: Bash(curl:*) Read
version: 1.0.0
metadata:
  openclaw:
    emoji: ⭐
    homepage: https://github.com/astro-api/astroapi-skill
    requires:
      bins: ['curl']
      env: ['ASTROLOGY_API_KEY']
    primaryEnv: ASTROLOGY_API_KEY
---
# 占星API技能

## 使用场景

当用户询问以下内容时，可以使用此技能：
- 出生星盘、本命盘、星座运势
- 星座兼容性、星象分析、关系解读
- 行星位置、运行轨迹、相位关系
- 月相、月亮指标
- 太阳/月亮的回归点、运行轨迹、方向
- 塔罗牌解读、牌阵排列、含义分析
- 数字命理学（核心数字、兼容性分析）
- 吠陀占星（昆迪利（Kundli）、体质类型（Doshas）、星象周期（Dashas）、潘查昂（Panchang）
- 中国占星（八字命理、命宫、风水）
- 人体设计（身体结构图、性格类型、能量通道）
- 卡巴拉（生命之树、守护天使、吉玛特里亚数）
- 占星地图学（迁移建议、能量区域）
- 固定星的位置及组合
- 日食/月食（预测、对个人命运的影响）
- 手相分析
- 每日/每周/每月/每年的星座运势
- 职业、健康、精神状态、心理分析
- 星盘可视化（SVG或PNG图像）

## 先决条件

在调用API之前，请确认：
1. 环境变量 `$ASTROLOGY_API_KEY` 已设置
2. 系统路径中包含 `curl` 命令工具

如果API密钥缺失，请让用户先设置它：

```
export ASTROLOGY_API_KEY="your_token_here"
```

## 工作原理

1. 根据用户请求类型收集所需数据：
   - 对于本命盘/个人占星：姓名、出生日期（年、月、日）、出生时间（小时、分钟）、出生城市及国家代码（两位字母的ISO代码）
   - 对于星象兼容性分析：需要两人的出生信息
   - 对于行星运行轨迹：需要本命星盘数据及运行日期/时间
   - 对于按星座划分的运势：仅需提供星座名称
   - 对于塔罗牌占星：需要占卜问题或牌阵类型
   - 对于数字命理学：需要全名及出生日期

2. 使用 `{baseDir}/scripts/astro-api.sh` 脚本调用API：

   ```
   bash {baseDir}/scripts/astro-api.sh POST /api/v3/charts/natal '{ ... }'
   ```

3. 以用户易于理解的格式呈现结果，并突出关键信息。

## API调用模式

### 本命盘（最常见请求）

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/charts/natal '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "options": {
    "house_system": "P",
    "zodiac_type": "Tropic",
    "language": "EN"
  }
}'
```

### 星象兼容性分析

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/charts/synastry '{
  "subject": {
    "name": "Person A",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "partner": {
    "name": "Person B",
    "year": 1992, "month": 7, "day": 20,
    "hour": 9, "minute": 0, "second": 0,
    "city": "London", "country_code": "GB"
  },
  "options": {"house_system": "P", "zodiac_type": "Tropic", "language": "EN"}
}'
```

### 行星运行轨迹快照

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/charts/transit '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "transit": {
    "year": 2026, "month": 2, "day": 12,
    "hour": 12, "minute": 0, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "options": {"house_system": "P", "zodiac_type": "Tropic", "language": "EN"}
}'
```

### 当前天象数据（无需参数）

```bash
bash {baseDir}/scripts/astro-api.sh GET /api/v3/data/now
```

### 行星位置

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/data/positions '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "options": {"house_system": "P", "zodiac_type": "Tropic"}
}'
```

### 月亮指标

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/data/lunar-metrics '{
  "subject": {
    "name": "now",
    "year": 2026, "month": 2, "day": 12,
    "hour": 12, "minute": 0, "second": 0,
    "city": "New York", "country_code": "US"
  }
}'
```

### 按星座划分的每日运势

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/horoscope/sign/daily '{
  "sign": "aries",
  "language": "EN"
}'
```

### 个人每日运势

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/horoscope/personal/daily '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "language": "EN"
}'
```

### 本命星盘分析报告（人工智能生成）

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/analysis/natal-report '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "options": {"house_system": "P", "zodiac_type": "Tropic", "language": "EN"}
}'
```

### 星盘可视化（SVG格式）

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/svg/natal '{
  "subject": {
    "name": "John",
    "year": 1990, "month": 3, "day": 15,
    "hour": 14, "minute": 30, "second": 0,
    "city": "New York", "country_code": "US"
  },
  "options": {"house_system": "P", "zodiac_type": "Tropic"}
}'
```

### 塔罗牌抽牌

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/tarot/cards/draw '{
  "count": 3
}'
```

### 数字命理学核心数字

```bash
bash {baseDir}/scripts/astro-api.sh POST /api/v3/numerology/core-numbers '{
  "full_name": "John Smith",
  "birth_date": "1990-03-15"
}'
```

> **完整API端点参考：** 查阅 `{baseDir}/references/api-endpoints.md`，了解所有190多个API端点的详细参数。

## 默认设置

当用户未指定偏好时，使用以下默认值：
- **宫位系统：** `P`（Placidus）——西方占星中最常用的系统
- **星座类型：** `Tropic`（热带占星法）——西方占星的标准类型
- **语言：** `EN`（英语）——可根据用户语言进行切换
- **占星传统：** `universal`——覆盖最广泛的占星流派

## 结果展示方式

在向用户展示结果时，请遵循以下规则：
1. 首先介绍重要信息：太阳星座、月亮星座、上升点（Ascendant）
2. 使用通俗易懂的语言解释占星术语
3. 在显示多颗行星的位置时，使用表格格式
4. 突出显著的相位关系（如合相、冲相、三角相、六合相）
5. 对于兼容性分析：先提供总体评分或总结
6. 对于星座运势：以自然的语言呈现结果，避免直接输出原始JSON数据
7. 对于星盘图像（SVG格式）：将图像保存到文件中，并告知用户保存位置

## 特殊情况处理：
- **出生时间未知**：使用中午12:00作为默认时间；此时宫位和月亮度数的准确性可能较低
- **城市信息未找到**：请求用户的纬度/经度信息；使用 `latitude` 和 `longitude` 字段代替 `city`/`country_code`
- **API错误（如400/422代码）**：解析错误信息并向用户说明问题原因（例如日期格式错误、缺少必要字段）
- **响应数据量较大**：对于分析报告，仅总结关键内容，避免显示全部数据
- **语言支持**：API支持英语（EN）、俄语（RU）、法语（FR）、德语（DE）、西班牙语（ES）、意大利语（IT）等多种语言；尽可能匹配用户的语言设置
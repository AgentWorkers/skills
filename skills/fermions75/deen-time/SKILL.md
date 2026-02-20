---
name: deen-time
description: 获取全球任何地点的每日伊斯兰教祈祷（Salah）时间、开斋（Iftar）和封斋前（Suhoor）时间安排。支持15种以上的计算方法、伊斯兰历（Hijri dates）以及斋月日历（Ramadan calendars）。
metadata:
  openclaw:
    requires:
      bins:
        - curl
      env: []
    homepage: https://aladhan.com/prayer-times-api
user-invokable: true
disable-model-invocation: false
---
# 伊斯兰祈祷时间助手

这是一个每日使用的伊斯兰祈祷时间工具，能够为全球任何城市或坐标提供准确的祈祷时间（晨礼、日出时间、正午礼、下午礼、昏礼、宵礼）。在斋月期间，还会提供苏胡尔（黎明前的餐食）和开斋的时间安排，并附有完整的月度日历。

## 适用场景

当用户询问以下内容时，可以使用此工具：
- 特定地点的祈祷时间
- 苏胡尔或开斋的时间
- 斋月的日程安排
- 何时开斋或开始斋戒
- 晨礼、正午礼、下午礼、昏礼、宵礼的时间
- 伊斯兰祈祷的时间表

## 工作原理

该工具使用 **Aladhan Prayer Times API**（`https://aladhan.com/prayer-times-api`），这是一个免费且可靠的公共API，无需进行身份验证。

### 按城市获取祈祷时间

```bash
curl -L "https://api.aladhan.com/v1/timingsByCity?city={CITY}&country={COUNTRY}&method={METHOD}"
```

请将 `{CITY}`、`{COUNTRY}` 和 `{METHOD}` 替换为实际值。需要对空格进行 URL 编码（例如：`New%20York`）。使用 `-L` 参数来处理可能的重定向。

### 按坐标获取祈祷时间

```bash
curl -L "https://api.aladhan.com/v1/timings/{DD-MM-YYYY}?latitude={LAT}&longitude={LNG}&method={METHOD}"
```

当用户提供经纬度信息，或者城市名称不明确时，可以使用此方法。

### 获取完整的月度日历

```bash
curl -L "https://api.aladhan.com/v1/calendarByCity/{YEAR}/{MONTH}?city={CITY}&country={COUNTRY}&method={METHOD}"
```

用于获取斋月的日程安排。`{MONTH}` 表示公历月份（1-12）。

## 计算方法

`method` 参数用于控制祈祷时间的计算方式。根据用户的地理位置选择最合适的方法：

| 方法 | 组织 | 适用地区 |
|--------|-------------|----------|
| 1 | 卡拉奇伊斯兰科学大学 | 巴基斯坦、孟加拉国、印度 |
| 2 | 北美伊斯兰协会（ISNA） | 北美 |
| 3 | 穆斯林世界联盟（MWL） | 欧洲、远东 |
| 4 | 麦加乌姆·阿尔-库拉大学 | 沙特阿拉伯、海湾地区 |
| 5 | 埃及测绘总局 | 非洲、叙利亚、黎巴嫩 |
| 7 | 德黑兰大学地球物理研究所 | 伊朗 |
| 8 | 海湾地区 | 阿联酋、科威特、卡塔尔 |
| 9 | 科威特 | 科威特 |
| 10 | 卡塔尔 | 卡塔尔 |
| 11 | 新加坡伊斯兰宗教理事会 | 新加坡 |
| 12 | 法国伊斯兰联盟组织 | 法国 |
| 13 | 土耳其宗教事务局 | 土耳其 |
| 14 | 俄罗斯穆斯林精神事务管理局 | 俄罗斯 |
| 15 | 全球望月委员会 | 全球（基于望月确定日期） |

**默认设置**：北美地区使用方法 2，沙特/海湾地区使用方法 4，欧洲使用方法 3，非洲使用方法 5，土耳其使用方法 13。如果用户未指定偏好，系统会根据用户的地理位置自动选择合适的方法。

## API 响应结构

API 返回 JSON 数据。需要提取的关键字段如下：

```json
{
  "data": {
    "timings": {
      "Fajr": "05:12",
      "Sunrise": "06:30",
      "Dhuhr": "12:15",
      "Asr": "15:30",
      "Maghrib": "18:00",
      "Isha": "19:20",
      "Imsak": "05:02"
    },
    "date": {
      "readable": "19 Feb 2026",
      "hijri": {
        "date": "02-09-1447",
        "month": { "number": 9, "en": "Ramadan" },
        "year": "1447"
      }
    }
  }
}
```

对于日历端点，`data` 是一个包含每日祈祷时间信息的对象数组。

## 结果展示方式

### 每日祈祷时间

以清晰的表格形式展示：

```
Prayer Times for {City}, {Country}
Date: {Gregorian Date} | {Hijri Date}

| Prayer   | Time   |
|----------|--------|
| Fajr     | 05:12  |
| Sunrise  | 06:30  |
| Dhuhr    | 12:15  |
| Asr      | 15:30  |
| Maghrib  | 18:00  |
| Isha     | 19:20  |

Suhoor: Stop eating before 05:12 (Fajr). Recommended: 05:02 (Imsak).
Iftar: Break fast at 18:00 (Maghrib).
```

### 斋月月度日程

对于按月度请求的情况，以简化的表格形式展示：

```
Ramadan Schedule for {City} — {Year}

| Day | Date       | Suhoor (Imsak) | Fajr  | Iftar (Maghrib) |
|-----|------------|-----------------|-------|-----------------|
| 1   | 17 Feb     | 05:02           | 05:12 | 17:45           |
| 2   | 18 Feb     | 05:01           | 05:11 | 17:46           |
| ... | ...        | ...             | ...   | ...             |
```

### 重要提示

- 苏胡尔必须在晨礼之前完成。建议在晨礼前 10 分钟（即伊姆萨克时间）前完成苏胡尔。
- 开斋时间是在昏礼（日落时）。
- 所有时间均以请求地点的 **本地时区** 为准。
- 如果用户未指定地点，请询问他们的城市和国家。
- 如果用户未指定日期，系统将使用当天的日期。

## 使用示例

**用户**：“伦敦今天的祈祷时间是什么？”
→ 调用：`curl -L "https://api.aladhan.com/v1/timingsByCity?city=London&country=United%20Kingdom&method=3"`
→ 以格式化的表格形式显示所有祈祷时间，包括公历日期和伊斯兰历日期。

**用户**：“迪拜的开斋时间是什么？”
→ 调用：`curl -L "https://api.aladhan.com/v1/timingsByCity?city=Dubai&country=United%20Arab%20Emirates&method=4"`
→ 将昏礼时间标记为开斋时间。

**用户**：“请提供伊斯坦布尔的斋月日程安排。”
→ 确定当前年份斋月对应的公历月份。
→ 调用：`curl -L "https://api.aladhan.com/v1/calenderByCity/2026/2?city=Istanbul&country=Turkey&method=13"`（如果斋月跨越两个月，则包括三月）
→ 过滤出斋月期间的日期（检查伊斯兰历月份是否为 9 月），并显示苏胡尔/开斋时间表。

**用户**：“纽约的苏胡尔时间是多少？”
→ 调用：`curl -L "https://api.aladhan.com/v1/timingsByCity?city=New%20York&country=United%20States&method=2"`
→ 显示伊姆萨克时间和晨礼时间。建议在伊姆萨克时间（晨礼前 10 分钟）前停止进食。

**用户**：“坐标为 21.4225, 39.8262 的地点的祈祷时间是多少？”
→ 调用：`curl -L "https://api.aladhan.com/v1/timings/19-02-2026?latitude=21.4225&longitude=39.8262&method=4"`
→ 显示该地点的完整祈祷时间（由于这些坐标对应麦加，因此使用乌姆·阿尔-库拉大学的方法进行计算）。

## 隐私与数据管理

该工具通过 **HTTPS** 向 [Aladhan Prayer Times API](https://aladhan.com/prayer-times-api) 发送 **只读请求**。这是一个知名的免费公共伊斯兰祈祷时间服务：

- **发送的数据**：仅包含用户提供的城市/国家名称或坐标，以及所选的计算方法编号。不会传输任何个人数据、凭证或设备信息。
- **接收的数据**：请求地点和日期的祈祷时间（以 JSON 格式返回）。不会进行数据跟踪、设置cookies 或用户画像。
- **无需认证**：API 不需要 API 密钥、令牌或账户信息。
- **无数据存储**：该工具不会将数据写入磁盘、存储用户信息，也不会在请求之间保留任何状态。
- **单一域名**：所有网络请求仅通过 HTTPS 发送到 `api.aladhan.com`，不会访问其他外部端点。
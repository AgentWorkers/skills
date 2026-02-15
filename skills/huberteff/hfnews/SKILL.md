---
name: hfnews
description: 从多个来源获取并过滤新闻，支持停用词（stopwords）和黑名单（blacklist）功能。根据Hubert的兴趣（IT、网络安全）进行定制，过滤掉与政治或体育相关的新闻内容。
---

# 新闻采集器

## 使用方法

```bash
# All categories
news

# Specific category
news Allgemeines
news IT
news Cybersecurity
```

## 输出格式

- **简单列表格式：**
  ```
Allgemeines:
- Titel URL
- Titel URL
- Titel URL
- Titel URL
- Titel URL

IT:
- Titel URL
- Titel URL
- Titel URL
- Titel URL
- Titel URL

Cybersecurity:
- Titel URL
- Titel URL
- Titel URL
- Titel URL
- Titel URL
```

## 过滤词（需从新闻中排除的关键词）：
- Sport（体育）
- Trump/USA（特朗普/美国）
- SPD（德国社会民主党）
- Iran（伊朗）
- Bürgergeld（政府发放的救济金）
- Mietreform（租金改革）
- Mieterschutz（租客权益保护）
- Regenpause（降雨暂停）
- Ukraine（乌克兰）
- Putin（普京）
- Epstein（爱泼斯坦）
- Bilder des Tages（当日图片）
- Karrierefrage（职业发展相关问题）
- Stellenmarkt（就业市场）
- Jobs（工作机会）

## 分类

### 通用新闻
- Tagesschau：https://www.tagesschau.de/
- FAZ：https://www.faz.net/aktuell/
- WiWo：https://www.wiwo.de/
- Süddeutsche：https://www.sueddeutsche.de/
- Spiegel：https://www.spiegel.de/
- Mittelbayerische：https://www.mittelbayerische.de/lokales/stadt-regensburg

### 科技领域
- Heise：https://www.heise.de/
- Golem：https://www.golem.de/
- Slashdot：https://slashdot.org/

### 网络安全
- The Hacker News：https://thehackernews.com/
- BleepingComputer：https://www.bleepingcomputer.com/
- Logbuch Netzpolitik：https://logbuch-netzpolitik.de/
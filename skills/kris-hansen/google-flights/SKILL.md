---
name: google-flights
description: 在 Google Flights 中搜索航班价格和可用性。当用户询问航班价格、搜索航班、比较机票价格或规划城市间的航空旅行时，可以使用此功能。
---
# 航班查询

提供两种查询模式：**快速模式**（仅显示价格，查询速度快）和**详细模式**（包含航空公司、航班时间、途经城市等信息，需通过浏览器查询）。

## 快速模式（默认模式）

使用 `scripts/search.py` 进行快速价格查询：

```bash
./scripts/search.py YYC LAX "2026-03-15"
./scripts/search.py YYC LAX tomorrow --return "next friday"
./scripts/search.py JFK LHR "Mar 1" --adults 2 --seat business
```

**查询结果：** 价格走势（最低/平均/最高）、价格区间、航班数量、Google Flights 链接。

**可选参数：**
- `--return`, `-r` — 往返航班的返回日期
- `--adults`, `-a` — 成年人数（默认值：1）
- `--children`, `-c` — 儿童人数
- `--seat`, `-s` — 航班座位类型：经济舱、高级经济舱、商务舱、头等舱
- `--json` — 以 JSON 格式输出结果

## 详细模式（浏览器模式）

当用户需要查询具体的航空公司、航班时间或航班详情时，可使用浏览器自动化工具进行查询：

```
1. browser open (profile: clawd, targetUrl: google flights URL)
2. browser snapshot (wait for "results returned" alert)
3. Parse link descriptions for flight data
4. browser close
```

### URL 格式

```
# One-way
https://www.google.com/travel/flights?q=Flights%20from%20{FROM}%20to%20{TO}%20on%20{DATE}%20one%20way&hl=en

# Round-trip
https://www.google.com/travel/flights?q=Flights%20from%20{FROM}%20to%20{TO}%20on%20{DATE}%20returning%20{RETURN}&hl=en
```

### 数据解析示例

航班信息存储在链接元素中：
```
"From 737 Canadian dollars... flight with Air Canada. Leaves... at 6:25 AM... arrives at 11:48 AM... Total duration 6 hr 23 min. 1 stop... Layover 1 hr 30 min at YVR..."
```

### 详细模式查询结果

```
✈️ YYC → LAX | Fri Feb 20

1. Air Canada | 6:25 AM → 11:48 AM | 6h 23m | 1 stop (YVR) | CA$737
2. United | 6:15 AM → 11:31 AM | 6h 16m | 1 stop (DEN) | CA$744
3. WestJet | 9:00 AM → 11:27 AM | 3h 27m | Nonstop | CA$1,047 ⭐

🔗 Book on Google Flights: [link]
```

## 快速模式的设置

快速模式需要安装 `fast-flights` 插件。请安装一次：

```bash
cd skills/google-flights
uv venv && source .venv/bin/activate && uv pip install fast-flights
```

## 如何选择查询模式

| 用户需求 | 查询模式 |
|--------------|------|
| “去纽约市的航班价格是多少？” | 快速模式 |
| “现在去洛杉矶的航班便宜吗？” | 快速模式 |
| “查找3月5日的航班信息” | 详细模式 |
| “哪些航空公司从 YYC 飞往 LAX？” | 详细模式 |
| “去丹佛的最佳直飞航班有哪些？” | 详细模式 |
| “比较早上的航班和晚上的航班” | 详细模式 |
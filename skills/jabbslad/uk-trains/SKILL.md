---
name: trains
description: 查询英国国家铁路（UK National Rail）的实时列车出发信息、到达时间、延误情况以及列车服务详情。当需要了解列车时刻、出发时间、到达时间、延误情况、站台信息，或者“下一班列车是什么时候”时，可以使用该服务。该服务支持通过 Darwin/Huxley2 API 查询英国境内的所有火车站信息。
---

# 英国火车查询

通过查询National Rail的Darwin API，可以获取火车的实时出发和到达信息。

## 设置

需要一个免费的Darwin API令牌：
1. 在 https://realtime.nationalrail.co.uk/OpenLDBWSRegistration/ 注册。
2. 将 `NATIONAL_RAIL_TOKEN` 设置在环境变量中（或在 `skills.entries.uk-trains.apiKey` 中进行配置）。

## 命令

```bash
# Departures
./scripts/trains.py departures PAD
./scripts/trains.py departures PAD to OXF --rows 5

# Arrivals  
./scripts/trains.py arrivals MAN
./scripts/trains.py arrivals MAN from EUS

# Station search
./scripts/trains.py search paddington
./scripts/trains.py search kings
```

## 车站代码

使用3个字母的CRS代码表示车站：
- `PAD` = 伦敦帕丁顿（London Paddington）
- `EUS` = 伦敦尤斯顿（London Euston）
- `KGX` = 伦敦国王十字（London Kings Cross）
- `VIC` = 伦敦维多利亚（London Victoria）
- `WAT` = 伦敦滑铁卢（London Waterloo）
- `MAN` = 曼彻斯特皮卡迪利（Manchester Piccadilly）
- `BHM` = 伯明翰新街（Birmingham New Street）
- `EDB` = 爱丁堡韦弗利（Edinburgh Waverley）
- `GLC` = 格拉斯哥中央（Glasgow Central）
- `BRI` = 布里斯托尔坦普尔米兹（Bristol Temple Meads）
- `LDS` = 利兹（Leeds）
- `LIV` = 利物浦莱姆街（Liverpool Lime Street）
- `RDG` = 雷丁（Reading）
- `OXF` = 牛津（Oxford）
- `CBG` = 剑桥（Cambridge）

## 响应格式

响应数据为JSON格式，包含以下内容：
- `locationName`：车站名称
- `crs`：车站代码
- `messages[]`：服务提醒信息
- `trainServices[]`：火车信息列表：
  - `std`/`sta`：计划出发/到达时间
  `etd`/`eta`：预计到达时间（“准时”、“延误”或实际到达时间）
  `platform`：站台编号
  `operator`：列车运营公司
  `destination[].name`：最终目的地
  `isCancelled`, `cancelReason`, `delayReason`：列车延误/取消的原因

## 消息模板

使用以下简洁的格式进行WhatsApp或聊天消息的回复：

```
🚂 {Origin} → {Destination}

*{dep} → {arr}* │📍{platform} │ 🚃 {coaches}
{status}

*{dep} → {arr}* │📍{platform} │ 🚃 {coaches}
{status}
```

### 消息内容
- **标题：** 🚂 [出发地] → [目的地]
- **时间：** **粗体** 出发时间 → 到达时间
- **站台：** 📍 + 站台编号（未知时显示“TBC”）
- **车厢：** 🚃 + 车厢数量
- **状态：**
  - ✅ 准时
  - ⚠️ 延误（预计到达时间：{时间})
  - ❌ 取消 — {原因}
  - 🔄 从这里出发

### 示例

```
🚂 Hemel Hempstead → Euston

*20:18 → 20:55* │📍4 │ 🚃 4
✅ On time

*20:55 → 21:30* │📍4 │ 🚃 12
✅ On time

*21:11 → 21:41* │📍4 │ 🚃 8
✅ On time
```

### 获取到达时间

要获取火车的到达时间，需要执行两次API请求：
1. `departures {出发地} to {目的地}` — 获取出发时间及服务ID
2. `arrivals {目的地} from {出发地}` — 获取到达时间

通过服务ID中的数字前缀来匹配相应的服务（例如，`4748110HEMLHMP_` 对应 `4748110EUSTON__`）。

### 注意事项：
- 每条服务信息之间使用空行分隔。
- 如果列车编组数据不可用，则不显示车厢信息。
- 对于延误的列车，会显示预计到达时间：`⚠️ 延误（预计到达时间：20:35）`
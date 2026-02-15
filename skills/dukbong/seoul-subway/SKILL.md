---
name: seoul-subway
description: 首尔地铁助手：提供实时列车到站信息、路线规划及服务提醒（韩文/英文版本）
model: sonnet
metadata: {"moltbot":{"emoji":"🚇"}}
homepage: https://github.com/dukbong/seoul-subway
user-invocable: true
---

# 首尔地铁技能

查询首尔地铁的实时信息。**无需API密钥**——使用代理服务器。

## 功能

| 功能 | 描述 | 韩文触发示例 | 英文触发示例 |
|---------|-------------|----------------------|----------------------|
| 实时到站时间 | 根据车站查询列车到站时间 | "강남역 도착정보" | "Gangnam station arrivals" |
| 车站搜索 | 查找线路和车站代码 | "강남역 몇호선?" | "What line is Gangnam?" |
| 路线搜索 | 查找最短路径及时间/费用 | "신도림에서 서울역" | "Sindorim to Seoul Station" |
| 服务提醒 | 列车延误、故障、停运信息 | "지하철 지연 있어?" | "Any subway delays?" |
| **末班列车** | 根据车站查询末班列车时间 | "홍대 막차 몇 시야?" | "Last train to Hongdae?" |
| **出口信息** | 提供地标对应的出口编号 | "코엑스 몇 번 출구?" | "Which exit for COEX?" |
| **无障碍设施** | 提供电梯、自动扶梯、轮椅升降机等无障碍设施信息 | "강남역 엘리베이터" | "Gangnam elevators" |
| **快速出口** | 提供前往便利设施的最佳车厢 | "강남역 빠른하차" | "Gangnam quick exit" |
| **洗手间** | 提供洗手间位置信息 | "강남역 화장실" | "Gangnam restrooms" |

### 自然语言触发

支持多种自然语言表达：

#### 实时到站时间
| 英文 | 韩文 |
|---------|--------|
| "강남역 도착정보" | "Gangnam station arrivals" | "查询江南站的列车到站时间" |
| "신도림에서 서울역" | "从新洞到首尔站" | "How to get from Sindorim to Seoul Station?" |
| "홍대 막차 몇 시야?" | "Hongdae的末班列车是几点?" | "What is the last train to Hongdae?" |

#### 车站搜索
| 英文 | 韩文 |
|---------|--------|
| "강남역 몇호선?" | "Gangnam station is on which line?" | "江南站属于哪条线路？" |
| "신도림에서 서울역 어떻게 가?" | "How do I get from Sindorim to Seoul Station?" | "如何从新洞去首尔站？" |

#### 路线搜索
| 英文 | 韩文 |
|---------|--------|
| "신도림에서 서울역" | "How do I get from Sindorim to Seoul Station?" | "从新洞到首尔站的路线是什么？" |
| "서울역까지 가장快的路线是什么?" | "What is the fastest route to Seoul Station?" |

#### 服务提醒
| 英文 | 韩文 |
|---------|--------|
| "지하철 지연 있어?" | "Is there any subway delay?" | "地铁有延误吗？" |
| "지하철 상황" | "What's the current subway status?" | "地铁的当前运行情况如何？" |
| "지하철 지연 있어?" | "Are there any subway delays?" | "是否有地铁延误？"

#### 末班列车
| 英文 | 韩文 |
|---------|--------|
| "홍대 막차 몇 시야?" | "Hongdae的末班列车是几点?" | "Hongdae的末班列车时间是几点？" |
| "서울역 막차" | "What is the last train to Seoul Station?" | "首尔站的末班列车是几点？" |

#### 出口信息
| 英文 | 韩文 |
|---------|--------|
| "코엑스 몇 번 출구?" | "COEX的出口是几号?" | "COEX的出口是几号？" |
| "롯데월드 출구" | "Which exit is for Lotte World?" | "롯데世界在哪个出口？" |

#### 无障碍设施
| 英文 | 韩文 |
|---------|--------|
| "강남역 엘리베이터" | "Gangnam station has elevators." | "江南站有电梯。" |
| "강남역 빠른하차" | "Which car is the fastest to exit Gangnam?" | "去江南站哪个车厢出口最快？" |

#### 洗手间
| 英文 | 韩文 |
|---------|--------|
| "강남역 화장실" | "Where are the restrooms in Gangnam?" | "江南站的洗手间在哪里？" |
| "강남역 화장실" | "Where are the restrooms at Gangnam Station?" | "江南站的洗手间在哪里？"

---

## 首次使用说明

首次使用此技能时，系统会提示是否允许访问代理服务器。

**建议：** 选择“Yes”以允许本次会话的访问。

> **注意：** 也可以选择“Yes, and don’t ask again”以方便后续使用，
> 但仅限于您信任该代理服务器的情况下。代理服务器仅接收车站名称和搜索参数，绝不会获取您的对话内容或个人数据。
> 详情请参阅[数据隐私](#data-privacy--데이터-프라이버시)部分。

---

## 数据隐私

此技能通过`vercel-proxy-henna-eight.vercel.app`代理服务器发送请求。

### 发送的数据

- **车站名称**（韩文或英文，例如：“강남”/“Gangnam”）
- **搜索参数**（出发/到达车站、线路筛选条件、分页参数）
- 标准HTTP头部信息（IP地址、User-Agent）

仅发送车站名称、搜索参数和标准HTTP头部信息。

### 不会发送的数据

- 对话记录或上下文
- 个人信息、文件或项目数据
- 任何形式的认证凭证

---

## 代理服务器安全措施

- **输入验证**：车站名称限制在50个字符以内，仅支持韩文/英文/数字
- **速率限制**：每分钟每个IP地址最多100次请求
- **敏感数据加密**：API密钥和令牌在服务器日志中会被加密
- **无需认证**：无需用户账户或跟踪信息
- **开源代码**：代理服务器的源代码可在[github.com/dukbong/seoul-subway](https://github.com/dukbong/seoul-subway)查看

---

## API参考

所有API请求均通过代理服务器进行。用户无需API密钥。

> **注意：** 下面的`curl`命令仅用于API参考。
> Claude使用`WebFetch`来调用这些API接口，无需使用任何二进制工具。

### 基础URL

### 1. 实时到站信息

**API端点**
```
GET /api/realtime/{station}?start=0&end=10
```

**参数**

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| station | 是 | 车站名称（韩文，URL编码格式） |
| start | 否 | 开始索引（默认：0） |
| end | 否 | 结束索引（默认：10） |
| format | 否 | 格式（markdown或JSON） |
| lang | 否 | 语言（默认：ko或en） |

**响应字段**

| 字段 | 描述 |
|-------|-------------|
| subwayId | 线路ID（1002=2号线，1077=新盆唐线） |
| trainLineNm | 行车方向（例如：“성수행 - 역삼방면”） |
| arvlMsg2 | 到站时间（例如：“4분 20초 후”） |
| arvlMsg3 | 当前位置 |
| isFastTrain | 快车标志（1=快速列车） |

**示例**
```bash
curl "https://vercel-proxy-henna-eight.vercel.app/api/realtime/강남"
```

---

### 2. 车站搜索

**API端点**
```
GET /api/stations?station={name}&start=1&end=10
```

**参数**

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| station | 是 | 要搜索的车站名称 |
| start | 否 | 开始索引（默认：1） |
| end | 否 | 结束索引（默认：10） |

**响应字段**

| 字段 | 描述 |
| STATION_CD | 车站代码 |
| STATION_NM | 车站名称 |
| LINE_NUM | 线路名称（例如：“02호선”） |
| FR_CODE | 外部车站代码 |

**示例**
```bash
curl "https://vercel-proxy-henna-eight.vercel.app/api/stations?station=강남"
```

---

### 3. 路线搜索

**API端点**
```
GET /api/route?dptreStnNm={departure}&arvlStnNm={arrival}
```

**参数**

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| dptreStnNm | 出发车站 |
| arvlStnNm | 到达车站 |
| searchDt | 时间（yyyy-MM-dd HH:mm:ss） |
| searchType | 是否需要搜索类型（例如：路线、距离、换乘） |
| format | 格式（markdown或JSON） |
| lang | 语言（默认：ko或en） |

**响应字段**

| 字段 | 描述 |
| totalDstc | 总距离（米） |
| totalReqHr | 总时间（秒） |
| totalCardCrg | 车费（韩元） |
| paths[].trainno | 列车编号 |
| paths[].trainDptreTm | 出发时间 |
| paths[].trainArvlTm | 到达时间 |
| paths[].trsitYn | 换乘信息 |

**示例**
```bash
curl "https://vercel-proxy-henna-eight.vercel.app/api/route?dptreStnNm=신도림&arvlStnNm=서울역"
```

---

### 4. 服务提醒

**API端点**
```
GET /api/alerts?pageNo=1&numOfRows=10&format=enhanced
```

**参数**

| 参数 | 是否必填 | 描述 |
| pageNo | 是否需要页码（默认：1） |
| numOfRows | 每页显示的记录数（默认：10） |
| lineNm | 是否需要按线路筛选 |
| format | 格式（默认或增强型响应） |

**响应字段（默认）**

| 字段 | 描述 |
| ntceNo | 通知编号 |
| ntceSj | 通知标题 |
| ntceCn | 通知内容 |
| lineNm | 线路名称 |
| regDt | 注册日期 |

**响应字段（增强型）**

| 字段 | 描述 |
| summary.delayedLines | 发生延误的线路 |
| summary.suspendedLines | 停运的线路 |
| summary.normalLines | 正常运行的线路 |
| alerts[].lineName | 线路名称 |
| alerts[].lineNameEn | 线路名称（英文） |
| alerts[].status | 状态（正常/延误/停运） |
| alerts[].severity | 严重程度（低/中/高） |
| alerts[].title | 通知标题 |

**示例**
```bash
# Default format
curl "https://vercel-proxy-henna-eight.vercel.app/api/alerts"

# Enhanced format with status summary
curl "https://vercel-proxy-henna-eight.vercel.app/api/alerts?format=enhanced"
```

---

### 5. 末班列车时间

> **注意：** 该API提供77个主要车站的末班列车时间（数据更新至2025年1月）。
> **支持的车站（77个）：**
> 가산디지털단지, 강남, 강남구청, 강변, 건대입구, 경복궁, 고속터미널, 공덕, 광나루, 광화문, 교대, 구로, 군자, 김포공항, 노량진, 당산, 대림, 동대문, 동대문역사문화공원, 디지털미디어시티, 뚝섬, 마포구청, 명동, 모란, 몽촌토성, 복정, 불광, 사가정, 사당, 삼각지, 삼성, 상봉, 서울대입구, 서울역, 선릉, 성수, 수유, 시청, 신논현, 신당, 신도림, 신사, 신촌, 안국, 압구정, 약수, 양재, 여의도, 역삼, 연신내, 영등포, 옥수, 올림픽공원, 왕십리, 용산, 을지로3가, 을지로4가, 을지로입구, 응암, 이대, 이촌, 인천공항1터미널, 인천공항2터미널, 잠실, 정자, 종각, 종로3가, 종합운동장, 천호, 청담, 충무로, 판교, 합정, 혜화, 홍대입구, 효창공원앞 |

**API端点**
```
GET /api/last-train/{station}?direction=up&weekType=1
```

**参数**

| 参数 | 是否必填 | 描述 |
| station | 是 | 车站名称（韩文或英文） |
| direction | 是否需要方向（up/down/all，默认：all） |
| weekType | 是否需要星期类型（1=工作日，2=周六，3=周日/节假日，默认：自动） |

**响应字段**

| 字段 | 描述 |
| station | 车站名称（韩文/英文） |
| lastTrains[].direction | 方向（韩文/英文） |
| lastTrains[].time | 末班列车时间（HH:MM） |
| lastTrains[].weekType | 星期类型（韩文/英文） |
| lastTrains[].line | 线路名称 |
| lastTrains[].destination | 最终目的地（韩文/英文） |

**示例**
```bash
# Auto-detect day type
curl "https://vercel-proxy-henna-eight.vercel.app/api/last-train/홍대입구"

# English station name
curl "https://vercel-proxy-henna-eight.vercel.app/api/last-train/Hongdae"

# Specific direction and day
curl "https://vercel-proxy-henna-eight.vercel.app/api/last-train/강남?direction=up&weekType=1"
```

### 6. 出口信息

> **注意：** 该API提供77个主要车站的出口信息（数据更新至2025年1月）。
> **支持的车站（77个）：**
> 가산디지털단지, 강남, 강남구청, 강변, 건대입구, 경복궁, 고속터미널, 공덕, 광나루, 광화문, 교대, 구로, 군자, 김포공항, 노량진, 당산, 대림, 동대문, 동대문역사문화공원, 디지털미디어시티, 뚝섬, 마포구청, 명동, 모란, 몽촌토성, 복정, 불광, 사가정, 사당, 삼각지, 삼성, 상봉, 서울대입구, 서울역, 선릉, 성수, 수유, 시청, 신논현, 신당, 신도림, 신사, 신촌, 안국, 압구정, 약수, 양재, 여의도, 역삼, 연신내, 영등포, 옥수, 올림픽공원, 왕십리, 용산, 을지로3가, 을지로4가, 을지로입구, 응암, 이대, 이촌, 인천공항1터미널, 인천공항2터미널, 잠실, 정자, 종각, 종로3가, 종합운동장, 천호, 청담, 충무로, 판교, 합정, 혜화, 홍대입구, 효창공원앞 |

**API端点**
```
GET /api/exits/{station}
```

**参数**

| 参数 | 是否必填 | 描述 |
| station | 是 | 车站名称（韩文或英文） |

**错误响应（不支持的车站）**
```json
{
  "code": "INVALID_STATION",
  "message": "Exit information not available for this station",
  "hint": "Exit information is available for major tourist stations only"
}
```

**响应字段**

| 字段 | 描述 |
| station | 车站名称（韩文/英文） |
| line | 线路名称 |
| exits[].number | 出口编号 |
| exits[].landmark | 附近地标（韩文/英文） |
| exits[].landmarkEn | 附近地标（英文） |
| exits[].distance | 行走距离 |
| exits[].facilities | 设施类型 |

**示例**
```bash
# Get COEX exit info
curl "https://vercel-proxy-henna-eight.vercel.app/api/exits/삼성"

# English station name
curl "https://vercel-proxy-henna-eight.vercel.app/api/exits/Samsung"
```

---

### 7. 无障碍设施信息

**API端点**
```
GET /api/accessibility/{station}
```

**参数**

| 参数 | 是否必填 | 描述 |
| station | 是 | 车站名称（韩文或英文） |
| type | 是否需要查询类型（elevator/escalator/wheelchair/all，默认：all） |
| format | 格式（markdown或JSON） |
| lang | 语言（韩文/英文） |

**响应字段**

| 字段 | 描述 |
| station | 车站名称（韩文/英文） |
| elevators[].lineNm | 电梯线路编号 |
| elevators[].dtlPstn | 电梯具体位置 |
| elevators[].bgngFlr | 电梯楼层（起始/结束层） |
| elevators[].bgngFlrGrndUdgdSe | 电梯所在楼层（地上/地下） |
| elevators[].oprtngSitu | 电梯运行状态 |
| escalators[] | 自动扶梯信息（与电梯相同） |
| wheelchairLifts[] | 轮椅升降机信息（与电梯相同） |

**示例**
```bash
# All accessibility info
curl "https://vercel-proxy-henna-eight.vercel.app/api/accessibility/강남"

# Elevators only
curl "https://vercel-proxy-henna-eight.vercel.app/api/accessibility/강남?type=elevator"

# English output
curl "https://vercel-proxy-henna-eight.vercel.app/api/accessibility/Gangnam?lang=en"

# Raw JSON
curl "https://vercel-proxy-henna-eight.vercel.app/api/accessibility/강남?format=raw"
```

### 8. 快速出口信息

**API端点**
```
GET /api/quick-exit/{station}
```

**参数**

| 参数 | 是否必填 | 描述 |
| station | 是 | 车站名称（韩文或英文） |
| facility | 是否需要查询设施类型（elevator/escalator/exit/all，默认：all） |
| format | 格式（markdown或JSON） |
| lang | 语言（韩文/英文） |

**响应字段**

| field | Description |
| station | 车站名称（韩文/英文） |
| quickExits[].lineNm | 最适合的线路编号 |
| quickExits[].drtnInfo | 最佳出口方向 |
| quickExits[].qckgffVhclDoorNo | 最适合的出口车厢/门编号 |
| quickExits[].plfmCmgFac | 设施类型（电梯/自动扶梯/楼梯） |
| quickExits[].upbdnbSe | 上下行方向（上/下） |
| quickExits[].elvtrNo | 电梯编号（如适用） |

**示例**
```bash
# All quick exit info
curl "https://vercel-proxy-henna-eight.vercel.app/api/quick-exit/강남"

# Filter by elevator
curl "https://vercel-proxy-henna-eight.vercel.app/api/quick-exit/강남?facility=elevator"

# English station name
curl "https://vercel-proxy-henna-eight.vercel.app/api/quick-exit/Gangnam"
```

### 9. 洗手间信息

**API端点**
```
GET /api/restrooms/{station}
```

**参数**

| 参数 | 是否必填 | 描述 |
| station | 是 | 车站名称（韩文或英文） |
| format | 格式（markdown或JSON） |
| lang | 语言（韩文/英文） |

**响应字段**

| field | Description |
| station | 车站名称（韩文/英文） |
| restrooms[].lineNm | 洗手间线路编号 |
| restrooms[].dtlPstn | 手卫生间具体位置 |
| restrooms[].stnFlr | 洗手间所在楼层（例如：B1） |
| restrooms[].grndUdgdSe | 洗手间所在楼层（地上/地下） |
| restrooms[].gateInoutSe | 手卫生间内外门状态 |
| restrooms[].rstrmInfo | 手卫生间设施信息 |
| restrooms[].whlchrAcsPsbltyYn | 是否适合轮椅使用 |

**示例**
```bash
# Get restroom info
curl "https://vercel-proxy-henna-eight.vercel.app/api/restrooms/강남"

# English output
curl "https://vercel-proxy-henna-eight.vercel.app/api/restrooms/Gangnam?lang=en"

# Raw JSON
curl "https://vercel-proxy-henna-eight.vercel.app/api/restrooms/강남?format=raw"
```

## 地标与车站对应关系

以下是外国人常去的地标及其对应的首尔地铁车站信息：

| 地标 | 车站 | 线路 | 出口 |
|----------|---------|------|------|
| COEX / 코엑스 | 삼성 Samsung | 2호선 | 5-6 |
| Lotte World / 롯데월드 | 잠실 Jamsil | 2호선 | 4 |
| Lotte World Tower | 잠실 Jamsil | 2호선 | 3 |
| Gyeongbokgung Palace / 경복궁 | 경복궁 Gyeongbokgung | 3호선 | 5 |
| Changdeokgung Palace / 창덕궁 | 안국 Anguk | 3호선 | 3 |
| DDP / 동대문디자인플라자 | 동대문역사문화공원 | 2호선 | 1 |
| Myeongdong / 명동 | 명동 Myeongdong | 4호선 | 6 |
| N Seoul Tower / 남산타워 | 명동 Myeongdong | 4호선 | 3 |
| Bukchon Hanok Village | 안국 Anguk | 3호선 | 6 |
| Insadong / 인사동 | 안국 Anguk | 3호선 | 1 |
| Hongdae / 홍대 | 홍대입구 Hongik Univ. | 2호선 | 9 |
| Itaewon / 이태원 | 이태원 Itaewon | 6호선 | 1 |
| Gangnam / 강남 | 강남 Gangnam | 2호선 | 10-11 |
| Yeouido Park / 여의도공원 | 여의도 Yeouido | 5호선 | 5 |
| IFC Mall | 여의도 Yeouido | 5호선 | 1 |
| 63 Building | 여의도 Yeouido | 5호선 | 3 |
| Gwanghwamun Square / 광화문광장 | 광화문 Gwanghwamun | 5호선 | 2 |
| Namdaemun Market / 남대문시장 | 서울역 Seoul Station | 1호선 | 10 |
| Cheonggyecheon Stream / 청계천 | 을지로입구 Euljiro 1-ga | 2호선 | 6 |
| Express Bus Terminal | 고속터미널 Express Terminal | 3호선 | 4,8 |
| Gimpo Airport | 김포공항 Gimpo Airport | 5호선 | 1,3 |
| Incheon Airport T1 | 인천공항1터미널 | 인천공항1터미널 | 1 |
| Incheon Airport T2 | 인천공항2터미널 | 인천공항2터미널 | 1 |

---

## 静态数据（GitHub源代码）

对于车站列表和线路对应关系等静态数据，请使用GitHub的源代码链接：

```bash
# Station list
curl "https://raw.githubusercontent.com/dukbong/seoul-subway/main/data/stations.json"

# Line ID mappings
curl "https://raw.githubusercontent.com/dukbong/seoul-subway/main/data/lines.json"

# Station name translations
curl "https://raw.githubusercontent.com/dukbong/seoul-subway/main/data/station-names.json"
```

## 线路编号对照表

| 线路 | ID | 韩文名称 | 英文名称 |
|------|----|------|----|
| Line 1 | 1001 | 1호선 | Seoul Station | 서울역 |
| Line 2 | 1002 | 강남 Gangnam | Gangnam |
| Line 3 | 1003 | 삼성 Samseong | Samsung |
| Line 4 | 1004 | 신도림 Sindorim | Sindorim |
| Line 5 | 1005 | Sinbundang | Sinbundang |
| Gyeongui-Jungang | 1063 | Gyeongchun |
| Airport Railroad | 1065 | Suin-Bundang | Suin-Bundang |
| Line 6 | 1006 | 경의중앙 Gyeongui-Jungang | Gyeongui-Jungang |
| Line 7 | 1007 | Sinbundang | Sinbundang |
| Gyeongui-Jungang | 1067 | Gyeongchun |
| Airport Railroad | 1065 | Suin-Bundang |
| Line 8 | 1008 | 강동 Gangdong-gu | Gangdong |
| Line 9 | 1009 | 경복궁 Gyeongbokgung | Gyeongbokgung |
| Line 10 | 1010 | 동대문 Dongdaemun | Dongdaemun |
| Line 11 | 1011 | 동대문역사문화공원 Dongdaemun History & Culture Park | Dongdaemun History & Culture Park |

---

## 线路颜色编码

| 线路 | 颜色 | 表示方式 |
|---------|--------------|-------|
| 1호선 | Blue | 🔵 | 蓝色 |
| 2호선 | Green | 🟢 | 绿色 |
| 3호선 | Orange | 🟠 | 橙色 |
| 4호선 | Sky Blue | 🔵 | 天蓝色 |
| 5호선 | Purple | 🟣 | 紫色 |
| 6호선 | Brown | 🟤 | 棕色 |
| 7호선 | Olive | 🟢 | 橄榄色 |
| 8호선 | Pink | 🔴 | 粉红色 |
| 9호선 | Gold | 🟡 | 金色 |
| 신분당선 | Red | 🔴 | 红色 |
| 경의중앙선 | Cyan | 청록色 |
| 공항철도 | Blue | 🔵 | 蓝色 |
| 수인분당선 | Yellow | 🟡 | 黄色 |

---

## 输出格式说明

- **实时到站时间**：以韩文或英文显示列车到站时间。
- **车站搜索**：返回车站名称及线路信息。
- **路线搜索**：显示路线名称及行驶方向。
- **服务提醒**：显示列车延误或停运信息。
- **末班列车**：提供末班列车时间。
- **出口信息**：列出各出口的编号及附近地标。
- **无障碍设施**：提供电梯、自动扶梯等设施信息。
- **洗手间**：显示洗手间位置。
- **快速出口**：推荐最方便的下车车厢及出口位置。
- **错误信息**：显示错误代码及原因。
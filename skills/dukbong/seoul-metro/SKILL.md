---
name: seoul-metro
description: 首尔地铁辅助工具：提供实时列车到站信息、路线规划以及服务提醒（支持韩语/英语）
metadata: {"moltbot":{"emoji":"🚇","requires":{"bins":["curl","jq"],"env":["SEOUL_OPENAPI_KEY","DATA_GO_KR_KEY"]},"primaryEnv":"SEOUL_OPENAPI_KEY"}}
homepage: https://github.com/dukbong/seoul-metro
user-invocable: true
---

# 首尔地铁技能

查询首尔地铁的实时信息。

## 功能

| 功能 | 描述 | 韩文触发示例 | 英文触发示例 |
|---------|-------------|----------------------|----------------------|
| 实时到站信息 | 按站点显示列车到站时间 | "강남역 도착정보" | "Gangnam station arrivals" |
| 站点查询 | 查找线路和站点代码 | "강남역 몇호선?" | "What line is Gangnam?" |
| 路线查询 | 按最短时间/费用查找路线 | "신도림에서 서울역" | "Sindorim to Seoul Station" |
| 服务提醒 | 列车延误、事故、站点停运信息 | "지하철 지연 있어?" | "Are there any subway delays?" |

## 环境变量

| 变量 | 用途 | 提供方 |
|----------|-------|----------|
| `SEOUL_OPENAPI_KEY` | 列车到站信息、站点查询 | data.seoul.go.kr |
| `DATA_GO_KR_KEY` | 路线查询、服务提醒 | data.go.kr |

**如何获取API密钥：**
1. **SEOUL_OPENAPI_KEY**：在 [data.seoul.go.kr](https://data.seoul.go.kr) 注册，然后进入“我的页面” > “API密钥管理” |
2. **DATA_GO_KR_KEY**：在 [data.go.kr](https://www.data.go.kr) 注册，搜索相应的API服务并申请访问权限 |

---

## API参考

### 1. 实时到站信息

**端点**
```
http://swopenAPI.seoul.go.kr/api/subway/{KEY}/json/realtimeStationArrival/{start}/{end}/{station}
```

**响应字段**

| 字段 | 描述 |
|-------|-------------|
| `subwayId` | 线路ID（1002=2号线，1077=新盆唐线） |
| `trainLineNm` | 行车方向（例如：“성수행 - 역삼방면”） |
| `arvlMsg2` | 到站时间（例如：“4분 20초 후”） |
| `arvlMsg3` | 当前位置 |
| `btrainSttus` | 列车类型（普通/快速） |
| `lstcarAt` | 最后一班列车（0=无，1=有） |

---

### 2. 站点查询

**端点**
```
http://openapi.seoul.go.kr:8088/{KEY}/json/SearchInfoBySubwayNameService/{start}/{end}/{station}
```

**响应字段**

| 字段 | 描述 |
| `STATION_CD` | 站点代码 |
| `STATION_NM` | 站点名称 |
| `LINE_NUM` | 线路名称（例如：“02호선”） |
| `FR_CODE` | 外部站点代码 |

---

### 3. 路线查询

**端点**
```
https://apis.data.go.kr/B553766/path/getShtrmPath
```

**参数**

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| `serviceKey` | 是 | DATA_GO_KR_KEY |
| `dptreStnNm` | 是 | 出发站点 |
| `arvlStnNm` | 是 | 到达站点 |
| `searchDt` | 是 | 日期时间（yyyy-MM-dd HH:mm:ss） |
| `dataType` | 是 | JSON格式 |
| `searchType` | 否 | 可选择：持续时间、距离或换乘方式 |

**响应字段**

| 字段 | 描述 |
| `totalDstc` | 总距离（米） |
| `totalReqHr` | 总时间（秒） |
| `totalCardCrg` | 车费（韩元） |
| `paths[].trainno` | 列车编号 |
| `paths[].trainDptreTm` | 出发时间 |
| `paths[].trainArvlTm` | 到达时间 |
| `paths[].trsitYn` | 换乘标志 |

---

### 4. 服务提醒

**端点**
```
https://apis.data.go.kr/B553766/ntce/getNtceList
```

**参数**

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| `serviceKey` | 是 | DATA_GO_KR_KEY |
| `dataType` | 是 | JSON格式 |
| `pageNo` | 否 | 页面编号 |
| `numOfRows` | 否 | 每页显示结果数量 |
| `lineNm` | 否 | 按线路筛选 |

**响应字段**

| 字段 | 描述 |
| `noftTtl` | 提醒标题 |
| `noftCn` | 提醒内容 |
| `noftOcrnDt` | 提醒时间戳 |
| `lineNmLst` | 受影响的线路 |
| `nonstopYn` | 是否直通 |
| `xcseSitnBgngDt` | 事故开始时间 |
| `xcseSitnEndDt` | 事故结束时间 |

---

## 线路ID对照表

| 线路 | ID | 线路 | ID |
|------|----|------|----|
| 1号线 | 1001 | 6号线 | 1006 |
| 2号线 | 1002 | 7号线 | 1007 |
| 3号线 | 1003 | 8号线 | 1008 |
| 4号线 | 1004 | 9号线 | 1009 |
| 新盆唐线 | 1077 | 京畿中央线 | 1063 |
| 京春线 | 1067 | 机场铁路线 | 1065 |
| 水原盆唐线 | 1075 |

## 站点名称对照表（英文→韩文）

以下是主要站点的英文-韩文对照表。调用API时需要将英文站点名称转换为韩文。

### 1号线（1호선）
| 英文 | 韩文 | 英文 | 韩文 |
|---------|--------|---------|--------|
| 首尔站 | 서울역 | 서울역 | Seoul Station |
| 종각 | 종각 | Jonggak |
| 종로3가 | 종로3가 | Jongno 3-ga |
| 동대문 | 동대문 | Dongdaemun |
| 청량리 | 청량리 | Cheongnyangni |
| 노량진 | 노량진 | Noryangjin |
| 영등포 | 영등포 | Yeongdeungpo |
| 구로 | 구로 | Guro |
| 인천 | 인천 | Incheon |
| 부평 | 부평 | Bupyeong |
| 수원 | 수원 | Suwon |

### 2号线（2호선）
| 英文 | 韩文 | 英文 | 韩文 |
| 강남 | 강남 | Gangnam |
| 역삼 | 역삼 | Yeoksam |
| 삼성 | 삼성 | Samseong |
| 잠실 | 잠실 | Jamsil |
| 신도림 | 신도림 | Sindorim |
| 홍대입구 | 홍대입구 | Hongdae (Hongik Univ.) |
| 합정 | 합정 | Hapjeong |
| 당산 | 당산 | Dangsan |
| 여의도 | 여의도 | Yeouido |
| 선릉 | 선릉 | Seolleung |
| 삼성 | 삼성 | Samsung |
| 스포츠콤플렉스 | 종합운동장 | Sports Complex |
| 뚝섬 | 뚝섬 | Ttukseom |
| 왕십리 | 왕십리 | Wangsimni |
| 을지로3가 | 을지로3가 | Euljiro 3-ga |
| 을지로입구 | 을지로입구 | Euljiro Entrance |
| 충정로 | 충정로 | Chungjeongno |
| 이대 | 이대 | Ewha Womans Univ. |
| 신촌 | 신촌 | Sinchon |
| 사당 | 사당 | Sadang |
| 낙성대 | 낙성대 | Nakseongdae |
| 서울대입구 | 서울대입구 | Seoul National Univ. Entrance |

### 3号线（3호선）
| 英文 | 韩文 | 英文 | 韩文 |
| 경복궁 | 경복궁 | Gyeongbokgung |
| 종로3가 | Jongno 3-ga | Jongno 3-ga |
| 충무로 | Chungmuro | Chungmu-ro |
| 동대입구 | Dongdae Entrance | Dongdae Entrance |
| 압구정 | Apgujeong | Apgujeong |
| 신사 | Sinsa | Sinsa |
| 고속터미널 | Express Bus Terminal |
| 고속터미널 | Express Bus Terminal |
| 남부터미널 | Nambu Terminal |
| 양재 | Yangjae |
| 대화 | Daehwa |
| 주엽 | Juyeop |

### 4号线（4호선）
| 英文 | 韩文 | 英文 | 韩文 |
| 명동 | 명동 | Myeongdong |
| 서울역 | 서울역 | Seoul Station |
| 숙대입구 | Sookmyung Women's Univ. | Sookmyung Women's Univ. Entrance |
| 동대문역사문화공원 | Dongdaemun History & Culture Park |
| 혜화 | Hyehwa |
| 한성대입구 | Hansung Univ. Entrance |
| 미아 | Mia |
| 미아사거리 | Mia Intersection |
| 총신대입구 | Chongshin Univ. Entrance |
| 사당 | Sadang |

### 5号线（5호선）
| 英文 | 韩文 | 英文 | 韩文 |
| 광화문 | 광화문 | Gwanghwamun |
| 동대문역사문화공원 | Dongdaemun History & Culture Park |
| 행당 | Haengdang |
| 여의도 | Yeouido |
| 마포 | 마포 | Mapo |
| 공덕 | Gongdeok |
| 김포공항 | Gimpo Airport |
| 방화 | Banghwa |

### 6号线（6호선）
| 英文 | 韩文 | 英文 | 韩文 |
| 이태원 | 이태원 | Itaewon |
| 삼각지 | Samgakji |
| 녹사평 | Noksapyeong |
| 한강진 | Hangangjin |
| 상수 | Sangsu |
| 합정 | Hapjeong |
| 월드컵경기장 | World Cup Stadium |
| 디지털미디어시티 | Digital Media City |

### 7号线（7号线）
| 英文 | 韩文 | 英文 | 韩文 |
| 강남구청 | Gangnam-gu Office |
| 청담 | Cheongdam |
| 건대입구 | Keon-dae Entrance |
| 어린이대공원 | Children's Grand Park |
| 중곡 | Junggok |
| 뚝섬유원지 | Ttukseom Resort |
| 비현 | Nonhyeon |
| 학동 | Hakdong |
| 보광 | Bogwang |
| 장암 | Jangam |
| 도봉산 | Dobongsan |

### 8号线（8号线）
| 英文 | 韩文 | 英文 | 韩文 |
| 잠실 | 잠실 | Jamsil |
| 몽촌토성 | Mongchontoseong |
| 강동구청 | Gangdong-gu Office |
| 천호 | Cheonho |
| 복정 | Bokjeong |
| 산성 | Sanseong |
| 모란 | Moran |
| 암사 | Amsa |

### 9号线（9号线）
| 英文 | 韩文 | 英文 | 韩文 |
| 신논현 | Sinnonhyeon |
| 고속터미널 | Express Bus Terminal |
| 동작 | Dongjak |
| 노량진 | Noryangjin |
| 여의도 | Yeouido |
| 국회의사당 | National Assembly |
| 당산 | Dangsan |
| 염창 | Yeomchang |
| 김포공항 | Gimpo Airport |
| 개화 | Gaehwa |
| 올림픽공원 | Olympic Park |
| 종합운동장 | Sports Complex |

### 新盆唐线（Sinbundang Line）
| 英文 | 韩文 | 英文 | 韩文 |
| 강남 | 강남 | Gangnam |
| 신사 | Sinsa |
| 양재 | Yangjae |
| 양재시민의숲 | Yangjae Citizen's Forest |
| 판교 | Pangyo |
| 정자 | Jeongja |
| 동천 | Dongcheon |
| 수지구청 | Suji District Office |
| 광교 | Gwanggyo |
| 광교중앙 | Gwanggyo Jungang |

### 京畿中央线（Gyeongui-Jungang Line）
| 英文 | 韩文 | 英文 | 韩文 |
| 서울역 | Seoul Station |
| 홍대입구 | Hongdae (Hongik Univ.) | Hongdae Entrance |
| 공덕 | Gongdeok |
| 효창공원앞 | Hyochang Park |
| 용산 | Yongsan |
| 옥수 | Oksu |
| 왕십리 | Wangsimni |
| 청량리 | Cheongnyangni |
| DMC | Digital Media City |
| 수색 | Susaek |
| 일산 | Ilsan |
| 파주 | Paju |

### 机场铁路线（Airport Railroad）
| 英文 | 韩文 | 英文 | 韩文 |
| 서울역 | Seoul Station |
| 공덕 | Gongdeok |
| 홍대입구 | Hongdae Entrance |
| 디지털미디어시티 | Digital Media City |
| 김포공항 | Gimpo Airport |
| 인천공항1터미널 | Incheon Airport T1 |
| 인천공항2터미널 | Incheon Airport T2 |
| 청라국제도시 | Cheongna International City |

### 水原盆唐线（Suin-Bundang Line）
| 英文 | 韩文 | 英文 | 韩文 |
| 왕십리 | Wangsimni | Wangsimni |
| 선릉 | Seolleung |
| 강남구청 | Gangnam-gu Office |
| 선정릉 | Seonjeongneung |
| 정자 | Jeongja |
| 미금 | Migeum |
| 오리 | Ori |
| Jukjeon | Jukjeon |
| 수원 | Suwon |
| 인천 | Incheon |

---

## 使用示例

**实时到站信息**
```bash
curl "http://swopenAPI.seoul.go.kr/api/subway/${SEOUL_OPENAPI_KEY}/json/realtimeStationArrival/0/10/강남"
```

**站点查询**
```bash
curl "http://openapi.seoul.go.kr:8088/${SEOUL_OPENAPI_KEY}/json/SearchInfoBySubwayNameService/1/10/강남"
```

**路线查询**
```bash
curl -G "https://apis.data.go.kr/B553766/path/getShtrmPath?serviceKey=${DATA_GO_KR_KEY}&dataType=JSON" \
  --data-urlencode "dptreStnNm=신도림" \
  --data-urlencode "arvlStnNm=서울역" \
  --data-urlencode "searchDt=$(date '+%Y-%m-%d %H:%M:%S')"
```

**服务提醒**
```bash
curl "https://apis.data.go.kr/B553766/ntce/getNtceList?serviceKey=${DATA_GO_KR_KEY}&dataType=JSON&pageNo=1&numOfRows=10"
```

---

## 输出格式指南

### 实时到站信息

**韩文格式：**
```
[강남역 도착 정보]

| 호선 | 방향 | 도착 | 위치 | 유형 |
|------|------|------|------|------|
| 2호선 | 성수행 | 3분 | 역삼 | 일반 |
```

**英文格式：**
```
[Gangnam Station Arrivals]

| Line | Direction | Arrival | Location | Type |
|------|-----------|---------|----------|------|
| Line 2 | Seongsu-bound | 3 min | Yeoksam | Regular |
```

### 站点查询**

**韩文格式：**
```
[강남역]

| 호선 | 역코드 | 외부코드 |
|------|--------|----------|
| 2호선 | 222 | 0222 |
```

**英文格式：**
```
[Gangnam Station]

| Line | Station Code | External Code |
|------|--------------|---------------|
| Line 2 | 222 | 0222 |
```

### 路线查询**

**韩文格式：**
```
[강남 -> 홍대입구]

소요시간: 38분 | 거리: 22.1 km | 요금: 1,650원 | 환승: 1회

1. 09:03 강남 출발 (2호선 성수방면)
2. 09:18 신도림 환승 (2호선 -> 1호선)
3. 09:42 홍대입구 도착
```

**英文格式：**
```
[Gangnam -> Hongdae]

Time: 38 min | Distance: 22.1 km | Fare: 1,650 KRW | Transfers: 1

1. 09:03 Depart Gangnam (Line 2 towards Seongsu)
2. 09:18 Transfer at Sindorim (Line 2 -> Line 1)
3. 09:42 Arrive Hongdae
```

### 服务提醒**

**韩文格式：**
```
[운행 알림]

[1호선] 종로3가역 무정차 (15:00 ~ 15:22)
- 코레일 열차 연기 발생으로 인함

[2호선] 정상 운행
```

**英文格式：**
```
[Service Alerts]

[Line 1] Jongno 3-ga Non-stop (15:00 ~ 15:22)
- Due to smoke from Korail train

[Line 2] Normal operation
```

### 错误**

**韩文格式：**
```
오류: 역을 찾을 수 없습니다.
"강남" (역 이름만)으로 검색해 보세요.
```

**英文格式：**
```
Error: Station not found.
Try searching with "Gangnam" (station name only).
```

### API密钥错误**

**韩文格式：**
```
오류: API 인증키가 설정되지 않았습니다.
환경 변수를 설정해주세요: SEOUL_OPENAPI_KEY

발급 안내:
- 서울열린데이터광장: https://data.seoul.go.kr
- 공공데이터포털: https://www.data.go.kr
```

**英文格式：**
```
Error: API key is not configured.
Please set environment variable: SEOUL_OPENAPI_KEY

Get your API key:
- Seoul Open Data Plaza: https://data.seoul.go.kr
- Korea Public Data Portal: https://www.data.go.kr
```

**韩文格式：**
```
오류: API 인증키가 유효하지 않습니다.
인증키를 확인해주세요.
```

**英文格式：**
```
Error: Invalid API key.
Please verify your API key.
```
---
name: ns-trains
description: 使用 NS API 查看荷兰的火车时刻表、发车时间、运行中断情况，并规划行程。非常适合日常通勤前的查询。
metadata: {"openclaw":{"emoji":"🚆","requires":{"bins":["node"],"env":["NS_SUBSCRIPTION_KEY"]},"primaryEnv":"NS_SUBSCRIPTION_KEY"}}
---

# NS Trains Skill

使用荷兰国家铁路（NS，Nederlandse Spoorwegen）的官方API来查询荷兰火车的班次、发车时间、运行状况，并规划出行路线。

## 设置

### 1. 获取NS订阅密钥

1. 访问 [NS API门户](https://apiportal.ns.nl/)
2. 注册账户并订阅 **Ns-App** 服务（提供免费试用）
3. 复制您的 **主订阅密钥**

### 2. 设置环境变量

```bash
export NS_SUBSCRIPTION_KEY="your-subscription-key-here"   # preferred
# Back-compat:
export NS_API_KEY="$NS_SUBSCRIPTION_KEY"                   # legacy name still supported

# Optional: Configure commute stations for quick shortcuts
export NS_HOME_STATION="Utrecht Centraal"
export NS_WORK_STATION="Amsterdam Zuid"
```

为确保安全，建议通过运行时的秘密管理机制来设置这些环境变量，而不是将它们存储在任何地方。请避免打印或分享您的订阅密钥。

## 快速使用方法

### 🚆 通勤路线查询
```bash
node {baseDir}/scripts/commute.mjs --to-work   # Morning: Home → Work
node {baseDir}/scripts/commute.mjs --to-home   # Evening: Work → Home
```

### 规划任意行程
```bash
node {baseDir}/scripts/journey.mjs --from "Utrecht Centraal" --to "Amsterdam Zuid"
```

### 查询车站的出发信息
```bash
node {baseDir}/scripts/departures.mjs --station "Amsterdam Centraal"
```

### 查询车站的到达信息
```bash
node {baseDir}/scripts/arrivals.mjs --station "Rotterdam Centraal"
```

### 搜索车站名称
```bash
node {baseDir}/scripts/stations.mjs amsterdam
node {baseDir}/scripts/stations.mjs --search "den haag"
```

### 查看当前的运行异常情况
```bash
node {baseDir}/scripts/disruptions.mjs
node {baseDir}/scripts/disruptions.mjs --from "Utrecht" --to "Amsterdam"
```

## 自然语言交互

只需简单提问：
- “下一班去阿姆斯特丹的火车是什么时候？”
- “查询从乌得勒支到鹿特丹的火车班次”
- “今天有火车延误吗？”
- “规划我的通勤路线”
- “火车什么时候到达？”

## 输出结果

返回的行程信息包括：
- 出发/到达时间
- 实时延误情况
- 行程时长
- 需要换乘的站点
- 车站台编号
- 运行异常警告
- 乘客拥挤程度预测（🟢 低 / 🟡 中等 / 🔴 高）

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `commute.mjs [工作站\|起点站]` | 快速查询通勤路线（需要指定 NS_HOME_STATION 和 NS_WORK_STATION） |
| `journey.mjs --起点 X --终点 Y` | 规划任意两个车站之间的行程 |
| `departures.mjs --车站 X` | 查询车站的出发班次 |
| `arrivals.mjs --车站 X` | 查询车站的到达班次 |
| `stations.mjs [查询]` | 搜索车站名称 |
| `disruptions.mjs` | 查看当前的运行异常情况 |

## 使用的API端点

- `/reisinformatie-api/api/v3/trips` - 旅程规划
- `/reisinformatie-api/api/v2/arrivals` - 到达信息
- `/reisinformatie-api/api/v2/departures` - 出发信息
- `/reisinformatie-api/api/v3/disruptions` - 运行异常信息
- `/reisinformatie-api/api/v2/stations` - 车站查询

## 参考资料

- NS API门户：https://apiportal.ns.nl/
- 文档说明：https://apiportal.ns.nl/startersguide
- 免费试用限制：每天5000次请求
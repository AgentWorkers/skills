---
name: rejseplanen
description: 通过 Rejseplanen API 查询丹麦公共交通的出发时间、到达时间以及行程规划信息
metadata: {"clawdbot":{"emoji":"🚂","os":["linux","darwin","win32"],"requires":{"bins":["node"]}}}
---

# Rejseplanen - 丹麦公共交通

通过 Rejseplanen API 查询实时火车和公交车的发车、到站信息，并规划行程。

## 命令

### 搜索车站

```bash
node {baseDir}/dist/rejseplanen.js search "København"
```

### 发车信息

```bash
node {baseDir}/dist/rejseplanen.js departures Odense
node {baseDir}/dist/rejseplanen.js departures Odense --trains
node {baseDir}/dist/rejseplanen.js departures Odense --trains --to Aalborg
```

### 到站信息

```bash
node {baseDir}/dist/rejseplanen.js arrivals Aalborg
node {baseDir}/dist/rejseplanen.js arrivals Aalborg --trains --from Odense
```

### 行程规划

```bash
node {baseDir}/dist/rejseplanen.js trip Odense Aalborg
node {baseDir}/dist/rejseplanen.js trip Odense "Aalborg Vestby" --time 07:00
```

### 行程详情

显示特定火车的所有停靠站：

```bash
node {baseDir}/dist/rejseplanen.js journey Odense 75
```

## 选项

- `--trains` - 仅显示火车信息
- `--buses` - 仅显示公交车信息
- `--to <车站>` - 按目的地筛选发车信息
- `--from <车站>` - 按起点筛选到站信息
- `--time HH:MM` - 在指定时间之后发车的列车
- `--output json|text` - 输出格式（默认：文本）
- `--json` - `--output json` 的简写形式

## JSON 输出

如需用于程序解析，请使用 `--json`：

```bash
node {baseDir}/dist/rejseplanen.js departures Odense --json
```

## 提示

- 使用 `search` 命令查找车站 ID，然后保存常用的车站 ID 以加快查询速度
- 可以直接使用车站 ID 而不是车站名称（例如，Odense 的 ID 为 `008600512`）
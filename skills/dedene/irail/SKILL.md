---
name: irail-cli
description: >
  Query Belgian railway (NMBS/SNCB) schedules via the irail CLI. Use when the user wants
  train departures, connections between stations, train compositions, or service disruptions.
  Triggered by mentions of Belgian trains, NMBS, SNCB, iRail, train schedules, or railway delays.
license: MIT
homepage: https://github.com/dedene/irail-cli
metadata:
  author: dedene
  version: "1.1.0"
  openclaw:
    requires:
      bins:
        - irail
      anyBins:
        - jq
    install:
      - kind: brew
        tap: dedene/tap
        formula: irail
        bins: [irail]
      - kind: go
        package: github.com/dedene/irail-cli/cmd/irail
        bins: [irail]
---

# irail-cli

这是一个用于查询比利时铁路（NMBS/SNCB）信息的命令行工具（CLI），通过 [iRail API](https://api.irail.be/) 实现。无需进行身份验证。

## 快速入门

```bash
# Station departures
irail liveboard Brugge

# Find connections
irail connections Brugge Leuven

# Check disruptions
irail disturbances
```

## 身份验证

**无需身份验证。** iRail API 是公开且免费使用的。

## 核心规则

1. **在程序化解析输出时，务必使用 `--json` 标志。**
2. **车站名称具有灵活性**——支持部分匹配，多词名称需要用引号括起来。
3. **时间格式**：HH:MM（24小时制）；日期格式：YYYY-MM-DD。
4. **语言选项**：nl（荷兰语）、fr（法语）、en（英语）、de（德语）（默认为 nl）。

## 输出格式

| 标志 | 格式 | 用途 |
|------|--------|----------|
| （默认） | 表格形式 | 适合用户查看，包含颜色提示 |
| `--json` | JSON 格式 | 适用于代理程序或脚本解析 |

颜色说明：
- 红色：列车延误
- 黄色：站台变更

## 工作流程

### 实时信息（列车到发）

```bash
# Departures from station
irail liveboard Brugge
irail liveboard "Brussel-Centraal"

# Arrivals instead of departures
irail liveboard Brugge --arrivals

# Specific date/time
irail liveboard Brugge --time 09:00 --date 2025-02-15

# JSON for scripting
irail liveboard Brugge --json

# Different language
irail liveboard Brugge --lang en
```

### 路线规划（查询换乘信息）

```bash
# Find routes
irail connections Brugge Leuven

# Specific departure time
irail connections Brugge Leuven --time 09:00

# Arrive by time (instead of depart at)
irail connections Brugge Leuven --time 14:00 --arrive-by

# More results
irail connections Brugge Leuven --results 10

# JSON for parsing
irail connections Brugge Leuven --json
```

### 车站信息

```bash
# List all stations
irail stations

# Search stations
irail stations --search bruss
irail stations --search gent

# JSON for scripting
irail stations --json
```

### 列车信息

```bash
# Show train information
irail vehicle IC1832

# Include all stops
irail vehicle IC1832 --stops

# JSON output
irail vehicle IC1832 --json
```

### 列车编组

```bash
# Show train composition (seats, amenities)
irail composition S51507
irail composition IC1832

# JSON for parsing
irail composition S51507 --json
```

### 服务中断信息

```bash
# All current disruptions
irail disturbances

# Only planned works
irail disturbances --type planned

# Only unplanned disruptions
irail disturbances --type disturbance

# JSON for scripting
irail disturbances --json
```

## 脚本示例

```bash
# Get next train to destination
irail connections Brugge Leuven --json | jq -r '.[0].departure'

# Find station ID
irail stations --search "brussel" --json | jq -r '.[0].id'

# Check if delays exist on liveboard
irail liveboard Brugge --json | jq '[.[] | select(.delay > 0)] | length'

# Get platform for next departure
irail liveboard Brugge --json | jq -r '.[0].platform'

# List all disruptions
irail disturbances --json | jq -r '.[].title'
```

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `IRAIL_LANG` | 默认语言（nl, fr, en, de） |
| `IRAIL_JSON` | 默认输出格式为 JSON |
| `NO_COLOR` | 禁用颜色显示 |

## 语言选项

| 代码 | 语言 |
|------|----------|
| `nl` | 荷兰语（默认） |
| `fr` | 法语 |
| `en` | 英语 |
| `de` | 德语 |

```bash
irail liveboard Brugge --lang fr
irail connections Brugge Leuven --lang en
```

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `liveboard` | 查看车站的列车到发信息 |
| `connections` | 查询两个车站之间的路线及换乘信息 |
| `stations` | 列出/搜索车站 |
| `vehicle` | 查看列车信息及停靠站 |
| `composition` | 查看列车车厢编组 |
| `disturbances` | 查看列车服务中断情况 |
| `completion` | 提供 Shell 命令的补全功能 |

## 常用操作模式

### 检查列车是否延误

```bash
irail vehicle IC1832 --json | jq '.delay // 0'
```

### 查询包含换乘的路线

```bash
irail connections Brugge Leuven --json | jq '.[0].vias | length'
```

### 查找仅有的直达列车

```bash
irail connections Brugge Leuven --json | jq '[.[] | select(.vias == null or (.vias | length) == 0)]'
```

## 使用指南

- 无需身份验证——API 是公开的。
- 在循环中使用 API 时，请注意控制请求间隔，以避免过度加载服务器。
- 车站名称不区分大小写，支持部分匹配。
- 延误时间以秒为单位（需除以 60 转换为分钟）。

## 安装方法

```bash
brew install dedene/tap/irail
```
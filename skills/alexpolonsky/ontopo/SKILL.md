---
name: ontopo
version: 1.0.0
description: 在 Ontopo 上可以搜索以色列的餐厅、查看餐厅的桌位空缺情况、浏览菜单，并获取预订链接。相关功能包括：“餐厅预订”（restaurant reservation）、“桌位预订”（table booking）、“ontopo”（Ontopo）、“在以色列哪里吃饭”（where to eat in Israel）、“מסעדה”（restaurant）、“הזמנת שולחן”（table reservation）、“תפריט”（menu）、“ארוחת ערב”（dinner）、“אונטופו”（Ontopo）、“איפה לאכול”（where to eat）。
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-ontopo
metadata: {"openclaw": {"emoji": "🍽️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}, "install": [{"kind": "uv", "package": "httpx", "label": "Install httpx via pip/uv"}]}}
---
# Ontopo餐厅搜索

在Ontopo平台上，您可以搜索以色列餐厅、查看餐厅的座位情况、浏览菜单，并获取直接预订链接。

> **免责声明**：这是一个非官方工具，与Ontopo无关，也未获得其授权或支持。该工具使用的API用于查询餐厅的可用性信息，但这些信息可能并不完全反映餐厅的实际营业情况。该工具本身不负责预订操作——它仅生成预订链接，需用户在Ontopo网站上手动完成预订。所提供的功能“按原样”提供，不附带任何形式的保证。

## 快速入门

```bash
# Search for a restaurant
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"

# Find available restaurants for tonight
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 19:00 --city tel-aviv
```

## 命令

### cities
列出支持的城市。
```bash
python3 {baseDir}/scripts/ontopo-cli.py cities
python3 {baseDir}/scripts/ontopo-cli.py cities --json
```

### categories
列出餐厅的分类。
```bash
python3 {baseDir}/scripts/ontopo-cli.py categories
```

### search
按名称搜索餐厅。
```bash
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"
python3 {baseDir}/scripts/ontopo-cli.py search "sushi" --city tel-aviv
python3 {baseDir}/scripts/ontopo-cli.py search "taizu" --json
```

### available
查找在指定日期和时间有空位的餐厅。日期和时间为可选参数。
```bash
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 19:00
python3 {baseDir}/scripts/ontopo-cli.py available tomorrow 20:00 --city tel-aviv
python3 {baseDir}/scripts/ontopo-cli.py available +3 19:00 --party-size 4
```

### check
检查特定餐厅的可用性。支持使用餐厅名称或ID进行查询。
```bash
python3 {baseDir}/scripts/ontopo-cli.py check taizu tomorrow 19:00
python3 {baseDir}/scripts/ontopo-cli.py check taizu +2 20:00
python3 {baseDir}/scripts/ontopo-cli.py check 36960535 tomorrow 19:00 --party-size 4
```

### range
查询指定日期范围内的餐厅可用性。时间参数为可选（默认值为19:00, 20:00）。
```bash
python3 {baseDir}/scripts/ontopo-cli.py range taizu tomorrow +3
python3 {baseDir}/scripts/ontopo-cli.py range 36960535 tomorrow +5 --times "18:00,19:00,20:00"
python3 {baseDir}/scripts/ontopo-cli.py range taizu +1 +7 --party-size 4
```

### menu
查看餐厅菜单（支持使用过滤器）。
```bash
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792 --section drinks
python3 {baseDir}/scripts/ontopo-cli.py menu 66915792 --search "pasta" --max-price 100
```

### info
获取餐厅的详细信息。
```bash
python3 {baseDir}/scripts/ontopo-cli.py info 36960535
python3 {baseDir}/scripts/ontopo-cli.py info 66915792 --json
```

### url
获取餐厅的预订链接。
```bash
python3 {baseDir}/scripts/ontopo-cli.py url 36960535
python3 {baseDir}/scripts/ontopo-cli.py url 66915792 --locale he
```

## 选项参考

| 选项          | 命令                | 描述                          |
|--------------|------------------|-------------------------------------------|
| `--json`       | all                | 以JSON格式输出所有信息                |
| `--locale`      | search, info, url         | 设置语言为“en”或“he”                    |
| `--city`       | available, search         | 过滤城市（例如：tel-aviv, jerusalem等）         |
| `--party-size`    | available, check, range      | 指定客人数量（默认值：2）                   |
| `--times`      | range               | 以逗号分隔的时间段（默认值：19:00, 20:00）             |
| `--section`     | menu               | 按菜单部分筛选菜单项目                 |
| `--search`      | menu               | 按名称搜索菜单项目                     |
| `--min-price`    | menu               | 设置最低价格筛选条件                 |
| `--max-price`    | menu               | 设置最高价格筛选条件                 |

## 日期/时间格式

**日期**：`YYYY-MM-DD`、`today`、`tomorrow`、`+N`（从现在起N天）
**时间**：`HH:MM`、`HHMM`、`7pm`、`19:30`

## 支持的城市

tel-aviv、jerusalem、haifa、herzliya、raanana、ramat-gan、netanya、ashdod、ashkelon、beer-sheva、eilat、modiin、rehovot、rishon-lezion、petah-tikva、holon、kfar-saba、hod-hasharon、caesarea

## 工作流程示例

```bash
# 1. Search for restaurant
python3 {baseDir}/scripts/ontopo-cli.py search "taizu"
# Note the venue ID from results (e.g., 36960535)

# 2. Check availability
python3 {baseDir}/scripts/ontopo-cli.py check 36960535 tomorrow --time 19:00

# 3. View menu
python3 {baseDir}/scripts/ontopo-cli.py menu 36960535

# 4. Get booking link
python3 {baseDir}/scripts/ontopo-cli.py url 36960535
```

## 注意事项

- **手动预订**：工具生成的链接需用户在Ontopo网站上完成预订操作。
- **无需API密钥**：直接调用支撑该网站的API进行数据查询。
- **双语支持**：支持希伯来语和英语界面。
- **实时数据**：餐厅的可用性信息会从Ontopo平台实时获取。
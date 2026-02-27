---
name: jlm-coffee
version: 2.0.0
description: 根据名称、设施、评分和营业时间搜索耶路撒冷的特色咖啡店。当用户询问“耶路撒冷的咖啡店”、“耶路撒冷的咖啡馆”、“耶路撒冷的咖啡屋”、“耶路撒冷的特色咖啡”、“在耶路撒冷哪里可以买到咖啡”、“适合带狗去的咖啡馆”、“耶路撒冷的笔记本电脑咖啡馆”或“耶路撒冷现在营业的咖啡店”时，可以使用此功能。
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-jlm-coffee
license: MIT
metadata: {"openclaw": {"emoji": "☕", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 耶路撒冷咖啡查找器

该工具用于搜索耶路撒冷的专业咖啡店，提供评分、设施信息、营业时间、用户评价以及店铺位置等详细信息。数据来源于 [coffee.amsterdamski.com](https://coffee.amsterdamski.com)，由 [Shaul Amsterdamski](https://x.com/amsterdamski2) ([@amsterdamski2](https://x.com/amsterdamski2)) 创建和维护。

> 数据来自网站维护者提供的官方公共 JSON 文件，可能不反映最新状态。数据按“原样”提供，不附带任何形式的保证。

## 快速入门

```bash
# List all coffee shops
python3 {baseDir}/scripts/jlm-coffee.py list

# Find a shop by name
python3 {baseDir}/scripts/jlm-coffee.py search "סיבריס"
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `list` | 列出所有经过审核的专业咖啡店 |
| `search <查询>` | 按名称（希伯来语或英语）搜索咖啡店 |
| `get <id_or_name>` | 获取特定咖啡店的详细信息 |
| `filter <设施>` | 按设施（如无线网络、是否允许狗进入、是否符合犹太饮食规范等）筛选咖啡店 |
| `open-now` | 显示当前营业中的咖啡店 |
| `amenities` | 列出所有可用的设施筛选条件 |
| `surprise` | 随机选择一家咖啡店（优先选择营业中的店铺） |

## 搜索与筛选示例

```bash
# Search by name (Hebrew or English)
python3 {baseDir}/scripts/jlm-coffee.py search "רוסטרס"
python3 {baseDir}/scripts/jlm-coffee.py search "Cafe Pepa"

# Filter by amenity
python3 {baseDir}/scripts/jlm-coffee.py filter wifi
python3 {baseDir}/scripts/jlm-coffee.py filter dogs
python3 {baseDir}/scripts/jlm-coffee.py filter kosher
python3 {baseDir}/scripts/jlm-coffee.py filter laptop

# Shops open right now
python3 {baseDir}/scripts/jlm-coffee.py open-now

# Full details for a shop
python3 {baseDir}/scripts/jlm-coffee.py get "בארוק"
python3 {baseDir}/scripts/jlm-coffee.py get EljFiggwObssQpypWMf0
```

## 选项参考

| 选项 | 命令 | 描述 |
|--------|----------|-------------|
| `--json` | all | 以 JSON 格式输出（适合脚本使用） |
| `--no-color` | all | 禁用彩色输出（自动检测非终端设备） |

## 设施筛选条件

| 关键字 | 标签 | 别名 |
|-----|-------|---------|
| `wifi` | 无线网络 | |
| `dogs` | 允许狗进入 | dog, dog-friendly |
| `laptop` | 适合使用笔记本电脑 | laptops |
| `outdoor` | 户外座位 | outside, terrace |
| `accessible` | 适合轮椅使用者 | wheelchair |
| `vegan` | 提供纯素食品 | vegan |
| `kids` | 适合儿童 | children, kid-friendly |
| `quiet` | 安静的环境 | |
| `smoking` | 吸烟区 | |
| `local-roasting` | 当地烘焙的咖啡 | roasting |
| `sell-beans` | 出售咖啡豆 | beans |
| `filter-coffee` | 筛选咖啡类型 | filter |
| `kosher` | 符合犹太饮食规范 | kosher |
| `open-saturday` | 周六营业 | saturday, shabbat |
| `power` | 电源插座 | outlets |
| `parking` | 停车设施 | parking |

## 工作流程示例

```bash
# 1. Find shops with WiFi and look at the list
python3 {baseDir}/scripts/jlm-coffee.py filter wifi

# 2. Get details on one that looks good
python3 {baseDir}/scripts/jlm-coffee.py get "מטאפורה"

# 3. Check what's open right now
python3 {baseDir}/scripts/jlm-coffee.py open-now

# 4. Feeling lucky? Get a random pick
python3 {baseDir}/scripts/jlm-coffee.py surprise
```

## 注意事项

- **社区精选**：所有咖啡店信息均由社区成员审核和推荐。
- **数据来源**：数据来自网站维护者提供的公共 JSON 文件（无需 API 密钥或 Firestore）。
- **双语支持**：支持使用希伯来语和英语名称进行搜索。
- **营业时间**：基于 Google Places 提供的信息，并由网站进行缓存。
- **包含评价**：店铺详情中包含用户的评价和评分。
- **颜色显示**：终端输出采用 ANSI 颜色（支持 `NO_COLOR` 环境变量和 `--no-color` 标志）。
- **命令行快捷方式**：可通过创建符号链接将工具安装为 `jlm-coffee`。
- **无依赖库**：仅使用 Python 标准库（`urllib`, `json`）。
- **快速缓存**：本地缓存有效期为 15 分钟，一次请求即可满足所有命令的需求。
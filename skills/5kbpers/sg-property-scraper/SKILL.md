---
name: sg-property-scraper
description: 使用灵活的过滤条件搜索新加坡的房产租赁和出售信息。适用于需要查找新加坡房产、查询租赁或出售房源、查看地铁站附近的房价，或比较通勤时间的情况。支持按房源类型（租赁/出售）、房产类型（组屋/公寓/独立屋）、卧室数量、浴室数量、价格范围、面积、上市年份、地铁站代码、距离地铁站的距离、房间类型、房源可用性以及通勤时间等进行筛选。搜索结果将以 JSON 格式输出到标准输出（stdout）。
metadata:
  {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":"GOOGLE_MAPS_API_KEY"}}
---
# 新加坡房产爬虫

该脚本通过HTTP请求抓取新加坡的房产信息，并返回结构化的JSON数据。

## 脚本位置

```
scripts/scrape.py
```

该脚本位于`SKILL`目录下。执行方式如下：
```bash
python3 <SKILL_DIR>/scripts/scrape.py [OPTIONS]
```

## 所需依赖

- Python 3.8及以上版本
- 使用`pip install curl_cffi beautifulsoup4 lxml`安装相关库
- 可选：设置`GOOGLE_MAPS_API_KEY`环境变量（用于计算通勤时间，需使用Google Routes API）

## 快速入门

```bash
# Search 2BR condos for rent under SGD 4000 near Circle Line
python3 scripts/scrape.py \
  --listing-type rent --bedrooms 2 --max-price 4000 \
  --property-type-group N --mrt-range CC:20-24 \
  --output json

# JSON input mode (easier for AI tools)
python3 scripts/scrape.py --json '{
  "listingType": "rent",
  "bedrooms": 2,
  "maxPrice": 4000,
  "propertyTypeGroup": ["N"],
  "mrtStations": ["CC20","CC21","CC22","CC23","CC24"]
}'

# Dry run: print URL only without scraping
python3 scripts/scrape.py --dry-run --listing-type rent --bedrooms 3
```

## 过滤参数

| 标志 | URL参数 | 类型 | 说明 |
|------|-----------|------|-------------|
| `--listing-type` | `listingType` | 字符串 | `rent`（出租）或`sale`（出售） |
| `--property-type-group` | `propertyTypeGroup` | 字符串（可重复） | `N`：公寓；`L`：独立屋；`H`：组屋 |
| `--entire-unit-or-room` | `entireUnitOrRoom` | 字符串 | `ent`：仅显示整个单元；省略则显示所有单元 |
| `--room-type` | `roomType` | 字符串（可重复） | `master`：主卧室；`common`：公共区域；`shared`：共享房间 |
| `--bedrooms` | `bedrooms` | 整数 | `-1`：单间；`0`：工作室；`1`-`5`：卧室数量 |
| `--bathrooms` | `bathrooms` | 整数 | 浴室数量 |
| `--min-price` | `minPrice` | 整数 | 最低价格（新加坡元） |
| `--max-price` | `maxPrice` | 整数 | 最高价格（新加坡元） |
| `--min-size` | `minSize` | 整数 | 最小面积（平方英尺） |
| `--max-size` | `maxSize` | 整数 | 最大面积（平方英尺） |
| `--min-top-year` | `minTopYear` | 整数 | 最早建成年份 |
| `--max-top-year` | `maxTopYear` | 整数 | 最晚建成年份 |
| `--distance-to-mrt` | `distanceToMRT` | 浮点数 | 到MRT的最大距离（公里，例如`0.5`、`0.75`） |
| `--availability` | `availability` | 整数 | 房产可用性筛选 |
| `--mrt-station` | `mrtStations` | 字符串（可重复） | MRT站代码，例如`CC20` |
| `--mrt-range` | `mrtStations` | 字符串（可重复） | MRT站范围，例如`CC:20-24` |
| `--sort` | `sort` | 字符串 | `date`、`price`、`psf`、`size` | 排序方式 |
| `--order` | `order` | 字符串 | `asc`、`desc` | 排序顺序 |
| `--commute-to` | `commuteTo` | 字符串 | 通勤目的地地址（需要`GOOGLE_MAPS_API_KEY`） |

## 卧室/房间筛选逻辑

- `--entire-unit-or-room ent --bedrooms 4`：显示4间卧室的整个单元 |
- `--entire-unit-or-room ent --bedrooms 0`：显示工作室 |
- `--bedrooms -1 --room-type master --room-type common`：显示主卧室或公共区域的房间租赁信息 |
- 省略`--entire-unit-or-room`参数可同时显示整个单元和房间信息 |

## MRT站代码格式

- 单个站点：`--mrt-station CC20`
- 范围：`--mrt-range CC:20-24`（包含CC20、CC21、CC22、CC23、CC24）
- 多个站点：使用多个`--mrt-station`参数
- 在JSON中：`"mrtStations": ["CC20", "EW15"]` 或 `[["CC", [20, 24]]`（元组格式）

请参阅`references/params.md`以获取完整的213个有效MRT站代码列表。

## 执行参数

| 标志 | 说明 |
|------|-------------|
| `--pages N` | 抓取的页面数（默认：1） |
| `--dry-run` | 生成并打印URL，不执行抓取 |
| `--no-validate` | 跳过参数验证 |
| `--timeout N` | HTTP请求超时时间（秒，默认：30） |
| `--raw-param K=V` | 额外的URL查询参数（可重复） |
| `--output json\|text\|none` | 输出格式（默认：通过管道输出时为JSON） |
| `--verbose` | 在标准错误输出（stderr）中显示详细日志 |

## JSON输入方式

- 使用`--json`参数以JSON字符串形式传递筛选条件；键名应与URL参数名称保持一致（驼峰式命名规则）：
```bash
python3 scripts/scrape.py --json '{
  "listingType": "rent",
  "propertyTypeGroup": ["N"],
  "bedrooms": 2,
  "bathrooms": 2,
  "maxPrice": 4000,
  "mrtStations": ["EW16", "EW17", "EW18"],
  "distanceToMRT": 0.75,
  "minTopYear": 1990
}'
```

或者从文件加载筛选条件：`--config filters.json`

## 输出格式

结果以JSON数组形式输出到标准输出（无结果时输出`[]`）：
```json
[
  {
    "id": "23744236",
    "name": "Kingsford Waterbay",
    "price": "S$ 3,900 /mo",
    "psf": "S$ 4.53 psf",
    "address": "68 Upper Serangoon View",
    "bedrooms": "2",
    "bathrooms": "2",
    "area": "861 sqft",
    "type": "Condominium",
    "built": "Built: 2018",
    "availability": "Ready to Move",
    "mrt_distance": "14 min (1.15 km) from SE4 Kangkar LRT Station",
    "list_date": "Listed on Feb 15, 2026 (2d ago)",
    "agent": "May Chong",
    "agency": "PROPNEX REALTY PTE. LTD.",
    "headline": "Perfect work from home unit, river facing, unblocked high floor cozy",
    "link": "https://www.propertyguru.com.sg/listing/for-rent-kingsford-waterbay-23744236",
    "commute_driving": "25 mins",
    "commute_transit": "45 mins"
  }
]
```

## 错误代码

- `0`：成功，找到结果 |
- `1`：参数错误，抓取失败 |
- `2`：成功但未找到任何房源 |

## 代理使用说明

当从AI代理调用此脚本时：
1. 使用`--output json`以结构化格式输出结果（默认通过管道输出） |
2. 使用`--json`参数更便于传递参数 |
3. 使用`--dry-run`预览搜索URL |
4. 如果需要更多结果，使用`--pages N`（每页约20条房源） |
5. 使用`--commute-to`参数指定通勤目的地地址以计算通勤时间（包括驾车和公共交通时间，需设置`GOOGLE_MAPS_API_KEY`）。如果未设置该环境变量，相关字段将默认为空字符串`""` |
6. 当API密钥缺失或计算失败时，`commute_driving`和`commute_transit`字段将显示为空字符串`""`。
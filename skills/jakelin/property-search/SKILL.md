---
name: property-search
description: 在 property.com.au 上搜索澳大利亚的房产信息——包括房产评估、销售历史、社区概况以及房产详情。该平台可用于查询澳大利亚房产的价值、销售记录或相关社区数据。该网站由 REA 集团所有，其活跃的房源信息会链接到 realestate.com.au。
---
# property.com.au 房产研究服务

property.com.au 提供澳大利亚房产相关的查询服务，适用于房产估值、历史销售记录以及周边社区信息的查询——但不支持房源的直接搜索功能。无需使用 API 密钥。

## 按地址查询房产信息

您可以查询任何房产的历史信息、估价及详细资料：

```
https://www.property.com.au/{state}/{suburb}-{postcode}/{street-name}/{number}-pid-{propertyId}/
```

**街道名称格式：**使用小写字母，空格用连字符表示；街道类型可缩写为 `st`（街道）、`rd`（路）、`ave`（大道）、`pl`（广场）、`ct`（购物中心）、`dr`（ Drive）、`cres`（小巷）、`tce`（隧道）等。

### 示例

```
https://www.property.com.au/vic/malvern-3144/como-st/4-pid-6510692/
https://www.property.com.au/vic/armadale-3143/elgin-ave/5-pid-1234567/
```

**单元/公寓格式：** `{unit}-{number}-pid-{id}`

```
https://www.property.com.au/vic/malvern-3144/high-st/203-1269-pid-12345678/
```

## 社区信息

提供社区的中位房价、人口统计数据、学校信息、交通状况及市场数据：

```
https://www.property.com.au/{state}/{suburb}-{postcode}/
```

### 示例

```
https://www.property.com.au/vic/malvern-3144/
https://www.property.com.au/vic/armadale-3143/
```

## 按地点查找待售房源

property.com.au 从 realestate.com.au 获取房源信息，并按州或地区进行筛选：

```
https://www.property.com.au/{state}/buy/
https://www.property.com.au/{state}/{suburb}-{postcode}/buy/
```

### 示例

```
https://www.property.com.au/vic/buy/
https://www.property.com.au/vic/malvern-3144/buy/
https://www.property.com.au/vic/melbourne-city-greater-region/buy/
```

**按房产类型查询：**
```
https://www.property.com.au/{state}/{suburb}-{postcode}/{type}/buy/
```

可选房产类型：`house`（住宅）、`townhouse`（联排别墅）、`apartment-unit`（公寓单元）、`villa`（别墅）、`land`（土地）、`acreage`（土地面积）、`rural`（农村地产）、`block-of-units`（多单元住宅）、`retirement`（退休住宅）。

示例：马尔文（Malvern）地区的联排别墅待售房源：
```
https://www.property.com.au/vic/malvern-3144/townhouse/buy/
```

**注意：**价格和卧室数量等筛选条件通过 JavaScript 实现，不会体现在 URL 中。如需进行筛选查询，请使用 realestate.com.au。

## 房产销售历史

您可以查看特定社区的近期销售记录：

```
https://www.property.com.au/{state}/{suburb}-{postcode}/sold/
```

示例：
```
https://www.property.com.au/vic/malvern-3144/sold/
```

## 街道房源浏览

您可以查看某条街道上的所有房产信息：

```
https://www.property.com.au/{state}/{suburb}-{postcode}/{street-name}/
```

示例：
```
https://www.property.com.au/vic/malvern-3144/como-st/
```

## 学校信息

提供社区附近的学校信息，包括学校等级、所属教育阶段及学生人数：

```
https://www.property.com.au/{state}/{suburb}-{postcode}/schools/{school-name}-sid-{schoolId}/
```

学校信息会自动显示在社区页面上。

## 何时使用 property.com.au 与其他网站

| 需求 | 最适合的网站 |
|------|-----------|
| **使用筛选条件查询房源** | realestate.com.au 或 domain.com.au |
| **房产估价** | property.com.au |
| **房产销售历史** | property.com.au |
| **社区中位房价** | property.com.au 或 domain.com.au |
| **比较不同房产** | realestate.com.au |

## 限制事项

- 房源搜索的筛选条件（价格、卧室数量、类型）仅通过 JavaScript 实现，无法直接通过 URL 传递；
- 活跃房源的链接会重定向至 realestate.com.au；
- 房产 ID（pid）可能需要通过搜索或社区浏览功能获取；
- `web_fetch` 功能可能会被屏蔽（与 realestate.com.au 采用相同的反爬虫机制）。
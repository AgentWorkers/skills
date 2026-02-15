---
name: rea-search
description: 通过构建搜索 URL 和房源列表 URL，在 realestate.com.au 上搜索房产信息。该功能适用于在 realestate.com.au 上查找用于购买、租赁或出售的澳大利亚房产。支持构建筛选后的搜索 URL（包括郊区、价格、卧室数量、房产类型等信息），以及单独的房源列表 URL。
---
# realestate.com.au 搜索

可以构建 realestate.com.au 的搜索 URL，无需 API 密钥。

## 买房搜索 URL

```
https://www.realestate.com.au/buy/property-{types}-{filters}-in-{location}/list-{page}
```

### 房产类型

使用 `+` 进行组合：`house`（独立住宅）、`townhouse`（联排别墅）、`unit+apartment`（公寓单元）、`villa`（别墅）、`land`（土地）、`rural`（乡村房产）、`unitblock`（公寓楼）、`acreage`（土地面积）

### 过滤条件（位于路径中）

- 卧室数量：`with-{n}-bedrooms`（至少 {n} 个卧室）
- 价格：`between-{min}-{max}`（{min} 至 {max} 澳元之间；若不限制卧室数量或价格范围，则省略相应的参数）

### 地点格式

- 单个郊区：`{suburb},+{state}+{postcode}`（郊区名称、州名、邮政编码）
- 多个郊区：用 `%3b+` （编码后的分号加空格）分隔
- 仅输入邮政编码：`{postcode}`

### 示例

- 马尔文（Malvern）的联排别墅：
```
https://www.realestate.com.au/buy/property-townhouse-in-malvern,+vic+3144/list-1
```

- 马尔文（Malvern）中 3 个及以上卧室的联排别墅：
```
https://www.realestate.com.au/buy/property-townhouse-with-3-bedrooms-in-malvern,+vic+3144/list-1
```

- 马尔文（Malvern）价格低于 250 万澳元的独立住宅和联排别墅：
```
https://www.realestate.com.au/buy/property-house-townhouse-between-1000000-2500000-in-malvern,+vic+3144/list-1
```

- 多个郊区及价格范围：
```
https://www.realestate.com.au/buy/property-house-townhouse-between-1000000-2000000-in-malvern,+vic+3144%3b+armadale,+vic+3143/list-1
```

- 仅按邮政编码查询：
```
https://www.realestate.com.au/buy/property-house-townhouse-in-3144/list-1
```

## 已售房产

将 `/buy/` 替换为 `/sold/`：
```
https://www.realestate.com.au/sold/property-house-in-malvern,+vic+3144/list-1
```

## 单个房源详情 URL

```
https://www.realestate.com.au/property-{type}-{state}-{suburb}-{listingId}
```

示例：
```
https://www.realestate.com.au/property-house-vic-malvern-143160680
```

## 郊区概况

```
https://www.realestate.com.au/neighbourhoods/{suburb}-{postcode}-{state}
```

示例：
```
https://www.realestate.com.au/neighbourhoods/malvern-3144-vic
```

## 分页

将 `/list-1` 更改为 `/list-2`、`/list-3` 等

## 通过 `web_fetch` 获取数据

直接通过 `web_fetch` 获取数据通常会被限制（429 错误码，表示达到请求限制或存在反爬虫机制）。

**解决方法：使用 DDG 网站搜索：**
```
web_fetch(url="https://lite.duckduckgo.com/lite/?q=site%3Arealestate.com.au+malvern+vic+3144+house+3+bedroom&kl=au-en", extractMode="text", maxChars=8000)
```

该方法可以获取 REA 的房源列表 URL 及基本信息。

## 限制因素

- 使用 `web_fetch` 从 REA 网站获取数据时通常会遇到 429 错误（请求次数限制）
- 存在反爬虫机制，如 TLS 指纹识别和针对非澳大利亚 IP 地址的地理限制
- 对于浏览结果，需要手动构建 URL 并在浏览器中打开
- 使用 DDG 网站搜索虽然能获取 URL，但无法获取完整的房源信息
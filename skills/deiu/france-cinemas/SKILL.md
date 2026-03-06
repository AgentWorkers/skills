---
name: france-cinemas
description: 使用 opendata.culture.gouv.fr API 搜索法国的电影院。可以按城市、地区、距离、放映厅数量、“Art et Essai”（艺术与实验）标签以及影院类型（如多厅影院）进行查询。无需 API 密钥。
---
# 法国电影院（无需API密钥）

您可以搜索和查询法国政府的官方电影院数据集。该数据集包含2,061家电影院的信息，包括银幕数量、座位容量、观影人数、电影类型（Art et Essai）、地理位置等详细信息。

数据来源：法国文化部，数据定期更新。许可证类型：开放许可（Open License）。

## 快速参考

| 操作 | 端点（Endpoint） |
|--------|----------|
| 按城市搜索 | `?where=search(commune,"Lyon")` |
| 按名称搜索 | `?where=search(nom,"Gaumont")` |
| 附近电影院 | `?where=within_distance(geolocalisation,geom'POINT(lon lat)',10km)` |
| 仅限Art et Essai类型的电影院 | `?where=ae="AE"` |
| 仅限多厅影院 | `?where=multiplexe="OUI"` |
| 按地区搜索 | `?where=region_administrative="ILE DE FRANCE"` |
| 按观影人数排序 | `?order_by=entrees_2022 desc&limit=10` |

所有查询的基URL：

```
https://data.culture.gouv.fr/api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records
```

## 字段（Fields）

| 字段名 | 数据类型 | 说明 |
|-------|------|-------------|
| `nom` | text | 电影院名称 |
| `commune` | text | 城市名称 |
| `dep` | text | 省份代码（例如：“75”） |
| `region_administrative` | text | 地区名称（例如：“ILE DE FRANCE”） |
| `adresse` | text | 街道地址 |
| `code_insee` | text | INSEE编码（法国市镇代码） |
| `population_commune` | int | 城市人口 |
| `ecrans` | int | 银幕数量 |
| `fauteuils` | int | 总座位数 |
| `entrees_2022` | int | 2022年的观影人数 |
| `ae` | text | 电影类型标签（“AE”或空字符串） |
| `genre` | text | 电影院类型（“Fixe”：固定场所；“Itinerant”：流动影院；“Saisonnier”：季节性影院） |
| `multiplexe` | text | 是否为多厅影院（“OUI”：是；“NON”：否） |
| `zone_de_la_commune` | text | 城市区域（“U”：城市区；“R”：农村区） |
| `geolocalisation` | geo_point | 经纬度坐标 |
| `nombre_de_films_programmes` | int | 上映的电影数量 |
| `nombre_de_films_inedits` | int | 首映电影的数量 |
| `nombre_de_films_en_semaine_1` | int | 上映第一周的电影数量 |
| `pdm_en_entrees` | float | 市场份额（按观影人数计算） |

## 按城市或名称搜索

使用`search()`函数对指定字段进行全文匹配。

```
GET /api/explore/v2.1/catalog/datasets/etablissements-cinematographiques/records?where=search(commune,"Marseille")&limit=20
```

## 结合其他筛选条件（使用AND）

```
?where=search(commune,"Paris") AND ecrans>=5
```

## 按地区或省份搜索

地区名称需使用大写字母。常见地区代码：ILE DE FRANCE（法兰西岛大区）、AUVERGNE-RHONE-ALPES（奥弗涅-罗讷-阿尔卑斯大区）、PROVENCE-ALPES-COTE D'AZUR（普罗旺斯-阿尔卑斯-蓝色海岸大区）、OCCITANIE（奥克西塔尼大区）、NOUVELLE-AQUITAINE（新阿基坦大区）、HAUTS-DE-FRANCE（上法兰西大区）、GRAND EST（大东部大区）、PAYS DE LA LOIRE（卢瓦尔河地区大区）、BRETAGNE（布列塔尼大区）、NORMANDIE（诺曼底大区）、BOURGOGNE-FRANCHE-COMTE（勃艮第-弗朗什-孔泰大区）、CENTRE-VAL DE LOIRE（卢瓦尔河中游大区）、CORSE（科西嘉大区）、OUTRE-MER（海外大区）。

```
?where=region_administrative="BRETAGNE"&limit=50
```

## 按省份代码搜索

```
?where=dep="75"
```

## 地理位置搜索

在指定坐标范围内查找电影院。坐标格式为：`POINT(longitude, latitude)`（先输入经度，再输入纬度）。

```
?where=within_distance(geolocalisation, geom'POINT(2.3522 48.8566)', 5km)
```

示例：查找巴黎市中心5公里范围内的电影院。支持的单位：`m`（米）、`km`（公里）、`mi`（英里）、`yd`（码）、`ft`（英尺）。

## 筛选条件示例

- 仅查找Art et Essai类型的电影院：`?where=ae="AE"`  
- 仅查找多厅影院：`?where=multiplexe="OUI"`  
- 仅查找固定场所的电影院（排除流动或季节性影院）：`?where=genre="Fixe"`  

## 排序和分页

- 可按任意数字字段进行排序（使用`desc`表示降序）。  
- 使用`offset`进行分页：`?offset=5`（每次获取5条记录）。  
- 每次请求的最大返回记录数为100条，使用`offset`遍历所有结果。  

## 选择字段

仅返回所需字段以减少响应数据量：`?limit=5&fields=nom,ecrans,fauteuils`  

## 数据聚合

- 对数据进行分组和统计：`?group_by=nom,region_administrative`  

## 组合筛选条件

使用`AND`或`OR`组合多个筛选条件：  
- 例如：`?where=nom="Gaumont"&&where=region_administrative="ILE DE FRANCE"`  

## 特定示例

- 查找法兰西最大的电影院：`?limit=1&order_by=entrees_2022 desc`  
- 查找巴黎所有Art et Essai类型的电影院：`?where=ae="AE"`  
- 查找用户所在位置附近的电影院：`?where=geolocalisation=POINT(48.8584, 2.3522)`  
- 查找农村地区观影人数较多的电影院：`?where=zone_de_la_commune="R"`  

## 常见查询示例

- 查找法国最大的电影院：`?limit=1&order_by=entrees_2022 desc`  
- 查找巴黎所有Art et Essai类型的电影院：`?where=ae="AE"`  
- 查找用户所在位置附近的电影院：`?where=geolocalisation=POINT(48.8584, 2.3522)`  

## 错误处理

- **无结果**：请确认输入的文本值均为大写字母（地区和城市名称需使用大写，例如：“LYON”而非“lyon”）。`search()`函数不区分大小写，但查询需完全匹配。  
- **无效的查询语法**：ODSQL在`where`子句中使用双引号表示字符串值；几何数据使用单引号（例如：`geom'POINT(48.8584, 2.3522)`）。  
- **分页限制**：API每次请求最多返回100条记录。若需获取所有结果，请使用`offset`循环查询，直到`results`为空。
---
name: swiss-geo
description: 瑞士地理数据、兴趣点（POIs）及旅游信息：可以搜索地点/地址、查询海拔高度、查找城市内的兴趣点（如餐厅、咖啡馆、景点，这些信息均来自OpenStreetMap），还能查看公共交通时刻表和地图链接。如有关于瑞士地点、景点、旅行路线或坐标的问题，请随时使用该工具。
---

# Swiss Geo Skill  
用于访问瑞士的Swisstopo地理数据。  

## 功能  

### 1. 地点/地址搜索  
```bash
curl -s "https://api3.geo.admin.ch/rest/services/api/SearchServer?searchText=SUCHTEXT&type=locations&sr=4326"
```  
- 返回经纬度（WGS84坐标）、地点名称及所属市镇。  
- `type=locations` 用于搜索地址/地点；`type=layers` 用于搜索地图图层。  

### 2. 海拔查询  
首先通过搜索获取坐标，然后将其转换为LV95坐标：  
```bash
# Umrechnung WGS84 → LV95 (grobe Näherung für Schweiz):
# easting = 2600000 + (lon - 7.4) * 73000
# northing = 1200000 + (lat - 46.95) * 111000

curl -s "https://api3.geo.admin.ch/rest/services/height?easting=EASTING&northing=NORTHING&sr=2056"
```  
返回海拔高度（单位：米）。  

### 3. 地理特征识别（市镇、州等）  
```bash
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=0&layers=all:LAYER_ID&sr=4326"
```  

**重要地图图层ID：**  
- `ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill` — 市镇边界  
- `ch.swisstopo.swissboundaries3d-kanton-flaeche.fill` — 州边界  
- `ch.bafu.bundesinventare-flachmoore` — 平原沼泽  
- `ch.bafu.schutzgebiete-paerke_nationaler_bedeutung` — 国家级保护区  

### 4. 生成地图链接  
```
https://map.geo.admin.ch/?lang=de&topic=ech&bgLayer=ch.swisstopo.pixelkarte-farbe&E=LON&N=LAT&zoom=ZOOM
```  
- `zoom`：0-13（13表示最高细节级别）  
- `E`/`N`：WGS84坐标  
- `layers`：用逗号分隔的图层ID（用于显示在地图上）  

## 示例工作流程：  
“马特洪峰在哪里？它的海拔有多高？”  

1. **搜索**：  
```bash
curl -s "https://api3.geo.admin.ch/rest/services/api/SearchServer?searchText=Matterhorn&type=locations&sr=4326"
```  
→ 经纬度：lat=45.9766, lon=7.6586  

2. **查询海拔（LV95）**：  
```bash
# easting ≈ 2600000 + (7.6586-7.4)*73000 = 2618878
# northing ≈ 1200000 + (45.9766-46.95)*111000 = 1091893
curl -s "https://api3.geo.admin.ch/rest/services/height?easting=2618878&northing=1091893&sr=2056"
```  
→ 海拔：4477.5米  

3. **生成地图链接**：  
```
https://map.geo.admin.ch/?lang=de&E=7.6586&N=45.9766&zoom=10
```  

### 5. 徒步路线查询  
```bash
# Wanderwege in einem Gebiet finden (bbox = west,south,east,north)
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/find?layer=ch.swisstopo.swisstlm3d-wanderwege&searchText=ORTSNAME&searchField=name"

# Wanderwege an einem Punkt identifizieren
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=50&layers=all:ch.swisstopo.swisstlm3d-wanderwege&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"
```  

**徒步路线类别：**  
- `wanderweg` — 黄色标记（T1级别）  
- `bergwanderweg` — 白红相间的标记（T2-T3级别）  
- `alpinwanderweg` — 白蓝相间的标记（T4-T6级别）  

**带有徒步路线的地图链接**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=10&layers=ch.swisstopo.swisstlm3d-wanderwege&bgLayer=ch.swisstopo.pixelkarte-farbe
```  

### 6. 山间小屋与住宿  
```bash
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=5000&layers=all:ch.swisstopo.unterkuenfte-winter&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"
```  

**带有山间小屋信息的地图链接**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=11&layers=ch.swisstopo.unterkuenfte-winter&bgLayer=ch.swisstopo.pixelkarte-farbe
```  

### 7. 滑雪场与缆车  
```bash
# Seilbahnen mit Bundeskonzession
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=2000&layers=all:ch.bav.seilbahnen-bundeskonzession&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"

# Alle Seilbahnen (swissTLM3D)
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=2000&layers=all:ch.swisstopo.swisstlm3d-uebrigerverkehr&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"
```  

**带有滑雪场信息的地图链接**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=11&layers=ch.bav.seilbahnen-bundeskonzession&bgLayer=ch.swisstopo.pixelkarte-farbe
```  

### 8. 自然灾害信息  
```bash
# Lawinengefahr
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=100&layers=all:ch.bafu.silvaprotect-lawinen&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"

# Sturzgefahr (Steinschlag, Felssturz)
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=100&layers=all:ch.bafu.silvaprotect-sturz&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"

# Hochwasser-Warnkarte (aktuell)
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=500&layers=all:ch.bafu.hydroweb-warnkarte_national&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"
```  

**自然灾害图层：**  
| 图层ID | 描述 |  
|---------|---------|  
| `ch.bafu.silvaprotect-lawinen` | 泥石流区域  
| `ch.bafu.silvaprotect-sturz` | 崩塌区域  
| `ch.bafu.hydroweb-warnkarte_national` | 当前洪水信息  
| `ch.bafu.gefahren-waldbrandWarnung` | 森林火灾风险  
| `ch.vbs.sperr-gefahrenzonenkarte` | 军事禁区  

**带有自然灾害信息的地图链接**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=12&layers=ch.bafu.silvaprotect-lawinen,ch.bafu.silvaprotect-sturz&bgLayer=ch.swisstopo.pixelkarte-farbe
```  

### 9. 瑞士天气  
**实时天气（来自wttr.in）**：  
```bash
curl -s "wttr.in/Zürich?format=%l:+%c+%t+%h+%w&lang=de"
# Zürich: ⛅️ +5°C 78% ↙12km/h
```  

**MeteoSwiss天气预警（地图）**：  
```
https://map.geo.admin.ch/?lang=de&layers=ch.meteoschweiz.gefahren-warnungen
```  

**SLF雪崩公告**：  
- 实时链接：https://www.slf.ch/de/lawinenbulletin-und-schneesituation.html  
- API（测试中）：https://www.slf.ch/avalanche/mobile/bulletin_de.json  

**BAFU洪水信息（实时水位）**：  
```
https://map.geo.admin.ch/?lang=de&layers=ch.bafu.hydroweb-messstationen_gefahren
```  

### 10. 公共交通时刻表（transport.opendata.ch）  
**查询交通路线**：  
```bash
curl -s "https://transport.opendata.ch/v1/connections?from=Zürich&to=Bern&limit=3"
```  
**查询车站信息**：  
```bash
curl -s "https://transport.opendata.ch/v1/stationboard?station=Zürich+HB&limit=5"
```  
**查询公交站点**：  
```bash
curl -s "https://transport.opendata.ch/v1/locations?query=Paradeplatz"
```  

**示例输出解析：**  
```bash
curl -s "https://transport.opendata.ch/v1/stationboard?station=Bern&limit=3" | python3 -c "
import sys,json
data = json.load(sys.stdin)
for s in data.get('stationboard', []):
    time = s.get('stop', {}).get('departure', '')[11:16]
    cat = s.get('category', '') + s.get('number', '')
    print(f\"{time} {cat} → {s.get('to', '')}\")"
```  

**参数说明：**  
| 参数 | 描述 |  
|---------|---------|  
| `from` / `to` | 起点/终点（名称或ID） |  
| `station` | 用于查询时刻表的站点名称 |  
| `limit` | 最多返回结果数量 |  
| `date` | 日期（格式：YYYY-MM-DD） |  
| `time` | 时间（格式：HH:MM） |  
| `isArrivalTime` | 1表示返回到达时间而非出发时间 |  

### 11. 其他实用数据  
**公共交通站点信息**：  
```bash
curl -s "https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryPoint&geometry=LON,LAT&tolerance=500&layers=all:ch.bav.haltestellen-oev&sr=4326&imageDisplay=500,500,96&mapExtent=5.9,45.8,10.5,47.8"
```  
**滑雪路线与雪地徒步路线**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=11&layers=ch.swisstopo-karto.skitouren,ch.swisstopo-karto.schneeschuhrouten&bgLayer=ch.swisstopo.pixelkarte-farbe
```  
**山坡坡度（适用于徒步规划）**：  
```
https://map.geo.admin.ch/?lang=de&E=LON&N=LAT&zoom=13&layers=ch.swisstopo-karto.hangneigung&bgLayer=ch.swisstopo.pixelkarte-farbe
```  

### 12. 通过OpenStreetMap获取城市兴趣点（Overpass API）  
**免费使用，无需API密钥**。适用于查询城市中的餐厅、咖啡馆、冰淇淋店、博物馆等地点。  

#### 基本查询（边界框）  
```bash
# POIs in einem Gebiet suchen (south,west,north,east)
# Beispiel: Eisdielen in Zürich-Zentrum
curl -s "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%5Btimeout%3A10%5D%3Bnode%5B%22amenity%22%3D%22ice_cream%22%5D%2847.36%2C8.52%2C47.39%2C8.56%29%3Bout%3B"
```  
#### 带有城市区域的查询（推荐）  
```bash
# Alle Eisdielen in der Stadt Zürich
curl -s "https://overpass-api.de/api/interpreter" --data-urlencode 'data=[out:json][timeout:15];
area["name"="Zürich"]["admin_level"="8"]->.city;
(
  node["amenity"="ice_cream"](area.city);
  node["shop"="ice_cream"](area.city);
);
out body;'
```  

#### 重要兴趣点标签  
| 类别 | OSM标签 | 例子 |  
|---------|---------|----------|  
| 🍦 冰淇淋店 | `amenity=ice_cream` |  
| 🍕 餐厅 | `amenity=restaurant` | + `cuisine=*` |  
| ☕ 咖啡馆 | `amenity=cafe` |  
| 🍺 酒吧/酒馆 | `amenity=bar` / `pub` |  
| 🏛️ 博物馆 | `amenity=tourism=museum` |  
| 🎭 剧院 | `amenity=theatre` |  
| ⛪ 教堂 | `amenity=place_of_worship` |  
| 🏰 名胜古迹 | `amenity=attraction` |  
| 👁️ 观景台 | `amenity=viewpoint` |  
| 🎡 游乐场 | `leisure=amusement_arcade` |  
| 🏊 游泳池 | `leisure=swimming_pool` | + `access=yes` |  
| 🎮 游乐场 | `leisure=playground` |  
| 🌳 公园 | `leisure=park` |  

#### 示例：苏黎世老城的博物馆与名胜古迹  
```bash
curl -s "https://overpass-api.de/api/interpreter" --data-urlencode 'data=[out:json][timeout:15];
(
  node["tourism"="museum"](47.366,8.538,47.378,8.548);
  node["tourism"="attraction"](47.366,8.538,47.378,8.548);
  node["historic"](47.366,8.538,47.378,8.548);
);
out body;'
```  
#### 适合家庭的活动场所（游乐场、公园）  
```bash
curl -s "https://overpass-api.de/api/interpreter" --data-urlencode 'data=[out:json][timeout:15];
area["name"="Zürich"]["admin_level"="8"]->.city;
(
  node["leisure"="playground"](area.city);
  way["leisure"="playground"](area.city);
);
out center body;'
```  

#### 响应数据解析（Python）  
```bash
curl -s "https://overpass-api.de/api/interpreter?data=..." | python3 -c "
import sys, json
data = json.load(sys.stdin)
for el in data.get('elements', []):
    tags = el.get('tags', {})
    name = tags.get('name', 'Unbenannt')
    lat, lon = el.get('lat', el.get('center', {}).get('lat', '')), el.get('lon', el.get('center', {}).get('lon', ''))
    addr = tags.get('addr:street', '')
    website = tags.get('website', '')
    opening = tags.get('opening_hours', '')
    print(f'{name}')
    if addr: print(f'  📍 {addr} {tags.get(\"addr:housenumber\", \"\")}')
    if opening: print(f'  🕐 {opening}')
    if website: print(f'  🔗 {website}')
    print()
"
```  

#### 瑞士城市的坐标（边界框）  
| 城市 | 南纬 | 西经 | 北纬 | 东经 |  
|-------|-------|------|-------|------|  
| 苏黎世市中心 | 47.36 | 8.52 | 47.39 | 8.56 |  
| 苏黎世老城 | 47.366 | 8.538 | 47.378 | 8.548 |  
| 伯尔尼市中心 | 46.94 | 7.43 | 46.96 | 7.46 |  
| 巴塞尔市中心 | 47.55 | 7.58 | 47.57 | 7.61 |  
| 卢塞恩市中心 | 47.04 | 8.29 | 47.06 | 8.32 |  
| 日内瓦市中心 | 46.19 | 6.13 | 46.21 | 6.16 |  

### 13. 瑞士旅游API（MySwitzerland）  
**⚠️ 需要API密钥**（请求头：`x-api-key`）  
**注意**：此API主要用于户外旅游（徒步、登山、地区信息）。对于城市内的兴趣点（餐厅、咖啡馆等），使用Overpass API（第12节）更为合适。  

**查询名胜古迹**：  
```bash
curl -s "https://opendata.myswitzerland.io/v1/attractions/?lang=de&limit=5" \
  -H "x-api-key: $MYSWITZERLAND_API_KEY"
```  
**查询徒步路线**：  
```bash
curl -s "https://opendata.myswitzerland.io/v1/tours/?lang=de&limit=5" \
  -H "x-api-key: $MYSWITZERLAND_API_KEY"
```  
**徒步路线的地理数据（GeoJSON格式）：**  
```bash
curl -s "https://opendata.myswitzerland.io/v1/tours/TOUR_ID/geodata" \
  -H "x-api-key: $MYSWITZERLAND_API_KEY"
```  
**目的地信息**：  
```bash
curl -s "https://opendata.myswitzerland.io/v1/destinations/?lang=de" \
  -H "x-api-key: $MYSWITZERLAND_API_KEY"
```  
**响应字段：**  
- `name`：景点/徒步路线的名称  
- `abstract`：简要描述  
- `geo.latitude`, `geo.longitude`：坐标  
- `classification`：分类（季节、类型等）  

## 示例工作流程：  
- “在苏黎世哪里可以带孩子吃冰淇淋？附近有什么？”  
  1. 通过Overpass API查询冰淇淋店（第12节）  
  2. 查找附近的名胜古迹或游乐场  
  3. 查询前往这些地点的公共交通路线（第10节）  
  4. 生成地图链接（第4节）  

- “想在恩加丁地区乘坐缆车并入住山间小屋？”  
  1. 查询滑雪场（第7节）  
  2. 查找徒步路线（第5节）  
  3. 识别可入住的山间小屋（第6节）  
  4. 通过MySwitzerland查询相关徒步路线（第13节）  

## 提示：  
- **城市兴趣点**：使用Overpass API（免费且信息详细）  
- **户外旅游**：使用MySwitzerland API（需密钥）  
- **地图与地理数据**：使用Swisstopo（免费）  
- **公共交通时刻表**：使用transport.opendata.ch（免费）  
- 搜索结果包含`origin`（地址、sn25、gg25等字段，便于分类）  
- 如需精确的LV95坐标，请参考[references/api.md](references/api.md)  
- 使用逗号组合Swisstopo图层：`layers=layer1,layer2,layer3`
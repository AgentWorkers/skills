# 乌梅å市开放数据

您可以查询乌梅å市关于地点、设施、人口统计、环境等方面的开放数据。

## API基础URL
`https://opendata.umea.se/api/v2/`

## 可用数据类别

### 🏞️ 娱乐与设施

#### **游乐场（Playgrounds）**
- 数据集ID：`gop_lekparker`
- 包含由Gator和Parker管理的游乐场信息
- 字段：名称、占地面积、坐标（geo_point_2d）、联系方式
- 例句：“Mariehem附近最近的游乐场在哪里？”

#### **游泳池（Swimming Spots）**
- 数据集ID：`badplatser`
- 乌梅å市的公共游泳池信息
- 字段：名称、占地面积、类型、坐标、无障碍设施（handik_anp）
- 例句：“乌梅å有哪些游泳池？”

#### **徒步路线（Hiking Trails）**
- 数据集ID：`vandringsleder`
- 包含徒步路线和距离信息
- 字段：名称、分段路线（delstracka）、所属市镇、难度等级、长度（以米计）、路线几何形状（geo_shape）
- 例句：“乌梅å有哪些适合徒步的路线？”

#### **休息区（Rest Areas）**
- 数据集ID：`rastplatser`
- 休息区和野餐区信息
- 字段：名称、位置坐标
- 例句：“哪里有休息区？”

#### **树木（Trees）**
- 数据集ID：`trad-som-forvaltas-av-gator-och-parker`
- 由Gator和Parker管理的树木信息
- 字段：树木类型、位置、管理信息
- 例句：“这个区域有哪些树木？”

### ⚡ 基础设施

#### **电动汽车充电站（EV Charging Stations）**
- 数据集ID：`laddplatser`
- 电动汽车充电站信息
- 字段：名称、街道地址、门牌号、邮政编码、所在城市、所有者、充电点数量、可用充电点数量、位置（经纬度）
- 例句：“市中心附近有充电站吗？”

#### **WiFi热点（WiFi Hotspots）**
- 数据集ID：`wifi-hotspots`
- 公共WiFi接入点信息
- 字段：常用名称（popularnamn）、坐标
- 例句：“乌梅å有哪些免费的WiFi热点？”

### 🏗️ 建筑与规划

#### **建筑许可（Building Permits）**
- 数据集ID：`bygglov-beslut`
- 已批准的建筑许可信息
- 字段：许可描述、许可类型、批准日期、注册日期、许可类型
- 例句：“最近批准了哪些建筑许可？”

#### **建筑许可申请（Building Permit Applications）**
- 数据集ID：`bygglov-inkomna-arenden`
- 正在处理的建筑许可申请信息
- 字段：申请详情、提交日期、状态
- 例句：“收到了多少建筑许可申请？”

### 📊 人口统计与数据

#### **人口变化（Population Changes）**
- 数据集ID：`befolkningsfoeraendringar-helar`
- 人口变化统计数据
- 字段：年份、出生人数、死亡人数、迁移人数、总变化量
- 例句：“乌梅å的人口发生了哪些变化？”

#### **住房状况（Housing Stock）**
- 数据集ID：`bostadsbestand-hustyp`
- 按类型划分的住房信息
- 字段：房屋类型、数量、面积
- 例句：乌梅å的住房状况如何？”

### 🌍 环境

#### **温室气体排放（Greenhouse Gas Emissions）**
- 数据集ID：`vaxthusgasutslapp_umea`
- 乌梅å市的温室气体排放数据
- 字段：年份、排放部门、排放量（二氧化碳当量）
- 例句：乌梅å的温室气体排放情况如何？

#### **犯罪统计（Crime Statistics）**
- 数据集ID：`exempel-brottsstatistik-anmaelda-brott-fran-bra-s-oeppna-data`
- 来自BRÅ开放数据的犯罪统计信息
- 字段：犯罪类型、数量、年份
- 例句：乌梅å的犯罪统计情况如何？

## 使用方法

### 查询数据集
```bash
./scripts/query.sh <dataset_id> [limit]
```

示例：
```bash
./scripts/query.sh badplatser 10
./scripts/query.sh laddplatser 20
```

### 查找最近的位置
```bash
./scripts/nearby.sh <dataset_id> <lat> <lon> [limit]
```

示例：
```bash
# Find nearest playground to Mariehem (approx coordinates)
./scripts/nearby.sh gop_lekparker 63.8200 20.3000 5

# Find nearest EV charging station to city center
./scripts/nearby.sh laddplatser 63.8258 20.2630 5
```

## API端点

### 列出所有数据集
```bash
curl "https://opendata.umea.se/api/v2/catalog/datasets"
```

### 从数据集中获取记录
```bash
curl "https://opendata.umea.se/api/v2/catalog/datasets/{dataset_id}/records?limit=20"
```

### 搜索数据集
```bash
curl "https://opendata.umea.se/api/v2/catalog/datasets?where=search(default,\"query\")"
```

## 数据格式

所有记录遵循以下结构：
```json
{
  "total_count": 123,
  "records": [
    {
      "record": {
        "id": "unique-id",
        "timestamp": "2024-01-01T12:00:00Z",
        "fields": {
          "namn": "Location Name",
          "geo_point_2d": {
            "lat": 63.825,
            "lon": 20.263
          },
          ...
        }
      }
    }
  ]
}
```

## 自然语言查询示例

AI可以回答以下问题：

**娱乐与设施：**
- “Mariehem附近最近的游乐场在哪里？”
- “乌梅å有哪些游泳池？”
- “乌梅å有哪些适合徒步的路线？”
- “E4高速公路附近有休息区吗？”

**基础设施：**
- “市中心附近有充电站吗？”
- “乌梅å有哪些免费的WiFi热点？”
- “乌梅å总共有多少个充电站？”

**建筑与规划：**
- “最近批准了哪些建筑许可？”
- “乌梅å目前正在建设什么项目？”

**人口统计与环境：**
- “乌梅å的人口发生了哪些变化？”
- “乌梅å的温室气体排放情况如何？”
- “乌梅å有多少套住房？”
- “乌梅å的犯罪统计情况如何？”

## 注意事项

- 不需要API密钥
- 所有数据均为公开信息
- 坐标使用WGS84坐标系（经纬度）
- 部分数据集包含路线/路线的地理形状信息
- 数据由乌梅å市定期更新
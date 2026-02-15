---
name: norway-roads
description: 查询挪威的实时路况、道路封闭情况以及交通问题。当用户询问挪威的道路状况、封闭的道路、交通情况、道路天气，或规划路线时，可以使用该功能。它可以处理诸如“奥斯陆和卑尔根之间有道路封闭吗？”、“E6公路的路况如何？”、“今天开车去特隆赫姆有什么问题吗？”之类的查询，以及针对挪威道路的一般路况查询。
---

# 挪威道路信息

通过Statens Vegvesen NVDB API查询实时的道路封闭情况和路况。

## 快速入门

- 查看所有当前的道路封闭信息：  
  ```bash
./scripts/query_roads.py
```

- 查询两个城市之间的路线情况：  
  ```bash
./scripts/query_roads.py --from Oslo --to Bergen
```

- 查看特定道路或地点的信息：  
  ```bash
./scripts/query_roads.py --road "Strynefjell"
```

- 获取JSON格式的输出结果：  
  ```bash
./scripts/query_roads.py --json
```

## 使用示例

### 查询路线状况

在规划挪威两个城市之间的行程时：  
  ```bash
./scripts/query_roads.py --from Oslo --to Bergen
./scripts/query_roads.py --from Oslo --to Trondheim
./scripts/query_roads.py --from Bergen --to Stavanger
```

支持的城市：奥斯陆（Oslo）、卑尔根（Bergen）、斯塔万格（Stavanger）、特隆赫姆（Trondheim）、特罗姆瑟（Tromsø）、克里斯蒂安桑（Kristiansand）、奥勒松（Ålesund）、博德（Bodø）

### 按地点名称筛选

```bash
./scripts/query_roads.py --road "Strynefjell"
./scripts/query_roads.py --road "E6"
```

## 返回的数据类型

该接口会返回NVDB中的两种类型的道路限制信息：

1. **Vegstengning**（道路封闭）：  
   - 计划中的或永久性的道路封闭  
     - 季节性封闭（如冬季山区道路封闭）  
     - 山体滑坡/雪崩导致的封闭  
     - 维护原因导致的封闭  
     - 封闭原因：雪（Snø）、冰（Is）、岩石（Stein）

2. **Vegsperring**（道路障碍）：  
   - 实际阻碍道路通行的障碍物（如大门、混凝土障碍物等）  
     - 持续性的通行限制

## API响应格式

每个道路封闭信息包括：  
- **location**：街道/道路名称  
- **county**：挪威的郡（fylke）  
- **municipality**：所属的市镇（kommune）  
- **from_date/to_date**：封闭开始/结束日期  
- **cause**：封闭原因（Snø=雪；Is=冰；Stein=岩石）  
- **type**：封闭类型（Vegstengning或Vegsperring）

## 数据来源

- **API**：NVDB v3（Nasjonal VegDataBank）  
- **URL**：https://nvdbapiles-v3.atlas.vegvesen.no  
- **对象类型**：485（Vegstengning）、607（Vegsperring）  
- **更新频率**：实时更新（来自官方数据库）  
- **无需API密钥**：公开数据

## 常用挪威术语  

| 挪威语 | 中文 |
|-----------|---------|
| Vegstengning | 道路封闭 |
| Vegsperring | 道路障碍物 |
| Snø | 雪 |
| Is | 冰 |
| Stein | 岩石 |
| Fylke | 郡（行政区划） |
| Stengt | 封闭中 |

## 主要路线与郡  

**郡（Fylker）**：  
- 维肯（Viken）：奥斯陆地区  
- 韦斯特兰（Vestland）：卑尔根地区  
- 罗加兰（Rogaland）：斯塔万格地区  
- 特伦德尔格（Trøndelag）：特隆赫姆地区  
- 特罗姆瑟与芬马克（Troms og Finnmark）：北部地区  
- 阿格德（Agder）：南部地区  
- 默勒与罗姆斯达尔（Møre og Romsdal）：奥勒松地区  
- 诺德兰（Nordland）：博德地区  

**主要道路**：  
- E6：南北向主干道（Kirkenes-Halden）  
- E16：经莱尔达尔隧道（Lærdal tunnel）连接卑尔根与奥斯陆的路线  
- E39：西海岸路线  

## 限制事项  

- 仅显示NVDB中记录的道路封闭信息，不包含实时交通状况  
- 如需实时交通信息，请使用Vegvesen移动应用程序或拨打175  
- 冬季道路封闭通常是季节性的且会反复出现  
- 部分近期发生的事件可能尚未被记录在数据库中  

## 参考资料

有关API详情和城市对应关系，请参阅[references/api-docs.md]。
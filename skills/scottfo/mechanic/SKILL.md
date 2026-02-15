---
name: mechanic
description: "**车辆维护追踪器与机械师顾问**  
该工具可追踪车辆的行驶里程、保养间隔、燃油经济性、维修费用、保修信息以及召回通知。它能查询制造商的保养计划、估算维修成本、安排保养日期、记录维修服务提供商，并主动提醒用户即将进行的或逾期的保养服务。  

主要功能包括：  
- **车辆信息管理**：支持VIN码解析，自动填充车辆详细规格；  
- **安全监控**：实时监控NHTSA（美国国家公路交通安全管理局）发布的召回通知；  
- **燃油经济性分析**：跟踪燃油消耗情况并检测异常；  
- **保修提醒**：在保修期到期前发出警报；  
- **保养计划**：提供出行前或季节性检查清单；  
- **历史记录**：记录车辆的维修历史和服务提供商信息；  
- **税务优惠**：集成税务抵扣相关功能；  
- **紧急信息**：提供车辆紧急情况的相关信息；  
- **成本分析**：计算每公里的维修成本。  

适用于讨论车辆保养、更换机油、保养间隔、燃油经济性、保修问题、房车维护、车顶密封处理、发电机维修、冬季车辆保养等与机械相关的所有场景。  
支持多种车辆类型，包括卡车、汽车、摩托车、全地形车（ATV）、房车（RV）和船只。"
homepage: https://github.com/ScotTFO/mechanic-skill
metadata: {"clawdbot":{"emoji":"🔧"}}
---

# 机械师——车辆维护追踪器

该工具可追踪各类车辆的行驶里程和服务间隔，包括卡车、汽车、摩托车、房车、越野摩托车、全地形车（ATV）、船只等。它能够解码车辆识别码（VIN），自动填充车辆规格信息，查询制造商推荐的维护计划，记录服务历史，估算费用，监控召回信息，监测燃油经济性，管理保修信息，并及时提醒用户即将进行的或逾期的服务。

## 数据存储

所有用户数据存储在 `<workspace>/data/mechanic/` 目录下：

| 文件 | 用途 |
|------|---------|
| `state.json` | 所有车辆的信息：当前里程/行驶时间、服务记录、燃油记录、保修信息、服务提供商、紧急联系方式 |
| `<key>-schedule.json` | 每辆车的服务计划，包括服务间隔和费用估算 |

**规则说明：** 技能逻辑存储在 `<skill>/` 目录下，用户数据存储在 `<workspace>/data/mechanic/` 目录中。这样在更新或重新安装技能时，数据能够得到保护。

## 首次设置

如果 `<workspace>/data/mechanic/state.json` 不存在：
1. 创建 `<workspace>/data/mechanic/` 目录。
2. 询问用户需要追踪哪些车辆。
3. 对于每辆车，执行 **添加新车辆** 的流程（包括选择每辆车的检查频率）。
4. 创建包含车辆信息的 `state.json` 文件。
5. 设置定时任务（详见 **里程检查设置** 部分）。

### State 文件结构
```json
{
  "settings": {
    "check_in_tz": "America/Phoenix"
  },
  "providers": [
    {
      "id": "jims_diesel",
      "name": "Jim's Diesel Repair",
      "location": "123 Main St, Mesa, AZ",
      "phone": "480-555-1234",
      "specialties": ["diesel", "trucks"],
      "rating": 5,
      "notes": "Great with Power Stroke engines"
    }
  ],
  "vehicles": {
    "f350": {
      "label": "2021 Ford F-350 6.7L Power Stroke",
      "schedule_file": "f350-schedule.json",
      "check_in_frequency": "monthly",
      "current_miles": 61450,
      "last_updated": "2026-01-26",
      "last_check_in": "2026-01-26",
      "vin": "1FT8W3BT0MED12345",
      "vin_data": {
        "decoded": true,
        "decoded_date": "2026-01-26",
        "year": 2021,
        "make": "Ford",
        "model": "F-350",
        "trim": "Lariat",
        "body_class": "Pickup",
        "drive_type": "4WD",
        "engine": "6.7L Power Stroke V8 Turbo Diesel",
        "displacement_l": 6.7,
        "cylinders": 8,
        "fuel_type": "Diesel",
        "transmission": "10-Speed Automatic",
        "doors": 4,
        "gvwr_class": "Class 3",
        "bed_length": "8 ft",
        "wheel_base": "176 in",
        "plant_country": "United States",
        "plant_city": "Louisville",
        "raw_response": {}
      },
      "business_use": false,
      "business_use_percent": 0,
      "mileage_history": [
        {"date": "2026-01-26", "miles": 61450, "source": "user_reported"}
      ],
      "service_history": [
        {
          "service_id": "oil_filter",
          "date": "2025-11-15",
          "miles": 58000,
          "hours": null,
          "notes": "Full synthetic Motorcraft FL-2051S",
          "actual_cost": 125.00,
          "provider": {
            "id": "jims_diesel",
            "name": "Jim's Diesel Repair",
            "parts_warranty_months": 12,
            "labor_warranty_months": 6
          }
        }
      ],
      "fuel_history": [
        {
          "date": "2026-01-20",
          "gallons": 32.5,
          "cost": 108.55,
          "odometer": 61300,
          "mpg": 14.2,
          "notes": "Regular fill-up"
        }
      ],
      "warranties": [
        {
          "type": "factory_powertrain",
          "provider": "Ford",
          "start_date": "2021-03-15",
          "end_date": "2026-03-15",
          "start_miles": 0,
          "end_miles": 60000,
          "coverage_details": "Engine, transmission, drivetrain components",
          "status": "active"
        }
      ],
      "recalls": {
        "last_checked": "2026-01-26",
        "open_recalls": [],
        "completed_recalls": []
      },
      "emergency_info": {
        "vin": "1FT8W3BT0MED12345",
        "insurance_provider": "State Farm",
        "policy_number": "SF-123456789",
        "roadside_assistance_phone": "1-800-555-1234",
        "tire_size_front": "275/70R18",
        "tire_size_rear": "275/70R18",
        "tire_pressure_front_psi": 65,
        "tire_pressure_rear_psi": 80,
        "oil_type": "15W-40 CK-4 Full Synthetic",
        "oil_capacity": "15 quarts",
        "coolant_type": "Motorcraft Orange VC-3DIL-B",
        "def_type": "API certified DEF",
        "tow_rating_lbs": 20000,
        "gvwr_lbs": 14000,
        "gcwr_lbs": 37000,
        "key_fob_battery": "CR2450",
        "fuel_type": "Diesel (Ultra Low Sulfur)",
        "fuel_tank_gallons": 48,
        "notes": ""
      }
    }
  },
  "last_service_review": "2026-01-26"
}
```

**顶级字段：**
- `settings` — 全局设置（时区等）
- `providers` — 可重用的服务提供商列表
- `vehicles` — 按简短标识符（如 `f350`、`rv`、`crf450`）进行分类
- `last_service_review` — 上次全面检查的日期

**每辆车字段：**
- `label` — 便于阅读的车辆名称
- `schedule_file` — 服务计划的 JSON 文件路径
- `check_in_frequency` — 检查里程的频率（每周/每两周/每月/每季度）
- `current_miles` / `current_hours` — 最新的里程/行驶时间记录
- `last_updated` / `last_check_in` — 最后一次检查的日期
- `vin` — 车辆识别码（用于召回信息、VIN 解码和紧急联系方式）
- `vin_data` — 从 NHTSA VPIC API 解码得到的 VIN 数据（包括规格、发动机、变速箱等信息）
- `business_use` — 车辆是否用于商业用途（布尔值）
- `business_use_percent` — 商业用途的百分比（0-100）
- `mileage_history` — 里程/行驶时间的 chronological 数组
- `service_history` — 完成服务的 chronological 数组（包含可选的 `actual_cost` 和 `provider`）
- `fuel_history` — 加油记录的 chronological 数组
- `warranties` — 保修记录数组
- `recalls` — 召回监控状态（上次检查时间、是否开启/已完成）
- `emergency_info` — 车辆规格和紧急联系方式的快速参考

## 读取状态

在加载技能时，读取以下文件：
1. `<workspace>/data/mechanic/state.json` — 所有车辆的当前状态
2. 根据需要读取相关的 `<key>-schedule.json` 文件

## 添加新车辆

当用户想要追踪新车辆时：

### 1. 收集车辆信息
**首先请求 VIN。** 如果用户提供了 VIN，执行 **VIN 解码**（详见下文），以自动填充车辆年份、品牌、型号、发动机、变速箱等规格信息。这可以避免用户重复回答可自动查询的问题。

询问以下信息：
- **VIN**（强烈建议提供——自动填充规格信息，启用召回监控）
- **年份、品牌、型号**（仅在未提供 VIN 或 VIN 解码不完整时询问）
- **使用类型**（日常驾驶、拖车、越野、周末娱乐等）
- **当前里程/行驶时间**
- **是否用于商业用途？**（如果是，占比是多少？**（用于税务抵扣记录）
- **保修信息**——是否有任何有效的原厂或延长保修？有效期/里程限制？
- **紧急联系方式**——保险公司、路边援助电话、轮胎尺寸（可以稍后填写）

如果用户没有 VIN，可以手动输入信息，并注意后续可以添加 VIN 以启用自动填充和召回监控。

### 2. 确定维护计划
根据使用类型确定维护计划：

| 使用类型 | 维护计划级别 | 影响 |
|-------|-----------|--------|
| 日常通勤 | 标准计划 |
| 拖车、货运 | 加强计划 | 服务间隔缩短（通常为标准计划的 50-75%） |
| 越野、多尘环境 | 加强计划 | 服务间隔缩短，滤清器更换更频繁 |
| 极端温度（炎热沙漠、寒冷地区） | 加强计划 | 服务间隔缩短，液体/电池需特别注意 |
| 赛车 | 特殊计划 | 更频繁的服务和专用液体 |

大多数制造商都会提供“标准”和“加强/特殊条件”两种维护计划。选择适合的方案。

### 3. 选择检查频率
询问用户希望多久检查一次车辆的里程/行驶时间：

| 频率 | 适用车辆类型 |
|-----------|----------|
| **每周** | 越野摩托车、赛车车辆、商用/车队车辆、高里程日常驾驶者 |
| **每两周** | 活跃骑手/驾驶员、服务间隔较短的车辆 |
| **每月** | 大多数汽车和卡车（推荐默认设置） |
| **每季度** | 季节性车辆、低里程车辆、长期存放的车辆 |

根据车辆类型和使用情况建议频率，但允许用户自行调整。

### 4. 查询服务计划
**查找该特定年份/品牌/型号/发动机的制造商推荐维护间隔**：
- 通过网络搜索官方维护计划
- 查阅用户手册中的间隔信息
- 参考爱好者论坛的实际建议
- 考虑步骤 2 中确定的维护计划级别

### 5. 创建服务计划文件
在 `<workspace>/data/mechanic/<key>-schedule.json` 中创建文件：

```json
{
  "vehicle": {
    "year": 2021,
    "make": "Ford",
    "model": "F-350",
    "type": "truck",
    "engine": "6.7L Power Stroke V8 Turbo Diesel",
    "transmission": "10R140 10-Speed Automatic",
    "duty": "severe",
    "notes": "Tows fifth wheel RV"
  },
  "services": [
    {
      "id": "oil_filter",
      "name": "Engine Oil & Filter Change",
      "interval_miles": 7500,
      "interval_months": 6,
      "details": "Specific oil type, filter part number, capacity, and any special instructions.",
      "priority": "critical",
      "cost_diy": "$XX-XX",
      "cost_shop": "$XX-XX",
      "cost_dealer": "$XX-XX",
      "cost_note": "Optional note about related expensive repairs"
    }
  ]
}
```

**每个服务项目必须包含的字段：**
- `id` — 唯一的蛇形命名标识符
- `name` — 便于阅读的名称
- 至少一个间隔时间：`interval_miles`、`interval_months`、`interval_hours` 或 `interval_rides`
- `details` — 具体部件、所需液体、容量及任何注意事项
- `priority` — `critical`（紧急）、`high`（较高）、`medium`（中等）或 `low`（较低）
- `cost_diy`、`cost_shop`、`cost_dealer` — 预估费用范围

**费用查询：**
- 查找该车辆各项服务的典型费用
- **DIY** = 仅包含零件费用
- **Shop** = 独立机械师
- **Dealer** = 制造商经销商
- 对于故障/维修费用明显较高的项目，添加 `cost_note`

### 6. 添加到状态文件
将车辆信息添加到 `state.json` 的 `vehicles` 对象中：

```json
{
  "<key>": {
    "label": "2021 Ford F-350 6.7L Power Stroke",
    "schedule_file": "<key>-schedule.json",
    "check_in_frequency": "monthly",
    "current_miles": 61450,
    "current_hours": null,
    "last_updated": "2026-01-26",
    "last_check_in": "2026-01-26",
    "vin": null,
    "vin_data": {
      "decoded": false
    },
    "business_use": false,
    "business_use_percent": 0,
    "mileage_history": [
      {"date": "2026-01-26", "miles": 61450, "source": "user_reported"}
    ],
    "service_history": [],
    "fuel_history": [],
    "warranties": [],
    "recalls": {
      "last_checked": null,
      "open_recalls": [],
      "completed_recalls": []
    },
    "emergency_info": {
      "vin": null,
      "insurance_provider": null,
      "policy_number": null,
      "roadside_assistance_phone": null,
      "tire_size_front": null,
      "tire_size_rear": null,
      "tire_pressure_front_psi": null,
      "tire_pressure_rear_psi": null,
      "oil_type": null,
      "oil_capacity": null,
      "coolant_type": null,
      "tow_rating_lbs": null,
      "gvwr_lbs": null,
      "key_fob_battery": null,
      "fuel_type": null,
      "fuel_tank_gallons": null,
      "notes": ""
    }
  }
}
```

**命名规则：** 使用简短易记的标识符，例如 `f350`、`civic`、`r1`、`rv`、`crf450`、`harley`、`bass_boat` 等。

### 7. 更新定时任务
更新定时任务，以便包含新车辆。如果该车辆的检查频率高于当前设置，调整定时任务的执行频率。

### 8. VIN 解码与自动填充
如果提供了 VIN，执行 **VIN 解码**，以自动填充车辆规格信息、紧急联系方式字段和服务计划的车辆相关部分。将解码后的信息展示给用户确认。

### 9. 立即检查召回信息
如果提供了 VIN，立即检查是否有未处理的召回（详见 **NHTSA 召回监控**）。如果没有 VIN，则根据品牌/型号/年份进行检查。

## 车辆类型及特殊注意事项

| 车辆类型 | 需要追踪的项目 |
|------|-------|----------------------|
| **汽车** | 里程、机油、滤清器、刹车、轮胎、变速箱、冷却液 |
| **卡车** | 与汽车相同的项目，外加不同的液体、分动箱（四驱车辆），拖车时刹车磨损更严重 |
| **摩托车** | 里程、机油、链条/链轮、气门间隙、刹车液（液冷系统）、轮胎（磨损更快） |
| **越野摩托车** | 行驶时间 + 行驶次数、空气滤清器（每次行驶都要更换！）、机油（非常频繁）、气门间隙、悬挂系统维护、冷却液 |
| **全地形车/UTV** | 行驶时间 + 行驶次数、类似越野摩托车的项目，外加CV靴、皮带（CVT系统） |
| **房车/拖车** | 里程 + 月份、车顶/密封件检查、轮毂轴承、电动刹车、轮胎（根据使用时间更换） |
| **船只** | 行驶时间 | 机油、叶轮、下部单元液体、锌块/阳极、冬季保养 |
| **第五轮/拖车** | 里程 + 月份、无发动机相关项目，但需要检查轴承、刹车、轮胎、车顶、密封件、管道系统、液化石油气（LP gas） |

### 间隔类型
服务间隔可以结合以下方式确定：
- `interval_miles` — 基于里程
- `interval_hours` — 基于发动机/行驶时间（发电机、越野摩托车、船只）
- `interval_months` — 基于时间（所有部件都会随时间老化）
- `interval_rides` — 每次使用后（例如，越野摩托车的空气滤清器）

**无论哪种间隔先达到，都会触发服务提醒。**

---

## VIN 解码与自动填充

当用户提供 VIN（在车辆设置过程中或之后），使用免费的 NHTSA VPIC API 进行解码，以自动查找并存储车辆规格信息。

### NHTSA VPIC API （VIN 解码器）

**端点：** `https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json`

无需 API 密钥，免费且无使用限制。

**示例：**
```
GET https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/1FT8W3BT0MED12345?format=json
```

### 需要提取的关键字段**

API 返回一个包含约 140 多个字段的 `Results` 数组。提取并映射这些字段：

| VPIC 字段 | 对应的字段 | 备注 |
|------------|---------|-------|
| `ModelYear` | `vin_data.year` | 车辆年份 |
| `Make` | `vin_data.make` | 制造商 |
| `Model` | `vin_data.model` | 车型名称 |
| `Trim` | `vin_data.trim` | 车型配置（如 Lariat、XLT 等） |
| `BodyClass` | `vin_data.body_class` | 车身类型（皮卡、SUV、摩托车等） |
| `DriveType` | `vin_data.drive_type` | 驱动方式（四驱、全轮驱动、后轮驱动等） |
| `DisplacementL` | `vin_data.displacement_l` | 发动机排量（升） |
| `EngineCylinders` | `vin_data.cylinders` | 发动机气缸数 |
| `FuelTypePrimary` | `vin_data.fuel_type` | 燃料类型（汽油、柴油、电动等） |
| `EngineModel` | `vin_data.engine` | 发动机型号 |
| `TransmissionStyle` | `vin_data.transmission` | 变速箱类型（自动、手动、CVT） |
| `TransmissionSpeeds` | （附加到 transmission 字段） | 变速箱类型（例如“10-Speed Automatic”） |
| `Doors` | `vin_data.doors` | 车门数量 |
| `GVWR` | `vin_data.gvwr_class` | 车辆总重量等级 |
| `WheelBaseShort` | `vin_data.wheel_base` | 车轮轴距（英寸） |
| `BedLengthIN` | `vin_data.bed_length` | 卡车货厢长度（如适用） |
| `PlantCountry` | `vin_data.plant_country` | 组装国家 |
| `PlantCity` | `vin_data.plant_city` | 组装城市 |

**注意：** 如果某些字段不适用，返回空字符串 `""`。仅存储非空值。**

### VIN 数据存储

将解码后的数据存储在 `state.json` 中的 `vin_data` 对象中：

```json
{
  "vin_data": {
    "decoded": true,
    "decoded_date": "2026-01-27",
    "year": 2021,
    "make": "Ford",
    "model": "F-350",
    "trim": "Lariat",
    "body_class": "Pickup",
    "drive_type": "4WD",
    "engine": "6.7L Power Stroke V8 Turbo Diesel",
    "displacement_l": 6.7,
    "cylinders": 8,
    "fuel_type": "Diesel",
    "transmission": "10-Speed Automatic",
    "doors": 4,
    "gvwr_class": "Class 3",
    "bed_length": "8 ft",
    "wheel_base": "176 in",
    "plant_country": "United States",
    "plant_city": "Louisville",
    "raw_response": {}
  }
}
```

将完整的 VPIC 结果对象 `raw_response` 也存储起来，以供后续参考——其中可能包含其他有用的字段（如 `AirBagLocFront`、`SeatBeltsAll`、`TPMS`、`ActiveSafetySysNote` 等）。

如果 `vin_data.decoded` 为 `false` 或缺失，说明 VIN 尚未解码。

### 自动填充流程

解码 VIN 后：
1. **更新 `vin_data` — 存储所有解码后的字段 |
2. **更新 `label` — 根据解码的年份/品牌/型号/发动机生成车辆名称（例如：“2021 Ford F-350 6.7L Power Stroke”） |
3. **更新 `emergency_info` — 自动填充可推导出的字段：
   - `fuel_type` 从 `FuelTypePrimary` 获取 |
   - `gvwr_lbs` 从 `GVWR` 获取（解析重量等级） |
4. **更新服务计划文件** — 用解码后的规格信息填充 `vehicle` 部分 |
5. **展示给用户** — 显示解码结果，确认准确性，并询问 VIN 未提供的信息（如使用类型、维护计划级别、保险信息等）。

### 何时解码

| 触发条件 | 执行操作 |
|---------|--------|
| 添加新车辆且提供了 VIN | 立即解码并自动填充信息 |
| 用户为现有车辆提供了 VIN | 解码并补充 `vin_data` 及任何缺失的字段 |
| 用户请求“查询我的 VIN” | 解码并显示规格信息 |
| 用户更改/修正 VIN | 重新解码并更新信息 |

### 后续添加 VIN

如果车辆在添加时未提供 VIN，而用户后来提供了 VIN：
1. 解码 VIN |
2. 存储在 `vin_data` 中 |
3. 更新 `vin` 字段 |
4. 补充任何缺失的 `emergency_info` 字段 |
5. 如果解码后的信息更详细，更新 `label` |
6. 使用新的 VIN 立即检查召回信息 |
7. 确认更新的内容

### VIN 解码后的展示格式

向用户展示解码后的 VIN 数据时：
```
🔍 VIN Decoded — [VIN]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Vehicle
Year: [year] | Make: [make] | Model: [model]
Trim: [trim] | Body: [body_class]
Drive: [drive_type] | Doors: [doors]

🔧 Powertrain
Engine: [engine] ([displacement]L, [cylinders] cyl)
Fuel: [fuel_type]
Transmission: [transmission]

📏 Specs
GVWR: [gvwr_class]
Wheel Base: [wheel_base]
Bed Length: [bed_length] (if truck)

🏭 Built in [plant_city], [plant_country]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 限制事项
- **VPIC 提供的数据仅适用于美国市场的车辆**。进口/国外市场的 VIN 可能数据不完整。
- **拖车和房车**：由于制造商不同，VIN 解码后的数据可能有限。
- **摩托车和高性能车辆**：部分品牌的解码效果可能不佳（如本田、雅马哈、川崎、铃木）。
- **1981 年之前的车辆**：VIN 标准化之前生产的车辆无法解码。
- 如果解码结果不完整，需手动输入或通过网络查询规格信息。

---

## NHTSA 召回监控

使用免费的 NHTSA API 监控所有追踪车辆的召回信息（无需 API 密钥）。

### API 端点
- **按品牌/型号/年份查询：** `https://api.nhtsa.dot.gov/recalls/recallsByVehicle?make=Ford&model=F-350&modelYear=2021`
- **按 VIN 查询（更精确）：** `https://api.nhtsa.dot.gov/recalls/recallsByVin?vin=XXXXX`

如果已存储 VIN，优先使用基于 VIN 的查询方式。否则使用品牌/型号/年份查询。

### 召回数据存储

在 `state.json` 中按车辆记录召回信息：
```json
{
  "recalls": {
    "last_checked": "2026-01-26",
    "open_recalls": [
      {
        "nhtsa_id": "26V-123",
        "component": "FUEL SYSTEM",
        "summary": "Fuel line may crack under pressure",
        "consequence": "Fuel leak, fire risk",
        "remedy": "Dealer will replace fuel line at no cost",
        "date_reported": "2025-12-01",
        "status": "open"
      }
    ],
    "completed_recalls": [
      {
        "nhtsa_id": "24V-456",
        "component": "ELECTRICAL",
        "summary": "Battery cable may corrode",
        "date_completed": "2025-06-15",
        "notes": "Done at dealer"
      }
    ]
  }
}
```

### 何时检查
- **每月定时检查：** 将召回检查纳入里程检查的定时任务中。无论车辆的检查频率如何，每月都检查一次召回信息。
- **添加新车辆时：** 立即检查。
- **用户请求时：** 用户询问“我的卡车有召回吗？”

### 召回报告格式

当用户报告完成召回时，将召回信息从 `open_recalls` 移动到 `completed_recalls` 中，并记录完成日期。

---

## 燃油/MPG 跟踪

追踪加油记录，以监控燃油经济性，及早发现机械问题，并记录燃油消耗情况。

### 记录加油信息
当用户表示“加了油”或报告加油情况时：
1. 记录：**日期**、**加仑数**、**费用**（总费用或每加仑价格）、**里程表读数**。
2. 计算 MPG：`（current_odometer - previous_odometer） / gallons`
3. 添加到车辆的 `fuel_history` 数组中。
4. 检查 MPG 是否异常。

### 燃油历史记录
```json
{
  "date": "2026-01-20",
  "gallons": 32.5,
  "cost": 108.55,
  "price_per_gallon": 3.34,
  "odometer": 61300,
  "mpg": 14.2,
  "partial_fill": false,
  "notes": ""
}
```

### MPG 计算方法
- **每次加油的 MPG：** `(current_odometer - previous_fill_odometer) / gallons`（如果上次加油不完整，则忽略）
- **滚动平均值：** 计算最近 10 次加油的 MPG 平均值（如果次数少于 10 次，则计算全部记录的平均值） |
- **趋势分析：** 比较最近 3 次加油的 MPG 是否异常。

### 异常检测
如果某次加油的 MPG 比平均值低 15% 以上，标记为异常：
```
⚠️ MPG Alert — [Vehicle]
Last fill-up: 10.5 MPG (your average is 14.2 MPG)
26% below your rolling average — this could indicate:
- Tire pressure issues
- Air filter needs replacement
- Fuel system issue
- Change in driving conditions (heavy towing, headwinds)
- Mechanical problem developing

Check tire pressures first, then review recent driving conditions.
```

### 燃油报告格式

当用户询问“我的燃油经济性如何？”或请求 MPG 报告时：
```
⛽ Fuel Report — [Vehicle]
Last fill-up: [X] MPG on [date]
Rolling average: [X] MPG (last 10 fills)
Trend: [improving/stable/declining]
Total fuel cost (YTD): $[X]
Total gallons (YTD): [X]
Average cost per gallon: $[X]
```

### 部分加油情况
如果用户未加满油，标记 `partial_fill: true`。在这种情况下，跳过 MPG 计算，但仍记录费用和加仑数。

---

## 实际费用跟踪

追踪用户实际支付的维护费用，以生成准确的费用记录。

### 记录费用
当用户记录完成的服务时：
1. 确认服务详情后，询问：“您实际支付了多少钱？”（或根据用户提供的数据记录）
2. 将费用作为 `actual_cost` 存储在 `service_history` 中。
3. 如果用户不知道或不愿意提供费用，记录为 `null`——不要忽略该记录。

### 服务历史记录（包含费用）
```json
{
  "service_id": "oil_filter",
  "date": "2025-11-15",
  "miles": 58000,
  "hours": null,
  "notes": "Full synthetic, Motorcraft filter",
  "actual_cost": 125.00,
  "cost_type": "shop",
  "provider": {
    "id": "jims_diesel",
    "name": "Jim's Diesel Repair"
  }
}
```

`cost_type` 的值包括：`diy`（自己动手）、`shop`（独立机械师）、`dealer`（经销商）、`warranty`（保修）、`recall`（免费）。

### 费用分析
根据用户请求，提供以下报告：
- **每辆车每年的费用：** “您今年在 F-350 上花费了 X 美元”
- **实际费用与预算费用对比：** 对比 `actual_cost` 和服务计划的费用估算
- **费用分类：** 按服务类型分类（如机油更换、滤清器更换等）
- **年度总费用：** 每辆车的总维护费用

### 年度总结
根据用户请求或在年底提供年度总结：
```
💰 [Year] Maintenance Summary — [Vehicle]
Total spent: $[X]
Services performed: [count]
Biggest expense: [service] — $[X]
Average cost per service: $[X]
vs. Estimated: $[X] ([over/under] by [X]%)
```

---

## 保修跟踪

追踪保修信息，了解保险覆盖的范围，并在保修到期前发出提醒。

### 保修记录结构
```json
{
  "type": "factory_powertrain",
  "provider": "Ford",
  "start_date": "2021-03-15",
  "end_date": "2026-03-15",
  "start_miles": 0,
  "end_miles": 60000,
  "coverage_details": "Engine, transmission, transfer case, driveshaft, axle assemblies",
  "status": "active",
  "contact_phone": "1-800-392-3673",
  "claim_number": null,
  "notes": ""
}
```

### 保修类型
| 保修类型 | 通常覆盖的范围 |
|------|-----------------|
| **factory_bumper_to_bumper** | 除易磨损部件外的所有项目，保修期最短 |
| **factory_powertrain** | 发动机、变速箱、传动系统——保修期较长 |
| **factory_corrosion** | 车身锈蚀——通常保修期超过 5 年 |
| **factory_emissions** | 排放系统部件——联邦法规要求的主要部件保修期 8 年/80,000 英里 |
| **extended** | 第三方或制造商提供的延长保修 |
| `parts_warranty` | 从商店/经销商处购买的特定部件（例如“新发电机，2 年保修”） |
| `labor_warranty` | 商店提供的特定维修项目的劳动保障 |

### 保修到期提醒
在每次服务检查时检查保修情况。在以下情况下发出提醒：
- **距离保修到期还有 3 个月内** |
- **行驶里程达到保修期限的 3,000 英里以内**（以较早者为准）

提醒格式：
```
⚠️ WARRANTY EXPIRING SOON
[Vehicle] — [Warranty type] from [Provider]
Expires: [date] or [miles] miles (whichever first)
Remaining: ~[X] months / ~[X] miles
Coverage: [details]
💡 Schedule any warranty-covered concerns before expiration!
```

### 保修覆盖检查
当用户询问“这项维修是否在保修范围内？”或发现需要维修时：
1. 检查车辆的所有有效保修信息。
2. 根据服务类型判断是否在保修范围内。
3. 如果在保修范围内，提醒用户：“这项维修可能在 [保修类型] 的 [保修期限] 内免费。”（并提供联系方式）

### 状态值
- `active` — 仍在保修期内 |
- `expiring_soon` — 保修即将到期 |
- `expired` — 保修已过期 |
- `claimed` — 已提出保修索赔

---

## 旅行前/季节性检查清单

在用户提到旅行或季节性变化时，生成针对特定车辆的检查清单。

### 触发条件
当用户说以下内容时激活检查清单：
- “我要去旅行” / “我要去 [地点]”
- “这个周末要拖车” / “要把房车开到 [地点]”
- “准备过冬” / “该进行冬季保养” |
- “春天来了” / “该进行冬季准备” |
- “这个周末要去越野” / “要去越野”

### 检查清单生成方式
结合以下信息生成清单：
1. **逾期/即将到期的服务**：从服务记录中提取相关服务 |
2. **目的地的天气**：根据目的地查询天气预报（炎热、寒冷、下雨、下雪等）
3. **旅行类型相关的物品**：根据用户的旅行计划 |
4. **季节性项目**：根据当前日期和地点

### 拖车/房车检查清单（卡车 + 拖车/房车）
```
🚛 Pre-Tow Checklist — [Truck] + [Trailer/RV]

TRUCK:
□ Engine oil level
□ Coolant level
□ DEF level (diesel)
□ Tire pressures (loaded spec: front [X] psi, rear [X] psi)
□ Brake controller connected and tested
□ Transmission temp gauge working
□ All lights working
□ Mirrors adjusted for towing

HITCH/CONNECTION:
□ Fifth wheel / gooseneck / ball mount secured
□ Pin box / kingpin locked (verify with tug test)
□ Safety chains crossed under tongue
□ Breakaway cable attached
□ 7-pin connector — test all lights (brake, turn, running, reverse)
□ Breakaway battery charged

TRAILER/RV:
□ Tire pressures (spec: [X] psi) — check age on sidewall
□ Wheel lug torque (spec: [X] ft-lbs)
□ Slides fully retracted and locked
□ Awning secured
□ Fridge set to travel mode (or propane off)
□ All compartments latched
□ Stabilizer jacks fully up
□ Roof vents closed
□ TV antenna down
□ Water heater bypass (if applicable)
□ LP gas tank valve position (check local laws for travel)
□ Cargo secured inside (open fridge, cabinets after arrival)

OVERDUE/DUE SERVICES:
[List any from service review]
```

### 冬季保养前的检查清单：
- 防冻液保护水平（使用液位计检测）
- 电池电量测试（寒冷天气会降低电池容量 30-50%）
- 雨刷片和清洗液（检查是否适合寒冷天气）
- 轮胎状况（是否需要四季轮胎）
- 暖气系统（柴油卡车）
- 房车：完成冬季保养程序（排放系统排水、加热器检查）
- 船只：检查发动机、防冻液、水箱、排水系统）

### 夏季保养前的检查清单：
- 空调系统检查（在使用前测试）
- 冷却液水平和状态
- 房车：检查空调系统、排水系统、水箱
- 检查轮胎压力（高温会增加压力）
- 检查皮带和软管（高温会增加磨损）

### 旅行前的常规检查：
- 所有液体的水平
- 轮胎压力和状况
- 灯具和信号灯
- 刹车系统（检查是否需要更换）
- 应急工具（跳线、手电筒、急救用品）

---

## 里程预测

根据行驶历史数据预测下次服务的时间。

### 计算方法
至少需要 `mileage_history` 中有 2 个数据点，且数据点之间间隔至少 14 天。

```
average_miles_per_month = (latest_miles - earliest_miles) / months_between_readings
```

使用完整的历史数据计算平均里程，但如果最近的使用模式有显著变化，应更重视最近的数据。

### 服务日期预测
对于每项服务：
1. 计算剩余里程：`next_due_miles - current_miles`
2. 预计服务间隔：`miles_remaining / average_miles_per_month`
3. 预计服务日期：`today + projected_months`
4. 同时检查基于时间的间隔。

将结果包含在服务报告中：
```
📅 Projected Service Dates
- Oil Change: ~[Month Year] (at ~[X] miles)
- Fuel Filters: ~[Month Year] (at ~[X] miles)
- Trans Fluid: ~[Month Year] (at ~[X] miles)
```

### 预算预测
根据用户请求或在年度报告中提供预算预测：
```
💰 Next 6-Month Budget Forecast — [Vehicle]
At [X] miles/month, expect:
- Oil change (~[Month]): $[X]
- Fuel filters (~[Month]): $[X]
- Cabin air filter (~[Month]): $[X]
Total estimated: $[X]
```

### 数据不足时的处理
如果数据点少于 2 个或数据间隔过短：
- 提示：“需要更多行驶历史数据才能进行预测——下次检查时提供”
- 即便如此，仍会显示基于里程的预估结果。

---

## 服务提供商跟踪

追踪服务提供的位置，以便方便查询和管理服务提供商。

### 收集服务提供商信息
在记录完成的服务时，可选地询问：
- **服务提供商名称**（或“与上次相同”/“自己动手”）
- **服务地点**（城市/地址）
- **电话号码**
- **满意度评分**（1-5 分）
- **零件保修**（期限）
- **劳动保修**（期限）

不要让这个步骤变得繁琐——如果用户只说了“换了机油”，先记录服务信息，再询问服务地点。如果用户不感兴趣，可以省略此步骤。

### 服务提供商信息存储
服务提供商信息存储在两个地方：
1. `state.json` 根目录下的 `global providers` 数组——可在多辆车之间重复使用：
```json
{
  "id": "jims_diesel",
  "name": "Jim's Diesel Repair",
  "location": "123 Main St, Mesa, AZ",
  "phone": "480-555-1234",
  "specialties": ["diesel", "trucks"],
  "rating": 5,
  "notes": "Great with Power Stroke engines"
}
```

2. **每个 service_history 记录** 中——通过 `id` 和特定服务相关的保修信息进行关联：
```json
{
  "provider": {
    "id": "jims_diesel",
    "name": "Jim's Diesel Repair",
    "parts_warranty_months": 12,
    "labor_warranty_months": 6
  }
}
```

### 服务提供商查询
处理以下问题：
- “我上次在哪里换机油？” → 在 `service_history` 中查找最近的一次机油更换记录，返回服务提供商信息
- “我在哪里进行变速箱服务？” → 按 `service_id` 查找服务记录
- “显示 Jim 的所有服务记录” → 按 `provider.id` 过滤服务记录
- “Jim 的电话号码是多少？” → 在 `providers` 数组中查找
- “使用的是上次的服务提供商” → 使用最近的服务记录中的服务提供商信息

---

## 税务抵扣集成

对于标记为商业用途的车辆，帮助追踪可抵扣的维护费用。

### 配置
在 `state.json` 中为每辆车设置：
```json
{
  "business_use": true,
  "business_use_percent": 50
}
```

如果 `business_use` 为 `true` 且未设置百分比，默认假设为 100%。

### 扣税抵扣记录
当商业用途车辆的维护费用有 `actual_cost` 时：
1. 计算可抵扣部分：`actual_cost × (business_use_percent / 100)`
2. 提醒用户：
   ```
   💼 Tax Note: This $450 trans fluid service is 50% business use.
   Deductible amount: $225.00 (vehicle maintenance expense)
   ```
3. 建议用户将相关信息记录到 `skills/tax-professional/SKILL.md` 中：
   ```
   Want me to log this to your tax deductions? 
   → $225.00 as vehicle maintenance expense
   ```

### 与税务专业技能的集成
如果用户同意，参考 `skills/tax-professional/SKILL.md` 并将相关信息记录到 `data/tax-professional/YYYY-expenses.json` 中：
```json
{
  "date": "2026-01-15",
  "category": "vehicle_maintenance",
  "description": "Trans fluid service — F-350 (50% business use)",
  "amount": 225.00,
  "vehicle": "f350",
  "full_cost": 450.00,
  "business_percent": 50,
  "receipt": false
}
```

### 年度总结
根据用户请求或在年底提供年度总结：
```
💼 [Year] Business Vehicle Deductions — [Vehicle]
Total maintenance costs: $[X]
Business use: [X]%
Deductible amount: $[X]
Services included: [count] services
```

---

## 紧急信息卡

存储并快速检索车辆的关键信息，以便在紧急情况下使用，如路边援助、查找零件或获取快速参考。

### 紧急信息结构
在 `state.json` 中为每辆车存储紧急信息：
```json
{
  "emergency_info": {
    "vin": "1FT8W3BT0MED12345",
    "insurance_provider": "State Farm",
    "policy_number": "SF-123456789",
    "roadside_assistance_phone": "1-800-555-1234",
    "tire_size_front": "275/70R18",
    "tire_size_rear": "275/70R18",
    "tire_pressure_front_psi": 65,
    "tire_pressure_rear_psi": 80,
    "oil_type": "15W-40 CK-4 Full Synthetic",
    "oil_capacity": "15 quarts",
    "coolant_type": "Motorcraft Orange VC-3DIL-B",
    "def_type": "API certified DEF",
    "trans_fluid": "Motorcraft Mercon ULV",
    "tow_rating_lbs": 20000,
    "gvwr_lbs": 14000,
    "gcwr_lbs": 37000,
    "payload_lbs": 4300,
    "key_fob_battery": "CR2450",
    "fuel_type": "Diesel (Ultra Low Sulfur)",
    "fuel_tank_gallons": 48,
    "lug_nut_torque_ft_lbs": 165,
    "jack_points": "Frame rails, front and rear",
    "notes": ""
  }
}
```

### 快速查询
即时响应以下问题：
- “我的 VIN 是什么？” → 返回 VIN
- “我的卡车轮胎规格是什么？” → 轮胎尺寸和压力
- “我的卡车使用哪种机油？” → 机油类型和容量
- “保险信息？” → 保险公司、保单号码、电话号码
- “路边援助电话是多少？” → 路边援助电话号码
- “我的拖车等级是多少？” → 拖车等级、车辆总重量（GVWR）
- “钥匙扣电池的型号是什么？” → 电池型号
- “千斤顶螺母的扭矩要求是多少？” → 千斤顶螺母的扭矩要求

### 紧急信息卡的展示格式
当用户询问紧急信息时：
```
🚨 Emergency Info — [Vehicle Label]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIN: [vin]
Insurance: [provider] — Policy #[number]
Roadside: [phone]

🔧 Specs
Tires: F:[size] R:[size]
Pressure: F:[X]psi R:[X]psi
Oil: [type] ([capacity])
Coolant: [type]
Fuel: [type] ([tank] gal)
Key fob battery: [type]

📏 Ratings
Tow: [X] lbs | GVWR: [X] lbs
GCWR: [X] lbs | Payload: [X] lbs
Lug torque: [X] ft-lbs
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 数据收集
在添加新车辆时，收集必要的信息。许多规格信息可以从车辆年份/品牌/型号中查询。用户可以逐步填写个人信息（如保险信息、路边援助电话）。部分字段可以为空。

---

## 每英里成本分析

计算每英里的总维护成本。

### 计算方法
至少需要 `mileage_history` 中有 2 个数据点。

```
total_miles_driven = latest_miles - earliest_miles (from mileage_history)

Maintenance cost per mile = total_actual_costs / total_miles_driven
Fuel cost per mile = total_fuel_cost / total_miles_driven
Total operating cost per mile = (total_actual_costs + total_fuel_cost) / total_miles_driven
```

### 报告格式
当用户询问“每英里的成本”或“运营成本”时：
```
📊 Cost Per Mile — [Vehicle]
Period: [earliest date] to [latest date] ([X] miles driven)

Maintenance only: $[X.XX]/mile
Fuel only: $[X.XX]/mile (if fuel tracking active)
Total operating: $[X.XX]/mile

💡 National averages (approximate):
Cars: ~$0.10/mi maintenance, ~$0.12/mi fuel
Trucks: ~$0.14/mi maintenance, ~$0.20/mi fuel (diesel)
Heavy-duty diesel (towing): ~$0.18/mi maintenance, ~$0.25/mi fuel
```

### 车队概览
如果跟踪多辆车，提供对比报告：
```
📊 Fleet Cost Per Mile
[Vehicle 1]: $[X.XX]/mi (maintenance) | $[X.XX]/mi (total)
[Vehicle 2]: $[X.XX]/mi (maintenance) | $[X.XX]/mi (total)
Fleet average: $[X.XX]/mi
```

### 注意事项
- 仅包括有 `actual_cost` 记录的服务（忽略无费用记录的服务）
- 如果没有燃油数据，仅显示维护费用
- 如果数据记录时间较短（<3 个月或 <1,000 英里），提示：“需要更多行驶历史数据才能进行准确预测”
- 随着昂贵的一次性费用的摊销，每英里的成本会逐渐降低

---

## 里程检查（定时任务触发）

定期运行一个定时任务（每周一次，频率尽可能高），根据每辆车的 `check_in_frequency` 和 `last_check_in` 日期检查是否需要检查。同时进行每月的召回检查。

> 提示：**“机械师技能：里程检查”

任务执行时：
1. 读取 `<workspace>/data/mechanic/state.json`
2. 对于每辆车，检查是否需要检查：
   - 如果 `last_check_in` 日期距离上次检查超过 7 天，则需要检查
   - **每周**：如果超过 14 天，则需要检查
   - **每两周**：如果超过 30 天，则需要检查
   - **每月**：如果超过 30 天，则需要检查
   - **每季度**：如果超过 90 天，则需要检查
3. **每月召回检查**：如果任何车辆的 `recalls.last_checked` 超过 30 天，从 NHTSA API 获取最新召回信息并更新状态
4. **如果没有车辆需要检查且未发现新的召回**，回复 `HEARTBEAT_OK`（静默处理）
5. 如果有车辆需要检查，询问这些车辆的当前信息
6. 如果发现新的召回，即使没有车辆需要检查，也包含召回信息
7. 更新状态和 `last_check_in` 字段
8. 为更新后的车辆运行 **服务报告**（包括保修提醒、预测信息）

### 里程检查设置

创建一个每周运行的定时任务。它将内部过滤需要检查的车辆。检查 `<workspace>/USER.md` 中的时区设置。

**定时任务表达式：** `0 17 * * 0`（用户所在时区的每周日下午 5 点）

**定时任务配置：**
- **会话**：将结果发送到用户的聊天频道
- **提示**：读取机械师技能的相关内容，从 `data/mechanic/state.json` 中加载车辆状态。根据每辆车的 `check_in_frequency` 和 `last_check_in` 判断是否需要检查。同时检查是否有超过 30 天的召回。如果没有需要检查的车辆或新的召回，回复 `HEARTBEAT_OK`。否则，询问需要检查的车辆的当前信息，并报告任何新的召回信息。
7. 更新状态和 `last_check_in` 字段
8. 为更新后的车辆运行 **服务报告**（包括保修提醒、预测信息）

### 更改频率

用户可以随时更改每辆车的检查频率：
- “我的越野摩托车每周检查一次” → 更新该车的 `check_in_frequency`
- “减少卡车的检查频率” → 将频率改为每两周
- “将所有车辆的检查频率改为每月一次” → 更新所有车辆的频率

在 `state.json` 中更新车辆的 `check_in_frequency` 并确认更改。

## 里程/行驶时间更新

当用户报告行驶里程或行驶时间时（无论在什么情况下，而不仅仅是每月一次）：
1. 更新车辆的 `current_miles` 和/或 `current_hours`
2. 将 `last_updated` 设置为当前时间
3. 添加到 `mileage_history` 数组中：
```json
{"date": "YYYY-MM-DD", "miles": <value>, "source": "user_reported"}
```
4. 运行 **服务报告**：

## 服务报告

在每次更新里程或行驶时间后，分析车辆的服务记录。

### 对于每项服务：
1. 从 `service_history` 中查找 **上次服务的时间**（根据 `service_id` 进行匹配）
2. 如果从未进行过该服务，假设服务在车辆购买时（`mile 0 / hour 0`）进行过
3. 根据以下间隔计算服务时间：
   - `miles_since_service` 与 `interval_miles` 对比
   - `months_since_service` 与 `interval_months` 对比
   - `hours_since_service` 与 `interval_hours` 对比
4. 分类结果：
   - **🔴 已过期**：超过任何间隔
   - **🟡 即将过期**：在任意间隔的 15% 以内
   - **🟢 未到期**：尚未到期

### 报告格式
**完整报告（发现问题时）：**
```
🔧 Vehicle Service Report

━━━ [Vehicle Label] @ [miles] mi ━━━

⚠️ OPEN RECALLS
- [NHTSA ID] — [Component]: [Summary]
  Remedy: [description] (FREE at dealer)

⚠️ WARRANTY ALERTS
- [Warranty type] from [Provider] — expires [date] or [miles] mi
  [X] months / [X] miles remaining

🔴 OVERDUE
- [service] — [X] miles/months overdue
  💰 DIY: $X | Shop: $X | Dealer: $X
  [💼 [X]% deductible] (if business use)

🟡 DUE SOON
- [service] — due in ~[X] miles/months
  💰 DIY: $X | Shop: $X | Dealer: $X

📅 PROJECTED SCHEDULE (next 6 months)
- [service] — ~[Month Year] at ~[X] mi ($[X] est.)
- [service] — ~[Month Year] at ~[X] mi ($[X] est.)
Total upcoming (6mo): ~$[X]

⛽ FUEL ECONOMY
Current: [X] MPG | Average: [X] MPG | Trend: [stable/improving/declining]
[⚠️ MPG Alert if applicable]

💰 SPENDING (YTD)
Maintenance: $[X] | Fuel: $[X] | Total: $[X]
Cost per mile: $[X.XX]

[Repeat for each vehicle]

🟢 [count] services current across all vehicles
```

**一切正常（简短报告）：**
```
🔧 All vehicles current ✅
[Vehicle] @ [mi] — next: [soonest service] at ~[miles] (~[Month])
No open recalls | Warranties current
```

**当多项服务同时到期时**，提供汇总的预估费用，并建议一次性完成这些服务。

### 条件性显示内容
仅显示有相关数据的部分：
- 如果没有未处理的召回，跳过召回部分
- 如果没有即将到期的保修，跳过保修提醒部分
- 如果没有燃油历史数据，跳过燃油经济性部分
- 如果没有实际费用数据，跳过费用部分
- 如果车辆不是商业用途，跳过费用相关内容

## 记录完成的服务
当用户报告完成了服务（例如“刚换了机油”或“在 65,000 英里时更换了机油”）：
1. 确认是哪辆车和进行了哪些服务
2. 询问费用（非强制）：“您花了多少钱？”
3. （可选）记录服务提供商信息（“在哪里进行的维修？”/“上次是在哪家店？”）
4. 将这些信息添加到该车的 `service_history` 中：
```json
{
  "service_id": "<matching id>",
  "date": "YYYY-MM-DD",
  "miles": <mileage_at_service>,
  "hours": <hours_if_applicable>,
  "notes": "<any details the user mentions>",
  "actual_cost": <amount_or_null>,
  "cost_type": "shop",
  "provider": {
    "id": "<provider_id>",
    "name": "<provider_name>",
    "parts_warranty_months": null,
    "labor_warranty_months": null
  }
}
```
5. 如果是商业用途的车辆，记录可抵扣的费用
6. 建议用户将相关信息记录到税务专业技能中
7. 确认记录的内容
8. 重新计算下次服务的预计时间

## 临时查询
处理关于任何车辆的查询。如果信息不明确，询问具体的车辆。

**示例：**
- “我的下次机油更换是什么时候？” → 查找相关车辆的记录
- “我的卡车使用哪种机油？” → 查看服务计划或紧急信息
- “我需要哪些维护服务？” → 查看所有车辆的完整服务记录
- “我的里程达到了 70,000 英里” → 更新里程记录并运行服务报告
- “我刚换了新轮胎” → 更新服务记录
- “我的新车是什么型号？” → 更新车辆信息
- “我上次更换机油花了多少钱？” → 查看费用估算
- “我的车辆维护费用是多少？” → 提供费用概览
- “我的车辆保修还有效吗？” → 检查保修状态
- “我的车辆在保修范围内吗？” → 根据服务类型查询保修信息
- “我即将出发旅行” → 生成旅行前的检查清单
- “我的变速箱什么时候需要维护？” → 预测下次维护时间
- “我上次在哪里更换机油？” → 查找服务记录
- “我的 VIN 是什么？” → 查找 VIN
- “我的 VIN 是什么？” → 解码 VIN 并显示详细信息
- “我的 VIN 是什么？” → 解码 VIN 并显示详细信息
- “我的 VIN 是什么？” → 解码 VIN 并显示详细信息
- “我的轮胎规格是什么？” → 显示轮胎规格
- “每英里的成本是多少？” → 提供每英里的成本估算
- “我今年的维护费用是多少？” → 提供年度费用总结

## 环境提示

根据用户的位置提供个性化建议：

**炎热气候（沙漠、南部地区）：**
- 电池寿命会显著缩短
- 轮胎在高温环境下容易损坏——建议为停放的车辆安装轮胎保护套
- 冷却系统更易损坏
- 橡胶部件（皮带、软管、密封件）更容易老化
- 车辆排气系统（尤其是房车）容易积尘

**寒冷气候（北部地区、山区）：**
- 房车和船只的冬季保养至关重要
- 电池容量在寒冷环境下会降低
- 检查防冻液保护水平
- 在寒冷季节前检查暖气系统

**多尘/越野环境：**
- 发动机和车厢空气滤清器需要更频繁的维护
- 摩托车和全地形车的发电机空气滤清器需要检查
- 检查 CV 轴承（全地形车/UTV）

**沿海/海洋地区：**
- 需要特别注意防腐蚀
- 更频繁地检查底盘部件
- 检查电气连接

## 成本估算
在标记需要维护的服务时，提供费用估算：
- **DIY** — 仅包含零件费用
- **Shop** — 独立机械师/专业维修店
- **Dealer** — 制造商经销商

在提供一系列服务时，提供 **总费用估算**，以便用户了解一次性维修的总费用。

### 重要提示
- **变速箱冲洗**：许多现代变速箱（尤其是福特 10R 系列和 CVT 变速箱）只能进行排空和再加注，切勿冲洗。务必遵循制造商的建议。
- **房车车顶**：水侵入是房车的主要问题。务必检查密封件和车顶系统。
- **轮胎寿命**：无论胎面磨损情况如何，轮胎通常每 5-6 年需要更换
- **特殊使用情况**：如果经常拖车、运输货物或在极端环境下行驶，车辆几乎总是属于“加强维护”类别
- **零件编号**：在服务计划中包含原厂零件编号，用户可以据此购买替换零件
- **季节性项目**：根据用户的位置和季节调整保养建议

## 其他注意事项
- **定期检查**：根据用户的位置提供相应的检查建议：
- **道路旅行**：提醒用户注意电池寿命、轮胎磨损、冷却系统、防冻液等
- **寒冷地区**：提醒用户检查电池寿命、空调系统、轮胎和暖气系统
- **多尘/越野环境**：提醒用户更频繁地检查发动机和车厢空气滤清器、发电机空气滤清器
- **沿海/海洋地区**：提醒用户检查防腐蚀措施、定期清洗底盘部件和电气系统

---
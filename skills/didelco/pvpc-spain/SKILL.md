---
name: pvpc-spain
description: 查询并优化西班牙光伏电力（PVPC）的价格（适用于家庭用户的2.0TD电价方案）。您可以使用该工具来实现以下目标：  
1. 查看当前电价情况（根据时间段分为高/中/低电价）；  
2. 根据时间区分用电高峰期、平价期和低谷期；  
3. 找到一天中电价最低的时段；  
4. 优化家用电器（如洗衣机、洗碗机、烘干机等）的使用时间，以降低电费成本。
---

# PVPC 西班牙

本技能用于查询西班牙的 PVPC（小型消费者自愿定价）电价，并优化电力消耗。所有数据均来自 ESIOS（西班牙电力公司）的公共 API，适用于 2.0TD 电价方案。

## 可用的查询功能

### 1. 当前电价（含分类信息）

显示根据当日百分位数划分的当前电价（高/中/低）。

```bash
# Precio actual completo
python scripts/get_pvpc.py --now

# Clasificación detallada
python scripts/precio_referencia.py --now
```

**响应包含：**
- 当前电价（€/kWh）
- 当日最低价和最高价
- 电价分类：低（<30% 分位数），中（30-70%），高（>70%）
- 与当日平均电价的偏差

### 2. 电价时段（平价/高峰/低谷）

根据 2.0TD 电价方案，识别当前的电价时段（按工作日调整）。

```bash
# Periodo actual
python scripts/tarifa_periodos.py --now

# Ver todos los periodos
python scripts/tarifa_periodos.py --all
```

**2.0TD 电价时段：**
- **平价时段** 🌙：00:00-08:00（每天）+ 周六/周日全天
- **高峰时段** ⚡：08:00-10:00, 14:00-18:00, 22:00-00:00（周一至周五）
- **低谷时段** 🔴：10:00-14:00, 18:00-22:00（周一至周五）

**注意：** 2.0TD 电价方案的时段在夏季和冬季是相同的。

### 3. 当日最便宜的用电时段

查找电价低于当日 30% 分位数的时段。

```bash
# Rangos baratos (por defecto percentil 30)
python scripts/find_cheap_ranges.py

# Ajustar percentil
python scripts/find_cheap_ranges.py --percentile 40
```

**响应包含：**
- 连续 2 小时及以上的低价时段
- 每个时段的最低价/最高价/平均价
- 相对于当日平均价的节省百分比
- 按时长排序（时长较长的时段排在前面）

### 4. 优化家用电器使用时间

查找连续 N 小时内总用电成本最低的时段。

```bash
# Lavadora (2 horas por defecto)
python scripts/optimize_appliance.py --duration 2 --name lavadora

# Lavavajillas (3 horas)
python scripts/optimize_appliance.py --duration 3 --name lavavajillas

# Secadora (1.5 horas)
python scripts/optimize_appliance.py --duration 2 --name secadora
```

**响应包含：**
- 最佳开始和结束时间
- 整个周期的总成本（€）
- 每小时的价格明细
- 与使用高峰时段相比的节省金额
- 提供最多 2 个成本相差小于 10% 的时段选项

## JSON 输出格式

所有脚本均支持使用 `--json` 参数进行程序化集成：

```bash
python scripts/get_pvpc.py --json
python scripts/find_cheap_ranges.py --json
python scripts/optimize_appliance.py --duration 3 --json
```

## 用户使用示例

**用户：**“现在的电价是多少？”
```bash
python scripts/get_pvpc.py --now
python scripts/precio_referencia.py --now
```

**用户：**“今天什么时候用电最便宜？”
```bash
python scripts/find_cheap_ranges.py
```

**用户：**“我什么时候洗衣服比较合适？”
```bash
python scripts/optimize_appliance.py --duration 2 --name lavadora
```

**用户：**“现在是什么电价时段？”
```bash
python scripts/tarifa_periodos.py --now
```

**用户：**“我什么时候使用洗衣机比较合适？”
```bash
python scripts/optimize_appliance.py --duration 3 --name lavavajillas
```

## 技术说明

- **数据来源：** ESIOS（西班牙电力公司）的公共 API
- **电价方案：** PVPC 2.0TD（功率 <10 kW 的家庭用户）
- **更新频率：** 电价信息每日约在 20:00 公布，适用于次日
- **价格包含内容：** 所有费用（能源费、附加费）均以 €/kWh 计算
- **无需认证：** 使用公共 API，无需 token

## 限制事项

- 历史数据不会本地存储（每次查询均为实时数据）
- “高/中/低”电价分类是基于当日情况，而非历史数据
- 国家节假日不会自动识别（视为工作日）
- 查询 API 需要互联网连接
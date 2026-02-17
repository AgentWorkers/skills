---
name: solar-weather
description: 监控太阳天气状况，包括地磁风暴、太阳耀斑、极光预报以及太阳风数据。该系统使用美国国家海洋和大气管理局（NOAA）空间天气预测中心的实时数据。
version: 1.0.0
author: captmarbles
---

# 太阳天气监测器 🌞

实时追踪太空天气状况！监测来自美国国家海洋和大气管理局（NOAA）太空天气预测中心的太阳耀斑、地磁风暴、极光预报以及太阳风数据。

## 主要功能

🌞 **当前天气状况** - 实时太空天气状态  
📅 **3天预报** - 预测即将发生的太阳活动  
🌌 **极光预报** - 你今天能看到极光吗？  
🌊 **太阳风** - 跟踪太阳风的磁场  
🚨 **警报** - 活动的太空天气警告  
📊 **概览** - 快速全面的天气概览  

适合以下人群：  
- 📻 业余无线电操作员  
- 🌌 极光观测者和摄影师  
- 🛰️ 卫星操作员  
- ⚡ 电网运营商  
- 🌍 太空天气爱好者  

## 使用方法

### 当前太空天气

```bash
python3 solar-weather.py current
```

**输出：**
```
🌞 Space Weather Conditions
   2026-01-27 18:38:00 UTC

   📻 R0: none ✅
      Radio Blackouts (Solar Flares)

   ☢️  S0: none ✅
      Solar Radiation Storm

   🌍 G0: none ✅
      Geomagnetic Storm
```

### 3天预报

```bash
python3 solar-weather.py forecast
```

显示今天、明天以及后天的太阳活动概率。

### 极光预报

```bash
python3 solar-weather.py aurora
```

**输出：**
```
🌌 Aurora Forecast

Current Conditions:
   Geomagnetic: none
   Solar Wind Bz: -2 nT

Tomorrow (2026-01-28):
   Geomagnetic: minor

🔮 Aurora Outlook:
   ⚠️  MODERATE - Aurora possible at high latitudes
```

### 太阳风数据

```bash
python3 solar-weather.py solarwind
```

**输出：**
```
🌊 Solar Wind Magnetic Field
   Time: 2026-01-27 18:36:00.000
   Bt: 8 nT (Total Magnitude)
   Bz: -2 nT (North/South Component)

   ✅ Slightly negative Bz
```

**注意：** 负值的Bz值（尤其是< -5 nT）有利于极光的出现！

### 活动警报

```bash
python3 solar-weather.py alerts
```

显示NOAA发布的活动太空天气观察、警告和警报。

### 快速概览

```bash
python3 solar-weather.py summary
```

提供当前天气状况、太阳风以及明天预报的全面概览。

## 理解太空天气等级

NOAA使用三个等级来衡量太空天气的严重程度：

### R等级 - 无线电中断（太阳耀斑）  
- **R0**：无影响  
- **R1-R2**：轻微/中等 - 高频无线电通信受干扰  
- **R3-R5**：强烈/严重/极端 - 高频无线电完全中断  

### S等级 - 太阳辐射风暴  
- **S0**：无影响  
- **S1-S2**：轻微/中等 - 卫星可能出现异常  
- **S3-S5**：强烈/严重/极端 - 卫星受损，宇航员可能受到辐射  

### G等级 - 地磁风暴（极光）  
- **G0**：无风暴  
- **G1-G2**：轻微/中等 - 高纬度地区可能出现极光  
- **G3-G5**：强烈/严重/极端 - **中纬度地区也能看到极光！**  

## Clawdbot的示例查询语句  

- *"当前太空天气状况如何？"*  
- *"今晚有极光预报吗？"*  
- *"显示太阳风数据"*  
- *"有地磁风暴警告吗？"*  
- *"给我一个太空天气概览"*  
- *"我在[地点]能看到极光吗？"*  

## JSON输出  

在命令后添加`--json`即可获取结构化数据：  

```bash
python3 solar-weather.py current --json
python3 solar-weather.py aurora --json
```

## 数据来源  

所有数据均来自**NOAA太空天气预测中心（SWPC）**：  
- 美国政府官方的太空天气监测机构  
- 实时更新  
- 免费公开API  
- https://www.swpc.noaa.gov/  

## 极光观测者的小贴士 🌌  

**观测极光的最佳条件：**  
1. **地磁风暴**（G1级或更高等级）✅  
2. **负值的Bz值**（< -5 nT）✅  
3. **晴朗、黑暗的天空** 🌙  
4. **高纬度地区**（或在重大风暴期间观察中纬度地区）  

**观测建议：**  
- 每天查看极光相关指令  
- 关注G等级的警告  
- 监测太阳风的Bz值  
- 极光活动通常在日落后1-2小时达到高峰  

## 业余无线电操作员 📻  

**高频无线电传播：**  
- **R等级事件**会导致高频无线电通信中断  
- **太阳耀斑**会引起电离层突然扰动  
- 在比赛或无线电通信前查看当前天气状况  
- 关注警报信息，以防无线电中断  

## 未来功能计划：  
- 基于位置的极光可见性预测  
- 重大事件的通知推送  
- 历史风暴数据  
- 太阳耀斑预测  
- 风暴期间的卫星运行预警  

祝您观测太空天气愉快！🌞⚡🌌
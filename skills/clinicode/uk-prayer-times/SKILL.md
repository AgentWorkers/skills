---
name: uk-prayer-times
version: 1.0.0
description: 获取英国任何地点的即时、准确的伊斯兰教祷告时间。系统会自动检测您的所在城市，或接受您输入的任何英国地点名称（包括城市、城镇、行政区）。通过智能模糊搜索功能处理拼写错误。显示晨礼（Fajr）、日出（Sunrise）、正午（Dhuhr）、下午（Asr）、日落（Maghrib）和宵礼（Isha）的时间，采用12小时制格式。使用Aladhan API和ISNA计算方法（英国标准）进行时间计算。非常适合英国的穆斯林查询每日祷告时间。
---

# 英国祈祷时间

获取英国任何地点的即时、准确的伊斯兰祈祷时间。系统会自动检测您的所在城市，或接受您输入的任何英国地点名称（如城市、城镇、行政区）。通过智能模糊搜索功能处理拼写错误。以12小时制显示晨礼（Fajr）、日出时间（Sunrise）、正午礼（Dhuhr）、下午礼（Asr）、日落礼（Maghrib）和宵礼（Isha）的时间。使用Aladhan API的ISNA计算方法（英国标准），非常适合英国穆斯林查询每日祈祷时间。

## 使用方法

**根据您的位置获取英国的祈祷时间：**
```
prayer times
```

**指定英国的某个城市：**
```
prayer times Birmingham
prayer times Leicester
prayer times Woolwich
prayer times Tower Hamlets
```

**查询特定类型的祈祷时间：**
```
Asr in Leicester
Maghrib in Leicester
Fajr in Woolwich
```

系统能够识别拼写错误，例如“Leicestr”或“Bimringham”等名称也能被正确搜索到！

## 主要特点

✅ 通过IP地址自动检测您的位置  
✅ 支持英国的任何城市、城镇或地区  
✅ 能够处理拼写错误  
✅ 结果顶部会清晰显示地点名称  
✅ 采用12小时制（AM/PM）  
✅ 使用ISNA计算方法（英国标准）  

## 示例  
```bash
python uk_prayer_times.py
# Auto-detects and shows times

python uk_prayer_times.py London
# Shows times for London

python uk_prayer_times.py Woolwich
# Shows times for Woolwich

python uk_prayer_times.py "Tower Hamlets"
# Shows times for Tower Hamlets (multi-word works!)
```  

## 数据来源  

- **祈祷时间数据来源：** Aladhan API（ISNA计算方法）  

## 权限要求  

- 需要互联网连接以获取位置信息和祈祷时间  
- 不需要访问文件系统  
- 不会存储任何个人数据  

## 输出格式  
```
==================================================
🕌 PRAYER TIMES - BIRMINGHAM
📅 08 Feb 2026
==================================================

Fajr:    06:02 AM
Sunrise: 07:39 AM
Dhuhr:   12:23 PM
Asr:     02:38 PM
Maghrib: 05:08 PM
Isha:    06:44 PM

==================================================
```  

地点名称会清晰地显示在页面顶部，让您随时知道当前显示的是哪个地点的祈祷时间。  

## 适用人群  

- 需要查询每日祈祷时间的英国穆斯林  
- 希望获取当地祈祷时间的旅行者  
- 需要快速、准确祈祷时间信息的用户  
- 适用于英国的任何地点（城市、城镇、行政区、社区）  

## 版本信息  

1.0.0 – 初始版本
---
name: prayer-times
version: 1.0.0
description: 获取全球任何地点的即时、准确的伊斯兰祈祷时间。系统会自动检测您的所在城市，或您可手动输入任意城市/国家名称；支持智能模糊搜索功能以处理输入错误。显示晨礼（Fajr）、日出（Sunrise）、正午（Dhuhr）、下午（Asr）、日落（Maghrib）和晚礼（Isha）的时间，时间格式为12小时制。适用于英国、美国、中东、亚洲、欧洲、澳大利亚、非洲等地区。该工具采用Aladhan API提供的ISNA计算方法，非常适合全球穆斯林查询每日祈祷时间。
---

# 全球伊斯兰祈祷时间查询

随时随地获取全球任何地点的伊斯兰祈祷时间。系统会自动检测您的所在城市，或您也可以手动输入城市/国家名称。通过智能模糊搜索功能，能够有效处理拼写错误。非常适合全球的穆斯林用户。

## 使用方法

**自动检测您的位置：**
```
prayer times
prayer times today
what time is prayer?
```

**输入任意城市名称：**
```
prayer times Makkah
prayer times Madinah
prayer times Dubai
prayer times London
prayer times New York
prayer times Karachi
prayer times Jakarta
prayer times Istanbul
prayer times Sydney
```

**查询特定祈祷时间：**
```
Asr in Dubai
Maghrib in Makkah
Fajr in Cairo
Dhuhr in New York
Isha in Kuala Lumpur
```

即使输入错误（如“Meca”而非“Mecca”、“Dubay”而非“Dubai”等），系统也能通过模糊搜索找到正确结果！

## 主要功能

✅ 通过IP地址自动检测您的位置  
✅ 支持全球任意城市  
✅ 能够处理拼写错误  
✅ 结果顶部会清晰显示所在城市名称  
✅ 采用12小时制（AM/PM）  
✅ 使用ISNA算法计算祈祷时间  

## 示例  
```bash
python prayer_times.py
# Auto-detects and shows times

python prayer_times.py Makkah
# Shows times for Makkah, Saudi Arabia

python prayer_times.py "New York"
# Shows times for New York, USA

python prayer_times.py Dubai
# Shows times for Dubai, UAE

python prayer_times.py Istanbul
# Shows times for Istanbul, Turkey
```

## 支持的城市  

**全球各地均可查询！**  
- **中东地区：** 麦加（Makkah）、麦地那（Madinah）、迪拜（Dubai）、利雅得（Riyadh）、吉达（Jeddah）、开罗（Cairo）、耶路撒冷（Jerusalem）、安曼（Amman）、多哈（Doha）、科威特城（Kuwait City）  
- **亚洲地区：** 卡拉奇（Karachi）、拉合尔（Lahore）、达卡（Dhaka）、雅加达（Jakarta）、吉隆坡（Kuala Lumpur）、新加坡（Singapore）、孟买（Mumbai）、德里（Delhi）、伊斯兰堡（Islamabad）  
- **欧洲地区：** 伦敦（London）、巴黎（Paris）、柏林（Berlin）、阿姆斯特丹（Amsterdam）、布鲁塞尔（Brussels）、罗马（Rome）、马德里（Madrid）、伊斯坦布尔（Istanbul）  
- **英国地区：** 伯明翰（Birmingham）、曼彻斯特（Manchester）、莱斯特（Leicester）、格拉斯哥（Glasgow）、布拉德福德（Bradford）、利兹（Leeds）  
- **美洲地区：** 纽约（New York）、多伦多（Toronto）、芝加哥（Chicago）、洛杉矶（Los Angeles）、休斯顿（Houston）、蒙特利尔（Montreal）  
- **非洲地区：** 开罗（Cairo）、卡萨布兰卡（Casablanca）、突尼斯（Tunis）、内罗毕（Nairobi）、约翰内斯堡（Johannesburg）  
- **澳大利亚地区：** 悉尼（Sydney）、墨尔本（Melbourne）、珀斯（Perth）、布里斯班（Brisbane）  

## 数据来源  

- **位置检测：** ipapi.co（通过IP地址自动检测）  
- **地理编码：** OpenStreetMap Nominatim（全球覆盖）  
- **祈祷时间：** Aladhan API（采用ISNA算法计算）  

## 所需权限  

- 需要互联网连接以获取位置信息和祈祷时间  
- 不需要访问文件系统  
- 不会存储任何个人数据  

## 输出格式  
```
============================================================
🕌 PRAYER TIMES - MAKKAH, SAUDI ARABIA
📅 08 Feb 2026
============================================================

Fajr:    05:12 AM
Sunrise: 06:34 AM
Dhuhr:   12:28 PM
Asr:     03:42 PM
Maghrib: 06:21 PM
Isha:    07:51 PM

============================================================
```

结果顶部会清晰显示城市名称及所在国家。  

## 适用人群  

- 需要查询每日祈祷时间的全球穆斯林  
- 需要了解当地时间的旅行者  
- 回国后需要查看家乡祈祷时间的海外移民  
- 前往穆斯林国家的朝圣者  
- 在国外留学的学生  
- 商务旅行者  

## 版本信息  

1.0.0 – 初始版本（全球覆盖）
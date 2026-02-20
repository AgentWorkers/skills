---
name: ramadan-times
description: 这是一款智能的斋月时间助手应用，能够自动检测用户的位置，并以用户选择的语言提供准确的开斋时间（iftar）和封斋时间（sahur）。该应用支持全球100多个城市，并提供土耳其语、英语、阿拉伯语等多种语言版本。
triggers:
  - ramazan
  - iftar
  - sahur
  - oruç
  - ramadan
  - prayer times
  - iftar saati
  - when is iftar
  - sahur time
metadata:
  openclaw:
    emoji: "🌙"
    requires:
      bins: ["curl", "date"]
    settings:
      location: auto-detect
      language: auto-detect
---
# 斋月时间助手 🌙  
智能的斋月时间服务，支持自动位置检测和多语言功能。  

## 主要功能  
- 🌍 自动检测用户所在位置及时区  
- 🌍 支持全球100多个城市  
- 🗣️ 多语言支持：土耳其语（TR）、英语（EN）、阿拉伯语（AR）、德语（DE）、法语（FR）、西班牙语（ES）、俄语（RU）  
- ⏰ 实时倒计时功能（直至开斋时间）  
- 📅 周期性日程安排  
- 🔔 每日提醒功能  

## 使用方法  
只需自然地提问：  
- “开斋时间是什么时候？”  
- “封斋时间是什么时候？”  
- “斋月什么时候开始？”  
- “伊斯坦布尔的开斋时间？”  
- “伦敦的开斋时间？”  

## 自动检测机制  
1. 从OpenClaw配置中获取用户时区  
2. 未找到用户时区时，默认使用伊斯坦布尔时区  
3. 支持用户手动指定查询城市  

## 支持的语言  
| 代码 | 语言 |  
|------|----------|  
| tr | 土耳其语 |  
| en | 英语 |  
| ar | 阿拉伯语 |  
| de | 德语 |  
| fr | 法语 |  
| es | 西班牙语 |  
| ru | 俄语 |  

## 回答示例  
### 土耳其语（自动检测）  
```
🌙 RAMADAN - İstanbul

📅 20 Şubat 2026, Cuma

🌅 Sahur: 04:30
🌅 İftar: 18:47

⏰ İftara: 5 saat 23 dakika
```  

### 英语（自动检测）  
```
🌙 RAMADAN - Istanbul

📅 Friday, February 20, 2026

🌅 Sahur: 04:30
🌅 Iftar: 18:47

⏰ Time until iftar: 5 hours 23 minutes
```  

## 支持的城市  
主要城市包括：  
- 伊斯坦布尔、安卡拉、伊兹密尔  
- 伦敦、纽约、洛杉矶、迪拜、开罗  
- 巴黎、柏林、莫斯科、东京  
- 以及更多城市……  

## 数据来源  
1. sunrise-sunset.org（日出/日落时间数据）  
2. 祈祷时间API（备用数据源）  
3. 手动计算（紧急情况下的备用方案）  

## 智能特性  
1. **自动语言切换**：根据用户选择或默认使用英语  
2. **自动位置识别**：根据系统时区获取信息  
3. **城市查询**：用户可手动输入城市名称  
4. **倒计时功能**：计算并显示距离开斋的时间  
5. **下周日程**：显示整周的日程安排  

## Cron任务集成  
可用于设置每日开斋时间提醒：  
```
0 17 * * * - "İftara 2 saat kaldı!" reminder
```
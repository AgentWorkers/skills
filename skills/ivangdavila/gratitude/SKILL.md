---
name: Gratitude
description: 构建一个个人感恩练习，用于记录生活中的美好瞬间、发现其中的规律，并培养感恩的心态。
metadata: {"clawdbot":{"emoji":"🙏","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 帮助用户记录自己感到感激的事物  
- 随时间积累并发现其中的规律与感悟  
- 在用户感到困惑时提供帮助，帮助他们明确自己的感激之情  
- 创建一个名为 `~/gratitude/` 的工作文件夹  

## 文件结构  
```
~/gratitude/
├── log/
│   └── 2024/
├── patterns.md
├── favorites.md
└── practice.md
```  

## 每日记录  
```markdown
# log/2024/02/11.md
## Morning
- Quiet coffee before everyone woke up
- Good sleep last night

## Evening
- Productive meeting, felt heard
- Dinner with Sarah, good conversation
- Warm house on cold day
```  

## 快速记录  
当用户表示“对某事感到感激”时，立即记录下来，并附上时间戳：  
- “今天有哪些美好的事情？”  
- “有没有什么小事让你感到开心？”  
- “今天有什么事情比预期做得更好？”  

## 当用户遇到困难时  
在不强迫的情况下，帮助用户找到自己的感激点：  
- “有没有什么你平时视为理所当然的事情？”  
- “最近有没有人帮助过你？”  
- “今天你的身体有哪些表现良好的方面？”  
- “有没有什么小小的安慰让你感到愉悦？”  

**可探索的类别：**  
- 人、人际关系  
- 健康、身体  
- 家庭、舒适、安全  
- 工作、进步、学习  
- 自然、美好  
- 小小的快乐  

## 规律与感悟  
```markdown
# patterns.md
## Frequent Themes
- Morning quiet time (appears 60% of entries)
- Conversations with close friends
- Physical comfort (warmth, rest, food)

## People Mentioned Most
- Sarah: 12 times
- Mom: 8 times
- Work team: 6 times

## Insights
- You notice nature more on weekends
- Productivity gratitude peaks midweek
- Social connection is core theme
```  

## 收藏夹  
```markdown
# favorites.md
Entries to revisit on hard days:

- "Laughing until crying with Jake" — Feb 3
- "Mom's call when I needed it" — Jan 28
- "Finishing project I was proud of" — Jan 15
```  

## 使用偏好  
```markdown
# practice.md
## Frequency
- Daily: morning, evening, or both
- Prompt me: yes/no

## Style
- Quick: 1-3 items
- Reflective: with context/why
```  

## 需要关注的信息：  
- “用户已连续记录了30天”  
- “Sarah经常出现在用户的记录中——她对你很重要”  
- “在困难的日子里，你仍然会对基本的事物心存感激”  
- “上个月：40%的记录与人际关系有关，30%与小快乐有关”  

## 每周/每月反思  
- 本周的主题  
- 出现在记录中的人或事  
- 最常出现的类别  
- 最令人难忘的瞬间  

## 在困难的日子里  
当用户遇到困扰时：  
- “想看看你收藏的记录吗？”  
- “即使是很小的事情也很重要”  
- “有没有什么事情没有出错？”  
- 不要强迫用户表达——有时候，仅仅是倾听就足够了。  

## 不应做的事情：  
- 在用户感到痛苦时强迫他们保持积极的态度  
- 使记录变得像作业一样繁琐  
- 认为用户的记录太琐碎而不值得关注  
- 对用户的记录进行评判或宣扬感恩的好处
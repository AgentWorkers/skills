---
name: Prayers
description: 构建一个适用于任何信仰传统的个人祈祷系统，该系统具备日程安排、记录功能以及灵性追踪功能。
metadata: {"clawdbot":{"emoji":"🙏","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 无偏见地支持任何宗教传统  
- 提供祈祷时间安排与提醒服务  
- 记录用户的祈祷内容及灵性反思  
- 自动创建名为 `~/prayers/` 的工作文件夹  
- 保持高度尊重，绝不强行规定用户的祈祷方式  

## 文件结构  
```
~/prayers/
├── practice.md       # User's tradition and preferences
├── schedule.md       # Prayer times and routines
├── log/
│   └── 2024/
├── prayers/          # Saved prayers and texts
├── intentions.md     # Prayer intentions
└── reflections.md
```  

## 初始设置  
- 轻柔地询问：  
  - “您信仰哪种宗教传统（如果有的话）？”  
  - “您有固定的祈祷时间吗？还是比较灵活？”  
  - “您需要祈祷提醒吗？”  
  - “您希望如何使用这个工具？”  

## 使用配置  
```markdown
# practice.md
## Tradition
[User's faith: Catholic, Muslim, Jewish, Buddhist, Hindu, Orthodox, Protestant, Non-denominational, Spiritual, Other]

## Prayer Times
- Fixed times: [e.g., Fajr, Lauds, Shacharit]
- Flexible: when moved to pray
- Daily routine: morning, evening

## Reminders
- Notify at prayer times: yes/no
- Gentle or silent: [preference]
```  

## 祈祷时间示例  
```markdown
# schedule.md
## Islamic
- Fajr: dawn
- Dhuhr: midday
- Asr: afternoon
- Maghrib: sunset
- Isha: night

## Christian Liturgy of Hours
- Lauds: morning
- Vespers: evening
- Compline: night

## Jewish
- Shacharit: morning
- Mincha: afternoon
- Maariv: evening

## Custom
- Morning: 7am
- Evening: 9pm
```  

## 祈祷记录  
```markdown
# log/2024/02/11.md
## Morning — 7:00 AM
Prayer: Morning offering
Duration: 10 min
Intentions: Family, gratitude
Notes: Felt peaceful

## Evening — 9:00 PM
Prayer: Rosary / Evening reflection
Duration: 15 min
State: Distracted but persevered
```  

## 祈祷意向追踪  
```markdown
# intentions.md
## Ongoing
- Family health
- Guidance on decision
- Gratitude practice

## Specific
- Mom's surgery (Feb 15)
- Friend going through difficulty

## Answered/Resolved
- Job situation — resolved Jan 2024
```  

## 祈祷建议  
当用户询问“我应该祈祷什么”或“帮我祈祷”时：  
- 如果用户的情况不明确（如感到焦虑、感激、悲伤或需要指引），先询问具体情境  
- 提供该宗教传统中的具体祈祷文（包括实际文字内容，而不仅仅是名称）  
- 根据用户的理解能力选择合适的祈祷形式（完整版本或简短版本）  
- 若用户需要学习，可逐步指导他们如何进行祈祷  

## 保存的祈祷记录  
```markdown
# prayers/favorites.md
[Prayers that resonate with user]
```  

## 灵性反思  
```markdown
# reflections.md
## Feb 11, 2024
Struggled to focus today but showed up.
Grateful for the discipline even when feelings aren't there.
```  

## 显示的信息  
- “15分钟后是 Maghrib 祈祷时间”  
- “您已经连续7天进行祈祷了”  
- “上个月的祈祷意向是否仍然有效？”  
- “今天是您宗教传统中的[神圣节日]”  

## 主动提供的支持  
- 提供祈祷时间提醒（如用户需要）  
- 通知用户宗教传统中的重要节日及习俗  
- 提醒用户的斋戒时间  
- “您通常在这个时间进行祈祷”  

## 需要追踪的信息  
- 祈祷是否完成（简单确认）  
- 祈祷时长（可选）  
- 用户的祈祷意向  
- 祈祷时的状态或感受（可选，个人隐私）  
- 灵性反思内容（可选）  

## 不应做的行为  
- 无端假设用户的宗教传统  
- 评判用户的祈祷频率或质量  
- 强制推荐特定的祈祷方式或实践  
- 不要强行灌输宗教观念  
- 不要将任何宗教传统视为默认选项
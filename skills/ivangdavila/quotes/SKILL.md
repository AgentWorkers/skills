---
name: Quotes
description: 构建一个个人名言系统，用于保存名言、发现其中有意义的词汇，并自动提取这些词汇。
metadata: {"clawdbot":{"emoji":"💬","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 用户分享引文时，会将其连同上下文和标签一起保存。  
- 当用户需要灵感时，系统会推荐相关的引文。  
- 系统会根据预设的时间表或条件自动发送引文。  
- 系统会创建一个名为 `~/quotes/` 的工作文件夹来存储所有引文。  

## 文件结构  
```
~/quotes/
├── collection/
│   ├── by-author/
│   ├── by-topic/
│   └── by-source/
├── favorites.md
├── delivery.md
└── discover.md
```  

## 引文录入  
```markdown
# collection/by-author/marcus-aurelius.md
## On Control
"You have power over your mind — not outside events. Realize this, and you will find strength."
- Source: Meditations, Book 6
- Added: Feb 2024
- Tags: stoicism, control, mindset

## On Time
"It is not that we have a short time to live, but that we waste a lot of it."
- Source: Meditations
- Tags: time, mortality, urgency
```  

## 按主题分类  
```markdown
# collection/by-topic/creativity.md
"Creativity is just connecting things."
— Steve Jobs

"The chief enemy of creativity is good sense."
— Pablo Picasso

"You can't use up creativity. The more you use, the more you have."
— Maya Angelou
```  

## 按来源分类  
```markdown
# collection/by-source/books.md
## Meditations — Marcus Aurelius
[quotes...]

## Man's Search for Meaning — Viktor Frankl
"Those who have a 'why' to live, can bear with almost any 'how'."

# collection/by-source/conversations.md
## Dad
"The best time to plant a tree was 20 years ago. The second best time is now."
- Said when I was hesitating on career change
```  

## 收藏夹  
```markdown
# favorites.md
Top quotes that resonate most:

"We suffer more in imagination than in reality."
— Seneca

"The obstacle is the way."
— Marcus Aurelius

"What would you do if you weren't afraid?"
— Sheryl Sandberg
```  

## 自动推送  
```markdown
# delivery.md
## Daily Morning
- Time: 7:00 AM
- Type: Random from favorites
- Channel: notification

## Weekly Reflection
- Day: Sunday 8:00 PM
- Type: Stoicism topic
- Include: reflection prompt

## Context-Based
- Feeling stressed → stoicism, calm
- Need motivation → action, discipline
- Creative block → creativity, artists

## By Mood Tags
- stressed: calm, perspective, stoicism
- unmotivated: action, discipline, purpose
- sad: hope, resilience, meaning
- celebrating: gratitude, joy
```  

## 引文推荐机制  
- “晨间引文：[随机推荐的收藏夹中的引文]”  
- “您保存了5条来自《Meditations》的引文”  
- “根据您当前的情况，推荐相关的引文”  
- “您正在阅读的书籍中有新的引文吗？”  

## 快速采集引文信息  
当用户分享引文时：  
- 保存引文的完整文本  
- 询问/推断引文的作者  
- 询问/推断引文的来源  
- 建议合适的主题标签  
- （可选）记录该引文为何引起用户的共鸣  

## 需要跟踪的信息  
- 引文文本（完整内容）  
- 作者  
- 来源（书籍、演讲、对话等）  
- 主题标签  
- 添加引文的时间  
- 引文的重要性（可选）  

## 功能逐步完善计划  
- 初始阶段：添加10条收藏夹中的引文  
- 按主题和作者对引文进行分类  
- 设置每日自动推送功能  
- 持续从书籍和播客中收集引文  

## 需要避免的行为  
- 错误地标注引文的来源（尽可能核实信息）  
- 仅保存引文而忽略其上下文（这会导致引文失去意义）  
- 忘记个人分享的引文（如家人或导师的引文）  
- 只收集引文而不进行后续回顾  

---

（注：由于提供的 `SKILL.md` 文件内容较为简短，部分部分（如文件结构、引文录入、自动推送等）的详细说明可能需要在完整的软件文档中提供。上述翻译基于文件中的关键信息进行了整理。）
---
name: Affirmations
description: 构建一个个人肯定系统，用于日常练习、定制肯定语以及心态强化。
metadata: {"clawdbot":{"emoji":"✨","os":["linux","darwin","win32"]}}
---

## 核心功能  
- 根据用户的需求提供积极的肯定语（affirmations）  
- 帮助用户创建个性化的肯定语  
- 跟踪用户的练习情况以及哪些肯定语能够产生共鸣  
- 创建一个名为 `~/affirmations/` 的工作文件夹用于存储用户创建的肯定语  

## 文件结构  
```
~/affirmations/
├── my-affirmations.md    # Personal, custom
├── favorites.md          # Ones that resonate
├── practice.md           # Preferences
└── log/
```  

## 设置步骤  
1. 询问用户：  
   - “您希望在哪些方面进行提升？”（自信、焦虑、自我价值、财富、健康、人际关系等）  
   - “您希望什么时候收到肯定语？”（早晨、晚上、随时需要）  
   - “是由我发送还是由您自己选择？”  

## 练习偏好设置  
```markdown
# practice.md
## Focus Areas
- Self-worth
- Anxiety/calm
- Career confidence

## Delivery
- Morning: 7am, 3 affirmations
- Style: gentle / bold / spiritual

## Rotation
- Mix of favorites + new
```  

## 个人肯定语  
帮助用户自己创建肯定语：  
```markdown
# my-affirmations.md
## Self-Worth
- I am enough exactly as I am
- I deserve good things

## Career
- I bring unique value to my work
- I handle challenges with confidence

## Calm
- I release what I cannot control
- I am safe in this moment
```  

## 创建自定义肯定语  
当用户需要个性化肯定语时：  
- 询问用户目前遇到的困难  
- 将负面的想法转化为积极的、现在时态的表述（例如：“我……”或“我选择……”或“我相信……”）  
- 测试这些肯定语：用户是否感到自然、舒适，或者是否感觉生硬/不自然？  

## 传递方式  
根据用户的偏好选择不同的表达风格：  
- **温和风格**： “你值得被爱和被接纳。”  
- **坚定风格**： “我势不可挡，我能创造自己的现实。”  
- **灵性风格**： “宇宙会支持我实现最美好的目标。”  
- **实用风格**： “我具备应对今天挑战的能力。”  

## 每日练习  
早晨时发送肯定语：  
```
Good morning. Your affirmations today:

• I am capable of achieving my goals
• I choose peace over worry
• I am worthy of success and happiness

Have a powerful day.
```  

## 需要跟踪的内容  
```markdown
# log/2024-02.md
## Practice
- Days practiced: 18/28
- Streak: 5 days

## Resonated
- "I release what I cannot control" — saved to favorites

## Didn't Land
- Abundance affirmations feel forced right now
```  

## 用户收藏的肯定语  
```markdown
# favorites.md
Affirmations that deeply resonate:

- I am enough exactly as I am
- I trust the timing of my life
- I choose progress over perfection
```  

## 需要显示的信息：  
- 早晨发送的肯定语（如果用户设置了自动发送）  
- “上周特别有效的肯定语”  
- “您已经连续练习了10天”  
- “是否需要添加新的关注领域？”  

## 情境特定的肯定语  
当用户分享自己的困扰时：  
- 对于焦虑情绪：提供安抚和稳定的肯定语  
- 对于自我怀疑：提供关于自我价值和能力的肯定语  
- 活动前：提供增强自信和准备状态的肯定语  
- 失败后：提供关于恢复力和自我关怀的肯定语  

## 注意事项：  
- 避免说教或使用过于刻意、不自然的积极语言  
- 如果用户对某些肯定语没有共鸣，不要强迫他们使用  
- 如果用户的风格不适合灵性语言，不要强行使用  
- 不要让使用肯定语成为一种负担（比如像做作业一样）
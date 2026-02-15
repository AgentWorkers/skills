---
name: brand-voice
description: 管理所有写作内容中的品牌风格/语调
author: 무펭이 🐧
---

# 品牌语言风格管理

通过管理写作风格配置文件，确保每个品牌在所有内容中保持一致的语气和风格。您可以通过所有内容创作技能中的 `--voice` 选项来选择所需的语言风格。

## 品牌配置文件

### 🐧 무펭이（默认）
- **语气**：友好且随意
- **风格**：非正式，使用表情符号
- **格式**：仅包含核心要点，穿插幽默元素
- **示例**：
  - ❌ “大家好！今天我将介绍 MUFI Photobooth 的新功能。”
  - ✅ “MUFI Photobooth 新功能发布了！这太棒了！” 🐧

### 🎯 MUFI 官方
- **语气**：专业且礼貌
- **风格**：使用正式语言
- **格式**：简洁明了，适用于 B2B/官方渠道
- **示例**：
  - ✅ “MUFI Photobooth 是大学活动的理想选择。简单的设置和直观的用户界面让任何人都能轻松使用。”

### 👤 Hyungnim 个人风格
- **语气**：随意但富有洞察力
- **风格**：结合随意与正式元素，以分享个人见解为主
- **格式**：以思维流程为主，分享值得借鉴的观点
- **示例**：
  - ✅ “在活动中负责搭建展位后，我意识到人们最终追求的是‘乐趣’。无论技术有多好，如果用户体验复杂，他们就不会使用它。”

## 配置文件存放位置

**位置**：`workspace/brand/profiles/`

```
brand/
  profiles/
    mupengyi.md         # 무펭이 profile
    mufi-official.md    # MUFI official profile
    hyungnim.md         # Hyungnim personal profile
```

### 配置文件结构

```markdown
# 무펭이 🐧

## Tone
Friendly and casual

## Style
- Use informal language
- Actively use emojis 🐧🎉✨
- Abbreviations OK

## Format
- Core points only
- Remove unnecessary modifiers
- Mix in humor

## Forbidden Expressions
- Formal expressions like "we will provide", "we shall"
- Verbose greetings
- Excessive formality

## Preferred Expressions
- "This is real", "insane", "jackpot"
- "Yo", "you", "your"
- Lots of exclamation marks OK!!!

## Examples
- ❌ "Hello, today..."
- ✅ "Yo check this out 🐧"
```

## 写作技能集成

以下技能支持 `--voice` 选项：
- **copywriting**：撰写标题/文案
- **cardnews**：卡片新闻文本
- **social-publisher**：社交媒体帖子
- **mail**：电子邮件撰写
- **content-recycler**：内容复用

### 使用示例

```
"Write Insta caption --voice mufi-official"
→ Write in MUFI official tone

"Create card news --voice mupengyi"
→ Create in 무펭이 style

"Write Threads post in Hyungnim tone"
→ Use Hyungnim personal profile
```

## 配置文件切换指南

### 平台推荐
- **Instagram MUFI 官方账号** → 使用 `mufi-official`
- **Instagram 个人账号** → 使用 `hyungnim`
- **Threads** → 使用 `mupengyi`（随意风格）
- **Discord/私信** → 使用 `mupengyi`
- **官方电子邮件** → 使用 `mufi-official`
- **博客文章** → 使用 `hyungnim`（注重分享见解）

### 情境推荐
- **产品介绍** → 使用 `mufi-official`
- **日常分享** → 使用 `mupengyi` 或 `hyungnim`
- **客户服务** → 使用 `mufi-official`
- **社区互动** → 使用 `mupengyi`

## 语气一致性检查

写作完成后会自动进行验证：
- ✅ 是否使用了推荐的表达方式？
- ❌ 是否包含了禁止使用的表达？
- 🎯 语气是否符合目标受众？

**预处理集成**：
```
Before writing skill execution → brand-voice-check
→ Warn if doesn't match selected profile
```

## 添加/编辑配置文件

如何添加新的品牌配置文件：

```
"Create new brand profile: MUFI recruiting"
→ Create brand/profiles/mufi-recruit.md

- Tone: Friendly but professional
- Style: Formal language
- Format: Emphasize company culture
```

## 关键搜索词
- “品牌语气”
- “品牌语言风格”
- “写作风格”
- “配置文件切换”
- “语气与表达方式”

## 集成机制
- **预处理**：写作前确认所选配置文件
- **后处理**：写作后检查语气一致性
- **学习机制**：通过良好的用户互动学习语气回归模式

## 事件日志集成

记录写作时使用的语言风格配置文件：
**位置**：`events/voice-used-YYYY-MM-DD.json`

```json
{
  "timestamp": "2026-02-14T14:30:00Z",
  "skill": "copywriting",
  "voice": "mupengyi",
  "platform": "instagram",
  "result": "Caption writing complete"
}
```

## 经验总结
- 使用 **무펭이** 的语气在 Instagram 上提升了 40% 的互动率（数据来自 Performance Tracker）
- **MUFI 官方语气** 提高了 B2B 电子邮件的回复率
- **Hyungnim 的语气** 增加了博客文章的阅读时长

---

> 🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统技能
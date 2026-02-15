---
name: islamic-daily-reflection
version: 1.0.0
description: 每日伊斯兰灵修指南（使用Python脚本编写）：提供格式化的灵性指导，并结合日历信息（如斋月、聚礼日、古尔邦节等）。内容包含《古兰经》和圣训的权威引用，以及每日可实践的修行建议。
author: clinicode
---

# 伊斯兰每日反思

## 重要提示：务必运行脚本

当用户请求每日反思内容时，你必须执行以下 Python 脚本：
```bash
python scripts/reflection.py
```

**请严格按照脚本返回的格式显示全部输出内容。**

该脚本提供以下功能：
- ✅ 带有 ═══ 边界的格式化输出
- ✅ 希吉里历（Hijri calendar）相关信息
- ✅ 斋月（Ramadan）、聚礼（Jummah）及平日的反思内容
- ✅ 可操作的每日挑战
- ✅ 可参考的《古兰经》（Quran）和圣训（Hadith）内容

**切勿自行生成反思内容，务必运行脚本。**

## 用户指令

用户可能会输入以下指令：
- "daily reflection"（每日反思）
- "islamic reminder"（伊斯兰提醒）
- "inspire me"（激励我）
- "motivate me islamically"（以伊斯兰方式激励我）
- "friday reflection"（周五反思）
- "ramadan reflection"（斋月反思）

对于所有这些请求，均需执行 `python scripts/reflection.py` 脚本。

## 脚本输出格式

脚本返回的文本格式如下：
```
═══════════════════════════════════════
📅 Thursday, 13 February 2026 | 25 Sha'ban 1447

🤲 Patience in Small Trials

[Reflection content...]

💡 Today's Action (X min):
[Actionable challenge...]

📖 [Quran/Hadith reference]
═══════════════════════════════════════
```

请严格按照接收到的格式显示输出内容，包括所有格式、表情符号（emojis）和边界（borders）。

## 技术细节

该脚本（`scripts/reflection.py`）具备以下特性：
- 自动检测当前日期（公历和希吉里历）
- 根据日期选择合适的反思主题：
  - 斋月（Ramadan）第 1-30 天的特定反思内容
  - 聚礼（Jummah，即周五）的反思内容
  - 平日的反思内容（30 个循环主题）
- 采用统一的格式进行输出
- 无需依赖任何外部库，仅使用 Python 标准库

## 反思主题

**平日反思主题循环如下：**
- 耐心（Patience）
- 感恩（Gratitude）
- 信任真主（Tawakkul）
- 敬畏真主（Taqwa）
- 诚心（Ikhlas）
- 谦逊（Humility）
- 满足现状（Contentment）
- 希望（Hope）
- 对真主的敬畏（Khashyah）
- 对真主的爱（Love for Allah）
- 兄弟情谊（Brotherhood）
- 诚实（Honesty）
- 公正（Justice）
- 仁慈（Mercy）
- 宽恕（Forgiveness）
- 慈善（Charity）
- 善良品质（Good Character）
- 记念真主（Dhikr）
- 关爱父母（Kindness to Parents）
- 关爱邻居（Neighbors）
- 避免诽谤（Avoiding Backbiting）
- 控制愤怒（Controlling Anger）
- 在逆境中保持感恩（Thankful in Trials）
- 祈祷（Dua）
- 诵读《古兰经》（Quran Reading）
- 守夜（Tahajjud）
- 斋戒（Fasting）
- 记住死亡（Remembering Death）

**特殊场合：**
- 斋月（Ramadan，第 9 个月）：特定日期的反思内容
- 排尔希贾月（Dhul Hijjah，第 12 个月，第 1-10 天）：朝觐相关主题的反思内容
- 聚礼（Jummah，周五）：周五专属的反思内容
-穆哈兰姆月（Muharram，第 10 天）：阿舒拉节（Ashura）相关的反思内容

## 版本信息

1.0.0 — 一个包含预设反思内容的 Python 脚本
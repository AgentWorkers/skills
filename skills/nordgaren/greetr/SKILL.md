---
name: greet
description: |
  Greets the user with a friendly, personalized welcome message.
  USE WHEN user says "hello", "hi", "hey", "greet me", "good morning",
  "good afternoon", "good evening", or any greeting phrase.
---

# 问候功能

## 何时激活此功能
- 用户发送问候语（如 “hello”、“hi”、“hey”、“what’s up” 等）
- 用户请求系统“向我问候”
- 用户说 “good morning”、“good afternoon” 或 “good evening”
- 系统在会话开始时需要自动发送问候语

## 问候行为
当触发此功能时，系统应回复以下内容：
1. **根据当前时间表示问候** – 使用系统时间来恰当地说出 “Good morning”、“Good afternoon” 或 “Good evening”。
2. **简洁自然** – 保持问候语简短且符合对话风格。
3. **提供帮助** – 以一句简短的表示愿意提供帮助的话语作为结尾。

## 不同时间段的问候语
| 系统时间       | 问候语            |
|--------------|-----------------|
| 上午 5:00 - 11:59   | Good morning       |
| 下午 12:00 - 4:59   | Good afternoon     |
| 下午 5:00 - 8:59   | Good evening       |
| 晚上 9:00 - 第二天上午 4:59 | Hey, night owl!     |

## 示例回复
> 早上好！希望你的一天有一个美好的开始。需要我帮忙吗？
> 晚上好！今晚我们打算做什么？
> 嘿，夜猫子！还在加班吗？需要我帮忙吗？
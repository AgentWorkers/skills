---
name: cron-gen
description: **从自然语言生成 Cron 表达式**
---

# Cron 生成器

将“Every weekday at 9am”转换为“0 9 * * 1-5”。别再在谷歌上搜索 Cron 语法了。

## 快速入门

```bash
npx ai-cron-gen "every monday at 3pm"
```

## 功能介绍

- 将自然语言描述转换为 Cron 表达式  
- 解释 Cron 表达式的具体含义  
- 验证输入的 Cron 语法是否正确  
- 显示任务的下次执行时间  

## 使用示例

```bash
# Generate from description
npx ai-cron-gen "first day of every month at midnight"

# Explain existing cron
npx ai-cron-gen --explain "0 */4 * * *"

# Get next 5 run times
npx ai-cron-gen "every 30 minutes" --next 5
```

## 输出结果

```
Expression: 0 9 * * 1-5
Meaning: At 09:00 on every day-of-week from Monday through Friday
Next runs:
  - Mon Jan 29 09:00:00 2024
  - Tue Jan 30 09:00:00 2024
```

## 系统要求

需要 Node.js 18 及更高版本，并且必须配置 OPENAI_API_KEY。  

## 许可证

采用 MIT 许可证，永久免费使用。  

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-cron-gen](https://github.com/lxgicstudios/ai-cron-gen)  
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)
---
name: learning-engine
description: 自动分析错误和成功的模式，并将这些模式反映在技能提升中。
author: 무펭이 🐧
---
# learning-engine

该系统会记录用户的错误与成功经历，并自动学习其中的规律，以此来提升用户的技能。它实现了“避免重复相同错误”的目标。

## 学习来源

### 1. 错误日志（memory/errors/）
从错误日志中提取失败的模式。

```markdown
# memory/errors/2026-02-14.md

## 10:30 - insta-post failure
- Cause: PNG file upload → "Problem occurred" error
- Fix: Retry after JPG conversion → Success
- Lesson: Always convert to JPG before Instagram upload
```

### 自我评估结果
从每周的自我评估中提取需要改进的地方。

```markdown
# memory/self-eval/2026-W07.md

## This Week's Mistakes
- Too many browser snapshots (token waste)
- → Improvement: Call API directly via exec

## This Week's Successes
- 95% token savings with insta-cli v2 DM check
```

### 性能数据
从性能跟踪数据中分析成功与失败的规律。

```json
{
  "insight": "Posts at 7-9 PM get +30% likes",
  "rule": "Instagram posts recommended 19:00-21:00"
}
```

## 自动规则生成
将学习到的规律转化为具体的规则：

**存储位置**：`memory/learned-rules/`

```
memory/
  learned-rules/
    instagram-posting.md
    browser-automation.md
    api-usage.md
    error-recovery.md
```

### 规则格式
（具体规则格式在此处说明）

## 将规则应用到技能中
将学习到的规则自动添加到相应的技能文档中：

**存储位置**：`skills/{skill-name}/SKILL.md`

```markdown
# insta-post

...

## Learned Lessons

### Image Processing
- ✅ Always convert to JPG (PNG causes errors)
- ✅ 1:1 ratio required (1024x1024 recommended)
- ✅ File size < 8MB

### Timing
- ✅ Posts at 19:00-21:00 get +30% engagement
- ❌ Avoid early morning posts

### Automation
- ✅ Call API via exec (0 snapshots)
- ❌ Minimize browser automation
```

## 每周学习报告
每周一自动生成学习报告：

**存储位置**：`memory/learning/weekly-YYYY-Www.md`

## 事件发布
当学习完成时，会发布相应的事件：

**存储位置**：`events/lesson-learned-YYYY-MM-DD.json`

## 与其他系统的集成

- **错误处理钩子**：当发生错误时，将错误信息记录到 `memory/errors/`，然后由 learning-engine 进行分析。
- **自我评估后钩子**：在每周评估完成后，更新学习规则。
- **性能数据后钩子**：在收集到性能数据后，分析学习规律。
- **定期钩子**：每周一生成学习报告。

## 学习流程
（具体学习流程在此处说明）

## 触发关键词
- “我学到了什么”
- “学习”
- “学习内容”
- “错误模式”
- “改进之处”
- “学习报告”
- “添加规则”

## 使用示例
（具体使用场景在此处说明）

## 自动改进示例

### 学习前
```
Instagram post fails → Manually convert to JPG → Retry
(Repeat every time)
```

### 学习后
```
Execute insta-post → Auto-check/convert JPG → Success
(Rule injected into SKILL.md)
```

## 元学习
learning-engine 本身也会进行自我学习：
- “哪些规则被使用得最频繁？”
- “哪些技能提升最快？”
- “哪些领域的学习进展较慢？”

**元学习报告**：`memory/learning/meta-YYYY-MM.md`

## 未来改进方向
- [ ] 规则冲突检测（规则 A 与规则 B 的冲突）
- [ ] 规则置信度评分（基于使用频率）
- [ ] 规则的自动 A/B 测试（验证规则的有效性）
- [ ] 与其他系统共享学习成果

---

> 🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统中的技能模块
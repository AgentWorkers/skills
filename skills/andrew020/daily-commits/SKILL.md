---
name: daily-commits
description: Summarize a person's git commits for a specific date, grouped by feature points, in English. Use when reviewing daily work output.
argument-hint: [date:YYYY.MM.DD] [author-name]
allowed-tools: Bash, Read
---

# 每日提交摘要

汇总在 **$0** 时间段内由 **$1** 执行的所有 Git 提交，按功能/模块进行分组，并以英文形式呈现。

## 步骤

1. 运行 `git log`，并根据日期和作者进行过滤：

```
git log --after="<start-of-day>" --before="<end-of-day>" --author="$1" --pretty=format:"%h %s" --no-merges
```

将日期 `$0`（格式：`YYYY.MM.DD`）转换为正确的 Git 日期范围：
- `--after` = 当天 00:00:00
- `--before` = 第二天 00:00:00

2. 同时运行 `git log` 并添加 `--stat` 选项，以了解更改的范围：

```
git log --after="<start-of-day>" --before="<end-of-day>" --author="$1" --stat --no-merges
```

3. 分析所有提交，并根据以下标准将它们按功能/模块进行分组：
   - 提交信息的前缀（feat、fix、refactor、docs、style、test、chore 等）
   - 相关的文件路径和模块
   - 相关更改的逻辑分组

4. 以以下格式输出清晰的摘要：

```
## Daily Commits Summary: <author> — <date>

### <Feature Area 1>
- <concise description of what was done> (`commit-hash`)
- ...

### <Feature Area 2>
- <concise description of what was done> (`commit-hash`)
- ...

**Total: X commits**
```

## 规则

- 仅使用英文进行输出
- 按功能进行分组，而不是按提交类型的前缀进行分组
- 每个条目都应是一个简洁、易于阅读的描述（而不仅仅是原始的提交信息）
- 如果提交信息已经包含常规前缀（如 `feat(meeting)`），则使用该前缀作为分组的依据
- 忽略合并提交
- 如果没有找到任何提交，请明确说明这一点
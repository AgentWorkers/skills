---
name: content-pipeline
description: 协调完整的内容工作流程（规划→撰写→设计→发布→跟踪）。适用于自动化从规划到发布的整个内容工作流程的场景。
author: 무펭이 🐧
---
# content-pipeline

这是一个用于协调整个内容制作流程的元技能（meta skill）。

## 流程阶段

```
1. seo-content-planner → Keyword analysis & content planning
2. copywriting → Write body text
3. cardnews → Generate card news images
4. social-publisher → Publish to Instagram/SNS
5. Performance tracking → Feedback via daily report
```

## 使用方法

### 全自动执行
```bash
content-pipeline --auto --topic "Photobooth usage tips"
```

### 单个阶段执行
```bash
# Stage 1: Planning
content-pipeline --step plan --topic "Photobooth trends"

# Stage 2: Write body (auto-loads previous stage event)
content-pipeline --step write

# Stage 3: Generate card news
content-pipeline --step design

# Stage 4: Publish
content-pipeline --step publish

# Stage 5: Check performance
content-pipeline --step track
```

## 事件集成（Event Integration）

每个阶段会自动从 `events/` 目录中读取前一个阶段的结果：
- `seo-plan-YYYY-MM-DD.json` → 用于获取写作输入
- `content-draft-YYYY-MM-DD.json` → 用于获取卡片新闻（cardnews）的输入
- `content-published-YYYY-MM-DD.json` → 用于获取每日报告（daily-report）的输入

## 参数选项

- `--auto` — 自动执行所有阶段
- `--step <plan|write|design|publish|track>` — 仅执行特定阶段
- `--topic <topic>` — 指定内容主题
- `--skip-review` — 跳过每个阶段的审核（风险较高）

## 执行流程

### 自动模式 (`--auto`)
1. 执行 `seo-content-planner` → 生成 `events/seo-plan-YYYY-MM-DD.json`
2. 使用生成的关键词/主题执行写作任务 → 生成 `events/content-draft-YYYY-MM-DD.json`
3. 根据草稿生成卡片新闻 → 生成 `events/cardnews-ready-YYYY-MM-DD.json`
4. 使用图片和标题执行社交媒体发布任务 → 生成 `events/content-published-YYYY-MM-DD.json`
5. 自动将发布结果包含在每日报告中

### 分阶段执行模式 (`--step`)
每个阶段都需要请求审核：
- 审核计划 → 批准 → 进入下一阶段
- 审核草稿 → 批准 → 进入下一阶段
- 预览卡片新闻 → 批准 → 发布

## 示例

### 生成婚礼摄影亭相关内容
```bash
content-pipeline --auto --topic "Preserving wedding memories with photobooths"
```

**结果：**
- SEO 关键词：wedding photobooth, wedding photo booth 等
- 博文草稿（1200个字符）
- 卡片新闻（5张幻灯片，尺寸为1024x1024像素）
- 自动发布到 Instagram（标记合作账号）
- 将发布结果包含在每日报告中

### 分阶段手动审核
```bash
# 1. Review plan first
content-pipeline --step plan --topic "University festival photobooths"
# → Generate events/seo-plan-2026-02-14.json

# 2. Write draft after reviewing plan
content-pipeline --step write
# → Generate events/content-draft-2026-02-14.json

# 3. Design after reviewing draft
content-pipeline --step design
# → Generate 5 card news slides

# 4. Publish after final review
content-pipeline --step publish
```

## 注意事项

- `--auto` 模式会自动执行所有阶段，因此在最终发布前请务必审核内容
- 图片必须为 JPG 格式（PNG 格式可能导致 Instagram 出现问题）
- 发布后，`events/content-published-YYYY-MM-DD.json` 会自动被纳入每日报告中

## 实施指南

由于这是一个元技能，在实际实施过程中请按照以下步骤操作：
1. 检查 `events/seo-plan-*.json` 文件是否存在；如果不存在，则执行 `seo-content-planner`
2. 将结果作为输入传递给下一个技能
3. 在每个阶段生成相应的事件文件（event file）

---

**作者**: 무펭이 🐧  
**创建时间**: 2026-02-14  
**状态**: 已准备好投入使用（Production Ready）
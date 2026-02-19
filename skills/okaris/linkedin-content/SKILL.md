---
name: linkedin-content
description: "使用钩子公式（hook formulas）、格式化规则以及互动策略来撰写 LinkedIn 帖子。内容涵盖帖子类型、算法推荐机制、字符限制以及内容构建的核心要素。适用于：LinkedIn 帖子、专业内容创作、思想领导力展示（thought leadership）、B2B 营销内容、个人品牌建设。相关关键词：LinkedIn 帖子、LinkedIn 内容、LinkedIn 写作技巧、LinkedIn 策略、LinkedIn 互动策略、LinkedIn 算法机制、LinkedIn 格式化、思想领导力、专业内容、B2B 营销、LinkedIn 用户增长。"
allowed-tools: Bash(infsh *)
---
# LinkedIn 内容策略

通过 [inference.sh](https://inference.sh) 命令行工具来撰写能够吸引用户互动的 LinkedIn 发文。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Research trending LinkedIn content patterns
infsh app run tavily/search-assistant --input '{
  "query": "LinkedIn viral post examples 2024 high engagement patterns"
}'

# Post to X (cross-posting reference)
infsh app run x/post-create --input '{
  "text": "Your cross-posted version here"
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 来完成安装。

## 发文结构

```
┌─────────────────────────────────────┐
│ HOOK (first 1-2 lines)             │ ← Visible before "...see more"
│                                     │
│ ...see more ─────────────────────── │ ← The click gate
│                                     │
│ BODY (story/value)                  │
│ - Formatted with line breaks        │
│ - Short paragraphs (1-2 sentences)  │
│ - Lists or numbered points          │
│                                     │
│ CTA (last 1-2 lines)              │ ← Ask for engagement
│                                     │
│ #hashtags (3-5)                     │
└─────────────────────────────────────┘
```

## 字符限制

| 元素 | 限制 |
|---------|-------|
| 发文正文 | 3,000 个字符 |
| “查看更多”前的可见内容 | 约 210 个字符（手机上显示约 2 行） |
| 标签 | 建议使用 3-5 个 |
| 评论 | 1,250 个字符 |
| 文章标题 | 100 个字符 |
| 文章正文 | 125,000 个字符 |

**最关键的是前 210 个字符。** 如果钩子（即吸引用户点击 “查看更多”的内容）不够吸引人，就没有人会点击 “查看更多” 了。

## 发文技巧公式

### 成功的技巧

| 公式 | 例子 |
|---------|---------|
| **提出相反观点** | “ unpopular opinion: 代码审查是浪费时间。” |
| **以个人故事开头** | “我在一个周二被解雇了。但这却是我做过的最棒的事。” |
| **提供令人惊讶的数据** | “92% 的初创企业会失败。但原因并非你想象的那样。” |
| **列出要点** | “我雇佣了 200 多名工程师。以下是我会关注的 5 个危险信号。” |
| **使用强调句** | “你的简历并不重要。真正重要的是……” |
| **对比前后情况** | “3 年前我连一次面试机会都没有。昨天我拒绝了一家 FAANG 公司的offer。” |
| **突然中断模式** | “在发送那封冷冰冰的邮件之前，请先读一下这个。”

### 失败的技巧

```
❌ "Excited to announce that we are pleased to share..." (corporate speak)
❌ "In today's rapidly evolving landscape..." (cliché, says nothing)
❌ "I'd like to take a moment to..." (slow, no hook)
❌ "Just published a new blog post!" (no value proposition)
❌ Starting with a hashtag or emoji
```

## 格式规则

### 换行是你的最佳帮手

```
❌ Dense paragraph:
"I learned something important about leadership last week. My team was struggling with a deadline and instead of pushing harder, I decided to remove scope. The result was incredible — we shipped faster and the quality was better. Sometimes less really is more."

✅ Formatted for LinkedIn:
"I learned something about leadership last week.

My team was struggling with a deadline.

Instead of pushing harder, I removed scope.

The result?

We shipped faster.
And the quality was BETTER.

Sometimes less really is more."
```

### 格式指南

| 规则 | 原因 |
|------|-----|
| 每行写一个句子 | 在手机上更容易阅读 |
| 段落之间留空行 | 便于视觉上的停顿 |
| 段落简短（1-2 句） | 适合手机阅读 |
| 使用换行来制造戏剧性效果 | 有助于控制阅读节奏和营造悬念 |
* **仅在使用关键短语时使用粗体** | 使重要内容更显眼 |
| 用编号列表列出要点 | 更易于阅读和分享 |
* **避免长篇大论** | 人们通常不会阅读冗长的文本

## 发文类型（按互动率排序）

| 发文类型 | 互动率 | 适合的场景 |
|-----------|-----------|----------|
| **个人故事 + 经验教训** | 非常高 | 建立联系，展现真实性 |
| **提出相反观点** | 高 | 引发讨论，提高曝光率 |
| **轮播图（文档类型）** | 高 | 教育性内容，实用建议 |
| **列表/技巧（带编号）** | 高 | 实用性强，便于分享 |
| **投票** | 中等偏高 | 容易引发互动，便于收集数据 |
| **图片 + 故事** | 中等 | 使内容更人性化，适合分享事件相关内容 |
| **视频（原生格式）** | 中等 | 适合展示操作过程或个人特色 |
| **链接文章** | 低 | 算法会降低文章的传播范围 |
| **转发** | 非常低 | 最好原创内容

## 发文链接策略

LinkedIn 会对包含链接的文章进行惩罚（从而降低其传播范围）。应对方法：

1. **评论方式**：先发布文章，再将链接作为第一条评论添加；之后编辑文章说明 “链接在评论中”。
2. **不加链接的方式**：在文章正文中总结内容，并注明 “如需链接，请私信”。
3. **必须添加链接时**：将链接放在文章的最后，放在有吸引力的独立内容之后。

## 内容支柱

每个 LinkedIn 发文者都应该有 3-5 个固定的内容支柱，并轮流使用它们：

| 支柱 | 内容范围 | 例子 |
|--------|---------------|---------|
| **专业知识** | 行业知识，操作指南 | “每位工程师都应该了解的 5 种数据库模式” |
| **个人故事** | 个人经历、失败与成功 | “我收到过的最严厉的反馈” |
| **观点** | 对行业趋势的独到见解 | “AI 不会取代工程师，糟糕的管理者才会。” |
| **幕后花絮** | 公开分享工作流程 | “这是我们实际的冲刺回顾方式” |
| **精选见解** | 行业趋势、数据总结 | “我分析了 500 条招聘信息，发现了这些变化”

## 算法判断因素

| 判断因素 | 影响因素 | 对策 |
|--------|--------|-----|
| **停留时间** | 非常高 | 长篇内容更容易被完整阅读 |
| **评论数量** | 非常高 | 促进提问和讨论 |
| **被保存的次数** | 高 | 实用性强，值得参考的内容 |
| **“查看更多” 的点击率** | 高 | 强有力的钩子能吸引用户继续阅读 |
| **分享次数** | 中等 | 与读者产生共鸣的内容更容易分享 |
| **互动反应** | 中等 | 虽容易获得，但权重较低 |
| **外部链接** | 负面影响 | 会降低传播范围——建议将链接放在评论中 |
| **发布后的编辑** | 负面影响 | 发布后一小时内不要编辑文章 |
| **发布频率** | 每周 3-5 次 | 每天发布一次即可，每天多次发布反而可能适得其反 |

## 发文时间安排

| 时间 | 最佳发布时间（根据目标受众的时区） |
|-----|------|
| 星期二至周四 | 上午 7-8 点、中午 12 点、下午 5-6 点 |
| 星期一 | 上午 8 点（适合人们查看最新内容） |
| 星期五 | 上午 7-8 点（人们在下班前） |
| 周末 | 可选择不发布或发布简短内容 |

**发布后请参与评论 30-60 分钟** —— 这比文章本身更重要。

## 视觉内容

```bash
# Generate a visual for a LinkedIn post
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1080px;height:1080px;background:#0f172a;display:flex;align-items:center;justify-content:center;padding:80px;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:56px;font-weight:900;line-height:1.2;margin:0\">The best code is the code you don&apos;t write</h1><p style=\"font-size:22px;opacity:0.5;margin-top:24px\">— Every senior engineer</p></div></div>"
}'

# Generate a professional photo for a personal post
infsh app run falai/flux-dev-lora --input '{
  "prompt": "candid professional photo, person speaking at a conference podium, audience in background blurred, natural stage lighting, authentic moment, corporate event photography",
  "width": 1200,
  "height": 900
}'
```

## 提升互动性的结尾语

在每篇文章的结尾使用能激发互动性的语句：

| 结尾语类型 | 例子 |
|----------|---------|
| 提问 | “你收到过最糟糕的职业建议是什么？” |
| 表达同意或不同意 | “你同意吗？” |
| 鼓励分享 | “如果这篇文章触动你，请转发 ♻️” |
| 提醒保存 | “保存这篇文章，以备将来使用 🔖” |
| 征求建议 | “你会在这个列表中添加什么？” |
| 询问经历 | “这种情况你遇到过吗？” |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| **钩子不够吸引人** | 没有人点击 “查看更多” | 使用上述的写作技巧 |
| **长篇大论** | 在手机上难以阅读 | 每行写一个句子，段落之间留空行 |
| **在正文中间添加链接** | 算法会降低传播范围 | 将链接放在评论中 |
| **使用过多标签** | 看起来像垃圾信息 | 最多使用 3-5 个相关标签 |
* **使用公司术语** | 读者会直接跳过 | 用通俗的语言表达 |
* **过度自我推广** | 会降低读者互动 | 内容中80%应体现价值，20%用于自我推广 |
* **没有结尾语** | 没有引导互动的方向 | 每篇文章结尾都要提出问题或提出请求 |
* **转发时没有添加新内容** | 几乎不会被分享 | 建议原创内容 |
* **发布后立即消失** | 会削弱评论互动 | 发布后请保持互动 30-60 分钟 |
* **内容过于泛泛** | 通用性强的内容容易被忽略 | 使用具体故事和数据来增强吸引力 |

## 相关技能

```bash
npx skills add inference-sh/skills@social-media-carousel
npx skills add inference-sh/skills@content-repurposing
npx skills add inference-sh/skills@twitter-thread-creation
```

浏览所有可用工具：`infsh app list`
---
name: pitch-deck-visuals
description: |
  Investor pitch deck structure with slide-by-slide framework, visual design rules, and data presentation.
  Covers the 12-slide framework, chart types, team slides, and common investor turn-offs.
  Use for: fundraising decks, investor presentations, startup pitch, demo day, grant proposals.
  Triggers: pitch deck, investor deck, startup pitch, fundraising deck, demo day,
  pitch presentation, investor presentation, seed deck, series a deck, pitch slides,
  startup presentation, vc pitch, investor meeting
allowed-tools: Bash(infsh *)
---

# 投资者演示文稿（Pitch Deck）视觉设计

通过 [inference.sh](https://inference.sh) 命令行工具来创建适合投资者的演示文稿视觉素材。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a slide background
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1920px;height:1080px;background:linear-gradient(135deg,#0f0f23,#1a1a3e);display:flex;align-items:center;padding:100px;font-family:system-ui;color:white\"><div><p style=\"font-size:24px;color:#818cf8;text-transform:uppercase;letter-spacing:3px\">The Problem</p><h1 style=\"font-size:72px;margin:16px 0;font-weight:800;line-height:1.1\">Teams waste 12 hours/week on manual reporting</h1><p style=\"font-size:28px;opacity:0.7\">Source: Forrester Research, 2024</p></div></div>"
}'
```

## 12 张幻灯片的框架

| 序号 | 幻灯片 | 时长 | 内容 |
|---|-------|----------|---------|
| 1 | **标题** | 15秒 | 公司名称、标语、您的姓名 |
| 2 | **问题** | 45秒 | 与数据相关的问题点 |
| 3 | **解决方案** | 45秒 | 用一句话概括您的产品 |
| 4 | **产品演示** | 60秒 | 屏幕截图或实时演示 |
| 5 | **市场规模** | 30秒 | 总市场容量（TAM）→ 目标市场容量（SAM）→ 可服务市场容量（SOM） |
| 6 | **商业模式** | 30秒 | 您如何盈利 |
| 7 | **发展情况** | 45秒 | 增长指标、客户数量 |
| 8 | **竞争分析** | 30秒 | 产品定位（而非功能列表） |
| 9 | **团队** | 30秒 | 为什么您能胜出 |
| 10 | **财务数据** | 30秒 | 收入预测、单位经济模型 |
| 11 | **投资需求** | 15秒 | 需要投资多少、用于什么目的 |
| 12 | **联系方式** | 10秒 | 电子邮件地址、下一步行动 |

**总时长：约6分钟。** 幻灯片数量不得超过20张。

## 幻灯片设计规则

### 字体排版

| 元素 | 尺寸（1920x1080） | 规则 |
|---------|-----------------|------|
| 幻灯片标题 | 48-72px | 最多6个字 |
| 关键数据/数字 | 96-144px | 每张幻灯片最多一个 |
| 正文文本 | 24-32px | 每条要点最多6个字 |
| 说明/数据来源 | 16-20px | 必须注明数据来源 |
| 字体 | 仅使用无衬线字体（如 Inter, Helvetica, SF Pro 等） |

### “1-6-6”原则

- 每张幻灯片展示一个核心观点 |
- 每条要点最多6个字 |
- 每张幻灯片最多6个要点 |

如果需要更多内容，就需要增加幻灯片数量。

### 颜色搭配

| 元素 | 颜色指南 |
|---------|-----------|
| 背景 | 深色（如海军蓝、炭黑色）或纯白色 | 选择一种并保持一致 |
| 强调色 | 使用品牌统一颜色 |
| 正文文字 | 深色背景上使用白色，或浅色背景上使用深灰色（#333） |
| 图表 | 最多使用2-3种颜色，其中一种应为品牌颜色 |
| 避免使用：渐变色、霓虹色、超过3种颜色 |

### 布局规则

| 规则 | 原因 |
|------|-----|
| 保持一致的页边距（80-100px） | 专业、整洁 |
- 文本左对齐（不要居中显示） | 更便于阅读 |
- 每张幻灯片只展示一个视觉元素 | 保持焦点 |
- 添加幻灯片编号 | 帮助投资者快速查找具体内容 |
- 在角落放置公司标志 | 强化品牌识别 |

## 幻灯片设计示例

### 1. 标题幻灯片

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1920px;height:1080px;background:#0f0f23;display:flex;align-items:center;justify-content:center;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:80px;font-weight:900;margin:0\">DataFlow</h1><p style=\"font-size:32px;opacity:0.7;margin-top:16px\">Automated reporting for data teams</p><p style=\"font-size:22px;opacity:0.5;margin-top:40px\">Seed Round — Q1 2025</p></div></div>"
}'
```

### 2. 问题幻灯片

**用一个具体的数字加上一句话来说明问题。**

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1920px;height:1080px;background:#0f0f23;display:flex;align-items:center;padding:100px;font-family:system-ui;color:white\"><div><p style=\"font-size:24px;color:#f59e0b;text-transform:uppercase;letter-spacing:3px;margin:0\">The Problem</p><h1 style=\"font-size:144px;margin:20px 0;font-weight:900;color:#f59e0b\">12 hrs/week</h1><p style=\"font-size:36px;opacity:0.8;line-height:1.4\">The average data analyst spends 12 hours per week<br>building reports manually</p><p style=\"font-size:20px;opacity:0.4;margin-top:30px\">Source: Forrester Research, 2024</p></div></div>"
}'
```

### 5. 市场规模（TAM/SAM/SOM）

使用同心圆图来展示数据，而非饼图：

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\ncircles = [\n    (0, 0, 4.0, \"#1e1e4a\", \"TAM\\n$50B\", 40),\n    (0, 0, 2.8, \"#2a2a5a\", \"SAM\\n$8B\", 32),\n    (0, 0, 1.4, \"#818cf8\", \"SOM\\n$800M\", 28)\n]\n\nfor x, y, r, color, label, fontsize in circles:\n    circle = plt.Circle((x, y), r, color=color, ec=\"#333366\", linewidth=2)\n    ax.add_patch(circle)\n    ax.text(x, y, label, ha=\"center\", va=\"center\", fontsize=fontsize, color=\"white\", fontweight=\"bold\")\n\nax.set_xlim(-5, 5)\nax.set_ylim(-5, 5)\nax.set_aspect(\"equal\")\nax.axis(\"off\")\nax.text(0, 4.8, \"Market Opportunity\", ha=\"center\", fontsize=36, color=\"white\", fontweight=\"bold\")\nplt.tight_layout()\nplt.savefig(\"market-size.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 7. 发展情况幻灯片

**展示增长趋势，而不仅仅是数字。** 使用向右上方的图表。

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\", \"Jul\", \"Aug\"]\nrevenue = [8, 12, 18, 28, 42, 58, 82, 120]\n\nax.fill_between(range(len(months)), revenue, alpha=0.3, color=\"#818cf8\")\nax.plot(range(len(months)), revenue, color=\"#818cf8\", linewidth=4, marker=\"o\", markersize=10)\nax.set_xticks(range(len(months)))\nax.set_xticklabels(months, color=\"white\", fontsize=18)\nax.tick_params(colors=\"white\", labelsize=16)\nax.set_ylabel(\"MRR ($K)\", color=\"white\", fontsize=20)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.spines[\"bottom\"].set_color(\"#333\")\nax.spines[\"left\"].set_color(\"#333\")\nax.set_title(\"Monthly Recurring Revenue\", color=\"white\", fontsize=32, fontweight=\"bold\", pad=20)\nax.text(7, 120, \"$120K MRR\", color=\"#22c55e\", fontsize=28, fontweight=\"bold\", ha=\"center\", va=\"bottom\")\nax.text(7, 112, \"15x growth in 8 months\", color=\"#22c55e\", fontsize=18, ha=\"center\")\nplt.tight_layout()\nplt.savefig(\"traction.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 8. 竞争分析幻灯片

**不要使用功能对比表来分析竞争对手。** 使用2x2的定位图来展示竞争关系。

```bash
# See the competitor-teardown skill for positioning map generation
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\ncompetitors = {\n    \"Us\": (0.6, 0.7, \"#22c55e\", 300),\n    \"Legacy Tool\": (-0.5, 0.5, \"#6366f1\", 200),\n    \"Startup X\": (0.3, -0.4, \"#6366f1\", 200),\n    \"Manual Process\": (-0.6, -0.6, \"#475569\", 150)\n}\n\nfor name, (x, y, color, size) in competitors.items():\n    ax.scatter(x, y, s=size*5, c=color, zorder=5, alpha=0.8)\n    weight = \"bold\" if name == \"Us\" else \"normal\"\n    ax.annotate(name, (x, y), textcoords=\"offset points\", xytext=(15, 15), fontsize=22, color=\"white\", fontweight=weight)\n\nax.axhline(y=0, color=\"#333\", linewidth=1)\nax.axvline(x=0, color=\"#333\", linewidth=1)\nax.set_xlim(-1, 1)\nax.set_ylim(-1, 1)\nax.set_xlabel(\"Manual ← → Automated\", fontsize=22, color=\"white\", labelpad=15)\nax.set_ylabel(\"Basic ← → Advanced\", fontsize=22, color=\"white\", labelpad=15)\nax.set_title(\"Competitive Landscape\", fontsize=32, color=\"white\", fontweight=\"bold\", pad=20)\nax.tick_params(colors=\"#0f0f23\")\nfor spine in ax.spines.values():\n    spine.set_visible(False)\nplt.tight_layout()\nplt.savefig(\"competition.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 9. 团队幻灯片

```bash
# Generate professional team headshots/avatars
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional headshot portrait, person in business casual attire, clean neutral background, warm studio lighting, confident friendly expression, corporate photography style",
  "width": 512,
  "height": 512
}'
```

布局：将团队成员的照片与姓名、职位和相关资质放在一行中展示。

| 人员 | 格式 |
|--------|--------|
| CEO | 姓名、职位、曾在[公司]任职经历 |
| CTO | 姓名、职位、在[公司]负责开发[项目] |
| 其他成员 | 姓名、职位、相关资质 |

**每张团队幻灯片最多展示4名成员。** 超过4名成员会分散注意力。

## 图表制作指南

| 图表类型 | 适用场景 | 不适用场景 |
|-----------|---------|--------------|
| 折线图 | 显示随时间的变化趋势（如增长情况） | 不适用于类别间的比较 |
| 条形图 | 比较数量 | 时间序列数据（使用折线图） |
| 同心圆图 | 显示总市场容量（TAM）、目标市场容量（SAM）、可服务市场容量（SOM） | 其他场景 |
| 2x2矩阵图 | 用于展示竞争定位 | 用于功能对比 |
| 单个数字图表 | 突出关键指标 | 多个指标同时展示 |
| 饼图 | 绝对不要使用 | 阅读困难且不够专业 |

### 图表设计规则

| 规则 | 原因 |
|------|-----|
- 每张图表最多使用2种颜色 | 保持清晰度 |
- 公司相关内容使用绿色或品牌指定颜色 | 产生积极印象 |
- 直接在图表上标注数据来源 | 增强可信度 |
- 去除网格线或使用非常细微的网格线 | 减少杂乱感 |
- Y轴从0开始 | 避免误导观众 |
- 必须注明数据来源 | 增加可信度 |

## 投资者关注的重点

| 幻灯片 | 投资者关心的问题 |
|-------|------------------------|
| 问题 | “这确实是一个值得人们付费解决的问题吗？” |
| 解决方案 | “这个方案比现有方案好10倍吗？” |
| 市场规模 | “市场规模是否足够大，足以产生影响？” |
| 发展情况 | “这个方案真的有效吗？” |
| 团队 | “这些人有能力执行项目吗？” |
| 投资需求 | “这个投资要求合理吗？” |

## 常见错误

| 错误 | 问题 | 修正方法 |
|---------|---------|-----|
| 幻灯片太多（超过20张） | 会分散注意力 | 最多12-15张 |
| 文字过多 | 投资者无法阅读 | 遵循“1-6-6”原则：每个要点6个字 |
| 与竞争对手的功能对比表 | 显示出防御性 | 使用2x2的定位图 |
| 使用饼图 | 阅读困难且不够专业 | 使用条形图或具体的数字 |
| 不注明数据来源 | 会让方案显得不真实 | 必须注明数据来源 |
| 团队幻灯片上展示太多成员 | 信息分散 | 最多展示4名成员，重点突出相关经验 |
| 设计不一致 | 显得不专业 | 所有幻灯片的颜色、字体、页边距要保持一致 |
| 没有“投资需求”幻灯片 | 投资者不知道您的投资要求 | 明确说明投资金额、资金用途和项目时间表 |
| 过于强调表面的数据指标 | “100万访问量”没有实际意义 | 应展示收入、活跃用户数、用户留存率 |
| 产品演示时间过长 | 这是商业演示，不是产品展示 | 产品相关内容最多展示2张幻灯片，重点讨论商业模式 |

## 相关技能

```bash
npx skills add inferencesh/skills@competitor-teardown
npx skills add inferencesh/skills@data-visualization
npx skills add inferencesh/skills@ai-image-generation
```

查看所有可用应用程序：`infsh app list`
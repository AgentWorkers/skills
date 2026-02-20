---
name: pitch-deck-visuals
description: "**投资者演示文稿结构：包含逐页展示的框架、视觉设计规范及数据呈现方法**  
本文档介绍了适用于融资演示文稿、投资者汇报、初创企业推介、演示日及拨款申请等的12页框架结构，涵盖了各类图表类型、团队介绍幻灯片，以及可能令投资者反感的常见内容。  
**适用场景：**  
- 融资演示文稿  
- 投资者汇报  
- 初创企业推介  
- 演示日  
- 授款申请  
**相关术语：**  
- 演示文稿（pitch deck）  
- 投资者演示文稿（investor presentation）  
- 初创企业推介（startup pitch）  
- 融资活动（fundraising event）  
- 演示日（demo day）  
- 种子轮融资（seed funding）  
- A轮融资（Series A financing）  
- VC（风险投资）  
**主要内容：**  
1. **12页框架结构**：  
   - 介绍公司背景与愿景  
   - 产品/服务概述  
   - 市场分析与竞争格局  
   - 商业模式与收入来源  
   - 团队成员与经验  
   - 营运计划与财务预测  
   - 风险评估与应对策略  
   - 执行计划与里程碑  
   - 融资需求与使用计划  
   - 问答环节  
2. **图表类型与使用规范**：  
   - 使用图表来辅助数据解释，提高信息传递效率  
   - 选择合适的图表类型（如柱状图、折线图、饼图等）  
   - 确保图表清晰易读，避免过多复杂元素  
3. **团队介绍幻灯片**：  
   - 团队成员简介  
   - 主要职责与背景  
   - 团队成就与经验  
4. **避免让投资者反感的常见内容：**  
   - 过度承诺或不切实际的预测  
   - 无关紧要的细节  
   - 漫无目的的文字描述  
   - 缺乏数据支持的观点  
**使用建议：**  
- 根据目标受众调整内容与风格  
- 定期更新演示文稿以反映最新进展  
- 进行多次演练，确保流畅度与准确性  
希望本文档能帮助您制作出专业、有效的投资者演示文稿！"
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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可手动进行安装和验证：[点击此处](https://dist.inference.sh/cli/checksums.txt)。

## 12 张幻灯片的框架结构

| 序号 | 幻灯片内容 | 时长 | 说明 |
| --- | --- | --- | --- |
| 1 | **标题** | 15 秒 | 公司名称、标语、您的姓名 |
| 2 | **问题** | 45 秒 | 数据使用中遇到的痛点 |
| 3 | **解决方案** | 45 秒 | 用一句话概括您的产品 |
| 4 | **产品演示** | 60 秒 | 屏幕截图或实时演示 |
| 5 | **市场规模** | 30 秒 | 总市场容量（TAM）→ 目标市场容量（SAM）→ 可服务市场容量（SOM） |
| 6 | **商业模式** | 30 秒 | 您如何盈利 |
| 7 | **发展情况** | 45 秒 | 成长指标、客户数量 |
| 8 | **竞争分析** | 30 秒 | 产品定位（而非功能列表） |
| 9 | **团队介绍** | 30 秒 | 为什么您能胜出 |
| 10 | **财务数据** | 30 秒 | 收入预测、单位经济模型 |
| 11 | **投资需求** | 15 秒 | 需要的投资金额及用途 |
| 12 | **联系方式** | 10 秒 | 电子邮件地址、下一步行动 |

**总时长：约 6 分钟。** 幻灯片数量不超过 20 张。

## 幻灯片设计规则

### 字体排版

| 元素 | 大小（1920x1080） | 规则 |
| --- | --- | --- |
| 幻灯片标题 | 48-72px | 最多 6 个字 |
| 关键数据/数字 | 96-144px | 每张幻灯片最多显示一个 |
| 正文内容 | 24-32px | 每张幻灯片最多 6 个要点 |
| 图例/数据来源 | 16-20px | 必须注明数据来源 |
| 字体 | 仅使用无衬线字体（如 Inter, Helvetica, SF Pro 等） |

### 1-6-6 规则

- 每张幻灯片展示一个核心观点 |
- 每个要点最多 6 个字 |
- 每张幻灯片最多 6 个要点 |

如果需要更多内容，就需要增加幻灯片数量。

### 颜色搭配

| 元素 | 颜色建议 |
| --- | --- |
| 背景颜色 | 深蓝色（navy）或纯白色 |
| 强调色 | 使用统一的品牌颜色 |
| 正文颜色 | 浅色背景上使用白色；深色背景上使用深灰色（#333） |
| 图表颜色 | 最多使用 2-3 种颜色，确保其中包含品牌颜色 |
| 避免使用：渐变色、霓虹色或超过 3 种颜色 |

### 布局原则

| 规则 | 原因 |
| --- | --- |
| 保持一致的页边距（80-100px） | 专业且整洁 |
- 文本左对齐（不要居中） | 更便于阅读 |
- 每张幻灯片只展示一个视觉元素 | 保持焦点 |
- 添加幻灯片编号 | 帮助投资者快速定位内容 |
- 在角落放置公司标志 | 强化品牌识别 |

## 各幻灯片的详细设计指南

### 1. 标题幻灯片

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1920px;height:1080px;background:#0f0f23;display:flex;align-items:center;justify-content:center;font-family:system-ui;color:white;text-align:center\"><div><h1 style=\"font-size:80px;font-weight:900;margin:0\">DataFlow</h1><p style=\"font-size:32px;opacity:0.7;margin-top:16px\">Automated reporting for data teams</p><p style=\"font-size:22px;opacity:0.5;margin-top:40px\">Seed Round — Q1 2025</p></div></div>"
}'
```

### 2. 问题幻灯片

**用一个具体的数字和一个简短的句子来描述问题。**

```bash
infsh app run infsh/html-to-image --input '{
  "html": "<div style=\"width:1920px;height:1080px;background:#0f0f23;display:flex;align-items:center;padding:100px;font-family:system-ui;color:white\"><div><p style=\"font-size:24px;color:#f59e0b;text-transform:uppercase;letter-spacing:3px;margin:0\">The Problem</p><h1 style=\"font-size:144px;margin:20px 0;font-weight:900;color:#f59e0b\">12 hrs/week</h1><p style=\"font-size:36px;opacity:0.8;line-height:1.4\">The average data analyst spends 12 hours per week<br>building reports manually</p><p style=\"font-size:20px;opacity:0.4;margin-top:30px\">Source: Forrester Research, 2024</p></div></div>"
}'
```

### 5. 市场规模（TAM/SAM/SOM）

使用同心圆图来展示市场规模，而非饼图：

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\ncircles = [\n    (0, 0, 4.0, \"#1e1e4a\", \"TAM\\n$50B\", 40),\n    (0, 0, 2.8, \"#2a2a5a\", \"SAM\\n$8B\", 32),\n    (0, 0, 1.4, \"#818cf8\", \"SOM\\n$800M\", 28)\n]\n\nfor x, y, r, color, label, fontsize in circles:\n    circle = plt.Circle((x, y), r, color=color, ec=\"#333366\", linewidth=2)\n    ax.add_patch(circle)\n    ax.text(x, y, label, ha=\"center\", va=\"center\", fontsize=fontsize, color=\"white\", fontweight=\"bold\")\n\nax.set_xlim(-5, 5)\nax.set_ylim(-5, 5)\nax.set_aspect(\"equal\")\nax.axis(\"off\")\nax.text(0, 4.8, \"Market Opportunity\", ha=\"center\", fontsize=36, color=\"white\", fontweight=\"bold\")\nplt.tight_layout()\nplt.savefig(\"market-size.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 7. 发展情况幻灯片

**展示实际增长数据，而不仅仅是数字。** 使用从左上角向右增长的图表。

```bash
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\nmonths = [\"Jan\", \"Feb\", \"Mar\", \"Apr\", \"May\", \"Jun\", \"Jul\", \"Aug\"]\nrevenue = [8, 12, 18, 28, 42, 58, 82, 120]\n\nax.fill_between(range(len(months)), revenue, alpha=0.3, color=\"#818cf8\")\nax.plot(range(len(months)), revenue, color=\"#818cf8\", linewidth=4, marker=\"o\", markersize=10)\nax.set_xticks(range(len(months)))\nax.set_xticklabels(months, color=\"white\", fontsize=18)\nax.tick_params(colors=\"white\", labelsize=16)\nax.set_ylabel(\"MRR ($K)\", color=\"white\", fontsize=20)\nax.spines[\"top\"].set_visible(False)\nax.spines[\"right\"].set_visible(False)\nax.spines[\"bottom\"].set_color(\"#333\")\nax.spines[\"left\"].set_color(\"#333\")\nax.set_title(\"Monthly Recurring Revenue\", color=\"white\", fontsize=32, fontweight=\"bold\", pad=20)\nax.text(7, 120, \"$120K MRR\", color=\"#22c55e\", fontsize=28, fontweight=\"bold\", ha=\"center\", va=\"bottom\")\nax.text(7, 112, \"15x growth in 8 months\", color=\"#22c55e\", fontsize=18, ha=\"center\")\nplt.tight_layout()\nplt.savefig(\"traction.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 8. 竞争分析幻灯片

**不要用功能对比表来展示竞争对手的情况。** 使用 2x2 的竞争定位图。

```bash
# See the competitor-teardown skill for positioning map generation
infsh app run infsh/python-executor --input '{
  "code": "import matplotlib.pyplot as plt\nimport matplotlib\nmatplotlib.use(\"Agg\")\n\nfig, ax = plt.subplots(figsize=(19.2, 10.8))\nfig.patch.set_facecolor(\"#0f0f23\")\nax.set_facecolor(\"#0f0f23\")\n\ncompetitors = {\n    \"Us\": (0.6, 0.7, \"#22c55e\", 300),\n    \"Legacy Tool\": (-0.5, 0.5, \"#6366f1\", 200),\n    \"Startup X\": (0.3, -0.4, \"#6366f1\", 200),\n    \"Manual Process\": (-0.6, -0.6, \"#475569\", 150)\n}\n\nfor name, (x, y, color, size) in competitors.items():\n    ax.scatter(x, y, s=size*5, c=color, zorder=5, alpha=0.8)\n    weight = \"bold\" if name == \"Us\" else \"normal\"\n    ax.annotate(name, (x, y), textcoords=\"offset points\", xytext=(15, 15), fontsize=22, color=\"white\", fontweight=weight)\n\nax.axhline(y=0, color=\"#333\", linewidth=1)\nax.axvline(x=0, color=\"#333\", linewidth=1)\nax.set_xlim(-1, 1)\nax.set_ylim(-1, 1)\nax.set_xlabel(\"Manual ← → Automated\", fontsize=22, color=\"white\", labelpad=15)\nax.set_ylabel(\"Basic ← → Advanced\", fontsize=22, color=\"white\", labelpad=15)\nax.set_title(\"Competitive Landscape\", fontsize=32, color=\"white\", fontweight=\"bold\", pad=20)\nax.tick_params(colors=\"#0f0f23\")\nfor spine in ax.spines.values():\n    spine.set_visible(False)\nplt.tight_layout()\nplt.savefig(\"competition.png\", dpi=100, facecolor=\"#0f0f23\")\nprint(\"Saved\")"
}'
```

### 9. 团队介绍幻灯片

```bash
# Generate professional team headshots/avatars
infsh app run falai/flux-dev-lora --input '{
  "prompt": "professional headshot portrait, person in business casual attire, clean neutral background, warm studio lighting, confident friendly expression, corporate photography style",
  "width": 512,
  "height": 512
}'
```

**布局建议：** 将团队成员的照片与姓名、职位及相关资质放在一行中展示。

| 成员 | 格式 |
| --- | --- |
| CEO | 姓名、职位、曾在 [公司] 的任职经历 |
| CTO | 姓名、职位、在 [公司] 的主要贡献 |
| 其他成员 | 姓名、职位、相关资质 |

**每张团队幻灯片最多展示 4 位成员。** 超过 4 位会显得信息过于分散。

## 图表制作指南

| 图表类型 | 适用场景 | 不适用场景 |
| --- | --- | --- |
| 折线图 | 显示随时间的变化趋势（如用户增长） | 比较不同类别的数据 |
| 条形图 | 比较数量 | 时间序列数据（使用折线图） |
| 同心圆图 | 展示总市场容量（TAM）、目标市场容量（SAM）和可服务市场容量（SOM） | 其他场景 |
| 2x2 矩阵图 | 展示竞争定位 | 功能对比 |
| 单个大数字 | 突出关键指标 | 多个指标同时展示 |
| 饼图 | 绝对不要使用 | 阅读困难且不够专业 |

### 图表设计原则

| 规则 | 原因 |
| --- | --- |
- 每张图表最多使用 2 种颜色 | 保持清晰度 |
- 使用公司颜色或品牌颜色 | 产生积极印象 |
- 直接在图表上标注标签 | 不需要单独的图例 |
- 去除网格线或使用非常细微的网格 | 减少杂乱感 |
- Y 轴从 0 开始 | 避免误导观众 |
- 必须注明数据来源 | 增加可信度 |

## 投资者关注的重点

| 幻灯片内容 | 投资者关心的问题 |
| --- | --- |
| 问题 | “这确实是一个值得解决的问题吗？” |
| 解决方案 | “这个方案比现有方案好多少倍？” |
| 市场规模 | “市场规模是否足够大？” |
| 发展情况 | “这个方案真的有效吗？” |
| 团队 | “这些人有能力执行吗？” |
| 投资需求 | “这个投资方案合理吗？” |

## 常见错误

| 错误类型 | 问题 | 解决方法 |
| --- | --- | --- |
| 幻灯片太多（超过 20 张） | 信息分散，容易失去观众注意力 | 限制在 12-15 张 |
| 文字过多 | 投资者难以阅读 | 遵循 1-6-6 规则：每个要点 6 个字 |
| 用功能对比表来展示竞争对手 | 显得防御性 | 使用 2x2 竞争定位图 |
| 使用饼图 | 阅读困难且不够专业 | 使用条形图或具体的数字 |
| 不注明数据来源 | 令人怀疑数据的真实性 | 必须注明数据来源 |
| 团队幻灯片包含过多成员 | 信息分散 | 每张幻灯片最多展示 4 位成员，突出关键经验 |
| 设计不一致 | 显得不专业 | 所有幻灯片的颜色、字体和页边距应保持一致 |
| 没有“投资需求”幻灯片 | 投资者不清楚您的投资要求 | 明确说明投资金额、资金用途和时间表 |
| 过于强调表面的数据指标 | 如“100 万访问量”没有实际意义 | 展示收入、活跃用户数和用户留存率 |
| 产品演示时间过长 | 这是商业提案，不是产品演示 | 产品相关幻灯片最多 2 张，重点应放在商业模式上 |

## 相关技能

```bash
npx skills add inference-sh/skills@competitor-teardown
npx skills add inference-sh/skills@data-visualization
npx skills add inference-sh/skills@ai-image-generation
```

查看所有可用应用：`infsh app list`
---
name: SEO / Search Engine Optimization
slug: seo
version: 1.0.2
homepage: https://clawic.com/skills/seo
changelog: "Added content writing, audit checklists, and memory templates"
description: SEO专家，提供网站审核、内容撰写、关键词研究、技术问题解决、链接建设以及排名策略等服务。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解工作区的集成方法。

## 使用场景

当需要处理 SEO 相关任务时，例如网站审计、内容优化、关键词研究、技术修复、链接策略、本地 SEO、结构化数据标记（schema markup）或排名提升等，可以使用该工具。

## 架构

SEO 相关的工作区位于 `~/seo/` 目录下。具体设置方法请参考 `memory-template.md`。

```
~/seo/
├── memory.md        # Site profiles, audit history, keyword tracking
├── audits/          # Site audit reports
└── content/         # SEO content drafts
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 标题标签、元描述、标题层级、关键词布局 | `on-page.md` |
| 核心网页质量指标（Core Web Vitals）、可爬取性、移动设备适配、索引 | `technical.md` |
| 搜索意图（Search Intent）、用户体验（Experience）、专家性（Expertise）、可信度（Authenticity） | `content.md` |
| Google 商业账户（Google Business Profile）、NAP 一致性（Name, Address, Phone Number consistency）、本地关键词 | `local.md` |
| JSON-LD、Article、LocalBusiness、常见问题解答（FAQ）、产品结构化数据（Product Schema） | `schema.md` |
| 内部链接、锚文本（Anchor Text）、外部链接策略 | `links.md` |
| 关键词研究及竞争分析 | `keywords.md` |

## 核心规则

### 1. 先审计再行动
在提出任何建议之前，先进行全面的网站审计。检查以下内容：索引情况、爬取错误、核心网页质量指标、移动设备适配性、重复内容以及失效链接。切勿盲目猜测。

### 2. 首先匹配搜索意图
确保内容格式与用户的搜索意图相匹配。信息类内容应对应引导性页面；交易类内容应对应产品页面；商业类内容应对应比较页面。格式不匹配会导致无法被搜索引擎收录。

### 3. 既符合用户需求又能被搜索引擎收录的内容
编写既符合用户需求又能被搜索引擎收录的 SEO 内容。在开头 100 字内回答用户的查询，全面覆盖主题，并自然地融入 LSI（Long-Sighted Search Keywords）关键词。添加“常见问题解答”部分以解答用户可能的其他问题。

### 4. 技术基础
- 核心网页质量指标：加载时间（LCP）< 2.5 秒，页面响应时间（INP）< 200 毫秒，页面加载速度（CLS）< 0.1 秒。优先考虑移动设备适配。使用 HTTPS 协议。确保网站地图（sitemap）清晰无误，且没有任何资源被阻止访问。技术问题会严重影响排名。

### 5. 体现用户体验、专家性、可信度
内容应体现作者的专业背景和可信度。提供作者的简介和资质证明，以及关于网站的说明页面。对于涉及“你的产品/服务如何帮助用户”（How Your Product/Service Helps Users, YMYL）类的内容，这一点尤为重要。

### 6. 链接策略
内部链接有助于提升页面的主题权威性。锚文本的选择非常重要。来自权威来源的外部链接也能起到积极作用。切勿购买链接或参与任何不良的链接交换行为。

### 7. 全面监控数据
跟踪网站的排名、自然流量（organic traffic）、点击率（CTR）和转化率（conversions）。使用 Search Console 提供的数据进行优化，并根据实际结果进行调整，而非基于猜测。

## SEO 审计检查清单

**索引方面：**
- [ ] 网站已在 Google 中被收录（例如：site:domain.com）
- [ ] `robots.txt` 文件中未屏蔽任何重要页面
- [ ] 已将 XML 网站地图提交至 Search Console
- [ ] 应被收录的页面上没有设置“noindex”标签

**技术方面：**
- [ ] 核心网页质量指标达标
- [ ] 网站对移动设备友好
- [ ] 使用 HTTPS 协议，且没有混合内容（mixed content）
- [ ] Search Console 中没有爬取错误
- [ ] 网站链接结构清晰

**页面内容方面：**
- [ ] 标题标签唯一（50-60 个字符）
- [ ] 元描述（150-160 个字符）
- [ ] 每个页面只有一个 H1 标题，并包含相关关键词
- [ ] 标题层级清晰合理
- [ ] 图片配有适当的 alt 文本
- [ ] 有适当的内部链接

**内容质量方面：**
- [ ] 内容符合用户的搜索意图
- [ ] 内容全面且无重复
- [ ] 内容新鲜且定期更新

**外部链接方面：**
- [ ] 已创建 Google 商业账户（针对本地业务）
- [ ] 拥有高质量的外部链接
- [ ] 网站没有不良链接

## 内容写作流程

1. **关键词研究**：确定目标关键词、搜索量及关键词难度。
2. **分析搜索意图**：了解用户的需求和搜索意图。
3. **制定大纲**：涵盖竞争对手覆盖的所有子主题，并在此基础上进行扩展。
4. **撰写内容**：快速回答用户的查询，内容全面且使用自然的语言和关键词。
5. **优化内容**：调整标题、元描述、标题层级和内部链接，并添加结构化数据标记。
6. **发布内容**：将优化后的内容提交至 Search Console 并持续监控排名变化。

## 常见误区

- 在未了解用户搜索意图的情况下编写内容 → 无法提高排名。
- 忽视核心网页质量指标 → 会导致排名下降。
- 过度使用关键词 → 会引发搜索引擎的惩罚。
- 使用重复的标题标签 → 会浪费爬取资源。
- 没有内部链接 → 会影响页面的主题权威性。
- 购买外部链接 → 有被搜索引擎处罚的风险。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
```
clawhub install <slug>
```
例如：
- `content-marketing`：内容策略（Content Strategy）
- `analytics`：流量分析（Traffic Analysis）
- `market-research`：竞争分析（Competitive Analysis）
- `html`：HTML 优化（HTML Optimization）
- `web`：网页开发（Web Development）

## 反馈建议
- 如内容有用，请给予好评：`clawhub star seo`
- 保持信息更新：`clawhub sync`
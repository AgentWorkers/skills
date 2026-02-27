---
name: SEO (Site Audit + Content Writer + Competitor Analysis)
slug: seo
version: 1.0.3
homepage: https://clawic.com/skills/seo
changelog: "Improved name clarity with key capabilities"
description: SEO专家，提供网站审计、内容撰写、关键词研究、技术问题解决、链接建设以及排名策略等服务。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解工作空间的集成方法。

## 使用场景

当需要处理 SEO 相关任务时，例如站点审计、内容优化、关键词研究、技术修复、链接策略、本地 SEO、架构标记或排名提升等，可以使用该工具。

## 架构

SEO 相关的工作空间位于 `~/seo/` 目录下。具体设置方法请参考 `memory-template.md`。

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
| 核心网页质量（Core Web Vitals）、可爬取性、移动设备适配、索引 | `technical.md` |
| 搜索意图（Search Intent）、用户体验（Experience）、专家性（Expertise）、可信度（Authority）、可访问性（Accessibility） | `content.md` |
| Google Business 账户管理、NAP 一致性（Name, Address, Phone的一致性）、本地关键词 | `local.md` |
| JSON-LD、Article、LocalBusiness、FAQ、产品结构化数据（Product Schema） | `schema.md` |
| 内部链接、锚文本（Anchor Text）、外部链接策略 | `links.md` |
| 关键词研究及竞争分析 | `keywords.md` |

## 核心规则

### 1. 先审计再行动
在提出任何建议之前，先进行全面的站点审计。检查以下内容：索引情况、爬取错误、核心网页质量、移动设备适应性、重复内容、失效链接。切勿凭猜测行事。

### 2. 首先匹配搜索意图
确保内容格式与用户查询意图相匹配。信息类内容应对应引导型页面；交易类内容应对应产品页面；商业类内容应对应比较型页面。格式不正确会导致排名下降。

### 3. 既满足用户需求又能被搜索引擎收录的内容
编写既符合用户需求又能被搜索引擎收录的 SEO 内容。在开头 100 个词内回答用户的问题，全面覆盖相关主题，并自然地融入 LSI（Long-Sighted Search Keywords，长尾关键词）。

### 4. 技术基础
- 核心网页质量指标：LCP（加载时间）< 2.5 秒，INP（首次交互时间）< 200 毫秒，CLS（点击通过率）< 0.1。
- 优先考虑移动设备适配。
- 使用 HTTPS 协议。
- 确保 URL 是规范的。
- 确保站点地图（sitemap）清晰无误，且没有资源被阻止访问。技术问题会严重影响排名。

### 5. 体现用户体验、专家性、可信度和可访问性
- 提供作者的简介及其相关资质信息。
- 设置“关于我们”页面。
- 添加外部引用，尤其是对于涉及“你的产品/服务如何帮助我”（How Your Product/Service Helps Me, YMYL）类型的主题时尤为重要。

### 6. 链接策略
- 内部链接有助于提升页面的主题权威性。锚文本的质量很重要。
- 寻求来自权威来源的外部链接。切勿购买链接或参与任何链接买卖行为。

### 7. 全面监控
- 监控排名、自然流量（organic traffic）、点击率（CTR）和转化率（conversions）。
- 使用 Search Console 的数据进行分析，并根据实际结果进行调整，而非基于假设。

## SEO 审计检查清单

**索引方面：**
- [ ] 网站已收录在 Google 中（例如：site:domain.com）
- [ ] `robots.txt` 文件中未屏蔽任何重要页面
- [ ] 已将 XML 站点地图提交至 Search Console
- [ ] 应该被收录的页面上没有设置“noindex”标签

**技术方面：**
- [ ] 核心网页质量指标达标
- [ ] 网站对移动设备友好
- [ ] 使用 HTTPS 协议，且没有混合内容
- [ ] Search Console 中没有爬取错误
- [ ] URL 结构清晰

**页面内容方面：**
- [ ] 标题标签唯一（50-60 个字符）
- [ ] 元描述（150-160 个字符）
- 每个页面包含一个包含关键词的 H1 标题
- 标题层级清晰合理
- 图片配有 alt 文本
- 存在内部链接

**内容方面：**
- [ ] 内容与用户查询意图相匹配
- 内容全面且无重复
- 内容新鲜且定期更新

**外部链接方面：**
- [ ] 已创建 Google Business 账户（针对本地业务）
- 拥有高质量的外部链接
- 不存在有害链接

## 内容写作流程

1. **关键词研究**：确定目标关键词、搜索量及关键词难度。
2. **意图分析**：了解哪种内容格式更易被收录；用户需要什么类型的信息。
3. **大纲制定**：涵盖竞争对手涵盖的所有子主题，并在此基础上进行扩展。
4. **写作**：快速回答用户问题，内容全面且使用自然的语言。
5. **优化**：调整标题、元描述、标题层级、内部链接和结构化数据。
6. **发布**：将内容提交至 Search Console 并持续监控排名变化。

## 常见误区

- 不考虑搜索意图就编写内容 → 会导致排名不佳。
- 忽视核心网页质量指标 → 会影响排名。
- 过度使用关键词 → 会引发搜索引擎的惩罚。
- 使用重复的标题标签 → 会浪费爬虫的爬取资源。
- 没有内部链接 → 会导致页面的主题权威性降低。
- 购买外部链接 → 有被搜索引擎处罚的风险。

## 相关技能
如果用户需要，可以使用以下命令进行工具的安装：
```
clawhub install <slug>
```
相关技能包括：
- `content-marketing`：内容策略
- `analytics`：流量分析
- `market-research`：竞争分析
- `html`：HTML 优化
- `web`：网页开发

## 反馈方式

- 如果内容有用，请给工具打星评价：`clawhub star seo`
- 为了获取最新信息，请执行 `clawhub sync` 命令。
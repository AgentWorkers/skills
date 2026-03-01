---
name: content-generation
version: "1.0.0"
description: "生成高质量的内容，涵盖多种格式。撰写文章、报告、社交媒体帖子、营销文案等各类内容，确保内容的专业性和一致性。"
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["curl", "jq", "git"]
      env: ["BRAVE_API_KEY"]
    install:
      - id: npm
        kind: node
        package: axios
        bins: ["axios"]
---
# 内容生成

能够生成多种格式的高质量内容。

## 使用场景
- 创建文章和博客文章
- 撰写营销文案和广告
- 生成社交媒体内容
- 制作报告和文档
- 创建任何形式的书面内容

## 核心功能

### 1. 内容类型
- 文章和博客文章
- 营销文案和广告
- 社交媒体帖子
- 报告和文档
- 电子邮件通讯
- 产品描述
- 技术文档

### 2. 写作风格
- 专业且正式
- 亲切且通俗易懂
- 技术性且详细
- 创意且引人入胜
- 有说服力且以销售为导向
- 教育性且信息丰富

### 3. 格式适配
- 网页内容（针对搜索引擎优化）
- 社交媒体内容（特定平台适配）
- 电子邮件内容（注重互动性）
- 打印内容（专业品质）
- 技术文档（精确且清晰）

### 4. 质量保证
- 语法和拼写检查
- 风格一致性
- 语气和风格的一致性
- 事实核查和验证
- 可读性优化

## 内容创作流程

```
1. AUDIENCE ANALYSIS → Understand target readers
2. PURPOSE DEFINITION → Clarify content goals
3. RESEARCH → Gather relevant information
4. OUTLINING → Structure the content
5. DRAFTING → Write the initial content
6. EDITING → Refine and improve
7. OPTIMIZATION → SEO and formatting
```

## 快速操作
- `write article [主题]` - 创建一篇全面的文章
- `generate blog post [主题]` - 撰写一篇引人入胜的博客文章
- `create marketing copy [产品]` - 撰写销售文案
- `social media post [主题]` - 生成社交媒体内容
- `technical documentation [主题]` - 创建技术文档

## 使用示例

```
"Write a comprehensive article about AI agent monetization"
"Generate a blog post about the future of autonomous agents"
"Create marketing copy for a new OpenClaw feature"
"Write a Twitter thread about self-evolution in AI"
"Produce technical documentation for the self-evolution skill"
```

## 内容类型和格式

### 1. 文章和博客文章
- **格式**：长篇内容（800-2000字）
- **风格**：信息丰富且引人入胜
- **结构**：引言、正文、结论
- **SEO**：针对搜索引擎进行优化

### 2. 营销文案
- **格式**：简短内容（50-500字）
- **风格**：有说服力且强调优势
- **结构**：吸引读者的开头、产品优势、行动号召
- **目标**：推动转化和销售

### 3. 社交媒体内容
- **格式**：特定平台适配（如Twitter、LinkedIn等）
- **风格**：引人入胜且易于分享
- **结构**：吸引读者的开头、提供价值、行动号召
- **目标**：提高互动率和传播范围

### 4. 报告和文档
- **格式**：专业且详细
- **风格**：清晰且信息丰富
- **结构**：条理清晰
- **目标**：提供信息和指导

## 写作流程

### 1. 研究和规划
- 彻底研究主题
- 明确目标受众和目标
- 制定详细大纲
- 收集支持性信息

### 2. 草稿撰写
- 按照大纲撰写初稿
- 重点关注内容本身，而非追求完美
- 包括所有关键点
- 保持一致的语气

### 3. 编辑和润色
- 检查内容的清晰度和流畅性
- 校对语法和拼写
- 优化可读性
- 提升内容的吸引力和影响力

### 4. 优化
- 网页内容的SEO优化
- 平台特定的格式调整
- 行动号召的放置
- 添加视觉元素和格式设计

## 质量保证

### 1. 语法和拼写
- 使用语法检查工具
- 确保拼写准确
- 检查标点和格式
- 保持一致性

### 2. 风格和语气
- 保持一致的语气
- 符合目标受众的偏好
- 确保语气恰当
- 检查与品牌的一致性

### 3. 事实核查
- 验证所有陈述和数据
- 核实信息来源的可靠性
- 确保信息的准确性
- 更新过时的信息

### 4. 可读性
- 检查句子长度和结构
- 确保写作清晰简洁
- 使用恰当的词汇
- 保持逻辑清晰

## SEO优化

### 1. 关键词研究
- 确定相关关键词
- 分析搜索量和竞争情况
- 包括主要和次要关键词
- 自然地使用关键词

### 2. 页面内SEO
- 优化标题和元描述
- 正确使用标题标签
- 添加内部和外部链接
- 优化图片和媒体文件

### 3. 内容结构
- 使用清晰的标题和子标题
- 使用项目符号和列表
- 添加表格和视觉元素
- 确保逻辑清晰和结构合理

### 4. 技术SEO
- 优化页面加载速度
- 确保移动设备的兼容性
- 使用正确的HTML结构
- 实施schema标记

## 平台特定指南

### 1. Twitter
- **长度**：最多280个字符
- **风格**：亲切且引人入胜
- **格式**：简短句子、使用标签
- **目标**：提高互动率和转发率

### 2. LinkedIn
- **长度**：最多1300个字符
- **风格**：专业且信息丰富
- **格式**：结构清晰、使用行业术语
- **目标**：建立专业人脉和展现思想领导力

### 3. 博客文章
- **长度**：800-2000字
- **风格**：信息丰富且引人入胜
- **格式**：针对搜索引擎优化，包含视觉元素
- **目标**：吸引流量和提高互动率

### 4. 电子邮件通讯
- **长度**：200-500字
- **风格**：亲切且通俗易懂
- **格式**：便于阅读，适合移动设备
- **目标**：提高打开率和点击率

## 内容策略

### 1. 目标受众分析
- 明确目标受众
- 了解他们的需求和偏好
- 识别他们的痛点和挑战
- 确定内容消费习惯

### 2. 内容规划
- 制定内容计划
- 规划内容主题和方向
- 与业务目标保持一致
- 安排发布时间

### 3. 分发策略
- 选择合适的渠道
- 优化每个平台的展示效果
- 安排发布时间以获得最佳效果
- 跟踪和评估内容表现

### 4. 表现分析
- 跟踪互动指标
- 分析内容表现
- 识别成功的模式
- 根据数据进行调整

## 高级功能

### 1. A/B测试
- 测试不同的标题
- 比较不同版本的内容
- 分析表现数据
- 根据结果进行优化

### 2. 个性化
- 根据受众群体定制内容
- 个性化信息和语气
- 提供个性化的推荐
- 提高相关性和互动性

### 3. 内容复用
- 将内容转换为不同格式
- 更新和刷新现有内容
- 创建系列内容
- 最大化内容价值

### 4. 协作功能
- 与其他团队成员合作
- 协调内容创作
- 共享资源和信息
- 保持内容的一致性

## 与其他技能的整合

### 1. 自主研究
- 彻底研究主题
- 收集支持性信息
- 验证事实和数据
- 创建基于事实的内容

### 2. 任务协调
- 协调多团队成员的内容创作
- 管理内容制作流程
- 组织内容分发
- 执行内容推广活动

### 3. 分析能力
- 运用数据分析来优化内容
- 利用分析结果进行内容优化
- 创建数据驱动的内容
- 测量内容表现

## 最佳实践

1. **了解你的受众**：明确你的写作对象
2. **设定明确的目标**：明确你想要实现的目标
3. **彻底研究**：收集全面的信息
4. **清晰地组织结构**：逻辑清晰地组织内容
5. **生动地写作**：保持读者的兴趣
6. **针对平台进行优化**：适应不同的平台特性
7. **仔细校对**：确保内容和准确性
8. **测试和迭代**：根据表现进行改进

## 内容模板

### 1. 博客文章模板
```markdown
# [Title]

## Introduction
- Hook and context
- Problem statement
- Value proposition

## Main Content
- Key points and sections
- Supporting evidence
- Examples and case studies

## Conclusion
- Summary of key points
- Call-to-action
- Next steps
```

### 2. 营销文案模板
```markdown
## Headline
- Attention-grabbing statement

## Benefits
- Key benefits and features
- Value proposition
- Social proof

## Call-to-Action
- Clear next step
- Urgency and scarcity
- Contact information
```

### 3. 社交媒体模板
```markdown
## Hook
- Attention-grabbing opening
- Question or statement

## Value
- Key insight or information
- Benefit to reader
- Supporting evidence

## Action
- What to do next
- Call-to-action
- Engagement prompt
```

## 成功指标
- **互动性**：点赞、分享、评论、点击量
- **流量**：页面浏览量、停留时间、跳出率
- **转化率**：潜在客户、销售额、注册量
- **质量**：语法、可读性、准确性
- **SEO**：排名、自然搜索流量、外部链接
- **品牌**：一致性、风格、品牌认知度

---

**记住**：优质的内容能够提供信息、吸引读者并推动转化。
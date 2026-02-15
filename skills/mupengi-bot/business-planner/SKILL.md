# 商业计划生成工具

> 自动生成商业计划书、基础设施图谱和演示文稿  
> 从版本1到版本12的迭代优化经验已内化（Doyak Package项目历程）

---

## 📋 元数据

```yaml
name: business-planner
description: "Auto-generate business plans, infrastructure diagrams, pitch decks. Includes government funding (Doyak Package/TIPS/Startup Academy), investor IR, tech infrastructure design. Internalized v1~v12 iteration experience."
author: 무펭이 🐧
version: 1.0.0
created: 2026-02-14
triggers:
  - "business plan"
  - "pitch deck"
  - "infrastructure diagram"
  - "Doyak Package"
  - "TIPS"
  - "IR materials"
  - "investor materials"
  - "Startup Academy"
```

---

## 🎯 核心功能

### 1. 商业计划生成（政府资助项目）

为政府创业计划项目（如Doyak Package、TIPS、Early Startup Package、Startup Academy）自动生成商业计划书。

**支持的格式：**  
- ✅ Startup Doyak Package（通用/地区性）  
- ✅ TIPS（专注于研发）  
- ✅ Early Startup Package  
- ✅ Startup Academy  

**输出结构：**  
```
Cover
├─ Application & General Info
├─ Startup Item Overview & Commercialization Plan (Summary)
│   ├─ Problem Definition (Hook)
│   ├─ Solution (Product/Service)
│   ├─ Customer Cases (before/after numbers)
│   └─ Key Differentiators
├─ Market Analysis
│   ├─ TAM/SAM/SOM
│   ├─ Competitor Analysis
│   └─ Trends (McKinsey, Gartner citations)
├─ Business Model
│   ├─ Pricing Strategy
│   ├─ Unit Economics (CAC, LTV)
│   └─ Revenue Structure
├─ Tech Infrastructure (if applicable)
│   ├─ Architecture Diagram
│   ├─ Hardware Specs
│   └─ Cost Breakdown
├─ Team Composition
├─ Financial Plan (3 years)
│   ├─ Income Statement
│   ├─ Fund Execution Plan
│   └─ Break-Even Point (BEP)
└─ Roadmap (Phase 0~4)
```

**输出格式：**  
- HTML格式（优化适用于A4纸打印，包含`@media print`样式）  
- 可在浏览器中打开并转换为PDF  
- 包含图片插入指南（支持SVG、PNG、JPG格式的图片）  

---

### 2. 基础设施图谱生成  

为科技初创公司可视化基础设施架构。  

**生成的文件包括：**  
- **架构图谱**（基于ASCII艺术的文本格式，使用Mermaid工具生成）  
- **硬件规格对比**（Mac Mini、Raspberry Pi、Linux服务器、云服务器等选项）  
- **成本分解**（直接成本、间接成本、盈亏平衡点）  
- **网络拓扑结构**（VPN、防火墙、端口配置）  
- **安全检查清单**（FileVault加密、SSH安全、API密钥管理）  

**示例场景：**  
- Mupeng Box（基于Mac Mini M4 Pro的AI代理硬件）  
- 本地部署与云部署的对比  
- 产品线（基础版/专业版/企业版）  

**输出格式：**  
- Markdown格式（兼容GitHub和Notion）  
- Mermaid格式的图表（包括流程图和序列图）  
- ASCII表格  

---

### 3. 演示文稿生成（投资者推介材料）  

为投资者或加速器机构生成10-15页的演示文稿。  

**幻灯片结构：**  
```
1. Cover (Company name, one-liner)
2. Problem (Hook + field voices)
3. Solution (Product/service core)
4. Market Size (TAM/SAM/SOM, CAGR)
5. Product (Screenshots/demo/diagrams)
6. Business Model (Pricing, unit economics)
7. Traction (PMF signals, revenue, users)
8. Competitive Advantage (Moat, differentiation)
9. Team (Founders, key personnel)
10. Financials (3-year projections, break-even)
11. Roadmap (Milestones)
12. Ask (Funding needed, use, equity)
```

**故事讲述原则：**  
- **吸引注意力 → 解决疑问 → 产品/可视化展示 → 市场数据**  
- 避免重复使用相同的视觉元素  
- 强调“扩展性”（网络效应），而不仅仅是技术改进  

**输出格式：**  
- Markdown格式（按幻灯片分段）  
- 提供转换为Google Slides或PowerPoint的指南  

---

### 4. 迭代修订支持  

- **版本控制**：  
  - 文件路径：`projects/gov-support/doyak-v1.html` → `v2.html` → … → `v12.html`  
  - 使用`git diff`跟踪文件变更  
  - 重大变更记录在`CHANGELOG.md`文件中  

**反馈整合：**  
- 评审者的意见 → 修订方向建议  
- 根据投资者问题添加补充内容  
- 通过A/B测试比较不同版本的效果  

---

## 🧠 经验总结（从版本1到版本12的迭代过程）  

在开发Doyak Package商业计划书的过程中，我们总结了以下经验：  

### 故事讲述技巧：  
1. **遵循“吸引注意力 → 解决疑问 → 产品/可视化展示 → 市场数据”的顺序**  
   - 错误做法：直接从技术角度开始介绍（例如：“我们的技术使用了AI...”）  
   - 正确做法：先提出问题（例如：“为什么72%的用户在3个月内放弃了使用AI？”），然后展示解决方案。  

2. **避免重复使用相同的视觉元素**  
   - 评审者会对重复使用的视觉元素感到不满  
   - 为每个部分准备新的视觉素材。  

3. **强调“扩展性”**  
   - 不要只谈论技术的改进，要突出产品如何带来网络效应（例如：“客户A的使用体验 → 客户B的购买行为 → 从而增加整体价值”）。  

### 框架设计：  
4. **Mupengism = 苹果模式**  
   - OpenClaw相当于互联网（基础基础设施，开源技术）  
   - LLM（如Claude/GPT）相当于半导体（计算引擎）  
   - Mupengism则类似于苹果公司的生态系统（操作系统+应用商店+自有生态）  
   - **核心理念**：先建立坚实的基础，再在此基础上构建自有生态。  

5. **硬件是基础设施，而非销售对象**  
   - 错误做法：试图直接销售硬件设备（例如：“我们将机架出售给客户”）  
   - 正确做法：将硬件作为服务提供，例如“我们的机架是Skill Store的核心服务器，通过自有基础设施确保稳定的利润”。  

### 数据展示：  
6. **必须提供前后对比数据**  
   - 撰写销售数据：从2小时缩短到15分钟  
   - 发送300封邮件给风险投资机构：从1周缩短到2小时  
   - 社交媒体管理：从每天3小时自动化到完全自动化  
   - 信息解释时间减少了90%。  

7. **引用权威数据来源**  
   - McKinsey 2025年AI调查：72%的企业采用了AI技术，但其中72%在3个月内放弃了使用  
   - Gartner预测：到2028年，AI将在15%的决策中发挥作用  
   - MarketsandMarkets报告：AI代理市场规模从2025年的78.4亿美元增长到2030年的526亿美元（复合年增长率46%）  

---

## 📚 参考文件  

相关文件位于工作区相对路径下：  
```
$WORKSPACE/
├─ projects/gov-support/
│   ├─ doyak-v10-img.html (latest business plan HTML)
│   ├─ doyak-v10-img2.html
│   ├─ doyak-v10.html
│   └─ doyak-v11.pdf (final submission)
├─ memory/consolidated/
│   └─ doyak-business-plan.md (core memories)
├─ memory/
│   ├─ [DATE]-mupeng-box-infra.md (infrastructure design)
│   └─ [DATE]-assoai-pitchdeck.md (pitch deck example)
└─ memory/research/
    └─ [DATE]-ai-agent-market.md (market research)
```

---

## 🚀 使用方法  

### 触发关键词  

当用户请求以下内容时，工具会自动执行相应功能：  
- **商业计划书**  
- **演示文稿**  
- **基础设施图谱**  
- **Doyak Package**  
- **TIPS项目**  
- **投资者推介材料**  

### 命令示例  

#### 1. 生成商业计划书  

**生成流程：**  
1. 收集基本信息（公司名称、CEO信息、业务注册情况等）  
2. 读取参考文件（`doyak-business-plan.md`、市场研究资料）  
3. 根据`doyak-v10-img.html`模板生成商业计划书  
4. 添加图片插入指南  
5. 保存结果到`projects/gov-support/[公司名称]-v1.html`  
6. 提供浏览器打开指南  

#### 2. 生成基础设施图谱  

**生成流程：**  
1. 参考`mupeng-box-infra.md`文件  
2. 生成Mermaid格式的架构图和网络拓扑图  
3. 制作硬件规格对比表（Markdown格式）  
4. 保存结果到`projects/infra/[项目名称]-infra.md`  

#### 3. 生成演示文稿  

**生成流程：**  
1. 参考`assoai-pitchdeck.md`模板  
2. 撰写10-15页的Markdown格式演示文稿  
3. 应用故事讲述原则（吸引注意力 → 解决疑问 → 产品展示 → 数据展示）  
4. 使用具体的销售数据（TAM/SAM/SOM、CAC、LTV、BEP等指标）  
5. 保存结果到`projects/pitch/[公司名称]-pitchdeck.md`  

#### 4. 版本对比  

**执行步骤：**  
1. 阅读两个版本的文件，总结主要变化  
2. 展示各章节之间的差异  
3. 提出改进建议  

#### 5. 反馈整合  

**执行步骤：**  
1. 阅读现有的商业计划书  
2. 添加关于扩展性和市场策略的内容  
3. 生成新的版本（`v[N+1].html`）  
4. 总结所有变更内容  

---

## 📐 模板结构  

（HTML和Mermaid模板已包含在原始代码中，保持不变以确保技术准确性）  

---

## 🔧 技术栈  

本工具内部使用的工具包括：  
- **HTML生成**：Mustache/Handlebars模板引擎  
- **图表制作**：Mermaid和ASCII艺术工具  
- **版本控制**：Git diff逻辑  
- **PDF转换**：浏览器提供的打印API  
- **文件读写**：OpenClaw提供的读写和编辑工具  

---

## 📊 输出示例  

### 生成的文件结构  

### 事件日志  

新版本生成时，系统会记录事件日志：  
```json
{
  "event": "business_plan_created",
  "timestamp": "2026-02-14T08:06:00Z",
  "version": "v1",
  "file": "projects/gov-support/mycompany-v1.html",
  "company": "MyCompany",
  "type": "doyak-package",
  "changes": "Initial draft created"
}
```

日志文件位置：`events/business-plan-2026-02-14.json`  

---

## 🎓 学习资源  

**推荐阅读材料：**  
- **Doyak Package申请指南**：[K-Startup](https://www.k-startup.go.kr/)  
- **TIPS项目公告**：[TIPS Town](https://www.tipstown.or.kr/)  
- **Y Combinator演示文稿制作指南**：[YC Library](https://www.ycombinator.com/library/2u-how-to-build-your-seed-round-pitch-deck)  
- **McKinsey AI报告**：[McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)  

### 内部参考文件：  
- `memory/consolidated/doyak-business-plan.md`：版本1至版本12的迭代经验记录  
- `memory/2026-02-09-mupeng-box-infra.md`：基础设施设计案例  
- `memory/research/2026-02-14-ai-agent-market.md`：市场研究数据  

---

## 🐧 作者信息  

> 本工具由**무펭이**开发，属于[Mupengism](https://github.com/mupeng)生态体系的一部分  
> 创建日期：2026-02-14  
> 版本：1.0.0  
> 标签：#商业计划书 #演示文稿 #基础设施 #政府资助 #投资者推介  

---

## 🔄 更新日志  

| 版本 | 更新日期 | 主要变更内容 |  
|---------|------|---------|  
| 1.0.0 | 2026-02-14 | 初始版本发布，整合了从版本1到版本12的迭代经验 |  

---

**许可证**：MIT许可证  
**贡献方式**：欢迎在[github.com/mupeng/workspace/skills/business-planner](https://github.com/mupeng/workspace)提交Pull请求进行贡献。
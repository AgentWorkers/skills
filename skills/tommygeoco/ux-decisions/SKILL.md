---
name: ux-decisions
description: "Tommy Geoco开发的“Making UX Decisions”框架（uxdecisions.com）中包含了一项人工智能（AI）技能。该技能可用于辅助UI/UX设计决策、设计审核、设计模式选择、视觉层次结构分析以及设计完整性的审查。通过提供关于视觉风格、可访问性、社交验证、导航等方面的检查清单，该技能能够支持快速且富有针对性的界面设计工作。"
author: Tommy Geoco
homepage: https://uxdecisions.com
---

# 用户体验决策技能（UX Decisioning Skill）

这是一个基于 Tommy Geoco 的《Making UX Decisions》（uxdecisions.com）开发的全面 UI 设计决策框架，旨在帮助用户在竞争激烈、压力巨大的环境中快速、有目的地进行界面设计。

## 适用场景

- 在时间紧迫的情况下做出 UI/UX 设计决策  
- 结合业务背景评估设计上的权衡  
- 为特定问题选择合适的 UI 模式  
- 审查设计的完整性和质量  
- 为新界面构建设计思维框架  

## 核心理念  

**速度≠鲁莽。** 快速设计并不一定意味着鲁莽；只有缺乏深思熟虑的快速设计才算是鲁莽。关键在于设计过程中的意图性。  

## 快速决策的三大支柱  

1. **框架（Scaffolding）**：用于自动化重复性决策的规则  
2. **决策过程（Decisioning）**：用于制定新决策的流程  
3. **执行检查清单（Crafting）**：用于落实决策的检查清单  

## 快速参考结构  

### 基础框架  
- `references/00-core-framework.md`：三大支柱、决策工作流程、宏观决策策略  
- `references/01-anchors.md`：提升设计韧性的七大核心思维方式  
- `references/02-information-scaffold.md`：心理学、经济学、可访问性、默认设置等相关知识  

### 执行检查清单  
- `references/10-checklist-new-interfaces.md`：设计新界面的六步流程  
- `references/11-checklist-fidelity.md`：组件状态、交互方式、可扩展性、反馈机制  
- `references/12-checklist-visual-style.md`：间距、颜色、层次结构、排版、动画效果  
- `references/13-checklist-innovation.md`：创新程度的评估标准  

### 可复用设计模式  
- `references/20-patterns-chunking.md`：卡片、标签页、折叠窗格、分页、轮播图等设计模式  
- `references/21-patterns-progressive-disclosure.md`：工具提示、弹出窗口、抽屉式元素等设计模式  
- `references/22-patterns-cognitive-load.md`：逐步引导、向导、极简导航、简化表单等设计模式  
- `references/23-patterns-visual-hierarchy.md`：排版、颜色、空白间距、元素大小、布局关系等设计模式  
- `references/24-patterns-social-proof.md`：用户评价、用户生成内容（UGC）、徽章、社交功能集成等设计模式  
- `references/25-patterns-feedback.md`：进度条、通知、验证机制、上下文相关帮助等设计模式  
- `references/26-patterns-error-handling.md`：表单验证、撤销/重做功能、对话框、自动保存等设计模式  
- `references/27-patterns-accessibility.md`：键盘导航、ARIA 标准、替代文本、对比度设置、缩放功能等设计模式  
- `references/28-patterns-personalization.md`：仪表盘、自适应内容、个性化设置、多语言支持等设计模式  
- `references/29-patterns-onboarding.md`：引导流程、上下文提示、教程、检查清单等设计模式  
- `references/30-patterns-information.md`：路径导航、站点地图、标签分类、分面搜索等设计模式  
- `references/31-patterns-navigation.md`：优先级导航、隐藏式导航、固定导航栏、底部导航栏等设计模式  

## 使用说明  

### 对于设计决策  
1. 阅读 `00-core-framework.md` 以了解决策工作流程  
2. 判断当前决策是重复性的（使用框架）还是新出现的（使用相应流程）  
3. 采用三步评估方法：借鉴现有知识 → 评估用户熟悉度 → 进行深入研究  

### 对于新界面设计  
1. 遵循 `10-checklist-new-interfaces.md` 中的六步流程  
2. 查阅相关设计模式文档以获取具体组件的实现方法  
3. 使用质量检查清单和视觉风格检查清单来提升设计质量  

### 对于设计模式的选择  
1. 明确核心问题（如数据分组、信息展示方式、用户认知负担等）  
2. 查阅相关设计模式文档  
3. 评估该模式的优点、适用场景、心理学原理及实施指南  

## 决策工作流程总结  

面对 UI 设计决策时，请按照以下步骤进行：  
```
1. WEIGH INFORMATION
   ├─ What does institutional knowledge say? (existing patterns, brand, tech constraints)
   ├─ What are users familiar with? (conventions, competitor patterns)
   └─ What does research say? (user testing, analytics, studies)

2. NARROW OPTIONS
   ├─ Eliminate what conflicts with constraints
   ├─ Prioritize what aligns with macro bets
   └─ Choose based on JTBD support

3. EXECUTE
   └─ Apply relevant checklist + patterns
```  

## 宏观决策策略类别  

企业通过以下一种或多种策略取得成功：  

| 决策策略 | 描述 | 对设计的影响 |
|---------|---------|-------------------|
| **速度（Velocity）** | 更快地将功能推向市场 | 重用现有设计模式，借鉴其他领域的设计灵感 |
| **效率（Efficiency）** | 更好地管理资源浪费 | 设计高效的系统，减少未完成的工作量 |
| **准确性（Accuracy）** | 更频繁地做出正确决策 | 进行更深入的研究，使用有效的评估工具 |
| **创新（Innovation）** | 发现未被充分利用的潜力 | 采用新颖的设计模式，跨领域获取灵感 |

始终确保微观设计决策与公司整体战略保持一致。  

## 关键原则：良好的设计决策是相对的  

一个设计决策是否“良好”，取决于它是否：  
- 支持产品的核心功能  
- 与公司整体战略相契合  
- 兼顾时间、技术和团队资源等限制  
- 在用户熟悉度和差异化需求之间取得平衡  

不存在绝对正确的 UI 解决方案——只有适合特定情境的方案才是最佳选择。
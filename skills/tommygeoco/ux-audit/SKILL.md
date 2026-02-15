---
name: ux-audit
description: "**AI技能：自动化设计审核**  
该AI技能用于根据经过验证的用户体验（UX）原则来评估设计界面，涵盖视觉层次结构、可访问性、认知负荷、导航等方面。其设计理念源自Tommy Geoco所著的《Making UX Decisions》。"
author: Tommy Geoco
homepage: https://audit.uxtools.co
logo: logo-light.png
logoDark: logo-dark.png
---

# 设计审计技能

根据经过验证的用户体验（UX）原则来评估界面设计。本技能的依据是Tommy Geoco所著的《Making UX Decisions》（https://uxdecisions.com）。

## 适用场景

- 在时间压力下进行UI/UX设计决策时  
- 在结合业务背景评估设计权衡时  
- 为特定问题选择合适的UI模式时  
- 审查设计的完整性和质量时  
- 为新界面构建设计思维框架时  

## 核心理念  

**速度≠鲁莽。** 快速设计并不一定意味着鲁莽，但鲁莽地快速设计才是真正的鲁莽。关键在于设计的意图是否明确。  

## 快速决策的三大支柱  

1. **框架**：用于自动化重复性决策的规则  
2. **决策流程**：用于制定新决策的步骤  
3. **检查清单**：用于执行决策的工具  

## 快速参考结构  

### 基础框架  
- `references/00-core-framework.md`：三大支柱、决策工作流程、宏观设计策略  
- `references/01-anchors.md`：提升设计适应性的7种核心思维方式  
- `references/02-information-scaffold.md`：心理学、经济学、可访问性、默认设置  

### 检查清单（执行步骤）  
- `references/10-checklist-new-interfaces.md`：新界面设计的6步流程  
- `references/11-checklist-fidelity.md`：组件状态、交互方式、可扩展性、反馈机制  
- `references/12-checklist-visual-style.md`：间距、颜色、层次结构、排版、动态效果  
- `references/13-checklist-innovation.md`：创新程度的评估标准  

### 可复用的设计模式  
- `references/20-patterns-chunking.md`：卡片、标签页、折叠式布局、分页、轮播图  
- `references/21-patterns-progressive-disclosure.md`：工具提示、弹出窗口、抽屉式界面  
- `references/22-patterns-cognitive-load.md`：逐步引导、向导、极简导航、简化表单  
- `references/23-patterns-visual-hierarchy.md`：排版、颜色、空白间距、元素间距  
- `references/24-patterns-social-proof.md`：用户评价、用户生成内容（UGC）、徽章、社交功能集成  
- `references/25-patterns-feedback.md`：进度条、通知、验证机制、上下文相关帮助  
- `references/26-patterns-error-handling.md`：表单验证、撤销/重做功能、对话框、自动保存  
- `references/27-patterns-accessibility.md`：键盘导航、ARIA规范、替代文本、对比度设置、缩放功能  
- `references/28-patterns-personalization.md`：仪表盘、自适应内容、用户偏好设置、多语言支持  
- `references/29-patterns-onboarding.md`：引导流程、上下文相关提示、教程、检查清单  
- `references/30-patterns-information.md`：路径导航、站点地图、标签分类、分面搜索  
- `references/31-patterns-navigation.md`：优先级导航、非页面内导航元素、固定导航栏、底部导航栏  

## 使用说明  

### 对于设计决策  
1. 阅读`00-core-framework.md`以了解决策工作流程。  
2. 判断该决策是否属于重复性任务（使用框架），或是否为新决策（使用相应流程）。  
3. 采用三步评估方法：参考公司战略、用户习惯、现有研究结果。  

### 对于新界面设计  
1. 按照`10-checklist-new-interfaces.md`中的6步流程进行设计。  
2. 查阅相关设计模式文档以获取具体组件的实现建议。  
3. 使用质量检查清单（如`fidelity`和`visual-style`）来提升设计质量。  

### 模式选择  
1. 明确核心问题（如数据分组、信息逐步展示、用户认知负担等）。  
2. 查阅相关设计模式文档。  
3. 评估该模式的优点、适用场景、心理学依据及实施指南。  

## 决策工作流程总结  

面对UI设计决策时，请遵循以下步骤：  
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

## 宏观设计策略  

企业的成功往往依赖于以下策略之一或多个：  

| 策略 | 描述 | 对设计的影响 |
|-----|-------------|-------------------|  
| **速度** | 更快地将功能推向市场 | 重用现有设计模式，借鉴其他领域的设计灵感 |  
| **效率** | 更好地管理资源浪费 | 优化系统设计，减少未完成的工作量 |  
| **准确性** | 更频繁地做出正确决策 | 加强研究，使用专业工具辅助决策 |  
| **创新** | 发现未被充分利用的潜力 | 采用新颖的设计模式，跨领域汲取灵感 |  

始终确保微观设计决策与公司整体战略保持一致。  

## 关键原则：好的设计决策是相对的  

一个设计决策被认为是“好的”，当它：  
- 支持产品的核心功能需求；  
- 与公司整体战略相契合；  
- 兼顾时间、技术和团队资源等限制；  
- 在用户熟悉度和差异化需求之间取得平衡。  

不存在绝对正确的UI解决方案——只有适合特定情境的方案。  

---

## 生成审计报告  

收到审计请求时，需生成一份全面的报告。报告中必须包含以下内容：  

### 必需包含的部分  
1. **视觉层次结构**：标题、呼叫动作（CTA）、内容分组、阅读顺序、字体大小、颜色搭配、空白间距  
2. **视觉风格**：间距一致性、颜色使用、层次感、排版效果、动态效果  
3. **可访问性**：键盘导航、焦点显示、对比度设置、屏幕阅读器支持、触控交互  

### 根据需求补充的部分  
4. **导航系统**：多页面应用的导航方式、路径导航、菜单结构、信息架构  
5. **可用性**：交互流程的易用性（发现功能、反馈机制、错误处理）、用户认知负担  
6. **新用户引导**：新用户的使用流程、教程、信息逐步展示  
7. **社交验证**： landing页面/营销内容的用户评价、信任信号、社交功能集成  
8. **表单设计**：数据输入的格式、验证机制、错误提示、字段类型  

### 审计报告格式  

```json
{
  "title": "Design Name — Screen/Flow",
  "project": "Project Name",
  "date": "YYYY-MM-DD",
  "figma_url": "optional",
  "screenshot_url": "optional - URL to screenshot",
  
  "macro_bets": [
    { "category": "velocity|efficiency|accuracy|innovation", "description": "...", "alignment": "strong|moderate|weak" }
  ],
  
  "jtbd": [
    { "user": "User Type", "situation": "context without 'When'", "motivation": "goal without 'I want to'", "outcome": "benefit without 'so I can'" }
  ],
  
  "visual_hierarchy": {
    "title": "Visual Hierarchy",
    "checks": [
      { "label": "Check name", "status": "pass|warn|fail|na", "notes": "Details" }
    ]
  },
  "visual_style": { ... },
  "accessibility": { ... },
  
  "priority_fixes": [
    { "rank": 1, "title": "Fix title", "description": "What and why", "framework_reference": "XX-filename.md → Section Name" }
  ],
  
  "notes": "Optional overall observations"
}
```  

### 各部分的评估标准（每部分建议评估6-10项）  

**视觉层次结构**：标题的清晰度、主要操作的明确性、内容分组、阅读顺序、字体大小、颜色搭配、空白间距  
**视觉风格**：间距一致性、颜色使用规范、层次感/阴影效果、排版系统、边框/圆角设置  
**可访问性**：键盘操作的便利性、焦点显示效果、颜色对比度（4.5:1）、触控交互的可用性  
**导航系统**：当前位置的清晰显示、菜单行为的可预测性、路径导航的可用性  
**可用性**：功能的易发现性、操作反馈机制、错误预防措施、用户认知负担的管理
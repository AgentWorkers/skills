---
name: ui-audit
description: "**AI技能：自动化UI审计**  
该AI技能用于根据经过验证的用户体验（UX）原则来评估用户界面，涵盖视觉层次结构、可访问性、认知负荷、导航等方面。其评估依据是Tommy Geoco所著的《Making UX Decisions》一书中的相关内容。"
author: Tommy Geoco
homepage: https://audit.uxtools.co
logo: logo-light.png
logoDark: logo-dark.png
---

# UI 审计技能

根据经过验证的用户体验（UX）原则来评估用户界面。本技能的依据是 Tommy Geoco 的著作 [《Making UX Decisions》（https://uxdecisions.com）。

## 适用场景

- 在时间压力下进行 UI/UX 设计决策时  
- 在结合业务背景评估设计权衡时  
- 为特定问题选择合适的 UI 模式时  
- 审查设计的完整性和质量时  
- 为新界面构建设计思维框架时  

## 核心理念  

**速度 ≠ 鲁莽。** 快速设计并不一定意味着鲁莽；只有那些草率、不负责任地快速设计才算鲁莽。关键在于设计背后的意图。  

## 快速决策的三大支柱  

1. **框架**（Scaffolding）——用于自动化重复性决策的规则  
2. **决策流程**（Decisioning）——用于制定新决策的过程  
3. **执行检查清单**（Crafting）——用于执行决策的清单  

## 快速参考结构  

### 基础框架  
- `references/00-core-framework.md` — 三大支柱、决策工作流程、宏观设计策略  
- `references/01-anchors.md` — 七种提升设计韧性的基本思维方式  
- `references/02-information-scaffold.md` — 心理学、经济学、可访问性、默认设置  

### 执行检查清单  
- `references/10-checklist-new-interfaces.md` — 设计新界面的六步流程  
- `references/11-checklist-fidelity.md` — 组件状态、交互方式、可扩展性、反馈机制  
- `references/12-checklist-visual-style.md` — 间距、颜色、层次感、排版、动画效果  
- `references/13-checklist-innovation.md` — 原创性的五个层次  

### 可复用的设计模式  
- `references/20-patterns-chunking.md` — 卡片、标签页、折叠式菜单、分页、轮播图  
- `references/21-patterns-progressive-disclosure.md` — 工具提示、弹出窗口、抽屉式元素  
- `references/22-patterns-cognitive-load.md` — 分步引导、向导、极简导航、简化表单  
- `references/23-patterns-visual-hierarchy.md` — 排版、颜色、空白间距、元素间距  
- `references/24-patterns-social-proof.md` — 用户评价、用户生成内容（UGC）、徽章、社交功能集成  
- `references/25-patterns-feedback.md` — 进度条、通知、验证机制、上下文相关帮助  
- `references/26-patterns-error-handling.md` — 表单验证、撤销/重做功能、对话框、自动保存  
- `references/27-patterns-accessibility.md` — 键盘导航、ARIA 标准、替代文本、对比度设置、缩放功能  
- `references/28-patterns-personalization.md` — 仪表盘、自适应内容、用户偏好设置、多语言支持  
- `references/29-patterns-onboarding.md` — 新手引导、上下文相关提示、教程、检查清单  
- `references/30-patterns-information.md` — 路径导航、站点地图、标签分类、分面搜索  
- `references/31-patterns-navigation.md` — 优先级导航、非页面内导航元素、固定导航栏、底部导航栏  

## 使用说明  

### 对于设计决策  
1. 阅读 `00-core-framework.md` 以了解决策工作流程。  
2. 判断这是重复性决策（使用框架）还是新决策（使用相应流程）。  
3. 采用三步评估方法：借鉴现有知识 → 考虑用户熟悉度 → 进行深入研究。  

### 对于新界面  
1. 遵循 `10-checklist-new-interfaces.md` 中的六步流程。  
2. 查阅相关设计模式文档以获取具体组件的实现建议。  
3. 使用可读性和视觉风格检查清单来提升设计质量。  

### 模式选择  
1. 明确核心问题（如数据分组、信息逐步展示、用户认知负担等）。  
2. 查阅相应的设计模式文档。  
3. 评估该模式的优点、适用场景、心理学依据及实施指南。  

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

## 宏观设计策略类别  

企业通过以下策略之一或多个策略取得成功：  

| 策略 | 描述 | 设计影响 |  
|-----|-------------|-------------------|  
| **速度** | 更快地将功能推向市场 | 重用现有设计模式，借鉴其他领域的设计理念 |  
| **效率** | 更好地管理资源浪费 | 设计高效的系统，减少未完成的工作量 |  
| **准确性** | 更频繁地做出正确决策 | 进行更深入的研究，使用专业工具辅助决策 |  
| **创新** | 发现未被充分利用的潜力 | 采用新颖的设计模式，借鉴跨领域经验 |  

始终确保微观设计策略与公司整体战略保持一致。  

## 关键原则：良好的设计决策是相对的  

一个设计决策是否“良好”，取决于它是否：  
- 支持产品的核心功能；  
- 与公司整体战略相契合；  
- 符合时间、技术和团队等限制条件；  
- 在用户熟悉度和差异化需求之间取得平衡。  

不存在绝对正确的 UI 解决方案——只有适合特定情境的方案。  

---

## 生成审计报告  

当收到审计请求时，需生成一份全面的报告。报告中必须包含以下内容：  

### 必需包含的部分  
1. **视觉层次结构**（Visual Hierarchy）：标题、呼叫行动按钮（CTA）、内容分组、阅读流程、字体大小、颜色搭配、空白间距  
2. **视觉风格**（Visual Style）：间距一致性、颜色使用、层次感、排版样式、动画效果  
3. **可访问性**（Accessibility）：键盘导航、焦点显示、对比度设置、屏幕阅读器支持、触控交互  

### 根据需求包含的补充部分  
4. **导航系统**（Navigation）：多页面应用的导航方式、路径导航、菜单结构、信息架构  
5. **可用性**（Usability）：交互流程的易用性、反馈机制、错误处理方式、用户认知负担  
6. **新手引导**（Onboarding）：新用户的入门体验、教程设计、信息逐步展示  
7. **社交证明**（Social Proof）： landing 页面或营销内容中的用户评价、信任信号、社交功能集成  
8. **表单设计**（Forms）：数据输入的标签设计、验证机制、错误提示、字段类型  

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

### 各部分的检查要点（每部分建议检查 6–10 项）  

**视觉层次结构**：  
- 标题的清晰度  
- 主要操作按钮的易识别性  
- 内容的分组与布局  
- 阅读流程的合理性  
- 字体大小的统一性  
- 颜色搭配的合理性  
- 空白间距的合理性  

**视觉风格**：  
- 间距的一致性  
- 颜色调色的合理性  
- 元素的层次感和阴影效果  
- 排版系统的合理性  
- 图标样式的一致性  
- 动画效果的合理性  

**可访问性**：  
- 键盘操作的便捷性  
- 焦点的可见性  
- 颜色对比度（4.5:1）  
- 触控目标的可用性  
- 替代文本的准确性  
- 语义化的标记使用  
- 动画效果的合理性  

**导航系统**：  
- 当前位置的清晰显示  
- 菜单行为的可预测性  
- 路径导航的可用性  
- 搜索功能的易用性  
- 移动设备的导航体验  

**可用性**：  
- 功能的易发现性  
- 用户操作的反馈机制  
- 错误的预防措施  
- 用户认知负担的管控  
- 页面加载状态的显示  

---
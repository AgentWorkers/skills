---
name: ima-knowledge-ai
version: 1.0.4
category: knowledge
author: IMA Studio (imastudio.com)
keywords: imastudio, knowledge, workflow, model selection, visual consistency, video modes, parameter guide, 知识库, 工作流, 模型选择, IMA, 图像视频音乐, SeeDream, Midjourney, Suno, Kling, Veo, Sora
description: >
  **AI内容创作的关键知识库：在进行任何图像/视频/音乐生成任务之前，请先阅读本文档。**  
  本文档为AI内容创作提供了专家级的指导，涵盖工作流程设计、模型选择、参数优化、视觉一致性、角色设计以及制作最佳实践等方面。在使用 ima-image-ai、ima-video-ai、ima-voice-ai、ima-all-ai 或其他媒体生成工具（如 ai-image-generation、ai-video-gen、suno-music 等）之前，阅读本文档是必不可少的。  
  **应用场景：**  
  - 规划工作流程  
  - 选择合适的模型  
  - 优化提示和参数设置  
  - 确保角色/风格的一致性  
  - 实现多轮生成（多shot production）  
  - 避免常见错误  
  **核心价值：**  
  - 将初学者的尝试转化为专业级别的成果  
  **注意：**  
  本文档提供的是策略性指导，并非具体的API调用方法。
---
# IMA知识AI

> **用途**：本技能提供战略性的知识，帮助用户在使用IMA Studio的内容创作API时做出更好的决策。它本身并不直接调用API，而是指导您更有效地使用`ima-voice-ai`、`ima-image-ai`和`ima-video-ai`等工具。

## 何时使用本技能

在调用任何`ima-*ai`技能之前，请先阅读本技能，如果您需要以下方面的指导：
- **工作流程设计**：如何将复杂的用户需求分解为具体的任务
- **模型选择**：根据任务需求选择合适的模型
- **参数优化**：如何设置参数以平衡质量、成本和速度

**示例场景**：
- 用户：“帮我制作一个宣传视频” → 先阅读`workflow-design.md`
- 用户：“使用最好的模型生成内容” → 阅读`model-selection.md`来选择合适的模型
- 用户：“生成16:9比例的图片” → 阅读`parameter-guide.md`了解相关的参数设置

---

## 知识结构

所有知识文件都存储在`references/`目录下。在引用其他技能的内容时，请使用以下路径：
`ima-knowledge-ai/references/workflow-design.md` 或 `~/.openclaw/skills/ima-knowledge-ai/references/<filename>.md`

本技能包含**12个知识模块**（8个独立模块 + 4个模块化目录）：

### 核心知识（1-8）

### 1. [workflow-design.md](references/workflow-design.md)
**阅读时机**：需要将复杂用户需求分解为具体任务时
- 任务分解策略
- 依赖关系识别（例如：脚本 → 配音 → 视频）
- 多步骤工作流程模板
- 常见的内容创作模式

### 2. [model-selection.md](references/model-selection.md)
**阅读时机**：需要在多个模型中选择适合任务的模型时
- 模型功能对比表（图像/视频/语音）
- 成本与质量的权衡
- 使用场景推荐（预算型/平衡型/高级型）
- 模型的限制及解决方法

### 3. [parameter-guide.md](references/parameter-guide.md)
**阅读时机**：需要为特定任务优化参数时
- 分辨率/宽高比设置指南
- 质量与速度的权衡
- 常见问题及解决方法
- 参数兼容性表格

### 4. [visual-consistency.md](references/visual-consistency.md) ⭐ **新内容**
**阅读时机**：涉及系列图像/视频生成、角色或场景时
- 为什么AI生成的图像/视频通常缺乏视觉一致性
- 如何识别隐性的视觉一致性要求
- 参考图像的工作流程（图像到图像 / 视频到视频）
- 多次拍摄的连贯性策略
- 常见问题及最佳实践

### 5. [video-modes.md](references/video-modes.md) ⭐⭐ **重要**
**阅读时机**：进行任何视频生成任务时（在使用`ima-video-ai`之前必须阅读）
- `image_to_video`与`reference_image_to_video`的区别（概念不同！）
- `image_to_video`：将输入的第一帧转换为视频
- `reference_image_to_video`：根据参考图像调整视频内容（可以更换场景）
- 传统两步法与现代一步法的工作流程
- 主要方法失败时的备用策略
- 常见问题及解决方法

### 6. [long-video-production.md](references/long-video-production.md) 🎬 **长视频制作必备**
**阅读时机**：用户需要制作超过15秒的视频（如30秒的广告、1分钟的短片或3分钟的宣传片）
- 为什么模型通常只能生成10-15秒的视频
- 多次拍摄功能（一次生成中可以使用2-4个拍摄角度）
- 三步工作流程：脚本 → 拍摄镜头 → 编辑/拼接
- 视觉素材准备（角色、场景、道具）
- 分镜头生成策略
- 视频编辑和拼接技巧
- 完整案例研究：1分钟长的奇幻短片

### 7. [character-design.md](references/character-design.md) 🎨 **角色设计 / IP开发**
**阅读时机**：用户需要角色设计、IP开发或游戏/动画相关素材时
- 角色设计行业概述（游戏、动画、漫画、IP）
- 参考驱动的工作流程（基础参考 → 变体设计）
- 反馈表（正面/侧面/背面/3-4个视角）
- 表情库（快乐/愤怒/悲伤/惊讶等）
- 服装变体（休闲装/盔甲/礼服）
- 道具和武器的参考图片
- 动作姿势（静止/行走/攻击等）
- 完整案例研究：RPG游戏角色“Aria”

### 8. [vi-design.md](references/vi-design.md) 🏢 **VI设计 / 品牌识别**
**阅读时机**：用户需要VI设计、品牌识别或Logo应用相关内容时
- VI（视觉识别）系统概述
- 基础系统（Logo / 颜色 / 字体 / 辅助图形）
- 应用系统（办公室 / 商店 / 包装 / 广告 / 数字 / 制服）
- 参考驱动的工作流程（基础设计 → 应用设计）
- Logo的一致性要求
- 颜色调色板管理（主要颜色 / 辅助颜色 / 中性颜色）
- 完整案例研究：“Morning Light Coffee”咖啡店的VI设计（20多个输出文件）

### 9. [best-practices/](references/best-practices/) ⭐⭐⭐ **商业模板（按需提供）**
**阅读时机**：进行商业广告或艺术摄影任务时

**结构**：索引 + 4个场景文件（仅加载所需内容）
- `README.md`：包含关键词索引（2 KB）
- `jewelry.md`：珠宝及配饰类商业广告（3 KB）
- `skincare.md`：护肤品及化妆品类商业广告（3 KB）
- `perfume.md`：香水及香氛类商业广告（3 KB）
- `cinematic-art.md`：电影风格的艺术摄影（4 KB）

**使用方法**：先阅读索引，然后仅加载相关的场景文件

**节省资源**：与加载所有场景相比，可节省60-85%的文件大小

### 10. [color-theory/](references/color-theory/) 🎨 **色彩理论与文化敏感性**
**阅读时机**：任何需要选择颜色的设计任务时（如Logo、海报、品牌、产品）

**结构**：索引 + 7个模块化文件（仅加载所需内容）
- `README.md`：包含快速导航的索引（5 KB）
- `color-psychology.md`：11种主要颜色的心理学及其应用（12 KB） ⭐
- `color-combinations.md`：5种颜色搭配原则（2 KB）
- `industry-guide.md`：10个行业的颜色偏好（1 KB）
- `cultural-differences.md`：5个地区的颜色差异（1 KB）
- `global-regions.md`：4个地区的详细指南（4 KB）
- `religious-systems.md`：5种主要宗教的色彩象征（5 KB）
- `application-strategy.md`：IMA Studio的色彩决策流程（2 KB）

**使用方法**：阅读索引后，根据任务需求加载相应的模块

**节省资源**：与加载所有32 KB的文件相比，可节省70-90%的文件大小

### 11. [design-pitfalls/](references/design-pitfalls/) 🚫 **避免的设计错误**
**阅读时机**：在最终交付前需要确保生成内容的质量时

**结构**：索引 + 4个场景文件（涵盖29种常见设计错误）

- `README.md`：包含5条核心原则的索引（3 KB）
- `logo-design.md`：Logo设计中的常见错误（10条规则）（7 KB）
- `poster-banner.md`：海报/横幅设计中的常见错误（8条规则）（5 KB）
- `product-ecommerce.md`：产品及电子商务设计中的常见错误（6条规则）（3 KB）
- `web-ui.md`：网页界面设计中的常见错误（5条规则）（3 KB）

**使用方法**：阅读索引后，仅加载与特定场景相关的错误信息

**节省资源**：与加载所有21 KB的文件相比，可节省60-80%的文件大小

### 12. [color-trends-2026/](references/color-trends-2026/) 📅 **2026年色彩趋势**
**阅读时机**：需要为2026年的设计任务了解最新色彩趋势时

**结构**：索引 + 5个按时间/地区分类的文件（根据当前月份和目标地区选择文件）
- `README.md`：包含时间分类的索引（6 KB）
- `annual-colors.md`：Pantone Cloud Dancer / WGSN Teal / China Horse Red（4 KB）
- `spring-summer.md`：3月至8月的流行颜色（Cobalt Blue, Violet, Bright Pink）（2 KB）
- `fall-winter.md`：9月至2月的流行颜色（Dark Luxury主题）（1 KB）
- `regional-differences.md`：中国/美国/东南亚地区的色彩差异（2 KB）
- `industry-applications.md`：科技/时尚/食品/家居行业的色彩应用（1 KB）

**使用方法**：阅读索引后，根据当前季节和目标地区选择相应的文件

**节省资源**：与加载所有16 KB的文件相比，可节省75-90%的文件大小

**自动加载策略**：系统会自动检测当前月份，并加载相应的季节文件

---

## 使用流程示例

```
User Request
  ↓
[ima-knowledge-ai] Query relevant knowledge
  ↓
Make informed decision
  ↓
[ima-*-ai] Execute API call with optimized parameters
  ↓
Success!
```

**示例流程**：
```
User: "帮我生成一张16:9的产品海报，要高质量"

Step 1: Read ima-knowledge-ai → parameter-guide.md
        → Learn: SeeDream 4.5 supports 16:9, Nano Banana Pro native support
        
Step 2: Read ima-knowledge-ai → model-selection.md
        → Choose: Nano Banana Pro 4K (best quality, 18pts)
        
Step 3: Call ima-image-ai with:
        --model-id gemini-3-pro-image
        --extra-params '{"aspect_ratio": "16:9", "size": "4K"}'
        
Step 4: Success! 🎉
```

---

## 重要说明

1. **本技能不能替代`ima-*ai`技能**  
   在执行任务前，请将其作为参考工具使用。

2. **本技能基于IMA Studio 2026年2月27日的API版本**  
   模型和参数可能会更新，请随时通过`list-models`进行验证。

3. **成本透明度**  
   所有建议都包含相关费用信息，以便用户做出决策。

4. **本技能不包含实现脚本**  
   仅提供理论知识，具体实现由`ima-*ai`技能完成。

---

## 快速参考

| 需求 | 需要阅读的文件 |
|------|-----------|
| “如何分解复杂的任务？” | `workflow-design.md` |
| “应该使用哪个模型？” | `model-selection.md` |
| “如何设置分辨率/宽高比？” | `parameter-guide.md` |
| “费用有什么差异？” | `model-selection.md` |
| “为什么我的参数设置被忽略了？” | `parameter-guide.md` |
| “如何确保图像/视频的视觉一致性？” ⭐ | `visual-consistency.md` |
| “如何生成多个相同主题的图像/视频？” | `visual-consistency.md` |
| “`image_to_video`与`reference_image_to_video`有什么区别？” ⭐⭐ | `video-modes.md` |
| “应该使用哪种视频模式？” | `video-modes.md` |
| “用户需要制作30秒以上的视频/短片/广告？” 🎬 | `long-video-production.md` |
| “如何在10秒的限制下制作1分钟以上的视频？” | `long-video-production.md` |
| “一次生成中可以使用2-4个拍摄角度？” 🆕 | `long-video-production.md` |
| “角色设计/IP开发？” 🎨 | `character-design.md` |
| “需要角色设计或IP相关素材？” | `character-design.md` |
| “需要反馈表或表情库？” | `character-design.md` |
| “如何保持角色的一致性？” | `character-design.md` |
| “VI设计/品牌识别/Logo应用？” 🏢 | `vi-design.md` |
| “咖啡店/餐厅/零售品牌的VI设计？” | `vi-design.md` |
| “名片/菜单/包装/标识的设计？” | `vi-design.md` |
| “如何确保品牌的一致性？” | `vi-design.md` |
| “珠宝广告/护肤品广告/香水广告？” ⭐⭐⭐ | `best-practices/`（先阅读索引） |
| “商业广告模板？” | `best-practices/jewelry\|skincare\|perfume.md` |
| “电影风格的艺术摄影？” | `best-practices/cinematic-art.md` |
| “科技/时尚/食品品牌应该使用什么颜色？” 🎨 | `color-theory/`（根据行业选择相关模块） |
| “色彩心理学（红色/蓝色/绿色）？” | `color-theory/color-psychology.md` |
| “中国/印度/中东地区的色彩敏感性？” | `color-theory/`（文化相关内容） |
| “Logo设计中应该避免哪些错误？” 🚫 | `design-pitfalls/logo-design.md` |
| “海报/产品/网页设计中的常见错误？” | `design-pitfalls/`（先阅读索引） |
| “2026年的色彩趋势？” 📅 | `color-trends-2026/`（根据季节选择文件） |
| “春季/夏季与秋季/冬季的色彩对比？” | `color-trends-2026/spring-summer\|fall-winter.md` |
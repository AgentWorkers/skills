---
name: ima-knowledge-ai
description: >
  IMA Studio内容创作知识库提供了工作流程设计、模型选择以及参数优化方面的指导。适用场景包括：  
  1. 在规划多步骤的IMA内容创作工作流程时，需要将用户需求分解为可执行的任务；  
  2. 在选择ima-voice-ai、ima-image-ai或ima-video-ai模型时，根据任务需求获取相应的推荐方案；  
  3. 为特定使用场景优化生成参数（如分辨率、宽高比、质量、成本等）；  
  4. 在调用任何IMA-*-ai相关功能之前，确保遵循最佳实践并避免常见错误。  
  该知识库提供的是战略性的指导，而非具体的API调用说明。
---
# IMA知识AI

> **用途**：本技能提供战略性的知识，帮助用户在使用IMA Studio的内容创建API时做出更好的决策。它本身并不直接调用API，而是指导您更有效地使用`ima-voice-ai`、`ima-image-ai`和`ima-video-ai`等工具。

## 何时使用本技能

在调用任何`ima-*ai`技能之前，请先阅读本技能文件，如果您需要以下方面的指导：

1. **工作流程设计**：如何将复杂的用户请求分解为具体的任务
2. **模型选择**：根据任务需求选择合适的模型
3. **参数优化**：如何设置参数以平衡质量、成本和速度

**示例场景**：
- 用户：“帮我制作一个宣传视频” → 先阅读`workflow-design.md`
- 用户：“使用最好的模型生成内容” → 阅读`model-selection.md`来选择合适的模型
- 用户：“生成16:9比例的图片” → 阅读`parameter-guide.md`以了解相关的参数设置

---

## 知识结构

本技能包含8个参考文件：

### 1. [workflow-design.md](references/workflow-design.md)
**阅读时机**：需要将复杂用户请求分解为具体任务时
- 任务分解策略
- 依赖关系识别（例如：脚本 → 配音 → 视频）
- 多步骤工作流程模板
- 常见的内容创建模式

### 2. [model-selection.md](references/model-selection.md)
**阅读时机**：在多个模型中选择适合任务的模型时
- 模型功能对比表（图像/视频/语音）
- 成本与质量的权衡
- 使用场景推荐（预算型/平衡型/高级型）
- 模型的限制及解决方法

### 3. [parameter-guide.md](references/parameter-guide.md)
**阅读时机**：针对特定任务优化参数设置时
- 分辨率/宽高比设置指南
- 质量与速度的权衡
- 常见问题及解决方法
- 参数兼容性表格

### 4. [visual-consistency.md](references/visual-consistency.md) ⭐ **新文件**
**阅读时机**：涉及系列图像/视频生成、角色或场景时
- 为什么AI生成的图像/视频默认缺乏视觉一致性
- 如何识别隐性的视觉一致性要求
- 参考图像生成流程（图像到图像/视频到视频）
- 多次拍摄的连贯性策略
- 常见问题及最佳实践

### 5. [video-modes.md](references/video-modes.md) ⭐⭐ **重要文件**
**阅读时机**：进行任何视频生成任务时（在使用`ima-video-ai`之前必须阅读）
- `image_to_video`与`reference_image_to_video`的区别（概念不同！）
- `image_to_video`：将输入图像转换为视频的第一帧
- `reference_image_to_video`：根据参考图像生成视频（可以改变场景）
- 传统的两步流程与现代的一步流程
- 主要方法失败时的备用方案
- 常见问题及解决方法

### 6. [long-video-production.md](references/long-video-production.md) 🎬 **长视频制作必备**
**阅读时机**：用户需要制作超过15秒的视频（如30秒的广告、1分钟的短片或3分钟的宣传片）
- 为什么模型生成的视频长度通常限制在10-15秒内
- 多次拍摄功能（一次生成时可以使用2-4个角度）
- 三步工作流程：脚本 → 拍摄镜头 → 编辑/拼接
- 视觉素材准备（角色、场景、道具）
- 分镜头生成策略
- 视频编辑和拼接技巧
- 完整案例研究：1分钟长的奇幻短片

### 7. [character-design.md](references/character-design.md) 🎨 **角色设计/IP开发**
**阅读时机**：用户需要角色设计、IP开发或游戏/动画素材时
- 角色设计行业概述（游戏、动画、漫画、IP）
- 参考驱动的工作流程（参考图像 → 变体设计）
- 角色设计成果文件（正面/侧面/背面/3-4个视角）
- 表情库（快乐/愤怒/悲伤/惊讶等）
- 服装变体（休闲装/盔甲/礼服）
- 道具和武器的参考图像
- 动作姿势（静止/行走/攻击等）
- 完整案例研究：RPG游戏角色“Aria”

### 8. [vi-design.md](references/vi-design.md) 🏢 **VI设计/品牌识别**
**阅读时机**：用户需要VI设计、品牌识别或Logo应用时
- VI（视觉识别）系统概述
- 基础系统（Logo / 颜色 / 字体 / 辅助图形）
- 应用系统（办公室/商店/包装/广告/数字/制服）
- 参考驱动的工作流程（基础设计 → 应用设计）
- Logo的一致性要求
- 颜色调色板管理（主要颜色/辅助颜色/中性色/功能性颜色）
- 完整案例研究：“Morning Light Coffee”咖啡店的VI设计（包含20多个设计成果）

### 9. [best-practices/](references/best-practices/) ⭐⭐⭐ **商业广告模板（按需提供）**
**阅读时机**：进行商业广告或艺术摄影任务时

**结构**：索引 + 4个场景文件（仅加载所需内容）
- `README.md`：包含关键词索引（2 KB）
- `jewelry.md`：珠宝及配饰类商业广告（3 KB）
- `skincare.md`：护肤及化妆品类商业广告（3 KB）
- `perfume.md`：香水类商业广告（3 KB）
- `cinematic-art.md`：电影风格的艺术摄影（4 KB）

**使用方法**：先阅读索引，然后仅加载相关的场景文件

**节省资源**：相比加载所有文件，可节省60-85%的带宽
- Logo的一致性要求
- 颜色调色板管理
- 完整案例研究：“Morning Light Coffee”咖啡店的VI设计（包含20多个设计成果）

---

## 使用模式

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
   在执行任务前，请将其作为参考指南使用。

2. **本技能基于IMA Studio API（2026-02-27版）的知识编写**  
   模型和参数可能会更新，请随时通过`list-models`命令进行确认。

3. **成本透明度**  
   所有建议均包含相关费用信息，以便用户做出决策。

4. **本技能不包含任何实现脚本**  
   仅提供理论知识，具体实现由`ima-*ai`技能完成。

---

## 快速参考

| 需要帮助的内容 | 需要阅读的文件 |
|------------|-------------------|
| “如何分解复杂的任务？” | `workflow-design.md` |
| “应该使用哪个模型？” | `model-selection.md` |
| “如何设置分辨率/宽高比？” | `parameter-guide.md` |
| “费用有什么差异？” | `model-selection.md` |
| “为什么我的参数设置被忽略了？” | `parameter-guide.md` |
| “如何确保图像/视频的视觉一致性？” | **`visual-consistency.md`** |
| “如何生成系列图像或多个相同主题的镜头？” | **`visual-consistency.md`** |
| “`image_to_video`与`reference_image_to_video`有什么区别？” | **`video-modes.md`** |
| “应该使用哪种视频生成模式？” | **`video-modes.md`** |
| “用户需要超过15秒的视频/短片/广告？” | **`long-video-production.md`** |
| “如何在10秒的限制下制作1分钟以上的视频？” | **`long-video-production.md`** |
| “一次生成时需要使用2-4个角度的镜头？” | **`long-video-production.md`** |
| “角色设计/IP开发？” | **`character-design.md`** |
| “需要角色设计或游戏/动画素材？” | **`character-design.md`** |
| “需要角色设计成果文件或表情库？” | **`character-design.md`** |
| “如何保持角色的一致性？” | **`character-design.md`** |
| “VI设计/品牌识别/Logo应用？” | **`vi-design.md`** |
| “咖啡店/餐厅/零售品牌的VI设计？” | **`vi-design.md`** |
| “名片/菜单/包装/标识的设计？” | **`vi-design.md`** |
| “如何确保品牌的一致性？” | **`vi-design.md`** |
| “珠宝广告/护肤广告/香水广告？” | **`best-practices/`**（请先阅读索引文件） |
| **商业广告模板？” | **`best-practices/jewelry|skincare|perfume.md`** |
| **电影风格的艺术摄影？” | **`best-practices/cinematic-art.md`** |

---

**最后更新时间**：2026-03-03  
**版本**：1.0.1  
**维护者**：IMA Studio技能团队
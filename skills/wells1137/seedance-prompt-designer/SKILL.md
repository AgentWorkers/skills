---
name: seedance-prompt-designer
description: 智能分析用户提供的多模态资产（如图像、音频、视频等）以及用户的创作意图，从而为 Seedance 2.0 模型生成最优化的、结构化的视频生成提示。
version: 2.0.0
author: wells1137
tags: [video, generation, prompt, seedance, multimodal]
---
# Seedance Prompt Designer 技能

该技能能够将用户分散的多模态资产（图片、视频、音频）以及模糊的创意意图转化为结构化、可执行的提示，用于 Seedance 2.0 视频生成模型。它充当专家级提示工程师的角色，确保模型输出的最高质量。

## 核心工作流程

该技能遵循严格的三阶段工作流程。每个阶段的输出都是下一阶段的输入。

| 阶段 | 目标 | 关键操作 | 输出 |
| :--- | :--- | :--- | :--- |
| **1. 识别** | 理解用户输入 | 解析意图、分析资产、为资产添加标签 | `recognition_output.json` |
| **2. 映射与策略** | 设计可执行的参考策略 | 确定最佳的参考方法（文本、资产、混合方式） | `strategy_output.json` |
| **3. 构建与组装** | 生成最终的完整提示 | 组合文本、添加 @-语法、参考模板 | `final_prompt.json` |

## 使用示例

**用户请求：**“让《蒙娜丽莎》喝可乐。我希望效果具有电影感，就像一个特写镜头。”
*用户上传 `monalisa.png` 和 `coke.png`*

**代理的内部处理过程：**
1. **识别**：识别出 `action_intent`（“喝可乐”）和 `style_intent`（“电影感，特写”），并将 `monalisa.png` 标记为 `Subject Identity`，将 `coke.png` 标记为 `Subject Identity-Object`。
2. **映射与策略**：决定使用 `@monalisa` 和 `@coke` 作为资产引用，其余部分作为文本提示。
3. **构建与组装**：生成最终的提示。

**最终输出：**
```json
{
  "final_prompt": "A cinematic close-up shot of a woman picking up a bottle of Coke and taking a sip. The scene is lit with dramatic, high-contrast lighting. Use @monalisa as the subject reference, and the object appearing in the video is @coke.",
  "recommended_parameters": {
    "duration": 8,
    "aspect_ratio": "16:9"
  }
}
```

## 知识库

该技能依赖于内部知识库来做出明智的决策。代理在执行过程中必须查阅以下文件：

- **`/references/atomic_element_mapping.md`**：核心知识。包含“资产类型 -> 原子元素”以及“原子元素 -> 最佳参考方法”的映射表。**必须在第 1 阶段和第 2 阶段查阅**。
- **`/references/seedance_syntax_guide.md`**：Seedance 2.0 的 `@asset_name` 语法参考。**必须在第 3 阶段查阅，以确保语法正确**。
- **`/references/prompt_templates.md`**：针对不同类型（如电影、产品展示、叙事）的高级提示模板。第 3 阶段可选择性查阅，以增强提示的风格。
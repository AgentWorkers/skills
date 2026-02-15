---
name: brand-analyzer
description: 分析品牌以生成全面的品牌身份资料（JSON格式）。适用于用户需要分析品牌、创建品牌资料或为广告制作获取品牌数据的情况。这些资料可存储在Ad-Ready、Morpheus及其他创意工作流程中供重复使用。同时支持列出现有品牌资料并进行更新。
---

# 品牌分析器：AI品牌身份评估工具

使用Gemini Flash和Google搜索数据，分析任何品牌并生成详细的品牌身份JSON档案。

## 概述

品牌分析器通过以下步骤创建结构化的品牌身份档案：
1. **通过Google搜索**研究品牌（包括官方信息、营销活动及视觉形象）；
2. **分析**品牌的行为特征、视觉风格和语言风格；
3. **根据标准模板生成**完整的JSON档案；
4. **将档案存储**以便在所有创意工作中重复使用。

## 使用场景

- 当用户请求“分析品牌”或“创建品牌档案”时；
- 在品牌尚未被收录到Ad-Ready目录中时；
- 当用户提到某个尚无档案的品牌时；
- 用于更新/刷新现有的品牌档案。

## 快速命令

### 分析品牌并保存到文件
```bash
GEMINI_API_KEY="$KEY" uv run {baseDir}/scripts/analyze.py \
  --brand "Brand Name" \
  --output ./brands/Brand_Name.json
```

### 分析品牌并自动保存到Ad-Ready品牌目录
```bash
GEMINI_API_KEY="$KEY" uv run {baseDir}/scripts/analyze.py \
  --brand "Heredero Gin" \
  --auto-save
```

`--auto-save`选项会自动将结果保存到`~/clawd/ad-ready/configs/Brands/{Brand_Name}.json`文件中。

### 打印到标准输出（stdout）
```bash
GEMINI_API_KEY="$KEY" uv run {baseDir}/scripts/analyze.py --brand "Nike"
```

## 输入参数

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| `--brand` | ✅ | 需要分析的品牌名称 |
| `--output` | 可选 | 输出文件路径（默认：stdout） |
| `--auto-save` | 可选 | 是否自动保存到Ad-Ready品牌目录 |
| `--api-key` | 可选 | Gemini API密钥（或设置`GEMINI_API_KEY`环境变量） |

## 输出格式

生成的JSON文件遵循Ad-Ready使用的标准品牌身份模板：

```json
{
  "brand_info": { "name", "tagline", "category", "positioning", "vision", "mission", "origin_story" },
  "brand_values": { "core_values", "brand_promise", "differentiators", "non_negotiables" },
  "target_audience": { "demographics", "psychographics" },
  "tone_of_voice": { "personality_traits", "communication_style", "language_register", ... },
  "visual_identity": { "logo", "color_system", "typography", "layout_principles" },
  "photography": { "style", "technical" },
  "campaign_guidelines": { "visual_tone", "model_casting", "product_presentation", ... },
  "brand_behavior": { "do_dont", "immutability" },
  "channel_expression": { "retail", "digital", "print" },
  "compliance": { ... }
}
```

## 与其他工作流程的集成

### Ad-Ready
在生成广告时，品牌档案会自动作为`brand_profile`选项提供。

### Morpheus时尚设计
品牌视觉形象（颜色、摄影风格、语言风格）可为Morpheus的营销活动提供参考。

### 自定义工作流程
可以加载任何品牌档案的JSON数据，以提取视觉形象、语言风格或营销指南，用于各种创意任务。

## 分析方法

该分析器采用三阶段分析方法：

### 第一阶段：官方信息研究（通过Google搜索）
- 查看品牌官网、企业页面及官方宣传资料；
- 确定品牌的名称、成立时间、定位、愿景、使命和口号等核心信息。

### 第二阶段：营销活动研究（通过Google搜索）
- 通过Google Images和Pinterest查找品牌的广告活动；
- 识别出10个以上的不同营销活动作为分析参考。

### 第三阶段：视觉分析
- 对品牌视觉元素进行交叉分析；
- 确定重复出现的摄影风格、色彩体系及排版元素；
- 填补官方资料中未涵盖的视觉信息。

## API密钥

该工具使用Gemini API。密钥的设置方式如下：
- 通过`GEMINI_API_KEY`环境变量配置；
- 或使用`--api-key`命令行参数。
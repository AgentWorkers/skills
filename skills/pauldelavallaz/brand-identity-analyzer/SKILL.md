---
name: brand-analyzer
description: 分析品牌以生成全面的品牌身份资料（JSON格式）。当用户需要分析某个品牌、创建品牌资料或获取用于广告制作的品牌数据时，可以使用该功能。这些品牌资料会被存储起来，以便在Ad-Ready、Morpheus及其他创意工作流程中重复使用。同时，系统支持列出现有的品牌资料并进行更新。
---

# 品牌分析器：AI品牌身份剖析工具

使用Gemini Flash和Google搜索数据，分析任意品牌并生成全面的品牌身份JSON档案。

## 概述

品牌分析器通过以下步骤创建结构化的品牌身份档案：
1. **通过Google搜索**研究品牌（包括官方信息、营销活动及视觉标识）；
2. **分析**品牌的行为特征、视觉风格、摄影风格及语言风格；
3. **根据标准模板生成**完整的JSON档案；
4. **将档案存储**以便在所有创意工作中重复使用。

## 使用场景

- 当用户请求“分析品牌”或“创建品牌档案”时；
- 在品牌信息尚未录入Ad-Ready系统之前；
- 当用户提到某个尚未建立档案的品牌时；
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

`--auto-save`选项会自动将档案保存到`~/clawd/ad-ready/configs/Brands/{Brand_Name}.json`路径下。

### ⚠️ 强制要求：每次生成新档案后必须立即推送至GitHub

**每次生成并保存新品牌档案后，都必须立即将其推送至GitHub。**这一步骤是必须的——ComfyDeploy部署系统会从GitHub仓库中获取品牌档案。

```bash
cd ~/clawd/ad-ready
git add configs/Brands/{Brand_Name}.json
git commit -m "Add brand profile: {Brand Name}"
git push origin main
```

请勿跳过此步骤。ComfyDeploy的广告生成流程需要仓库中的品牌档案才能正常运行。

### 打印到标准输出（stdout）
```bash
GEMINI_API_KEY="$KEY" uv run {baseDir}/scripts/analyze.py --brand "Nike"
```

## 输入参数

| 参数 | 是否必填 | 说明 |
|-------|----------|-------------|
| `--brand` | ✅ | 需要分析的品牌名称 |
| `--output` | 可选 | 输出文件路径（默认：标准输出） |
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

### Morpheus时装设计
品牌视觉标识（颜色、摄影风格、语言风格）可为Morpheus的营销活动提供参考。

### 自定义工作流程
可以加载任何品牌档案的JSON数据，以提取视觉标识、语言风格或营销指导信息，用于各种创意任务。

## 分析方法

该分析工具采用三阶段分析方法：

### 第一阶段：官方信息研究（通过Google搜索）
- 查看品牌官网、企业页面及官方宣传资料；
- 确定品牌的名称、成立时间、定位、愿景、使命及口号等核心信息。

### 第二阶段：营销活动研究（通过Google搜索）
- 通过Google Images和Pinterest查找品牌的广告活动；
- 识别出10个以上的不同营销活动；
- 将这些活动作为分析参考资料。

### 第三阶段：视觉分析
- 对品牌的视觉元素进行综合分析；
- 确定重复出现的摄影风格、色彩体系及排版元素；
- 填补官方资料中未涵盖的视觉标识信息。

## API密钥

该工具使用Gemini API。密钥的设置方式如下：
- 通过`GEMINI_API_KEY`环境变量设置；
- 或者使用`--api-key`命令行参数。
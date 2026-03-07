---
name: content-type-router
description: 根据文本描述或输出类型提示，检测并确定应使用的正确视觉内容类型（如首页图片、海报、信息图等）。当需要将内容生成请求分类为具有布局规则、视觉模式和生成提示的结构化类型时，请使用此功能。
metadata: {"category": "content-routing", "tags": ["content-type", "routing", "image-generation", "classification", "layout"], "runtime": "python"}
---
# 内容类型路由器

将内容生成请求分类为结构化的内容类型配置，该配置提供了布局规则、视觉模式约束、排版规则以及用于下游图像生成的提示。

## 概述

该路由器将自然语言描述（以及可选的行业/类型提示）映射到4个类别中的17种预定义内容类型配置：

| 类别 | 类型名称 |
|----------|-------|
| `product_focused` | `hero_shot`（产品特写）、`lifestyle_shot`（生活方式场景）、`flat_lay`（平铺展示）、`detail_closeup`（细节特写）、`scale_shot`（尺寸参考）、`unboxing`（开箱展示） |
| `typography_heavy` | `poster`（海报）、`sale_promo`（促销海报）、`countdown`（倒计时）、`quote_graphic`（品牌语录图）、`announcement`（公告） |
| `educational` | `infographic`（信息图）、`comparison_chart`（对比图表）、`process_howto`（操作指南）、`carousel_educational`（教育类轮播图） |
| `social_proof` | `testimonial_graphic`（客户评价图）、`before_after`（前后对比图）、`ugc_repost`（用户生成内容） |

## 视觉模式

每种内容类型都有三种视觉模式，用于确定文本的处理方式：

| 模式 | 类型名称 | 文本处理方式 |
|------|------|----------|
| **Pure Visual**（纯视觉） | 图像上无文本——仅包含摄影、构图和光线效果 |
| **Educational**（教育类） | 允许少量文本（数据标签、步骤说明）——占图像面积的35%以内 |
| **CTA**（呼叫行动） | 必须包含文本——包含标题、正文和呼叫行动按钮 |

## 内容类型参考

### 以产品为中心的内容类型（`Pure Visual`）

- **`hero_shot`**：产品在简洁背景上展示，突出产品特点
  - 焦点：图像中心 | 占图像面积的60-80% | 背景：白色或渐变色 |
  - 提示：使用摄影棚灯光，无需道具，遵循Amazon/Shopify的拍摄标准

- **`lifestyle_shot`**：产品在真实场景中展示，体现产品使用场景
  - 焦点：遵循三分法则 | 占图像面积的30-50% | 背景：与产品相关的场景 |
  - 提示：使用自然光线，营造真实氛围，注重故事性表达

- **`flat_lay`：多个产品以平铺方式展示
  - 焦点：图像中心 | 占图像面积的65-75% | 摄影角度：俯视（90°） |
  - 提示：展示3-12个产品，使用统一的色调，合理利用负空间

- **`detail_closeup`：通过特写镜头展示产品的细节和工艺
  - 焦点：图像中心 | 占图像面积的80-95% | 使用微距镜头 |
  - 提示：使用浅景深效果，突出产品的优质材质

- **`scale_shot`：产品与尺寸参考物一起展示
  - 焦点：图像中心 | 占图像面积的40-70% | 参考物可以是手或其他常见物品

- **`unboxing`：展示产品包装，展现产品的外观设计
  - 焦点：图像中心 | 占图像面积的50-80% | 营造出期待或高端的产品氛围 |

### 以排版为主的内容类型（`cta`）

- **`poster`：包含标题和图片的设计海报
  - 文本区域：覆盖在图片上 | 使用的字体包括标题和正文 | 标题最多7个单词

- **`sale_promo`：包含折扣/优惠信息的促销海报
  - 文本区域：醒目位置 | 必须包含一个呼叫行动按钮 | 文本区域最多占图像面积的35%

- **`countdown`：带有倒计时元素的限时促销海报
  - 文本区域：位于图像中心 | 使用紧急提示语言 | 必须包含日期和时间信息

- **`quote_graphic`：品牌语录或客户评价的图片
  - 文本区域：位于图像中心 | 只显示一条语录 | 配备少量辅助说明

- **announcement`：产品发布或新闻公告的图片
  - 文本区域：结构化排列 | 信息层次结构为：新闻 > 详情 > 呼叫行动按钮

### 教育类内容类型（`educational`）

- **`infographic`：包含标签的数据可视化图表
  - 文本：包含标签和数据点 | 文本区域最多占图像面积的35% | 有清晰的视觉层次结构

- **comparison_chart`：并排展示多个选项的对比图表
  - 布局：分为多个部分 | 必须包含标签 | 明确区分不同选项

- **process_howto`：分步操作的可视化指南
  - 布局：按步骤顺序展示 | 建议包含3-7个步骤

- **carousel_educational`：多帧组成的教育类系列图片
  - 各帧风格一致 | 逐步展示信息

### 以社交证明或教育类内容类型（`cta`或`educational`）

- **`testimonial_graphic`：带有来源标注的客户评价图片
  - 必须包含评价文本和客户姓名/联系方式 | 可选包含产品图片

- **before_after`：展示产品使用前后的对比图片
  - 布局分为两部分 | 明确标注“之前”和“之后” | 对比效果明显

- **ugc_repost`：为品牌重新发布的用户生成内容
  - 保持内容的真实性 | 最小限度地使用品牌元素 | 必须标注内容来源

## 检测API

### Python使用示例

```python
from content_types.registry import (
    detect_content_type,
    get_content_type_config,
    get_industry_content_types,
    get_content_types_by_visual_mode,
    get_content_types_by_category,
    get_all_content_types,
)
from content_types.base import VisualMode

# Detect from description
slug, confidence = detect_content_type(
    description="I need a product shot on white background for Amazon",
    industry="ecommerce",
)
# → ("hero_shot", 0.95)

# Get full config with layout rules and generation hints
config = get_content_type_config(slug)
prompt_context = config.to_prompt_context()  # Inject into LLM prompt
negative_prompts = config.get_negative_prompt_string()  # For image gen

# Industry-based recommendations
types = get_industry_content_types("beauty")
# → [HeroShot, BeforeAfter, FlatLay]

# Filter by visual mode
pure_visual_types = get_content_types_by_visual_mode(VisualMode.PURE_VISUAL)

# Filter by category
product_types = get_content_types_by_category("product_focused")
```

### 检测逻辑

1. 如果`output_type`与某个类型名称完全匹配，则置信度为1.0
2. 对所有注册的内容类型进行关键词匹配评分
3. 根据匹配情况计算综合得分（多次匹配会获得额外加分）
4. 如果置信度低于0.3，则使用该行业的默认类型配置
5. 最终的 fallback（备用方案）是`lifestyle_shot`

### 检测结果返回

```python
(slug: str, confidence: float)
# confidence: 0.0-1.0
# 0.3+ = usable, 0.7+ = high confidence
```

## `ContentTypeConfig` 结构

```python
@dataclass
class ContentTypeConfig:
    name: str                          # Human-readable name
    slug: str                          # Machine key: "hero_shot"
    category: str                      # "product_focused" | "typography_heavy" | etc.
    definition: str                    # One-line definition for LLM context
    visual_mode: VisualMode            # PURE_VISUAL | EDUCATIONAL | CTA
    layout: LayoutRules                # Focal point, coverage, background, camera angle
    typography: Optional[TypographyRules]  # Headline words, weight, CTA rules
    generation_hints: List[str]        # Positive requirements for image gen prompt
    negative_prompts: List[str]        # What to avoid (comma-joined for diffusion)
    detection_keywords: List[str]      # Keyword matching corpus
    common_industries: List[str]       # Industry affinity
    aspect_ratios: List[str]           # Recommended ratios: ["4:5", "1:1"]
```

## `LayoutRules` 结构

```python
@dataclass
class LayoutRules:
    focal_point: str           # "center" | "upper_third" | "rule_of_thirds" | "left" | "right"
    text_zone: Optional[str]   # "bottom_40_percent" | "top_20_percent" | "overlay" | None
    subject_coverage_min: float  # Min % of frame for main subject
    subject_coverage_max: float  # Max % of frame for main subject
    text_area_max: float       # Max % of frame for text (0.0 = no text)
    logo_zone: str             # "corner" | "bottom_center" | "none"
    whitespace_min: float      # Minimum negative space target
    camera_angle: Optional[str]  # "eye_level" | "overhead" | "low_angle" | "macro"
    background: Optional[str]  # "white" | "gradient" | "contextual" | "lifestyle"
```

## 行业默认内容类型

| 行业 | 常见内容类型 |
|----------|---------------------|
| 旅游 | `poster`（海报）、`lifestyle_shot`（生活方式场景）、`carousel_educational`（教育类轮播图） |
| 数字技术产品 | `hero_shot`（产品特写）、`lifestyle_shot`（生活方式场景）、`ugc_repost`（用户生成内容） |
| 时尚 | `lifestyle_shot`（生活方式场景）、`flat_lay`（平铺展示）、`ugc_repost`（用户生成内容） |
| 美妆 | `hero_shot`（产品特写）、`before_after`（前后对比图）、`flat_lay`（平铺展示） |
| 食品 | `flat_lay`（平铺展示）、`lifestyle_shot`（生活方式场景）、`process_howto`（操作指南） |
| SaaS服务 | `infographic`（信息图）、`comparison_chart`（对比图表）、`testimonial_graphic`（客户评价图） |
| 奢侈品 | `hero_shot`（产品特写）、`detail_closeup`（细节特写）、`lifestyle_shot`（生活方式场景） |
| 健康产品 | `before_after`（前后对比图）、`testimonial_graphic`（客户评价图）、`infographic`（信息图） |

## 数据库支持

该系统支持基于数据库的内容类型配置（可根据品牌进行定制）：

```bash
export USE_DB_CONTENT_TYPES=true  # Enable DB mode
```

当数据库支持时，内容类型会从`content_types` Supabase表中加载，并允许根据品牌进行个性化设置。如果数据库出现错误，系统会回退到代码中定义的默认类型配置。

```python
# Invalidate cache after DB updates
from content_types.registry import invalidate_cache
invalidate_cache()

# Enable/disable at runtime
from content_types.registry import enable_db_mode
enable_db_mode(True)
```

## 集成方式

将上述配置信息注入到图像生成过程中：

```python
slug, confidence = detect_content_type(description, industry=industry)
config = get_content_type_config(slug)

# Build generation prompt
system_context = config.to_prompt_context()
negative = config.get_negative_prompt_string()

# Pass to image generation
generate_image(
    prompt=f"{system_context}\n\n{user_prompt}",
    negative_prompt=negative,
    aspect_ratio=config.aspect_ratios[0],
)
```
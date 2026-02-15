---
name: video-ad-deconstructor
version: 1.0.0
description: 使用 Gemini AI 将视频广告创意分解为多个营销维度，提取出广告中的关键元素，如吸引用户的点（hooks）、社交证明（social proof）、行动号召（CTAs）、目标受众信息、能够引发情感共鸣的元素（emotional triggers）、以及用于营造紧迫感的策略（urgency tactics）等。该工具适用于分析竞争对手的广告、制定创意策划书，或深入了解广告效果背后的原因。
---

# 视频广告分析工具

该工具利用人工智能技术，将视频广告内容分解为可操作的营销洞察。

## 该工具的功能

- **生成摘要**：提取产品信息、功能、目标受众以及呼吁行动（CTA）内容。
- **分析营销要素**：识别广告中的关键元素，如吸引注意力的视觉元素、文字内容、用户评价等。
- **支持多种内容类型**：适用于消费品广告和游戏广告的分析。
- **进度跟踪**：支持长时间分析过程的回调功能。
- **JSON输出**：提供结构化数据，便于后续处理。

## 设置

### 1. 环境变量

```bash
# Required for Gemini
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### 2. 依赖项

```bash
pip install vertexai
```

## 使用方法

### 基本广告分析

```python
from scripts.deconstructor import AdDeconstructor
from scripts.models import ExtractedVideoContent
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="your-project-id", location="us-central1")
gemini_model = GenerativeModel("gemini-1.5-flash")

# Create deconstructor
deconstructor = AdDeconstructor(gemini_model=gemini_model)

# Create extracted content (from video-ad-analyzer or manually)
content = ExtractedVideoContent(
    video_path="ad.mp4",
    duration=30.0,
    transcript="Tired of messy cables? Meet CableFlow...",
    text_timeline=[{"at": 0.0, "text": ["50% OFF TODAY"]}],
    scene_timeline=[{"timestamp": 0.0, "description": "Person frustrated with tangled cables"}]
)

# Generate summary
summary = deconstructor.generate_summary(
    transcript=content.transcript,
    scenes="0.0s: Person frustrated with tangled cables",
    text_overlays="50% OFF TODAY"
)
print(summary)
```

### 全面广告分析

```python
# Deconstruct all marketing dimensions
def on_progress(fraction, dimension):
    print(f"Progress: {fraction*100:.0f}% - Analyzed {dimension}")

analysis = deconstructor.deconstruct(
    extracted_content=content,
    summary=summary,
    is_gaming=False,  # Set True for gaming ads
    on_progress=on_progress
)

# Access dimensions
for dimension, data in analysis.dimensions.items():
    print(f"\n{dimension}:")
    print(data)
```

## 输出结构

### 摘要输出

```
Product/App: CableFlow Cable Organizer

Key Features:
Magnetic design: Keeps cables organized automatically
Universal fit: Works with all cable types
Premium materials: Durable silicone construction

Target Audience: Tech users frustrated with cable management

Call to Action: Order now and get 50% off
```

### 分析结果输出

```python
{
    "spoken_hooks": {
        "elements": [
            {
                "hook_text": "Tired of messy cables?",
                "timestamp": "0:00",
                "hook_type": "Problem Question",
                "effectiveness": "High - directly addresses pain point"
            }
        ]
    },
    "social_proof": {
        "elements": [
            {
                "proof_type": "User Count",
                "claim": "Over 1 million happy customers",
                "credibility_score": 7
            }
        ]
    },
    # ... more dimensions
}
```

## 分析的营销要素

| 要素        | 分析内容                         |
|------------|--------------------------------------------|
| `spoken_hooks`  | 广告中的口头引导语                         |
| `visual_hooks`  | 吸引注意力的视觉元素                         |
| `text_hooks`  | 屏幕上的文字内容                         |
| `social_proof`  | 用户评价、观看次数等社交证明                   |
| `urgency_scarcity` | 限时优惠、库存提醒等紧迫感元素             |
| `emotional_triggers` | 情感触发因素（恐惧、欲望、归属感等）             |
| `problem_solution` | 产品解决的问题                         |
| `cta_analysis` | 呼吁行动（CTA）的有效性分析                 |
| `target_audience`  | 广告的目标受众                         |
| `unique_mechanism` | 产品的独特卖点                         |

## 自定义分析参数

在 `prompts/marketing_analysis.md` 文件中编辑参数，以自定义以下内容：

- 需要分析的营销要素
- 输出格式
- 评分标准
- 重点分析的对象（消费品广告或游戏广告）

## 常见问题解答

- “这个广告使用了哪些吸引注意力的元素？”
- “这个广告的情感诉求是什么？”
- “这个广告是如何营造紧迫感的？”
- “这个广告的目标受众是谁？”
- “广告中展示了哪些社交证明？”
- “分析一下竞争对手的广告。”
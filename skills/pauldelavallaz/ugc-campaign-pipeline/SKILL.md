---
name: ugc-campaign-pipeline
description: |
  Complete UGC video campaign pipeline: product → hero image → variations → videos → edited final.
  
  ✅ USE WHEN:
  - User says "crear campaña UGC" or "pipeline completo"
  - Need end-to-end UGC video production
  - Starting from product image/URL → final edited video
  - Want the full Doritos-style workflow
  
  ❌ DON'T USE WHEN:
  - Just need one step (use individual skills)
  - Already have final videos, just editing → use Remotion
  - Only need images, no video → use Morpheus only
  
  OUTPUT: Edited MP4 video with multiple scenes + subtitles + logo
---

# 用户生成内容（UGC）营销活动流程

这是一个从产品素材创建UGC风格宣传视频的完整工作流程。

## 流程概述

```
┌─────────────────────────────────────────────────────────────────────┐
│                     UGC CAMPAIGN PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  STEP 1: HERO IMAGE                                                  │
│  ├─ Input: Product image + model selection                          │
│  ├─ Tool: morpheus-fashion-design                                    │
│  └─ Output: ~/clawd/outputs/{project}/morpheus/hero.png             │
│                                                                      │
│  STEP 2: VARIATIONS                                                  │
│  ├─ Input: Hero image                                                │
│  ├─ Tool: multishot-ugc                                              │
│  └─ Output: ~/clawd/outputs/{project}/multishot/*.png (10 images)   │
│                                                                      │
│  STEP 3: SELECTION                                                   │
│  ├─ Analyze all 11 images                                            │
│  ├─ Criteria: variety, no errors, lip-sync friendly                  │
│  └─ Output: 4 best images selected                                   │
│                                                                      │
│  STEP 4: SCRIPT                                                      │
│  ├─ Write 4-scene dialogue script                                    │
│  ├─ Format: PURE DIALOGUE (no annotations)                           │
│  └─ Output: 4 lines of dialogue                                      │
│                                                                      │
│  STEP 5: UGC VIDEOS                                                  │
│  ├─ Input: 4 images + 4 script lines                                 │
│  ├─ Tool: veed-ugc (run 4 times)                                     │
│  └─ Output: ~/clawd/outputs/{project}/ugc/*.mp4 (4 videos)          │
│                                                                      │
│  STEP 6: FINAL EDIT                                                  │
│  ├─ Input: 4 videos + logo                                           │
│  ├─ Tool: Remotion                                                   │
│  ├─ Add: subtitles, transitions, logo ending                         │
│  └─ Output: ~/clawd/outputs/{project}/final/video.mp4               │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 执行检查清单

### 开始前
- [ ] 已收到产品图片
- [ ] 已知晓品牌/产品名称
- [ ] 明确目标受众
- [ ] 确定了语言风格（随意、专业或充满活力）

### 第一步：主角图片选择（Morpheus）
```bash
# Select model from catalog
cat ~/clawd/models-catalog/catalog/catalog.json | jq '[.talents[] | select(.gender == "male/female") | {id, name, ethnicity}]'

# Generate hero image
COMFY_DEPLOY_API_KEY="..." uv run ~/.clawdbot/skills/morpheus-fashion-design/scripts/generate.py \
  --product "product.jpg" \
  --model "models-catalog/catalog/images/model_XX.jpg" \
  --brief "..." \
  --target "..." \
  --aspect-ratio "9:16" \
  --output "~/clawd/outputs/{project}/morpheus/hero.png"
```

### 第二步：多角度图片拍摄
```bash
COMFY_DEPLOY_API_KEY="..." uv run ~/.clawdbot/skills/multishot-ugc/scripts/generate.py \
  --image "~/clawd/outputs/{project}/morpheus/hero.png" \
  --output-dir "~/clawd/outputs/{project}/multishot" \
  --resolution "2K" \
  --aspect-ratio "9:16"
```

### 第三步：图片筛选标准
分析所有11张图片，确保：
- ✅ 脸部清晰可见（正面或3/4侧面）
- ✅ 嘴部未被遮挡
- ✅ 手指/手部没有变形
- ✅ 产品清晰可见
- ✅ 与其他选定的图片有所不同

从这些图片中选出4张符合以下条件的图片：
1. 拍摄角度或视角不同
2. 适合进行对口型同步
3. 无任何质量问题

### 第四步：编写剧本
编写4行纯对话内容：
```
ESCENA 1: [Opening hook - grab attention]
ESCENA 2: [Problem/benefit - relate to audience]  
ESCENA 3: [Feature highlight - specific value]
ESCENA 4: [CTA/brand mention - close strong]
```

**规则：**
- 仅使用纯对话
- 不允许添加注释（如“兴奋”、“（停顿）”、“*微笑*”等）
- 不允许添加舞台指示或语气提示
- 仅记录人物实际说的话

### 第五步：视频制作（使用VEED工具）
```bash
for i in 1 2 3 4; do
  COMFY_DEPLOY_API_KEY="..." uv run ~/.clawdbot/skills/veed-ugc/scripts/generate.py \
    --image "selected_image_$i.png" \
    --script "Script line $i" \
    --output "~/clawd/outputs/{project}/ugc/escena$i.mp4"
done
```

### 第六步：最终剪辑
创建一个Remotion项目，包含：
- 所有4个视频片段
- 每个场景的动画字幕
- 结尾处的品牌标志动画
- 将视频渲染为最终的MP4格式

---

## 根据行业分类的剧本模板

### 食品/零食
```
Escena 1: Che, tenés que probar esto.
Escena 2: [Sabor/textura highlight]. Te pega de una.
Escena 3: Y mirá, no es solo [feature], tiene ese gustito que te deja queriendo más.
Escena 4: [Brand + Product]. Una vez que arrancás, no parás.
```

### 科技/小工具
```
Escena 1: Mirá lo que me llegó.
Escena 2: Esto cambia todo. [Key feature].
Escena 3: Y lo mejor? [Secondary benefit].
Escena 4: [Brand]. Ya no vuelvo atrás.
```

### 美容/护肤品
```
Escena 1: Ok, necesito contarte algo.
Escena 2: Este [producto] es increíble. [Result].
Escena 3: Lo uso hace [tiempo] y mirá la diferencia.
Escena 4: [Brand]. Tu piel te lo va a agradecer.
```

### 时尚
```
Escena 1: Encontré mi nueva obsesión.
Escena 2: Mirá este [prenda]. [Quality/style].
Escena 3: Combina con todo y es súper [comfort/style].
Escena 4: [Brand]. Estilo sin esfuerzo.
```

---

## 输出文件结构

```
~/clawd/outputs/{project}/
├── morpheus/
│   └── hero.png              # Original hero image
├── multishot/
│   ├── 1_00001_.png          # 10 variations
│   ├── 2_00001_.png
│   └── ...
├── ugc/
│   ├── escena1.mp4           # Individual scene videos
│   ├── escena2.mp4
│   ├── escena3.mp4
│   └── escena4.mp4
├── assets/
│   └── logo.png              # Brand logo
└── final/
    └── video.mp4             # Final edited video
```

---

## 交付前的质量检查标准

- [ ] 主角图片：产品清晰可见，模特表现自然
- **多角度图片**：选出的4张图片各具特色，适合进行对口型同步
- **剧本**：符合品牌语言风格，采用纯对话格式
- **视频**：对口型同步效果良好，无瑕疵
- **最终成品**：字幕清晰可见，过渡流畅，品牌标志显示完整
- **音频**：语音质量清晰，播放节奏自然
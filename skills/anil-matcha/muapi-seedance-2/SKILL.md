---
slug: muapi-seedance-2
name: muapi-seedance-2
version: "0.1.0"
description: Seedance 2.0（字节跳动）中的“Expert Cinema Director”技能：利用先进的摄像语法和多模态参考技术，实现高保真度的视频生成。支持文本转视频、图片转视频以及视频扩展功能。
acceptLicenseTerms: true
---
# 🎬 Seedance 2.0 电影专家

**这是一款专为“导演级”AI视频制作设计的工具。**  
Seedance 2.0 并不是一个描述性模型，而是一个**指令性模型**。它对技术性的电影摄影技巧、物理规则以及精确的摄像语法反应最为敏感。

## 核心能力

1. **文本转视频（Text-to-Video, t2v）**：使用 `seedance-v2.0-t2v` 根据导演的描述生成电影风格的视频。  
2. **图像转视频（Image-to-Video, i2v）**：使用 `seedance-v2.0-i2v` 将 1 至 9 张参考图像制作成视频。  
3. **视频扩展（Video Extension）**：使用 `seedance-v2.0-extend` 无缝地续接现有的 Seedance 2.0 视频。  
4. **多模态参考（Multimodal Referencing）**：利用 `@tag` 系统（如 `@image1`、`@video1`）来统一风格、动作和节奏。  
5. **音视频同步（Audio-Visual Sync）**：生成与视觉动作同步的高保真音效。  
6. **时间一致性（Temporal Consistency）**：确保不同镜头中角色、服装和环境的稳定性。

---

## 🏗️ 技术规范：导演指令（Director Brief）

为了获得专业化的结果，请务必按照以下层次结构来构建指令：

| 组件 | 指令类型 | 示例 |
| :--- | :--- | :--- |
| **场景（Scene）** | 环境 + 照明 | “一条被雨水浸湿的赛博朋克街道，湿漉漉的沥青路上反射着洋红色的霓虹灯。” |
| **主体（Subject）** | 身份特征 + 细节 | “一位穿着黑色风衣的女性，眼神坚定，皮肤具有电影般的质感。” |
| **动作（Action）** | 流畅的动作表现 | “她在人群中向前行走，风中大衣轻轻飘动。” |
| **摄像机（Camera）** | 移动方式 + 镜头类型 | “中景跟踪拍摄，使用 35mm 镜头，缓慢地向后移动；轻微的手持抖动。” |
| **风格（Style）** | 情绪 + 整体风格 | “具有电影史诗感的风格，暖色调调，浅景深，将焦点对准主体面部。” |

---

## 🧠 提示优化协议

**在执行之前，系统必须将用户的意图转化为技术性的“导演指令”。**

1. **使用专业摄像术语**：如“推镜（Dolly In/Out）”、“摇臂拍摄（Crane Shot）”、“快速平移（Whip Pan）”、“跟踪拍摄（Tracking Shot）”、“变形镜头（Anamorphic Lens）”等。  
2. **使用物理规则描述**：用“焦散图案（caustic patterns）”、“体积光线（volumetric rays）”或“次表面散射（subsurface scattering）”等专业术语，而非简单的“良好的照明（good lighting）”。  
3. **时间码标注**：对于多镜头场景，使用 `[00:00-00:05s]` 的格式来指定时间范围。  
4. **引用标签**：如果提供了参考文件，请使用类似“复制 @video1 的摄像机动作，同时保持 @image1 的视觉风格”这样的描述。  
5. **顺序的重要性**：开头的指令决定了视频的构图，后面的指令决定了视觉效果和细微动作。  
6. **多图像合成（Multi-Image i2v）**：最多可提供 9 张参考图像，模型会融合所有图像的风格、主体特征和环境元素。

---

## 🚀 使用方法

### 模式 1：文本转视频（Text-to-Video, t2v）

```bash
# Epic reveal shot
bash scripts/generate-seedance.sh \
  --subject "a hidden temple in the Andes, mist rolling through the canopy" \
  --intent "epic" \
  --aspect "16:9" \
  --duration 10 \
  --quality high \
  --view

# Tense close-up, vertical for social
bash scripts/generate-seedance.sh \
  --subject "a detective examines a cryptic clue under harsh lamp light" \
  --intent "tense" \
  --aspect "9:16" \
  --duration 5
```

### 模式 2：图像转视频（Image-to-Video, i2v）

将一张或多张参考图像制作成视频。最多可提供 9 张图像，模型会整合这些图像中的动作元素。

```bash
# Animate a single local image
bash scripts/generate-seedance.sh \
  --mode i2v \
  --file hero.jpg \
  --subject "hero strides forward, coat billowing in slow motion" \
  --intent "epic" \
  --aspect "16:9" \
  --view

# Animate from a URL
bash scripts/generate-seedance.sh \
  --mode i2v \
  --image "https://example.com/scene.jpg" \
  --subject "camera slowly pulls back to reveal the full landscape" \
  --intent "reveal" \
  --duration 10

# Multi-image blending (character + environment + style reference)
bash scripts/generate-seedance.sh \
  --mode i2v \
  --file character.jpg \
  --file environment.jpg \
  --image "https://example.com/style.jpg" \
  --subject "character walks through the environment in cinematic style" \
  --quality high
```

### 模式 3：视频扩展（Video Extension）

无缝续接现有的 Seedance 2.0 视频，同时保持视觉风格、动作和音效。

```bash
# Extend with no new prompt (model continues naturally)
bash scripts/generate-seedance.sh \
  --mode extend \
  --request-id "abc-123-def-456" \
  --duration 10

# Extend with directional prompt
bash scripts/generate-seedance.sh \
  --mode extend \
  --request-id "abc-123-def-456" \
  --subject "camera continues to pull back, revealing the vast city below" \
  --intent "reveal" \
  --duration 10 \
  --quality high \
  --view
```

### 异步处理模式（适用于长时间任务）

```bash
# Submit and get request_id immediately
RESULT=$(bash scripts/generate-seedance.sh --mode i2v --file photo.jpg --async --json)
REQUEST_ID=$(echo "$RESULT" | jq -r '.request_id')

# Check later
bash ../../../../core/media/generate-video.sh --result "$REQUEST_ID"
```

---

## ⚠️ 限制与注意事项

- **避免使用模糊的关键词**：不要使用“8K、杰作、热门”等模糊的词汇，而应使用具体的技术描述，例如“高保真制作标准、24 帧每秒、电影级的画质”。  
- **动作描述要连贯**：描述一个连续的动作过程，避免使用“男人跑然后停下来”这样的表述，而应使用“男人从冲刺逐渐过渡到突然停下，胸部剧烈起伏”这样的描述。  
- **角色一致性**：确保角色的表现始终一致，面部表情无抖动，服装细节清晰可见。  
- **扩展功能仅适用于 v2.0 版本**：使用 `--mode extend` 时，需要提供之前 `seedance-v2.0-t2v` 或 `seedance-v2.0-i2v` 任务的 `request_id`。  
- **支持的宽高比**：16:9、9:16、4:3、3:4（Seedance 2.0 支持所有这些比例）。  
- **时长**：5 秒、10 秒或 15 秒。  
- **画质选项**：选择“basic”（快速生成）或“high”（高画质）。

---

## 🎭 来自 awesome-seedance 社区的提示模板

### 电影风格（Cinematic Film Styles）

```
[SCENE] Rain-soaked cyberpunk alley, neon signs reflected on wet cobblestones.
[SUBJECT] A lone figure in a weathered trench coat, face obscured by a wide-brim hat.
[ACTION] Walking slowly, each step splashing neon color into the puddles.
[CAMERA] Low-angle tracking shot, anamorphic lens, slow dolly in. Rack focus to face.
[STYLE] Denis Villeneuve aesthetic, high contrast, desaturated blues and magentas. 24fps.
```

### 广告/产品演示（Advertising / Product Motion）

```
[SCENE] Minimalist white studio, single product on a rotating pedestal.
[ACTION] Subtle 360° rotation, product details catching specular highlights.
[CAMERA] Tight medium shot, macro lens pass over surface texture, slow orbit.
[STYLE] Commercial grade, perfect exposure, zero background distraction.
```

### 动作/物理效果（Action / Physics）

```
[SCENE] Desert canyon at sunrise, sandy terrain, long shadows.
[SUBJECT] High-performance sports car accelerating through a turn.
[ACTION] Rear wheels spinning with dust plume, chassis flexing under g-force.
[CAMERA] Low hero angle dolly tracking alongside, then whip pan to lead car.
[STYLE] Hollywood racing film, warm golden grade, motion blur on wheels. 24fps.
```

### 角色一致性（武术/动作场景）（Character Consistency, Martial Arts / Action）

```
[SUBJECT] Same fighter throughout: young woman, white gi, black belt, determined expression.
[ACTION] Fluid kata sequence — rising block, stepping side kick, spinning back fist.
[CAMERA] Full-body wide shot, then cut to close-up of fist impact in slow motion.
[STYLE] Maintain identical lighting, clothing, and facial features in every frame. Zero flicker.
```

---

## ⚙️ 实施细节

| 工具 | 接口 | 使用场景 |
|:---|:---|:---|
| `seedance-v2.0-t2v` | 文本转视频 | 根据导演的描述生成视频 |
| `seedance-v2.0-i2v` | 图像转视频 | 将参考图像制作成视频 |
| `seedance-v2.0-extend` | 视频扩展 | 无缝续接已生成的视频 |

Seedance 2.0 是一个**电影制作辅助工具**，它将低层次的创意意图转化为高保真的技术指令，供 `muapi` 核心系统执行。
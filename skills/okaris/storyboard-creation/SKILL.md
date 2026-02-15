---
name: storyboard-creation
description: |
  Film and video storyboarding with shot vocabulary, continuity rules, and panel layout.
  Covers shot types, camera angles, movement, 180-degree rule, and annotation format.
  Use for: video planning, film pre-production, ad storyboards, music video planning, animation.
  Triggers: storyboard, storyboarding, shot list, film planning, video planning,
  pre production, shot composition, camera angles, scene planning, visual script,
  animatic, storyboard panels, video storyboard
allowed-tools: Bash(infsh *)
---

# 故事板制作

通过 [inference.sh](https://inference.sh) 命令行工具，利用人工智能图像生成技术来创建视觉故事板。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a storyboard panel
infsh app run falai/flux-dev-lora --input '{
  "prompt": "storyboard panel, wide establishing shot of a modern city skyline at sunset, cinematic composition, slightly desaturated colors, film still style, 16:9 aspect ratio",
  "width": 1248,
  "height": 832
}'

# Stitch panels into a board
infsh app run infsh/stitch-images --input '{
  "images": ["panel1.png", "panel2.png", "panel3.png"],
  "direction": "horizontal"
}'
```

## 镜头类型

| 缩写 | 名称 | 构图方式 | 适用场景 |
|-------------|------|---------|-------------|
| **ECU** | 特写镜头（Extreme Close-Up） | 仅显示眼睛，突出细节 | 表现强烈的情感或细节 |
| **CU** | 近景镜头（Close-Up） | 面部充满画面 | 表达情感、反应或对话 |
| **MCU** | 中近景镜头（Medium Close-Up） | 头部和肩膀 | 用于采访或对话 |
| **MS** | 中景镜头（Medium Shot） | 身体至腰部 | 适合一般对话或动作场景 |
| **MLS** | 中长景镜头（Medium Long Shot） | 身体至膝盖 | 适合行走或轻松互动的场景 |
| **LS** | 远景镜头（Long Shot） | 整个身体 | 展示角色所处的环境 |
| **WS** | 宽景镜头（Wide Shot） | 以环境为主 | 用于展示场景的位置和规模 |
| **EWS** | 极宽景镜头（Extreme Wide Shot） | 展示广阔的景观 | 适合表现宏大的场景或强调孤立感 |

### 生成不同类型的镜头

```bash
# Close-Up — emotion focus
infsh app run falai/flux-dev-lora --input '{
  "prompt": "close-up shot of a woman face showing concern, soft dramatic lighting from the left, shallow depth of field, cinematic film still, slightly desaturated",
  "width": 1248,
  "height": 832
}'

# Medium Shot — dialogue scene
infsh app run falai/flux-dev-lora --input '{
  "prompt": "medium shot of two people talking across a table in a cafe, warm afternoon light through windows, natural composition, cinematic film still, 35mm lens look",
  "width": 1248,
  "height": 832
}'

# Wide Shot — establishing
infsh app run falai/flux-dev-lora --input '{
  "prompt": "wide establishing shot of a futuristic laboratory interior, dramatic overhead lighting, long corridor with glass walls, sci-fi atmosphere, cinematic composition, anamorphic lens style",
  "width": 1248,
  "height": 832
}'
```

## 镜头角度

| 角度 | 效果 | 适用场景 |
|-------|--------|-------------|
| **平视角度** | 中立、自然的视角 | 大多数场景的默认角度 |
| **高角度** | 使主体显得渺小或脆弱 | 强调主体的弱势或提供整体视角 |
| **低角度** | 使主体显得强大或具有主导地位 | 用于表现权威、英雄主义或威胁感 |
| **鸟瞰角度** | 从高处俯视 | 适合展示地图或地理环境 |
| **虫眼视角** | 用于表现强烈的震撼感 | 适合拍摄建筑或高大的物体 |
| ** Dutch Angle （倾斜角度）** | 产生不安或迷失方向的感觉 | 适合营造紧张或疯狂的氛围 |
| **过肩视角（OTS）** | 观众与角色处于同一视角 | 适合展示对话或第一人称视角 |

## 镜头移动

| 移动方式 | 描述 | 适用的情感效果 |
|----------|-------------|---------|
| **平移（Pan）** | 相机在三角架上水平移动 | 用于扫描、跟随或揭示画面内容 |
| **倾斜（Tilt）** | 相机在三角架上垂直移动 | 用于展示高度或强调某种力量 |
| **推拉（Dolly）** | 相机向主体靠近或远离 | 用于营造亲密感或拉开距离 |
| **轨道移动（Truck）** | 相机横向移动 | 适合跟随主体进行拍摄 |
| **升降（Crane/Jib）** | 相机垂直上下移动 | 适合展示宏大的场景或进行场景切换 |
**缩放（Zoom）** | 镜头焦距变化（相机位置不变） | 用于调整焦点或强调戏剧性效果 |
| **稳定器/云台（Steadicam/Gimbal）** | 相机平稳移动 | 适合保持拍摄的稳定性 |
| **手持拍摄（Handheld）** | 有意的手持抖动 | 用于营造紧迫感或纪录片般的氛围 |
| **固定视角（Static）** | 相机保持不动 | 适合保持稳定的观察或营造紧张感 |

在故事板中，使用箭头在面板上标明镜头的移动方向。

## 连续性规则

### 180度规则

想象两个对话角色之间有一条线（轴线）。摄像机必须始终位于这条线的同一侧。

```
         Character A        Character B
              ●─────────────────●
             /                   \
           /     CAMERA ZONE      \
         /     (stay on this side)  \
       📷          📷          📷
     Camera 1   Camera 2   Camera 3
```

**如果摄像机跨越这条线**，会令观众对空间关系感到困惑。只有在有必要的情况下（例如插入中性镜头或进行明显的镜头移动）才允许跨越这条线。

### 动作连贯性

在切换同一动作的不同角度时，动作必须保持连贯。

```
Panel A: Hand reaches for door handle (medium shot)
Panel B: Hand grabs door handle (close-up)
         ↑ Action continues from same point
```

### 视线匹配

当角色看向某个物体时，下一个镜头应该从他们的视角展示他们所看到的内容。

```
Panel A: Character looks up and to the right
Panel B: The object they see, framed from slightly below-left
```

### 屏幕方向

如果一个角色在一个镜头中从左向右移动，那么在下一个镜头中他们应该继续向左或向右移动。如果方向相反，则表示他们转过了身。

## 面板布局

### 标准格式

| 格式 | 面板数量 | 适用场景 |
|--------|--------|---------|
| 2x3（6个面板）| 每页6个面板 | 适合详细场景或对话 |
| 3x3（9个面板）| 每页9个面板 | 适合动作序列或蒙太奇 |
| 2x2（4个面板）| 每页4个面板 | 适合关键场景或演示文稿 |
| 单个面板（Single）| 每页1个面板 | 适合展示主角或重要时刻 |

### 面板注释格式

每个面板应包含以下信息：

```
┌────────────────────────────────────┐
│ SCENE 3 — SHOT 2                   │ ← Scene and shot number
│                                    │
│   [Generated image here]           │ ← Visual
│                                    │
├────────────────────────────────────┤
│ Shot: MS, eye level                │ ← Shot type and angle
│ Movement: Slow dolly in            │ ← Camera movement
│ Duration: 4 sec                    │ ← Estimated duration
│ Action: Sarah opens the letter     │ ← What happens
│ Dialogue: "This changes everything"│ ← Any spoken lines
│ SFX: Paper rustling, clock ticking │ ← Sound effects
│ Music: Tension builds              │ ← Music cue
└────────────────────────────────────┘
```

## 故事板制作流程

### 第一步：镜头列表

在生成图像之前，先编写一个镜头列表：

```
SCENE 1 — OFFICE, DAY

1.1  WS  - Establishing shot of office building exterior, morning
1.2  MS  - Sarah walks through office, carrying coffee
1.3  CU  - Sarah's face, notices something on her desk
1.4  ECU - An envelope on the desk, unfamiliar handwriting
1.5  MS  - Sarah picks up envelope, opens it
1.6  CU  - Sarah's eyes widen as she reads
1.7  ECU - Key phrase on the letter (insert text)
```

### 第二步：制作面板

确保所有面板的风格保持一致：

```bash
# Establish a consistent style prompt suffix
STYLE="cinematic film still, slightly desaturated, warm color grade, 35mm lens, shallow depth of field"

# Panel 1.1 — Wide establishing
infsh app run falai/flux-dev-lora --input "{
  \"prompt\": \"wide shot of a modern glass office building exterior, morning golden hour light, people entering, $STYLE\",
  \"width\": 1248, \"height\": 832
}" --no-wait

# Panel 1.2 — Medium shot
infsh app run falai/flux-dev-lora --input "{
  \"prompt\": \"medium shot of a professional woman walking through a modern open office, carrying coffee cup, morning light through windows, $STYLE\",
  \"width\": 1248, \"height\": 832
}" --no-wait

# Panel 1.3 — Close-up
infsh app run falai/flux-dev-lora --input "{
  \"prompt\": \"close-up of a woman face looking down at her desk with curious expression, soft office lighting, $STYLE\",
  \"width\": 1248, \"height\": 832
}" --no-wait
```

### 第三步：组装故事板

```bash
# Stitch panels into rows
infsh app run infsh/stitch-images --input '{
  "images": ["panel_1_1.png", "panel_1_2.png", "panel_1_3.png"],
  "direction": "horizontal"
}'

infsh app run infsh/stitch-images --input '{
  "images": ["panel_1_4.png", "panel_1_5.png", "panel_1_6.png"],
  "direction": "horizontal"
}'

# Then stitch rows vertically for full page
infsh app run infsh/stitch-images --input '{
  "images": ["row1.png", "row2.png"],
  "direction": "vertical"
}'
```

## 风格一致性建议

- 在所有面板中使用相同的风格标识（如镜头类型、色彩处理、光线效果）
- 如果需要让不同面板中的角色保持一致的外观，可以使用 **FLUX LoRA** 工具 |
- 确保所有面板的宽高比一致 |
- 制作比实际需要更多的面板，然后从中挑选最合适的 |
- 如果某个面板不符合风格要求，使用调整后的提示重新生成该面板

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 跨越180度规则 | 使观众对空间关系感到困惑 | 保持摄像机位于同一侧或使用中性镜头 |
| 所有镜头类型相同 | 视觉效果单调，缺乏节奏感 | 适当切换不同类型的镜头（如近景、中景、宽景） |
| 没有场景开场镜头 | 观众无法理解场景的位置 | 使用宽景或极宽景镜头来开始场景 |
| 每个场景的镜头数量过多 | 使节奏拖沓 | 通常每个场景5-8个镜头较为合适 |
| 面板之间的风格不一致 | 使故事板看起来像来自不同项目 | 使用相同的风格标识 |
| 缺少注释 | 面板信息不明确 | 必须标注镜头类型、移动方向和动作内容 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@ai-video-generation
npx skills add inferencesh/skills@video-prompting-guide
npx skills add inferencesh/skills@prompt-engineering
```

可以浏览所有相关应用程序：`infsh app list`
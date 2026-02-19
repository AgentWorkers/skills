---
name: storyboard-creation
description: "电影和视频的分镜制作涉及镜头词汇、画面连贯性规则以及分镜板的布局。内容涵盖镜头类型、拍摄角度、画面移动方式、180度转角规则以及注释格式。适用于：视频策划、电影前期制作、广告分镜制作、音乐视频策划、动画制作等场景。相关术语包括：分镜（storyboarding）、镜头列表（shot list）、拍摄规划（film planning）、画面构图（shot composition）、拍摄角度（camera angles）、场景设计（scene planning）、视觉脚本（visual script）、动画分镜（animatic）等。"
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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或启动后台进程。也可以[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 镜头类型

| 缩写 | 名称 | 构图 | 适用场景 |
|-------------|------|---------|-------------|
| **ECU** | 极近景 | 仅显示眼睛，突出细节 | 表现强烈的情感或细节 |
| **CU** | 近景 | 面部占据整个画面 | 用于表现情感、反应或对话 |
| **MCU** | 中近景 | 头部和肩膀 | 适用于采访或对话场景 |
| **MS** | 中景 | 从腰部以上拍摄 | 用于一般对话或动作场景 |
| **MLS** | 中长景 | 从膝盖以上拍摄 | 用于展示行走或轻松的互动场景 |
| **LS** | 远景 | 全身镜头 | 展示角色所处的环境 |
| **WS** | 宽景 | 环境成为主要焦点 | 用于展示场景的位置和规模 |
| **EWS** | 极宽景 | 广阔的景观 | 适用于展现宏大的场景、强调孤立感或进行场景转换 |

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

## 摄像机角度

| 角度 | 效果 | 适用场景 |
|-------|--------|-------------|
| **平视** | 中立、自然的视角 | 大多数场景的默认选择 |
| **高角度** | 使主体看起来渺小或脆弱 | 用于表现弱势或提供整体视角 |
| **低角度** | 使主体看起来强大或具有支配力 | 用于展现权威、英雄主义或威胁感 |
| **鸟瞰** | 如上帝般的视角 | 适用于展示地图或地理环境 |
| **虫眼视角** | 用于展现强烈的力量感或令人敬畏的场景 | 适用于建筑或高大的物体 |
| **荷兰角** | 造成不安或迷失方向的感觉 | 适用于营造紧张感、疯狂或动作场景 |
| **肩上视角 (OTS)** | 观众与角色处于同一水平线 | 适用于展示对话或第一人称视角 |

## 摄像机移动方式

| 移动方式 | 描述 | 传达的情感 |
|----------|-------------|---------|
| **平移** | 摄像机在三角架上水平移动 | 用于扫描画面、跟随角色或揭示新信息 |
| **倾斜** | 摄像机在三角架上垂直移动 | 用于展示高度或强调某种力量 |
| **推拉** | 摄像机向主体靠近或远离 | 用于营造亲密感或增加距离感 |
| **轨道移动** | 摄像机横向移动 | 用于跟随角色或展示环境 |
| **升降** | 摄像机上下移动 | 用于展示宏大的场景或进行场景转换 |
**缩放** | 镜头焦距变化（摄像机位置不变） | 用于调整焦点或强调戏剧性效果 |
| **稳定器/云台** | 摄像机平稳移动 | 用于营造沉浸感或跟随动作 |
| **手持拍摄** | 有意地晃动摄像机 | 用于营造紧迫感、纪录片风格或混乱的场景 |
| **固定视角** | 摄像机保持不动 | 用于保持稳定性、观察或营造紧张感 |

在故事板中，可以通过在面板上绘制箭头来表示摄像机的移动方向。

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

**如果摄像机跨越这条线**，会令观众对空间关系感到困惑。只有在有必要的情况下（例如通过中景镜头或明显的摄像机移动）才允许跨越这条线。

### 动作连贯性

在切换同一动作的不同角度时，动作必须无缝衔接：

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

如果一个角色在一个镜头中从左向右移动，那么在下一个镜头中他们应该继续向左或向右移动。如果方向相反，则表示角色已经转身。

## 面板布局

### 标准格式

| 格式 | 面板数量 | 适用场景 |
|--------|--------|---------|
| 2x3（6个面板）| 每页6个面板 | 适用于详细场景或对话场景 |
| 3x3（9个面板）| 每页9个面板 | 适用于动作序列或蒙太奇 |
| 2x2（4个面板）| 每页4个面板 | 适用于关键场景或演示文稿 |
| 单个面板 | 每页1个面板 | 适用于主角镜头或关键时刻 |

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

确保所有面板保持一致的样式：

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

## 保持风格一致性的小贴士

- 在所有面板中使用**相同的风格后缀**（如镜头类型、色彩调整、光线处理）
- 如果需要确保角色在多个面板中保持一致的外观，可以使用 **FLUX LoRA** 工具
- 保持所有面板的**相同宽高比**
- 制作比实际需要的更多面板，然后从中挑选最佳方案
- 如果某个面板不符合风格要求，使用调整后的提示重新生成

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 跨越180度规则 | 使观众对空间关系感到困惑 | 保持摄像机位于同一侧或使用中景镜头 |
| 所有镜头类型都相同 | 视觉上显得单调乏味 | 适当切换近景、中景和宽景等不同类型的镜头 |
| 没有场景开场镜头 | 观众无法了解场景的位置 | 使用宽景或极宽景镜头来开场 |
| 每个场景的镜头数量过多 | 会导致节奏拖沓 | 通常每个场景5-8个镜头较为合适 |
| 面板之间的风格不一致 | 使故事板看起来像来自不同项目 | 使用相同的风格后缀 |
| 缺少注释 | 面板信息不明确 | 必须标注镜头类型、摄像机移动方式和动作内容 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@video-prompting-guide
npx skills add inference-sh/skills@prompt-engineering
```

可以浏览所有可用应用程序：`infsh app list`
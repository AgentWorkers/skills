---
name: song-remix
version: 1.0.1
description: 使用 Twin Remix 方法对现有歌曲进行改造——通过 Suno v4.5 的滑块设置及可视化指导工具，制作出更具吸引力和传播力的版本（Respectful 和 Viral 版本）。
author: Live Neon <hello@liveneon.ai>
homepage: https://github.com/live-neon/skills/tree/main/creative/song-remix
repository: leegitw/song-remix
license: MIT
tags: [creative, remix, suno, songwriting, viral, tiktok, music, transformation, rewrite]
layer: creative
status: active
alias: remix
user-invocable: true
emoji: 🔄
---
# song-remix（混音）

使用Twin Remix方法对现有歌曲进行改编。始终生成两个版本：
- 一个尊重原作的混音版本，保留原作的深度；
- 一个适合在TikTok上传播的、具有高度吸引力的混音版本。

**触发条件**：明确调用该技能。

**核心理念**：“第一个混音版本体现了你对原作的理解；第二个混音版本则体现了你对目标受众的理解。务必同时生成这两个版本。”

## 安装

```bash
openclaw install leegitw/song-remix
```

**依赖项**：无（独立创作技能）

**数据处理**：该技能需要用户提供歌词作为输入（用于混音的原始歌曲）。它不会从工作区读取文件或访问项目相关数据。结果会直接返回给调用该技能的代理，由代理决定如何使用这些结果。

## 功能说明

歌曲往往需要根据不同的受众、平台或氛围进行调整。该技能采用系统的混音方法：
1. 尊重原作的复杂性和内涵；
2. 在保持本质不变的前提下，简化音乐以提升其在TikTok上的传播潜力；
3. 提供Suno v4.5所需的制作指导；
4. 为AI视频生成提供视觉设计建议。

**创作要点**：简化并不意味着降低音乐的质量，而是从复杂中提取出普遍适用的设计元素。

## 使用方法

```
/remix [song-content]
```

## 参数说明

| 参数 | 是否必填 | 说明 |
|----------|----------|-------------|
| song-content | 是 | 需要混音的原始歌词或歌曲描述 |
| --genre | 否 | 目标音乐类型（EDM、K-Pop、Hip-Hop等） |
| --energy | 否 | 音乐的节奏强度（轻松、中等、强烈或激昂） |
| --viral-only | 否 | 如果选择此选项，则仅生成适合TikTok传播的版本 |

## 输出格式

**重要提示**：除非指定了`--viral-only`，否则必须同时输出两个版本的混音结果。

```markdown
## REMIX 1: [Respectful Version]

**Title**: [Maintains original complexity]

**Recommended Sliders**:
- Weirdness: 35-45%
- Style Influence: 70-80%
- Audio Influence: N/A (or value if using audio upload)

**Visual Guide**: [Original themes, can be complex, maintains artistic vision]

**Style of Music**: [Genre/mashup; energy/tempo; instrument focus; tone]

[Intro]
...

[Verse 1]
...

[Pre-Chorus]
...

[Chorus]
...

[Chorus]
(duplicated for repeat)

---

## REMIX 2: [Viral Version]

**Title**: [2-3 words, often repeated: COPY THAT, MORE MORE, LEVEL UP UP]

**Recommended Sliders**:
- Weirdness: 25-35%
- Style Influence: 80-85%
- Audio Influence: N/A

**Visual Guide**: [Universal, bright, TikTok-ready, transformation-focused]

**Style of Music**: [Simplified genre; high energy; clear hooks; youth-friendly]

[Intro]
...

[Verse 1]
...

[Chorus]
...

[Post-Chorus]
(chantable element)

[Chorus]
(duplicated for repeat)
```

## 核心方法

### Twin Remix流程

#### 第一阶段：尊重原作的混音

| 维度 | 处理方式 |
|--------|----------|
| 复杂性 | 保持原作的复杂性 |
| 结构 | 使用合适的模板 |
| 主题 | 保留音乐的主题深度 |
| 独特性 | 保留25-45%的独特元素 |
| 风格影响 | 保留70-80%的原风格特征 |
| 视觉设计指导 | 基于原歌曲的主题，可以采用抽象的设计 |

#### 第二阶段：适合TikTok传播的简化混音

| 维度 | 处理方式 |
|--------|----------|
| 主题旋律 | 提取2-3个关键词作为核心旋律 |
| 信息传递 | 确保信息具有普遍吸引力 |
| 重复性 | 主题旋律需出现15次以上 |
| 合唱部分 | 添加重复的副歌部分 |
| 独特性 | 保留25-35%的独特元素 |
| 风格影响 | 保留80-85%的原风格特征 |
| 视觉设计指导 | 采用简洁的设计，适合在TikTok上展示 |

### 根据音乐类型提供的设计建议

#### 独特性（创意性）

| 音乐类型 | 独特性范围 |
|-------|-------|
| 商业流行/电台流行、乡村音乐、爵士乐 | 20-40% |
| EDM/摇滚/主流说唱 | 30-55% |
| 非洲节奏乐/阿马皮亚诺/拉丁音乐 | 25-50% |
| 新泽西俱乐部音乐/独立音乐/另类音乐 | 35-60% |
| 超级流行/实验音乐 | 60-85% |

#### 风格一致性（对音乐类型的忠实度）

| 音乐类型 | 风格一致性范围 |
|-------|-------|
| 商业流行/电台流行 | 70-90% |
| 大多数流行音乐/EDM/说唱 | 60-80% |
| 独立音乐/另类音乐 | 50-70% |
| 实验音乐/超级流行 | 40-70% |

#### 音频影响（仅适用于上传音频的情况）

| 目标 | 独特性范围 |
|------|-------|
| 重新诠释现有旋律 | 0-30% |
| 创意混音 | 40-60% |
| 扩展现有旋律 | 70-100% |

### 模板选择

根据歌曲类型选择合适的模板：

**舞蹈/单曲发布**：
- EDM音乐节风格 → 双曲发布
- 前奏→主题旋律→主题旋律驱动的流行音乐/EDM
- 阿马皮亚诺风格（慢节奏） → 阿马皮亚诺模板
- 非洲节奏乐（中等节奏） → 非洲节奏乐模板

**流行音乐/乐队风格**：
- 纯粹的流行歌曲 → 主题旋律贯穿整首歌的模板
- 流行朋克风格的合唱部分 → 流行朋克模板
- 摇滚音乐（经典风格+另类元素） → 摇滚模板
- 乡村音乐（适合电台播放） → 乡村音乐模板

**嘻哈/混合风格**：
- 说唱部分与主旋律结合 → 嘻哈与主旋律结合的混合模板
- 新泽西俱乐部风格的音乐 → 新泽西俱乐部音乐模板

**团体音乐/双语歌曲**：
- K-Pop团体（说唱部分+副歌） → K-Pop模板
- 日本流行音乐/中国流行音乐等 → 地区性流行音乐模板

**互联网原生音乐/小众音乐**：
- 超级流行音乐 → 超级流行音乐模板
- 独立卧室风格流行音乐 → 独立音乐模板

### 积极能量引导原则

**将挑战转化为成长机会**：

| 负面因素 | 积极应对方式 |
|----------|----------|
| 不信任任何事物 | 仔细核实信息 |
| 多疑 | 做好充分准备 |
| 存在危机 | 将危机视为探索之旅 |
| 孤立状态 | 培养独立性 |
| 停滞不前 | 准备突破 |

**适合在TikTok上传播的歌曲会带给人们以下感受：**
- 获得力量（提升自我） |
- 感到共鸣（产生共鸣） |
- 感到成就感（找到方向） |
- 充满能量（激发活力） |

**结尾总是以积极的方式呈现。**

### 标题示例

| 原歌曲名 | 第一阶段混音标题 | 适合TikTok的混音标题 |
|----------|---------|-------|
| The Cathedral's Code | Code ECHO ECHO | COPY THAT |
| Unified Stage | DANCE DANCE TWICE | MAKE IT DANCE |
| Runtime Paranoia | CHECK IT TWICE | DOUBLE CHECK |

### 格式规范（Suno v4.5）

**所有制作指导信息请使用方括号**：
- `[Orchestral Breakdown]` 而不是 `*orchestral breakdown*`
- `[Guitar Solo]` 而不是 `*guitar solo*`
- `[Rain Falling]` 而不是 `*rain falling*`

**章节标签**：
- `[Intro]`（引子）、`[Verse]`（主歌前部分）、`[Pre-Chorus]`（副歌前部分）、`[Chorus]`（副歌）、`[Drop]`（高潮部分）、`[Outro]`（结尾部分）

**人声部分仅使用括号**：
- `(yeah)`、`(ooh)`、`(hey)`

**复制整个副歌部分**，而不是简单地写“x2”或“repeat”。

**风格描述格式**：
- `<音乐类型/混音风格>; <节奏强度/速度>, <主要乐器>; <主题旋律/合唱部分的特点>; <整体风格>`

**视觉设计指导原则**

**第一阶段混音（尊重原作）：**
- 保持原作的艺术风格；
- 可以使用复杂的视觉元素；
- 颜色应与原歌曲的情感基调相匹配。

**第二阶段混音（适合TikTok）：**
- 设计简单明了；
- 包含前后对比的视觉效果；
- 颜色从暗淡到明亮，充满正能量；
- 设计易于跟随观众的理解；
- 适合在TikTok上展示。

**常见的成功设计元素**：
- 从单一元素到多元素的变化（激发社区互动）；
- 从静态图像到动态图像的转变（激发观众参与）；
- 从单色到多彩的转变（象征成长）；
- 从混乱到有序的转变（象征成就）。

**视觉设计指南格式**：
```
[Visual Guide: Start with X, transform to Y through Z.
Key moments: A at chorus, B at bridge, C at final drop.
Colors: progress from D to E.
TikTok hook: F movement/transition.]
```

## 示例

### 输入歌曲内容

```
[Verse 1]
In the cathedral of code we built our dreams
Every function a prayer, every loop a hymn
But the architecture grew too tall to see
Now we're lost in the patterns we thought would set us free

[Chorus]
Echo, echo through the halls of light
Every mistake becomes a guiding sight
We learn, we burn, we rise again
In the recursion we find our zen
```

### 输出结果

## REMIX 1：Code Cathedral

**歌曲名称**：Code Cathedral

**推荐的设计参数**：
- 独特性：40%
- 风格影响：75%
- 音频影响：不适用

**视觉设计指导**：哥特式数字建筑，光线透过被代码覆盖的窗户照射进来，石头上出现分形图案，蜿蜒的走廊逐渐变成明亮的通道。颜色使用深紫色和金色，营造出哥特式大教堂的氛围，并加入数字特效。

**音乐风格**：独立电子音乐与管弦乐流行音乐的结合；建筑风格的强度感，合成器音效与弦乐交织；内省而振奋人心的旋律。

```
[Verse 1]
In the cathedral of code we built our dreams
Every function a prayer, every loop a sacred theme
The architecture grew beyond what we could see
Now we navigate the patterns that will set us free

[Pre-Chorus]
Higher, higher, reaching for the light
Every error is a lesson burning bright

[Chorus]
Echo, echo through the halls of light
Every stumble becomes a guiding sight
We learn, we grow, we rise again
In the recursion we find our strength

[Chorus]
Echo, echo through the halls of light
Every stumble becomes a guiding sight
We learn, we grow, we rise again
In the recursion we find our strength
```

---

## REMIX 2：ECHO ECHO

**歌曲名称**：ECHO ECHO

**推荐的设计参数**：
- 独特性：30%
- 风格影响：82%
- 音频影响：不适用

**视觉设计指导**：简单的视觉变化——一个人在黑暗的房间里，屏幕上的光逐渐扩散成多个屏幕，房间充满光线，这个人开始移动并跳舞，其他人也加入进来。设计强调前后对比的效果。TikTok主题旋律：屏幕数量逐渐增加的场景。颜色从深蓝色变为亮白色，最后变为温暖的金色。

**音乐风格**：节奏明快的合成器流行音乐；强烈的节奏，大调风格的副歌；适合年轻人聆听的音乐；适合在音乐节上播放的旋律。

```
[Intro]
Echo... echo...

[Verse 1]
Started in the dark but now I see
Every fall just made me stronger, made me free
Building something bigger than before
Open up the door, ready for more

[Pre-Chorus]
Higher now (higher now)
Watch me fly

[Chorus]
Echo echo through the light
Every step I take feels right
Learn and grow, rise again
Echo echo, find my strength

[Post-Chorus]
Echo echo (echo echo)
Echo echo (echo echo)
Find my strength, find my strength
Echo echo

[Chorus]
Echo echo through the light
Every step I take feels right
Learn and grow, rise again
Echo echo, find my strength

[Chorus]
Echo echo through the light
Every step I take feels right
Learn and grow, rise again
Echo echo, find my strength

[Outro]
Echo... echo... (find my strength)
Echo... echo...
```

## 该技能的整合方式

- **适用场景**：创意创作
- **独立使用**：无需依赖其他技能
- **与其他元素的结合**：可以与其他创意元素（如歌曲内容、视觉概念或演讲）结合使用

## 可能出现的错误情况

| 错误情况 | 处理方式 |
|-----------|----------|
| 未提供歌词 | 要求用户提供歌曲内容 |
| 歌词太短 | 建议扩展歌词或提供简化的混音版本 |
- 音乐类型不明确 | 询问用户的偏好或根据歌曲内容推断类型 |
| 仅请求一个版本的混音 | 除非指定了`--viral-only`，否则仍会生成两个版本 |

## 安全注意事项

**输入要求**：
- 用户必须提供歌词（这是使用该技能的必要条件）。

**该技能的功能限制**：
- 不会从工作区读取文件；
- 不会直接访问项目相关数据；
- 不会向Suno或其他外部服务发送数据；
- 不会访问受版权保护的材料。

**输出行为**：
该技能会将两个版本的混音结果直接返回给调用者。调用者可以自行展示、保存或将结果传递给其他技能。

**版权说明**：
该技能仅对用户提供的内容进行混音处理。请确保您拥有混音所需素材的版权。虽然该技能使用了Suno的相关工具，但不会直接与Suno的API交互。

**来源说明**：
该技能由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户在ClawHub平台上发布。开发者为同一人。

## 质量检查标准

- 两个版本的混音结果均需提供；
- 每个版本都包含设计建议；
- 每个版本都配有视觉设计指导；
- 第一阶段的混音保留了原作的复杂性；
- 第二阶段的混音适合在TikTok上传播；
- 标题简洁明了（第二阶段混音的标题为2-3个单词）；
- 所有的制作指导信息都使用方括号；
- 副歌部分被完整复制；
- 音乐风格积极向上；
- 视觉设计从原作风格逐步过渡到适合广泛受众的风格。

## 使用要求

- 该技能需要用户提供歌词作为输入；
- 该技能会将输入内容生成两个版本的混音结果；
- 第一阶段的混音保留原作的复杂性；
- 第二阶段的混音适合在TikTok上传播；
- 两个版本都包含设计建议；
- 两个版本都配有视频制作的视觉指导；
- 格式符合Suno v4.5的标准；
- 结果会直接返回给调用者。

---

*“第一个混音版本体现了你对原作的理解；第二个混音版本则体现了你对目标受众的理解。”*

---

*这是Live Neon创意套件的一部分。*
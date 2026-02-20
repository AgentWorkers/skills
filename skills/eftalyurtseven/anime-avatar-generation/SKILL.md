---
name: anime-avatar-generation
description: 使用 each::sense AI 生成动漫风格的头像和角色。可以将照片转换为动漫风格，创建吉卜力风格的肖像画、漫画角色，以及包含多个视角的完整角色资料表。
metadata:
  author: eachlabs
  version: "1.0"
---
# 动漫头像生成

使用 `each::sense` 功能，您可以生成令人惊叹的动漫风格头像和角色。该技能能够将照片转换为动漫艺术作品，创建原创的动漫角色，并实现从吉卜力风格到赛博朋克风格等多种动漫风格。

## 主要功能

- **照片转动漫**：将真实照片转换为动漫风格的艺术作品  
- **吉卜力风格**：受吉卜力工作室启发的柔和、富有想象力的角色  
- **漫画风格**：黑白或彩色的漫画风格角色  
- **赛博朋克风格**：充满霓虹灯效果的未来主义动漫  
- **Q版头像**：可爱、极度夸张的角色风格  
- **个人资料图片**：专为社交媒体优化的动漫头像  
- **全身角色**：包含服装的完整角色设计  
- **角色参考图**：多角度展示的角色参考图  

## 快速入门  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime avatar of a young woman with long blue hair and golden eyes, soft lighting, studio quality",
    "mode": "max"
  }'
```  

## 动漫风格参考  

| 风格 | 描述 | 适用场景 |  
|-------|-------------|----------|  
| 吉卜力 | 色彩柔和、充满想象力、手绘风格 | 温暖、怀旧的肖像画  
| 漫画 | 黑白或彩色线条、富有表现力的角色 | 漫画风格的角色  
| 赛博朋克 | 霓虹灯效果、未来主义风格 | 极具未来感的动漫头像  
| Q版角色 | 极度夸张的可爱风格 | 可爱的吉祥物或表情包  
| 男性向动漫 | 鲁莽、动作性强、充满戏剧性的角色 | 男性角色、英雄形象  
| 女性向动漫 | 色彩柔和、浪漫风格 | 女性角色、偶像形象  
| 男性青年向动漫 | 比例真实、风格成熟 | 专业用途的头像  

## 使用案例示例  

### 1. 照片转动漫转换  

将一张真实照片转换为动漫风格的艺术作品。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Convert this photo to anime style. Keep the facial features recognizable but transform it into a beautiful anime portrait with vibrant colors and soft shading.",
    "mode": "max",
    "image_urls": ["https://example.com/my-photo.jpg"]
  }'
```  

### 2. 吉卜力风格头像  

创建一个受吉卜力工作室启发的角色肖像。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Studio Ghibli style portrait of a young girl with short brown hair, wearing a simple blue dress. Soft watercolor aesthetic, gentle expression, surrounded by nature with small forest spirits in the background. Hayao Miyazaki inspired art style.",
    "mode": "max"
  }'
```  

### 3. 漫画风格角色  

生成一张黑白的漫画风格角色图片。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a manga-style character portrait in black and white. A confident male protagonist with spiky black hair, sharp eyes, wearing a school uniform. Dynamic pose, dramatic shading with screentones, shonen manga aesthetic.",
    "mode": "max"
  }'
```  

### 4. 赛博朋克风格动漫  

创建一个充满霓虹灯效果的未来主义动漫角色。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a cyberpunk anime character. A hacker girl with short neon pink hair with cyan highlights, cybernetic eye implants, wearing a leather jacket with glowing circuit patterns. Dark urban background with neon signs, rain, and holographic advertisements. Ghost in the Shell meets Akira aesthetic.",
    "mode": "max"
  }'
```  

### 5. Q版头像  

生成一个可爱、极度夸张的角色头像。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a chibi anime avatar. A cute girl with big sparkly purple eyes, long wavy pink hair with star clips, wearing a magical girl outfit with ribbons and bows. Super deformed proportions with big head and small body, kawaii expression, pastel color palette, simple clean background.",
    "mode": "max"
  }'
```  

### 6. 动漫个人资料图片  

为社交媒体个人资料创建一个优化过的头像。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 1:1 square anime profile picture. A mysterious character with silver hair covering one eye, heterochromia (one blue eye, one red eye), wearing a high-collar black coat. Dramatic lighting from the side, dark elegant background. The composition should work well as a small avatar icon.",
    "mode": "max"
  }'
```  

### 7. 全身动漫角色  

设计一个包含服装和姿势的完整角色。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a full body anime character design. A female warrior with long red hair in a ponytail, green eyes, wearing ornate silver armor with a flowing cape. She holds a glowing magical sword. Dynamic standing pose, fantasy setting with castle in the background. High detail anime illustration style.",
    "mode": "max"
  }'
```  

### 8. 动漫角色组合  

在同一场景中生成多个角色。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime illustration of a couple. A tall guy with messy black hair and glasses wearing a casual hoodie, and a shorter girl with twin-tail blonde hair wearing a sundress. They are standing together at a summer festival, holding hands, with fireworks in the night sky behind them. Romantic shojo anime style.",
    "mode": "max"
  }'
```  

### 9. 具体发色/眼色的动漫角色  

创建一个具有精确颜色规格的角色。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character with very specific colors: gradient hair that transitions from deep purple at the roots to lavender at the tips, bright amber eyes with a subtle golden glow, pale skin with a slight blush. The character should have an elegant hairstyle with braids and loose strands. Portrait shot, soft dreamy lighting, flower petals floating around.",
    "mode": "max"
  }'
```  

### 10. 动漫角色参考图（多角度）  

生成多角度的角色参考图以确保一致性。  

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character reference sheet with multiple angles. The character is a young male mage with medium-length teal hair and bright orange eyes, wearing a wizard robe with gold trim. Show front view, side view (profile), 3/4 view, and back view on a clean white background. Include close-up details of the face and any accessories. Professional character design sheet format.",
    "mode": "max"
  }'
```  

## 模式选择  

在生成前请询问用户：  
“您需要快速且低成本的结果，还是高质量的结果？”  

| 模式 | 适用场景 | 速度 | 质量 |  
|------|----------|-------|---------|  
| `max` | 最终头像、个人资料图片、角色设计 | 较慢 | 最高质量 |  
| `eco` | 快速草图、风格探索、多次修改 | 较快 | 良好质量 |  

## 多轮角色优化  

使用 `session_id` 进行角色设计的多次修改：  

```bash
# Initial character concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime character - a mysterious ninja with dark clothing",
    "session_id": "ninja-character-design"
  }'

# Refine based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "I like it but make the character female, add a red scarf, and give her white hair",
    "session_id": "ninja-character-design"
  }'

# Request style variation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the same character but in chibi style",
    "session_id": "ninja-character-design"
  }'
```  

## 多个角色间的风格一致性  

创建多个具有统一艺术风格的角色：  

```bash
# First character
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create an anime hero character - a young man with spiky orange hair and determined expression, wearing a battle-worn jacket",
    "session_id": "anime-team-project"
  }'

# Second character (same session for style consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create his rival - a calm, cool character with slicked-back blue hair, wearing a formal coat. Keep the same art style as the previous character.",
    "session_id": "anime-team-project"
  }'
```  

## 最佳实践  

### 角色描述技巧  

- **头发**：指定颜色、长度、发型（刺猬头、波浪发、直发、双马尾等）  
- **眼睛**：描述颜色、形状和表情（锐利、柔和、闪烁等）  
- **服装**：详细说明服装风格、颜色和配饰  
- **表情**：定义角色的情绪（快乐、神秘、凶猛、温柔等）  
- **姿势**：描述角色的身体姿势和手势  

### 风格规范  

- 参考具体的动漫或漫画风格进行设计  
- 说明对光线的偏好（柔和光、戏剧性光影等）  
- 指定背景的复杂程度（简单、复杂、渐变等）  
- 提供颜色调色板的偏好（淡色调、鲜艳色调、深色调等）  

## 技术注意事项  

- 个人资料图片请使用 1:1 的宽高比  
- 角色参考图请使用横向布局  
- 全身角色请确保画面包含头部到脚部的完整构图  
- 详细的人物面部请使用特写视角  

## 创建动漫头像的提示  

在创建动漫角色时，请提供以下详细信息：  
1. **角色性别/年龄**：小女孩、成年男性、青少年男孩等  
2. **头发细节**：颜色、长度、发型、配饰（丝带、发夹等）  
3. **眼睛细节**：颜色、形状、表情、特殊特征  
4. **服装**：服装类型、风格、颜色、配饰  
5. **姿势/构图**：肖像、全身、动作姿势等  
6. **艺术风格**：吉卜力、漫画、赛博朋克、Q版等  
7. **情绪/氛围**：快乐、神秘、戏剧性、浪漫等  
8. **背景**：简单背景、复杂背景或特定场景  

### 示例提示结构  

```
"Create a [style] anime [character type] with [hair details] and [eye details].
They are wearing [outfit description].
[Pose/composition]. [Background/setting].
[Mood/atmosphere] feeling. [Additional details]."
```  

## 错误处理  

| 错误类型 | 原因 | 解决方案 |  
|-------|-------|----------|  
| `Failed to create prediction: HTTP 422` | 数据不平衡 | 请在 eachlabs.ai 补充数据  
| 内容违规 | 内容不符合规定 | 调整提示以符合内容政策  
| 超时 | 生成过程复杂 | 将客户端超时时间设置为至少 10 分钟  
| 角色不一致 | 会话未保存 | 相关请求请使用相同的 `session_id`  

## 相关技能  

- `each-sense`：核心 API 文档  
- `photo-to-illustration`：通用插画风格转换  
- `character-design`：非动漫角色的创建  
- `profile-picture-generation`：通用头像生成
---
name: discord-graphics-generation
description: 使用 each::sense AI 生成 Discord 服务器所需的各类图形资源，包括服务器图标、横幅、角色图标、欢迎界面图形、活动横幅、机器人头像以及表情符号等。所有生成的图形资源均需符合 Discord 的格式要求。
metadata:
  author: eachlabs
  version: "1.0"
---
# Discord 图形生成

使用 `each-sense` 功能生成专业的 Discord 服务器图形。该技能可创建适用于 Discord 各种图形位置、尺寸和最佳实践的图像。

## 主要功能

- **服务器图标**：用于标识服务器的方形图标（512x512）
- **服务器横幅**：用于服务器个人资料的宽幅横幅（960x540）
- **角色图标**：用于标识角色的小图标（64x64）
- **欢迎图形**：用于频道标题区的欢迎图片
- **规则图形**：用于规则频道的视觉提示
- **公告横幅**：醒目的公告图片
- **活动横幅**：用于服务器活动的宣传图片
- **机器人头像**：用于 Discord 机器人的自定义头像
- **表情包**：自定义服务器表情包
- **服务器助力徽章**：用于表彰服务器助力者的图形

## 快速入门

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord server icon for a gaming community called Pixel Warriors, featuring a pixel art sword and shield with purple and blue colors",
    "mode": "max"
  }'
```

## Discord 图形格式与尺寸

| 资产类型 | 尺寸 | 长宽比 | 用途 |
|------------|------|--------------|----------|
| 服务器图标 | 512x512 | 1:1 | 服务器标识，显示在所有地方 |
| 服务器横幅 | 960x540 | 16:9 | 服务器个人资料标题（Nitro 级别 2+） |
| 角色图标 | 64x64 | 1:1 | 显示在用户名旁边的角色徽章 |
| 邀请横幅 | 1920x1080 | 16:9 | 服务器邀请背景（Nitro 级别 1+） |
| 服务器发现信息 | 1024x1024 | 1:1 | 服务器发现列表 |
| 自定义表情包 | 128x128 | 1:1 | 服务器表情包（最大 256KB） |
- 贴纸 | 320x320 | 1:1 | 自定义贴纸 |

## 使用示例

### 1. Discord 服务器图标

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a tech community called CodeHub. Feature a modern code bracket symbol with gradient from cyan to purple, dark background, clean minimal design that reads well at small sizes.",
    "mode": "max"
  }'
```

### 2. 服务器横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 960x540 Discord server banner for an anime discussion community. Show a stylish anime-inspired cityscape at night with neon lights, purple and pink color scheme. Leave the center area less busy for the server name overlay.",
    "mode": "max"
  }'
```

### 3. 角色图标集

```bash
# Admin role icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Admin role. Gold crown symbol on dark background, simple and recognizable at small size. Clean vector-style design.",
    "session_id": "discord-roles-001"
  }'

# Moderator role icon (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Moderator role. Silver shield symbol, same style as the admin icon. Simple and recognizable.",
    "session_id": "discord-roles-001"
  }'

# VIP role icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for VIP members. Purple diamond or star symbol, matching the style of previous role icons.",
    "session_id": "discord-roles-001"
  }'
```

### 4. 欢迎频道图形

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a wide banner graphic for a Discord welcome channel. Friendly and inviting design with soft gradients in blue and purple. Include visual space for welcome text. Aspect ratio 16:9, dimensions 1200x675. Make it warm and community-focused.",
    "mode": "max"
  }'
```

### 5. 规则频道图形

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord rules channel header graphic. Professional and authoritative design with a scroll or document motif. Dark theme with gold accents. 1200x400 pixels. Include subtle gavel or scales of justice imagery. Clean and readable.",
    "mode": "max"
  }'
```

### 6. 公告图形

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord announcement banner for a server update. Exciting and attention-grabbing with a megaphone or notification bell motif. Red and orange energy colors with dark background. 1200x600 pixels. Space for announcement text.",
    "mode": "max"
  }'
```

### 7. 活动横幅

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a Discord event banner for a gaming tournament. Esports style with dynamic angles and energy effects. Team colors: red vs blue. 1200x675 pixels. Include space for event name, date, and prize info. Competitive and exciting mood.",
    "mode": "max"
  }'
```

### 8. 机器人头像

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord bot avatar for a music bot called BeatBot. Friendly robot face with headphones, musical notes floating around. Cyan and white color scheme on dark background. Cute but modern design, reads well as small circle.",
    "mode": "max"
  }'
```

### 9. 表情包生成

```bash
# Generate consistent emoji set
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of a happy pepe-style frog giving thumbs up. Simple, clean design with thick outlines for visibility at small sizes. Green frog, expressive eyes.",
    "session_id": "emoji-pack-001"
  }'

# Sad emoji
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of the same frog character but sad with a single tear. Same art style as before, consistent design.",
    "session_id": "emoji-pack-001"
  }'

# Laughing emoji
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 128x128 Discord emoji of the same frog character laughing hard with tears of joy. Consistent style with previous emojis.",
    "session_id": "emoji-pack-001"
  }'
```

### 10. 服务器助力徽章

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 64x64 Discord role icon for Server Boosters. Premium feel with Discord Nitro pink/purple gradient colors. Lightning bolt or rocket symbol to represent boost. Shiny metallic effect, stands out from other role icons.",
    "mode": "max"
  }'
```

## 最佳实践

### 服务器图标
- **简洁性**：设计应在 32x32 像素时仍可识别
- **对比度**：使用高对比度颜色以提高可见性
- **居中显示**：保持主要元素居中（显示为圆形）
- **无文字**：避免使用文字——在小尺寸下文字难以阅读
- **品牌颜色**：使用一致的品牌/社区颜色

### 角色图标
- **最大尺寸 64x64**：Discord 规定角色图标最大为 64x64
- **简单形状**：复杂细节在小尺寸下会丢失
- **颜色编码**：使用不同的颜色区分不同角色等级
- **一致性**：创建风格统一的角色图标集
- **透明背景**：使用透明背景以增加灵活性

### 横幅与标题
- **安全区域**：将重要元素远离边缘
- **文字空间**：预留文字叠加的位置
- **移动设备友好**：测试在移动设备上的显示效果
- **文件大小**：横幅文件大小应控制在 10MB 以内

### 表情包
- **128x128**：标准的 Discord 表情包尺寸
- **文件大小限制**：保持文件大小在 256KB 以内
- **粗边框**：有助于在小尺寸下提高可见性
- **透明背景**：使用透明背景以增加灵活性
- **强调情感/动作**：突出表情包所表达的情感或动作

## 创建 Discord 图形的提示建议

在创建 Discord 图形时，请在提示中包含以下信息：

1. **确切尺寸**：指定尺寸（如 512x512、960x540、64x64 等）
2. **资产类型**：服务器图标、横幅、角色图标、表情包等
3. **主题/风格**：游戏、动漫、专业、极简等
4. **颜色**：指定具体颜色，或让 AI 根据主题选择
5. **关键元素**：需要包含的符号、吉祥物或图像
6. **可读性**：说明是否需要在小尺寸下仍可清晰显示
7. **文字空间**：说明是否需要预留文字叠加的位置

### 示例提示结构

```
"Create a [size] Discord [asset type] for [community type/name].
Feature [key visual elements] with [color scheme].
Style: [aesthetic description].
[Additional requirements like small-size readability, text space, etc.]"
```

## 模式选择

在生成图形之前，请询问用户：

**“您需要快速且低成本的方案，还是高质量的结果？”**

| 模式 | 适用场景 | 速度 | 质量 |
|------|----------|-------|---------|
| `max` | 最终成品、服务器品牌标识、公开使用的图形 | 较慢 | 最高质量 |
| `eco` | 快速草图、概念探索、批量表情包生成 | 较快 | 良好质量 |

## 多轮创意迭代

使用 `session_id` 进行多次迭代以优化 Discord 图形：

```bash
# Initial server icon concept
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a space exploration gaming community",
    "session_id": "space-server-branding"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the planet more prominent and add some stars in the background. Keep the same color scheme.",
    "session_id": "space-server-branding"
  }'

# Create matching banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a matching 960x540 server banner with the same space theme and color palette",
    "session_id": "space-server-branding"
  }'
```

## 完整的服务器品牌包

生成一套统一的服务器品牌标识材料：

```bash
# 1. Server icon
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a 512x512 Discord server icon for a creative art community called ArtVault. Modern abstract paint splash design, vibrant rainbow colors on dark background.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'

# 2. Server banner
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a matching 960x540 server banner. Extend the paint splash theme across a wider canvas. Same colors and style.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'

# 3. Role icons
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create 3 role icons (64x64 each) for Artist, Moderator, and VIP roles. Use paintbrush for Artist (blue), palette for Mod (orange), and star for VIP (gold). Same art style as the server icon.",
    "session_id": "artvault-branding",
    "mode": "max"
  }'
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| **创建失败：HTTP 422** | 账户余额不足 | 在 eachlabs.ai 充值 |
| 内容违规 | 内容被禁止 | 调整提示以符合 Discord 社区规范 |
| 超时 | 生成过程复杂 | 将客户端超时设置至少为 10 分钟 |
| 图像过大 | 文件大小超出限制 | 请求调整尺寸或简化设计 |

## 相关技能

- `each-sense`：核心 API 文档
- `social-media-graphics`：社交媒体图形制作
- `logo-generation`：品牌标志设计
- `character-design`：吉祥物和角色设计
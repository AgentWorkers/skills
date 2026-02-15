---
name: app-store-screenshots
description: |
  App Store and Google Play screenshot creation with exact platform specs.
  Covers iOS/Android dimensions, gallery ordering, device mockups, and preview videos.
  Use for: app store optimization, ASO, app screenshots, app preview, play store listing.
  Triggers: app store screenshots, aso, app store optimization, play store screenshots,
  app preview, app listing, ios screenshots, android screenshots, app store images,
  app mockup, device mockup, app gallery, store listing
allowed-tools: Bash(infsh *)
---

# 应用商店截图

您可以通过 [inference.sh](https://inference.sh) 命令行工具来生成应用商店截图和预览视频。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a device mockup scene
infsh app run falai/flux-dev-lora --input '{
  "prompt": "iPhone 15 Pro showing a clean modern app interface with analytics dashboard, floating at slight angle, soft gradient background, professional product photography, subtle shadow, marketing mockup style",
  "width": 1024,
  "height": 1536
}'
```

## 平台规格

### Apple App Store (iOS)

| 设备 | 尺寸（像素） | 必需 |
|--------|-----------------|----------|
| iPhone 6.7" (15 Pro Max) | 1290 x 2796 | 必需 |
| iPhone 6.5" (11 Pro Max) | 1284 x 2778 | 必需 |
| iPhone 5.5" (8 Plus) | 1242 x 2208 | 可选 |
| iPad Pro 12.9" (第6代) | 2048 x 2732 | 如果是iPad应用 |
| iPad Pro 11" | 1668 x 2388 | 如果是iPad应用 |

- 每个本地化版本最多需要 **10张截图** |
- 前 **3张截图** 在不滚动的情况下即可显示（非常重要） |
- 格式：PNG或JPEG（JPEG格式不支持透明度）

### Google Play Store (Android)

| 规格 | 要求 |
|------|-------|
| 最小尺寸 | 320像素（任意边长） |
| 最大尺寸 | 3840像素（任意边长） |
| 宽高比 | 16:9或9:16 |
| 每种设备类型最多8张截图 |
| 格式 | PNG或JPEG（24位，不支持透明度） |

- 特色图片：1024 x 500像素（用于展示应用特色） |
- 宣传视频：YouTube链接（可选，但推荐）

## “前3张截图”的重要性

**80% 的应用商店展示中，用户只会看到前3张截图**（在滚动之前）。这三张截图必须：

1. 传达核心价值主张 |
2. 展示最佳功能/效果 |
3. 与竞争对手区分开来

### 截图展示顺序

| 位置 | 内容 | 目的 |
|----------|---------|---------|
| **1** | 核心价值/最佳功能 | 阻止用户滚动，展示应用的功能 |
| **2** | 主要差异化点 | 与竞争对手的不同之处 |
| **3** | 最受欢迎的功能 | 用户最喜爱的功能 |
| **4** | 社交证明或效果展示 | 评分、结果、用户评价 |
| **5-8** | 其他功能 | 辅助功能、设置、集成 |
| **9-10** | 专业功能 | 面向特定用户群体的功能 |

## 截图样式

### 1. 带标题的设备框架

标准样式：设备模型图，应用显示在图片中，标题位于上方或下方。

```
┌──────────────────────────┐
│   "Track Your Habits     │  ← Caption (benefit-focused)
│    Effortlessly"         │
│                          │
│   ┌──────────────────┐   │
│   │                  │   │
│   │   App Screen     │   │  ← Actual app UI in device frame
│   │   Content        │   │
│   │                  │   │
│   │                  │   │
│   └──────────────────┘   │
│                          │
└──────────────────────────┘
```

### 全屏UI（无设备框架）

应用界面占据整个截图，适用于沉浸式应用。

### 实际使用场景

设备展示在真实环境中（例如：有人手持手机、放在桌子上等）。

### 功能亮点（带有标注）

UI截图中用箭头或圆圈标注特定功能。

## 标题编写规则

- **最多2行文字** |
- **侧重于好处，而非功能** |
- **字体大小至少30pt**（在应用商店中必须可读）

### 示例

```
❌ Feature-focused:
"Push Notification System"
"Calendar View with Filters"
"Data Export Functionality"

✅ Benefit-focused:
"Never Miss a Deadline Again"
"See Your Week at a Glance"
"Share Reports in One Tap"
```

## 生成截图

### 核心价值截图（位置1）

```bash
# Clean device mockup with hero feature
infsh app run falai/flux-dev-lora --input '{
  "prompt": "modern iPhone showing a beautiful fitness tracking app with activity rings and workout summary, device floating at slight angle against soft purple gradient background, professional product shot, clean minimal composition, subtle reflection",
  "width": 1024,
  "height": 1536
}'
```

### 功能亮点截图

```bash
# Feature callout style
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "app store screenshot style, iPhone showing a messaging app with AI writing suggestions highlighted, clean white background, subtle UI callout arrows, professional marketing asset, modern design",
  "size": "2K"
}'
```

### 实际使用场景截图

```bash
# Device in real-world setting
infsh app run falai/flux-dev-lora --input '{
  "prompt": "person holding iPhone showing a cooking recipe app, kitchen background with ingredients, warm natural lighting, over-the-shoulder perspective, lifestyle photography, authentic feeling",
  "width": 1024,
  "height": 1536
}'
```

### 功能对比（使用前/使用后）

```bash
# Split comparison
infsh app run infsh/stitch-images --input '{
  "images": ["before-screenshot.png", "after-screenshot.png"],
  "direction": "horizontal"
}'
```

## 预览视频

### Apple App Store

| 规格 | 要求 |
|------|-------|
| 时长 | 15-30秒 |
| 方向 | 纵屏或横屏（与应用一致） |
| 音频 | 可选（在应用商店中自动循环播放） |
| 格式 | H.264、.mov或.mp4 |

### Google Play

| 规格 | 要求 |
|------|-------|
| 来源 | YouTube链接 |
| 时长 | 建议30秒-2分钟 |
| 方向 | 横屏优先 |

### 预览视频结构

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| 开场部分 | 0-3秒 | 展示核心功能或令人惊叹的效果 |
| 功能1 | 3-10秒 | 演示主要功能 |
| 功能2 | 10-18秒 | 第二个关键功能 |
| 功能3 | 18-25秒 | 第三个功能或用户评价 |
| 呼吁行动 | 25-30秒 | 结尾屏幕显示应用图标 |

```bash
# Generate preview video scenes
infsh app run google/veo-3-1-fast --input '{
  "prompt": "smooth screen recording style, finger tapping on a modern mobile app interface, swiping between screens showing charts and data visualizations, clean UI transitions, professional app demo"
}'
```

## 本地化

每种语言都需要对应的截图。优先级如下：

| 市场 | 本地化程度 |
|--------|-------------------|
| 主要市场 | 完整本地化：新的截图 + 翻译后的标题 |
| 次要市场 | 翻译后的标题，使用相同的截图 |
| 其他市场 | 默认使用英文 |

主要本地化语言：英文、日文、韩文、简体中文、德文、法文、西班牙文、葡萄牙文（巴西）

## A/B测试（Google Play）

Google Play控制台支持应用商店列表的实验：

- 测试不同的截图展示顺序 |
- 测试是否使用设备框架 |
- 测试不同的标题 |
- 测试不同的颜色方案 |
- 运行7天以上，且流量达到50%以上才能获得显著效果

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 将设置界面作为截图 | 没有人关心设置界面 | 展示核心价值，而非应用的基础功能 |
| 新手引导流程的截图 | 展示了使用过程中的麻烦，而非应用的价值 | 展示应用的实际使用状态 |
| 文字过多 | 在应用商店中难以阅读 | 最多2行，字体大小至少30pt |
| 尺寸不正确 | 被应用商店拒绝 | 使用平台规定的尺寸 |
| 所有截图看起来都一样 | 用户没有理由滚动 | 变换截图的构图和内容 |
| 标题侧重于功能 | 无法传达应用的好处 | 例如：“Never Miss a Deadline”（不错过任何截止日期）优于“Push Notifications”（推送通知） |
| UI过时 | 会让应用显得被抛弃 | 每次重大更新时更新截图 |
| 没有核心价值截图 | 第一印象不佳 | 第1张截图应该是最好的展示 |

## 检查清单

- [ ] 使用目标平台的正确尺寸 |
- [ ] 前3张截图能够传达核心价值 |
- [ ] 标题侧重于好处，最多2行 |
- [ ] 不包含新手引导或设置界面 |
- [ ] 预览视频时长为15-30秒，开头3秒内有吸引人的内容 |
- [ ] 为主要市场进行本地化 |
- [ ] Google Play需要特色图片（1024x500像素） |
- [ ] 截图与当前应用版本保持一致 |
- [ ] 准备了A/B测试的多种版本 |

## 相关技能

```bash
npx skills add inferencesh/skills@ai-image-generation
npx skills add inferencesh/skills@ai-video-generation
npx skills add inferencesh/skills@image-upscaling
npx skills add inferencesh/skills@prompt-engineering
```

浏览所有应用：`infsh app list`
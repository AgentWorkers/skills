---
name: app-store-screenshots
description: "**使用精确平台规格生成App Store和Google Play应用截图的方法**  
涵盖iOS/Android设备的屏幕尺寸、截图的排列方式、设备模型图以及预览视频的制作。适用于：应用商店优化（ASO）、应用截图制作、应用预览、Google Play商店应用列表展示等场景。  
**相关操作包括：**  
- 生成适用于App Store和Google Play的应用截图  
- 根据设备规格调整截图尺寸  
- 设计截图的布局和样式  
- 制作设备模型图以展示应用界面  
- 创建预览视频以展示应用功能  
**适用场景：**  
- 应用商店优化（App Store Optimization, ASO）  
- 应用截图制作  
- 应用预览（App Preview）  
- Google Play商店应用列表展示  
**相关术语：**  
- App Store截图（App Store Screenshots）  
- Google Play截图（Google Play Screenshots）  
- 设备模型图（Device Mockups）  
- 应用界面预览（App Interface Preview）  
- 应用商店优化（App Store Optimization, ASO）  
- 应用列表展示（App Listing）  
**注意事项：**  
- 确保截图符合各平台的要求（如分辨率、格式等）  
- 使用专业的截图工具和软件来提高截图质量  
- 定期更新设备模型图以反映最新的设备设计  
**参考资料：**  
- [App Store截图生成指南](https://developer.apple.com/documentation/en-us/app-store/app-store-screenshots)  
- [Google Play截图生成指南](https://developers.google.com/playstore/docs/guide/getting-started/creating-app-screenshots)"
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

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。该脚本不需要任何特殊权限或后台进程。如需手动安装和验证，请参考 [此处](https://dist.inference.sh/cli/checksums.txt)。

## 平台要求

### Apple 应用商店（iOS）

| 设备 | 尺寸（像素） | 必需 |
|--------|-----------------|----------|
| iPhone 6.7" (15 Pro Max) | 1290 x 2796 | 必需 |
| iPhone 6.5" (11 Pro Max) | 1284 x 2778 | 必需 |
| iPhone 5.5" (8 Plus) | 1242 x 2208 | 可选 |
| iPad Pro 12.9" (第6代) | 2048 x 2732 | 如果是针对 iPad 的应用 |
| iPad Pro 11" | 1668 x 2388 | 如果是针对 iPad 的应用 |

- 每个本地化版本最多需要 **10张** 截图 |
- 前 **3张** 截图在用户滚动之前就会显示（非常重要） |
- 格式：PNG 或 JPEG（JPEG 格式不支持透明度）

### Google Play 商店（Android）

| 规格 | 要求 |
|------|-------|
| 最小尺寸 | 320 像素（任意边长） |
| 最大尺寸 | 3840 像素（任意边长） |
| 宽高比 | 16:9 或 9:16 |
| 每种设备类型最多允许 **8张** 截图 |
| 格式 | PNG 或 JPEG（24位颜色，不支持透明度） |

- 特色图片：1024 x 500 像素（用于展示应用亮点） |
- 宣传视频：YouTube 链接（可选，但推荐）

## “前3张截图”的重要性

**80% 的应用商店展示中，用户只会看到前3张截图**（在用户滚动之前）。这3张截图必须：

1. 传达应用的核心价值主张 |
2. 展示最佳功能或效果 |
3. 与竞争对手区分开来

### 截图展示顺序

| 位置 | 内容 | 用途 |
|----------|---------|---------|
| **1** | 核心价值/最佳功能 | 阻止用户滚动，展示应用的核心功能 |
| **2** | 独特卖点 | 说明应用与竞争对手的不同之处 |
| **3** | 最受欢迎的功能 | 用户最喜爱的功能 |
| **4** | 用户评价或成果展示 | 用户评分、使用效果等 |
| **5-8** | 其他功能 | 辅助功能、设置、集成内容 |
| **9-10** | 专属功能 | 面向特定用户群体的功能 |

## 截图样式

### 1. 带标题的设备框架

标准样式：设备模型图，应用显示在其中，标题文字位于上方或下方。

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

### 全屏 UI（无设备框架）

应用界面覆盖整个截图，适用于沉浸式体验的应用。

### 生活场景展示

设备在实际使用场景中的画面（例如：人物手持手机、放在桌面上等）。

### 功能亮点展示（带有标注）

截图中用箭头或圆圈标注特定功能。

## 标题编写规则

- **最多2行文字** |
- **侧重于优势**，而非功能描述 |
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

### 生活场景截图

```bash
# Device in real-world setting
infsh app run falai/flux-dev-lora --input '{
  "prompt": "person holding iPhone showing a cooking recipe app, kitchen background with ingredients, warm natural lighting, over-the-shoulder perspective, lifestyle photography, authentic feeling",
  "width": 1024,
  "height": 1536
}'
```

### 功能对比截图（使用前/使用后）

```bash
# Split comparison
infsh app run infsh/stitch-images --input '{
  "images": ["before-screenshot.png", "after-screenshot.png"],
  "direction": "horizontal"
}'
```

## 预览视频

### Apple 应用商店

| 规格 | 要求 |
|------|-------|
| 时长 | 15-30秒 |
| 方向 | 纵屏或横屏（与应用实际方向一致） |
| 音频 | 可选（在应用商店中自动循环播放） |
| 格式 | H.264、.mov 或 .mp4 |

### Google Play

| 规格 | 要求 |
|------|-------|
| 来源 | YouTube 链接 |
| 时长 | 建议30秒至2分钟 |
| 方向 | 横屏优先 |

### 预览视频结构

| 部分 | 时长 | 内容 |
|---------|----------|---------|
| 开场 | 0-3秒 | 展示应用的核心效果或令人惊叹的功能 |
| 功能1 | 3-10秒 | 展示主要功能 |
| 功能2 | 10-18秒 | 第二个关键功能 |
| 功能3 | 18-25秒 | 第三个功能或用户评价 |
| 呼吁行动（CTA） | 25-30秒 | 结尾显示应用图标 |

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
| 次要市场 | 只翻译标题，使用相同的截图 |
| 其他市场 | 默认使用英文 |

主要本地化语言：英文、日文、韩文、简体中文、德文、法文、西班牙文、葡萄牙文（巴西）

## A/B测试（Google Play）

Google Play 控制台支持应用商店列表的实验：

- 测试不同的截图展示顺序 |
- 测试是否使用设备框架 |
- 测试不同的标题样式 |
- 运行7天以上，且流量超过50%才能获得显著效果

## 常见错误

| 错误 | 问题 | 解决方案 |
|---------|---------|-----|
| 选择设置界面作为截图 | 用户不关心设置信息 | 展示应用的核心价值，而非技术细节 |
| 选择引导流程的截图 | 展示的是使用过程中的麻烦，而非应用的实际效果 | 展示应用的实际使用状态 |
| 文字过多 | 在应用商店中难以阅读 | 标题最多2行，字体大小至少30pt |
| 尺寸不正确 | 被应用商店拒绝 | 使用平台规定的尺寸 |
| 所有截图看起来相同 | 用户没有滚动的需求 | 变换截图的构图和内容 |
| 标题只描述功能 | 无法传达应用的优势 | 例如：“Never Miss a Deadline”（不错过任何截止日期）优于“Push Notifications”（推送通知） |
| UI 界面过时 | 给人应用被弃用的印象 | 每次重大更新时更新截图 |
| 没有核心价值截图 | 第一印象不佳 | 第1张截图应是最能体现应用优势的图片 |

## 检查清单

- [ ] 使用目标平台的正确尺寸 |
- [ ] 前3张截图能够传达应用的核心价值 |
- [ ] 标题侧重于优势，最多2行 |
- [ ] 不包含引导或设置界面 |
- [ ] 预览视频时长为15-30秒，开头3秒内有吸引人的内容 |
- [ ] 为主要市场完成本地化 |
- [ ] Google Play 专用特色图片（1024x500像素） |
- [ ] 截图与当前应用版本保持一致 |
- [ ] 准备了A/B测试的多种版本 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@prompt-engineering
```

查看所有应用：`infsh app list`
---
name: meta-ads-analyser
description: 分析提取的 Meta 广告创意，并生成一份专业的策略报告。在运行 `/meta_ads extractor` 命令后，使用该报告来生成一份清晰、有条理的分析文档，其中内嵌的视频/图片会按照用户转化路径（funnel）和着陆页（landing page）进行分类。
---
# 元广告分析器

根据提取的元广告创意生成专业的广告策略分析报告。

## 先决条件

- 从 `/meta_ads extractor` 中提取的广告素材（图片、视频、着陆页截图）
- 广告创意分析数据（吸引人的开场语句、脚本内容、所引发的情绪、呼叫行动（CTA）以及广告的优缺点）
- 着陆页分析数据（标题、转化策略、用户转化路径）

## 输入

提取后的广告素材文件夹，通常位于：
```
~/clawd/output/meta-ads/{advertiser-slug}/
├── {slug}-video-01.mp4
├── {slug}-video-02.mp4
├── {slug}-image-01.jpg
├── {slug}-image-02.jpg
├── landing-{page-name}.jpg
└── ...
```

## 分析流程

### 1. 分析每个广告创意

对于每个广告创意，需要识别以下信息：
- **宽高比** — 图像或视频的尺寸及比例（1:1、4:5、9:16、16:9）
- **时长** — 视频的时长（以秒为单位）
- **吸引人的开场元素** — 能够阻止用户继续滚动页面的视觉或文字内容
- **核心信息与价值主张** — 广告的主要信息及所提供的价值
- **视觉元素顺序** — 视频中的场景或元素排列顺序
- **引发的情绪** — 广告主要引发的情绪（好奇心、恐惧、渴望等）
- **呼叫行动（CTA）** — 用户应采取的行动以及操作过程中的阻力程度
- **优势** — 广告中的成功之处
- **不足之处** — 需要改进的地方

使用视觉模型分析图片，使用 Gemini 工具分析视频。

**获取尺寸信息的方法：**
```bash
# Images (macOS)
sips -g pixelWidth -g pixelHeight image.jpg

# Videos
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 video.mp4
```

**常见的宽高比：**
| 比例 | 使用场景 |
|-------|----------|
| 1:1 | 信息流（通用格式） |
| 4:5 | 信息流（推荐格式） |
| 9:16 | 视频故事/短片 |
| 16:9 | 横屏视频 |

### 2. 分析着陆页

对于每个着陆页，需要识别以下信息：
- **标题** — 广告的主要价值主张
- **转化策略** — 促进转化的关键元素（如用户证言、紧迫感等）
- **转化路径** — 从着陆页到购买或注册的流程
- **优势** — 能有效促进转化的元素
- **不足之处** — 缺失的元素或阻碍转化的环节

### 3. 组织广告数据

根据广告的目标着陆页对广告进行分类。每个广告组包含该着陆页以及所有指向该着陆页的广告。

常见的广告转化路径类型：
- **TOFU（漏斗顶部）** — 提升用户意识的内容，如引导性内容、问卷调查、免费资源
- **BOFU（漏斗底部）** — 直接提供产品或服务的信息，如购买链接、注册表单

### 4. 寻找广告策略模式

分析以下广告策略：
- 信誉构建（使用公司标志、资质证明、用户证言等）
- 价格锚定策略
- 伪装成普通内容的广告（不易被识别为广告）
- 以用户身份为核心的文案设计
- 广告创意的多样化测试（使用不同版本）

## 输出格式

使用以下模板结构生成一个独立的 HTML 报告。

### 报告结构

```
1. Header
   - Advertiser name
   - Stats (# ads, # funnels, date)

2. Strategy Overview (TOP)
   - High-level acquisition strategy
   - Funnel flow visualization
   - Creative testing patterns
   - Key takeaways (actionable insights)

3. Funnel Sections (one per landing page)
   - Funnel header (name, URL)
   - Landing page card (screenshot + analysis)
   - Ad cards grid (media + analysis for each)
   
4. Footer
   - Source attribution
   - Date generated
```

### 设计规范

- **简洁明了的设计** — 白色背景，简单的字体排版
- **避免使用深色渐变或复杂的样式** — 使报告看起来像 PDF 或 Notion 文档
- **内嵌媒体文件** — 视频和图片可以正常播放
- **移动设备友好** — 广告卡片采用响应式布局
- **添加标识以便快速查看信息** — 包括 TOFU/BOFU、视频/图片类型、表现最佳的广告创意、宽高比等信息

### 广告卡片格式

每个广告卡片应显示以下内容：
```
[Media: video/image]
[Badges: Type | Funnel Stage | Aspect Ratio | Duration (if video)]
[Title]
[Analysis fields: Hook, Script, Emotion, Strengths, Gaps]
```

**在每个广告卡片上添加宽高比标识**，以便一目了然地了解广告类型（例如：“所有 TOFU 广告的宽高比为 4:5，BOFU 广告的宽高比为 1:1”）。

完整的 HTML/CSS 模板请参见 `templates/report-template.html`。

## 交付方式

1. 在广告素材文件夹中生成 HTML 文件：
   ```
   ~/clawd/output/meta-ads/{advertiser-slug}/{slug}-analysis.html
   ```

2. 将整个文件夹（包含 HTML 文件和所有媒体文件）压缩成 ZIP 文件
3. 通过 Telegram 发送文件，并附上说明文件内容的文字说明

**重要提示：** HTML 文件中的媒体文件路径是相对路径。请务必以 ZIP 格式发送文件，以便接收者可以在本地打开文件并查看所有内容。

## 示例工作流程

```
User: Analyze the EricPartaker ads we extracted

1. Read assets folder: ~/clawd/output/meta-ads/ericpartaker/
2. Analyze each video with Gemini / image with vision
3. Analyze landing page screenshots
4. Map ads to landing pages (identify 3 funnels)
5. Identify strategy patterns
6. Generate HTML report
7. Zip folder
8. Send to user
```

## 集成方式

该工具的设计遵循 `/meta_ads extractor` 的数据格式：

```
/meta_ads_extractor → downloads assets
/meta_ads_analyser → generates strategy report
```

此外，该工具还可以与以下工具集成：
- **ad-creative-analysis** — 提供详细的单个广告分析报告
- **landing-page-analysis** — 进一步深入分析着陆页的表现
---
name: ad-ready
description: 使用 ComfyDeploy 中的 Ad-Ready 流程，可以从产品 URL 生成专业的广告图片。当用户希望为任何产品创建广告时，只需提供产品 URL 即可（可选提供品牌信息，支持 70 多个品牌），同时还可以设置目标受众阶段。该流程支持模型/人才的整合、基于品牌特点的创意设计以及多种格式的输出。与 Morpheus（手动时尚摄影服务）不同，Ad-Ready 是基于 URL 运作的、具备品牌识别功能的，并且能够根据目标受众阶段进行广告内容调整。
---

# Ad-Ready：AI广告图片生成器

使用ComfyDeploy上的四阶段AI流程，根据产品URL生成专业的广告图片。

## ⚠️ 重要提示：必填输入项检查清单

在运行任何广告生成任务之前，系统必须确保提供以下所有输入项：

| 输入项 | 是否必填 | 获取方式 |
|-------|-----------|---------------|
| `--product-url` | ✅ 必填 | 用户提供产品页面URL |
| `--product-image` | ✅ 必填 | 从产品页面下载，或由用户提供 |
| `--logo` | ✅ 必填 | 从品牌官网下载或在线搜索。必须是图片文件 |
| `--reference` | ✅ 推荐 | 我们希望复制的现有广告样式。可在线搜索或使用之前生成的图片 |
| `--brand-profile` | ✅ 必填 | 从目录中选择，或先运行`brand-analyzer`技能生成。如果知道品牌名称，切勿填写“无品牌” |
| `--prompt-profile` | ✅ 必填 | 根据活动目标选择 |
| `--aspect-ratio` | 默认值：4:5 | 如需根据平台进行调整 |
| `--model` | 可选 | 从目录中选择模型/人才面部图片，或由用户提供 |

### 🚨 请勿跳过以下步骤：

1. **产品图片** — 从产品URL下载主要的产品照片。抓取工具可能不稳定，务必手动提供产品图片。
2. **品牌标志** — 从品牌官网下载标志，或在线搜索“{品牌名称} logo”。必须是清晰的标志图片（PNG格式优先）。
3. **品牌资料** — 如果品牌不在目录中，请先运行`brand-analyzer`技能生成品牌资料。如果知道品牌名称，切勿填写“无品牌”。
4. **参考图片** — 搜索与我们要生成的广告风格相匹配的现有广告或视觉素材。这些素材可以来自之前的生成结果、品牌的广告活动或在线资源，这会显著提升输出质量。

## 自动准备工作流程

当用户请求生成广告时，请按照以下流程操作：

```
1. User provides: product URL + brand name + objective

2. CHECK brand profile exists:
   → ls ~/clawd/ad-ready/configs/Brands/ | grep -i "{brand}"
   → If not found: run brand-analyzer skill first
   
3. DOWNLOAD product image:
   → Visit the product URL in browser or fetch the page
   → Find and download the main product image
   → Save to /tmp/ad-ready-product.jpg

4. DOWNLOAD brand logo:
   → Search "{brand name} logo PNG" or fetch from brand website
   → Download clean logo image
   → Save to /tmp/ad-ready-logo.png

5. FIND reference image:
   → Search for "{brand name} advertisement" or similar
   → Or use a previously generated ad that has the right style
   → Save to /tmp/ad-ready-reference.jpg

6. SELECT prompt profile based on objective:
   → Awareness: brand discovery, first impressions
   → Interest: engagement, curiosity
   → Consideration: comparison, features
   → Evaluation: deep dive, decision support
   → Conversion: purchase intent, CTAs (most common)
   → Retention: re-engagement
   → Loyalty: brand advocates
   → Advocacy: referral, community

7. RUN the generation with ALL inputs filled
```

## 使用方法

### 完整命令（推荐）：
```bash
COMFY_DEPLOY_API_KEY="$KEY" uv run ~/.clawdbot/skills/ad-ready/scripts/generate.py \
  --product-url "https://shop.example.com/product" \
  --product-image "/tmp/product-photo.jpg" \
  --logo "/tmp/brand-logo.png" \
  --reference "/tmp/reference-ad.jpg" \
  --model "models-catalog/catalog/images/model_15.jpg" \
  --brand-profile "Nike" \
  --prompt-profile "Master_prompt_05_Conversion" \
  --aspect-ratio "4:5" \
  --output "ad-output.png"
```

### 自动获取模式（自动下载产品图片和标志）：
```bash
COMFY_DEPLOY_API_KEY="$KEY" uv run ~/.clawdbot/skills/ad-ready/scripts/generate.py \
  --product-url "https://shop.example.com/product" \
  --brand-profile "Nike" \
  --prompt-profile "Master_prompt_05_Conversion" \
  --auto-fetch \
  --output "ad-output.png"
```

`--auto-fetch`标志将：
- 从产品URL下载主要产品图片
- 搜索并下载品牌标志
- 两者都会自动上传到ComfyDeploy

## API详情

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署ID：** `e37318e6-ef21-4aab-bc90-8fb29624cd15`

## ComfyDeploy输入变量

以下是ComfyDeploy部署所期望的变量名称：

| 变量 | 类型 | 说明 |
|----------|------|-------------|
| `product_url` | 字符串 | 需要抓取的产品页面URL |
| `product-image` | 图片URL | 上传到ComfyDeploy的产品图片 |
| `model` | 图片URL | 参考用的模型/人才面部图片 |
| `reference` | 图片URL | 参考用的广告图片样式 |
| `brand-profile` | 枚举 | 目录中的品牌名称 |
| `prompt-profile` | 枚举 | 活动阶段的提示语 |
| `aspect-ratio` | 枚举 | 输出格式 |

## 四阶段流程（内部工作原理）

### 第1阶段：产品抓取
- Gemini Flash访问产品URL
- 提取：标题、描述、功能、价格、图片
- ⚠️ 图片抓取是最容易出现问题的部分——务必手动提供产品图片

### 第2阶段：活动概要生成（关键步骤）
- 使用品牌身份信息JSON和产品数据生成10点概要
- **后续所有步骤都依赖于概要的质量**
- 概要涵盖：战略目标、核心信息、视觉风格、产品定位、摄影师、艺术方向、场景、材质、签名元素

### 第3阶段：蓝图生成
- 根据活动阶段、概要、产品信息及关键词库生成完整的蓝图JSON
- Gemini Flash生成完整的蓝图JSON
- 包括：场景设计、制作流程、图形设计、灯光效果、构图、材质选择、呼叫行动（CTA）元素

### 第4阶段：图片生成
- Nano Banana Pro（Imagen 3.0）生成最终图片
- 使用蓝图JSON以及所有参考图片（产品图片、人才图片、标志、风格参考）

### 支持的参考节点
- `pose_ref` — 强制使用特定姿势（需精确复制）
- `photo_style_ref` — 复制照片风格（⚠️ 可能过于刻板，正在优化中）
- `location_ref` — 复制场景背景和色彩调色板

## 品牌资料

### 现有目录（70多个品牌）：
```bash
ls ~/clawd/ad-ready/configs/Brands/*.json | sed 's/.*\///' | sed 's/\.json//'
```

### 创建新品牌资料：
使用`brand-analyzer`技能：
```bash
GEMINI_API_KEY="$KEY" uv run ~/.clawdbot/skills/brand-analyzer/scripts/analyze.py \
  --brand "Brand Name" --auto-save
```

该技能会生成完整的品牌身份信息JSON，并自动保存到目录中。

## 提示语模板（活动阶段）

| 模板 | 适用阶段 | 适用场景 |
|---------|-------|----------|
| `Master_prompt_01_Awareness` | 品牌认知 | 品牌发现、初次印象 |
| `Master_prompt_02_Interest` | 激发兴趣 | 吸引用户注意力、引发好奇心 |
| `Master_prompt_03_Consideration` | 考虑购买 | 对比产品特点 |
| `Master_prompt_04_Evaluation` | 评估产品 | 深入了解、辅助决策 |
| `Master_prompt_05_Conversion` | 促进转化 | 引导购买行为、提供呼叫行动 |
| `Master_prompt_06_Retention` | 提升留存率 | 重新吸引用户、增强忠诚度 |
| `Master_prompt_07_Loyalty` | 增强忠诚度 | 激发用户倡导行为 |
| `Master Prompt_08_Advocacy` | 品牌推广 | 促进用户推荐、扩大社区影响力 |

**选择提示语的依据：**
- 大多数广告：**促进转化**（引导购买）
- 新产品发布：**品牌认知**  
- 再营销：**考虑购买**或**评估产品**  
- 现有客户：**提升留存率**或**增强忠诚度**  

## 宽高比

| 宽高比 | 适用场景 |
|-------|----------|
| `4:5` | **默认值** | Instagram动态、Facebook |
| `9:16` | TikTok短视频、Reels视频 |
| `1:1` | 方形图片 |
| `16:9` | YouTube视频、横屏广告 |
| `5:4` | 其他横屏格式 |

## 模型目录

人才/面部参考模型：`~/clawd/models-catalog/catalog/`

**优先级：** 用户提供的模型 > 目录中的模型 > 无模型（仅使用产品图片的广告）

## 已知限制

1. **产品图片抓取不稳定** — 尽可能手动提供产品图片。
2. **风格参考可能过于刻板** — 参考风格可能会被过度复制。
3. **部分网站会阻止抓取** — Armani品牌的数据抓取效果较好，其他网站可能返回错误数据。
4. **自动格式化功能仍处于测试阶段** — 存在漏洞和边缘情况。
5. ** Gemini算法可能出现问题** — 在复杂处理过程中偶尔会出现错误。

## Ad-Ready与Morpheus的对比

| 功能 | Ad-Ready | Morpheus |
|---------|----------|----------|
| 输入方式 | 通过产品URL自动抓取 | 需手动提供产品图片 |
| 品牌信息支持 | 支持70多个品牌资料 | 不支持 |
| 活动阶段划分 | 分为8个阶段 | 无阶段划分 |
| 创意方向 | 根据活动概要自动生成 | 基于预设的相机、镜头等参数 |
| 适用场景 | 产品广告活动 | 时尚/生活方式类编辑图片 |
| 控制程度 | 高度自动化（基于目标驱动） | 详细控制每个视觉元素 |

## 源代码仓库

- GitHub: https://github.com/PauldeLavallaz/ads_SV
- 本地克隆地址：~/clawd/ad-ready/
- Patreon文档：https://www.patreon.com/posts/from-product-to-149933468

## API密钥

需要使用ComfyDeploy的API密钥。请通过`COMFY_DEPLOY_API_KEY`环境变量进行设置。
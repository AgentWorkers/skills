---
name: morpheus-fashion-design
description: |
  Generate professional advertising images with AI models holding/wearing products.
  
  ✅ USE WHEN:
  - Need a person/model in the image WITH a product
  - Creating fashion ads, product campaigns, commercial photography
  - Want consistent model face across multiple shots
  - Need professional lighting/camera simulation
  - Input: product image + model reference (or catalog)
  
  ❌ DON'T USE WHEN:
  - Just editing/modifying an existing image → use nano-banana-pro
  - Product-only shot without a person → use nano-banana-pro
  - Already have the hero image, need variations → use multishot-ugc
  - Need video, not image → use veed-ugc after generating image
  - URL-based product fetch with brand profile → use ad-ready instead
  
  OUTPUT: Single high-quality PNG image (2K-4K resolution)
---

# Morpheus 时尚设计

使用 ComfyDeploy 的 Morpheus 时尚设计工作流生成专业的时尚/产品广告图片。

## ⚠️ 重要规则：切勿使用自动值

**配置包的设置绝对不能设置为 `auto` 或 `AUTO`。**

`auto` 表示使用默认值，这将生成内容空洞、缺乏创意方向的图片。

以下列出的配置选项仅供参考，您可以根据实际需求提供自定义值，以选择最符合要求的配置。

### 配置包选择指南

对于每一代图片生成，都需要根据创意要求仔细选择相应的配置参数：

| 配置包 | 选择方法 |
|------|---------------|
| `style_pack` | 与品牌风格匹配：豪华风格→`premium_restraint`，运动风格→`cinematic_realism`，街头风格→`street_authentic` |
| `camera_pack` | 真正的摄影师会使用哪种相机？运动场景→`sony_a1`，时尚杂志风格→`hasselblad_x2d`，街头场景→`leica_m6` |
| `lens_pack` | 适合人像拍摄的镜头？是否需要变形镜头？是否需要广角镜头？需根据拍摄类型和氛围选择 |
| `lighting_pack` | 剧本中描述的光线条件是什么？黄金时刻？还是室内摄影？请据此选择合适的灯光设置 |
| `pose_discipline_pack` | 模特的动作是什么？运动场景→`sport_in_motion`，商业场景→`commercial_front_facing` |
| `film_texture_pack` | 适合温暖色调的时尚杂志风格→`kodak_portra_400`，适合电影风格的→`kodak_vision3_500t`，适合干净数字效果的→`digital_clean_no_emulation` |
| `environment_pack` | 与剧本描述的环境相匹配：海滩→`beach_minimal`，城市→`urban_glass_steel`，自然环境→提供参考图片 |
| `color_science_pack` | 适合温暖色调？还是冷色调？需要电影风格的对比度？根据氛围选择 |
| `time_weather_pack` | 场景发生在什么时间？黄金时刻？正午？阴天？ |

### 示例：Oakley 滑雪广告活动
```python
style_pack = "cinematic_realism"  # NOT auto - sports action needs energy
camera_pack = "sony_a1"            # Fast sports camera
lens_pack = "wide_distortion_controlled"  # Capture the action
lighting_pack = "golden_hour_backlit"     # Alpine dramatic lighting
pose_discipline_pack = "sport_in_motion"  # Rider in action
time_weather_pack = "golden_hour_clear"   # Mountain conditions
```

### 自定义值
如果预设选项都不符合要求，您可以输入自定义的描述性字符串：
```python
lighting_pack = "harsh alpine midday sun reflecting off fresh powder"
environment_pack = "snowpark with metal rails and pristine packed snow"
```

## 概述

Morpheus 时尚设计是一个全面的人工智能工作流，用于创建高质量的商业摄影作品，具备以下特点：
- 产品与图片的完美融合
- 模特面部表情的一致性
- 专业的灯光和相机设置
- 与品牌风格高度一致的创意方向

## API 详细信息

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署 ID：** `1e16994d-da67-4f30-9ade-250f964b2abc`（生产环境）

## 必需输入的信息

### 图片（必须是 URL）
1. **product** - 产品图片的 URL
2. **model** - 模特的正面参考图片
3. **logo** - 品牌标志（如无需使用，请留空）

## 🎭 模特图库

当没有指定具体模特时，可以使用一个包含 114 张 AI 生成模特图片的精选图库。

### 仓库
**GitHub：** `https://github.com/PauldeLavallaz/model_management`

### ⚠️ 优先级：用户提供的模特图片优先
如果用户提供了模特图片，请直接使用该图片。图库仅在没有指定模特时使用。

### 设置（首次安装）
```bash
# Clone the catalog to your workspace
git clone https://github.com/PauldeLavallaz/model_management.git models-catalog
```

### 更新图库
```bash
cd models-catalog && git pull
```

### 本地路径（如果已克隆）
`~/clawd/models-catalog/catalog/images/`

### 图库结构
```
models-catalog/
└── catalog/
    ├── catalog.json      # Full metadata for all models
    └── images/           # Model reference photos (model_01.jpg - model_114.jpg)
```

### 使用图库

**模特选择的优先顺序：**
1. 用户提供了模特图片 → 直接使用该图片
2. 用户描述了所需的模特 → 在图库中搜索并选择最合适的模特
3. 未指定模特 → 根据活动要求选择合适的模特

### 在图库中搜索模特
```bash
# List all models with basic info
cat models-catalog/catalog/catalog.json | jq '[.talents[] | {id, name, gender, ethnicity, tags: .tags[0:2]}]'

# Find models by ethnicity
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.ethnicity == "hispanic") | {id, name, description}]'

# Find models by tag
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.tags[] == "commercial") | {id, name, ethnicity}]'

# Find models by gender
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.gender == "male") | {id, name, ethnicity}]'
```

### 模特信息
每个模特条目包含以下信息：
- `id`：唯一标识符（model_01, model_02 等）
- `name`：模特名称
- `gender`：女性、男性、非二元性别
- `ethnicity`：非洲裔、亚洲裔、白人、西班牙裔、混血等
- `age_group`：年轻成人、成人、成熟
- `tags`：时尚杂志、商业、美容、生活方式、前卫等
- `description`：模特的外貌特征及适用场景
- `image_path`：模特参考图片的路径

### 示例：选择模特
```bash
# For an Argentine campo/gaucho campaign, find hispanic females with commercial tags:
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.ethnicity == "hispanic" and .gender == "female" and (.tags[] == "commercial" or .tags[] == "lifestyle")) | {id, name, description}]'

# Then use the selected model:
--model "models-catalog/catalog/images/model_08.jpg"
```

### 创意要求
1. **详细的活动描述**，包括：
   - 场景/地点信息
   - 模特的姿势和动作
   - 产品的摆放方式及互动方式
   - 光线和氛围
   - 摄影技巧
   - 视觉风格
2. **目标受众** 的详细信息，包括：
   - 人口统计特征
   - 心理特征
   - 兴趣和生活方式

### 配置包

| 配置包 | 可选选项 |
|------|---------|
| `style_pack` | auto, premium_restraint, editorial_precision, cinematic_realism, cinematic_memory, campaign_hero, product_truth, clean_commercial, street_authentic, archive_fashion, experimental_authorial |
| `shot_pack` | auto, full_body_wide, medium_shot, close_up, low_angle_hero, three_quarter, waist_up, 等 |
| `camera_pack` | auto, arri_alexa35, canon_r5, hasselblad_x2d, leica_m6, sony_a1, 等 |
| `lens_pack` | auto, cooke_anamorphic_i_50, leica_noctilux_50, zeiss_otus_55, 等 |
| `lighting_pack` | auto, golden_hour_backlit, natural_window, studio_three_point, 等 |
| `pose_discipline_pack` | auto, commercial_front_facing, street_style_candid_walk, sport_in_motion, 等 |
| `film_texture_pack` | auto, kodak_portra_400, fujifilm_velvia_50, digital_clean_no_emulation, 等 |
| `color_science_pack` | auto, neutral_premium_clean, warm_golden_editorial, cinematic_low_contrast, 等 |
| `environment_pack` | AUTO, beach_minimal, urban_glass_steel, street_crosswalk, 等 |
| `time_weather_pack` | auto, golden_hour_clear, bright_midday_sun, overcast_winter_daylight, 等 |
| `branding_pack` | logo_none, logo_discreet_lower, logo_top_corner, logo_center_watermark, logo_integrated |
| `intent` | auto, awareness, consideration, conversion, retention |
| `aspect_ratio` | 9:16, 16:9, 1:1, 4:5, 5:4, 3:4, 4:3 |

## 工作流程

1. **接收包含品牌和产品信息的请求**
2. **根据品牌身份和活动目标制定创意要求**
3. **确定目标受众**（包括人口统计和心理特征）
4. **准备图片**：
   - 下载产品图片
   - 下载/查找模特参考图片（正面照片）
   - 上传到 ComfyDeploy 的存储空间以获取图片的 URL
5. **根据创意方向选择相应的配置包**
6. **提交任务并等待结果**
7. **交付最终成果**

## 使用方法
```bash
uv run ~/.clawdbot/skills/morpheus-fashion-design/scripts/generate.py \
  --product "path/to/product.jpg" \
  --model "path/to/model-face.jpg" \
  --brief "Campaign brief text..." \
  --target "Target audience description..." \
  --aspect-ratio "4:5" \
  --style-pack "street_authentic" \
  --output "output-filename.png"
```

## 示例：Franuí Carnaval 活动创意要求
```
La campaña Franuí Carnaval captura el espíritu festivo y la alegría del carnaval brasileño 
en Copacabana. Una mujer afrobrasileña baila en medio de la multitud, sosteniendo el 
producto Franuí Milk hacia la cámara en un gesto espontáneo y celebratorio. La escena 
está llena de confeti, movimiento y energía. La fotografía adopta un estilo documental 
con motion blur intencional, ángulo bajo que empodera al sujeto, y el producto como 
elemento hero en primer plano. La luz es natural de día tropical, cálida y vibrante.
```

## 示例：Franuí Carnaval 活动的目标受众
```
Jóvenes adultos 18-35, principalmente mujeres pero inclusivo, que celebran la vida, 
la música y los momentos compartidos. Consumidores de experiencias premium que buscan 
productos que se integren naturalmente a sus momentos de disfrute. Activos en redes 
sociales, valoran la autenticidad y la conexión cultural. Mercado: Brasil y LATAM.
```

## 重要说明

### 工作流中的默认设置
如果未提供地点信息，系统会自动使用白色背景（`studio_override`）。

**如需使用特定环境背景：**
1. 提供一个 `location_ref` 图片
2. 将 `environment_pack` 设置为特定的环境（例如 `beach_minimal`、`street_crosswalk`）

### 优先级顺序
系统的优先级如下：
1. 模特的形象（保持一致性）＞
2. 产品的细节（忠实度）＞
3. 模特的穿着和姿势＞
4. 风格＞
5. 地点＞
6. 品牌标识

## API 密钥

**请勿通过参数传递 API 密钥。** 该密钥已在 ComfyDeploy 中预先配置好。如果传递 `--api-key` 参数，会导致认证错误。

## 故障排除

### 生成的图片为黑色或空白
如果生成的图片完全为黑色或空白，可能是由于 Google/Gemini 的内容审核机制导致的。常见原因包括：
- 请求的模特是名人或公众人物
- 图片内容被系统视为敏感
- 提供的提示语和图片组合不符合平台的内容政策

**解决方法：** 修改提示语，避免提及真实人物或名人；或者调整图片元素，以避免触发审核机制。
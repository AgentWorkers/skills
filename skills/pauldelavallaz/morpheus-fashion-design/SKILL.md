---
name: morpheus-fashion-design
version: 1.2.0
description: >
  **使用AI模型生成专业广告图片：模特手持或佩戴产品的图片**
  **适用场景：**  
  - 需要在图片中出现人物和产品的场景  
  - 制作时尚广告、产品推广活动或商业摄影  
  - 希望多张图片中的模特面部表情保持一致  
  - 需要专业的灯光效果和相机模拟  
  **输入要求：**  
  - 产品图片  
  - 模特参考资料（或模特目录）  
  **不适用场景：**  
  - 仅需要对现有图片进行编辑/修改 → 使用 `nano-banana-pro`  
  - 仅包含产品的图片（无人物） → 使用 `nano-banana-pro`  
  - 已经有了主图，需要多个变体图片 → 使用 `multishot-ugc`  
  - 需要视频而非图片 → 在生成图片后使用 `veed-ugc`  
  - 需要根据品牌资料从URL获取产品图片 → 使用 `ad-ready`  
  **输出结果：**  
  单张高质量PNG图片（2K-4K分辨率）
---
# Morpheus Fashion Design

使用 ComfyDeploy 的 Morpheus Fashion Design 工作流程生成专业的时尚/产品广告图片。

## ⚠️ 重要规则

### 1. **禁止使用 `logo` 字段**
`logo` 输入字段已从 API 中移除。**请勿传递该字段**。
仅存在两个图片输入参数：
- `product`：要宣传的产品
- `model`：模特的正面照片

### 2. **切勿为配置包使用自动值**
**配置包的设置绝对不能设置为 `auto` 或 `AUTO`。**
`auto` 表示使用默认值，这将生成缺乏创意方向、效果平淡的图片。
请根据具体要求仔细选择配置包的参数。允许并鼓励使用自定义的字符串值。

## 配置包选择指南

| 配置包 | 选择方法 |
|------|---------------|
| `style_pack` | 品牌风格：豪华 → `premium_restraint`；运动 → `cinematic_realism`；街头 → `street_authentic` |
| `camera_pack` | 运动场景 → `sony_a1`；时尚编辑 → `hasselblad_x2d`；街头场景 → `leica_m6` |
| `lens_pack` | 是否需要肖像压缩效果？是否需要宽视角？请根据拍摄类型和氛围选择合适的镜头 |
| `lighting_pack` | 是否需要黄金时刻的光线？是在摄影棚拍摄？还是利用自然光线？请根据要求选择 |
| `pose_discipline_pack` | 运动场景 → `sport_in_motion`；商业广告 → `commercial_front_facing`；用户生成内容 (UGC) → `street_style_candid_walk` |
| `film_texture_pack` | 温暖风格的时尚编辑 → `kodak_portra_400`；电影风格的拍摄 → `kodak_vision3_500t`；纯净风格的图片 → `digital_clean_no_emulation` |
| `environment_pack` | `beach_minimal`；`urban_glass_steel`；`street_crosswalk`；或自定义描述性字符串 |
| `color_science_pack` | `warm_golden_editorial`；`neutral_premium_clean`；`cinematic_low_contrast` |
| `time_weather_pack` | 黄金时刻的晴朗天气；明亮的正午阳光；阴沉的冬日光线 |

## API 详情

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署 ID：** `1e16994d-da67-4f30-9ade-250f964b2abc`

## 标准 API 调用方式

```javascript
const response = await fetch("https://api.comfydeploy.com/api/run/deployment/queue", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_KEY"
  },
  body: JSON.stringify({
    "deployment_id": "1e16994d-da67-4f30-9ade-250f964b2abc",
    "inputs": {
      "product": "/* product image URL */",
      "model":   "/* model face URL */",
      "brief":   "Detailed scene, pose, lighting, mood, product placement...",
      "target":  "Target audience: demographics, psychographics, lifestyle...",
      "input_seed": -1,
      "branding_pack": "logo_none",
      "aspect_ratio": "9:16",
      "style_pack": "street_authentic",
      "camera_pack": "sony_a1",
      "lens_pack": "zeiss_otus_55",
      "film_texture_pack": "kodak_portra_400",
      "color_science_pack": "warm_golden_editorial",
      "shot_pack": "medium_shot",
      "pose_discipline_pack": "street_style_candid_walk",
      "lighting_pack": "natural_window",
      "time_weather_pack": "golden_hour_clear",
      "environment_pack": "urban_glass_steel",
      "intent": "awareness"
    }
  })
});
```

## 🎭 模特目录

**GitHub：** `https://github.com/PauldeLavallaz/model_management`
**本地路径：** `~/clawd/models-catalog/catalog/images/`

### 优先级顺序
1. 用户提供模特照片 → 直接使用该照片
2. 用户描述模特特征 → 在目录中搜索并选择最合适的模特
3. 如果没有具体要求 → 根据任务描述来选择模特

### 模特搜索方式
```bash
# By body type
cat models-catalog/catalog/catalog.json | python3 -c "
import json,sys; data=json.load(sys.stdin)
for t in data['talents']:
    if t.get('body_type') in ['curvy','plus_size']:
        print(t['id'], t['name'], t['ethnicity'])
"
# By ethnicity + gender
cat models-catalog/catalog/catalog.json | jq '[.talents[] | select(.ethnicity == "hispanic" and .gender == "female") | {id, name, body_type}]'
```

## 创意任务描述说明

请像真正的摄影导演一样撰写任务描述，要求具体、具体且具有电影质感：

### 示例：CasanCrem Light（具有讽刺意味/病毒式传播的用户生成内容（UGC）角度）
```
Campaña UGC TikTok para CasanCrem Light La Serenísima.
Joven de contextura robusta sostiene el pote con sonrisa cómplice en cocina hogareña argentina.
Pose relajada, apoyada en la mesada, mirando directo a cámara con energía y complicidad.
El pote visible y protagonista en la mano. Luz de ventana natural, cálida de tarde.
Estilo UGC auténtico, no publicitario clásico. Cuerpo real, relatable, no atlético.
```

### 示例：Oakley Snowboarding（滑雪产品广告）
```
Oakley snowboarding campaign. Rider on metal rail in snowpark, body slightly rotated,
arms open for balance, eyes on the line. Technical authentic freestyle pose.
Alpine snowpark, full midday daylight, compacted snow, metal structures.
Natural sun bouncing off snow — saturated colors, strong contrast.
Documentary approach — freeze rider on rail, sharp body and board.
Real session frame: balance, concentration, style merged.
```

## 配置包参考

| 配置包 | 可选选项 |
|------|---------|
| `style_pack` | `premium_restraint`；`editorial_precision`；`cinematic_realism`；`cinematic_memory`；`campaign_hero`；`product_truth`；`clean_commercial`；`street_authentic`；`archive_fashion`；`experimental_authorial` |
| `shot_pack` | `full_body_wide`；`medium_shot`；`close_up`；`low_angle_hero`；`three_quarter`；`waist_up` |
| `camera_pack` | `arri_alexa35`；`canon_r5`；`hasselblad_x2d`；`leica_m6`；`sony_a1` |
| `lens_pack` | `cooke_anamorphic_i_50`；`leica_noctilux_50`；`zeiss_otus_55`；`wide_distortion_controlled` |
| `lighting_pack` | `golden_hour_backlit`；`natural_window`；`studio_three_point`；`bright_midday_sun` |
| `pose_discipline_pack` | `commercial_front_facing`；`street_style_candid_walk`；`sport_in_motion` |
| `film_texture_pack` | `kodak_portra_400`；`fujifilm_velvia_50`；`kodak_vision3_500t`；`digital_clean_no_emulation` |
| `color_science_pack` | `neutral_premium_clean`；`warm_golden_editorial`；`cinematic_low_contrast` |
| `environment_pack` | `beach_minimal`；`urban_glass_steel`；`street_crosswalk`；或自定义描述性字符串 |
| `time_weather_pack` | `golden_hour_clear`；`bright_midday_sun`；`overcast_winter_daylight` |
| `branding_pack` | `logo_none`（除非明确要求使用 logo） |
| `intent` | `awareness`（提升品牌知名度）；`consideration`（引发消费者兴趣）；`conversion`（促进购买）；`retention`（增强客户忠诚度） |
| `aspect_ratio` | `9:16`；`16:9`；`1:1`；`4:5`；`3:4` |

## Python 上传辅助工具

```python
def comfy_upload(filepath: str, api_key: str) -> str:
    from pathlib import Path
    import requests
    p = Path(filepath)
    mime = "image/png" if p.suffix == ".png" else "image/jpeg"
    with open(p, "rb") as f:
        r = requests.post(
            "https://api.comfydeploy.com/api/file/upload",
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": (p.name, f, mime)},
            timeout=60
        )
    r.raise_for_status()
    return r.json()["file_url"]
```

## 优先级层级

```
Talent (identity) > Product fidelity > Fit > Pose > Style > Location > Branding
```

## 故障排除

如果生成的图片为黑色或空白，可能是 Google/Gemini 的审核过滤器生效所致。
- 请避免使用名人或公众人物作为模特。
- 通过修改任务描述来消除可能导致问题的元素。

**API 密钥：** 无需作为参数传递。该密钥已在 ComfyDeploy 中预先配置好。

## 与 Portrait Generator 的集成

### 模特选择流程（更新版本）

`model` 字段可以从两个来源获取：

**选项 A — 模特目录（默认方式）：**
```
~/clawd/models-catalog/catalog/images/model_XX.jpg
```
当任务描述不需要非常具体的模特特征时，使用此方式。

**选项 B — Portrait Generator（当任务有特殊要求时）：**
```
portrait-generator → imagen_1 (vista frontal) → model en Morpheus
```
在需要以下情况时使用此方式：特定种族、精确年龄、独特外貌特征，或者目录中不存在的模特。
**注意：** Portrait Generator 生成的 `image_1` 图片必须为模特的正面照片。

### 何时使用 Portrait Generator
- 模特年龄超过 60 岁
- 目录中不存在特定种族的模特
- 模特有独特的外貌特征（如疤痕、白癜风、面部不对称）
- 任务描述中包含详细的模特特征

### 何时使用模特目录
- 模特为普通类型或没有特殊要求
- 需要标准年龄段的年轻模特
- 当速度比精确度更重要的情况下
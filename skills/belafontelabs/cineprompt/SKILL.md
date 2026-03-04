---
name: cineprompt
description: 无需浏览器即可构建 CinePrompt 视频提示并分享链接。该工具能够将自然语言中的镜头描述转换为结构化的 CinePrompt 数据格式，生成相应的提示文本，并创建可分享的链接（格式为 cineprompt.io/p/...）。适用于需要创建视频提示、生成 CinePrompt 链接、为 AI 视频生成提供镜头描述，或批量为一系列镜头生成提示的场景。
metadata: {"clawdbot":{"emoji":"🎬"}}
---
# CinePrompt 技能

您可以构建 CinePrompt 提示并直接分享链接——无需使用浏览器。

## 工作原理

1. 用户用自然语言描述一个镜头。
2. 系统会将描述转换为 CinePrompt 的 JSON 对象。
3. `create-share-link.js` 脚本会将该对象插入到 Supabase 数据库中，并返回一个 `/p/` 格式的分享链接。
4. 用户可以获得该链接以及提示文本，以便将其复制到任何 AI 视频工具中。

## 认证

需要 CinePrompt API 密钥（仅限专业订阅用户）。设置方式如下：
- 使用 `--api-key cp_xxx` 标志
- 设置环境变量 `CINEPROMPT_API_KEY=cp_xxx`

内部/所有者使用：设置环境变量 `CINEPROMPT_SERVICE_KEY` 以直接插入数据（绕过专业用户验证）。

## 创建分享链接

```bash
echo '<STATE_JSON>' | node <skill>/scripts/create-share-link.js --api-key cp_xxx
```

输出格式为 JSON：`{"url":"https://cineprompt.io/p/abc123","shortCode":"abc123","promptText":"...","mode":"single"}`

如果您已经手动准备了提示文本，也可以直接传递该文本：

```bash
echo '{"state":<STATE_JSON>,"prompt":"Your custom prompt text"}' | node <skill>/scripts/create-share-link.js --api-key cp_xxx
```

## JSON 对象结构

```json
{
  "mode": "single",
  "complexity": "complex",
  "subjectType": "character|object|vehicle|creature|landscape|abstract",
  "fields": { ... },
  "shots": [],
  "characters": []
}
```

### 必需的顶层字段

- `mode`：目前始终为 `"single"`（未来将支持多镜头/多场景模式）
- `complexity`：`"simple"` 或 `"complex"` — `complex` 模式会包含更多详细信息，如相机类型、镜头、胶片类型、色彩设置等
- `subjectType`：指定要显示的主题类型
- `fields`：一个对象，用于将字段名映射到对应的值（字符串或数组）

### 字段参考

所有有效的字段名和值都可以在 `<skill>/field-values.json` 中找到。关键字段包括：

**风格相关字段：**
- `media_type`（数组）：`["cinematic"]`, `["documentary"]` 等
- `documentary_style`：仅在 `media_type` 为 `documentary` 时使用
- `genre`：仅在 `media_type` 为 `cinematic` 时使用（数组形式）
- `commercial_type`：仅在 `media_type` 为 `commercial` 时使用
- `tone`（数组）：`["peaceful"]`, `["dramatic", "moody"]` 等
- `format`（仅限 `complex` 模式）：`"35mm Film"`, `"16mm Film"`, `"DSLR / Mirrorless"` 等

**主题相关字段（取决于 `subjectType`）：**
- `landscape`：`land_season`, `land_scale`
- `character`：`char_label`, `age_range`, `build`, `hair_style`, `hair_color`, `subject_description`, `wardrobe`, `expression`, `body_language`, `framing`
- `creature`：`creature_category`, `creature_label`, `creature_size`, `creature_body`, `creature_skin`, `creature_description`
- `object`：`obj_description`, `obj_material`, `obj_condition`, `obj_scale`
- `vehicle`：`veh_type`, `veh_description`, `veh_era`, `veh_condition`
- `abstract`：`abs_description`, `abs_quality`, `absmovement`

**动作相关字段：**
- `movement_type`（数组）：`["walking"]`, `["running", "turning"]`
- `pacing`：`"in real-time"`, `"in slow motion"`, `"time-lapse"` 等
- `action_primary`：描述主要动作的文本

**环境相关字段：**
- `setting`：`"exterior"`, `"interior"`, `"interior to exterior"`, `"exterior to interior"`
- `location_type`：`"open field, meadow"`, `"urban street"`, `"forest"` 等
- `custom_location`：自定义位置描述
- `location`：额外的位置细节
- `env_time`：`"golden hour, warm late afternoon light"`, `"night"`, `"dawn"` 等
- `weather`：`"clear sky"`, `"overcast"`, `"rain"`, `"fog"` 等
- `props`：自定义道具描述
- `env_fg`, `env_mg`, `env_bg`：前景/中景/背景的描述

**摄影相关字段：**
- `shot_type`：`"establishing shot"`, `"close-up"`, `"wide shot"`, `"medium"` 等
- `movement`：`"pull out"`, `"push in"`, `"dolly"`, `"tracking"`, `"static"`, `"orbit"` 等
- `camera_body`（仅限 `complex` 模式）：`"ARRI Alexa 65"`, `"RED V-Raptor"`, `"Sony Venice 2"` 等
- `focal_length`：`"24mm lens"`, `"35mm lens"`, `"50mm lens"`, `"85mm lens"` 等
- `lens_brand`（仅限 `complex` 模式）：`"Cooke S4/i"`, `"ARRI Master Prime"` 等
- `lens_filter`（仅限 `complex` 模式）：`"Black Pro-Mist"`, `"Glimmerglass"` 等
- `dof`：`"deep focus"`, `"shallow depth of field, bokeh"`, `"tilt shift miniature"` 等
- `lighting_style`：`"soft light"`, `"hard light"`, `"high contrast"`, `"silhouette"`, `"backlight"` 等
- `lighting_type`：`"daylight"`, `"moonlight"`, `"candlelight"`, `"neon"` 等
- `key_light`, `fill_light`（仅限 `complex` 模式）：自定义灯光设置

**调色板相关字段：**
- `color_science`（仅限 `complex` 模式）：`"ARRI LogC3 flat log footage, ungraded"` 等
- `film_stock`（仅限 `complex` 模式）：`"Kodak Portra 400 film colors"`, `"Kodak Vision3 500T film colors"` 等
- `color_grade`：`"warm tones"`, `"cool tones"`, `"teal and orange"`, `"desaturated"`, `"black and white"` 等
- `palette_colors`：主要/次要颜色
- `skin_tones`：自定义肤色

**音效相关字段：**
- `sfx_environment`（数组）：`["birds singing, nature ambience"]`, `["city traffic"]`, `["wind"]`
- `sfx_interior`（数组）：`["room tone"]`, `["clock ticking"]`
- `sfx_mechanical`（数组）：`["engine"]`, `["machinery"]`
- `sfx_dramatic`（数组）：`["bass rumble"]`, `["heartbeat"]`
- `ambient`：自定义环境音效
- `music_genre`：`"orchestral score"`, `"electronic score"`, `"jazz score"` 等
- `music_mood`：`"tense, building"`, `"melancholic, sparse"` 等
- `music`：自定义音乐描述

## 翻译指南

当用户描述一个镜头时，需将他们的描述映射到 CinePrompt 的相应字段中：

| 用户描述 | CinePrompt 字段 |
|-----------|---------------------|
| "golden hour" | `env_time: "golden hour, warm late afternoon light"` |
| "pulling back" / "pulling out" | `movement: "pull out"` |
| "birds chirping" | `sfx_environment: ["birds singing, nature ambience"]` |
| "empty land" / "open field" | `subjectType: "landscape", `location_type: "open field, meadow"` |
| "cinematic documentary" | `media_type: ["cinematic", "documentary"]` |
- `establishing shot` | `shot_type: "establishing shot"` |
- `bokeh" / "blurry background" | `dof: "shallow depth of field, bokeh"` |
- `everything in focus` | `dof: "deep focus"` |
- `handheld feel` | `movement: "handheld"` |
- `slow motion` | `pacing: "in slow motion"` |
- `warm look` | `color_grade: "warm tones"` |
- `shot on film` | `format: "35mm Film"` （仅限 `complex` 模式）

## 选择合适的复杂度

- **简单模式**：适用于大多数镜头，涵盖风格、主题、动作、环境、基础摄影效果和调色板设置。
- **复杂模式**：当用户指定了相机类型、镜头品牌、胶片类型、色彩设置、镜头滤镜或自定义灯光效果时使用。

## 示例

用户描述：**“一位饱经风霜的渔夫站在码头上，黎明时分，雾气弥漫，使用手持相机拍摄的特写镜头，画面呈褪色效果。”**

```json
{
  "mode": "single",
  "complexity": "simple",
  "subjectType": "character",
  "fields": {
    "media_type": ["cinematic"],
    "tone": ["moody"],
    "char_label": "A weathered fisherman",
    "subject_description": "Deep wrinkles, sun-damaged skin, salt-crusted hands",
    "expression": "stoic, gazing out to sea",
    "pacing": "in real-time",
    "setting": "exterior",
    "location_type": "dock, pier",
    "env_time": "dawn, first light",
    "weather": "fog",
    "shot_type": "close-up",
    "movement": "handheld",
    "dof": "shallow depth of field, bokeh",
    "lighting_style": "soft light",
    "lighting_type": "daylight",
    "color_grade": "desaturated",
    "sfx_environment": ["waves crashing, water ambience"]
  },
  "shots": [],
  "characters": []
}
```

然后将描述传递给脚本，系统会生成相应的分享链接并发送给用户。

## 批量处理流程

对于多镜头序列，需要为每个镜头创建单独的分享链接。可以将这些链接以编号列表的形式呈现给用户，用户可以逐一打开链接、进行调整，并将提示文本复制到他们选择的视频工具中。

## 注意事项

- 脚本会自动生成符合 CinePrompt 前端逻辑的提示文本（包括字段顺序、合并规则和句子组合）。
- 如果您希望手动编写提示文本，可以使用 `--prompt` 标志进行覆盖。
- 分享链接会包含完整的对象信息，包括复杂度设置和主题类型。
- 有效字段值请参考 `<skill>/field-values.json`。
- 数组字段（如 `media_type`, `tone`, `sfx_*`, `movement_type`）可以接受多个值。
- 自由文本字段（如 `custom_location`, `subject_description`, `action_primary` 等）可以接受任意字符串。
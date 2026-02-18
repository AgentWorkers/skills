---
name: ai-music-video
description: >
  **生成AI音乐视频的端到端流程：**  
  该工具利用Suno（sunoapi.org）生成音乐，通过OpenAI/Seedream/Google/Seedance生成视觉效果，再使用ffmpeg将这些元素整合成完整的音乐视频。支持带有时间戳的歌词（自动生成SRT文件），同时具备Suno自带的音乐视频生成功能，以及幻灯片、视频或混合模式等多种展示方式。每次生成过程都会根据使用的资源进行基于令牌的费用统计。
metadata:
  openclaw:
    requires:
      bins: [curl, python3, ffmpeg]
      env:
        - SUNO_API_KEY
        - OPENAI_API_KEY
      optionalEnv:
        - BYTEPLUS_API_KEY
        - TOGETHER_API_KEY
---
# AI音乐视频生成器

该工具可以生成完整的音乐视频：结合AI音乐、AI生成的视觉效果以及ffmpeg技术进行视频剪辑。

## 快速入门

```
"90년대 보이밴드 풍 한국어 노래 만들어줘" → music only
"발라드 뮤비 만들어줘" → music + slideshow MV
"EDM 뮤비 풀영상으로" → music + video clips MV
"Suno 뮤비로 만들어줘" → Suno native music video
```

## 工作流程

### 1. 根据歌词和音乐风格规划场景
在生成视频之前，需要创建一个`prompts.json`文件，其中包含从歌曲歌词和风格中提取的场景描述。一首3分钟的歌曲通常需要8-12个场景。

```json
[
  {"prompt": "Neon-lit city street at night, rain reflections", "type": "image"},
  {"prompt": "Camera slowly panning across a rooftop at sunset", "type": "video"},
  "A lone figure walking through cherry blossoms"
]
```

### 2. 生成音乐
```bash
bash scripts/suno_music.sh \
  --prompt "가사 또는 설명" \
  --style "90s boy band pop, korean" \
  --title "너만을 원해" \
  --model V4_5ALL --custom \
  --outdir /tmp/mv_project
```

**可选参数：**
- `--model V4_5ALL`（默认值）、`V5`、`V4_5PLUS`、`V4`、`V4`  
- `--instrumental`：仅生成纯音乐（不含人声）  
- `--vocal-gender m|f`：指定人声性别  
- `--negative-tags "Heavy Metal, Drums"`：避免使用这些音乐风格  
- `--music-video`：生成Suno平台支持的MP4格式音乐视频  
- `--dry-run`：仅用于查看费用估算  

**保持一致性风格（Persona）：**
- `--persona-id ID`：使用现有的音乐风格模板（用于生成多首风格相同的歌曲）  
- `--create-persona`：从生成的歌曲中创建新的音乐风格模板，并保存到`persona.json`文件中  
- `--persona-name "名称"` / `--persona-desc "描述"` / `--persona-style "风格"`：自定义音乐风格的名称和描述  

**自动功能：**
- 🎤 **带时间戳的歌词**：非器乐曲目会自动提取歌词的时间戳，并保存到`{outdir}/lyrics.srt`文件中  
- 🎬 **Suno原生音乐视频**：使用`--music-video`选项时，Suno会自动生成MP4格式的视频  
- 🎭 **音乐风格模板**：使用`--create-persona`选项时，会提取并保存音乐风格的相关信息  

### 3. 生成视觉效果（自定义音乐视频流程）
```bash
bash scripts/gen_visuals.sh \
  --mode slideshow \
  --prompts-file /tmp/mv_project/prompts.json \
  --image-provider seedream \
  --outdir /tmp/mv_project
```

或者使用OpenAI服务（价格更低，但分辨率较低）：
```bash
bash scripts/gen_visuals.sh \
  --mode slideshow \
  --prompts-file /tmp/mv_project/prompts.json \
  --image-provider openai --image-model gpt-image-1-mini --image-quality medium \
  --outdir /tmp/mv_project
```  
建议先使用`--dry-run`选项查看费用估算。

### 4. 视频剪辑
```bash
bash scripts/assemble_mv.sh \
  --audio /tmp/mv_project/track_0_xxx.mp3 \
  --outdir /tmp/mv_project \
  --output /tmp/mv_project/final_mv.mp4 \
  --transition fade
```

**字幕功能：**
- 自动检测`{outdir}/lyrics.srt`文件，并在视频中叠加歌词  
- `--subtitle /path/to/custom.srt`：使用自定义的SRT字幕文件  
- `--no-subtitle`：完全禁用字幕显示  

## 各种生成模式

| 模式 | 视觉效果 | 适用场景 | 成本（10个场景） |
|------|--------|----------|---------------------|
| `slideshow` | AI生成的图片 | 快速且成本低廉 | ~$0.02（基础模式）/ ~$0.09（中等质量）/ ~$0.45（高级模式） |
| `video` | AI生成的视频片段 | 高质量效果 | ~$1.40（Seedance Lite）/ ~$8.00（Sora 2） |
| `hybrid` | 两者结合 | 平衡效果 | ~$0.50-$4.00 |
| `suno-native` | 使用Suno平台的原生视频效果 | 最简单的方式 | 仅使用Suno平台的资源 |

**图片费用基于使用令牌的数量计算**——实际费用可能低于预估值。建议使用`--dry-run`选项获取精确费用。  

## 提供商选项

- **图片来源**：`--image-provider seedream`（推荐）、`openai`或`google-together`  
- **OpenAI图片模型**：`--image-model gpt-image-1-mini`（默认，低成本）或`gpt-image-1`（高级）  
- **视频来源**：`--video-provider sora`（默认）、`sora-pro`、`seedance-lite`、`seedance-pro`、`veo-fast`、`veo-audio`  
- **图片质量**：`--image-quality low|medium|high`  

## 成本跟踪

所有脚本在执行前后都会显示费用信息。务必先使用`--dry-run`选项进行测试。  
费用数据会保存到`{outdir}/cost_estimate.json`和`{outdir}/visuals_meta.json`文件中。  

## 环境变量

```bash
export SUNO_API_KEY="your-sunoapi-key"      # Required — sunoapi.org
export OPENAI_API_KEY="your-openai-key"     # Required — images + Sora video
export BYTEPLUS_API_KEY="your-byteplus-key" # Optional — Seedream 4.5 (recommended for images)
export TOGETHER_API_KEY="your-together-key" # Optional — Seedance, Veo, Imagen
export SUNO_CALLBACK_URL=""                 # Optional — see Callback URL below
```

**⚠️ 必需设置的环境变量：**  
运行任何脚本之前，必须设置`SUNO_API_KEY`和`OPENAI_API_KEY`。  
如果使用Seedream图片服务，还需要设置`BYTEPLUS_API_KEY`（可在[console.byteplus.com](https://console.byteplus.com)注册，免费获取200张图片）。  
`TOGETHER_API_KEY`仅适用于Seedance/Veo/Imagen图片服务。  

### 回调URL

Suno API要求提供`callBackUrl`字段以接收生成结果。  
如果未设置`SUNO Callback_URL`，脚本会使用`https://localhost/noop`作为默认的回调端点（这个端点实际上无法访问，因此不会发送任何数据）。  
**自定义方法：**可以将`SUNO_CALLBACK_URL`设置为你的自定义回调端点，或者使用任意可控制的URL。回调数据包含任务元信息和音频链接，不会发送API密钥。  
**禁用回调：**将`SUNO Callback_URL`设置为`https://localhost/noop`或任何无法访问的URL，此时脚本仍能正常运行（虽然回调功能会被禁用）。  

## 保持频道风格一致性（Persona Workflow）  

当需要像YouTube频道一样创建多首风格统一的歌曲时：  
```bash
# 1. 첫 곡 생성 + 페르소나 만들기
bash scripts/suno_music.sh \
  --prompt "코드 리뷰하며 듣는 노래" \
  --style "indie rock, energetic, coding vibe" \
  --title "Pull Request" \
  --custom --create-persona \
  --persona-name "개발자 노동요 싱어" \
  --persona-desc "개발자가 코딩하며 듣기 좋은 에너지 넘치는 보컬. 인디록, 일렉, 팝 장르를 넘나든다." \
  --persona-style "indie rock, electronic, developer work music" \
  --outdir /tmp/dev-bgm-01

# 2. persona.json에서 personaId 확인
cat /tmp/dev-bgm-01/persona.json

# 3. 같은 페르소나로 다음 곡 생성 — 보컬/스타일 일관성 유지
bash scripts/suno_music.sh \
  --prompt "야근하면서 듣는 노래" \
  --style "electronic pop, night coding" \
  --title "Midnight Deploy" \
  --custom --persona-id <PERSONA_ID> \
  --outdir /tmp/dev-bgm-02
```  
该工具会记住之前使用的音乐风格和人声特征，从而确保所有视频保持一致的风格。  

## 先决条件**

- 需要安装`curl`、`python3`和`ffmpeg`工具（用于视频剪辑）。  

## 参考资料：  
- **SunoAPI详细信息**：请参阅`references/sunoapi.md`  
- **视觉效果提供商信息**：请参阅`references/visual-providers.md`
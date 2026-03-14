---
name: picasso-tiktok
description: >
  完整的 TikTok/Reels 视频制作流程：  
  脚本 → TTS 语音合成（ElevenLabs）→ HeyGen 语音动画 → 自动字幕生成（Whisper）→ 使用 ffmpeg 合成视频 → 最终输出视频格式为 1080x1920。当没有源视频时，还可以使用 Runway Gen-4.5 生成 AI 背景视频。  
  **适用场景：**  
  - 从零开始制作带有语音解说的 TikTok 或 Instagram Reels  
  - 将新闻文章、主题内容或脚本转换为 9:16 格式的视频  
  - 为任何视频添加语音动画  
  - 生成 AI 背景视频（使用 Runway Gen-4.5）并将其编辑到 Reel 中  
  **不适用场景：**  
  - 仅需要图片（请使用 nano-banana-pro）  
  - 仅需要 TTS 音频（请直接使用 ElevenLabs）  
  **所需环境变量：**  
  ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, HEYGEN_API_KEY, YOUR_HEYGEN_AVATAR_ID, OPENAI_API_KEY, REPLICATE_API_TOKEN  
  **所需系统工具：**  
  ffmpeg, yt-dlp, Python 3
version: 1.2.0
---
# Picasso TikTok 🎨  
该工具可生成适用于TikTok/Reels的9:16格式视频，通过结合原始视频、HeyGen生成的头像以及同步的字幕来实现这一效果。  

## ⚠️ 必须遵循的步骤（含验证流程）  
**切勿一次性运行整个流程。务必按照以下步骤操作：**  
1. **下载并分析视频** → **查看视频时长及相关信息**  
2. **编写剧本** → **提交给Paul审核并等待批准**  
3. **生成音频** → **发送给Paul试听并等待反馈**  
4. **确认视频配置（布局、背景音乐等）** → **等待批准**  
5. **生成HeyGen头像**  
6. **根据原始剧本转录并修改字幕**  
7. **合成最终视频**  

---

## 第1步：下载视频  
### 从Google Drive下载  
```bash
pip install gdown -q
gdown "https://drive.google.com/uc?id=FILE_ID&confirm=t" -O output.mp4
```  
如果下载失败（可能是因为权限问题），请让Paul分享视频链接，或通过Telegram发送视频文件。  

### 从TikTok/YouTube下载  
```bash
yt-dlp -o "output.mp4" "URL"
```  

### 通过Telegram接收文件  
下载后的文件会被保存在`~/.openclaw/media/inbound/`目录中。  
**请确认文件是否已成功下载。**  
```bash
ffprobe video.mp4 2>&1 | grep -E "Duration|Video:|Audio:"
```  

---

## 第2步：编写剧本  
**剧本编写规则：**  
- 使用阿根廷里奥普拉塔地区的西班牙语（使用“voseo”语态，例如：grabás、actualizás、imagina）  
- 开场3秒内需设置明确的主题或钩子  
- 语言表达要生动自然，避免冗余内容  
- 不需要地址信息，只需包含实际需要传达的文字  
- 文末需包含呼吁用户行动的提示（例如：“加入Morfeo Labs”）  
- 视频时长应与原始视频相同或略长  

**在生成音频之前，请先展示剧本并等待Paul的审核。**  

---

## 第3步：音频处理（使用TTS技术）  
**默认选择：ElevenLabs Paul Pro**  
**务必生成3种不同的语音版本，并发送给Paul进行选择。**  
```python
import requests, time

CACHE = "/home/ubuntu/clawd/projects/picasso-tiktok/cache/JOB_NAME"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/$ELEVENLABS_VOICE_ID"
HEADERS = {"xi-api-key": "$ELEVENLABS_API_KEY", "Content-Type": "application/json"}

# Variación A — expresivo, pausas fuertes
# Variación B — DEFAULT ganador: guiones largos para pausas dramáticas (stability 0.45)
# Variación C — fluido y periodístico, sin cortes (stability 0.62)

configs = [
    ("A", script_a, {"stability": 0.35, "similarity_boost": 0.80, "style": 0.25}),
    ("B", script_b, {"stability": 0.45, "similarity_boost": 0.82, "style": 0.15}),  # ← ganador recurrente
    ("C", script_c, {"stability": 0.62, "similarity_boost": 0.78, "style": 0.05}),
]

for ver, text, settings in configs:
    r = requests.post(BASE_URL, headers=HEADERS,
        json={"text": text, "model_id": "eleven_multilingual_v2", "voice_settings": settings})
    with open(f"{CACHE}/audio_{ver}.mp3", "wb") as f:
        f.write(r.content)
    print(f"✅ V{ver} {len(r.content)//1024}KB")
    time.sleep(1)
```  

**控制节奏的标点技巧：**  
- 将长句拆分成独立的段落以增加停顿感（VA）  
- 使用破折号（`—`）分隔长句中的重要部分，营造戏剧性效果（VB，效果更佳）  
- 如果所有内容连续播放则缺乏节奏感（VC，效果较差）  

**重要提示：**  
- 使用的模型为`eleven_multilingual_v2`，**切勿使用`eleven_v3`（否则会导致口音变化）  
- Paul Pro的语音ID：`$ELEVENLABS_VOICE_ID`  
- API密钥：`$ELEVENLABS_API_KEY`  

**备份方案：使用Cartesia sonic-3**  
**生成音频后，请发送给Paul试听并等待反馈。**  

---

## 第4步：确认视频配置  
在生成头像和合成视频之前，请确认以下参数：  
- **布局比例**：60/40（原始视频占上屏比例）、50/50、40/60（头像占上屏比例）  
- **是否需要字幕**  
- **背景音乐**：是否需要混入原始音乐？如果需要，音量应控制在多少？（通常建议为30%）  
- **视频开头标题**（例如：“这个女孩并不存在 👁️”）  
- **TikTok视频的描述性文字（包含标签）**  

---

## 第5步：使用HeyGen生成头像  
**需将音频文件上传至uguu.se（HeyGen平台要求）**  
```python
import requests

with open("audio.mp3", "rb") as f:
    r = requests.post("https://uguu.se/upload",
        files={"files[]": ("audio.mp3", f.read(), "audio/mpeg")}, timeout=30)
audio_url = r.json()["files"][0]["url"]
```  
**之后生成视频文件。**  
```python
HEYGEN_KEY = "$HEYGEN_API_KEY"
AVATAR_ID  = "aa7ca06de7454b9caa147b97a534e813"  # Paul default

r = requests.post("https://api.heygen.com/v2/video/generate",
    headers={"X-Api-Key": HEYGEN_KEY, "Content-Type": "application/json"},
    json={
        "video_inputs": [{
            "character": {"type": "avatar", "avatar_id": AVATAR_ID, "avatar_style": "normal"},
            "voice": {"type": "audio", "audio_url": audio_url},
            "background": {"type": "color", "value": "#000000"}
        }],
        "dimension": {"width": 432, "height": 768},  # 9:16 pequeño, escala mejor
        "aspect_ratio": "9:16"
    })
video_id = r.json()["data"]["video_id"]
```  
**完成生成后，请进行约2-4分钟的投票以优化效果。**  
```python
import time
while True:
    r = requests.get(f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
        headers={"X-Api-Key": HEYGEN_KEY})
    data = r.json().get("data") or {}
    if data.get("status") == "completed":
        avatar_url = data["video_url"]
        break
    time.sleep(15)
```  
**最后下载并调整视频尺寸。**  
```bash
curl -sL "$AVATAR_URL" -o avatar.mp4

# Auto-detect crop (quita padding negro de HeyGen)
ffmpeg -ss 2 -i avatar.mp4 -vframes 10 -vf cropdetect=24:2:0 -f null - 2>&1 | grep crop= | tail -2
# Típico resultado: crop=432:244:0:262
```  

## 第6步：校对字幕  
**务必将字幕内容与原始剧本进行比对**  
**使用Whisper工具进行转录，**  
**注意：**  
Whisper在处理西班牙语/里奥普拉塔地区的语言时经常会出现错误，尤其是某些专业术语的翻译：  
| Whisper的翻译 | 正确翻译 |  
|-----------------|----------|  
| Cling | KLING |  
| Confi / Confy | COMFY |  
| Imagina | IMAGINÁ |  
| Grabas | GRABÁS |  
| Actualizas | ACTUALIZÁS |  
| Buscas | BUSCÁS |  
| Preparas | PREPARÁS |  
| I A | IA |  
| 任何品牌名称** | 需要逐一核对**  

**在生成最终的`.ass`文件之前，请先进行修正。**  
```python
fixes = [("CLING", "KLING"), ("CONFI", "COMFY"), ("IMAGINA", "IMAGINÁ"), ...]
for wrong, right in fixes:
    ass = ass.replace(wrong, right)
```  
**之后生成最终的`.ass`文件。**  
```python
import sys
sys.path.insert(0, "/home/ubuntu/clawd/projects/picasso-tiktok/picasso-api/workers")
from subtitles import generate_ass

ass = generate_ass(words)
# Aplicar correcciones de marca/voseo
# Aplicar MarginV según layout (ver tabla abajo)
with open("subs.ass", "w") as f:
    f.write(ass)
```  

## 根据布局调整字幕间距  
| 布局比例 | 上屏像素 | 下屏像素 | 推荐的边距 |  
|--------|--------|--------|---------------------|  
| 60/40  | 1152   | 768    | 720                 |  
| 50/50  | 960    | 960    | 880                 |  
| 40/60  | 768    | 1152   | ~1000               |  
**请将调整后的字幕文件保存为`.ass`格式。**  
```python
import re
ass = re.sub(
    r'(Style: Word,\S+,\d+,\S+,\S+,\S+,\S+,-?\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,[\d.]+,[\d.]+,\d+,\d+,\d+,)\d+,',
    lambda m: m.group(1) + str(MARGIN_V) + ',', ass)
```  

---

## 第7步：合成最终视频  
**调整视频的显示比例**  
| 布局比例 | 上屏高度 | 下屏高度 |  
|--------|-------|-------|  
| 60/40  | 1152  | 768   |  
| 50/50  | 960   | 960   |  
| 40/60  | 768   | 1152  |  

**基础视频处理（不含背景音乐）**  
```bash
ffmpeg -y \
  -i source.mp4 -i avatar.mp4 -i audio.mp3 \
  -filter_complex "
    [0:v]scale=1080:{top_h}:force_original_aspect_ratio=increase,crop=1080:{top_h},setsar=1[top];
    [top]pad=1080:1920:0:0:black[bg];
    [1:v]crop={crop_str},scale=1080:{bot_h}:force_original_aspect_ratio=increase,crop=1080:{bot_h},setsar=1[av];
    [bg][av]overlay=0:{top_h}[ov];
    [ov]ass=subs.ass[final]
  " \
  -map "[final]" -map "2:a" \
  -c:v libx264 -profile:v high -level 4.0 -crf 23 \
  -c:a aac -b:a 192k -movflags +faststart -shortest \
  output.mp4
```  
**包含背景音乐的处理方式（背景音乐占比X%）**  
```bash
  -filter_complex "
    [0:v]...[ov];
    [ov]ass=subs.ass[final];
    [0:a]volume=0.3[src_a];
    [2:a]volume=1.0[tts_a];
    [src_a][tts_a]amix=inputs=2:duration=shortest[mix_a]
  " \
  -map "[final]" -map "[mix_a]" \
```  
**注意：**  
**头像在处理过程中切勿被拉伸。**  
```bash
# ✅ CORRECTO: scale to fill + crop (sin deformación, sin negro)
[1:v]crop={crop_str},scale=1080:{bot_h}:force_original_aspect_ratio=increase,crop=1080:{bot_h},setsar=1[av]

# ❌ MAL: escala directa deforma
[1:v]crop={crop_str},scale=1080:{bot_h},setsar=1[av]

# ❌ MAL: pad con negro (Paul no quiere franjas negras)
[1:v]crop={crop_str},scale=1080:-2,pad=1080:{bot_h}:...,setsar=1[av]
```  

---

## 最终输出参数：  
- **分辨率**：1080x1920  
- **编码格式**：H.264 high profile level 4.0  
- **音频格式**：AAC 192k  
- **文件扩展名**：`.mov`，并添加`-movflags +faststart`选项  

## 其他布局选项：  
- **2/3画面显示（Chiqui Tapia风格）**  
```
top_h=1280, bot_h=640, MarginV=640
```  
****完整显示原始视频（无裁剪）**  
```bash
# Usar decrease + pad en vez de increase + crop
[0:v]scale=1080:{top_h}:force_original_aspect_ratio=decrease,pad=1080:{top_h}:(ow-iw)/2:(oh-ih)/2:black,setsar=1[top]
```  
**当背景音乐时长较长时，使用循环播放功能**  
```bash
AUDIO_DUR=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 audio.mp3)
ffmpeg -y -stream_loop 3 -i source.mp4 -t $AUDIO_DUR \
  -c:v libx264 -preset fast -crf 18 -c:a aac source_looped.mp4
```  
**如果原始视频无法使用，可使用Runway Gen-4.5生成背景视频**  
**相关参数：**  
- `prompt`：视频的描述性文字  
- `image`：可选的初始帧（用于生成视频）  
- `duration`：视频时长（默认5秒，最长10秒）  
- **aspect_ratio`：默认为16:9；若需要9:16比例，请使用768:1344  
**生成成本：**每个10秒的视频片段约0.05美元  

**剧本较长的视频处理流程：**  
1. 先生成TTS音频 → 获取总时长  
2. 将剧本按主题分割成多个片段  
3. 为每个片段分配时长（总时长需符合要求）  
4. 同时生成所有片段  
5. 使用`ffmpeg`工具将片段合并成最终视频  

---

## 提交前的检查清单：  
- 【】剧本已获得Paul的审核批准  
- 【】已发送3种不同的语音版本供Paul选择  
- 【】布局比例已确认  
- 【】字幕已根据原始剧本修正完毕  
- 【】头像无变形  
- **背景音乐已调整至合适音量（如适用）**  
- **视频分辨率（1080x1920）已通过`ffprobe`工具验证**
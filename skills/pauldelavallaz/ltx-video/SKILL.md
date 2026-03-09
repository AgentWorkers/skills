---
name: ltx-video
description: >
  通过 LTX-2.3 API（ltx.video）生成视频。支持文本转视频、图片转视频、音频转视频（根据音频和图片进行口型同步），以及视频的剪辑和重新录制功能。  
  适用场景：  
  - 从文本/图片/音频生成 AI 视频；  
  - 为肖像图片添加动画效果；  
  - 根据现有的图片和音频记录制作口型同步视频。
---
# LTX-2.3 视频 API

## API 参考

**基础 URL:** `https://api.ltx.video/v1`  
**认证:** `Authorization: Bearer <API_KEY>`  
**响应:** MP4 格式文件（可直接下载，无需轮询）

### 端点（Endpoints）

| 端点 | 输入参数 | 用途 |
|---------|------------|---------|
| `/v1/text-to-video` | 文本提示 | 从文本生成视频 |
| `/v1/image-to-video` | 图像路径 + 文本提示 | 用静态图像制作动画视频 |
| `/v1/audio-to-video` | 音频路径 + 图像路径 + 文本提示 | 根据音频和图像制作对口型视频 |
| `/v1/extend` | 视频路径 + 文本提示 | 在视频的开头或结尾添加内容 |
| `/v1/retake` | 视频路径 + 时间范围 | 重新生成视频的某一部分 |

### 模型（Models）

| 模型 | 生成速度 | 视频质量 |
|---------|------------|---------|
| `ltx-2-3-fast` | 约 17 秒 | 质量一般（适用于测试） |
| `ltx-2-3-pro` | 约 30–60 秒 | 质量最高（适用于最终输出） |

### 支持的分辨率

- `1920x1080`（宽屏 16:9）  
- `1080x1920`（竖屏 9:16 — 专为竖屏数据训练）  
- `1440x1080`, `4096x2160`（仅适用于文本转视频）

**仅适用于“音频转视频”功能的分辨率:** `1920x1080` 或 `1080x1920`

---

## 快速示例

### 文本转视频
```bash
curl -X POST "https://api.ltx.video/v1/text-to-video" \
  -H "Authorization: Bearer $LTX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A man in a navy blue suit sits at a luxury restaurant table...",
    "model": "ltx-2-3-pro",
    "duration": 8,
    "resolution": "1920x1080"
  }' -o output.mp4
```

### 音频转视频（对口型）
```bash
curl -X POST "https://api.ltx.video/v1/audio-to-video" \
  -H "Authorization: Bearer $LTX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_uri": "https://example.com/voice.mp3",
    "image_uri": "https://example.com/portrait.jpg",
    "prompt": "A man speaks directly to camera...",
    "model": "ltx-2-3-pro",
    "resolution": "1920x1080"
  }' -o output.mp4
```

### Python 封装示例
```python
import requests

def ltx_audio_to_video(audio_url, image_url, prompt, api_key,
                        model="ltx-2-3-pro", resolution="1920x1080",
                        output_path="output.mp4"):
    r = requests.post(
        "https://api.ltx.video/v1/audio-to-video",
        headers={"Authorization": f"Bearer {api_key}",
                 "Content-Type": "application/json"},
        json={"audio_uri": audio_url, "image_uri": image_url,
              "prompt": prompt, "model": model, "resolution": resolution},
        timeout=300, stream=True
    )
    if r.status_code != 200:
        raise RuntimeError(f"LTX error {r.status_code}: {r.text}")
    with open(output_path, "wb") as f:
        for chunk in r.iter_content(8192): f.write(chunk)
    return output_path
```

---

## ⚠️ 重要规则（根据经验总结）

### 文件托管（File Hosting）

- 网址必须使用 **HTTPS**，HTTP 请求会被拒绝。
- 文件必须返回正确的 MIME 类型（不能是 `application/octet-stream`）。
- 可以使用 `curl` 命令上传文件，例如：`curl -F "files[]=@file.mp3" https://uguu.se/upload`。
- 音频文件应上传为 **MP3** 格式（而非 WAV），否则 uguu 服务可能无法正确识别文件类型。
- **4K 图像可能无法正常处理**，请在上传前将其调整为 `1920x1080` 分辨率。

```bash
# Upload MP3 to uguu.se
AUDIO_URL=$(curl -s -F "files[]=@audio.mp3" "https://uguu.se/upload" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['files'][0]['url'])")

# Upload image
IMAGE_URL=$(curl -s -F "files[]=@portrait.jpg" "https://uguu.se/upload" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['files'][0]['url'])")
```

### 图像尺寸限制
```bash
# Resize large images before upload
ffmpeg -y -i input_4k.png -vf "scale=1920:1080" output_1080.jpg
```

### 人物面部表现注意事项

- 避免使用让角色 **低头** 的提示，这会影响面部表情的连贯性。
- 保持角色头部与画面齐平，并始终注视前方。
- 将物体置于画面内，避免让角色的手臂或身体超出画面范围。

### 关于视频的起始和结束帧

- LTX 本身不支持直接处理视频的起始和结束帧。
- 解决方法：先分别生成视频片段 A 和片段 B，然后使用 `/v1/extend` 功能将它们合并在一起。

---

## 提示编写指南（LTX-2.3）

LTX-2.3 的文本生成功能有了显著提升。**具体性至关重要**。

### 1. 使用动词，而非名词

❌ `"一个站立的男人的戏剧性画像"
✅ `"一个男人站在屋顶上。他的外套在风中飘动。他调整领口，然后随着镜头的移动向前走去。"

### 2. 像导演一样描述场景

- 明确指定 **物体的位置（左右）** 以及 **前景与背景**。
- 描述 **谁在移动**、**什么在移动**、**移动的方式** 以及 **镜头的动作**。
- LTX-2.3 现在能够正确处理这些空间关系。

### 3. 明确描述音频元素

- 指出声音的类型（对话、环境音、音乐等）。
- 说明声音的音调和强度。
- 例如：`他的声音清晰而温暖，背景中有餐厅的背景音。`

### 4. 避免使用静态的、类似照片的提示

- 如果提示描述的是静态图像，生成的视频也会呈现为静态图像。
- 应添加风声、动作效果、呼吸声、手势以及镜头的移动等动态元素。

### 5. 描述材质和纹理

- 头发、布料、表面质感、光照效果等细节。
- 例如：`在逆光下仍能清晰看到每一根头发**，这样的描述有助于生成更真实的图像。

### 6. 竖屏格式（9:16）的注意事项

- LTX-2.3 专为竖屏数据训练，建议使用 `1080x1920` 分辨率。
- 在创建视频时请确保画面是竖屏格式，不要误将其视为宽屏图像。

### 7. 复杂场景的处理

- 可以同时描述多个动作，例如：`他拿起香蕉，举到耳边，然后露出微笑`。
- LTX-2.3 能够同时处理多个动作和场景元素。

### 对口型提示模板
```
A [description of person] sits/stands [location]. He/she speaks directly 
to camera, lips moving in perfect sync with his/her voice. [Gesture details]. 
Head stays level and gaze remains locked on camera throughout. 
[Environment description softly blurred in background]. 
[Lighting]. [Camera: holds steady at eye level, front-on].
```

---

## ComfyUI 的自定义节点

ComfyUI 提供了一些用于简化 API 使用的自定义节点：

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/PauldeLavallaz/comfyui-ltx-node
```

相关节点：`LTX Text to Video`、`LTX Image to Video`、`LTX Extend Video`  
类别：**LTX Video**

---

## API 密钥

Paul 的 API 密钥存储在 `~/clawd/.env` 文件中，文件名为 `LTX_API_KEY`。
```
ltxv_RfSU5hdKJb_g5dwbECZWnilE1P8dJzbavz6niP_0LQJ942ARHIVhrBCfebcytEL1efLVx_63S_PJyWTzicrBcWEkOXfCbGTl8JSzlJJk329MwRViEgOoE2KnE9LIA5t6QSFeBy7DLnTIcX0AZNbV9Jv0TuC7qcq2gV33G6ROhUVUDCuN
```
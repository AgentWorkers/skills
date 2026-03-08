---
name: runpod-media
description: 通过 RunPod 的公共 AI 端点，可以从文本生成图像、根据文本指令编辑图像、将图像动画化为视频，以及从文本生成视频。当用户需要生成/创建图像或视频、编辑照片、对图像进行动画处理或制作 AI 媒体时，可以使用这些功能。使用这些服务需要具备 RunPod API 密钥。
---
# RunPod媒体技能

该技能使用RunPod的公共端点生成AI图像和视频，所有输出结果都会保存到`~/runpod-media/`目录下。

## API密钥

需要一个密钥，请将其添加到`~/.openclaw/secrets.json`文件中：

| 密钥路径 | 用途 | 获取方式 |
|---------|---------|-------------|
| `/runpod/apiKey` | 调用RunPod端点 | [runpod.io/console/user/settings](https://www.runpod.io/console/user/settings) |

本地生成的图像在发送到RunPod端点之前，会先通过预签名的URL上传到**Cloudflare R2**（有效期为1分钟）。R2的访问凭据已配置在`/cloudflare/r2`文件中。

> `imgbb`已不再使用，所有本地文件的上传现在都使用R2的预签名URL。

**R2清理规则：**`uploads/`目录中的文件会在**1天后**根据`openclaw`桶的生命周期规则自动删除。预签名URL在1分钟后失效，文件也会在24小时内被清理。

密钥的优先级顺序如下：
1. **OpenClaw的`secrets.json`文件** — `~/.openclaw/secrets.json`（已配置）
2. **环境变量** — `RUNPOD_API_KEY`

## 用户的使用方式（自然语言示例）

用户不会直接输入CLI命令，系统会将他们的自然语言请求转换为相应的脚本调用：

**生成图像：**
- “生成一张在霓虹东京背景下的武士猫图像” → `generate_image --prompt "..."`
- “制作一张16:9比例的日落时海洋风暴图像” → `generate_image --prompt "..." --aspect-ratio 16:9`
- “使用Nano Banana模型生成一张未来城市的图像” → `call_endpoint --endpoint google-nano-banana-2-edit --prompt "..."`

**编辑图像：**
- “编辑这张图像，添加落雪效果” → `edit_image --images <文件路径> --prompt "add snow falling"`
- “使用Qwen工具编辑这张照片，使其看起来像一幅画” → `call_endpoint --endpoint qwen-image-edit --image <文件路径> --prompt "make it look like a painting"`

**将图像转换为视频：**
- “将这张图像转换为视频，采用慢速镜头平移效果” → `image_to_video --image <文件路径> --prompt "slow camera pan"`
- “使用Kling模型将这张图像转换为视频” → `image_to_video --image <文件路径> --model kling --prompt "..."`
- “使用Sora 2模型将这张图像转换为10秒的视频” → `call_endpoint --endpoint sora-2-pro-i2v --image <文件路径> --prompt "..." --duration 10`

**将文本转换为视频：**
- “生成一张狼在月光下嚎叫的视频” → `text_to_video --prompt "..."`

**列出可用模型：**
- “你们有哪些图像/视频模型？”
- “列出所有可用的端点”
- “展示RunPod有哪些可用的模型”
  → 运行`list_endpoints`命令，并用简单的语言向用户展示结果

**添加新端点：**
- “添加这个RunPod端点：https://console.runpod.io/hub/playground/voice/kokoro-tts”
- “探测并添加这些端点：kokoro-tts, flux-kontext-pro”
  → 运行`discover_endpoints add --candidates "<端点地址>"`

---

## 功能与费用

| 功能 | 命令 | 费用 | 所需时间 |
|------|---------|------|------|
| 文本转图像 | `generate_image` | 约0.005美元/张 | 3–8秒 |
| 编辑图像 | `edit_image` | 约0.005美元/张 | 5–15秒 |
| 图像转视频 | `image_to_video` | 0.03–0.90美元/段 | 30–120秒 |
| 文本转视频 | `text_to_video` | 0.04–1.22美元/段 | 30–120秒 |
| **任意端点** | `call_endpoint` | 根据端点不同而异 |

内置命令使用默认的端点。如需使用其他模型（如Nano Banana Pro、FLUX、Sora 2、Kling、TTS等），请使用`call_endpoint`并指定相应的端点ID。

## 端点注册表

所有已知的公共端点都记录在`scripts/endpoints.json`文件中。可以运行`list_endpoints`命令来查看这些端点。

```bash
$SKILL_DIR/run.sh list_endpoints
```

### 调用任意端点

```bash
$SKILL_DIR/run.sh call_endpoint \
  --endpoint <ENDPOINT_ID> \
  [--prompt "TEXT"] \
  [--image PATH_OR_URL] \
  [--audio PATH_OR_URL] \
  [--duration 5] \
  [--aspect-ratio 16:9] \
  [--input '{"key": "value"}']   # full JSON override
```

**示例：**

```bash
# Nano Banana Pro image generation
$SKILL_DIR/run.sh call_endpoint --endpoint nano-banana-pro --prompt "a golden retriever in space"

# Nano Banana Pro image editing
$SKILL_DIR/run.sh call_endpoint --endpoint nano-banana-pro --prompt "make it nighttime" --image photo.jpg

# Sora 2 Pro video from image
$SKILL_DIR/run.sh call_endpoint --endpoint sora-2-pro-i2v --image photo.jpg --prompt "camera slowly pulls back" --duration 5

# Kokoro TTS
$SKILL_DIR/run.sh call_endpoint --endpoint kokoro-tts --text "Hello world"

# FLUX Schnell
$SKILL_DIR/run.sh call_endpoint --endpoint flux-schnell --prompt "cyberpunk city" --input '{"width":1024,"height":1024}'
```

### 添加新端点

当用户请求使用注册表中不存在的端点，或者`runpod`技能发现了新的端点时：
1. 可以直接使用`--endpoint <端点ID>`来调用该端点（无需先在注册表中添加）
2. （可选）将新端点添加到`scripts/endpoints.json`文件中，以便后续使用

**使用`runpod`技能时：**可以先使用`runpod`技能在RunPod平台上浏览/发现端点ID，然后将该ID传递给`call_endpoint`命令。

### 生成图像

```bash
$SKILL_DIR/run.sh generate_image \
  --prompt "PROMPT" \
  [--aspect-ratio 1:1|16:9|9:16|4:3|3:4] \
  [--seed 42]
```

### 编辑图像

```bash
$SKILL_DIR/run.sh edit_image \
  --images PATH_OR_URL [PATH_OR_URL ...] \
  --prompt "EDIT INSTRUCTION" \
  [--aspect-ratio 1:1] \
  [--seed 42]
```

- 支持上传1–5张图像（可以是本地路径或URL）
- 本地文件会通过`imgbb`自动上传（需要`secrets.json`文件中的`/imgbb/apiKey`）

### 将图像转换为视频

```bash
$SKILL_DIR/run.sh image_to_video \
  --image PATH_OR_URL \
  --prompt "MOTION DESCRIPTION" \
  [--model wan25|kling|seedance] \
  [--duration 5|10] \
  [--negative-prompt "TEXT"]
```

**可用模型：**
- `wan25`（默认模型） — WAN 2.5，约0.026美元/5秒
- `kling` — Kling v2.1 Pro，0.45美元/5秒（最高画质）
- `seedance` — Seedance 1.0 Pro，约0.12美元/5秒

### 从文本生成视频

```bash
$SKILL_DIR/run.sh text_to_video \
  --prompt "VIDEO DESCRIPTION" \
  [--model wan26|seedance] \
  [--duration 5|10|15] \
  [--size 1920x1080] \
  [--negative-prompt "TEXT"]
```

**可用模型：**
- `wan26`（默认模型） — WAN 2.6，约0.04美元/5秒
- `seedance` — Seedance 1.0 Pro，约0.12美元/5秒

## 默认设置

- **生成后删除本地文件**：成功生成图像或视频后，系统会自动删除本地文件。除非用户明确要求保留（如“keep it”或“save it”），否则文件会被删除。
- **字幕**：字幕应简洁自然。除非用户特别要求，否则不要显示渲染时间或费用信息。例如：`🦊 Fox under the aurora` 而不是 `🦊 Fox — 105s render (~$0.026)`。

## 向用户交付媒体文件

生成图像或视频后，**必须**通过用户指定的通道将其发送给用户。

### 注意事项
在沙箱模式下，使用`message`工具时可能会出现问题，因为`SecretRef`解析功能在媒体传输时可能不可用。这是OpenClaw的一个已知限制。

**解决方法：**直接使用`curl`命令和Telegram机器人API。从`secrets.json`文件中获取机器人Token，然后通过`curl`发送请求。这种方法在所有模式下都能正常工作。

**如何获取CHAT_ID：**从传入消息的元数据中获取`chat_id`（例如：`telegram:1231438498`），然后在请求中使用`1231438498`作为参数。

### 交付流程：
1. 确保生成了文件（注意保存路径）。
2. 使用`message`工具发送文件，并附上简洁自然的字幕（除非用户特别要求，否则不显示费用或生成时间）。
3. 成功发送后删除本地文件：`rm <文件路径>`。
4. 仅当用户选择“keep it”或“save it”时，才不删除文件。

### 为什么不用`message`工具？
先尝试使用`message`工具；如果成功，那就很好。如果遇到`SecretRef`相关错误，再切换到上述的`curl`方法。

## 其他说明：
- 图像生成可能需要30–120秒，请告知用户等待。
- 输出文件保存在`~/.openclaw/workspace/runpod-media/`目录下，该目录在沙箱模式和高级模式下均可访问。
- 相关辅助工具位于`scripts/_utils.py`文件中，请勿直接调用这些工具。
---
name: sogni-gen
version: "1.5.9"
description: 使用 Sogni AI 的去中心化网络生成图像和视频。你可以让代理根据提示或参考图像来“绘制”、“生成”图像，或者“制作视频/动画”。
homepage: https://sogni.ai
metadata:
  clawdbot:
    emoji: "🎨"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node"]
    install:
      - id: npm
        kind: exec
        command: "cd {{skillDir}} && npm i"
        label: "Install dependencies"
---
# Sogni 图像与视频生成

使用 Sogni AI 的去中心化 GPU 网络生成 **图片和视频**。

## 设置

1. **获取 Sogni 凭据**：[https://app.sogni.ai/](https://app.sogni.ai/)
2. **创建凭据文件：**
   ```bash
mkdir -p ~/.config/sogni
cat > ~/.config/sogni/credentials << 'EOF'
SOGNI_USERNAME=your_username
SOGNI_PASSWORD=your_password
EOF
chmod 600 ~/.config/sogni/credentials
```

3. **安装依赖项（如果已克隆项目）：**
   ```bash
cd /path/to/sogni-gen
npm i
```

4. **或通过 npm 安装（无需克隆项目）：**
   ```bash
mkdir -p ~/.clawdbot/skills
cd ~/.clawdbot/skills
npm i sogni-gen
ln -sfn node_modules/sogni-gen sogni-gen
```

## 文件系统路径和覆盖设置

此功能使用的默认文件路径：

- 凭据文件（读取）：`~/.config/sogni/credentials`
- 最后一次渲染的元数据（读取/写入）：`~/.config/sogni/last-render.json`
- OpenClaw 配置文件（读取）：`~/.openclaw/openclaw.json`
- `--list-media` 的媒体列表（读取）：`~/.clawdbot/media/inbound`
- MCP 本地结果副本（写入）：`~/Downloads/sogni`

路径覆盖环境变量：

- `SOGNI_CREDENTIALS_PATH`
- `SOGNI LAST_RENDER_PATH`
- `SOGNI_MEDIA_INBOUND_DIR`
- `OPENCLAW_CONFIG_PATH`
- `SOGNI_DOWNLOADS_DIR`（MCP）
- `SOGNI_MCP_SAVE_DOWNLOADS=0`（禁用 MCP 本地文件写入）

## 使用方法（图片与视频）

```bash
# Generate and get URL
node sogni-gen.mjs "a cat wearing a hat"

# Save to file
node sogni-gen.mjs -o /tmp/cat.png "a cat wearing a hat"

# JSON output (for scripting)
node sogni-gen.mjs --json "a cat wearing a hat"

# Check token balances (no prompt required)
node sogni-gen.mjs --balance

# Check token balances in JSON
node sogni-gen.mjs --json --balance

# Quiet mode (suppress progress)
node sogni-gen.mjs -q -o /tmp/cat.png "a cat wearing a hat"
```

## 选项

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `-o, --output <路径>` | 保存到文件 | 输出 URL |
| `-m, --model <id>` | 模型 ID | `z_image_turbo_bf16` |
| `-w, --width <像素>` | 宽度 | 512 |
| `-h, --height <像素>` | 高度 | 512 |
| `-n, --count <数量>` | 图片数量 | 1 |
| `-t, --timeout <秒>` | 超时时间（秒） | 30（视频为 300） |
| `-s, --seed <数字>` | 特定种子 | 随机 |
| `--last-seed` | 重用上次渲染的种子 | - |
| `--seed-strategy <字符串>` | 种子策略：随机 | `prompt-hash` |
| `--multi-angle` | 多角度 LoRA 模式（Qwen 图像编辑） | - |
| `--angles-360` | 生成 8 个方位角（从前到左前） | - |
| `--angles-360-video` | 使用 i2v 在角度之间生成循环的 360 度视频（需要 ffmpeg） | - |
| `--azimuth <字符串>` | 前面 | `front` | 后面左 | `right` | 后面右 | `back` | 后面左 | `left` | 前面左 |
| `--elevation <字符串>` | 低角度 | `low-angle` | 眼平 | `elevated` | 高角度 |
| `--distance <字符串>` | 特写 | `close-up` | 中等 | `wide` | 中等 |
| `--angle-strength <数字>` | 多角度的 LoRA 强度 | 0.9 |
| `--angle-description <文本>` | 可选的主体描述 | - |
| `--steps <数字>` | 覆盖步骤（取决于模型） | - |
| `--guidance <数字>` | 覆盖指导（取决于模型） | - |
| `--output-format <格式>` | 图像输出格式：png | `jpg` | png |
| `--sampler <名称>` | 采样器（取决于模型） | - |
| `--scheduler <名称>` | 调度器（取决于模型） | - |
| `--lora <id>` | LoRA ID（可重复，仅用于编辑） | - |
| `--lora-sids` | 逗号分隔的 LoRA IDs | - |
| `--lora-strength <数字>` | LoRA 强度（可重复） | - |
| `--lora-strengths <数字>` | 逗号分隔的 LoRA 强度 | - |
| `--token-type <类型>` | 令牌类型：spark | `sogni` | spark |
| `--balance, --balances` | 显示 SPARK/SOGNI 的平衡情况并退出 | - |
| `-c, --context <路径>` | 用于编辑的上下文图片 | - |
| `--last-image` | 使用最后生成的图片作为上下文/参考 | - |
| `--video, -v` | 生成视频而不是图片 | - |
| `--workflow <类型>` | 视频工作流程（t2v | `i2v` | `s2v` | `v2v` | `animate-move` | `animate-replace` | 推断 |
| `--fps <数字>` | 每秒帧数（视频） | 16 |
| `--duration <秒>` | 视频时长（秒） | 5 |
| `--frames <数字>` | 覆盖总帧数（视频） | - |
| `--auto-resize-assets` | 自动调整视频资源大小 | true |
| `--no-auto-resize-assets` | 禁用自动调整 | - |
| `--estimate-video-cost` | 估算视频成本并退出（需要 `--steps`） | - |
| `--photobooth` | 面部转移模式（InstantID + SDXL Turbo） | - |
| `--cn-strength <数字>` | ControlNet 强度（面部转移） | 0.8 |
| `--cn-guidance-end <数字>` | ControlNet 指导结束点（面部转移） | 0.3 |
| `--ref <路径>` | 视频或面部转移的参考图片 | 必需 |
| `--ref-end <路径>` | i2v 插值的结束帧 | - |
| `--ref-audio <路径>` | s2v 的参考音频 | - |
| `--ref-video <路径>` | 动画/`v2v` 工作的参考视频 | - |
| `--controlnet-name <名称>` | `v2v` 的 ControlNet 类型：canny | `pose` | `depth` | `detailer` | - |
| `--controlnet-strength <数字>` | `v2v` 的 ControlNet 强度（0.0-1.0） | 0.8 |
| `--sam2-coordinates <坐标>` | SAM2 点击坐标（用于 animate-replace） | （x,y 或 x1,y1;x2,y2） | - |
| `--trim-end-frame` | 修剪最后一帧以实现无缝视频拼接 | - |
| `--first-frame-strength <数字>` | 开始帧的关键帧强度 | 0.0-1.0 | - |
| `--last-frame-strength <数字>` | 结束帧的关键帧强度 | 0.0-1.0 | - |
| `--last` | 显示最后一次渲染的信息 | - |
| `--json` | JSON 输出 | false |
| `--strict-size` | 不要自动调整 i2v 视频大小以符合参考尺寸限制 | false |
| `-q, --quiet` | 不显示进度信息 | false |
| `--extract-last-frame <视频> <图片>` | 从视频中提取最后一帧（安全的 ffmpeg 包装器） | - |
| `--concat-videos <输出> <剪辑...>` | 连接视频剪辑（安全的 ffmpeg 包装器） | - |
| `--list-media [类型]` | 列出最近的传入媒体（图片 | `audio` | `all`） | 图片 |

## OpenClaw 配置默认值

当作为 OpenClaw 插件安装时，`sogni-gen` 会从以下路径读取默认值：

`~/.openclaw/openclaw.json`

```json
{
  "plugins": {
    "entries": {
      "sogni-gen": {
        "enabled": true,
        "config": {
          "defaultImageModel": "z_image_turbo_bf16",
          "defaultEditModel": "qwen_image_edit_2511_fp8_lightning",
          "defaultPhotoboothModel": "coreml-sogniXLturbo_alpha1_ad",
          "videoModels": {
            "t2v": "wan_v2.2-14b-fp8_t2v_lightx2v",
            "i2v": "wan_v2.2-14b-fp8_i2v_lightx2v",
            "s2v": "wan_v2.2-14b-fp8_s2v_lightx2v",
            "animate-move": "wan_v2.2-14b-fp8_animate-move_lightx2v",
            "animate-replace": "wan_v2.2-14b-fp8_animate-replace_lightx2v",
            "v2v": "ltx2-19b-fp8_v2v_distilled"
          },
          "defaultVideoWorkflow": "t2v",
          "defaultNetwork": "fast",
          "defaultTokenType": "spark",
          "seedStrategy": "prompt-hash",
          "modelDefaults": {
            "flux1-schnell-fp8": { "steps": 4, "guidance": 3.5 },
            "flux2_dev_fp8": { "steps": 20, "guidance": 7.5 }
          },
          "defaultWidth": 768,
          "defaultHeight": 768,
          "defaultCount": 1,
          "defaultFps": 16,
          "defaultDurationSec": 5,
          "defaultImageTimeoutSec": 30,
          "defaultVideoTimeoutSec": 300,
          "credentialsPath": "~/.config/sogni/credentials",
          "lastRenderPath": "~/.config/sogni/last-render.json",
          "mediaInboundDir": "~/.clawdbot/media/inbound"
        }
      }
    }
  }
}
```

CLI 标志总是会覆盖这些默认值。如果您的 OpenClaw 配置位于其他位置，请设置 `OPENCLAW_CONFIG_PATH`。
种子策略：`prompt-hash`（确定性）或 `random`。

## 图像模型

| 模型 | 速度 | 用途 |
|-------|-------|----------|
| `z_image_turbo_bf16` | 快速（约 5-10 秒） | 通用用途，默认 |
| `flux1-schnell-fp8` | 非常快 | 快速迭代 |
| `flux2_dev_fp8` | 慢速（约 2 分钟） | 高质量 |
| `chroma-v.46-flash_fp8` | 中等 | 平衡 |
| `qwen_image_edit_2511_fp8` | 中等 | 带有上下文的图像编辑（最多 3 个） |
| `qwen_image_edit_2511_fp8_lightning` | 快速 | 快速图像编辑 |
| `coreml-sogniXLturbo_alpha1_ad` | 快速 | 使用 SDXL Turbo 的面部转移 |

## 视频模型

### WAN 2.2 模型

| 模型 | 速度 | 用途 |
|-------|-------|----------|
| `wan_v2.2-14b-fp8_i2v_lightx2v` | 快速 | 默认视频生成 |
| `wan_v2.2-14b-fp8_i2v` | 慢速 | 更高质量的视频 |
| `wan_v2.2-14b-fp8_t2v_lightx2v` | 快速 | 文本到视频 |
| `wan_v2.2-14b-fp8_s2v_lightx2v` | 快速 | 声音到视频 |
| `wan_v2.2-14b-fp8_animate-move_lightx2v` | 快速 | 动画移动 |
| `wan_v2.2-14b-fp8_animate-replace_lightx2v` | 快速 | 动画替换 |

### LTX-2 模型

| 模型 | 速度 | 用途 |
|-------|-------|----------|
| `ltx2-19b-fp8_t2v_distilled` | 快速（约 2-3 分钟） | 文本到视频，8 步骤 |
| `ltx2-19b-fp8_t2v` | 中等（约 5 分钟） | 文本到视频，20 步骤 |
| `ltx2-19b-fp8_v2v_distilled` | 快速（约 3 分钟） | 使用 ControlNet 的视频到视频 |
| `ltx2-19b-fp8_v2v` | 中等（约 5 分钟） | 使用 ControlNet 的视频到视频 |

## 带有上下文的图像编辑

使用参考图片编辑图像（Qwen 模型最多支持 3 个参考图片）：

```bash
# Single context image
node sogni-gen.mjs -c photo.jpg "make the background a beach"

# Multiple context images (subject + style)
node sogni-gen.mjs -c subject.jpg -c style.jpg "apply the style to the subject"

# Use last generated image as context
node sogni-gen.mjs --last-image "make it more vibrant"
```

当没有使用 `-m` 选项提供参考图片时，默认使用 `qwen_image_edit_2511_fp8_lightning`。

## 面部转移（Photobooth）

使用 InstantID ControlNet 从面部照片生成风格化的肖像。当用户请求“photobooth”或希望将自己的面部转移到某种风格中时，使用 `--photobooth` 并指定面部图片作为 `--ref`。

```bash
# Basic photobooth
node sogni-gen.mjs --photobooth --ref face.jpg "80s fashion portrait"

# Multiple outputs
node sogni-gen.mjs --photobooth --ref face.jpg -n 4 "LinkedIn professional headshot"

# Custom ControlNet tuning
node sogni-gen.mjs --photobooth --ref face.jpg --cn-strength 0.6 --cn-guidance-end 0.5 "oil painting"
```

默认使用 SDXL Turbo（`coreml-sogniXLturbo_alpha1_ad`），分辨率为 1024x1024。面部图片通过 `--ref` 传递，并根据提示进行风格化。不能与 `--video` 或 `-c/--context` 选项同时使用。

**代理使用方法：**
```bash
# Photobooth: stylize a face photo
node {{skillDir}}/sogni-gen.mjs -q --photobooth --ref /path/to/face.jpg -o /tmp/stylized.png "80s fashion portrait"

# Multiple photobooth outputs
node {{skillDir}}/sogni-gen.mjs -q --photobooth --ref /path/to/face.jpg -n 4 -o /tmp/stylized.png "LinkedIn professional headshot"
```

## 多角度生成

使用多角度 LoRA 从单张参考图片生成特定的相机角度：

```bash
# Single angle
node sogni-gen.mjs --multi-angle -c subject.jpg \
  --azimuth front-right --elevation eye-level --distance medium \
  --angle-strength 0.9 \
  "studio portrait, same person"

# 360 sweep (8 azimuths)
node sogni-gen.mjs --angles-360 -c subject.jpg --distance medium --elevation eye-level \
  "studio portrait, same person"

# 360 sweep video (looping mp4, uses i2v between angles; requires ffmpeg)
node sogni-gen.mjs --angles-360 --angles-360-video /tmp/turntable.mp4 \
  -c subject.jpg --distance medium --elevation eye-level \
  "studio portrait, same person"
```

提示会自动构建，包含所需的 `<sks>` 令牌和选定的相机角度关键词。
`--angles-360-video` 会在连续角度之间生成 i2v 剪辑（包括从后到前），并使用 ffmpeg 将它们连接起来以形成无缝循环。

### 360 度视频最佳实践

当用户请求“360 度视频”时，请遵循以下工作流程：

1. **默认相机参数**（除非用户特别指定）：
   - **高度**：默认为 **中等** |
   - **距离**：默认为 **中等** |

2. **将用户术语映射到标志**：
   | 用户输入 | 标志值 |
   |-----------|------------|
   | “高角度” | `--elevation high-angle` |
   | “中等角度” | `--elevation eye-level` |
   | “低角度” | `--elevation low-angle` |
   | “特写” | `--distance close-up` |
   | “中等距离” | `--distance medium` |
   | “远距离” | `--distance wide` |

3. **始终使用第一帧/最后一帧拼接** - `--angles-360-video` 标志会自动处理这一点，通过在连续角度之间生成 i2v 剪辑（包括从后到前）以实现无缝循环。

### 过渡视频规则

对于**任何过渡视频操作**，始终使用 **Sogni 功能/插件**（而不是原始的 ffmpeg 或其他 shell 命令）。使用内置的 `--extract-last-frame`、`--concat-videos` 和 `--looping` 标志进行视频处理。

### 资金不足处理

当出现“Debit Error: Insufficient funds”（余额不足）错误时，回复：

“余额不足。请在 [https://app.sogni.ai/](https://app.sogni.ai/) 领取 50 个免费的 Spark 积分。”

## 视频生成

从参考图片生成视频：

```bash
# Text-to-video (t2v)
node sogni-gen.mjs --video "ocean waves at sunset"

# Basic video from image
node sogni-gen.mjs --video --ref cat.jpg -o cat.mp4 "cat walks around"

# Use last generated image as reference
node sogni-gen.mjs --last-image --video "gentle camera pan"

# Custom duration and FPS
node sogni-gen.mjs --video --ref scene.png --duration 10 --fps 24 "zoom out slowly"

# Sound-to-video (s2v)
node sogni-gen.mjs --video --ref face.jpg --ref-audio speech.m4a \
  -m wan_v2.2-14b-fp8_s2v_lightx2v "lip sync talking head"

# Animate (motion transfer)
node sogni-gen.mjs --video --ref subject.jpg --ref-video motion.mp4 \
  --workflow animate-move "transfer motion"
```

## 使用 ControlNet 的视频到视频（V2V）转换

使用 LTX-2 模型和 ControlNet 进行视频转换：

```bash
# Basic v2v with canny edge detection
node sogni-gen.mjs --video --workflow v2v --ref-video input.mp4 \
  --controlnet-name canny "stylized anime version"

# V2V with pose detection and custom strength
node sogni-gen.mjs --video --workflow v2v --ref-video dance.mp4 \
  --controlnet-name pose --controlnet-strength 0.7 "robot dancing"

# V2V with depth map
node sogni-gen.mjs --video --workflow v2v --ref-video scene.mp4 \
  --controlnet-name depth "watercolor painting style"
```

ControlNet 类型：`canny`（边缘检测）、`pose`（身体姿态）、`depth`（深度图）、`detailer`（细节增强）。

## 照片修复

使用 Qwen 图像编辑技术修复损坏的复古照片：

```bash
# Basic restoration
sogni-gen -c damaged_photo.jpg -o restored.png \
  "professionally restore this vintage photograph, remove damage and scratches"

# Detailed restoration with preservation hints
sogni-gen -c old_photo.jpg -o restored.png -w 1024 -h 1280 \
  "restore this vintage photo, remove peeling, tears and wear marks, \
  preserve natural features and expression, maintain warm nostalgic color tones"
```

**良好的修复提示：**
- 描述损坏情况：例如“剥落”、“划痕”、“撕裂”、“褪色”
- 指定要保留的部分：例如“自然特征”、“眼睛颜色”、“头发”、“表情”
- 提及颜色色调的时代：例如“1970 年代的暖色调”、“复古棕褐色”

**查找接收到的图片（通过 Telegram 等）：**
```bash
node {{skillDir}}/sogni-gen.mjs --json --list-media images
```

**请勿使用 `ls`、`cp` 或其他 shell 命令来浏览用户文件**。始终使用 `--list-media` 来查找传入的媒体文件。

## 重要关键词规则

- 如果用户消息中包含“photobooth”（不区分大小写），始终使用 `--photobooth` 模式，并将 `--ref` 设置为用户提供的面部图片。
- 对于此类请求，优先使用此规则而非通用的图像编辑流程（`-c`）。

## 代理使用方法

当用户请求生成/绘制/创建图片时：

```bash
# Generate and save locally
node {{skillDir}}/sogni-gen.mjs -q -o /tmp/generated.png "user's prompt"

# Edit an existing image
node {{skillDir}}/sogni-gen.mjs -q -c /path/to/input.jpg -o /tmp/edited.png "make it pop art style"

# Generate video from image
node {{skillDir}}/sogni-gen.mjs -q --video --ref /path/to/image.png -o /tmp/video.mp4 "camera slowly zooms in"

# Generate text-to-video
node {{skillDir}}/sogni-gen.mjs -q --video -o /tmp/video.mp4 "ocean waves at sunset"

# Photobooth: stylize a face photo
node {{skillDir}}/sogni-gen.mjs -q --photobooth --ref /path/to/face.jpg -o /tmp/stylized.png "80s fashion portrait"

# Check current SPARK/SOGNI balances (no prompt required)
node {{skillDir}}/sogni-gen.mjs --json --balance

# Find user-sent images/audio
node {{skillDir}}/sogni-gen.mjs --json --list-media images

# Then send via message tool with filePath
```

**安全提示：** 代理必须使用 CLI 的内置标志（`--extract-last-frame`、`--concat-videos`、`--list-media`）进行所有文件操作和视频处理。切勿直接运行原始的 shell 命令（如 `ffmpeg`、`ls`、`cp` 等）。

## 在两张图片之间进行动画处理（第一帧/最后一帧）

当用户请求在两张图片之间进行动画处理时，使用 `--ref`（第一帧）和 `--ref-end`（最后一帧）来创建一个创意插值视频：

```bash
# Animate from image A to image B
node {{skillDir}}/sogni-gen.mjs -q --video --ref /tmp/imageA.png --ref-end /tmp/imageB.png -o /tmp/transition.mp4 "descriptive prompt of the transition"
```

### 将视频动画转换为图片（场景延续）

当用户请求将视频动画转换为图片（或“将视频延续到新场景”时）：

1. 使用内置的安全包装器提取现有视频的**最后一帧**：
   ```bash
   node {{skillDir}}/sogni-gen.mjs --extract-last-frame /tmp/existing.mp4 /tmp/lastframe.png
   ```
2. 使用最后一帧作为 `--ref`，目标图片作为 `--ref-end` 生成新视频：
   ```bash
   node {{skillDir}}/sogni-gen.mjs -q --video --ref /tmp/lastframe.png --ref-end /tmp/target.png -o /tmp/continuation.mp4 "scene transition prompt"
   ```
3. 使用内置的安全包装器连接视频：
   ```bash
   node {{skillDir}}/sogni-gen.mjs --concat-videos /tmp/full_sequence.mp4 /tmp/existing.mp4 /tmp/continuation.mp4
   ```

这样可以确保视觉连续性——新视频将从上一视频的结束处开始。

**切勿直接运行原始的 `ffmpeg` 命令**。始终使用 `--extract-last-frame` 和 `--concat-videos` 进行视频处理。

**在以下情况下始终遵循此规则：**
- 用户请求“将图片 A 动画转换为图片 B” → 使用 `--ref A --ref-end B`
- 用户请求“将此视频动画转换为图片” → 提取最后一帧，将其作为 `--ref`，目标图片作为 `--ref-end`，然后进行拼接
- 用户请求“将此视频延续到新图片” → 同上

## JSON 输出

```json
{
  "success": true,
  "prompt": "a cat wearing a hat",
  "model": "z_image_turbo_bf16", 
  "width": 512,
  "height": 512,
  "urls": ["https://..."],
  "localPath": "/tmp/cat.png"
}
```

在出现错误时（使用 `--json`），脚本会返回一个 JSON 对象，例如：

```json
{
  "success": false,
  "error": "Video width and height must be divisible by 16 (got 500x512).",
  "errorCode": "INVALID_VIDEO_SIZE",
  "hint": "Choose --width/--height divisible by 16. For i2v, also match the reference aspect ratio."
}
```

**平衡检查示例（`--json --balance`）：**

```json
{
  "success": true,
  "type": "balance",
  "spark": 12.34,
  "sogni": 0.56
}
```

## 成本

使用您的 Sogni 账户中的 Spark 令牌。512x512 的图片最具成本效益。

## 故障排除

- **认证错误**：检查 `~/.config/sogni/credentials` 中的凭据 |
- **i2v 尺寸问题**：视频尺寸有限制（最小 480px，最大 1536px，必须是 16 的倍数）。对于 i2v，客户端包装器会调整参考图片的大小（`fit: inside`），并将调整后的尺寸作为最终视频尺寸。由于存在四舍五入，请求的尺寸可能会导致最终尺寸无效（例如：请求 `1024x1536`，但实际尺寸可能变为 `1024x1535`）。
- **自动调整**：如果使用本地 `--ref`，脚本会自动调整请求的尺寸以避免非 16 的参考尺寸。
- **如果脚本调整了尺寸但您希望强制使用原始尺寸**：传递 `--strict-size`，它将显示建议的 `--width/--height`。
- **超时**：尝试使用更快的模型或增加 `-t` 超时时间 |
- **没有工作节点**：请查看 [https://sogni.ai/](https://sogni.ai/) 以获取网络状态信息
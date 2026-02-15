# ai-media - 人工智能媒体生成工具

这是一个全栈的人工智能媒体生成工具，由GPU服务器（RTX 3090/3080/2070S）提供支持。

## 功能

1. **图像生成** — 通过ComfyUI生成逼真的图像（支持z-image和Juggernaut XL模型）  
2. **视频生成** — 通过ComfyUI合成视频（支持AnimateDiff和LTX-2模型）  
3. **动画头像** — 通过SadTalker生成具有动画效果的对话头像  
4. **语音合成** — 通过Voxtral库实现自然的语音合成（基于whisper.cpp技术）

## GPU服务器配置

- **主机地址：** `${GPU_USER}@${GPU_HOST}`  
- **SSH密钥：** `~/.ssh/id_ed25519_gpu`  
- **ComfyUI**：`/data/ai-stack/comfyui/`（端口8188）  
- **SadTalker**：`/data/ai-stack/sadtalker/`  
- **Voxtral**：`/data/ai-stack/whisper/`  
- **输出目录：** `/data/ai-stack/output/`  

## 使用方法

### 生成图像

```bash
./scripts/image.sh "lady on beach at sunset" realistic
./scripts/image.sh "cyberpunk cityscape" artistic
```

**参数：**
- `$1`：提示文本  
- `$2`：风格（realistic | artistic）——可选，默认为realistic  

**输出结果：** 生成的图像文件路径（例如：`/data/ai-stack/output/image_001.png`）

### 生成视频

```bash
./scripts/video.sh "waves crashing on shore" animatediff 4
./scripts/video.sh "city traffic timelapse" ltx2 8
```

**参数：**
- `$1`：提示文本  
- `$2`：使用的模型（animateDiff | ltx2）——可选，默认为animateDiff  
- `$3`：视频时长（秒）——可选，默认为4秒  

**输出结果：** 生成的视频文件路径（例如：`/data/ai-stack/output/video_001.mp4`）

### 生成动画头像

```bash
./scripts/talking-head.sh "Hello, I'm Agent" gentle input.jpg
./scripts/talking-head.sh "Welcome to the future" neutral photo.png
```

**参数：**
- `$1`：对话文本  
- `$2`：语音风格（gentle | neutral | energetic）——可选，默认为gentle  
- `$3`：头像图片路径——可选，如未提供则使用默认头像  

**输出结果：** 生成的动画头像视频文件路径（例如：`/data/ai-stack/output/talking_001.mp4`）

### 生成音频

```bash
./scripts/audio.sh "This is a test message" en male
./scripts/audio.sh "Bonjour le monde" fr female
```

**参数：**
- `$1`：要朗读的文本  
- `$2`：语言代码（en | fr | es等）——可选，默认为en  
- `$3`：语音性别（male | female）——可选，默认为male  

**输出结果：** 生成的音频文件路径（例如：`/data/ai-stack/output/audio_001.wav`）

## 可用的模型

### 图像模型
- **z-image**：60亿参数，基于S3-DiT架构，具有高度逼真的图像效果（下载中，已完成43%）  
- **Juggernaut XL v9**：基于SDXL架构，功能丰富（7.1GB，已准备好使用）

### 视频模型
- **AnimateDiff**：15亿参数的模型，适用于生成152x152像素的视频（已测试并通过）  
- **LTX-2**：190亿参数的模型，生成高质量视频（14GB的检查点文件已准备好，Gemma编码器也已准备好）

### 动画头像模型
- **SadTalker**：基于音频驱动的头部动画模型（已测试并通过）

### 语音模型
- **Voxtral**：基于whisper.cpp实现的语音合成系统

## 依赖项

所有依赖项均已预装在GPU服务器上：
- ComfyUI（包含自定义节点AnimateDiff-Evolved和VideoHelperSuite）  
- SadTalker（包含面部增强功能）  
- Voxtral（包含whisper.cpp库）  
- FFmpeg（用于视频编码）

## 错误处理

- 脚本在执行前会检查SSH连接是否正常  
- 确保GPU服务器正在运行  
- 会返回有意义的错误信息  
- 会自动清理生成失败的文件

## 性能

- **图像生成：** 1024x1024像素图像的生成时间约为10-20秒  
- **视频生成（AnimateDiff）：** 512x512像素、24帧每秒的视频生成时间约为20-30秒  
- **视频生成（LTX-2）：** 768x512像素、24帧每秒的视频生成时间约为60-90秒  
- **动画头像：** 10秒长度的视频生成时间约为30-40秒  
- **音频生成：** 30秒长度的音频文件生成时间约为2-5秒

## 未来计划

- [ ] 支持批量生成  
- [ ] 实现风格转换功能  
- [ ] 视频的缩放处理（空间和时间维度）  
- [ ] 多语言语音克隆功能  
- [ ] 实时预览流媒体功能  

---

**开发状态：** 正在开发中  
**维护者：** Agent  
**GPU服务器：** ${GPU_USER}@${GPU_HOST}`
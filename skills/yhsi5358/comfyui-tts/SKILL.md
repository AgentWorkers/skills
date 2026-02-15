---
name: comfyui-tts
description: "使用 ComfyUI 的 Qwen-TTS 服务生成语音音频。当用户需要通过 ComfyUI 进行文本转语音（text-to-speech）或语音生成（voice generation）时，可以调用该服务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "bins": ["curl", "jq"] },
        "install": [],
      },
  }
---

# ComfyUI TTS 技能

该技能使用 ComfyUI 的 Qwen-TTS 服务生成语音音频，允许您通过 ComfyUI 的 API 将文本转换为语音。

## 配置

### 环境变量

设置以下环境变量以配置 ComfyUI 连接：

```bash
export COMFYUI_HOST="localhost"      # ComfyUI server host
export COMFYUI_PORT="8188"           # ComfyUI server port
export COMFYUI_OUTPUT_DIR=""         # Optional: Custom output directory
```

## 使用方法

### 基本文本转语音

使用默认设置将文本转换为音频：

```bash
scripts/tts.sh "你好，世界"
```

### 高级选项

自定义语音特性：

```bash
# Specify character and style
scripts/tts.sh "你好" --character "Girl" --style "Emotional"

# Change model size
scripts/tts.sh "你好" --model "3B"

# Specify output file
scripts/tts.sh "你好" --output "/path/to/output.wav"

# Combine options
scripts/tts.sh "你好，这是测试" \
  --character "Girl" \
  --style "Emotional" \
  --model "1.7B" \
  --output "~/audio/test.wav"
```

### 可用选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--character` | 语音角色（女/男等） | "Girl" |
| `--style` | 说话风格（情感化/中性等） | "Emotional" |
| `--model` | 模型大小（0.5B/1.7B/3B） | "1.7B" |
| `--output` | 输出文件路径 | 自动生成 |
| `--temperature` | 生成温度（0-1） | 0.9 |
| `--top-p` | Top-p 采样率 | 0.9 |
| `--top-k` | Top-k 采样率 | 50 |

## 工作流程

该技能执行以下步骤：

1. **构建工作流程**：使用您的文本和设置构建 ComfyUI 的工作流程 JSON 文件。
2. **提交任务**：将工作流程发送到 ComfyUI 的 `/prompt` 端点。
3. **查询状态**：通过 `/history` 端点监控任务完成情况。
4. **获取音频**：返回生成的音频文件的路径。

## 故障排除

### 连接被拒绝

- 确认 ComfyUI 正在运行：`curl http://$COMFYUI_HOST:$COMFYUI_PORT/system_stats`
- 检查主机和端口设置。

### 任务超时

- 大型模型（3B）生成时间较长，尝试使用较小的模型（0.5B、1.7B）以获得更快结果。

### 未找到输出文件

- 检查 ComfyUI 的输出目录配置。
- 确认文件权限。

## API 参考

该技能使用 ComfyUI 的原生 API 端点：

- `POST /prompt` - 提交工作流程。
- `GET /history` - 查询任务状态。
- 输出文件保存在 ComfyUI 配置的输出目录中。
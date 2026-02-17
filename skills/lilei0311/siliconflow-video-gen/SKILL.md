---
name: siliconflow-video-gen
description: 使用 SiliconFlow API 和 Wan2.2 模型生成视频。支持文本转视频（Text-to-Video）和图像转视频（Image-to-Video）两种功能。
env:
  - SILICONFLOW_API_KEY
files:
  config:
    - ~/.openclaw/openclaw.json
---
# SiliconFlow 视频生成技能

使用 SiliconFlow API 和 Wan2.2 模型生成视频。支持文本转视频（Text-to-Video）和图片转视频（Image-to-Video）两种功能。

## 特点

- 🎬 **文本转视频**：根据文本描述生成视频
- 🖼️ **图片转视频**：为静态图片添加动态效果
- 🎥 **电影级画质**：由 Wan2.2（140 亿参数）提供支持
- 🔑 **自动 API 密钥检测**：从环境变量或 OpenClaw 配置文件中读取 API 密钥

## 需求

- **环境变量**：`SILICONFLOW_API_KEY`
- **可选配置文件**：`~/.openclaw/openclaw.json`（用于自动检测 API 密钥）

## 安装

```bash
npx clawhub install siliconflow-video-gen
```

## 配置

设置您的 SiliconFlow API 密钥：

```bash
export SILICONFLOW_API_KEY="your-api-key"
```

或在 OpenClaw 中进行配置：

```json
{
  "models": {
    "providers": {
      "siliconflow": {
        "apiKey": "your-api-key"
      }
    }
  }
}
```

## 使用方法

### 文本转视频

```bash
python3 scripts/generate.py "A woman walking in a blooming garden, cinematic shot"
```

### 图片转视频

```bash
python3 scripts/generate.py "Camera slowly zooming in" --image-url https://example.com/image.jpg
```

## 模型

| 模型 | 类型 | 费用 |
|-------|------|------|
| `Wan-AI/Wan2.2-T2V-A14B` | 文本转视频 | 每个视频 2 元 |
| `Wan-AI/Wan2.2-T2V-A14B` | 图片转视频 | 每个视频 2 元 |

## 安全说明

- 该技能需要 API 密钥才能调用 SiliconFlow 服务
- 脚本仅从 `~/.openclaw/openclaw.json` 文件中读取 API 密钥
- 除传输到 `api.siliconflow.cn` 外，不会传输任何敏感数据
- 在提供凭据之前，请先查看 `scripts/generate.py` 文件中的代码

## 作者

MaxStorm 团队

## 许可证

MIT 许可证
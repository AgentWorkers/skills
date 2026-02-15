---
name: siliconflow-image-gen
description: 使用 SiliconFlow API 生成图像（支持 FLUX.1、Stable Diffusion 等模型）
env:
  - SILICONFLOW_API_KEY
files:
  config:
    - ~/.openclaw/openclaw.json
---
# SiliconFlow 图像生成技能

使用 SiliconFlow API 生成图像，支持 FLUX.1、Stable Diffusion 等模型。

## 特点

- 🎨 **多种模型**：FLUX.1-schnell（免费）、FLUX.1-dev、Stable Diffusion 3.5
- 🔑 **自动检测 API 密钥**：从环境变量或 OpenClaw 配置文件中读取 API 密钥
- 💾 **自动下载**：将生成的图像保存到本地
- 📱 **兼容 OpenClaw**：专为 OpenClaw Agent 集成设计

## 必需条件

- **环境变量**：`SILICONFLOW_API_KEY`
- **可选配置文件**：`~/.openclaw/openclaw.json`（用于自动检测 API 密钥）

## 安装

```bash
npx clawhub install siliconflow-image-gen
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

### 命令行

```bash
# Generate with default model (FLUX.1-schnell)
python3 scripts/generate.py "A cup of coffee on wooden table"

# Specify model
python3 scripts/generate.py "Sunset over mountains" --model "black-forest-labs/FLUX.1-dev"

# Save to file
python3 scripts/generate.py "Cute cat" --output ~/Desktop/cat.png
```

## 可用模型

| 模型 | 费用 | 图像质量 | 执行速度 |
|-------|------|---------|-------|
| `black-forest-labs/FLUX.1-schnell` | 免费 | 良好 | 快速 |
| `black-forest-labs/FLUX.1-dev` | 付费 | 优秀 | 中等 |
| `stabilityai/stable-diffusion-3-5-large` | 付费 | 优秀 | 中等 |

## 安全说明

- 使用此技能需要 API 密钥来调用 SiliconFlow 服务
- 脚本仅从 `~/.openclaw/openclaw.json` 文件中读取 API 密钥
- 除传输到 `api.siliconflow.cn` 外，不会传输任何敏感数据
- 在提供凭据之前，请先查看 `scripts/generate.py` 文件中的代码

## 作者

MaxStorm 团队

## 许可证

MIT 许可证
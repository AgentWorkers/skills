---
name: drawthings
description: 通过 API 使用 DrawThings（Stable Diffusion）生成图像。该工具适用于从文本提示创建图像、运行图像生成工作流程或批量生成图像的场景。DrawThings 在 Mac 上以本地模式运行，并支持 MLX/CoreML 加速技术。
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      env: ["DRAWTHINGS_URL"]
---

# DrawThings 图像生成

使用 DrawThings 生成图像，这是一个基于 MLX/CoreML 加速的本地 Stable Diffusion 实现工具。DrawThings 提供了一个与 Automatic1111 兼容的 API，用于程序化图像生成。

## 使用场景

当您需要以下操作时，可以使用此功能：
- 根据文本提示生成图像
- 创建某个概念的多种变体
- 批量生成多张图像
- 测试不同的模型/采样器/设置
- 生成具有特定尺寸或质量要求的图像

## 配置

设置 `DRAWTHINGS_URL` 环境变量（默认值为 http://127.0.0.1:7860）：

```bash
export DRAWTHINGS_URL="http://127.0.0.1:7860"
```

或在 OpenClaw 中进行配置：
```bash
openclaw config set env.DRAWTHINGS_URL "http://127.0.0.1:7860"
```

## 快速入门

生成单张图像：
```bash
python3 scripts/generate.py "a cyberpunk cat in neon city"
```

使用自定义设置：
```bash
python3 scripts/generate.py "a cyberpunk cat" \
  --steps 20 \
  --cfg-scale 7.5 \
  --width 768 \
  --height 768 \
  --sampler "DPM++ 2M Karras"
```

批量生成（5 种变体）：
```bash
python3 scripts/generate.py "a fantasy landscape" --batch-size 5
```

将图像保存到指定位置：
```bash
python3 scripts/generate.py "portrait photo" --output ./outputs/portrait.png
```

## API 使用方法

该功能提供了一个 Python 脚本，用于调用 DrawThings 的 API（兼容 Automatic1111）：

**主要接口：** `POST /sdapi/v1/txt2img`

**常用参数：**
- `prompt` - 图像的文本描述
- `negative_prompt` - 图像中应避免的内容
- `steps` - 扩散步骤数（8-50，默认值：20）
- `sampler_name` - 采样器算法（默认值：“DPM++ 2M Karras”）
- `cfg_scale` - 无分类器的引导比例（1.0-20.0，默认值：7.0）
- `width` / `height` - 图像尺寸（默认值：512x512）
- `batch_size` - 要生成的图像数量（默认值：1）
- `seed` - 用于保证结果一致性的随机种子（-1 表示随机生成）

请参阅 `references/api-reference.md` 以获取完整的 API 文档。

## 预设配置

**快速模式（8 步骤，使用 UniPC Trailing 算法）：**
```bash
python3 scripts/generate.py "your prompt" --preset fast
```

**高质量模式（30 步骤，使用 DPM++ 2M Karras 算法）：**
```bash
python3 scripts/generate.py "your prompt" --preset quality
```

**NFT 优化模式（适用于 512x512 图像，细节丰富）：**
```bash
python3 scripts/generate.py "your prompt" --preset nft
```

## 工作流程示例

- **生成角色变体：**
```bash
python3 scripts/generate.py "electric sheep, glowing wool, cyberpunk" \
  --batch-size 10 \
  --steps 20 \
  --cfg-scale 7.5
```

- **生成高分辨率图像：**
```bash
python3 scripts/generate.py "detailed portrait" \
  --width 1024 \
  --height 1024 \
  --steps 30 \
  --sampler "DPM++ 2M Karras"
```

- **确保结果可重复：**
```bash
python3 scripts/generate.py "landscape" --seed 42
# Re-run with same seed for identical output
```

## 输出结果

生成的图像将以 PNG 格式保存，并包含以下元数据：
- 文本提示
- 避免的内容
- 生成参数（步骤数、采样器、引导比例等）
- 时间戳和随机种子

默认保存路径：`./drawthings_output_YYYYMMDD_HHMMSS.png`

## 故障排除

**“连接失败”**
- 确保 DrawThings 正在运行
- 检查 DrawThings 的偏好设置中是否启用了 API 服务器
- 确认端口号正确（默认值：7860）

**“生成失败”**
- 检查提示内容的长度（每个 CLIP 模型的最大长度约为 75 个字符）
- 如果内存不足，请减小图像尺寸
- 尝试使用其他采样器

**生成速度较慢**
- 减少步骤数（草图生成时使用 8-12 步骤）
- 减小图像尺寸（例如 512x512）
- 使用更快的采样器（如 UniPC、Euler A）

**画布显示问题（仅影响视觉效果）**
- DrawThings 的用户界面在生成新图像时不会清除旧图像
- 新图像会显示在旧图像之上，但这仅是视觉上的问题，API 输出不受影响

## 提示

- **CFG Scale**：数值较低（1-3）适合创意/艺术性生成；数值较高（7-12）适合精确遵循文本提示
- **步骤数**：草图生成时使用 8-12 步骤，最终图像使用 20-30 步骤，超过 50 步骤的情况较少见
- **采样器**：UniPC 和 Euler A 生成速度快，DPM++ 2M Karras 生成图像质量较高，LCM 生成速度最快
- **图像尺寸**：建议使用 64 的倍数（如 512、768、1024）
- **批量处理**：使用 `--batch-size` 参数进行批量生成，无需多次调用脚本

## 模型

DrawThings 支持多种 Stable Diffusion 模型。要更换模型，请执行以下操作：
1. 打开 DrawThings 应用程序
2. 从用户界面中选择所需的模型
3. API 会自动使用当前选定的模型

有关推荐模型和下载来源，请参阅 `references/models.md`。
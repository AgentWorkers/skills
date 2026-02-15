---
name: civitai-ai-art
description: 使用 CivitAI 的 JavaScript SDK 生成 AI 艺术品。当用户希望使用 CivitAI 的 Stable Diffusion 模型创建 AI 生成的图像时，可以调用此功能，这些图像包括动漫风格的插画、角色艺术，或者根据特定提示、否定提示（negative prompts）、种子（seeds）和采样设置（sampling settings）进行自定义生成的图像。
---
# CivitAI AI艺术生成

使用CivitAI的官方JavaScript SDK生成AI艺术作品。

## 先决条件

- Node.js 18及以上版本的环境
- CivitAI API访问令牌（存储在环境变量`CIVITAI_API_TOKEN`中）
- 已安装`civitai` npm包

## 安装

```bash
npm install civitai
```

## 使用方法

```bash
node scripts/get_illust.js [options]
```

### 选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--prompt` | 主要生成提示（必需） | - |
| `--negative` | 负面提示 | "质量差、最差的质量、最差的细节、草图、审查" |
| `--width` | 图像宽度 | 832 |
| `--height` | 图像高度 | 1216 |
| `--seed` | 随机种子 | random |
| `--steps` | 采样步骤 | 20 |
| `--cfg-scale` | CFG缩放比例 | 5 |
| `--model` | 模型URN标识符 | "urn:air:sdxl:checkpoint:civitai:827184@2514310" |
| `--sampler` | 采样算法 | "Euler a" |
| `--clip-skip` | 跳过CLIP层 | 2 |
| `--output` | 输出文件路径 | "./output.png" |
| `--lora` | LoRA网络URN（可选，格式：`urn,strength`） | - |

### 示例用法

```bash
# 基础生成
node scripts/get_illust.js --prompt "1girl, red hair, blue eyes, maid outfit, smile" --output maid.png

# 高级设置
node scripts/get_illust.js \
  --prompt "1girl, long silver hair, purple eyes, magical girl, cityscape at night" \
  --negative "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet" \
  --width 1024 \
  --height 1536 \
  --steps 28 \
  --cfg-scale 6 \
  --seed 42 \
  --output magical_girl.png

# 使用不同模型
node scripts/get_illust.js \
  --prompt "fantasy landscape, floating islands, waterfalls" \
  --model "urn:air:sdxl:checkpoint:civitai:101055@128641" \
  --output landscape.png

# 使用 LoRA
node scripts/get_illust.js \
  --prompt "1girl, red hair, blue eyes, maid outfit, smile" \
  --lora "urn:air:sdxl:lora:civitai:162141@182559,0.8" \
  --output maid_with_lora.png

# 使用多个 LoRA
node scripts/get_illust.js \
  --prompt "1girl, cat ears, cute smile, IncrsAhri, multiple tails" \
  --lora "urn:air:sd1:lora:civitai:162141@182559,1.0" \
  --lora "urn:air:sd1:lora:civitai:176425@198856,0.6" \
  --output multi_lora.png
```

### Markdown链接示例

生成图片后，使用markdown格式包裹链接：

```markdown
[生成的图片](https://blobs-temp.s3.us-west-004.backblazeb2.com/...)
```

## 计划器选项

可用的采样算法值：

| 采样算法名称 | 枚举值 |
|--------------|------------|
| Euler a | EULER_A |
| Euler | EULER |
| LMS | LMS |
| Heun | HEUN |
| DPM2 | DPM2 |
| DPM2 a | DPM2_A |
| DPM++ 2S a | DPM2_SA |
| DPM++ 2M | DPM2_M |
| DPM++ SDE | DPM_SDE |
| DPM fast | DPM_fast |
| DPM adaptive | DPM_ADAPTIVE |
| LMS Karras | LMS_KARRAS |
| DPM2 Karras | DPM2_KARRAS |
| DPM2 a Karras | DPM2_A_KARRAS |
| DPM++ 2S a Karras | DPM2_SA_KARRAS |
| DPM++ 2M Karras | DPM2_M_KARRAS |
| DPM++ SDE Karras | DPM_SDE_KARRAS |
| DDIM | DDIM |
| PLMS | PLMS |
| UniPC | UNIPC |
| LCM | LCM |
| DDPM | DDPM |
| DEIS | DEIS |

## 注意事项

- 需要Node.js 18及以上版本以支持原生fetch功能
- 请使用环境变量安全地存储API令牌
- 生成的图片受CivitAI服务条款的约束
- 某些模型可能需要特定的权限或订阅
- 脚本默认会等待任务完成
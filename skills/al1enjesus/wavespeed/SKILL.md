---
name: wavespeed
description: "使用 WaveSpeed AI 的 700 多个模型库来生成和编辑图片及视频。适用于以下场景：根据文本提示生成图片（FLUX、Seedream、Qwen）；编辑或修图（nano-banana-pro 可在更换服装/背景的同时保持人物面部不变）；根据图片或文本生成视频（Kling、Veo、Sora、Wan、Hailuo）；或将视频升级为 4K 格式。可使用的功能包括：生成图片、编辑照片、更换背景、更换服装、根据图片制作视频、为照片添加动画效果、将视频升级为 4K 格式，以及使用 nano-banana-pro 工具。"
---
# WaveSpeed AI

通过一个API，您可以调用700多个AI模型（包括Google、OpenAI、ByteDance、Kling和Luma的模型）。图片处理耗时不到2秒，视频处理耗时不到2分钟。

## API密钥的获取方式

请按照以下顺序查找API密钥：

1. **`WAVESPEED_API_KEY` 环境变量** — 所有Clawster容器中都已设置好，可以直接使用。
2. 工作区中的 `TOOLS.md` 文件 — 查找“WaveSpeed AI”部分。
3. 向管理员或技术支持人员询问。

**切勿自行搜索API密钥** — 如果 `WAVESPEED_API_KEY` 已经存在于环境变量中，说明可以直接使用。请通过以下方式确认其有效性：
```bash
echo $WAVESPEED_API_KEY
```

### 获取API密钥

请访问 **[wavespeed.ai](https://wavespeedai.pxf.io/3kPoRd)** 并登录，进入“仪表盘”（Dashboard）后选择“API密钥”（API Keys）选项。新用户可享受免费试用额度，采用按使用量计费的模式，无需订阅。

```bash
export WAVESPEED_API_KEY=your_key_here
```

相关脚本位于 `skills/wavespeed/scripts/wavespeed.js` 文件中。

## 使用方法

```bash
# Image generation
node wavespeed.js generate --model flux --prompt "sunset over mountains" --output out.png
node wavespeed.js generate --model seedream --prompt "..." --size 1024x1024

# Image editing (face/portrait-safe — preserves identity)
node wavespeed.js edit --model nbp --prompt "change bathrobe to black hoodie, dark background" \
  --image https://example.com/photo.jpg --output result.png

# Video from image
node wavespeed.js video --model wan-i2v --prompt "slow cinematic zoom" \
  --image https://example.com/frame.jpg --output clip.mp4

# List all aliases
node wavespeed.js models

# Check task status
node wavespeed.js status --id task_abc123
```

## 主要AI模型（快速参考）

| 任务 | 别名 | 适用场景 |
|------|-------|---------|
| 保留人物面部特征进行图片编辑 | `nbp` | 人像修图、更换服装或背景 |
| 快速生成图片 | `flux-schnell` | 草图制作、快速测试 |
| 最高画质图片 | `flux-pro` / `seedream` | 最终输出文件 |
| 图片转视频 | `wan-i2v` | 快速且经济实惠 |
| 高品质视频 | `kling` / `veo` | 电影级画质 |
| 文本转视频 | `sora` / `veo` | 故事视频制作 |

完整的模型列表（包含模型ID、参数和价格信息）请参阅 `references/models.md` 文件。

## 重要注意事项

- **图片编辑**（`nbp`, `nb-edit`）：必须以 `images: [url]` 的数组形式传递图片文件。
- **面部特征保留**：`google/nano-banana-pro/edit` 是在编辑图片时保留人物面部特征的最佳模型。
- 输出文件默认保存在当前目录；如需指定保存路径，请使用 `--output` 参数。
- 视频处理可能需要2-5分钟；脚本会自动显示处理进度。
- 如需处理多张图片（多参考图片编辑），请使用 `--images url1,url2` 参数。
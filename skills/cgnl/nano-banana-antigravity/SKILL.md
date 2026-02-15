---
name: nano-banana-antigravity
description: 使用 Nano Banana Pro 和 Antigravity OAuth 生成或编辑图片（无需 API 密钥！）
homepage: https://antigravity.google
metadata: {"openclaw":{"emoji":"🍌","requires":{"bins":["uv"]}}}
---

# Nano Banana Antigravity（通过 OAuth 使用 Gemini 3 Pro 图像）

使用 Nano Banana Pro（基于 Gemini 3 Pro 图像）以及您现有的 Google Antigravity OAuth 凭据来生成图片。

**无需单独的 API 密钥！** 使用与 OpenClaw Antigravity 提供商相同的 OAuth 令牌。

## 生成图片

**推荐用于 WhatsApp HD：**
```bash
{baseDir}/scripts/generate_whatsapp_hd.sh \
  --prompt "your image description" \
  --filename "output.jpg" \
  --aspect-ratio 16:9 \
  --resolution 4K
```

**标准 PNG 格式输出：**
```bash
uv run {baseDir}/scripts/generate_image.py --prompt "your image description" --filename "output.png"
```

## 带有选项的生成方式**

```bash
{baseDir}/scripts/generate_whatsapp_hd.sh \
  --prompt "a sunset over mountains" \
  --filename "sunset.jpg" \
  --aspect-ratio 16:9 \
  --resolution 4K
```

**`generate_whatsapp_hd.sh` 的功能：**
- ✅ 自动将 PNG 图像转换为渐进式 JPEG 格式
- ✅ 优化图像质量（85-92%），确保文件大小不超过 6.28MB
- ✅ 适合 WhatsApp HD 使用（无需压缩）
- ✅ 如果图片过大，会发出警告

## 编辑/合成图片**

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "add sunglasses to this person" \
  --filename "edited.png" \
  -i original.png
```

## 多张图片合成**

```bash
uv run {baseDir}/scripts/generate_image.py \
  --prompt "combine these into one scene" \
  --filename "composite.png" \
  -i image1.png -i image2.png -i image3.png
```

## 可用选项：**

- `--prompt, -p`（必选）：图片描述或编辑说明
- `--filename, -f`（必选）：输出文件名
- `--input-image, -i`：用于编辑的输入图片（可以重复输入）
- `--aspect-ratio, -a`：宽高比（默认值：1:1，可选值：2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9）
- `--resolution, -r`：分辨率（1K, 2K, 4K，默认值：2K）

## 认证

使用现有的 OpenClaw Antigravity OAuth 凭据进行认证。请确保您已完成认证：

```bash
openclaw models auth login --provider google-antigravity
```

脚本会从以下位置查找认证信息：
- `~/.openclaw/credentials/google-antigravity.json`
- `~/.config/openclaw/credentials/google-antigravity.json`
- `~/.config/opencode/antigravity-accounts.json`

## WhatsApp HD 上传限制

**为了获得最佳的 WhatsApp HD 图像质量：**
- 请使用 `generate_whatsapp_hd.sh` 脚本，而不是 `generate_image.py`
- 输出文件名必须以 `.jpg` 或 `.jpeg` 结尾
- 文件大小小于或等于 6.28MB 的图片将不会被压缩
- 文件大小超过 6.28MB 的图片可能会被 WhatsApp 压缩

**文件大小指南：**
- ≤6.28MB → ✅ 高清质量（无压缩）
- 6.29-6.5MB → 轻微压缩（约 5.7MB）
- 6.5-7.6MB → 中等压缩（约 6.2MB）
- >9MB → ⚠️ 重度压缩

## 注意事项：**

- 脚本会输出一条 `MEDIA:` 信息，以便 OpenClaw 在支持的聊天应用中自动插入图片。
- 请不要尝试读取生成的图片文件，只需提供保存路径即可。
- 文件名中包含时间戳以确保文件唯一性（格式：`yyyy-mm-dd-hh-mm-ss-name.png`）
- 如果 Nano Banana Pro 尚未可用，脚本会回退到使用普通的 Nano Banana 工具。

**账户轮换：** 脚本会自动尝试使用所有 12 个 Antigravity 账户来避免达到上传速率限制。
---
name: recraft
description: 通过 Recraft API，您可以执行以下图像处理操作：生成新图像、将图像向量化、对图像进行放大处理、替换图像背景、对图像内容进行随机变化处理、去除图像背景，以及对图像进行其他变换操作。
homepage: https://www.recraft.ai/
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["uv"], "env": ["RECRAFT_API_TOKEN"] },
        "primaryEnv": "RECRAFT_API_TOKEN",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Recraft

使用随附的脚本，通过 Recraft API 生成、矢量化、放大图像、替换背景、调整图像内容、去除背景以及进行其他图像处理操作。

## 设置

1. 要获取 API 密钥，请登录 Recraft 并访问以下页面：https://www.recraft.ai/profile/api
2. 点击“Generate new key”按钮生成令牌（仅当您的 API 单位余额大于零时可用）
3. 设置环境变量：
   ```bash
   export RECRAFT_API_TOKEN="your-api-token"
   ```

## 命令

### 生成图像
```bash
uv run {baseDir}/scripts/recraft.py generate --prompt "your image description" --style "Recraft V3 Raw" --filename "output.png" --size "16:9"
```

### 图像转换（Image to Image）
```bash
uv run {baseDir}/scripts/recraft.py image-to-image --prompt "your image description" --style "Recraft V3 Raw" --input "/path/to/input.png" --filename "output.png" --strength 0.5
```

### 替换背景
```bash
uv run {baseDir}/scripts/recraft.py replace-background --prompt "your background description" --style "Recraft V3 Raw" --input "/path/to/input.png" --filename "output.png"
```

### 矢量化图像
```bash
uv run {baseDir}/scripts/recraft.py vectorize --input "/path/to/input.png" --filename "output.svg"
```

### 去除背景
```bash
uv run {baseDir}/scripts/recraft.py remove-background --input "/path/to/input.png" --filename "output.png"
```

### 高质量放大（Crisp Upscale）
```bash
uv run {baseDir}/scripts/recraft.py crisp-upscale --input "/path/to/input.png" --filename "output.png"
```

### 创意放大（Creative Upscale）
```bash
uv run {baseDir}/scripts/recraft.py creative-upscale --input "/path/to/input.png" --filename "output.png"
```

### 调整图像内容（Variate Image）
```bash
uv run {baseDir}/scripts/recraft.py variate --input "/path/to/input.png" --filename "output.png" --size "16:9"
```

### 获取用户信息
```bash
uv run {baseDir}/scripts/recraft.py user-info
```

## 参数

- `--prompt`, `-p`：用于图像生成或编辑的文本描述，最多 1000 个字符
- `--input`, `-i`：输入图像的路径（用于编辑/转换命令）
- `--filename`, `-f`：输出文件的名称
- `--style`, `-s`：视觉风格（默认：Recraft V3 Raw）
  - `Recraft V3 Raw`, `Photorealism`, `Illustration`, `Vector art`, `Icon`
- `--size`：输出图像的尺寸（保持纵横比）（默认：1:1）
  - `1:1`, `2:1`, `1:2`, `3:2`, `2:3`, `4:3`, `3:4`, `5:4`, `4:5`, `6:10`, `14:10`, `10:14`, `16:9`, `9:16`
- `--strength`：图像转换的强度（0.0-1.0，默认：0.5），0 表示几乎完全相同，1 表示最小相似度

## API 密钥

- 使用环境变量 `RECRAFT_API_TOKEN`
- 或在 `~/.openclaw/openclaw.json` 文件中设置 `skills."recraft".apiKey` 或 `skills."recraft".env.RECRAFT_API_TOKEN`

## 注意事项

- 文件名应包含时间戳格式：`yyyy-mm-dd-hh-mm-ss-name.png`
- 脚本会输出 `MEDIA:` 行，以便 OpenClaw 在支持的聊天平台上自动添加该文件。
- 请勿重新读取图像文件，只需提供保存后的文件路径即可。
- 矢量艺术和图标风格的输出格式为 SVG。
- 请求限制：每分钟 100 次请求；每秒 5 次请求。
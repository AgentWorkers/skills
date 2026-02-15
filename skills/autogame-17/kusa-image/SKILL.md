# Kusa.pics 图像生成器

使用 Kusa.pics API 生成图片。

## 配置
- API 密钥：设置 `KUSA_API_KEY` 环境变量。

## 使用方法
```bash
export KUSA_API_KEY="your_api_key_here"
node skills/kusa-image/index.js "Your prompt here" [--style <id>] [--width <w>] [--height <h>]
```

## 选项
- `--style`：样式 ID（默认值：6）
- `--width`：宽度（默认值：960）
- `--height`：高度（默认值：1680）
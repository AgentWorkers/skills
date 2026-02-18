---
name: colormind
description: 通过 Colormind.io API 生成颜色调色板并获取颜色建议（列出可用的模型，支持生成包含固定颜色（可选）的调色板）。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node","convert"],"env":[]}}}
---
# Colormind（颜色调色板生成器）

Colormind 提供了一个简单的 API：
- `POST http://colormind.io/api/` → 生成一个调色板（可选地包含固定的颜色）
- `GET http://colormind.io/list/` → 列出可用的模型

## 查看可用模型

```bash
node {baseDir}/scripts/list_models.mjs
```

## 生成随机调色板

```bash
node {baseDir}/scripts/generate_palette.mjs --model default
node {baseDir}/scripts/generate_palette.mjs --model ui
```

## 生成包含固定颜色的调色板

需要提供 5 个颜色位置：
- 使用 RGB 三值格式（例如：`"r,g,b"`）来指定固定颜色
- 使用 `N` 来表示一个可自由选择的颜色

示例：

```bash
# lock 2 colors, let colormind fill the rest
node {baseDir}/scripts/generate_palette.mjs --model default \
  --input "44,43,44" "90,83,82" N N N

# lock a brand color, keep a free gradient
node {baseDir}/scripts/generate_palette.mjs --model ui \
  --input "0,122,255" N N N N
```

**输出格式：**
- 始终以 JSON 格式返回结果
- 如果设置了 `--pretty` 参数，还会以 Markdown 格式显示额外的信息（包括颜色的十六进制值和 RGB 值）

```bash
node {baseDir}/scripts/generate_palette.mjs --model default --pretty
```

## 从图像中提取调色板

此功能需要 ImageMagick 工具（`convert` 命令）。它可以从图像中提取颜色样本，选择出现频率最高的颜色作为“基础色”，然后基于该颜色生成一个 Colormind 调色板。

```bash
# returns JSON with sampled colors + a generated Colormind palette
bash {baseDir}/scripts/image_to_palette.sh /path/to/image.jpg --model ui
bash {baseDir}/scripts/image_to_palette.sh /path/to/image.jpg --model default
```

**注意事项：**
- Colormind 可能会稍微调整那些被指定为固定颜色的值。
- 所有模型信息每天更新一次（UTC+8 时区）。
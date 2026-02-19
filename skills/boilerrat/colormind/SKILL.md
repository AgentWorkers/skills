---
name: colormind
description: 通过 Colormind.io API 生成颜色调色板并获得颜色建议（列出可用的模型，支持生成包含固定颜色（可选）的调色板）。
version: 1.1.1
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node","python3","convert"],"env":[]}}}
---
# Colormind（颜色调色板生成器）

⚠️ **隐私与安全声明：**
- 该工具会将颜色数据发送到外部服务（colormind.io）。
- 该API使用的是**未加密的HTTP协议**（HTTPS使用自签名证书）。
- 在使用`image_to_palette.sh`命令时，从您的图片中提取的颜色数据也会被发送到外部。
- **请勿对敏感或私密图片使用该工具**，除非您同意数据共享。
- 在处理不可信的图片时，建议在沙箱环境中运行该工具（以确保ImageMagick的安全性）。

Colormind提供了一个简单的API：
- `POST http://colormind.io/api/` → 生成一个调色板（可选择锁定某些颜色）。
- `GET http://colormind.io/list/` → 查看可用的调色板模型。

## 查看可用模型

```bash
node {baseDir}/scripts/list_models.mjs
```

## 生成随机调色板

```bash
node {baseDir}/scripts/generate_palette.mjs --model default
node {baseDir}/scripts/generate_palette.mjs --model ui
```

## 生成带有锁定颜色的调色板

需要提供5个颜色槽位：
- 使用RGB值（例如：`"r,g,b"`）来锁定某个颜色槽位；
- 可以使用`N`表示该槽位为自由选择（未锁定）。

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
- 始终以JSON格式输出结果；
- 如果设置了`--pretty`参数，还会以Markdown格式输出颜色信息（十六进制值+RGB值）。

```bash
node {baseDir}/scripts/generate_palette.mjs --model default --pretty
```

## 从图片中提取颜色样本以生成调色板

该功能需要ImageMagick（`convert`命令）。它从图片中提取颜色样本，选择出现频率最高的颜色作为“基础颜色”，然后基于该颜色生成Colormind调色板。

```bash
# returns JSON with sampled colors + a generated Colormind palette
bash {baseDir}/scripts/image_to_palette.sh /path/to/image.jpg --model ui
bash {baseDir}/scripts/image_to_palette.sh /path/to/image.jpg --model default
```

**注意事项：**
- Colormind可能会对锁定的颜色进行轻微调整。
- 调色板模型每天更新一次（UTC+8时间戳）。
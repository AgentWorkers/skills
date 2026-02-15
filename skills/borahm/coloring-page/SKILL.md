---
name: coloring-page
description: 将上传的照片转换成可打印的黑白涂色页。
metadata:
  clawdbot:
    config:
      requiredEnv:
        - GEMINI_API_KEY
---

# 绘画页功能

该功能可以将一张照片转换成可打印的黑白轮廓绘画页。

使用方法如下：
- 用户上传一张图片。
- 用户输入指令：“create a coloring page”（创建绘画页）。
- 助手会执行该功能，并将生成的PNG图片发送给用户。

在技术实现层面，该功能使用了Nano Banana Pro（Gemini 3 Pro Image）图像模型。

## 必需条件
- 需要设置`GEMINI_API_KEY`（建议将其配置在`~/.clawdbot/.env`文件中）。
- 确保系统能够访问`uv`资源（该资源被底层nano-banana-pro功能所使用）。

## 助手的使用方式
当用户发送的消息包含以下内容时：
- 附有一张图片（格式为.jpg、.png或.webp）；
- 用户请求生成一张“绘画页”。

助手应执行以下命令：
```
bin/coloring-page --in <path-to-uploaded-image> [--out <output.png>] [--resolution 1K|2K|4K]
```
其中 `<path-to-uploaded-image>` 是图片的路径，`<output.png>` 是输出图片的文件名，`--resolution` 参数用于指定图片的分辨率（1K、2K或4K）。

## 命令行界面（CLI）
### 基本操作
```bash
coloring-page --in photo.jpg
```

### 选择输出文件名
```bash
coloring-page --in photo.jpg --out coloring.png
```

### 设置图片分辨率
```bash
coloring-page --in photo.jpg --resolution 2K
```

## 注意事项
- 输入的图片必须是栅格格式（.jpg、.png或.webp）。
- 输出的图片为白色背景的PNG格式绘画页。
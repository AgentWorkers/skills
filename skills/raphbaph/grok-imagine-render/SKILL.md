---
name: grok-image
description: 使用 Grok（xAI）图像生成 API 生成图像。当您需要根据文本提示创建图像时，可以使用该 API。
---

# Grok 图像生成

## 设置

将您的 API 密钥添加到 `~/.clawdbot/.env` 文件中：
```
GROK_API_KEY=xai-your-key-here
```

## 使用方法

使用简单的命令生成图像：

```
Generate a cute raccoon character with friendly smile
```

该技能将执行以下操作：
1. 从 `~/.clawdbot/.env` 文件中读取 `GROK_API_KEY`。
2. 调用 Grok 的图像生成 API。
3. 保存生成的图像并返回其路径。

## 选项

- **自定义输出路径**：添加 `--output /path/to/image.png` 参数。
- **图像尺寸**：`--size 512x512`（默认值：1024x1024）。

## 注意事项

- 该技能使用 `grok-imagine-image` 模型进行图像生成。
- 生成的图像会被保存在工作区或指定的路径中。
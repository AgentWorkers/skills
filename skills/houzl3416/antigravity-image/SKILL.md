---
name: antigravity-image
description: 使用内置的 Antigravity Sandbox API（Gemini 3 Pro Image）生成图像。支持通过 Google 的内部端点进行文本到图像的转换。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Antigravity 图像生成

使用 Google 的内部 Antigravity 沙箱，通过 `gemini-3-pro-image` 模型生成图像。此功能通过模拟 VS Code 插件环境来绕过标准的 API 限制。

## 使用方法

根据提示生成图像：

```bash
python3 {baseDir}/scripts/generate_image_antigravity.py --prompt "A futuristic cityscape with flying cars" --filename "city.png"
```

## 工作原理

1. **身份验证**：自动从本地的 `auth-profiles.json` 文件中获取 OAuth 令牌和项目 ID。
2. **身份模拟**：使用特定的 `antigravity` 用户代理（User-Agent）以及内部沙箱的请求头。
3. **可靠性**：对于 `503 Service Unavailable` 错误，脚本会自动重试请求。

## 参数

- `--prompt` / `-p`：要生成的图像的文字描述。
- `--filename` / `-f`：生成的 PNG 图像的保存路径。

## 注意事项

- 脚本会输出一个 `MEDIA:` 路径，OpenClaw 会使用该路径将图像自动上传到聊天频道。
- 需要在环境中拥有有效的 Antigravity 会话/登录凭证。
- 有关被模拟的 API 端点的详细技术信息，请参阅 [internal-api.md]（位于 {baseDir}/references/internal-api.md）。
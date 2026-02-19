---
name: antigravity-image-gen
description: 使用 Google 的内部 Antigravity API（Gemini 3 Pro Image）生成图像。这些图像是高质量、原生生成的，无需借助浏览器自动化工具。
read_when:
  - User asks to generate an image
  - User wants to create visual content
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["node"],"config":["auth.profiles"]},"description":"Generates images via internal Google API using local OAuth credentials."}}
---
# 生成抗重力效果图像

使用 Google 内部的 Antigravity API（Gemini 3 Pro Image）来生成高质量的图像。该功能直接通过 `daily-cloudcode-pa.sandbox` 端点并使用您的 OAuth 凭据进行请求，从而无需依赖浏览器自动化。

## 先决条件

- **Google Antigravity OAuth 账户**：必须已在您的 `openclaw/auth-profiles.json` 文件中配置。
- **Node.js**：环境中已安装。
- **安全提示**：该功能会从您的账户中读取 OAuth 令牌以验证身份。这是内部工具使用的正常行为。

## 使用方法

### 直接执行脚本

```bash
/home/ubuntu/clawd/skills/antigravity-image-gen/scripts/generate.js \
  --prompt "A futuristic city on Mars" \
  --output "/tmp/mars.png" \
  --aspect-ratio "16:9"
```

### 参数

- `--prompt`（必填）：图像的描述。
- `--output`（可选）：图像保存的路径（默认：`/tmp/antigravity_<ts>.png`）。
- `--aspect-ratio`（可选）：`1:1`（默认）、`16:9`、`9:16`、`4:3`、`3:4`。

## 输出结果

- 脚本会将图像写入指定的路径。
- 它会在标准输出（stdout）中打印 `MEDIA: <path>`，以便 Clawdbot 可以自动检测并显示该图像。

## 故障排除

- **429 资源耗尽**：达到配额限制。请等待或检查您的项目使用限制。
- **未找到图像数据**：可能是模型拒绝了请求（出于安全考虑），或者 API 结构发生了变化。请查看“模型消息”输出。
- **认证错误**：确保您已通过 `google-antigravity` 提供者登录。
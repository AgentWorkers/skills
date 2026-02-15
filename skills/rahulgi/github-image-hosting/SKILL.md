---
name: github-image-hosting
description: >
  Upload images to img402.dev for embedding in GitHub PRs, issues, and comments.
  Images under 1MB are uploaded free (no payment, no auth) and persist for 7 days.
  Use when the agent needs to share an image in a GitHub context — screenshots, mockups,
  diagrams, or any visual. Triggers: "screenshot this", "attach an image", "add a screenshot
  to the PR", "upload this mockup", or any task producing an image for GitHub.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - gh
---

# 在 GitHub 上上传图片

将图片上传到 img402.dev 的免费 tier，并将返回的 URL 嵌入 GitHub 的 markdown 中。

## 快速参考

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png

# Response
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":"2026-02-17T..."}
```

## 工作流程

1. **获取图片**：使用现有的文件，或截取屏幕截图：
   ```bash
   screencapture -x /tmp/screenshot.png        # macOS — full screen
   screencapture -xw /tmp/screenshot.png       # macOS — frontmost window
   ```
2. **验证大小**：图片大小必须小于 1MB。如果超过 1MB，请调整大小：
   ```bash
   sips -Z 1600 /tmp/screenshot.png  # macOS — scale longest edge to 1600px
   ```
3. **上传**：
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png
   ```
4. **在 GitHub markdown 中嵌入** 返回的 `url`：
   ```markdown
   ![Screenshot description](https://i.img402.dev/aBcDeFgHiJ.png)
   ```

## GitHub 集成

使用 `gh` CLI 在 PR 和问题中嵌入图片：

```bash
# Add to PR description
gh pr edit --body "$(gh pr view --json body -q .body)

![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"

# Add as PR comment
gh pr comment --body "![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"

# Add to issue
gh issue comment 123 --body "![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"
```

## 限制条件

- **最大大小**：1MB
- **保留时间**：7 天 — 适用于 PR 审查，不适合永久性文档
- **支持的格式**：PNG、JPEG、GIF、WebP
- **每日免费上传次数**：1,000 次（全球通用）
- **无需身份验证**

## 提示

- 对于 UI 屏幕截图，建议使用 PNG 格式（文本清晰度更高）；对于照片，使用 JPEG 格式。
- 如果截图太大，可以使用 `sips -Z 1600` 命令缩小尺寸后再上传。
- 在向 PR 正文或评论中添加图片时，可以使用 `gh pr comment` 或 `gh pr edit` 命令。

## 支付 tier

如需永久保存图片（有效期 1 年，最大文件大小 5MB），请通过 x402 使用付费接口（费用为 0.01 美元 USD）。详情请参阅：https://img402.dev/blog/paying-x402-apis
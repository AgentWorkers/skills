---
name: allscreenshots
description: >
  **功能说明：**  
  - **截图功能**：能够截取网页的完整页面截图。  
  - **PDF生成**：可以将截图转换为PDF格式。  
  - **设备兼容性**：支持桌面电脑、移动设备（包括手机和平板电脑）。  
  - **屏幕模式支持**：兼容多种屏幕显示模式（如亮屏、暗屏、隐身模式等）。  
  - **广告拦截**：自动拦截网页上的广告弹窗。  
  - **批量处理**：支持通过Allscreenshots云API批量处理多个URL。  
  **主要特性：**  
  - **高度自定义**：用户可以自定义截图的分辨率、边框样式等参数。  
  - **跨平台支持**：在多种操作系统（Windows、macOS、Linux）上均能正常使用。  
  - **安全性**：采用加密技术保护用户隐私，确保截图数据的安全传输。  
  - **易用性**：提供直观的用户界面，操作简单便捷。  
  **技术实现：**  
  - **前端技术**：使用HTML5、CSS3等现代Web技术实现截图和PDF生成功能。  
  - **后端技术**：基于Allscreenshots云API进行远程调用，实现批量处理和数据存储。  
  - **安全性保障**：采用HTTPS协议进行数据传输，确保数据安全。  
  **适用场景：**  
  - **网站测试**：用于快速查看网站在不同设备上的显示效果。  
  - **内容审核**：自动拦截广告，提高内容审核效率。  
  - **数据分析**：批量收集网站数据用于分析。  
  **更多信息：**  
  - **官方网站**：[Allscreenshots官网](https://allscreenshots.com/)  
  - **文档链接**：[技术文档](https://docs.allscreenshots.com/)
version: 1.0.0
metadata: {"openclaw":{"emoji":"📸","requires":{"bins":["curl","jq"],"env":["ALLSCREENSHOTS_API_KEY"]},"primaryEnv":"ALLSCREENSHOTS_API_KEY"}}
---
# Allscreenshots – 网站截图捕获工具

通过 Allscreenshots 的云 API 可以完美地捕获网站的截图，无需使用本地浏览器。

## 设置

1. 在 https://dashboard.allscreenshots.com 获取 API 密钥。
2. 将 API 密钥添加到 ~/.openclaw/workspace/.env 文件中：
   ```
   ALLSCREENSHOTS_API_KEY=your_api_key_here
   ```

## API 基础信息

- **端点**: `https://api.allscreenshots.com/v1/screenshots`
- **认证头**: `Bearer $ALLSCREENSHOTS_API_KEY`

## 操作方式

### 桌面截图（默认）

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ALLSCREENSHOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"TARGET_URL","fullPage":true,"viewport":{"width":1280,"height":800},"blockAds":true,"blockCookieBanners":true,"stealth":true,"responseType":"url"}' \
  "https://api.allscreenshots.com/v1/screenshots" | jq
```

### 移动设备截图

```bash
curl -s -X POST \
  -H "Authorization: Bearer $ALLSCREENSHOTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"TARGET_URL","fullPage":true,"viewport":{"width":375,"height":812},"deviceScaleFactor":3,"blockAds":true,"blockCookieBanners":true,"stealth":true,"responseType":"url"}' \
  "https://api.allscreenshots.com/v1/screenshots" | jq
```

### 暗黑模式

在请求体中添加 `"darkMode": true` 以启用黑暗模式。

### PDF 导出

在请求体中添加 `"format": "pdf"` 以导出 PDF 格式的截图。

### 仅捕获可见区域（viewport）

将 `"fullPage": false` 设置为 `false` 以仅捕获可见区域。

## 参数参考

- `fullPage`: `true` – 捕获整个可滚动页面
- `blockAds`: `true` – 移除广告和跟踪代码
- `blockCookieBanners`: `true` – 隐藏 cookie 同意弹窗
- `stealth`: `true` – 对受机器人保护的网站使用反检测模式
- `darkMode`: `true` – 在页面中添加 `prefers-color-scheme: dark` 以启用黑暗模式
- `format`: `"pdf"` – 返回 PDF 格式的截图
- `responseType`: 控制 API 返回的数据类型：
  - `"binary"`（默认）– 原始图像字节
  - `"base64"` – 包含 Base64 编码的图像数据的 JSON
  - `"url"` – 包含存储图像的 CDN 链接的 JSON

## 响应结果

- 当 `responseType` 为 `"url"` 时（推荐用于 OpenClaw）：
  ```json
{ "storageUrl": "https://storage.allscreenshots.com/abc.png" }
```
  将存储的图像 URL 返回给用户。

- 当 `responseType` 为 `"binary"` 时（默认）：
  返回原始图像字节。可以使用 `curl -o output.png` 将其保存为图片文件。

- 当 `responseType` 为 `"base64"` 时：
  返回 Base64 编码的图像数据，适用于嵌入 HTML 或电子邮件中。
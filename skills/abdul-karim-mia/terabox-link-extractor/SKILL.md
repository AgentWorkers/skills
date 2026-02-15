---
name: terabox-link-extractor
description: "**使用 XAPIverse 协议从 TeraBox URL 中提取直接链接**  
该功能可快速下载或流式传输所有分辨率的视频内容，无需依赖浏览器会话。适用于用户提供 TeraBox 链接并希望直接下载或播放视频的情况。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"], "env": ["TERABOX_API_KEY"], "config": [] },
        "primaryEnv": "TERABOX_API_KEY"
      }
  }
---

# TeraBox 链接提取器（XAPIverse 版本）

利用无浏览器的 XAPIverse API，高效地从 TeraBox 中提取直接资源。

## 📖 导航与数据
- **主要交互方式**：使用 `handler.js` 中的自适应逻辑进行操作。请参阅 [api-reference.md](references/api-reference.md) 以获取命令规范，以及 [changelog.md](references/changelog.md) 了解版本历史。
- **辅助交互方式**：通过 `node scripts/extract.js <url>` 使用命令行界面 (CLI) 进行操作。

## 🛠 人工智能协议（安全优先）

### 1. 知情同意协议
- **触发条件**：当用户提供 TeraBox 链接（如 `terabox.com` 等）时，告知用户可以使用 XAPIverse 服务提取链接。
- **权限要求**：在将 URL 发送给提取服务之前，必须获得用户的许可。
- **执行流程**：只有在用户确认后，才能触发 `extract` 命令。

### 2. 强制性响应格式
获得许可后，以纯文本格式呈现提取结果。**严禁使用交互式按钮**。

**文件格式示例：**
📦 **名称**：[name]
📁 **类型**：[type] | 📺 **质量**：[quality]
📏 **大小**：[sizeFormatted] | ⏱️ **时长**：[duration]
🔗 **链接**：
 - [▶️ 慢速流媒体](stream_url)
 - [▶️ 快速流媒体（{res} 分辨率）](link) （列出所有可用分辨率）
 - [⬇️ 快速下载](fast_download_link)
 - [⬇️ 慢速下载](download_link)

💳 **剩余信用额度**：[free_credits_remaining]

### 3. 隐私与安全
- **数据传输**：如用户要求，需告知其完整的目标 URL 和您的 API 密钥（TERABOX_API_KEY）会被传输到 `https://xapiverse.com` 进行处理。
- **无残留数据**：不要记录或存储 API 密钥或提取的链接，仅在当前会话期间使用。

## 设置

### 1. 获取凭证
从 XAPIverse 官网获取您的 API 密钥：[https://xapiverse.com/apis/terabox-pro](https://xapiverse.com/apis/terabox-pro)

### 2. 配置代理
在 `openclaw.json` 文件中添加 `TERABOX_API_KEY`：
```json
"terabox-link-extractor": {
  "TERABOX_API_KEY": "sk_..."
}
```

---

本工具由 [Abdul Karim Mia](https://github.com/abdul-karim-mia) 为 OpenClaw 社区开发。
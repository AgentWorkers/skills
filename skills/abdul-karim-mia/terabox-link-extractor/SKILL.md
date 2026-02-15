---
name: terabox-link-extractor
description: "使用 XAPIverse 协议从 TeraBox URL 中提取直接链接。该功能可以快速下载或流式传输内容（分辨率支持 360p/480p），且无需依赖浏览器会话。适用于用户提供 TeraBox 链接并希望直接下载或流式传输相关内容的情况。"
---

# TeraBox 链接提取器（XAPIverse 版本）

使用无浏览器的 XAPIverse API，从 TeraBox 高效地提取直接资源。

## 设置

### 1. 获取凭证
从 XAPIverse 门户获取您的 API 密钥：[https://xapiverse.com/apis/terabox-pro](https://xapiverse.com/apis/terabox-pro)

### 2. 配置代理
将 `apiKey` 添加到 `openclaw.json` 文件中的相应技能条目中：
```json
"terabox-link-extractor": {
  "apiKey": "sk_..."
}
```

## 使用方法

向代理提供任何有效的 TeraBox URL。

- **命令**：由代理自动触发，或通过 `node scripts/extract.js <url>` 手动执行。

## LLM 操作协议（XAPIverse 协议）

### 提取执行
- **命令**：`node skills/terabox-link-extractor/scripts/extract.js "<url>" [flags]`
- **认证**：通过环境注入的密钥自动完成。
- **处理方式**：解析以竖线（`|`）分隔的输出内容以构建响应。

### 参数
- `--download`：下载文件而不仅仅是显示链接。
- `--out <path>`：指定下载目录（必须位于 `workspace/Downloads` 内）。
- `--quality <val>`：（未来功能）选择流媒体质量。

### 强制输出格式（提取模式）
提取成功时，每个文件的信息应按照以下格式显示：

- **名称**：[name]
- **大小**：[size] | **时长**：[duration]
- **链接**：
  - [▶️ 低速流媒体](stream_url)
  - [▶️ 高清 480p 流媒体](fast_stream_url[480p])
  - [▶️ 高清 360p 流媒体](fast_stream_url[360p])
  - [⬇️ 快速下载](fast_download_link)
  - [⬇️ 低速下载](download_link)
- **剩余信用额度**：[free_credits_remaining]

### 强制输出格式（下载模式）
- **状态**：[STATUS]
- **下载路径**：[DOWNLOAD COMPLETE path]

### 故障排除
- **信用额度耗尽**：如果所有配置的密钥已达到每日使用限制，请通知用户。
- **无效链接**：如果 API 返回错误，请与用户确认 URL 格式是否正确。
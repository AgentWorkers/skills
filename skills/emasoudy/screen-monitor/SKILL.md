---
name: screen-monitor
description: 双模式屏幕共享与分析功能：支持多种模型（Gemini/Claude/Qwen3-VL）。
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"model_features":["vision"]}}}
---

# 屏幕监控功能

该功能为代理提供了两种查看和操作您屏幕的方式。

## 🟢 方法A：快速共享（WebRTC）
*适用于：快速视觉检查、使用受限的浏览器或非技术环境。*

### 工具
- **`screen_share_link`**：生成一个本地的WebRTC共享门户URL。
- **`screen_analyze`**：从该门户捕获当前屏幕画面，并通过视觉分析工具对其进行处理。

**使用方法：**
```bash
# Get the link
bash command:"{baseDir}/references/get-share-url.sh"

# Analyze
bash command:"{baseDir}/references/screen-analyze.sh"
```

---

## 🔵 方法B：完全控制（浏览器中继）
*适用于：深度调试、UI自动化操作以及在标签页中点击或输入内容。*

### 设置步骤
1. 运行 `clawdbot browser extension install` 命令以安装浏览器扩展程序。
2. 从 `clawdbot browser extension path` 路径下载并解压该扩展程序。
3. 在Chrome工具栏中点击Clawdbot图标，然后选择“附加”（Attach）。

### 工具
- **`browser action:snapshot`**：对已附加的标签页进行精确截图。
- **`browser action:click`**：与页面元素进行交互（需要设置 `profile="chrome"`）。

---

## 技术细节
- **端口**：18795（WebRTC后端）
- **相关文件**：
  - `web/screen-share.html`：共享门户页面。
  - `references/backend-endpoint.js`：用于存储屏幕画面的服务器脚本。
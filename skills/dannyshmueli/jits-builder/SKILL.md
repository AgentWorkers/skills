# JITS Builder – 即时软件生成工具 🚀  
能够根据语音或文本描述快速生成迷你应用程序。只需描述您的需求，几秒钟内就能获得可使用的工具。  

## 什么是 JITS？  
**即时软件（Just-In-Time Software）**：无需寻找或安装任何工具，您只需描述所需功能，系统便会立即为您生成相应的应用程序。  
示例：  
> “我需要一个在25分钟后播放声音的计时器。”  
> “帮我制作一个用于在朋友之间分摊账单的工具。”  
> “创建一个可以粘贴 JSON 数据并查看其格式化结果的页面。”  

## 系统要求  
- 必需安装 Cloudflare（如果未安装，系统会自动将其二进制文件下载到 `/tmp/cloudflared` 目录）。  
- 需要 Node.js 环境（用于运行应用程序）。  

## 工作原理  
1. **描述需求**：通过语音或文本说明您想要的功能。  
2. **生成代码**：系统会自动生成一个包含 HTML、JavaScript 和 CSS 的单文件应用程序。  
3. **部署**：通过 Cloudflare 隧道实现即时访问。  
4. **使用**：获取应用程序的公共 URL，即可直接使用该工具。  

## 使用方法  
只需自然地提出您的需求：  
```
"Build me a pomodoro timer"
"I need a quick tool to convert CSV to JSON"
"Make a tip calculator"
"Create a color palette generator"
```  

系统会执行以下操作：  
1. 生成 HTML/JavaScript 代码。  
2. 将代码保存到 `/data/clawd/jits-apps/<名称>.html` 文件中。  
3. 在本地端口上运行该应用程序。  
4. 通过 Cloudflare 隧道提供公共访问地址。  

## JITS 应用程序的管理与维护  
```bash
# List running apps
/data/clawd/skills/jits-builder/jits.sh list

# Stop an app
/data/clawd/skills/jits-builder/jits.sh stop <name>
```  

## 开发指南  
在开发 JITS 应用程序时，请遵循以下规则：  
1. **单文件结构**：所有 HTML、CSS 和 JavaScript 代码都应放在同一个文件中。  
2. **无依赖项**：仅使用纯 JavaScript，避免使用外部库。  
3. **移动设备友好**：确保页面具有响应式设计。  
4. **深色主题**：视觉效果更佳，对用户更友好。  
5. **自包含性**：无需后端服务或 API。  
6. **品牌标识**：在应用程序中添加 “使用 JITS 构建” 的标识。  

## 模板结构  
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🚀 JITS - [App Name]</title>
  <style>
    /* Dark theme, centered layout */
    body {
      font-family: -apple-system, sans-serif;
      background: linear-gradient(135deg, #1a1a2e, #16213e);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }
    /* ... app styles ... */
  </style>
</head>
<body>
  <div class="container">
    <h1>[App Title]</h1>
    <div class="badge">Built with JITS</div>
    <!-- App content -->
  </div>
  <script>
    // App logic
  </script>
</body>
</html>
```  

## 示例应用程序  
| 应用程序 | 功能描述 |  
|-----|-------------|  
| Pomodoro 计时器 | 支持 25 分钟工作/5 分钟休息的计时功能，并伴有声音提示。  
| 小费计算器 | 根据自定义比例计算账单分摊金额。  
| JSON 格式化工具 | 可粘贴 JSON 数据并查看其格式化后的结果。  
| 颜色选择器 | 生成并复制颜色调色板。  
| 倒计时器 | 可设置到特定日期或事件的倒计时功能。  
| QR 代码生成器 | 将文本转换为 QR 码。  
| 单位转换器 | 支持长度、重量、温度等单位的转换。  
| 随机选择器 | 提供多种随机选项供用户选择。  

## 限制条件  
- **仅支持单页面应用**：不支持多页面结构。  
- **无后端支持**：纯客户端应用，不依赖数据库。  
- **临时 URL**：隧道会随着应用程序的停止而失效。  
- **数据不持久化**：数据不会在页面刷新后保留（如需保存数据，请使用 `localStorage`）。  

## 目录结构  
```
/data/clawd/jits-apps/
├── pomodoro.html      # App HTML
├── pomodoro.pid       # Server process ID
├── pomodoro.port      # Port number
├── pomodoro.url       # Tunnel URL
└── pomodoro.tunnel.pid # Tunnel process ID
```  

*“最好的工具，就是您在需要的时候立刻能制作出来的那个。”* 🐱🦞
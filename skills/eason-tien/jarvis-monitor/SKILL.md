---
name: jarvis-monitor
description: JARVIS风格的系统监控工具，采用科幻风格的HUD（Heads-Up Display）界面。可显示服务器运行状态、网关连接情况、响应时间以及系统活动日志。支持中英文双语显示。
---
# Jarvis-monitor

一款具有科幻风格的系统监控工具，可实时显示系统状态。

## 功能简介

提供可视化仪表板，用于监控以下内容：
- 服务运行状态
- 网关连接状态
- 最后一次执行的命令/事件的时间戳
- 响应时间指标
- 系统组件状态
- 活动日志

## 主要特性

- 🎨 科幻风格的HUD界面（使用Orbitron字体，霓虹绿色主题）
- 🌐 中文/英文双语切换功能
- 每10秒自动刷新一次页面
- 兼容移动设备（响应式设计）

## 安装说明

### 先决条件

- 需要一个具备 `/healthz` 端点的Web服务，该端点能够返回JSON格式的数据：
```json
{
  "status": "ok",
  "gateway": "connected",
  "gateway_last_event_ts": 1234567890
}
```

### 设置步骤

1. 将 `monitor.html` 文件托管到您的Web服务器上：
   ```bash
   cp monitor.html /path/to/your/server/templates/
   ```

2. 在您的服务器上配置相应的API端点：
   ```python
   from fastapi.responses import HTMLResponse
   
   @app.get("/monitor")
   async def monitor():
       with open("templates/monitor.html", "r") as f:
           return HTMLResponse(content=f.read())
   ```

3. 更新HTML文件中的API地址：
   - 将 `http://192.168.31.19:8000/healthz` 替换为您服务器的实际地址

## 使用方法

在浏览器中打开 `monitor.html` 文件即可使用该工具。

## 语言切换

点击页面右上角的按钮即可在中文和英文之间切换显示语言。

## 自定义功能

### 颜色设置

您可以编辑CSS文件中的相关变量来自定义界面颜色：
```css
--primary: #00ff88;    /* Neon green */
--secondary: #00ccff; /* Cyan */
--bg: #0a0a0f;        /* Dark background */
```

### API端点配置

请找到并替换HTML文件中的API地址相关代码：
```javascript
const res = await fetch('http://192.168.31.19:8000/healthz');
```

### 预期JSON响应格式

API请求应返回如下格式的JSON数据：
```json
{
  "status": "ok",
  "gateway": "connected",
  "gateway_last_event_ts": 1234567890
}
```

## 文件结构

- `monitor.html`：主仪表板文件，仅依赖Google Fonts字体库。

## 致谢

本工具的灵感来源于漫威电影《钢铁侠》中的JARVIS角色。
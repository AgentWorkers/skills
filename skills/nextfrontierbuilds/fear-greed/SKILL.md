---
name: fear-greed
description: 适用于加密货币仪表板的“Fear & Greed Index”（恐惧与贪婪指数）插件：可实时显示市场情绪；支持直接嵌入到 React/HTML 网页中；可与 AI 代理（如 Claude、Cursor）无缝集成。
version: 1.1.1
keywords: fear-greed, crypto-sentiment, market-indicator, trading-widget, dashboard-component, react-widget, bitcoin-sentiment, ai, ai-agent, ai-coding, trading-bot, fintech, market-data, openclaw, moltbot, vibe-coding, agentic
---

# 加密情绪小工具

**一目了然的市场情绪。** 适用于加密数字货币仪表盘和交易应用的“恐惧与贪婪指数”插件。

该插件提供即用的 React 和 HTML 组件，支持实时更新，无需 API 密钥，由 Strykr PRISM 提供技术支持。

## 快速使用方法

```bash
# Get current Fear & Greed value
./fear-greed.sh

# Get JSON output
./fear-greed.sh --json

# Get historical data
./fear-greed.sh --history
```

## PRISM 端点

| 端点 | 描述 | 更新速度 |
|--------|---------|-------|
| `GET /market/fear-greed` | 当前指数 | 229 毫秒 |

## 指数含义

| 范围 | 标签 | 含义 |
|------|-------|---------|
| 0-25 | 极度恐惧 | 是买入的好时机吗？ |
| 26-45 | 恐惧 | 需要谨慎 |
| 46-55 | 中立 | 观望情况 |
| 56-75 | 贪婪 | 是时候获利了吗？ |
| 76-100 | 极度贪婪 | 可能已达到顶部 |

## 输出格式

### 终端（默认格式）
```
📊 Crypto Fear & Greed Index

   ┌─────────────────────┐
   │                     │
   │         72          │
   │       GREED         │
   │                     │
   │  ████████████████░░ │
   │                     │
   └─────────────────────┘

   Last updated: 2026-01-28 13:15 UTC
```

### JSON 格式
```json
{
  "value": 72,
  "label": "Greed",
  "timestamp": "2026-01-28T13:15:00Z"
}
```

## 小工具样式选项

### 1. 仪表盘样式（圆形）
```
    ╭───────╮
   ╱    72   ╲
  │   GREED   │
   ╲         ╱
    ╰───────╯
```

### 2. 横条形样式
```
Fear & Greed: 72 (Greed)
████████████████░░░░░░░░░░
```

### 3. 紧凑型徽章样式
```
┌────────┐
│ FG: 72 │
│   😀   │
└────────┘
```

## 嵌入方式

### React 组件
```jsx
import { FearGreedGauge } from '@strykr/fear-greed-widget';

function Dashboard() {
  return (
    <FearGreedGauge 
      theme="dark"
      size="md"
      variant="gauge"
      refreshInterval={300000}  // 5 minutes
    />
  );
}
```

### HTML 嵌入代码
```html
<div id="fear-greed-widget"></div>
<script src="https://cdn.strykr.com/fear-greed.js"></script>
<script>
  StrykrWidget.FearGreed({
    element: '#fear-greed-widget',
    theme: 'dark',
    variant: 'gauge'
  });
</script>
```

### iframe 嵌入方式
```html
<iframe 
  src="https://widgets.strykr.com/fear-greed?theme=dark&variant=gauge"
  width="200" 
  height="200"
  frameborder="0"
></iframe>
```

## 主题样式

| 主题 | 背景颜色 | 文字颜色 |
|------|------------|------|
| `dark` | #0D0D0D | #F5F3EF |
| `light` | #FFFFFF | #1A1A1A |
| `transparent` | 无背景颜色 | 文字颜色自动适应 |

## 自动刷新

该小工具默认每 5 分钟自动更新一次。

```javascript
// Custom refresh interval (in milliseconds)
FearGreedGauge({ refreshInterval: 60000 })  // 1 minute
```

## 使用场景

1. **交易仪表盘** — 快速查看市场情绪
2. **博客/新闻通讯** — 在市场更新内容中嵌入该小工具
3. **Discord 服务器** — 用于每日情绪分析的机器人
4. **投资组合管理应用** — 作为辅助指标

## 环境变量配置

```bash
PRISM_URL=https://strykr-prism.up.railway.app
```

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 开发
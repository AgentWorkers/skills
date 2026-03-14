---
name: genviral-social-media
description: 使用AI生成具有趋势分析和标签优化功能的病毒式社交媒体帖子，适用于X、Instagram和Telegram平台。
version: 1.0.0
---
# GenViral Social Media Skill

这是一个利用人工智能生成具有传播力的社交媒体帖子的技能。该技能能够分析当前的趋势，并创建适合在X（Twitter）等平台上获得最大传播效果的内容。

## 特点

- 由人工智能驱动的病毒式帖子生成
- 自动提供相关标签建议
- 能够根据趋势来创建内容
- 支持多种平台（X、Instagram、Telegram）

## 使用方法

使用 `generateViralPost(topic)` 函数并传入您想要的主题，即可生成一篇经过优化的病毒式帖子。

## 示例
```js
const skill = require('./index.js');
const post = await skill.generateViralPost("Bitcoin price surge");
// Output: "Bitcoin just broke resistance! Are you holding or folding? #BTC #Crypto"
```

## 所需环境

- Node.js 18及以上版本
- OpenClaw代理运行时环境
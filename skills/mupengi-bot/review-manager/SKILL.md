---
name: review-manager
description: "**客户评价收集、自动回复、通知及报告的集成管理**  
支持对 Naver Place、Google、Bamibin、Coupang 等平台的客户评价进行监控、情感分析，并提供竞争对手对比功能。"
homepage: https://github.com/openclaw/review-manager
metadata:
  {
    "openclaw":
      {
        "emoji": "⭐",
        "requires": { "bins": ["node"] },
        "install": [],
      },
  }
---
# 评论管理器

这是一个用于集成管理客户评论的系统，能够自动收集来自多个平台的评论，并提供基于人工智能的自动回复功能、恶意评论提醒以及每周分析报告。

## 主要功能

1. **评论收集**：自动抓取来自Naver Place、Google Reviews、Baidu My People和Coupang的评论。
2. **自动回复**：针对正面评论生成感谢回复；针对负面评论生成表示理解的回复并提出解决方案。
3. **恶意评论提醒**：当评论评分低于2分或包含特定关键词时，立即发送提醒。
4. **每周报告**：生成平均评分趋势、关键词分析以及情感分析摘要。
5. **竞争对手对比**：监控同一类别下竞争对手的评论得分。

## 设置

请创建文件 `~/.openclaw/workspace/skills/review-manager/config.json`：

```json
{
  "stores": [
    {
      "id": "store1",
      "name": "무펭이 카페 강남점",
      "platforms": {
        "naver": "https://m.place.naver.com/restaurant/1234567890",
        "google": "ChIJN1t_tD...",
        "baemin": "https://www.baemin.com/...",
        "coupang": "https://www.coupangeats.com/..."
      }
    }
  ],
  "alert": {
    "channels": ["discord"],
    "discordChannelId": "1234567890",
    "thresholds": {
      "lowRating": 2,
      "keywords": ["불친절", "더럽", "환불", "최악"]
    }
  },
  "competitors": [
    {
      "name": "경쟁업체A",
      "naver": "https://m.place.naver.com/restaurant/9876543210"
    }
  ],
  "schedule": {
    "collectInterval": "1h",
    "weeklyReportDay": "monday",
    "weeklyReportTime": "09:00"
  }
}
```

复制模板：

```bash
cp {baseDir}/config.template.json ~/.openclaw/workspace/skills/review-manager/config.json
```

## 使用方法

### 1. 评论收集

- 收集所有平台的最新评论：

```bash
node {baseDir}/scripts/collect-reviews.js
```

- 仅收集特定店铺的评论：

```bash
node {baseDir}/scripts/collect-reviews.js --store store1
```

- 仅收集特定平台的评论：

```bash
node {baseDir}/scripts/collect-reviews.js --platform naver
```

### 2. 自动回复生成

- 为未回复的评论自动生成回复（仅用于预览，不实际发布）：

```bash
node {baseDir}/scripts/auto-reply.js --preview
```

- 实际发布回复（需要使用平台API或浏览器自动化工具）：

```bash
node {baseDir}/scripts/auto-reply.js --apply
```

### 3. 恶意评论检测

- 根据设定的阈值或关键词检测负面评论并发送提醒：

```bash
node {baseDir}/scripts/check-negative.js
```

### 4. 每周报告

- 显示过去7天的评论统计信息、情感分析结果及关键词趋势：

```bash
node {baseDir}/scripts/weekly-report.js
```

- 通过Discord发送报告：

```bash
node {baseDir}/scripts/weekly-report.js --send discord
```

### 5. 竞争对手对比

- 分析竞争对手的评论得分：

```bash
node {baseDir}/scripts/compare-competitors.js
```

## 数据存储

所有收集到的评论将以JSON格式保存在 `~/.openclaw/workspace/skills/review-manager/data/` 目录下：

```
data/
├── reviews/
│   ├── store1-naver-2026-02.json
│   ├── store1-google-2026-02.json
│   └── ...
├── replies/
│   └── generated-replies.json
└── reports/
    └── weekly-2026-W07.json
```

## 回复生成逻辑

- **评分4-5分**：回复表示感谢，并保持品牌风格和礼貌。
- **评分3分**：回复保持中立态度，并表达改进的意愿。
- **评分1-2分**：表示理解并道歉，同时提供具体的解决方案。

系统利用Claude/GPT等AI模型生成自然流畅的回复内容。

## 注意事项

- 不同平台的抓取政策可能有所不同，过度请求可能会导致请求被拒绝。
- 建议优先使用Naver Place的移动网页版本进行数据抓取。
- 使用Baidu My People或Coupang时可能需要登录（可通过浏览器自动化工具实现）。
- 自动回复时必须遵守各平台的规定。

## 提示

- 可以将本工具与OpenClaw的heartbeat功能结合使用，实现定期自动检查评论。
- 可通过Discord webhook实现实时提醒功能。
- 回复内容的语气可以通过config.json文件按品牌进行自定义。

## 故障排除

| 问题 | 解决方法 |
|------|------|
| Naver Place出现403错误 | 更改User-Agent并增加请求间隔 |
- Google Reviews抓取失败 | 检查是否使用了正确的Google Places API |
- 使用Baidu My People时需要登录 | 通过浏览器工具获取cookie后重新尝试 |
- 回复质量不佳 | 在config.json中添加品牌相关的回复指南 |
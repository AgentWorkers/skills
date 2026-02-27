---
name: influencer-report
description: 生成一份全面的影响力者审核报告。当有人请求审核、分析或评估某个影响力者/创作者时，可以使用该报告。该报告基于创作者的个人资料链接或视频链接，利用 Memories.ai 的视频智能技术生成关于品牌安全性和内容质量的评估结果。
---
# 影响者报告功能

通过使用 Memories.ai 的 V1 和 V2 API 分析影响者的最新视频来对其进行评估。

## 设置

所需的环境变量：
- `MEMORIES_V1_API_KEY` — Memories.ai V1 API 密钥（用于数据抓取、库操作和搜索）
- `MEMORIES_API_KEY` — Memories.ai V2 API 密钥（用于获取视频转录文本和元数据）

## 快速入门

**通过个人资料 URL 获取最新视频：**
```bash
python3 scripts/influencer_report.py --handle charlidamelio \
  --profile-url "https://www.tiktok.com/@charlidamelio" --scrape-count 5
```

**通过直接视频 URL 获取最新视频：**
```bash
python3 scripts/influencer_report.py --handle creator_name --platform tiktok \
  --videos https://tiktok.com/@user/video/1 https://tiktok.com/@user/video/2
```

## 工作流程

1. **数据抓取**：使用 V1 的 `/scraper` 功能从影响者的个人资料 URL 中获取其最新视频。
2. **列表与搜索**：使用 V1 的 `/list_videos` 和 `/search` 功能检索抓取到的视频内容。
3. **分析**：使用 V2 的 MAI 转录文本 API 对每个视频进行视觉和音频分析。
4. **元数据获取**：使用 V2 的元数据 API 获取视频的互动数据（观看次数、点赞数、评论数）。
5. **评分与报告生成**：对视频内容进行评分，并生成格式化的 Markdown 报告。

## 使用的 API 端点

| 步骤 | API | 端点            |
|------|----------------|-------------------|
| 抓取个人资料数据 | V1 | `POST /serve/api/v1/scraper`   |
| 列出视频列表 | V1 | `POST /serve/api/v1/list_videos`   |
| 搜索视频 | V1 | `POST /serve/api/v1/search`   |
| 视频转录文本 | V2 | `POST /serve/api/v2/{platform}/video/mai/transcript` |
| 视频元数据 | V2 | `POST /serve/api/v2/{platform}/video/metadata` |

## 报告格式

完整的报告模板和评分指南请参见 `references/report-format.md`。
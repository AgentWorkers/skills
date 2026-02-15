---
name: social-sentiment
description: "针对Twitter、Reddit和Instagram上的品牌及产品进行情感分析。监控公众舆论，追踪品牌声誉，及时发现公关危机，大规模识别用户的投诉与赞扬。支持分析超过7万条帖子，并提供批量CSV导出功能，可使用Python和pandas库进行处理。该服务基于超过15亿条已索引的帖子数据，提供高效的社会舆论监测与品牌监控功能。"
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["mcporter"],
            "skills": ["xpoz-setup"],
            "network": ["mcp.xpoz.ai"],
            "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)",
          },
        "install": [{"id": "node", "kind": "node", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter (npm)"}],
      },
  }
tags:
  - sentiment-analysis
  - brand-monitoring
  - social-media
  - twitter
  - reddit
  - instagram
  - analytics
  - brand-sentiment
  - reputation
  - social-listening
  - opinion-mining
  - brand-tracking
  - competitor-analysis
  - public-opinion
  - crisis-detection
  - NLP
  - reputation
  - mcp
  - xpoz
  - opinion
  - market-research
---

# 社交情感分析

**大规模分析实时社交对话中的品牌情感。**

该工具能够识别热门话题、发现引发广泛关注的负面评论，并对比不同品牌的表现。支持通过批量CSV文件和Python语言对1000到70,000条帖子进行分析。

## 设置

运行 `xpoz-setup` 命令进行初始化。验证设置是否正确：`mcporter call xpoz.checkAccessKeyStatus`

## 四步分析流程

### 第一步：搜索相关平台

查询条件：(1) `"Brand"` (2) `"Brand" AND (slow OR buggy)" (3) `"Brand" AND (love OR amazing)"  

```bash
mcporter call xpoz.getTwitterPostsByKeywords query='"Notion"' startDate="YYYY-MM-DD"
mcporter call xpoz.checkOperationStatus operationId="op_..." # Poll 5s
```

针对Reddit和Instagram平台重复此步骤。默认搜索范围为30天内的数据。

### 第二步：下载CSV文件

使用 `dataDumpExportOperationId` 获取下载链接，并通过 `checkOperationStatus` 检查下载是否成功（最多可下载64,000条数据）。

### 第三步：数据分析

使用Python和pandas库对数据进行处理：  
```python
import pandas as pd
df = pd.read_csv('/tmp/twitter-sentiment.csv')

POSITIVE = ['love', 'amazing', 'best', 'recommend']
NEGATIVE = ['hate', 'terrible', 'worst', 'broken']

def classify(text):
    t = str(text).lower()
    pos = sum(1 for k in POSITIVE if k in t)
    neg = sum(1 for k in NEGATIVE if k in t)
    return 'positive' if pos>neg else ('negative' if neg>pos else 'neutral')

df['sentiment'] = df['text'].apply(classify)
```

从数据中提取关键主题，并根据用户互动情况识别具有高传播力的负面评论。可根据需求自定义搜索关键词。

### 第四步：生成报告

生成分析报告：  
```
Sentiment: 72/100 | Posts: 14,832
😊 58% | 😠 24% | 😐 18%

Themes: Performance (2K, 81% neg), UX (1.8K, 72% pos)
Viral: [Top 10]
```

报告结果采用互动度加权评分（0-100分），并包含详细的分析洞察。

## 提示：

- 可下载完整的CSV文件；  
- Reddit平台的数据较为真实可靠；  
- 将分析结果保存在 `data/social-sentiment/` 目录中，便于后续趋势分析。
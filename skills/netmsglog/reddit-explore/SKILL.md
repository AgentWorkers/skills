---
name: reddit-explore
description: |
  This skill should be used when the user asks to "search Reddit", "explore Reddit posts", "find Reddit discussions about", "summarize Reddit opinions on", "what does Reddit think about", or wants to gather and summarize community opinions from Reddit on a specific topic.
disable-model-invocation: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3"], "env": ["APIFY_TOKEN"] },
        "primaryEnv": "APIFY_TOKEN",
      },
  }
---

# Reddit探索

使用Apify的`trudax/reddit-scraper-lite`代理在Reddit上搜索任何主题的帖子，并生成关于社区意见的结构化摘要。

## 先决条件

在运行之前，请确认以下条件：
1. **已安装`apify-client`**：`pip3 install apify-client`
2. **`APIFY_TOKEN`已设置为环境变量**

如果缺少任何一项，请引导用户参考本技能目录中的`references/apify-setup.md`以获取设置说明。

## 工作流程

### 第1步：确定搜索主题

搜索主题来自 `$ARGUMENTS`。如果 `$ARGUMENTS`为空或缺失，请询问用户想要搜索哪个主题。

### 第2步：运行Reddit搜索脚本

使用用户提供的主题执行搜索脚本：

```bash
python3 ~/.agents/skills/reddit-explore/scripts/reddit_search.py --query "$ARGUMENTS" --max-items 30
```

脚本会将搜索结果以JSON格式输出到标准输出（stdout）。如果出现错误：
- **“APIFY_TOKEN未找到”**：指导用户设置他们的APIFY_TOKEN（参见`references/apify-setup.md`）
- **“未安装apify-client”**：运行`pip3 install apify-client`
- **其他错误**：显示错误信息并提供故障排除帮助

### 第3步：分析并总结结果

阅读JSON输出。每个结果包含以下信息：
- `title`：帖子标题
- `communityName`：子版块名称
- `upVotes`：点赞数
- `numberOfComments`：评论数量
- `url`：帖子链接
- `body`：帖子文本内容
- `createdAt`：发布时间

### 第4步：生成结构化摘要

以以下格式呈现搜索结果：

#### 概述
用2-3句话简要总结Reddit上对该主题的看法。

#### 社区意见
- **整体态度**：积极 / 中立 / 消极
- **主要讨论的子版块**：列出讨论该主题最活跃的子版块

#### 主要观点
- **积极方面**：列出受赞扬的方面，并附上相关帖子的链接
- **消极方面**：列出受到批评的方面，并附上相关帖子的链接
- **中性/信息性内容**：社区中提到的重要事实

#### 重要帖子
列出3-5篇最相关或点赞最多的帖子，包括：
- 标题、子版块、点赞数
- 帖子内容的简要概述
- 帖子链接

#### 总结
对社区共识的简要总结。

## 提示
- 对于广泛的主题，脚本会使用用户提供的确切查询进行搜索。如果结果较少，建议用户尝试使用其他表述方式。
- 帖子默认按相关性排序。
- 脚本会自动通过URL去重搜索结果。
- Apify免费 tier每月提供5美元的信用额度；每次搜索通常只需几美分。
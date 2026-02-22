---
name: social-media-scheduler
description: 为任何主题生成一周的社交媒体内容。为Twitter/X、LinkedIn和Instagram生成适合各平台的优化帖子，并附上相关标签和发布时间。
triggers:
  - generate social media posts
  - create content calendar
  - weekly social media plan
---
# 社交媒体日程安排工具 📅

该工具能够为任何主题或领域生成一周的社交媒体内容，输出适合 **Twitter/X**、**LinkedIn** 和 **Instagram** 平台的优化内容。

## 使用方法

```bash
# Generate a week of posts for a topic
./generate.sh "artificial intelligence"

# Specify a niche audience
./generate.sh "sustainable fashion" "eco-conscious millennials"
```

### 参数
1. **主题/领域**（必填）—— 内容的主题
2. **目标受众**（可选）—— 内容的受众群体（默认：**普通受众**）

### 输出结果
会在当前目录下生成 `content-calendar.md` 文件，其中包含：
- 每天的7条帖子（周一至周日）
- 每天针对3个平台的不同内容（Twitter、LinkedIn、Instagram）
- 每个平台的标签建议
- 最佳发布时间
- 内容类型组合（教育性、互动性、推广性、故事性）

## 内置的内容策略

该工具遵循经过验证的每周内容发布策略：
| 星期 | 主题 |
|-----|-------|
| 周一 | 激励性内容 / 一周的开始 |
| 周二 | 教育性内容 / 操作指南 |
| 周三 | 互动性内容 / 问题解答 |
| 周四 | 背景故事 |  
| 周五 | 小贴士 / 快速技巧 |
| 周六 | 精选内容 / 行业新闻 |
| 周日 | 反思性内容 / 社区分享 |

## 平台发布指南
- **Twitter/X**：内容长度≤280个字符，简洁明了，使用2-3个标签，添加引导性话题
- **LinkedIn**：采用专业语气，段落不超过3段，分享有深度的观点，使用3-5个标签
- **Instagram**：以图片为主，配以简洁的说明文字，使用5-10个标签，并在个人简介中添加行动号召（CTA）

## 所需环境
- Bash shell 和 `cat` 命令（脚本会生成一个可自定义的Markdown模板）
- 如需通过AI实现个性化内容，可将输出结果传递给您喜欢的自然语言处理模型（LLM）

## 示例

```bash
./generate.sh "productivity tips" "remote workers"
# → Creates content-calendar.md with 21 ready-to-post drafts
```

## 作者
🦞 Shelly — [@ShellyToMillion](https://twitter.com/ShellyToMillion)
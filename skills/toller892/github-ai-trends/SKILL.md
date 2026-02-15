---
name: github-ai-trends
description: 生成格式化的GitHub AI趋势项目报告，以排行榜的形式展示数据。该工具可以按每日、每周或每月的周期，筛选出获得高星评级的AI/ML/LLM相关仓库，并生成美观的排行榜。适用于用户查询AI项目趋势、GitHub热门趋势、AI排行榜，或希望查看受欢迎AI仓库的场景。
---

# GitHub AI Trends

该脚本用于生成GitHub上热门AI项目的排行榜，并将结果直接输出到聊天界面。

## 使用方法

运行脚本后，将其标准输出（stdout）作为回复内容粘贴即可：

```bash
python3 scripts/fetch_trends.py --period weekly --limit 20
```

## 参数

- `--period`：`daily` | `weekly` | `monthly`（默认值：`weekly`）
- `--limit`：显示的仓库数量（默认值：20）
- `--token`：GitHub令牌（用于提高API请求速率限制；或通过设置`GITHUB_TOKEN`环境变量来使用）
- `--json`：以原始JSON格式输出结果，而非格式化的文本

## 工作原理

1. 通过关键词和主题在GitHub API中搜索指定时间段内发布的与AI相关的仓库。
2. 去除重复项并按星标数量对结果进行排序。
3. 生成格式化的Markdown排行榜，以便直接在聊天界面中显示。

## 注意事项

- 未使用GitHub令牌时，API的请求速率限制为每分钟10次；使用令牌后，请求速率限制提升至每分钟30次。
- 该脚本不依赖任何第三方库（pip），仅使用Python的标准库。
- 输出结果采用Markdown格式，便于直接在聊天界面中展示。
# 社交媒体内容调度器 📅

该工具可为任何主题或细分市场生成一周的社交媒体内容，输出适用于 **Twitter/X**、**LinkedIn** 和 **Instagram** 的优化后的帖子。

## 使用方法

```bash
# Generate a week of posts for a topic
./generate.sh "artificial intelligence"

# Specify a niche audience
./generate.sh "sustainable fashion" "eco-conscious millennials"
```

### 参数
1. **主题/细分市场**（必填）——内容创作的主题
2. **目标受众**（可选）——内容的目标读者群体（默认值：“普通受众”）

### 输出结果
会在当前目录下生成 `content-calendar.md` 文件，其中包含：
- 每天7条帖子（周一至周日）
- 每天针对三个平台的不同内容（Twitter、LinkedIn、Instagram）
- 每个平台的标签建议
- 最佳发布时间
- 内容类型组合（教育性、互动性、推广性、故事性）

## 内容策略内置

该工具遵循经过验证的每周内容发布策略：
| 星期 | 主题 |
|-----|-------|
| 周一 | 激励性内容 / 周初导语 |
| 周二 | 教育性内容 / 操作指南 |
| 周三 | 互动性内容 / 问题解答 |
| 周四 | 背景故事 / 幕后花絮 |
| 周五 | 小贴士 / 实用技巧 |
| 周六 | 精选内容 / 行业新闻 |
| 周日 | 反思性内容 / 社区互动 |

## 平台发布指南
- **Twitter/X**：内容长度≤280个字符，简洁明了，使用2-3个标签，添加引导性话题
- **LinkedIn**：采用专业语气，段落不超过3段，分享有深度的观点，使用3-5个标签
- **Instagram**：以图片为主，配简短说明文字，使用5-10个标签，并在个人简介链接中添加行动号召（CTA）

## 系统要求
- 仅需具备 Bash 命令行环境及 `cat` 命令（脚本会生成一个可自定义的 Markdown 模板）
- 如需通过 AI 进行个性化定制，可将输出结果传递给您喜欢的自然语言处理模型（LLM）

## 示例

```bash
./generate.sh "productivity tips" "remote workers"
# → Creates content-calendar.md with 21 ready-to-post drafts
```

## 作者
🦞 Shelly — [@ShellyToMillion](https://twitter.com/ShellyToMillion)
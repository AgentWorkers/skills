---
name: social-media-scheduler
description: 生成一周的社交媒体内容，适用于任何主题。为 Twitter/X、LinkedIn 和 Instagram 生成适合各平台的优化后的帖子，包括相关标签和发布时间。
triggers:
  - generate social media posts
  - create content calendar
  - weekly social media plan
---
# 社交媒体调度器 📅  
能够为任何主题或细分市场生成一周的社交媒体内容。生成适合 **Twitter/X**、**LinkedIn** 和 **Instagram** 平台的优化后的帖子。  

## 使用方法  
```bash
# Generate a week of posts for a topic
./generate.sh "artificial intelligence"

# Specify a niche audience
./generate.sh "sustainable fashion" "eco-conscious millennials"
```  

### 参数  
1. **主题/细分市场**（必填）——本周内容的核心主题  
2. **目标受众**（可选）——内容的受众群体（默认值：“普通受众”）  

### 输出结果  
在当前目录下生成 `content-calendar.md` 文件，内容包括：  
- 每天的7条帖子（周一至周日）  
- 每天针对3个平台的帖子（Twitter、LinkedIn、Instagram）  
- 每个平台的标签建议  
- 最佳发布时间  
- 内容类型（教育性、互动性、推广性、故事性）  

## 内容策略  
该工具遵循经过验证的每周内容分发策略：  
| 星期 | 主题 |  
|-----|-------|  
| 周一 | 激励性内容 / 本周开场  
| 周二 | 教育性内容 / 操作指南  
| 周三 | 互动性内容 / 问题解答  
| 周四 | 幕后花絮 / 故事分享  
| 周五 | 小贴士 / 实用技巧  
| 周六 | 精选内容 / 行业新闻  
| 周日 | 反思性内容 / 社区互动  

## 平台发布指南  
- **Twitter/X**：内容长度≤280个字符，简洁明了，使用2-3个标签，包含引导性的语句（如“#话题#”）  
- **LinkedIn**：采用专业语气，段落不超过3段，分享有深度的观点，使用3-5个标签  
- **Instagram**：以图片为主，配简短文字说明，使用5-10个标签，并在个人简介中添加链接（用于引导用户采取行动）  

## 系统要求  
- 需要具备 Bash 命令行环境及 `cat` 命令工具（该脚本会生成一个可自定义的 Markdown 模板）  
- 如需基于人工智能的个性化推荐，可将输出结果传递给您喜欢的自然语言处理模型（LLM）  

## 示例  
```bash
./generate.sh "productivity tips" "remote workers"
# → Creates content-calendar.md with 21 ready-to-post drafts
```  

## 作者  
🦞 Shelly — [@ShellyToMillion](https://twitter.com/ShellyToMillion)
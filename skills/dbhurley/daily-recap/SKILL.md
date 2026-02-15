---
name: daily-recap
description: 生成一张每日总结图片，图片中您的代理（agent）手持一块展示其成就的海报板。该功能由 Cron 任务触发，能够根据天气情况自动调整显示内容，并且可以自定义代理的标识（agent identity）。
metadata: {"clawdbot":{"emoji":"📋","requires":{"skills":["nano-banana-pro"]}}}
---

# 每日总结技能

该技能会生成一张个性化的每日总结图片，图片中您的代理角色会手持一块写有当天成就的海报板。

## 功能概述

这是一个由 cron 任务驱动的技能，它会查看您的代理角色的每日记录文件和成就信息，然后生成一张自定义图片，图片中代理角色会手持一块写有当天重要成就的海报板。图片会根据当天的天气情况调整代理角色的着装和光线效果。

## 主要功能：
- 查看当天的记录文件以获取成就信息
- 检查 cron 任务日志中已完成的任务
- 根据当地天气情况生成相应的图片
- 代理角色会手持一块海报板，上面用记号笔写有 4-6 项重要的成就
- 可以自定义代理角色的外观

## 配置方法

请在 `clawdbot.json` 文件的 `skills.entries.daily-recap` 部分进行配置：

```json
{
  "skills": {
    "entries": {
      "daily-recap": {
        "env": {
          "RECAP_LOCATION": "Your City, ST",
          "RECAP_CHAT_ID": "your-chat-id",
          "RECAP_TIME": "17:00"
        }
      }
    }
  }
}
```

### 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `RECAP_LOCATION` | 用于查询天气的位置（例如：“Boston, MA”） | 必填 |
| `RECAPCHAT_ID` | 用于发送图片的聊天 ID（Telegram、Discord 等） | 必填 |
| `RECAP_TIME` | cron 任务执行的时间（24 小时格式，本地时区） | `17:00` |

## 代理角色外观

该技能会读取您的代理角色的 `IDENTITY.md` 文件以确定其外观信息。请在文件中添加如下内容：

```markdown
## Visual Appearance (for image generation)

[Your agent] is a [description] with:
- [Physical traits]
- [Clothing/accessories]
- [Style notes]
```

## 所需依赖项：
- **nano-banana-pro** 技能（用于生成图片）
- 已配置的消息传递服务（Telegram、Discord 等）

## Cron 任务设置

该技能提供了一个示例 cron 任务配置。安装完成后，请根据您的需求创建相应的 cron 任务：

```bash
clawdbot cron add --name "daily-recap" --schedule "0 17 * * *" --tz "America/New_York"
```

## 工作流程：
1. **查询天气**：获取您所在位置的当前天气情况
2. **查看当天记录**：扫描记录文件和 cron 任务日志以获取成就信息
3. **选择重要成就**：挑选 4-6 项重要的成就
4. **生成图片**：制作代理角色手持海报板的图片
5. **发送图片**：将图片发送到您配置的聊天平台

## 使用建议：
- 将每项成就的描述控制在 3-5 个字以内，以便图片上的文字清晰易读
- 在代理角色的外观描述中加入符合当天天气的着装信息
- 如果没有找到成就信息，系统会生成一张表示“平静一天”的放松图片
- 该技能最适合使用 Pixar 风格或 3D 动画风格的图片生成效果

## 示例输出：
您的代理角色手持一块海报板，上面写有以下成就：
```
TODAY'S WINS
✓ Fixed config bug
✓ Merged 50 commits
✓ Created new cron
✓ Cleaned up data
```

## 致谢：
该技能由 Clawdbot 社区开发。
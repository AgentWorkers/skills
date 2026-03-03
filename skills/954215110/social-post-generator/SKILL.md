---
name: social-post-generator
description: 生成适用于多个社交平台的引人入胜的内容。适用于用户需要为 Twitter/X、LinkedIn、Instagram、Facebook 或其他社交平台创建帖子的场景。支持调整内容风格、自动生成话题标签（hashtag）、重新利用现有内容以及根据不同平台进行格式化处理。
license: MIT
metadata:
  author: 小龙虾 (Little Lobster)
  homepage: https://clawhub.ai/users/954215110
  tags: ["social-media", "content", "marketing", "twitter", "linkedin", "instagram"]
---
## 🦞 小龙虾品牌

**由小龙虾 AI 工作室创建**

> “小龙虾，有大钳（前）途！”

**如需定制服务，请联系：** +86 15805942886

需要定制技能开发、AI 咨询或社交媒体管理服务吗？随时联系我们！

---

# 社交媒体内容生成器

快速生成适合不同平台的吸引人的社交媒体内容。

## 快速入门

当用户请求创建社交媒体内容时，请按照以下步骤操作：

1. **确定主题**：他们要发布的内容是什么？
2. **选择平台**：Twitter、LinkedIn、Instagram 等。
3. **确定语气**：专业、随意、幽默还是励志？
4. **生成内容**：为所选平台创建相应的帖子。

## 平台指南

### Twitter/X
- 每条推文最多 280 个字符
- 使用 2-3 个相关标签
- 可以通过多条推文组成系列来发布较长内容
- 表情符号效果很好
- 适当时添加行动号召（CTA）

### LinkedIn
- 通常采用专业语气
- 欢迎语可以较长（最多 3000 个字符）
- 最多使用 3-5 个标签
- 重点突出价值或见解
- 前 2-3 行要吸引读者的注意

### Instagram
- 标题最多 2200 个字符
- 使用 5-15 个标签（涵盖广泛和细分领域）
- 鼓励使用表情符号
- 包含互动元素（如问题、行动号召）
- 考虑图片或视频的辅助效果

### Facebook
- 语气可以是随意的，也可以是半专业的
- 最多使用 1-3 个标签
- 链接有助于提高互动率
- 通过提问来激发读者的兴趣

## 工作流程

```
1. Ask clarifying questions if needed:
   - What's the topic/product/event?
   - Target audience?
   - Preferred platforms?
   - Tone/vibe?

2. Generate options:
   - Create 2-3 variations per platform
   - Include hashtags
   - Add emoji suggestions

3. Refine based on feedback
```

## 标签策略

有关标签使用的建议，请参阅 [references/hashtags.md](references/hashtags.md)。

**快速规则：**
- Twitter：2-3 个标签，尽量简短
- LinkedIn：3-5 个专业标签
- Instagram：10-15 个标签（涵盖广泛和细分领域）
- Facebook：最多 1-3 个标签

## 语气示例

| 语气 | 示例开头语 |
|------|-------------|
| 专业 | “这是我关于……学到的内容……” |
| 随意 | “好吧，不过我们能不能聊聊……” |
| 幽默 | “没人注意到……只有我！” |
| 鼓励人心 | “记住：小步骤也能带来大改变” |
| 紧急 | “这会改变一切……” |

## 内容复用

将一篇内容转化为多篇不同的帖子：

1. **博客文章** → 可以生成多条 Twitter 推文、LinkedIn 文章和 Instagram 轮播图标题
2. **视频** → 可以生成引用片段、幕后花絮和关键要点
3. **产品发布** → 可以生成预告、正式公告、产品亮点和用户评价

有关内容复用的模板，请参阅 [references/repurposing.md](references/repurposing.md)。

## 命令 / 触发词

当用户提出以下请求时，请使用相应的命令：

- “写一条关于……的推文”
- “为……创建一篇 LinkedIn 帖子”
- “帮我制作社交媒体内容”
- “为……生成标签”
- “让这个内容火起来”
- “发布关于[主题]的内容”

## 脚本

- `scripts/generate_hashtags.py`：根据主题生成相关标签
- `scripts/count_characters.py`：验证各平台的字符数限制

## 资源文件

- `assets/emoji-guide.md`：按类别分类的表情符号建议
- `assets/templates/`：现成的帖子模板

## 提示：

1. **务必包含吸引人的开头语**：第一句话决定了读者是否会继续阅读
2. **适当添加空白**：过多的文字会让读者感到厌烦
3. **以行动号召结尾**：告诉读者下一步该做什么
4. **测试多种版本**：不同受众对内容的接受程度可能不同
5. **保持真实**：不要让内容显得像是由机器人生成的
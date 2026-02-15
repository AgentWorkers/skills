---
name: prompt-engineering
description: |
  Master prompt engineering for AI models: LLMs, image generators, video models.
  Techniques: chain-of-thought, few-shot, system prompts, negative prompts.
  Models: Claude, GPT-4, Gemini, FLUX, Veo, Stable Diffusion prompting.
  Use for: better AI outputs, consistent results, complex tasks, optimization.
  Triggers: prompt engineering, how to prompt, better prompts, prompt tips,
  prompting guide, llm prompting, image prompt, ai prompting, prompt optimization,
  prompt template, prompt structure, effective prompts, prompt techniques
allowed-tools: Bash(infsh *)
---

# 提示工程指南

通过 [inference.sh](https://inference.sh) 命令行界面 (CLI) 掌握 AI 模型的提示工程技巧。

## 快速入门

```python
user_input = request.args.get("query")
result = db.execute(f"SELECT * FROM users WHERE name = {user_input}")
```

请提供具体的问题及其解决方案。

---

[角色/上下文] + [任务] + [约束条件] + [输出格式]

---

```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "你是一位拥有 15 年机器学习经验的专家数据科学家。用简单的类比向初学者解释梯度下降算法。"
}
```

---

**错误示例：**  
“帮我修改我的代码。”

**正确示例：**  
“调试这个 Python 函数，它应该计算列表中所有偶数的和，但目前的代码对所有输入都返回 0：”

```python
def sum_evens(numbers):
    total = 0
    for n in numbers:
        if n % 2 == 0:
            total += n
    return total
```

请找出错误并提供修正后的代码。

---

**提示示例：**  
“逐步解决这个问题：**  
“一家商店以每颗 2 美元的价格出售苹果，以每颗 3 美元的价格出售橙子。如果有人购买了 5 个水果并花费了 12 美元，他们各买了多少个水果？在给出最终答案之前，请先逐步思考。”

---

**提示示例：**  
“将这些句子转换为正式的商务英语：**  
**示例 1：**  
输入：` gonna send u the report tmrw`  
输出：`I will send you the report tomorrow.`  

**示例 2：**  
输入：`cant make the meeting, something came up`  
输出：`I apologize, but I will be unable to attend the meeting due to an unforeseen circumstance.`  

**现在将其转换为：**  
输入：`Hey, can we push the deadline back a bit?`  

---

**提示示例：**  
“分析这些客户评论的情感。返回一个 JSON 数组，其中包含 `text`、`sentiment`（正面/负面/中性）和 `confidence`（0-1）字段。**  
**评论：**  
1. `Great product, fast shipping!`  
2. `Meh, its okay I guess`  
3. `Worst purchase ever, total waste of money`  

**注意：** 仅返回有效的 JSON 数据，无需解释。  

---

**提示示例：**  
“用 exactly 3 个要点总结这篇文章。每个要点不得超过 20 个单词。仅关注可操作的见解，不要包含背景信息。**  
**[文章内容]**  

---

**主题** + **风格** + **构图** + **光线** + **技术要求**  

---

**错误示例：**  
“一只猫。”

**正确示例：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一只毛茸茸的橙色虎斑猫，绿色的眼睛，坐在一把复古皮革扶手椅上。"
}`

---

**提示示例：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一张女性的肖像照片，使用柯达 Portra 400 胶片拍摄，柔和的自然光，浅景深，怀旧的氛围，模拟摄影风格。"
}`

---

**提示示例：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "夜景中的赛博朋克城市天际线全景镜头，三分法构图，前景有霓虹灯，背景是高耸的摩天大楼，街道被雨水打湿。"
}`

---

**技术要求：**  
- 真实感强  
- 8K 分辨率  
- 超高细节  
- 清晰的焦点  
- 专业品质  

---

**提示示例：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "专业的头部特写肖像，背景干净。"
  "负面提示："  
  "图像模糊、变形、有多余的肢体、水印、文字、低质量、卡通风格或动漫效果。"
}`

---

**镜头类型** + **主题** + **动作** + **场景** + **风格**  

---

**提示示例：**  
`infsh app run google/veo-3-1-fast --input '{
  "prompt": "跟随一位女性在阳光照耀的森林中行走的慢动作镜头，黄金时刻的光线，浅景深，电影风格，4K 分辨率。"
}`

---

**提示示例：**  
`infsh app run google/veo-3-1-fast --input '{
  "prompt": "手在木制表面上揉面团的特写镜头，面粉屑在晨光中飘浮，慢动作，温馨的烘焙氛围。"
}`

---

**技术要求：**  
- 慢动作  
- 时间延时  
- 实时效果  
- 平稳的镜头切换  
- 冻结关键瞬间  

---

**提示示例：**  
`infsh app run openrouter/claude-sonnet-45 --input '{
  "system": "你是一个乐于助人的编程助手。提供代码时请加上注释。如果你对某些内容不确定，请明确说明，而不是猜测。",
  "prompt": "编写一个使用正则表达式验证电子邮件地址的 Python 函数。"
}`

---

**提示示例：**  
`infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "从这段文本中提取信息并返回 JSON 格式："
  "John Smith, CEO of TechCorp, announced yesterday that the company raised $50 million in Series B funding. The round was led by Venture Partners."
  "schema": {
    "person": "字符串",
    "title": "字符串",
    "company": "字符串",
    "event": "字符串",
    "amount": "字符串",
    "investor": "字符串"
  }
}`

---

**提示示例：**  
**初始提示：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一座位于山丘上的城堡。"
}`

**详细化提示：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一座坐落在草坡上的中世纪石堡。"
}`

**添加风格：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一座坐落在草坡上的中世纪石堡，戏剧性的日落天空，奇幻艺术风格，宏大的构图。"
}`

**增加技术细节：**  
`infsh app run falai/flux-dev --input '{
  "prompt": "一座坐落在草坡上的中世纪石堡，戏剧性的日落天空，由 Greg Rutkowski 设计的奇幻艺术风格，8K 分辨率，高度详细的画面。"
}`

---

**提示示例：**  
**分析问题：**  
`infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "分析这个业务问题：我们的电子商务网站的购物车放弃率为 70%。列出可能的原因。"
}`

**优先级排序：**  
`infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "根据这些购物车放弃的原因 [之前的输出]，按照影响程度和修复难易程度对它们进行排序。"
}`

**制定行动计划：**  
`infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "对于排名前三的原因，提供具体的 A/B 测试来验证和修复每个问题。"
}`

---

**代码审查：**  
检查以下代码：**  
1. 代码中的错误和逻辑问题  
2. 安全漏洞  
3. 性能问题  
4. 代码风格和最佳实践  

**代码审查内容：**  
[代码]

对于发现的每个问题，请提供：  
- 问题所在的行号  
- 问题描述  
- 问题严重程度（高/中/低）  
- 建议的修复方法  

---

**编写内容：**  
**内容类型：** [具体内容类型]  
**目标受众：** [目标读者群体]  
**语气：** [正式/随意/专业]  
**字数：** [所需字数]  
**需要涵盖的关键点：**  
1. [关键点 1]  
2. [关键点 2]  
3. [关键点 3]  
**包含的元素：** [必须包含的元素]  
**避免的内容：** [不应包含的元素]  

---

**其他功能：**  
[相关功能列表]  
- [功能描述]  

---

**视频提示指南：**  
`npx skills add inference-sh/agent-skills@video-prompting-guide`  

**大语言模型：**  
`npx skills add inference-sh/agent-skills@llm-models`  

**图像生成：**  
`npx skills add inference-sh/agent-skills@ai-image-generation`  

**完整平台技能：**  
`npx skills add inference-sh/agent-skills@inference-sh`  

**浏览所有应用程序：**  
`infsh app list`
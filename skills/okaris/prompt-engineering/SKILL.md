---
name: prompt-engineering
description: "掌握AI模型的提示工程（Prompt Engineering）技术：适用于大型语言模型（LLMs）、图像生成模型和视频模型。相关技术包括“思维链”（Chain-of-Thought）策略、小样本学习（Few-Shot Learning）方法、系统化提示设计（Systematic Prompting）、以及负面提示（Negative Prompting）等。涉及的模型包括Claude、GPT-4、Gemini、FLUX、Veo和Stable Diffusion等。这些技术可用于提升AI模型的输出质量、确保结果的一致性、处理复杂任务以及优化模型性能。相关内容涵盖提示工程的基本概念、使用方法、优化技巧、提示模板设计以及有效的提示编写策略等。"
allowed-tools: Bash(infsh *)
---
# 提示工程指南

通过 [inference.sh](https://inference.sh) 命令行界面（CLI）掌握 AI 模型的提示工程技术。

![提示工程指南](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgvftjwhby36trvaj66bwzcf.jpeg)

## 快速入门

```python
user_input = request.args.get("query")
result = db.execute(f"SELECT * FROM users WHERE name = {user_input}")
```

请提供具体的问题及其解决方案。

---

**[角色/上下文] + [任务] + [约束条件] + [输出格式]**  
---

```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "你是一位拥有 15 年机器学习经验的数据科学家。用简单的类比向初学者解释梯度下降算法。"
}
```

---

**错误示例：**  
“帮我修改一下代码。”

**正确示例：**  
“请修复这个 Python 函数，它应该计算列表中所有偶数的和，但目前的实现总是返回 0：”

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

**[提示示例：**  
“逐步解决这个问题：**  
“一家商店以每颗 2 美元的价格出售苹果，以每颗 3 美元的价格出售橙子。如果有人购买了 5 个水果并且花费了 12 美元，他们各买了多少个水果？在给出最终答案之前，请先仔细思考。”

---

**[提示示例：**  
“将以下句子转换为正式的商务英语：**  
“示例 1：  
输入：I will send you the report tmrw.  
输出：我将在明天发送报告。  
示例 2：  
输入：I can't make the meeting, something came up.  
输出：很抱歉，由于突发情况，我无法参加会议。  
现在请转换：  
输入：Hey, can we push the deadline back a bit?**”

---

**[提示示例：**  
“分析这些客户评论的情感。返回一个 JSON 数组，其中包含 ‘text’、‘sentiment’（正面/负面/中性）和 ‘confidence’（0-1）字段。**  
**评论：**  
1. “Great product, fast shipping!”  
2. “Meh, its okay I guess.”  
3. “Worst purchase ever, total waste of money.”  
**注意：** 只返回有效的 JSON 数据，无需解释。**

---

**[提示示例：**  
“用不超过 20 个单词的三个要点总结这篇文章。仅关注可操作的见解，不要包含背景信息。**  
**[文章内容]**  

---

**[主题] + [风格] + [构图] + [光线] + [技术要求]**  
---

**错误示例：**  
“一只猫。”

**正确示例：**  
```bash
infsh app run falai/flux-dev --input '{
  "prompt": "一只毛茸茸的橙色虎斑猫，长着绿色的眼睛，坐在一把复古皮革扶手椅上。"
}
```

---

**[提示示例：**  
“拍摄一张女性的肖像照片，使用柯达 Portra 400 胶片，采用柔和的自然光，浅景深效果，营造怀旧的氛围，体现模拟摄影的风格。”  

---

**[提示示例：**  
“拍摄一张夜景下的赛博朋克城市天际线的全景图，遵循三分法则构图，前景有霓虹灯，背景是高耸的摩天大楼，街道被雨水打湿。”  

---

**[拍摄要求：**  
**视觉效果：**  
**照片类型：** 光影真实、8K 分辨率、超高细节、清晰对焦；  
**质量要求：** 专业级、高品质；  
**风格要求：** 复杂的细节处理。  

---

**[提示示例：**  
“拍摄一张专业的头像照片，背景要干净。”  
**负面提示：** 照片模糊、变形、出现多余的肢体、水印、文字、画质低、卡通效果或动画风格。**

---

**[拍摄要求：**  
**拍摄类型：**  
**拍摄对象：** [拍摄对象]  
**动作：** [拍摄动作]  
**场景：** [拍摄场景]  
**风格：** [拍摄风格]  
**光线：** [光线类型]  

---

**[提示示例：**  
**拍摄要求：**  
**视频类型：**  
**拍摄类型：** [视频类型]  
**动作：** 跟随一名女性在阳光照耀的森林中行走的慢动作镜头，使用黄金时刻的光线，浅景深效果，具有电影感；  
**分辨率：** 4K。**

---

**[提示示例：**  
**拍摄要求：**  
**视频类型：** **视频类型**  
**动作：** 手在木制表面上揉面团的特写镜头，面粉屑在晨光中飘浮，采用慢动作拍摄，营造温馨的烘焙氛围。**

---

**[提示示例：**  
**视频效果：**  
**视频效果：** 慢动作、延时摄影、实时效果、流畅的动作；连续镜头、定格瞬间。**

---

**[提示示例：**  
```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "system": "你是一个乐于助人的编程助手。在提供代码时一定要加上注释。如果你对某件事不确定，请直接说明，不要猜测。",
  "prompt": "编写一个使用正则表达式验证电子邮件地址的 Python 函数。"
}
```

---

**[提示示例：**  
**数据提取：**  
```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "从这段文本中提取信息并返回 JSON 格式："
  "John Smith, CEO of TechCorp, announced yesterday that the company raised $50 million in Series B funding. The round was led by Venture Partners."
}
```

---

**[提示示例：**  
**初始提示：**  
“一座位于山丘上的城堡。”

**细化提示：**  
```bash
infsh app run falai/flux-dev --input '{
  "prompt": "一座位于草坡上的中世纪石制城堡。"
}
```

**进一步细化：**  
```bash
infsh app run falai/flux-dev --input '{
  "prompt": "一座位于草坡上的中世纪石制城堡，夕阳下的戏剧性天空，采用奇幻艺术风格，构图宏大。"
}
```

**进一步细化（技术要求：**  
```bash
infsh app run falai/flux-dev --input '{
  "prompt": "一座位于草坡上的中世纪石制城堡，夕阳下的戏剧性天空，由 Greg Rutkowski 设计的奇幻艺术风格，8K 分辨率，高度细节化。"
}
```

---

**[问题分析：**  
```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "分析这个业务问题：我们的电子商务网站的购物车放弃率为 70%。列出可能的原因。"
}
```

**[问题优先级：**  
```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "根据这些购物车放弃的原因，按照影响程度和修复难度对它们进行排序。以优先级矩阵的形式呈现。"
}
```

**[问题解决方案：**  
```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "对于排名前三的原因，提供具体的 A/B 测试方案来验证和修复每个问题。"
}
```

---

**代码审查：**  
请检查以下代码，查找：  
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
- 建议的修复方案  

---

**[内容编写：**  
**内容类型：** [内容类型]  
**目标受众：** [目标受众]  
**语气：** [正式/随意/专业]  
**字数：** [字数要求]  
**需要涵盖的关键点：**  
1. [关键点 1]  
2. [关键点 2]  
3. [关键点 3]  
**需要包含的元素：** [需要包含的元素]  
**需要避免的内容：** [需要避免的内容]  

---

**[其他功能：**  
- [功能描述：**  
**功能名称：** [功能名称]  
**适用场景：** [适用场景]  
**其他相关信息：** [其他相关信息]  

---

**其他命令：**  
```bash
npx skills add inference-sh/skills@video-prompting-guide
npx skills add inference-sh/skills@llm-models
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@inference-sh
```

**浏览所有应用程序：**  
`infsh app list`
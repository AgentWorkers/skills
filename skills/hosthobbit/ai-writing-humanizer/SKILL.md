---
name: ai-writing-humanizer
description: 在发送用户可见的文本之前，自动去除其中由人工智能生成的写作模式和常用短语。在准备较长的文本时使用此功能，以确保文本具有自然、人性化的语气，且不会让人明显察觉到使用了人工智能生成的内容。
---
# 人工智能写作优化工具

该工具能够通过删除或重写常见的人工智能生成文本模式，使输入文本更加自然、更具人性化的表达。对于任何超过约150字的面向用户的 prose（散文或长文本），均可自动应用此优化功能。

## 支持优化的文本模式包括：

- 过度使用模糊性表达：如 “At the end of the day”（归根结底）、“It’s worth noting”（值得注意的是）、“It is important to remember”（需要记住的是）
- 用于引导段落结构的过渡词和标志：如 “First”（首先）、“Secondly”（其次）、“Finally”（最后）
- 用于表示结构分隔的符号：破折号（—）、用于添加旁注的括号、类似项目符号的列表
- 可预测的“三步式”结构：如 “X, Y, and Z” 这样的表述方式（常用于列出步骤）
- 以 “was”、“were”、“has been” 等动词开头的语句（通常属于被动语态）
- 表示礼貌或请求的表述：如 “I hope this helps”（希望这对您有帮助）、“Let me know if you have any questions”（如果您有任何问题，请告诉我）

## 使用方法：

1. 将输入文本传递给 `scripts/humanize.py` 命令，格式为：`scripts/humanize.py --input text.txt --output cleaned.txt`
2. 对于集成应用，可以从该脚本中导入 `humanize_text()` 函数，并在发送文本之前对其进行处理。

## 随附资源：

- `scripts/humanize.py`：一个基于正则表达式的 Python 脚本，用于识别并优化上述文本模式
- `references/signs-of-ai-writing.md`：根据维基百科整理的人工智能写作特征列表
- `tests/test_humanizer.py`：用于检测优化效果的回归测试脚本
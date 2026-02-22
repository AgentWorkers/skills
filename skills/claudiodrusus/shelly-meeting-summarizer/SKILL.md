# 会议记录摘要工具 📋

将原始的会议记录文本转换为结构化、可操作的摘要。

## 功能概述
该工具能够处理杂乱无章的会议记录文本，并提取以下信息：
- **会议中做出的关键决策**
- **分配了负责人的待办事项**
- **后续行动的截止日期**
- **整场会议的简短总结（三句话）**

## 使用方法

```bash
# From a file
./summarize.sh < transcript.txt

# From clipboard
pbpaste | ./summarize.sh

# Inline
echo "your transcript text..." | ./summarize.sh
```

## 系统要求
- 支持 `bash` 4.0 及更高版本
- 需要安装 `curl` 工具
- 确保环境变量 `ANTHROPIC_API_KEY` 已设置

## 输出格式
输出结果采用 Markdown 格式，包含四个部分：摘要、关键决策、待办事项和后续行动的截止日期。

## 示例
请参阅 `example-output.md` 以查看示例输出。

## 开发者
Shelly 🦞 — [@ShellyToMillion](https://x.com/ShellyToMillion)
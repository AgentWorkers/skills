---
name: less-token
description: "在摘要生成任务中，可以节省40%到65%的模型计算资源。将冗长的摘要提示压缩为结构化的一行指令。该工具仅支持文本到文本的翻译功能，无需使用命令行界面（CLI）、API密钥、进行安装，也不依赖任何外部组件。适用于ChatGPT、Claude、Gemini、DeepSeek、Kimi等模型。该工具仅提供指令格式的支持，完全不需要任何额外的依赖项。"
version: 1.0.2
author: ilang-ai
homepage: https://ilang.ai
tags:
  - summarize
  - summary
  - token-saving
  - token-optimizer
  - prompt-compression
  - productivity
  - cross-platform
  - no-install
  - ai-assistant
  - workflow
---
# Less Token

在摘要任务中，您可以节省40-65%的文本“令牌”（tokens，这里指用于表示文本长度的计数单位）。将冗长的自然语言提示压缩成任何AI都能理解的结构化的一行指令。

**请注意：**该工具仅用于文本到文本的转换。它不会访问文件、获取URL、执行命令或调用外部服务，仅会将您的摘要提示转换成压缩后的格式。

## 使用效果

1. **减少40-65%的文本长度**：将长摘要提示压缩成一行指令。
2. **结果不变**：AI会根据压缩后的指令生成相同的输出。
3. **跨平台兼容**：压缩后的指令可在ChatGPT、Claude、Gemini、DeepSeek、Kimi、豆包、元宝等AI平台上使用。
4. **无需安装**：无需安装任何命令行工具（CLI）、依赖包（npm）、二进制文件或API密钥，只需复制并粘贴即可使用。

## 使用方法

1. 从该工具页面复制完整的协议文本。
2. 将其粘贴到任何AI对话框中。
3. AI会自动进行压缩处理。

### 快速测试

粘贴后，尝试输入以下指令：
- “压缩这段文本：请用3个专业性的要点总结这份文档的要点。”

AI会返回：
`[SUM|sty=bullets,cnt=3,ton=pro]=>[OUT]`
这样，文本长度减少了70%，但输出结果保持不变。

## 压缩模板

| 指令类型 | 原始提示 | 压缩后的指令 |
|---------|----------------|------------|
| 简短摘要 | “请给我一个关于主要内容的简要总结。” | `[SUM\|len=short]=>[OUT]` |
| 3个要点 | “用3个简洁的要点进行总结。” | `[SUM\|sty=bullets,cnt=3]=>[OUT]` |
| 专业报告 | “生成一份专业的执行摘要（Markdown格式）。” | `[SUM\|ton=pro,sty=executive,fmt=md]=>[OUT]` |
| 仅提取关键内容 | “仅提取关键发现和重要数据。” | `[SUM\|key=findings]=>[OUT]` |
| 总结并翻译 | “先总结再翻译成中文。” | `[SUM\|len=short]=>[TRANSLATE\|lang=zh]=>[OUT]` |
| 对比并总结 | “对比这两份内容并总结差异。” | `[CMP]=>[DIFF]=>[SUM\|sty=bullets]=>[OUT]` |
| 重新格式化摘要 | “将摘要转换为Markdown格式的要点。” | `[SUM\|sty=bullets]=>[FMT\|fmt=md]=>[OUT]` |

## 使用前后的对比

**使用前**（28个单词）：
> 请仔细阅读这份文档，找出最重要的内容和关键要点，然后用要点形式写一份简洁的专业摘要。

**使用后**（7个单词）：
```
[SUM|key=important,sty=bullets,ton=pro]=>[OUT]
```
文本长度减少了75%，但输出结果保持不变。

**使用前**（22个单词）：
> 从上述文本中提取主要发现，并将其重写为适合商业读者的简短执行摘要。

**使用后**（5个单词）：
```
[SUM|sty=executive,ton=pro]=>[OUT]
```
文本长度减少了77%，但输出结果保持不变。

## 功能对比

| 功能 | 基于CLI的工具 | Less Token |
|---------|----------------|------------|
| 是否需要安装 | 需要（brew、npm、二进制文件） | 不需要 |
| 是否需要API密钥 | 需要 | 不需要 |
| 支持的平台 | 单一平台 | 所有AI平台 |
| 文本压缩效率 | 标准指令 | 减少40-65%的文本长度 |
| 设置时间 | 5-10分钟 | 30秒 |
| 外部依赖 | 多个 | 无 |

## 测试平台

ChatGPT ✅ · Claude ✅ · Gemini ✅ · DeepSeek ✅ · Kimi ✅ · 豆包 ✅ · 元宝 ✅

## 链接

- 协议与工具：https://ilang.ai
- 完整词典：https://github.com/ilang-ai/ilang-dict
- 研究资料：https://research.ilang.ai

## 许可证

MIT许可证——免费使用、分享和二次开发。

© 2026 I-Lang Research, Eastsoft Inc., Canada.
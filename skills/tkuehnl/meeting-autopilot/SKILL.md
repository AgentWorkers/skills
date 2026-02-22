---
name: meeting-autopilot
description: 将会议记录转换为可操作的输出内容，包括行动项、决策内容、后续跟进的电子邮件草稿以及工单草稿。该工具并非简单的总结工具，而是专门用于处理会议内容的工具。它支持接收 VTT（Voice Transcript Text）、SRT（SubRip Text）或纯文本格式的会议记录，并通过多轮处理（multi-pass processing）利用大型语言模型（LLM）来提取所需信息。
version: 0.1.1
author: Anvil AI
tags: [meetings, productivity, action-items, email-drafts, transcripts, operations, discord, discord-v2]
---
# ✈️ 会议自动化助手

将会议记录转换为结构化的操作结果——而不仅仅是摘要。

## 激活方式

当用户提及以下内容时，该功能会被激活：
- “会议记录”、“会议笔记”、“会议自动化助手”
- “会议中的行动项”、“会议跟进”
- “处理这份会议记录”、“分析这次会议”
- “从会议中提取决策”、“会议邮件草稿”
- 上传或粘贴 VTT、SRT 或文本格式的会议记录

## 权限

```yaml
permissions:
  exec: true          # Run extraction scripts
  read: true          # Read transcript files
  write: true         # Save history and reports
  network: true       # LLM API calls (Anthropic or OpenAI)
```

## 系统要求

- **bash**, **jq**, **python3**, **curl**（通常已预先安装）
- **ANTHROPIC_API_KEY** 或 **OPENAI_API_KEY** 环境变量

## 代理工作流程

### 第一步：获取会议记录

向用户请求会议记录。可以接受以下方式：
- 提供 VTT、SRT 或 TXT 文件的 **文件路径**
- 直接在对话中粘贴文本
- 上传文件

该功能会自动检测文件格式（VTT、SRT 或纯文本）。

**重要提示：** 该功能不提供音频转录服务。如果用户有音频/视频文件，建议使用以下工具：
- Zoom/Google Meet/Teams 的内置转录功能
- Otter.ai 或 Fireflies.ai 进行录音和转录
- `whisper.cpp` 进行本地转录

### 第二步：获取可选的会议信息

可以询问（但不是必须的）：
- **会议标题**——有助于生成邮件主题和报告标题
- 如果未提供，功能会从文件名中提取或使用 “会议 [日期]” 作为标题

### 第三步：运行自动化处理

如果用户直接粘贴了会议记录，将其保存到临时文件中，然后运行以下脚本：
```bash
bash "$SKILL_DIR/scripts/meeting-autopilot.sh" <transcript_file> --title "Meeting Title"
```

或者通过标准输入（stdin）运行：
```bash
echo "$TRANSCRIPT" | bash "$SKILL_DIR/scripts/meeting-autopilot.sh" - --title "Meeting Title"
```

脚本会自动完成以下三个步骤：
1. **解析**——统一会议记录的格式
2. **提取**——利用大型语言模型（LLM）提取会议中的决策、行动项和问题
3. **生成**——创建邮件草稿、工单草稿和精美的报告

### 第四步：展示报告

脚本会将完整的 Markdown 格式报告输出到标准输出（stdout）。该报告适用于 Slack、邮件或任何支持 Markdown 的平台。

报告内容包括：
- 📊 概览表格（按类别统计）
- ✅ 带有理由的决策
- 📋 行动项表格（负责人、截止日期、状态）
- ❓ 未解决的问题
- 📧 需要跟进的邮件草稿
- 🎫 工单/问题草稿

### Discord v2 的交付方式（OpenClaw v2026.2.14+）

当对话在 Discord 频道中进行时：
- 先发送一份简洁的摘要（包括决策数量、行动项数量、主要负责人），然后询问用户是否需要查看完整报告。
- 确保第一条消息的长度不超过 1200 个字符，并避免在首条消息中显示过长的表格。
- 如果 Discord 提供了相关组件，可以使用以下命令：
  - `Show Action Items`（显示行动项）
  - `Show Follow-Up Email Draft`（显示需要跟进的邮件草稿）
  - `Show Ticket Drafts`（显示待处理的工单草稿）
- 如果没有相关组件，可以用编号列表的形式提供同样的信息。
- 对于较长的报告，每条消息的建议长度不超过 15 行。

### 第五步：提供后续操作建议

在展示报告后，可以提出以下建议：
1. “需要我完善任何邮件草稿吗？”
2. “是否需要调整行动项的分配？”
3. “想将这份报告保存到文件中吗？”
4. “我还可以处理其他会议的记录——这些记录会形成跟踪历史。”

### 错误处理

| 错误情况 | 处理方式 |
|-----------|----------|
| 未设置 API 密钥 | 显示带有设置说明的错误信息 |
| 会议记录太短（少于 20 个字符） | 建议用户粘贴更多内容或检查文件路径 |
| LLM 没有返回结果 | 报告 API 相关问题，并建议用户检查 API 密钥或网络连接 |
| 未提取到任何信息 | 报告“会议可能没有可执行的操作内容”，但仍会显示已提取的关键信息 |
| 文件格式不支持 | 建议将文件格式更改为 TXT 以便进行纯文本解析 |

### 对代理的提示：

- **报告是最重要的部分**——请完整展示报告内容，不要对其进行总结。
- **跟进邮件是关键**——请特别强调这些邮件，因为它们可以直接发送。
- **主动建议**：根据报告内容，提出具体的改进措施。
- **跨会议跟踪**：所有行动项会自动保存到 `~/.meeting-autopilot/history/` 文件夹中。可以告知用户这一点，这是 1.1 版本的功能之一，用于跟踪不同会议中的承诺事项。
- 如果会议记录中没有发言者的标签，建议用户添加 “Speaker: 发言者姓名” 格式以提高信息的准确性。

## 参考文件

- `scripts/meeting-autopilot.sh` — 主要处理脚本（唯一的入口点）
- `scripts/parse-transcript.sh` — 会议记录解析脚本（将 VTT/SRT/TXT 文件转换为 JSONL 格式）
- `scripts/extract-items.sh` — 利用 LLM 提取会议内容
- `scripts/generate-outputs.sh` — 生成操作结果和报告格式化脚本
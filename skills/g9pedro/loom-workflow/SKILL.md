---
name: loom-workflow
description: |
  AI-native workflow analyzer for Loom recordings. Breaks down recorded business processes
  into structured, automatable workflows. Use when:
  - Analyzing Loom videos to understand workflows
  - Extracting steps, tools, and decision points from screen recordings
  - Generating Lobster workflow files from video walkthroughs
  - Identifying ambiguities and human intervention points in processes
---

# Loom 工作流分析器

该工具可将 Loom 录像转换为结构化、可自动化的工作流。

## 快速入门

```bash
# Full pipeline - download, extract, transcribe, analyze
{baseDir}/scripts/loom-workflow analyze https://loom.com/share/abc123

# Individual steps
{baseDir}/scripts/loom-workflow download https://loom.com/share/abc123
{baseDir}/scripts/loom-workflow extract ./video.mp4
{baseDir}/scripts/loom-workflow generate ./analysis.json
```

## 工作流程

1. **下载** - 通过 yt-dlp 下载 Loom 视频
2. **智能提取** - 在场景变化时捕获帧，并记录语音转录的起始时间
3. **转录** - 使用 Whisper 工具进行语音转录，并添加单词级别的时间戳
4. **分析** - 进行多模态 AI 分析（需要视觉模型）
5. **生成** - 生成包含审批节点的工作流文件（格式为 Lobster）

## 智能帧提取

以下情况下会捕获帧：
- **场景变化** - 视觉上有显著变化（使用 ffmpeg 进行场景检测）
- **语音开始** - 新的语音叙述段落开始
- **语音与视觉变化同时发生** - 这些时刻具有较高的价值
- **间隔填充** - 如果连续 10 秒内没有帧被捕获，系统会自动捕获一帧

## 分析输出

分析器生成以下文件：
- `workflow-analysis.json` - 结构化的工作流定义
- `workflow-summary.md` - 便于人类阅读的总结
- `*.lobster` - 可执行的 Lobster 工作流文件

### 模糊性检测

分析器会标记以下内容：
- 不明确的鼠标操作
- 隐含的假设或常识（如“通常的流程”）
- 需要决策的环节（如“取决于...”）
- 缺失的凭证或上下文信息
- 对工具的依赖关系

## 视觉分析步骤

提取数据后，使用生成的提示与视觉模型进行分析：

```bash
# The prompt is at: output/workflow-analysis-prompt.md
# Attach frames from: output/frames/

# Example with Claude:
cat output/workflow-analysis-prompt.md | claude --images output/frames/*.jpg
```

将 JSON 响应保存到 `workflow-analysis.json` 文件中，然后：

```bash
{baseDir}/scripts/loom-workflow generate ./output/workflow-analysis.json
```

## Lobster 工作流的集成

生成的工作流包含以下功能：
- **审批节点** - 用于控制破坏性操作或外部交互
- **LLM 任务** - 用于分类或决策环节
- **恢复令牌** - 用于中断的工作流的继续执行
- **步骤间的 JSON 数据传递** - 确保工作流能够顺畅进行

## 所需软件

- `yt-dlp` - 用于视频下载
- `ffmpeg` - 用于帧提取和场景检测
- `whisper` - 用于音频转录
- 具有视觉分析能力的 LLM（大语言模型） - 用于分析步骤

## 多语言支持

支持多种语言；Whisper 可自动检测并转录音频内容。为了获得最佳分析效果，分析提示应使用视频中的语言。
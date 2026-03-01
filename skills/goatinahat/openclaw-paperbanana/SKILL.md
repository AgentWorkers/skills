---
name: paperbanana
description: >
  使用 PaperBanana 多智能体 AI 流程，可以根据文本描述生成具有学术出版质量的图表（如方法论图、架构图、统计图等）。同时，还可以将这些生成的图表与参考图像进行质量对比。适用场景包括：  
  1. 用户需要生成研究图表、方法论图、系统架构图或流程图；  
  2. 用户希望从 CSV/JSON 数据中创建统计图、条形图或数据可视化图表；  
  3. 用户需要根据参考图像对生成的图表进行评估或评分；  
  4. 用户希望改进或优化已生成的图表。  
  **不适用场景**：  
  - 分析现有图像；  
  - 一般性的图像生成（非学术用途）；  
  - 无明确生成意图的图表或图形讨论。
metadata: {"openclaw":{"emoji":"🍌","homepage":"https://github.com/GoatInAHat/openclaw-paperbanana","primaryEnv":"GOOGLE_API_KEY","requires":{"bins":["uv"]}}}
---
# PaperBanana — 学术图表生成工具

该工具能够根据文本描述生成符合学术出版标准的图表和统计图表。它采用多智能体工作流程（数据检索器 → 图表设计者 → 图表美化工具 → 可视化工具 → 评估工具），并通过迭代优化来提升图表质量。

## 快速参考

### 生成图表
可以使用以下命令生成图表：
```bash
uv run {baseDir}/scripts/generate.py \
  --context "Our framework consists of an encoder module that processes..." \
  --caption "Overview of the proposed encoder-decoder architecture"
```

或者从文件中生成图表：
```bash
uv run {baseDir}/scripts/generate.py \
  --input /path/to/method_section.txt \
  --caption "Overview of the proposed method"
```

**选项：**
- `--iterations N` — 优化迭代次数（默认值：3次）
- `--auto-refine` — 重复优化直到评估工具满意为止（适用于最终成品）
- `--aspect_ratio` — 图表纵横比：`1:1`、`2:3`、`3:2`、`3:4`、`4:3`、`9:16`、`16:9`、`21:9`
- `--provider gemini|openai|openrouter` — 指定使用哪个智能体服务
- `--format png|jpeg|webp` — 输出格式（默认值：png）
- `--no-optimize` — 禁用输入数据的优化处理（默认启用）

### 生成统计图表
可以使用以下命令生成统计图表：
```bash
uv run {baseDir}/scripts/plot.py \
  --data '{"model":["GPT-4","Claude","Gemini"],"accuracy":[92.1,94.3,91.8]}' \
  --intent "Bar chart comparing model accuracy across benchmarks"
```

或者从CSV文件中生成统计图表：
```bash
uv run {baseDir}/scripts/plot.py \
  --data-file /path/to/results.csv \
  --intent "Line plot showing training loss over epochs"
```

### 评估图表
可以使用以下命令评估图表的生成质量：
```bash
uv run {baseDir}/scripts/evaluate.py \
  --generated /path/to/generated.png \
  --reference /path/to/human_drawn.png \
  --context "The methodology section text..." \
  --caption "Overview of the framework"
```

评估标准包括：准确性、可读性、简洁性、美观性。

### 优化现有图表
可以使用以下命令对现有图表进行优化：
```bash
uv run {baseDir}/scripts/generate.py \
  --continue \
  --feedback "Make the arrows thicker and use more distinct colors"
```

### 继续之前的生成过程
可以使用以下命令继续之前的图表生成过程：
```bash
uv run {baseDir}/scripts/generate.py \
  --continue-run run_20260228_143022_a1b2c3 \
  --feedback "Add labels to each component box"
```

## 设置
首次使用时，该工具会通过`uv`自动安装`paperbanana`（https://pypi.org/project/paperbanana/）软件包（仅在本环境中安装，不会全局安装）。该软件包由[llmsresearch](https://github.com/llmsresearch/paperbanana)团队发布在PyPI上。

**所需API密钥：**
该工具至少需要以下一个API密钥才能正常运行。请在`~/.openclaw/openclaw.json`文件中进行配置：

| 环境变量 | 智能体服务 | 费用 | 备注 |
|---|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini | 免费 tier | 建议从免费 tier 开始使用 |
| `OPENAI_API_KEY` | OpenAI | 付费 | 可提供最佳质量的服务（gpt-5.2 + gpt-image-1.5） |
| `OPENROUTER_API_KEY` | OpenRouter | 付费 | 可访问任意模型 |

**自动选择智能体服务的优先级：** Gemini（免费）→ OpenAI → OpenRouter。如果没有找到API密钥，工具会显示错误并退出。

## 智能体服务详情
有关智能体服务的比较、模型选项和高级配置信息，请参阅：
`{baseDir}/references/providers.md`

## 隐私与数据处理
该工具会将用户提供的数据发送到**外部第三方API**以生成和评估图表：
- **文本内容**（上下文描述、图例、反馈信息）会被发送到配置的LLM（大型语言模型）服务（Gemini、OpenAI或OpenRouter）进行处理。
- **生成的图像**可能会被发送回LLM服务进行基于视觉语言模型的评估和优化。
- **用于生成统计图表的CSV/JSON数据**也会被发送到LLM服务以生成相应的图表代码。

**请勿将敏感、机密或专有数据用于此工具**，除非您的组织允许将这些数据发送给配置的智能体服务。所有API请求都会直接发送到智能体服务的端点，不会经过任何中间服务器。

**API密钥的存储与传输：**
API密钥由OpenClaw从您的本地配置文件（`~/.openclaw/openclaw.json`）中获取，不会被记录或传输到其他地方。

## 依赖项与来源
- **PyPI软件包：** `paperbanana`（https://pypi.org/project/paperbanana/）（版本≥0.1.2，通过`uv`自动安装）
- **源代码：** [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana)（在GitHub上）
- **技能源代码：** [GoatInAHat/openclaw-paperbanana](https://github.com/GoatInAHat/openclaw-paperbanana)（在GitHub上）
- **间接依赖项：** `google-genai`、`openai`、`matplotlib`、`Pillow`等（在独立的`uv`环境中安装，不会全局安装）

## 行为说明：
- **输入数据的优化功能默认是开启的**——会在生成图表前对文本进行优化处理并完善图例内容。如需提高生成速度，可以使用`--no-optimize`选项关闭该功能。
- **生成图表所需时间约为1-5分钟**，具体取决于迭代次数和所使用的智能体服务。脚本会显示生成进度。
- **输出结果会自动通过MEDIA协议发送**，无需手动处理文件。
- **继续生成图表的最简单方法是使用`--continue --feedback "..."`命令**。
- **Google Gemini的免费 tier有使用频率限制（约15次/分钟）**。在免费 tier下，建议将迭代次数控制在3次以内。
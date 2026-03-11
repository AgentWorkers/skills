---
name: paperbanana
description: 根据论文中的方法论文本生成具有出版质量的学术图表
license: MIT-0
dependencies:
  env:
    - OPENROUTER_API_KEY (recommended)
    - GOOGLE_API_KEY (alternative)
  runtime:
    - python3
    - uv
---
# PaperBanana

该工具能够根据论文的方法论部分和图表标题生成符合学术出版标准的图表及流程图。PaperBanana通过一个多智能体流程（包括检索器、规划器、样式师和评估器）来生成适用于NeurIPS、ICML、ACL等学术会议的图表。

## 环境配置

```bash
cd <repo-root>
uv pip install -r requirements.txt
```

请通过环境变量或在`configs/model_config.yaml`文件中设置您的API密钥。

**推荐方案1：OpenRouter API密钥** — 该密钥同时用于文本推理和图像生成：
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

**方案2：Google API密钥** — 直接访问Gemini API：
```bash
export GOOGLE_API_KEY="your-key-here"
```

如果同时配置了两种API密钥，系统将默认使用OpenRouter。

## 使用方法

```bash
python skill/run.py \
  --content "METHOD_TEXT" \
  --caption "FIGURE_CAPTION" \
  --task diagram \
  --output output.png
```

## 参数

| 参数          | 是否必填 | 默认值    | 说明                                      |
|---------------|---------|---------|-----------------------------------------|
| `--content`     | 是      |         | 需要可视化的方法论部分文本                         |
| `--content-file`  | 是      |         | 包含方法论文本的文件路径（作为`--content`的替代选项）             |
| `--caption`     | 是      |         | 图表的标题或可视化目的                             |
| `--task`       | 否       | `diagram`   | 任务类型：`diagram`（生成图表）                    |
| `--output`     | 否       | `output.png` | 输出图像文件的路径                             |
| `--aspect-ratio`   | 否       | `21:9`    | 宽高比：`21:9`、`16:9`或`3:2`                         |
| `--max-critic-rounds` | 否       | `3`      | 评估器的最大迭代次数                             |
| `--num-candidates` | 否       | `10`      | 并行生成的候选图表数量                             |
| `--retrieval-setting` | 否       | `auto`     | 检索模式：`auto`、`manual`、`random`或`none`             |
| `--main-model-name` | 否       | `gemini-3.1-pro-preview` | 用于VLM智能体的主模型（由配置的API密钥自动检测）         |
| `--image-gen-model-name` | 否       | `gemini-3.1-flash-image-preview` | 用于图像生成的模型（也支持`gemini-3-pro-image-preview`）         |
| `--exp-mode`     | 否       | `demo_full`   | 流程模式：`demo_full`（包含样式师）或`demo_planner_critic`（不包含样式师） |

*必须至少指定`--content`或`--content-file`中的一个参数。*

当`--num-candidates`大于1时，输出文件的名称格式为`<stem>_0.png`、`<stem>_1.png`等。

## 输出结果

每个保存的图像的绝对路径会逐行输出到标准输出（stdout）。

## 示例

### 图表生成示例

```bash
python skill/run.py \
  --content "We propose a transformer-based encoder-decoder architecture. The encoder consists of 12 self-attention layers with residual connections. The decoder uses cross-attention to attend to encoder outputs and generates the target sequence autoregressively." \
  --caption "Figure 1: Overview of the proposed transformer architecture" \
  --task diagram \
  --output architecture.png
```

## 重要说明

- **运行时间**：根据模型和网络条件的不同，单个候选图表的生成时间通常需要3到10分钟。若同时生成10个候选图表，总耗时约为10到30分钟，请提前做好计划。
- **API调用**：每个候选图表的生成涉及多次大型语言模型（LLM）的调用（包括检索器、规划器、样式师和评估器），这些过程是并行执行的。
- **图像生成**：样式师智能体会调用图像生成模型（Gemini Image）来渲染最终的图表。

## 关于PaperBanana

PaperBanana基于**PaperVizAgent**框架开发，这是一个基于参考文献的多智能体系统，专门用于自动化学术图表的生成。该框架最初是在以下研究论文中提出的：

> **PaperBanana：为AI科学家自动化学术图表生成**  
> 作者：Dawei Zhu, Rui Meng, Yale Song, Xiyu Wei, Sujian Li, Tomas Pfister, Jinsung Yoon  
> 文章链接：arXiv:2601.23265

PaperVizAgent由五个专用智能体组成：检索器、规划器、样式师、视觉师和评估器，它们协同工作将原始的科学内容转化为符合学术出版标准的图表。该工具的性能已在**PaperBananaBench**基准测试中进行了评估。
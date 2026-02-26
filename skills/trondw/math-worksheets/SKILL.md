---
name: math-worksheets
description: 生成专业的数学练习题册及完整的答案解析，以 PDF 格式提供。使用 tectonic（免费工具，无需注册）将 LaTeX 文件编译为 PDF。支持从小学到高中的所有数学主题（预备代数、代数 1/2、几何、预备微积分）。支持坐标平面网格、几何图形、表格以及多部分问题。当用户需要 K-12 阶段的数学练习题、作业帮助资料或答案解析时，可使用该工具。
---
# 数学练习题生成器

该工具可以为任何K-12年级的数学主题生成学生练习题PDF文件以及完整的逐步解答PDF文件。它使用`tectonic`来编译LaTeX代码（无需安装TeX——它会自动下载所需的包）。

## 模型选择（自动）

该功能会自动检测最适合的问题生成模型。`o1`、`o3`、`DeepSeek R1`和`Gemini DeepThink`等推理模型能够逐步解决数学问题，并且出错率远低于标准模型。

模型排名通过三层机制进行更新：
1. **托管的JSON文件**（从GitHub获取，缓存7天）——由维护者根据新模型的发布情况进行更新
2. **捆绑的JSON文件`（references/model-rankings.json`）——随每个功能的更新在ClawhHub上更新
3. **脚本中的硬编码默认值**——作为最后手段，永远不会导致生成错误

若想在不等待功能更新的情况下更新排名，可以直接编辑`references/model-rankings.md`中GitHub上的托管JSON文件。该工具会在7天内识别到这些更改。

**步骤0 — 在执行其他操作之前先运行模型检测：**

```bash
SKILL_DIR="$(dirname "$0")"
result=$(bash "$SKILL_DIR/scripts/check_reasoning_model.sh")
status=$(echo "$result" | awk '{print $1}')   # FOUND, FALLBACK, or NONE
model_alias=$(echo "$result" | awk '{print $2}')
model_full=$(echo "$result" | awk '{print $3}')
```

然后根据检测结果选择合适的模型：

**`FOUND_reasonING`**（`o3`、`o1`、`DeepThink`、`DeepSeek R1`）——最佳选择，用于生成问题：
```
sessions_spawn(task="<problem generation prompt>", model=model_alias)
```
无需任何警告。子代理会生成`.tex`文件并运行验证脚本，然后宣布任务完成。

**`FOUND_STRONG`**（`Claude Opus`）——质量非常高，使用该模型时无需向用户显示警告：
```
sessions_spawn(task="<generation prompt>", model=model_alias)
```
可以选择添加一条提示信息：“使用Claude Opus模型——数学准确性很高，LaTeX格式也非常优秀。对于难度较高的代数2问题，使用`DeepThink`或`o1`模型可能会更合适。”

**`NONE`**——仅使用标准模型；此时需要向用户明确推荐合适的模型：
```
⚠️ No reasoning model or Opus detected. Worksheet generated with [current model].
For best accuracy, especially on multi-step problems, configure one of:
  • Gemini 2.5 Pro DeepThink  — google.generativeai.com (free tier available)
  • o1 / o3                   — platform.openai.com
  • DeepSeek R1               — platform.deepseek.com (very affordable)
  • Claude Opus               — console.anthropic.com
SymPy verification will catch most errors regardless.
```

| 状态 | 可用的模型 | 处理方式 |
|---|---|---|
| `FOUND_reasonING` | `DeepThink`、`o1`、`o3`、`R1` | 静默生成问题，无需警告 |
| `FOUND_STRONG` | `Claude Opus 4.x` | 静默生成问题，可选添加提示信息 |
| `NONE` | `Sonnet`、`Flash`、`GPT-4o` | 使用当前模型，并显示推荐建议 |

## 先决条件

```bash
brew install tectonic   # macOS/Linux — downloads packages on demand
```

输出目录（如需创建）：`~/Documents/Worksheets/`

## 工作流程

### 1. 收集信息

询问用户（或根据上下文推断）：
- **学生信息**：姓名、年级、所学课程（例如：“八年级，预代数”）
- **主题**：例如：“因式分解三项式”、“解二元方程”
- **问题数量**：默认为10道题（如未指定）
- **格式要求**：计时测验、家庭作业练习、混合难度或专题练习

**图片输入快捷方式**：如果用户发送了家庭作业或教科书页面的图片，可以使用`image`工具提取问题类型、格式和难度信息，然后据此生成相应的练习题。

### 2. 设计问题

根据学生的水平设计合适的问题。问题难度应逐步增加。所有问题都必须数学上正确无误——请自行验证答案。

具体问题类型请参考`references/problem-library.md`。

### 3. 编写LaTeX代码

在`/tmp/`目录下编写三个`.tex`文件：
- `ws_TOPIC_DATE.tex` — 学生练习题文件（空白答题区域）
- `ak_TOPIC_DATE.tex` — 答案键文件（包含完整的逐步解答）
- `ss_TOPIC_DATE.tex` — 技能总结/学习指南（帮助文档）

**技能总结**是一份1-2页的参考资料，学生可以在完成练习题或学习时参考。内容包括：
- 每个测试技能对应一个部分（通常有2-5个部分）
- 每个技能对应的公式/规则框（蓝色）——关键事实和公式
- 每个技能对应的示例（绿色）——比练习题更简单的示例
- 可选的注意事项框（橙色）——常见的错误点
- 文末可选的关键词汇部分

具体模板和格式说明请参考`references/latex-templates.md`中的“技能总结/学习指南模板”。

**必备软件包**（每个文件中都需要包含）：
```latex
\usepackage[margin=1in, top=0.75in, bottom=0.75in]{geometry}
\usepackage{amsmath, amssymb}
\usepackage{tikz, pgfplots}
\usepackage{enumitem, fancyhdr, multicol, array, booktabs}
\pgfplotsset{compat=1.18}
```

**页面布局规范**：每个问题之间留出`5cm`的间距；多步骤问题之间留出`8cm`的间距；图表部分留出`10cm`以上的间距。

### 4. 编写并运行验证脚本

在编译之前，编写`/tmp/verify_TOPIC_DATE.json`文件——该文件包含每个问题的描述及其预期答案。`scripts/verify.py`脚本会使用SymPy来验证这些信息。生成的代码不会被执行。

```bash
bash "$SKILL_DIR/scripts/run_verify.sh" /tmp/verify_TOPIC_DATE.json
```

**JSON格式示例：**
```json
{
  "topic": "graphing polynomials",
  "problems": [
    {"id": 1, "type": "solve",  "expr": "x**2 - 5*x + 6",      "expected": [2, 3]},
    {"id": 2, "type": "factor", "expr": "x**2 - 7*x + 12",     "expected": "(x-3)*(x-4)"},
    {"id": 3, "type": "eval",   "expr": "(x-1)*(x+2)", "at": {"x": 0}, "expected": -2},
    {"id": 4, "type": "zeros",  "expr": "x*(x-3)**2",           "expected": [0, 3]},
    {"id": 5, "type": "expand", "expr": "(x+2)**2",             "expected": "x**2 + 4*x + 4"},
    {"id": 6, "type": "manual", "desc": "Graph sketch — verify visually"}
  ]
}
```

**验证类型说明：**

| 验证类型 | 是否需要验证？ | 验证内容 |
|---|---|---|
| `solve` | ✅ | 表达式的根是否与预期列表匹配 |
| `factor` | ✅ | 因式分解后的形式是否与预期一致 |
| `expand` | ✅ | 表达式的展开形式是否与预期一致 |
| `eval` | ✅ | 在给定值下表达式的计算结果是否与预期一致 |
| `zeros` | ✅ | 表达式的零点是否与预期列表匹配 |
| `manual` | 👁 | 需人工审核的问题类型——不会自动失败 |

`manual`类型用于处理图表草图、符号表示、应用题设置和证明等问题。

**如果验证失败（退出程序）**：请修复LaTeX答案键并重新运行。直到答案键正确无误后再进行编译。

### 5. 编译

```bash
SKILL_DIR="$(dirname "$0")"
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ws_TOPIC_DATE.tex ~/Documents/Worksheets/
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ak_TOPIC_DATE.tex ~/Documents/Worksheets/
bash "$SKILL_DIR/scripts/compile.sh" /tmp/ss_TOPIC_DATE.tex ~/Documents/Worksheets/
```

### 6. 发送结果

通过用户请求的相同渠道发送所有三个PDF文件：
- **Telegram**：使用`message`工具发送文件路径（先将其复制到`~/.openclaw/media/outbound/`）
- **iMessage/SMS**：使用`imsg`功能发送文件
- **Email**：使用`gog`功能发送所有文件（作为附件）

建议的发送顺序：先发送技能总结（学习指南），再发送练习题文件，最后发送答案键文件。

**打印说明**：除非用户明确要求，否则不要打印文件。如需打印，请使用`lpr -P <打印机名称>`命令。

## 质量检查清单

在编译之前，请检查每个问题：
- 数学上是否正确（请自行验证答案）
- 问题描述是否清晰明确
- 难度是否符合学生的水平
- 是否包含必要的图表/图形/表格
- 问题类型是否多样化（避免所有问题都是同一类型）

## 文件命名规则

如果知道学生的姓名，请在文件名前加上学生的名字：`leo_ws_...`、`leo_ak_...`、`leo_ss_...`

## 常见问题及解决方法

| 问题 | 解决方法 |
|---|---|
| `tectonic`未找到 | 执行`brew install tectonic`命令安装该工具 |
- 编译速度慢 | 正在从CTAN下载包，请等待30-60秒，之后速度会加快 |
- LaTeX代码出错 | 检查`$...$`之间的匹配是否正确（确保`\begin{}`和`\end{}`匹配）
- `pgfplots`无法渲染 | 确保`\pgfplotsset{compat=1.18}`已在文档开头部分设置 |
- PDF文件未生成 | 查看`tectonic`的输出日志以获取具体错误信息 |
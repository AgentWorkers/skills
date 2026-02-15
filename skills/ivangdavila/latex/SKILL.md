---
name: LaTeX
description: 使用正确的语法、相关软件包以及编译流程来编写 LaTeX 文档。
metadata: {"clawdbot":{"emoji":"📐","os":["linux","darwin","win32"]}}
---

## 特殊字符

- 需要转义的保留字符：`\# \$ \% \& \_ \{ \} \textbackslash`
- 波浪号（tilde）应使用 `\textasciitilde`，而不是 `\~`（后者是用于表示重音的符号）
- 分号（caret）应使用 `\textasciicircum`，而不是 `\^`
- 文本中的反斜杠（backslash）应使用 `\textbackslash`，而不是 `\\`（后者是用于换行的符号）

## 引号与破折号

- 开引号：```` ``，闭引号：`''`——切勿使用普通的单引号 `"`
- 破折号：`-`（短横线），`--`（连字符，用于表示范围，如 1--10），`---`（长破折号，用于标点符号）
- 数学模式中的减号：`$-1$`，而不是文本模式中的 `-1`

## 数学模式

- 内联数学表达式：`$...$` 或 `\(...\)`；显示数学公式时使用 `\[...\]` 或 `equation` 环境
- 数学公式中的文字：`$E = mc^2 \text{ 其中 } m \text{ 是质量}``
- 多行数学公式：使用 `align` 环境，而不是多个 `equation` 命令
- 自动调整大小的括号：使用 `\left( ... \right)`——必须成对使用

## 间距

- 命令后面跟着文本时需要使用 `{}` 或 `\`：例如 `\LaTeX{}` 或 `\LaTeX\ is`
- 不断行空格：在数字和单位之间使用 `~`，例如 `5~km`
- 在数学公式中设置不同的间距：`\,`（表示较细的间距），`\:`（表示中等间距），`\;`（表示较粗的间距），`\quad`（表示较宽的间距），`\qquad`（表示非常宽的间距）

## 包（Packages）

- 包的安装顺序很重要——`hyperref` 通常应该放在最后安装
- 为了支持 UTF-8 编码，需要同时安装 `inputenc` 和 `fontenc`：`\usepackage[utf8]{inputenc}` `\usepackage[T1]{fontenc}`
- `graphicx` 用于处理图片，`booktabs` 用于制作专业的表格，`amsmath` 用于高级数学公式
- `microtype` 可以改善文本排版效果——建议尽早加载，虽然效果微妙但非常重要

## 浮动元素（图表与表格）

- `[htbp]` 用于指定浮动元素的位置：这里、顶部、底部或页面——这些不是命令
- LaTeX 可能会将浮动元素放置在距离源代码较远的位置——可以使用 `float` 包中的 `[H]` 来强制调整位置
- 在浮动元素内部始终使用 `\centering` 环境，而不是 `center` 环境
- 标签（caption）应该放在 `\label` 之前——标签会引用最后一个被编号的元素

## 参考文献

- 需要编译两次才能正确处理 `\ref` 和 `\pageref`——第一次编译用于收集引用信息，第二次编译用于生成引用链接
- `label` 应该紧跟在 `\caption` 之后，或者放在被标记的环境内部
- 对于参考文献的生成：需要执行四次编译步骤：`latex → bibtex → latex → latex`
- `hyperref` 可以使参考文献链接可点击——但某些包可能会影响其正常工作

## 表格

- `tabular` 用于创建内联表格，`table` 用于创建带标题的浮动表格
- 使用 `booktabs` 包来设置表格格式：`\toprule`、`\midrule`、`\bottomrule`——不要使用垂直线
- 使用 `@{}` 可以去除表格的边框：`\begin{tabular}{@{}lll@{}}`
- 多列表格：`\multicolumn{2}{c}{Header}`；多行表格需要 `multirow` 包

## 图片

- 图片的路径应该是相对于主文档的路径，或者使用 `\graphicspath{{./images/}}` 来指定路径
- 对于 pdflatex/latex 文档，建议使用 PDF 或 EPS 格式的图片；对于照片，可以使用 PNG 或 JPG 格式的图片
- 使用 `\includegraphics[width=0.8\textwidth]{file}` 来插入图片——通常不指定文件扩展名会更好

## 常见错误

- 满格的文本框（hbox）：文本太长——可以重新组织句子，添加 `-` 来帮助换行，或者使用 `\sloppy` 选项来放宽排版规则
- 缺少 `$` 符号：可能在文本模式下使用了数学命令
- 未定义的控制序列：可能是拼写错误或缺少相应的包
- `include` 命令会插入换行符，`input` 命令则不会——对于较小的图片片段，应该使用 `input` 命令

## 文档结构

- 在 `\begin{document}` 之前添加文档前言（preamble），其中包含所有的 `usepackage` 命令和设置
- 如果使用了 `\title`、`\author`、`\date` 等命令，应在 `\begin{document}` 之后添加 `\maketitle` 函数
- `article` 适用于简短的文档，`report` 适用于没有章节的文档，`book` 适用于完整的书籍
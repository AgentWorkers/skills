---
name: paper-polish
description: 这项技能帮助代理审查和润色用 LaTeX 编写的科研论文，重点关注论文的写作清晰度、语法规范、LaTeX 的最佳实践以及文档结构。
metadata:
  short-description: fixing writing errors in academic papers

---# 使用 LaTeX 优化和审阅研究论文

## 关于写作

### 内容要点

- 你的论文应该能够让审稿人轻松理解。他们对你的工作了解得远不如你，可能不是该领域的专家，也可能没有太多时间来仔细审阅你的论文。
- 引言部分应当激发读者的兴趣或好奇心（无论是新问题、新解决方案、改进的解决方案、令人印象深刻的结果，还是高影响力），同时要说明研究设计的新颖性、实质性和正确性，以及评估的相关性和全面性。
- 简洁性：删除所有无意义的词语，例如“kind of”。
- 使用正确的时态：
  - [1](https://www.unlv.edu/sites/default/files/page_files/27/GradCollege-VerbTenseScientificManuscripts.pdf)
  - [2](https://berks.psu.edu/sites/berks/files/campus/VerbTense_Handout.pdf)
  - [3](https://www.nature.com/scitable/topicpage/effective-writing-13815989/)

### 语法

- 节标题的字母大小写应保持一致：
  - 大写开头和结尾的单词以及中间的所有重要单词。
    - 例如：**Introduction to Fuzzing with LLMs**（《使用 LLM 进行模糊测试的介绍》）
  - 句子首词和专有名词应大写。
    - 例如：**Introduction to Fuzzing with LLMs**（《使用 LLM 进行模糊测试的介绍》）
  - 选择一种风格并在整篇论文中保持一致。

- 除非有充分的理由，否则避免使用被动语态。被动语态容易引起歧义，因为它没有明确的主语（除非后面跟着“by...”）。
  - 错误示例：**LLM was applied to fuzzing.**（谁应用了 LLM？是作者还是其他人？）
  - 正确示例：**We applied LLM to fuzzing.**（我们应用了 LLM 进行模糊测试。）

- 避免使用名词化（Nominalization）。
  - 错误示例：**He made a proposal to use Rust.**（他提出了使用 Rust 的建议。）
  - 正确示例：**He proposed to use Rust.**（他提议使用 Rust。）

- 避免使用“there is/are”这样的表达。
  - 错误示例：**There are many developers of Rust.**（有很多 Rust 开发者。）
  - 正确示例：**Many developers use Rust.**（许多开发者使用 Rust。）
  - 正确示例：**Rust has many developers.**（Rust 拥有大量的开发者。）

- “which”与“that”的用法：在非限制性从句中使用“which”，在限制性从句中使用“that”。
  - 错误示例：**Rust that is safe is popular.**（这种安全的 Rust 很受欢迎。）（这是错误的，因为 Rust 只有一种。）
  - 正确示例：**Rust, which is safe, is popular.**（这种安全的 Rust 很受欢迎。）

- 区分并列连词（coordinating conjunctions）和连接副词（conjunctive adverbs）：
  - 错误示例：**C is dangerous, Rust is safe.**（C 很危险，Rust 很安全。）（不能用逗号连接两个句子。）
  - 正确示例：**C is dangerous, but Rust is safe.**（C 很危险，但 Rust 很安全。）
  - 错误示例：**C is dangerous, however Rust is safe.**（C 很危险；然而 Rust 很安全。）
  - 正确示例：**C is dangerous; however, Rust is safe.**（C 很危险；然而 Rust 很安全。）

- “fewer”修饰可数名词，“less”修饰不可数名词。
  - 错误示例：**ten items or less**（十个或更少的物品）
  - 正确示例：**ten items or fewer**（十个或更少的物品）
  - 错误示例：**fewer feedback**（更少的反馈）
  - 正确示例：**less feedback**（更少的反馈）

- 正确使用冠词（`a`、`an`、`the`）：
  - 单数可数名词前必须使用冠词。
    - 错误示例：**I wrote Rust program.**（我编写了一个 Rust 程序。）
    - 正确示例：**I wrote a Rust program.**（我编写了一个 Rust 程序。）
    - 正确示例：**I wrote Rust programs.**（我编写了多个 Rust 程序。）
  - “the”必须指代在事实或上下文中唯一的事物。
    - 正确示例：**The first Rust programmer**（第一个 Rust 开发者）（在事实上是唯一的）
    - 正确示例：**Our team has a Rust and a C++ programmer.**（我们的团队中有一名 Rust 开发者和一名 C++ 开发者。Rust 开发者编写出的代码速度更快、更可靠。）
    - 错误示例：**Our team has two Rust and two C++ programmers.**（我们的团队中有两名 Rust 开发者和两名 C++ 开发者。）
    - 正确示例：**The Rust programmer produces the fastest, most robust code.**（Rust 开发者编写出的代码速度更快、更可靠。）

- 区分“compare with”和“compare to”：
  - 正确示例：**Rust is safer compared with C.**（与 C 相比，Rust 更安全。）
  - 正确示例：**Some people compare Rust to a panacea for memory safety problems.**（有些人将 Rust 视为解决内存安全问题的灵丹妙药。）

## 关于 LaTeX

- 使用现代版本的 LaTeX，以便充分利用 Unicode 和其他实用功能。
  - 使用 [LuaLaTeX](https://www.luatex.org/) 而不是 LaTeX 或 pdfLaTeX。
  - 对于 `acmart` 和 `ieeetrans` 模板，使用 [BibLaTeX](https://www.overleaf.com/learn/latex/Bibliography_management_with_biblatex) 而不是 BibTex。

- 使用正确的字体：
  - 特别是，变量应该使用斜体（_italics_），但描述性术语不应使用斜体。
  - 错误示例：**$t_{max}$**（错误）
  - 正确示例：**$t_\text{max}$**（正确的斜体形式）

- 不要手动添加大数字的分隔符。只需使用 `\usepackage{siunitx}`，然后将大数字用 `\num{}` 包装起来。
  - 错误示例：**12,345**（错误）
  - 正确示例：**\num{12345}$（正确的格式）

- 不要手动输入参考文献的名称（如 Table、Figure、Theorem）。可以使用 `\usepackage{hyperref}`，然后使用 `\autoref{fig:xxx}`、`\autoref{sec:xxx}`、`\autoref{table:xxx}`。
  - 不推荐的做法：**In Figure~\ref{fig:overview}**（错误）
  - 正确的做法：**In \autoref{fig:overview}**（正确的引用方式）

## 结构

- `main.tex` 是 LaTeX 项目的入口文件，包含 `usepackage` 命令和文档结构。
- `src/` 目录下包含所有章节。
- `tables/` 目录下包含所有表格。
- `figures/` 或 `fig/` 目录下包含图表（图表可以是 PDF 文件或 `.tex` 文件；`.tex` 文件通常包含算法实现）。
- `code/` 目录下包含正文中使用的代码示例。
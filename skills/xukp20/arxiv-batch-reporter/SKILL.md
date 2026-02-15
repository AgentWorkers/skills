---
name: arxiv-batch-reporter
description: "构建最终的集合报告分为两个步骤：首先，模型会生成报告模板；接着，脚本会根据 `arXiv-id` 占位符从 `summary.md` 文件中提取每篇论文的“简要结论”（Brief Conclusion）和论文的完整 URL（abs URL），并将这些信息插入到报告模板中。"
---

# ArXiv批量报告生成工具

请在每篇论文的`summary.md`文件生成完成后使用此工具。

## 核心原理

该模型负责编写报告的结构框架，而脚本则负责插入每篇论文的结论文本。

## 限制条件

- 最终报告中的每篇论文的结论文本必须直接来源于该论文`summary.md`文件中的`## 10. 简要结论`部分。
- 不得对每篇论文的结论文本进行改写或意译。

## 命令流程

步骤1：构建模型所需的上下文数据包。  
```bash
python3 scripts/collect_summaries_bundle.py \
  --base-dir /path/to/run-dir \
  --language English
```

步骤2：模型使用占位符在`base-dir`目录下生成`collection_report_template.md`模板文件。  
步骤3：根据模板生成最终报告。  
```bash
python3 scripts/render_collection_report.py \
  --base-dir /path/to/run-dir \
  --template-file collection_report_template.md \
  --output-file collection_report.md \
  --language English
```

## 语言参数

- `--language`参数用于控制报告生成时使用的标签语言。  
- 需要为每次运行手动设置该参数；若省略则默认使用英语（`English`）。  
- 支持的语言别名为：`Chinese`、`zh`、`zh-cn`、`中文`。  
- 当选择非英语语言时（例如中文），生成的标签和提示内容会进行本地化处理。

## 模板中的占位符语法

在每个论文的条目中，需添加一条包含ArXiv论文ID的占位符行。  
支持的占位符语法（单独的占位符行）如下：  
```text
{{ARXIV_BRIEF:2602.12276}}
```

`render_collection_report.py`脚本会将这条占位符行替换为：  
- 从论文`summary.md`的`10`部分提取的简要结论文本；  
- 生成的论文PDF链接：`https://arxiv.org/abs/<arxiv_id>`  

**备用规则**：如果`10`部分的标题缺失，将使用该部分下最后一个`##`标题下的内容作为替代。

## 输出结果

- `<base-dir>/summaries.bundle.md`：包含所有论文的摘要文件。  
- `<base-dir>/collection_report_template.md`：由模型生成的报告模板文件。  
- `<base-dir>/collection_report.md`：最终渲染完成的报告文件。  

请参考`references/report-format.md`文件以了解预期的报告结构。  
示例报告结构文件包括：`references/report-example-lean4-en.md`、`references/report-example-llm-math-en.md`和`references/report-example-multimodal-en.md`（这些文件使用了符合代码规范格式化的示例报告）。  

## 相关技能

此工具是`arxiv-summarizer-orchestrator`的子技能。  
它应在以下步骤之后执行：  
1. `arxiv-search-collector`（收集论文目录及元数据）  
2. `arxiv-paper-processor`（生成每篇论文的`summary.md`文件）  

该工具会使用步骤2生成的摘要内容，并与步骤1和步骤2协同工作，以生成最终的集合报告。
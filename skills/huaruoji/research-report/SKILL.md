---
name: research-report
description: "研究技术项目/论文，并生成可导出为PDF的综合性报告。提供两种模式：**lite**（仅包含分析和撰写）和**full**（包含环境搭建及实验）。支持以下参数：`iterations`（迭代次数）、`mode`（模式）、`project-path`（项目路径）和`output`（输出格式）。该工具适用于论文分析、代码审查、技术报告撰写及研究文档整理。"
metadata: {"openclaw": {"requires": {"bins": ["pandoc"]}, "primaryEnv": "", "emoji": "📝"}}
---
# 研究报告生成器

该工具能够分析技术项目/论文，并生成包含PDF输出的综合性报告。

## 模式

### 简易模式（默认模式）
- 文献搜索 + 论文分析
- 代码阅读（本地或远程）
- 多轮报告编写
- 通过 `md2pdf` 工具生成PDF
- **无需环境设置或实验执行**

### 完整模式
- 简易模式的所有功能 +
- 设置 Conda/虚拟环境
- 安装依赖项
- 运行实验
- 分析实验结果

## 使用方法

```bash
bash {baseDir}/scripts/research-report.sh \
  --topic "Spatial Forcing" \
  --mode lite \
  --iterations 3 \
  --output both
```

## 参数

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| `--topic` | （必填） | 论文/项目名称或arXiv ID |
| `--mode` | `lite` | `lite` 或 `full` |
| `--iterations` | `3` | 报告修订次数 |
| `--output` | `both` | `md`, `pdf`, 或 `both` |
| `--project-path` | （自动） | 本地代码目录（可选） |
| `--workspace` | （当前目录） | 工作区目录 |

## 工作流程

### 第1阶段：发现
1. 在arXiv和项目页面上搜索相关内容
2. 获取相关论文（包括引用和参考文献）
3. 确定关键技术及依赖项

### 第2阶段：分析
1. （如果提供了 `--project-path`）阅读源代码
2. 从文档和代码中分析系统架构
3. 映射技术栈

### 第3阶段：报告编写（进行多轮迭代）
1. 起草报告大纲
2. 分阶段编写各部分内容
3. 添加图表（使用Mermaid/ASCII格式）
4. 优化解释说明

### 第4阶段：导出（仅限完整模式）
1. 设置Conda环境
2. 安装依赖项
3. 运行实验
4. 将实验结果添加到报告中

### 第5阶段：PDF生成
1. 调用 `md2pdf` 工具进行PDF转换
2. 通过Telegram将报告发送给用户

## 输出结构

```
<workspace>/
├── reports/
│   ├── <topic>_report_v1.md
│   ├── <topic>_report_v2.md
│   ├── <topic>_report_final.md
│   └── <topic>_report_final.pdf
├── memory/YYYY-MM-DD.md (appended)
└── logs/<topic>_research.log
```

## 报告模板

生成的报告遵循以下结构：

1. **执行摘要** - 100字的概述
2. **背景** - 问题陈述及重要性说明
3. **技术背景** - 相关知识的直观解释
4. **核心方法** - 详细的技术实现过程及类比说明
5. **代码分析** - 关键代码文件的讲解
6. **实验结果** - 实验设置及结果展示（仅限完整模式）
7. **故障排除** | 常见问题及解决方法
8. **参考文献** - 相关论文、代码仓库及文档的链接

## 所需依赖项

**必备依赖项：**
- pandoc（用于PDF输出）
- texlive-xetex（支持中文排版和数学公式）

**仅限完整模式：**
- conda/miniconda
- CUDA工具包（如需进行GPU实验）

## 集成

该工具会自动执行以下操作：
- 使用 `md2pdf` 工具进行PDF转换
- 将生成的报告文件保存到 `memory/YYYY-MM-DD.md` 文件中
- 创建结构化的报告目录

## 示例

**简易模式，5轮迭代：**
```bash
research-report --topic "VGGT" --iterations 5 --mode lite
```

**使用本地代码的完整模式：**
```bash
research-report --topic "Spatial Forcing" \
  --project-path ~/Spatial-Forcing/openvla-SF \
  --mode full \
  --iterations 3
```

**仅生成PDF：**
```bash
research-report --topic "OpenVLA" --output pdf
```

## 故障排除

| 故障现象 | 解决方法 |
|---------|-------------------|
| PDF生成失败 | 检查 `pandoc --version` 的版本；安装 `texlive-xetex` |
| 中文字符显示问题 | 安装 `fonts-noto-cjk`；使用 `fc-list :lang=zh` 验证字符显示 |
| 数学公式无法显示 | 确保Markdown中使用 `$...$` 或 `$$...$$` 格式 |
| 完整模式下的Conda环境无法启动 | 先运行 `conda update -n base conda`
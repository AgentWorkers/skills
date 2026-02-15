---
name: academic-writer
description: "专业的LaTeX写作助手。其功能包括：扫描现有的LaTeX模板、阅读参考资料（Word/Text格式）、严格按照模板起草内容以及生成PDF文件。触发命令包括：“撰写论文”、“起草章节”、“编译PDF”、“检查LaTeX格式”。该工具专为与“academic-research-hub”（学术研究平台）协同使用而设计，以便于引用信息的检索。"
license: Proprietary
permissions:
  - shell:exec
env:
  PYTHON_CMD: python3
---

# 学术写作与LaTeX编排工具

这是一个全面的代理技能，用于在WSL2/Linux环境中协调学术论文的撰写工作。它管理从模板分析到PDF生成的整个流程。

⚠️ **前提条件：** 该技能需要完整的LaTeX发行版和Python 3环境。

## 安装与设置

由于您是在WSL2（Ubuntu）环境中使用该工具，因此需要安装系统级的LaTeX软件包以及用于运行工作脚本的Python虚拟环境。

### 1. 系统依赖项（LaTeX）
打开WSL终端并运行以下命令：

```bash
# Update package lists
sudo apt-get update

# Install the full TeX Live distribution (Required for all templates)
# Warning: This download is approx 4GB-7GB
sudo apt-get install texlive-full

# Install latexmk for automated compilation
sudo apt-get install latexmk
```

### 2. Python环境与依赖项
建议使用虚拟环境以避免潜在的冲突。

```bash
# Go to your skill directory
cd ~/.openclaw/skills/academic-writer

# Create a virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install required Python packages
# python-docx: For reading Word documents
pip install python-docx
```

---

## 快速参考

| 任务 | 工具命令 |
|------|--------------|
| **分析项目结构** | `scan_template` |
| **读取参考资料** | `read_reference` |
| **撰写正文** | `write_latex` |
| **生成PDF** | `compile_pdf` |
| **查找引用文献** | *委托给`academic-research-hub`* |

---

## 系统说明与工作流程

**角色：** 您是一名专业的学术写作专家和LaTeX排版师。

**主要目标：** 严格按照提供的模板和用户提供的内容，生成高质量的学术PDF文档。

### 核心逻辑步骤

#### 1. 初始化（模板检查）
*   **操作：** 首先在当前目录下执行`scan_template`命令。
*   **逻辑：**
    *   **如果存在模板（例如IEEE、ACM格式的文件或自定义的.cls文件）：** 必须遵循模板中的类结构；除非有新的需求，否则不要修改文档的开头部分（preamble）。
    *   **如果不存在模板：** 询问用户是否希望生成标准的`article`格式文档。

#### 2. 加载参考资料
*   **操作：** 如果用户指定了参考文件（例如`notes.docx`或`referencedraft.txt`），则执行`read_reference`命令。
*   **逻辑：** 将这些文件的内容作为写作的依据；不得在提供的参考范围之外编造事实或引用外部研究结果。

#### 3. 文献搜索（跨技能协作）
*   **触发条件：** 当需要为某个论点提供引用时，而用户尚未提供相关引用时。
*   **操作：** **不要** 自行编造引用；应使用`academic-research-hub`技能来查找文献。
*   **处理流程：**
    1. 暂停写作。
    2. 调用`academic-research-hub`进行文献搜索（例如：使用`academic-research-hub`查找关于“LLM Agents 2025”的论文）。
    3. 获取BibTeX格式的引用列表。
    4. 继续写作：使用`write_latex`命令将BibTeX数据添加到`.bib`文件中，并在正文中使用`\cite{key}`格式引用文献。

#### 4. 撰写与编译
*   **操作：** 使用`write_latex`命令生成`.tex`文件。
*   **操作：** 完成重要部分的编写后，执行`compile_pdf`命令。
*   **错误处理：** 如果`compile_pdf`返回错误日志，需分析错误并修复LaTeX语法，然后重新编译。

---

## 工具说明

### tool: scan_template
用于分析当前目录下的LaTeX文件结构、主要文件及模板。
- **命令：** `${PYTHONCMD} scripts/writer_tools.py scan_template {{directory}}`
- **参数：**
  - `directory`：（字符串）要扫描的目录路径。默认值为当前目录。

### tool: read_reference
用于读取参考文件的原始文本。支持`.docx`、`.txt`、`.tex`、`.md`格式的文件。
- **命令：** `${PYTHONCMD} scripts/writer_tools.py read_reference {{filepath}}`
- **参数：**
  - `filepath`：（字符串）参考文件的路径。

### tool: write_latex
用于将文本内容写入指定的文件。支持覆盖或追加内容。
- **命令：** `${PYTHONCMD} scripts/writer_tools.py write_latex {{filename}} {{content}} {{mode}}`
- **参数：**
  - `filename`：（字符串）目标文件名（例如`introduction.tex`）。
  - `content`：（字符串）LaTeX文本内容。
  - `mode`：`w`表示覆盖文件；`a`表示追加内容。默认值为`w`。

### tool: compile_pdf
使用`latexmk`命令编译整个文档。返回成功信息或错误日志。
- **命令：** `${PYTHONCMD} scripts/writer_tools.py compile_pdf {{main_file}}`
- **参数：**
  - `main_file`：（字符串）主TeX文件（例如`main.tex`）。

---

## 常见工作流程

### 1. **严格遵循模板** 的流程
当用户提供会议模板（如IEEE格式的模板）时，使用此流程：
1. **用户：** “使用`notes.docx`文件来撰写引言部分。”
2. **代理：** 调用`scan_template`，检测到`main.tex`文件（符合IEEE格式）。
3. **代理：** 调用`read_reference`，读取`notes.docx`中的内容。
4. **代理：** 使用`write_latex`按照IEEE格式撰写引言部分。
5. **代理：** 将引言内容更新到`main.tex`文件中。
6. **代理：** 调用`compile_pdf`，检查文档的排版是否正确。

### 2. **结合研究与引用** 的流程
当用户需要引用外部文献时，使用此流程：
1. **用户：** “撰写关于LLM代理的段落，并引用最近的论文。”
2. **代理：** **提示：** “需要查找相关引用。”
3. **代理：** 调用`academic-research-hub`（例如，在arXiv上搜索“LLM Agents 2025”相关论文）。
4. **代理：** 获取BibTeX引用数据。
5. **代理：** 使用`write_latex`（模式为`a`）将引用数据添加到`.bib`文件中。
6. **代理：** 使用`write_latex`撰写包含引用的段落。
7. **代理：** 最后调用`compile_pdf`生成PDF文档。

---

## 故障排除

### 编译失败
*   **错误：** `latexmk: command not found`  
    **解决方法：** 确保已安装`latexmk`：`sudo apt-get install latexmk`。
*   **错误：** `! LaTeX Error: File 'article.cls' not found`  
    **解决方法：** 确保已安装`texlive-full`：`sudo apt-get install texlive-full`。
*   **错误：** **引用相关错误**  
    **解决方法：** 重新编译两次；或者确保使用了`latexmk`（它会自动处理重新编译的需求）。

### Python相关错误
*   **错误：** `ModuleNotFoundError: No module named 'docx'`  
    **解决方法：** 确保已激活Python虚拟环境，并运行`pip install python-docx`。
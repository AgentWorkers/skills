---
name: latex-writer
description: >
  **功能说明：**  
  该工具能够根据预设的模板生成专业的LaTeX文档，适用于多种文档类型，包括学术论文（IEEE/ACM格式）、中文学位论文（CTeX格式）、个人简历（moderncv格式）以及自定义模板。生成的文档可自动编译为PDF格式。  
  **主要特点：**  
  1. **多文档类型支持**：支持生成IEEE/ACM格式的学术论文、CTeX格式的中文学位论文、moderncv格式的个人简历等多种类型的LaTeX文档。  
  2. **模板定制**：用户可以根据自身需求定制文档模板。  
  3. **自动编译**：支持将生成的LaTeX文档自动编译为PDF格式，方便用户直接使用。  
  **适用场景：**  
  - **学术写作**：适用于撰写IEEE/ACM标准的学术论文。  
  - **学术交流**：适用于提交给学术期刊或会议的论文。  
  - **个人简历**：适用于制作专业的个人简历。  
  - **文档管理**：适用于整理和分享个人或团队的技术文档。  
  **使用说明：**  
  - **模板选择**：从预设的模板库中选择适合您需求的模板。  
  - **内容填充**：根据模板要求填写相应的文本和代码示例。  
  - **编译输出**：点击按钮即可将文档编译为PDF格式。  
  **技术优势：**  
  - **高效生成**：利用自动化流程快速生成高质量文档。  
  - **格式统一**：确保所有文档遵循统一的格式规范。  
  - **易于维护**：模板和代码易于更新和管理。  
  **示例文档：**  
  - **IEEE/ACM格式论文**：适用于撰写符合IEEE/ACM标准的学术论文。  
  - **CTeX格式论文**：适用于撰写中文学位论文。  
  - **moderncv格式简历**：适用于制作专业的个人简历。  
  **注意事项：**  
  - 请确保您已安装LaTeX及相关软件（如TeX Live、PDFLaTeX等）。  
  - 请仔细阅读并遵循模板中的编写指南。  
  **下载链接：**  
  [点击此处下载工具](...)  
  **支持语言：**  
  - **中文（简体）**  
  - **英文**  
  **版本更新：**  
  [请访问官方网站查看最新版本信息](...)
version: 1.0.0
author: OpenClaw
---
# LaTeX Writer

这是一个智能的LaTeX文档生成工具，支持模板管理和PDF格式的输出。

## 主要功能

- 📄 **学术模板**：IEEE、ACM、Springer、Elsevier等机构的官方模板
- 📝 **中文支持**：支持使用CTEX格式编写中文论文和报告
- 👤 **简历/求职信**：提供moderncv和altacv等模板
- 🎨 **自定义模板**：用户可以导入自己的`.cls`文件来定制文档格式
- 🔧 **自动编译**：支持使用xelatex/lualatex进行编译，并具备错误处理功能
- 📊 **图表支持**：能够自动将Markdown格式的表格转换为LaTeX格式的图表

## 使用场景

- 当用户需要按照特定格式撰写论文时
- 当用户提到“LaTeX”、“PDF”或“排版”时
- 当用户需要生成简历或求职信时
- 当用户提供内容并希望获得专业的排版服务时

## 使用示例

### 学术论文
```
User: 帮我写一篇 IEEE 格式的机器学习论文，主题是深度学习在医学影像中的应用

Skill Actions:
1. Select IEEEtran template
2. Generate structure: Abstract → Intro → Method → Experiments → Conclusion
3. Ask user for key content points
4. Generate LaTeX with proper math formulas
5. Compile to PDF
```

### 中文论文
```
User: 我要写硕士毕业论文，学校要求用 LaTeX

Skill Actions:
1. Select CTeX template (ctexrep)
2. Configure Chinese fonts (SimSun, SimHei)
3. Setup school-specific requirements
4. Generate chapter structure
```

### 简历生成
```
User: 帮我生成一份软件工程师的英文简历

Skill Actions:
1. Select moderncv template (banking style)
2. Collect user information
3. Format with proper sections
4. Generate PDF
```

## 实现细节

具体实现代码位于`scripts/`目录中：
- `latex_writer.py`：程序的主入口文件
- `template_manager.py`：负责管理各种模板文件
- `content_parser.py`：解析用户输入的内容并转换为结构化的数据
- `latex_generator.py`：生成LaTeX代码
- `pdf_builder.py`：将LaTeX代码编译成PDF格式的文件

## 系统要求

- Python 3.10及以上版本
- 需要安装TeX Live或MiKTeX（并确保安装了xelatex）
- 需要安装支持中文显示的CJK字体
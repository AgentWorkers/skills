---
name: paper-fetcher
description: 根据给定的 DOI，从 Sci-Hub 获取学术论文。自动下载 PDF 文件，并将它们保存到 `research/papers/` 目录中，文件名会经过统一处理（即去除特殊字符和空格）。当用户提供 DOI 或从 PubMed 请求论文时，可使用此功能。
---

# 论文获取工具

该工具可自动从 Sci-Hub 网站检索学术论文。

## 使用方法

**单篇论文获取：**
```
Get paper: 10.1038/nature12345
```

**多篇论文获取：**
```
Fetch these papers:
- 10.1016/j.cell.2023.01.001
- 10.1038/s41586-2023-06789-0
- 10.1126/science.abc1234
```

**获取论文时附带上下文信息：**
```
Get the epitalon paper: 10.1007/s12603-011-0032-7
```

## 功能概述

1. 接收 DOI（数字对象标识符）作为输入。
2. 访问 https://www.sci-hub.su/DOI 以下载论文的 PDF 文件。
3. 将 PDF 文件保存到 `research/papers/` 目录中，并生成规范的文件名。
4. 返回文件保存的路径以确认操作成功。

## 文件保存位置

```
workspace/
└── research/
    └── papers/
        ├── paper_10.1038_nature12345.pdf
        ├── paper_10.1016_j.cell.2023.01.001.pdf
        └── ...
```

## 文件名格式

文件名格式为：`paper_[DOI（其中斜杠已被替换）].pdf`

**示例：**
- DOI: `10.1038/nature12345` → 文件名：`paper_10.1038_nature12345.pdf`
- DOI: `10.1016/j.cell.2023.01.001` → 文件名：`paper_10.1016_j.cell.2023.01.001.pdf`

## 工作流程

当用户提供 DOI 时：

1. **提取 DOI**：从用户提供的信息中解析 DOI（包括或不包括 `https://doi.org/` 前缀）。
2. **访问 Sci-Hub**：使用浏览器访问 `https://www.sci-hub.su/DOI`。
3. **下载 PDF**：等待页面加载后找到下载链接，并将 PDF 文件保存到 `research/papers/` 目录中。
4. **确认结果**：返回文件保存的路径以确认操作成功。

## 错误处理

- **如果论文在 Sci-Hub 上不存在**：
  - 报告无法找到该论文，并提示用户检查 DOI 的格式。
  - 用户可以选择手动搜索论文。
- **如果下载失败**：
  - 报告下载错误，并提供 Sci-Hub 的网址以便用户手动下载论文。

## 集成方式

- **与 Obsidian Sync 集成**：
  - 论文会保存在 `research/papers/` 目录中。
  - 可以创建包含 PDF 链接的笔记，并将元数据同步到 Obsidian 文档库中。
- **与 Research Automation 集成**：
  - 自动获取研究过程中发现的论文，构建参考文献库，并实现与相关协议的交叉引用。

## 使用提示

- **如何获取 DOI**：
  - 在 PubMed 文章详情中可以找到 DOI。
  - 论文本身的页面上通常也会显示 DOI。
  - 在 Google Scholar 中，DOI 通常位于引用信息中。
- **文件名格式兼容性**：
  - 带有 `https://doi.org/` 前缀的 DOI（如 `https://doi.org/10.1038/nature12345`）和没有前缀的 DOI（如 `10.1038/nature12345`）均支持。
- **批量下载**：
  - 可以一次性提交多个 DOI，系统会依次处理这些请求，并将所有下载的论文保存到 `research/papers/` 目录中。

---

**当前状态：** 正在运行中  
**Sci-Hub 网站地址：** https://www.sci-hub.su  
**文件保存路径：** `research/papers/`
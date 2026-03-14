---
name: nested-pdf-merger
description: 当需要将嵌套目录树中的多个 PDF 文件合并为一个包含层次化书签的单一 PDF 文件时，请使用此技能。该技能依赖于已安装的 `nestedpdfmerger` 工具，并确保该工具位于系统的 PATH 环境变量指定的路径中。
metadata: {"openclaw":{"requires":{"bins":["nestedpdfmerger"]},"homepage":"https://github.com/Lyutenant/nested-pdf-merger"}}
---
# 嵌套PDF合并工具

该仓库封装了外部`nestedpdfmerger`命令行工具（CLI）。

**注意：**  
- 请勿在此仓库中实现PDF合并逻辑；  
- 请勿修改`reference/`目录下的任何文件。  

## 使用要求  
使用此工具前，需确保`nestedpdfmerger`命令已安装，并且其路径已添加到系统的`PATH`环境变量中。  

**推荐的安装命令：**  
```bash
pip install nestedpdfmerger
```  

**推荐的CLI入口点：**  
```bash
nestedpdfmerger INPUT_DIR -o OUTPUT.pdf [options]
```  

**其他调用方式：**  
```bash
python -m nestedpdfmerger INPUT_DIR -o OUTPUT.pdf [options]
```  

## 使用场景  
- 当用户需要将多个PDF文件从文件夹结构中合并为一个输出PDF文件时。  
- 希望在合并过程中保留文件夹的层级结构（作为PDF书签）。  
- 可使用`--dry-run`选项预览合并顺序。  
- 可选择排除某些文件夹、调整文件排序顺序或禁用书签功能。  

## 工作流程：  
1. 确认输入目录和所需的输出路径。  
2. 如需验证合并顺序，建议先使用`--dry-run`选项进行预览。  
3. 仅使用必要的参数运行CLI命令。  
4. 如果命令因缺少相关工具而失败，请提示用户使用`pip install nestedpdfmerger`进行安装。  

## 支持的参数：  
- `-o, --output PATH`：指定输出PDF文件的路径。  
- `--sort {natural,alpha,mtime}`：按自然顺序、字母顺序或修改时间顺序对文件进行排序。  
- `--reverse`：反向排序文件。  
- `--exclude NAME [NAME ...]`：排除指定的文件夹。  
- `--exclude-hidden`：排除隐藏文件（以`.`开头的文件）。  
- `--no-bookmarks`：禁用PDF书签功能。  
- `--dry-run`：仅执行合并操作，不生成输出文件。  
- `--strict`：严格检查输入参数的合法性。  
- `--verbose`：输出详细的日志信息。  
- `--quiet`：静默运行，不显示任何提示信息。  
- `--version`：显示工具的版本信息。  

## 示例：  
- 预览合并顺序：  
  ```bash
nestedpdfmerger ./reports --dry-run
```  

- 显式指定输出路径进行合并：  
  ```bash
nestedpdfmerger ./reports --output merged.pdf
```  

- 在合并过程中排除某些文件夹：  
  ```bash
nestedpdfmerger ./reports --output merged.pdf --exclude Backup Data
```
# 示例文本处理器

---

**名称**: sample-text-processor  
**级别**: 基础级 (BASIC)  
**类别**: 文本处理  
**依赖项**: 无（仅依赖 Python 标准库）  
**作者**: Claude Skills 工程团队  
**版本**: 1.0.0  
**最后更新**: 2026-02-16  

---

## 描述  

示例文本处理器是一个简单的工具，用于展示 Claude Skills 生态系统中预期的基本结构和功能。该工具提供了基本的文本处理能力，包括单词计数、字符分析以及简单的文本转换功能。  

该工具作为基础级要求的参考实现，可用于创建新的技能。它展示了正确的文件结构、文档编写标准以及符合生态系统最佳实践的实现模式。  

该工具能够处理文本文件，并以人类可读格式和 JSON 格式提供统计结果和转换结果，体现了 Claude Skills 仓库中对技能的双重输出要求。  

## 特点  

### 核心功能  
- **单词计数分析**: 统计总单词数、唯一单词数及单词频率  
- **字符统计**: 分析字符数量、行数及特殊字符  
- **文本转换**: 将文本转换为大写、小写或标题格式  
- **文件处理**: 单个文本文件处理或批量处理目录  
- **双重输出格式**: 生成 JSON 和人类可读格式的结果  

### 技术特性  
- 带有全面参数解析的命令行接口  
- 对常见文件和处理问题进行错误处理  
- 批量操作的进度报告  
- 可配置的输出格式和详细程度  
- 仅依赖标准库，具备跨平台兼容性  

## 使用方法  

### 基本文本分析  
```bash
python text_processor.py analyze document.txt
python text_processor.py analyze document.txt --output results.json
```  

### 文本转换  
```bash
python text_processor.py transform document.txt --mode uppercase
python text_processor.py transform document.txt --mode title --output transformed.txt
```  

### 批量处理  
```bash
python text_processor.py batch text_files/ --output results/
python text_processor.py batch text_files/ --format json --output batch_results.json
```  

## 示例  

### 示例 1: 基本单词计数  
```bash
$ python text_processor.py analyze sample.txt
=== TEXT ANALYSIS RESULTS ===
File: sample.txt
Total words: 150
Unique words: 85
Total characters: 750
Lines: 12
Most frequent word: "the" (8 occurrences)
```  

### 示例 2: JSON 输出  
```bash
$ python text_processor.py analyze sample.txt --format json
{
  "file": "sample.txt",
  "statistics": {
    "total_words": 150,
    "unique_words": 85,
    "total_characters": 750,
    "lines": 12,
    "most_frequent": {
      "word": "the",
      "count": 8
    }
  }
}
```  

### 示例 3: 文本转换  
```bash
$ python text_processor.py transform sample.txt --mode title
Original: "hello world from the text processor"
Transformed: "Hello World From The Text Processor"
```  

## 安装  

该工具仅需要 Python 3.7 或更高版本及标准库即可运行，无需任何外部依赖项。  

1. 克隆或下载该工具的目录  
2. 进入脚本目录  
3. 直接使用 Python 运行文本处理器  

```bash
cd scripts/
python text_processor.py --help
```  

## 配置  

该文本处理器支持通过命令行参数进行多种配置：  
- `--format`: 输出格式（json、text）  
- `--verbose`: 启用详细输出和进度报告  
- `--output`: 指定输出文件或目录  
- `--encoding`: 指定文本文件编码（默认：utf-8）  

## 架构  

该工具采用简单的模块化架构：  
- **TextProcessor 类**: 负责核心处理逻辑和统计计算  
- **OutputFormatter 类**: 负责生成双重输出格式  
- **FileManager 类**: 管理文件 I/O 操作和批量处理  
- **CLI Interface**: 负责命令行参数解析和用户交互  

## 错误处理  

该工具具备全面的错误处理机制，能够处理以下情况：  
- 文件未找到或权限问题  
- 无效的编码或损坏的文本文件  
- 大文件导致的内存限制  
- 输出目录创建或写入权限问题  
- 无效的命令行参数  

## 性能考虑  

- 通过流式处理方式，高效利用内存处理大文本文件  
- 使用字典查找优化单词计数  
- 处理大型数据集时提供进度报告  
- 支持对国际文本进行编码检测  

## 贡献方式  

欢迎对该工具进行贡献，以展示最佳实践：  
1. 遵循 PEP 8 编码标准  
2. 添加详细的文档字符串  
3. 为新功能添加测试用例  
4. 更新文档  
5. 确保向后兼容性  

## 限制  

作为基础级工具，部分高级功能被有意省略：  
- 复杂的文本分析（情感分析、语言检测）  
- 高级文件格式支持（PDF、Word 文档）  
- 数据库集成或外部 API 调用  
- 对于大型数据集的并行处理  

该工具展示了 Claude Skills 生态系统中基础级技能所需的基本结构和质量标准，同时保持简洁性，专注于核心功能。
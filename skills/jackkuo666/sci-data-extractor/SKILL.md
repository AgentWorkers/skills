---
name: Sci-Data-Extractor
description: 一款基于人工智能的工具，用于从科学文献的PDF文件中提取结构化数据。
---
您是一位专业的科学文献数据提取助手，帮助用户从科学论文的PDF文件中提取结构化数据。

## 核心功能

### PDF内容提取
- 使用Mathpix OCR或PyMuPDF从PDF中提取文本
- 支持公式和表格的识别

### 数据提取
- 利用大语言模型（如Claude/GPT-4o或兼容的API）从文献中提取结构化数据
- 自动识别字段类型和数据结构
- 支持自定义提取规则和提示

### 输出格式
- Markdown表格
- CSV文件

## 安装

### 先决条件
- Python 3.8及以上版本
- pip包管理器

### 设置步骤

1. **安装Python依赖项**（选择一种方法）：
   **方法1：使用uv（推荐 - 速度最快）**
   ```bash
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create virtual environment and install dependencies
   cd /path/to/sci-data-extractor
   uv venv
   source .venv/bin/activate  # Linux/macOS
   # or .venv\Scripts\activate  # Windows
   uv pip install -r requirements.txt
   ```

   **方法2：使用conda（适合科学/研究用户）**
   ```bash
   cd /path/to/sci-data-extractor
   conda create -n sci-data-extractor python=3.11 -y
   conda activate sci-data-extractor
   pip install -r requirements.txt
   ```

   **方法3：直接使用pip（内置，无需额外安装）**
   ```bash
   cd /path/to/sci-data-extractor
   pip install -r requirements.txt
   ```

2. **配置API凭证**：
   ```bash
   # Copy example configuration
   cp .env.example .env

   # Edit .env and add your API key
   # Get API key from: https://console.anthropic.com/
   EXTRACTOR_API_KEY=your-api-key-here
   EXTRACTOR_BASE_URL=https://api.anthropic.com
   EXTRACTOR_MODEL=claude-sonnet-4-5-20250929
   EXTRACTOR_MAX_TOKENS=16384
   ```

3. **可选：配置Mathpix OCR**（用于高精度OCR）：
   ```bash
   # Get credentials from: https://api.mathpix.com/
   MATHPIX_APP_ID=your-mathpix-app-id
   MATHPIX_APP_KEY=your-mathpix-app-key
   ```

### 验证安装
```bash
python extractor.py --help
```

### 获取API密钥
- **Anthropic Claude**：https://console.anthropic.com/
- **OpenAI**：https://platform.openai.com/api-keys
- **Mathpix OCR**：https://api.mathpix.com/

## 使用方法

当用户请求数据提取时：
1. **了解需求**：询问需要提取的数据类型
2. **选择方法**：
   - 使用预设模板（如enzyme/experiment/review）
   - 使用自定义提取提示
3. **执行提取**：
   ```bash
   python extractor.py input.pdf --template enzyme -o output.md
   ```
4. **验证结果**：显示提取的数据，并询问是否需要调整

## 预设模板

### 酶动力学数据（enzyme）
字段：酶（Enzyme）、生物体（Organism）、底物（Substrate）、Km（Km）、单位Km（Unit_Km）、Kcat（Kcat）、单位Kcat（Unit_Kcat）、Kcat_Km（Kcat_Km）、温度（Temperature）、pH值（pH）、突变体（Mutant）、辅底物（Cosubstrate）

### 实验结果数据（experiment）
字段：实验名称（Experiment）、实验条件（Condition）、实验结果（Result）、单位（Unit）、标准偏差（Standard_Deviation）、样本大小（Sample_Size）、p值（p_value）

### 文献综述数据（review）
字段：作者（Author）、年份（Year）、期刊（Journal）、标题（Title）、DOI（DOI）、关键词（Key_Findings）、方法论（Methodology）

## 配置要求

用户应设置环境变量（可选，也可以放在.env文件中）：
- `EXTRACTOR_API_KEY`：LLM API密钥
- `EXTRACTOR_BASE_URL`：API端点
- `EXTRACTOR_MODEL`：模型名称（默认：claude-sonnet-4-5-20250929）
- `EXTRACTOR_TEMPERATURE`：温度参数（默认：0.1）
- `EXTRACTOR_MAX_TOKENS`：最大输出令牌数（默认：16384）
- `MATHPIX_APP_ID`：Mathpix OCR应用ID（可选）
- `MATHPIX_APP_KEY`：Mathpix OCR密钥（可选）

## 最佳实践
1. 在提取数据之前验证API密钥配置
2. 建议用户验证提取数据的准确性
3. 长文档可能需要分段处理
4. 提醒用户正确引用原始文献

## 使用示例

- 酶动力学数据提取的示例命令：
```bash
python extractor.py paper.pdf --template enzyme -o results.md
```

- 自定义提取的示例：
```bash
python extractor.py paper.pdf -p "Extract all protein structures with PDB IDs" -o custom.md
```

- CSV格式输出的示例：
```bash
python extractor.py paper.pdf --template enzyme -o results.csv --format csv
```

## 注意事项
- 本工具仅用于学术研究
- 始终验证AI提取结果的准确性
- 使用提取的数据时请尊重版权
- 适当引用原始文献
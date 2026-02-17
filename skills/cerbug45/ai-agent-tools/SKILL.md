# AI Agent Tools - 用于AI代理的Python实用库

## 📖 概述

本库提供了现成的Python函数，AI代理可以利用这些函数执行各种任务，包括文件操作、文本分析、数据转换、内存管理和数据验证。

## ⚡ 快速入门

### 安装

#### 方法1：从GitHub克隆
```bash
git clone https://github.com/cerbug45/ai-agent-tools.git
cd ai-agent-tools
```

#### 方法2：直接下载
```bash
wget https://raw.githubusercontent.com/cerbug45/ai-agent-tools/main/ai_agent_tools.py
```

#### 方法3：复制粘贴
只需将`ai_agent_tools.py`文件复制到你的项目目录中即可。

### 系统要求
- Python 3.7或更高版本
- 无需外部依赖（仅使用标准库）

## 🛠️ 可用工具

### 1. FileTools - 文件操作
用于读写和管理文件。

**可用方法：**
```python
from ai_agent_tools import FileTools

# Read a file
content = FileTools.read_file("path/to/file.txt")

# Write to a file
FileTools.write_file("path/to/file.txt", "Hello World!")

# List files in directory
files = FileTools.list_files(".", extension=".py")

# Check if file exists
exists = FileTools.file_exists("path/to/file.txt")
```

**使用场景：**
- 读取配置文件
- 保存代理输出
- 列出可用资源
- 在执行操作前检查文件是否存在

---

### 2. TextTools - 文本处理
用于提取和处理文本数据。

**可用方法：**
```python
from ai_agent_tools import TextTools

text = "Contact: john@example.com, phone: 0532 123 45 67"

# Extract emails
emails = TextTools.extract_emails(text)
# Output: ['john@example.com']

# Extract URLs
urls = TextTools.extract_urls("Visit https://example.com")
# Output: ['https://example.com']

# Extract phone numbers
phones = TextTools.extract_phone_numbers(text)
# Output: ['0532 123 45 67']

# Count words
count = TextTools.word_count("Hello world from AI")
# Output: 4

# Summarize text
summary = TextTools.summarize_text("Long text here...", max_length=50)

# Clean whitespace
clean = TextTools.clean_whitespace("Too   many    spaces")
# Output: "Too many spaces"
```

**使用场景：**
- 从文档中提取联系信息
- 清理和格式化文本
- 文本摘要
- 从非结构化文本中提取数据

---

### 3. DataTools - 数据转换
用于在不同数据格式之间进行转换。

**可用方法：**
```python
from ai_agent_tools import DataTools

# Save data as JSON
data = {"name": "Alice", "age": 30}
DataTools.save_json(data, "output.json")

# Load JSON file
loaded_data = DataTools.load_json("output.json")

# Convert CSV text to dictionary list
csv_text = """name,age,city
Alice,30,New York
Bob,25,London"""
data_list = DataTools.csv_to_dict(csv_text)
# Output: [{'name': 'Alice', 'age': '30', 'city': 'New York'}, ...]

# Convert dictionary list to CSV
data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
csv = DataTools.dict_to_csv(data)
```

**使用场景：**
- 保存结构化数据
- 在不同格式之间进行转换
- 处理API响应
- 生成报告

---

### 4. UtilityTools - 通用工具
提供常用操作的辅助函数。

**可用方法：**
```python
from ai_agent_tools import UtilityTools

# Get current timestamp
timestamp = UtilityTools.get_timestamp()
# Output: "2026-02-15 14:30:25"

# Generate unique ID from text
id = UtilityTools.generate_id("user_john_doe")
# Output: "a3f5b2c1"

# Calculate percentage
percent = UtilityTools.calculate_percentage(25, 100)
# Output: 25.0

# Safe division (no divide by zero error)
result = UtilityTools.safe_divide(10, 0, default=0.0)
# Output: 0.0
```

**使用场景：**
- 为事件添加时间戳
- 生成唯一标识符
- 执行安全的数学运算
- 数据分析计算

---

### 5. MemoryTools - 内存管理
在代理执行过程中存储和检索数据。

**可用方法：**
```python
from ai_agent_tools import MemoryTools

# Initialize memory
memory = MemoryTools()

# Store a value
memory.store("user_name", "Alice")
memory.store("session_id", "abc123")

# Retrieve a value
name = memory.retrieve("user_name")
# Output: "Alice"

# List all keys
keys = memory.list_keys()
# Output: ["user_name", "session_id"]

# Delete a value
memory.delete("session_id")

# Clear all memory
memory.clear()
```

**使用场景：**
- 维护对话上下文
- 存储中间结果
- 会话管理
- 缓存计算结果

---

### 6. ValidationTools - 数据验证
用于验证不同类型的数据。

**可用方法：**
```python
from ai_agent_tools import ValidationTools

# Validate email
is_valid = ValidationTools.is_valid_email("user@example.com")
# Output: True

# Validate URL
is_valid = ValidationTools.is_valid_url("https://example.com")
# Output: True

# Validate phone number (Turkish format)
is_valid = ValidationTools.is_valid_phone("0532 123 45 67")
# Output: True
```

**使用场景：**
- 输入验证
- 数据质量检查
- 表单验证
- 数据预处理

---

## 💡 完整使用示例

```python
from ai_agent_tools import (
    FileTools, TextTools, DataTools, 
    UtilityTools, MemoryTools, ValidationTools
)

# Initialize memory for session
memory = MemoryTools()

# Read input file
text = FileTools.read_file("contacts.txt")

# Extract information
emails = TextTools.extract_emails(text)
phones = TextTools.extract_phone_numbers(text)

# Validate extracted data
valid_emails = [e for e in emails if ValidationTools.is_valid_email(e)]
valid_phones = [p for p in phones if ValidationTools.is_valid_phone(p)]

# Create structured data
contacts = []
for i, (email, phone) in enumerate(zip(valid_emails, valid_phones)):
    contact = {
        "id": UtilityTools.generate_id(f"contact_{i}"),
        "email": email,
        "phone": phone,
        "timestamp": UtilityTools.get_timestamp()
    }
    contacts.append(contact)

# Save results
DataTools.save_json(contacts, "output/contacts.json")

# Store in memory
memory.store("total_contacts", len(contacts))
memory.store("last_processed", UtilityTools.get_timestamp())

print(f"Processed {len(contacts)} contacts")
print(f"Saved to: output/contacts.json")
```

## 🎯 最佳实践

### 1. 错误处理
始终使用try-except块来封装文件操作：

```python
try:
    content = FileTools.read_file("data.txt")
    # Process content
except Exception as e:
    print(f"Error reading file: {e}")
```

### 2. 内存管理
不再需要数据时及时释放内存：

```python
memory = MemoryTools()
# ... use memory ...
memory.clear()  # Clean up
```

### 3. 数据验证
在处理数据之前务必进行验证：

```python
if ValidationTools.is_valid_email(email):
    # Process email
    pass
else:
    print(f"Invalid email: {email}")
```

### 4. 路径处理
使用绝对路径或确保工作目录正确：

```python
import os

base_dir = os.path.dirname(__file__)
filepath = os.path.join(base_dir, "data", "file.txt")
content = FileTools.read_file(filepath)
```

## 🔧 高级用法

### 链式操作
可以组合多个工具来执行一系列操作：

```python
# Read -> Process -> Validate -> Save pipeline
text = FileTools.read_file("input.txt")
cleaned = TextTools.clean_whitespace(text)
emails = TextTools.extract_emails(cleaned)
valid = [e for e in emails if ValidationTools.is_valid_email(e)]
DataTools.save_json({"emails": valid}, "output.json")
```

### 创建自定义工作流程

```python
class DataProcessor:
    def __init__(self):
        self.memory = MemoryTools()
        
    def process_document(self, filepath):
        # Read
        text = FileTools.read_file(filepath)
        
        # Extract
        emails = TextTools.extract_emails(text)
        urls = TextTools.extract_urls(text)
        
        # Store results
        self.memory.store("emails", emails)
        self.memory.store("urls", urls)
        
        # Generate report
        report = {
            "timestamp": UtilityTools.get_timestamp(),
            "file": filepath,
            "emails_found": len(emails),
            "urls_found": len(urls)
        }
        
        return report
```

## 📦 与AI代理集成

### 示例：与LangChain集成

```python
from langchain.tools import Tool
from ai_agent_tools import FileTools, TextTools

def create_file_reader_tool():
    return Tool(
        name="ReadFile",
        func=FileTools.read_file,
        description="Read contents of a file"
    )

def create_email_extractor_tool():
    return Tool(
        name="ExtractEmails",
        func=TextTools.extract_emails,
        description="Extract email addresses from text"
    )

tools = [create_file_reader_tool(), create_email_extractor_tool()]
```

### 示例：调用OpenAI函数

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file"
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]

# In your agent loop
def execute_function(name, arguments):
    if name == "read_file":
        return FileTools.read_file(arguments["filepath"])
```

## 🧪 测试
运行内置的测试套件：

```bash
python ai_agent_tools.py
```

预期输出：
```
=== AI Ajanları İçin Araçlar Kütüphanesi ===

1. Dosya Araçları:
   Okunan içerik: Merhaba AI Ajanı!

2. Metin Araçları:
   Bulunan emailler: ['ali@example.com']
   Bulunan telefonlar: ['0532 123 45 67']

3. Veri Araçları:
   CSV çıktısı:
   isim,yaş
   Ali,25
   Ayşe,30

...

✓ Tüm araçlar test edildi!
```

## 🤝 贡献
欢迎贡献！贡献方式如下：
1. 克隆仓库：`git fork repository`
2. 创建功能分支：`git checkout -b feature/new-tool`
3. 提交更改：`git commit -am '添加新工具'
4. 将分支推送到远程仓库：`git push origin feature/new-tool`
5. 提交拉取请求

## 📝 许可证
本项目采用MIT许可证，欢迎开源使用。

## 👤 作者
**GitHub账户：** [@cerbug45](https://github.com/cerbug45)

## 🐛 问题与支持
发现bug或需要帮助？请在GitHub上提交问题：
https://github.com/cerbug45/ai-agent-tools/issues

## 📚 额外资源
- [Python官方文档](https://docs.python.org/3/)
- [正则表达式指南](https://docs.python.org/3/howto/regex.html)
- [JSON格式规范](https://www.json.org/)

## 🔄 版本历史
### v1.0.0 (2026-02-15)
- 初始版本
- 包含6个工具类别
- 25多个实用函数
- 完整的文档
- 内置测试套件

---

**快乐编程！🚀**
---
name: openclaw-plus
description: 这是一个集开发能力和网页功能于一体的模块化超级技能。当用户需要执行 Python 代码、管理软件包、操作 Git 仓库、获取 URL 内容或与 API 进行交互时，可以使用该技能。其触发条件包括运行代码的请求、安装软件包、检查 Git 仓库状态、提交更改、获取网页内容或调用 API 等操作。该技能为开发任务和网页自动化提供了统一的工作流程。
license: Complete terms in LICENSE.txt
---
# OpenClaw+ 🚀

OpenClaw+ 是一个模块化的超级技能，它将必要的开发工具和网页功能整合到一个统一、强大的工作流程中。

## 概述

OpenClaw+ 将七项核心功能整合到一个简洁的技能中：

**开发技能：**
- `run_python` - 在适当的环境管理下执行 Python 代码
- `git_status` - 检查仓库状态并跟踪更改
- `git_commit` - 带有描述性信息的提交更改
- `install_package` - 安装 Python 包并处理依赖关系

**网页功能：**
- `fetch_url` - 带有强大错误处理的网页内容检索
- `call_api` - 进行 API 请求并解析响应

这种模块化设计使您能够高效地链接各种操作——安装包、运行代码、获取数据、提交结果——所有这些都在一个连贯的工作流程中完成。

---

## 何时使用 OpenClaw+

当用户的需求涉及以下内容时，请使用此技能：
- 运行 Python 脚本或代码片段
- 安装 Python 包（pip、conda、系统包）
- 检查 git 仓库状态
- 提交代码更改
- 从 URL 获取内容
- 进行 API 调用（REST、GraphQL 等）
- 将上述任何功能组合到一个工作流程中

**常见用法：**
- “安装 pandas 并运行此分析”
- “从该 API 获取数据并保存”
- “检查 git 状态并提交我的更改”
- “运行此脚本并调用该端点”
- “安装这些包，运行代码，然后提交”

---

## 核心功能

### 1. Python 执行 (`run_python`)

在适当的环境管理下执行 Python 代码，并捕获输出结果。

**主要特性：**
- 捕获标准输出（stdout）、标准错误（stderr）和返回值
- 优雅地处理异常
- 支持多行脚本
- 可访问已安装的包
- 支持环境变量

**使用示例：**
```python
# Simple execution
result = run_python("print('Hello, world!')")

# With installed packages
run_python("""
import pandas as pd
import numpy as np

data = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print(data.describe())
""")

# File operations
run_python("""
with open('output.txt', 'w') as f:
    f.write('Results: ...')
""")
```

**最佳实践：**
- 在执行前始终检查语法错误
- 小心处理文件路径（必要时使用绝对路径）
- 捕获异常并提供清晰的错误信息
- 对于大型脚本，考虑先创建一个 `.py` 文件

---

### 2. 包安装 (`install_package`)

安装 Python 包，并智能地解决依赖关系。

**主要特性：**
- 支持 pip 包安装
- 支持系统包（apt、brew 等）
- 支持 conda 环境
- 检测依赖冲突
- 固定版本

**使用示例：**
```bash
# Install single package
install_package("pandas")

# Install specific version
install_package("numpy==1.24.0")

# Install multiple packages
install_package("requests beautifulsoup4 lxml")

# Install from requirements.txt
install_package("-r requirements.txt")

# System packages (when needed)
install_package("libpq-dev", system=True)
```

**最佳实践：**
- 在此环境中使用 `--break-system-packages` 标志安装 pip
- 在安装前检查包是否已安装
- 明确处理版本冲突
- 提供关于安装成功/失败的明确反馈

**实现方式：**
```bash
pip install <package> --break-system-packages
```

---

### 3. Git 状态 (`git_status`)

检查仓库状态并跟踪更改。

**主要特性：**
- 显示已修改、已添加和已删除的文件
- 显示未跟踪的文件
- 显示当前分支
- 指示是否领先/落后于远程仓库
- 支持自定义 git 目录

**使用示例：**
```bash
# Check current directory
git_status()

# Check specific directory
git_status("/path/to/repo")

# Parse output for automation
status = git_status()
if "modified:" in status:
    print("Changes detected")
```

**最佳实践：**
- 在提交前始终检查状态
- 解析输出以检测具体更改
- 处理目录不是 git 仓库的情况
- 提供关于更改的上下文信息

**实现方式：**
```bash
git status
git diff --stat
git log -1 --oneline
```

---

### 4. Git 提交 (`git_commit`)

按照最佳实践提交带有描述性信息的更改。

**主要特性：**
- 支持传统的提交格式
- 多行提交信息
- 自动暂存选项
- 提交信息验证
- 支持修改提交（amend）

**使用示例：**
```bash
# Simple commit
git_commit("Add new feature")

# Conventional commit
git_commit("feat: add user authentication")

# Multi-line with description
git_commit("""
feat: add data processing pipeline

- Implement CSV reader
- Add data validation
- Create output formatter
""")

# Stage and commit
git_commit("fix: resolve parsing error", stage_all=True)
```

**最佳实践：**
- 使用传统的提交格式：`type(scope): description`
- 类型：feat、fix、docs、style、refactor、test、chore
- 保持第一行在 50 个字符以内
- 如有必要，添加详细的描述
- 在适用时引用问题编号

**实现方式：**
```bash
git add <files>  # if stage_all
git commit -m "<message>"
git log -1 --oneline  # confirm commit
```

---

### 5. URL 获取 (`fetch_url`)

从 URL 获取内容，并具有强大的错误处理能力。

**主要特性：**
- 支持 HTTP/HTTPS
- 自定义请求头
- 支持身份验证
- 处理重定向
- 超时处理
- 解析响应（JSON、XML、HTML、文本）

**使用示例：**
```python
# Fetch HTML
html = fetch_url("https://example.com")

# Fetch JSON
data = fetch_url("https://api.example.com/data", 
                 parse_json=True)

# With authentication
content = fetch_url("https://api.example.com/protected",
                    headers={"Authorization": "Bearer TOKEN"})

# With custom timeout
content = fetch_url("https://slow-site.com", timeout=30)

# POST request
response = fetch_url("https://api.example.com/submit",
                     method="POST",
                     data={"key": "value"})
```

**最佳实践：**
- 始终优雅地处理网络错误
- 设置适当的超时
- 在获取前验证 URL
- 根据内容类型解析响应
- 处理速率限制
- 遵守 robots.txt 文件

**实现方式：**
```python
import requests

response = requests.get(url, headers=headers, timeout=timeout)
response.raise_for_status()
return response.text  # or response.json()
```

---

### 6. API 调用 (`call_api`)

进行 API 请求，并解析响应。

**主要特性：**
- 支持 REST API
- 支持 GraphQL
- 支持身份验证（Bearer、Basic、API Key）
- 请求/响应日志记录
- 带有重试的错误处理
- 响应验证

**使用示例：**
```python
# Simple GET request
data = call_api("https://api.example.com/users")

# With authentication
data = call_api("https://api.example.com/data",
                auth_token="your-token")

# POST with JSON body
result = call_api("https://api.example.com/create",
                  method="POST",
                  json_data={"name": "John", "age": 30})

# With custom headers
data = call_api("https://api.example.com/endpoint",
                headers={"X-Custom-Header": "value"})

# GraphQL query
result = call_api("https://api.example.com/graphql",
                  method="POST",
                  json_data={
                      "query": "{ users { id name } }"
                  })
```

**最佳实践：**
- 在使用前验证 API 密钥/令牌
- 使用指数级退避策略处理速率限制
- 解析响应格式（JSON、XML 等）
- 为调试记录请求
- 处理大数据集的分页
- 验证响应格式
- 使用适当的 HTTP 方法（GET、POST、PUT、DELETE、PATCH）

**实现方式：**
```python
import requests

headers = {"Authorization": f"Bearer {token}"}
response = requests.request(
    method=method,
    url=url,
    headers=headers,
    json=json_data,
    timeout=30
)
response.raise_for_status()
return response.json()
```

---

## 工作流程模式

当结合多种功能时，OpenClaw+ 的优势更加明显：

### 模式 1：数据管道
```python
# 1. Install dependencies
install_package("pandas requests")

# 2. Fetch data from API
data = call_api("https://api.example.com/dataset")

# 3. Process with Python
run_python("""
import pandas as pd
import json

with open('raw_data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df_cleaned = df.dropna()
df_cleaned.to_csv('cleaned_data.csv', index=False)
print(f'Processed {len(df_cleaned)} records')
""")

# 4. Commit results
git_commit("feat: add cleaned dataset")
```

### 模式 2：网页抓取与分析
```python
# 1. Install scraping tools
install_package("beautifulsoup4 lxml requests")

# 2. Fetch webpage
html = fetch_url("https://example.com/data-page")

# 3. Parse and analyze
run_python("""
from bs4 import BeautifulSoup
import json

with open('page.html', 'r') as f:
    soup = BeautifulSoup(f, 'lxml')

data = []
for item in soup.find_all('div', class_='data-item'):
    data.append({
        'title': item.find('h2').text,
        'value': item.find('span', class_='value').text
    })

with open('scraped_data.json', 'w') as f:
    json.dump(data, f, indent=2)
""")

# 4. Check and commit
git_status()
git_commit("chore: update scraped data")
```

### 模式 3：API 集成测试
```python
# 1. Install testing tools
install_package("pytest requests-mock")

# 2. Run tests
run_python("""
import requests
import json

# Test API endpoint
response = requests.get('https://api.example.com/health')
assert response.status_code == 200

# Test with authentication
headers = {'Authorization': 'Bearer test-token'}
response = requests.get('https://api.example.com/data', headers=headers)
print(f'Status: {response.status_code}')
print(f'Data: {response.json()}')
""")

# 3. Commit test results
git_commit("test: add API integration tests")
```

### 模式 4：自动化报告
```python
# 1. Fetch data from multiple sources
api_data = call_api("https://api.example.com/metrics")
web_data = fetch_url("https://example.com/reports/latest")

# 2. Process and generate report
install_package("matplotlib pandas")
run_python("""
import pandas as pd
import matplotlib.pyplot as plt
import json

with open('api_data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'])
plt.title('Metrics Over Time')
plt.savefig('report.png')
print('Report generated')
""")

# 3. Commit report
git_commit("docs: add automated metrics report")
```

---

## 错误处理

每个功能都包含强大的错误处理机制：

### Python 执行错误
```python
try:
    result = run_python(code)
except SyntaxError as e:
    print(f"Syntax error: {e}")
except RuntimeError as e:
    print(f"Runtime error: {e}")
```

### 包安装错误
```bash
# Handle already installed
if package_installed("pandas"):
    print("Package already installed")
else:
    install_package("pandas")

# Handle installation failure
try:
    install_package("nonexistent-package")
except Exception as e:
    print(f"Installation failed: {e}")
```

### Git 操作错误
```bash
# Not a git repository
if not is_git_repo():
    print("Not a git repository")
    exit(1)

# Nothing to commit
status = git_status()
if "nothing to commit" in status:
    print("No changes to commit")
```

### 网络错误
```python
# Handle timeouts
try:
    data = fetch_url(url, timeout=5)
except TimeoutError:
    print("Request timed out")

# Handle HTTP errors
try:
    response = call_api(url)
except requests.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
```

---

## 最佳实践

### 1. **环境管理**
- 在使用 pip 时始终使用 `--break-system-packages` 标志
- 在安装前检查包是否已安装
- 在适当的情况下使用虚拟环境
- 记录包版本

### 2. **Git 操作**
- 在提交前检查状态
- 使用有意义的提交信息
- 遵循传统的提交格式
- 仅暂存相关的文件

### 3. **代码执行**
- 在运行前验证语法
- 优雅地处理异常
- 捕获并记录输出
- 清理临时文件

### 4. **API/网页请求**
- 设置适当的超时
- 处理速率限制
- 验证响应
- 为调试记录请求
- 遵守 API 使用限制

### 5. **工作流程组合**
- 逻辑地链接操作
- 在每个步骤处理错误
- 提供进度反馈
- 记录依赖关系

---

## 安全考虑

### API 密钥与凭证
- 不要硬编码凭证
- 使用环境变量
- 使用前进行验证
- 定期轮换

### 代码执行
- 验证输入代码
- 可能时使用沙箱环境
- 限制资源使用
- 监控执行过程

### 网页请求
- 验证 URL
- 尽可能使用 HTTPS
- 小心处理重定向
- 遵守 robots.txt 文件

---

## 调试与故障排除

### 常见问题

**Python 执行失败：**
- 使用 `python -m py_compile script.py` 检查语法
- 确认包已安装
- 检查文件路径
- 查看错误信息

**包安装失败：**
- 确保 pip 是最新版本
- 检查网络连接
- 验证包名称
- 查看依赖关系

**Git 操作失败：**
- 确认这是一个 git 仓库
- 检查文件权限
- 确保工作目录整洁
- 检查 git 配置

**API/URL 请求失败：**
- 确认 URL 是否正确
- 检查身份验证
- 检查速率限制
- 检查网络连接

---

## 示例

### 示例 1：完整的数据管道
```python
# User request: "Fetch weather data, analyze it, and commit results"

# Step 1: Install dependencies
install_package("requests pandas matplotlib")

# Step 2: Fetch data
weather_data = call_api(
    "https://api.weather.com/data",
    auth_token="your-api-key"
)

# Step 3: Save and analyze
run_python("""
import pandas as pd
import matplotlib.pyplot as plt
import json

# Load data
with open('weather_data.json', 'r') as f:
    data = json.load(f)

# Create DataFrame
df = pd.DataFrame(data['forecast'])
df['date'] = pd.to_datetime(df['date'])

# Analyze
avg_temp = df['temperature'].mean()
max_temp = df['temperature'].max()
min_temp = df['temperature'].min()

# Generate plot
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['temperature'], marker='o')
plt.title('Temperature Forecast')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.grid(True)
plt.savefig('temperature_forecast.png')

# Save summary
summary = {
    'avg_temp': avg_temp,
    'max_temp': max_temp,
    'min_temp': min_temp,
    'records': len(df)
}

with open('weather_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(f'Analysis complete: {len(df)} records processed')
print(f'Average temperature: {avg_temp:.1f}°F')
""")

# Step 4: Commit results
git_status()
git_commit("""
feat: add weather data analysis

- Fetch 7-day forecast from API
- Generate temperature plot
- Create summary statistics
""")
```

### 示例 2：网页抓取与存储
```python
# User request: "Scrape product data and save to database"

# Step 1: Install tools
install_package("beautifulsoup4 lxml requests sqlite3")

# Step 2: Fetch webpage
html = fetch_url("https://example-shop.com/products")

# Step 3: Parse and store
run_python("""
from bs4 import BeautifulSoup
import sqlite3
import json

# Parse HTML
with open('products.html', 'r') as f:
    soup = BeautifulSoup(f, 'lxml')

products = []
for item in soup.find_all('div', class_='product'):
    product = {
        'name': item.find('h3').text.strip(),
        'price': float(item.find('span', class_='price').text.strip('$')),
        'rating': float(item.find('span', class_='rating').text),
        'url': item.find('a')['href']
    }
    products.append(product)

# Store in SQLite
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        rating REAL,
        url TEXT
    )
''')

for p in products:
    cursor.execute('''
        INSERT INTO products (name, price, rating, url)
        VALUES (?, ?, ?, ?)
    ''', (p['name'], p['price'], p['rating'], p['url']))

conn.commit()
conn.close()

print(f'Scraped and stored {len(products)} products')
""")

# Step 4: Commit
git_commit("chore: update product database")
```

### 示例 3：API 测试套件
```python
# User request: "Test our API endpoints and generate report"

# Step 1: Install testing framework
install_package("pytest requests pytest-html")

# Step 2: Create test file and run
run_python("""
import requests
import json
from datetime import datetime

BASE_URL = "https://api.example.com"
results = []

# Test 1: Health check
try:
    response = requests.get(f"{BASE_URL}/health")
    results.append({
        'test': 'Health Check',
        'status': response.status_code,
        'passed': response.status_code == 200,
        'response_time': response.elapsed.total_seconds()
    })
except Exception as e:
    results.append({
        'test': 'Health Check',
        'status': 'Error',
        'passed': False,
        'error': str(e)
    })

# Test 2: Authentication
try:
    headers = {'Authorization': 'Bearer test-token'}
    response = requests.get(f"{BASE_URL}/auth/validate", headers=headers)
    results.append({
        'test': 'Authentication',
        'status': response.status_code,
        'passed': response.status_code == 200,
        'response_time': response.elapsed.total_seconds()
    })
except Exception as e:
    results.append({
        'test': 'Authentication',
        'status': 'Error',
        'passed': False,
        'error': str(e)
    })

# Test 3: Data retrieval
try:
    response = requests.get(f"{BASE_URL}/data/users")
    data = response.json()
    results.append({
        'test': 'Data Retrieval',
        'status': response.status_code,
        'passed': response.status_code == 200 and len(data) > 0,
        'records': len(data) if response.status_code == 200 else 0,
        'response_time': response.elapsed.total_seconds()
    })
except Exception as e:
    results.append({
        'test': 'Data Retrieval',
        'status': 'Error',
        'passed': False,
        'error': str(e)
    })

# Generate report
report = {
    'timestamp': datetime.now().isoformat(),
    'total_tests': len(results),
    'passed': sum(1 for r in results if r.get('passed')),
    'failed': sum(1 for r in results if not r.get('passed')),
    'results': results
}

with open('api_test_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print(f"Tests complete: {report['passed']}/{report['total_tests']} passed")
for r in results:
    status = '✓' if r.get('passed') else '✗'
    print(f"{status} {r['test']}")
""")

# Step 3: Check and commit
git_status()
git_commit("test: add API endpoint tests")
```

---

## 与其他技能的集成

OpenClaw+ 可与其他技能无缝配合使用：

### 与 `docx` 技能集成：
```python
# Generate data, then create report
call_api("https://api.example.com/stats")
run_python("process_stats.py")
# Then use docx skill to create formatted report
```

### 与 `xlsx` 技能集成：
```python
# Fetch data, process with Python, export to Excel
fetch_url("https://data-source.com/raw.csv")
run_python("clean_and_transform.py")
# Then use xlsx skill to create formatted spreadsheet
```

### 与 `pptx` 技能集成：
```python
# Generate charts and data visualizations
install_package("matplotlib seaborn")
run_python("generate_charts.py")
# Then use pptx skill to create presentation
```

---

## 快速参考

### Python 执行
```python
run_python(code_string)
```

### 包管理
```bash
install_package("package_name")
install_package("package==1.0.0")
install_package("-r requirements.txt")
```

### Git 操作
```bash
git_status()
git_commit("message")
git_commit("message", stage_all=True)
```

### 网页请求
```python
fetch_url(url, timeout=30)
call_api(url, method="GET", auth_token="token")
```

---

## 结论

OpenClaw+ 为开发和网页自动化工作流程提供了一个统一、强大的工具包。通过结合 Python 执行、包管理、Git 操作和网页功能，它使复杂的多步骤工作流程能够通过一个统一的技能轻松实现。

**主要优势：**
- ✅ 模块化设计——仅使用所需的功能
- ✅ 强大的错误处理——出色的故障恢复能力
- ✅ 工作流程组合——轻松链接操作
- ✅ 适合生产环境——遵循最佳实践
- ✅ 文档齐全——提供清晰的示例和模式

每当您的任务涉及代码执行、包管理、版本控制或网页交互——或这些功能的任意组合时，请使用 OpenClaw+！
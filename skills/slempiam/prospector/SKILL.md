---
name: prospector
description: |
  This skill should be used when the user wants to find leads, prospects, or contacts matching their ICP (Ideal Customer Profile). It searches for companies via Exa and enriches contacts via Apollo, outputting to CSV and optionally syncing to Attio CRM.

  MANDATORY TRIGGERS: "find leads", "prospecting", "ICP search", "find contacts", "lead generation", "/prospector"
version: 1.0.0
---

# Prospector

通过Exa公司搜索结合Apollo联系人信息 enrichment（数据丰富化）功能，找到符合您ICP（Investment Criteria Profile，投资标准配置）的潜在客户。

## 先决条件

首先运行 `/prospector:setup` 命令来配置您的API密钥：
- **Exa**（必需）：https://exa.ai - 用于公司信息查询
- **Apollo**（必需）：https://apollo.io - 用于联系人信息丰富化
- **Attio**（可选）：https://attio.com - 用于CRM系统数据同步

您也可以通过环境变量来设置这些密钥：
- `PROSPECTOR_EXA_API_KEY`
- `PROSPECTOR_APOLLO_API_KEY`
- `PROSPECTOR_ATTIO_API_KEY`（可选）

## 使用方法

### 设置（仅一次）

```
/prospector:setup
```

收集并验证API密钥，将其安全地存储在 `~/.config/prospector/config.json` 文件中。

### 寻找潜在客户

```
/prospector
```

根据用户提供的ICP标准提问，通过Exa进行搜索，利用Apollo进行数据丰富化处理，然后将结果以CSV格式输出到桌面。

## 主命令：/prospector

当用户调用 `/prospector` 时，请按照以下流程操作：

### 第一步：检查配置或环境变量

首先验证配置文件或环境变量是否存在：

```bash
python3 -c "
import json
import os
from pathlib import Path
config_path = Path.home() / '.config' / 'prospector' / 'config.json'
env_exa = bool(os.getenv('PROSPECTOR_EXA_API_KEY'))
env_apollo = bool(os.getenv('PROSPECTOR_APOLLO_API_KEY'))
env_attio = bool(os.getenv('PROSPECTOR_ATTIO_API_KEY'))
if not config_path.exists():
    print('NOT_FOUND')
else:
    with open(config_path) as f:
        config = json.load(f)
    print('FOUND')
    print(f'exa: {bool(config.get(\"exa_api_key\"))}')
    print(f'apollo: {bool(config.get(\"apollo_api_key\"))}')
    print(f'attio: {bool(config.get(\"attio_api_key\"))}')
print(f'env_exa: {env_exa}')
print(f'env_apollo: {env_apollo}')
print(f'env_attio: {env_attio}')
"
```

如果未找到配置文件或环境变量未设置，提示用户先运行 `/prospector:setup` 命令。

### 第二步：收集ICP标准

使用 `AskUserQuestion` 功能依次收集用户提供的ICP标准：
- **问题1：行业**
```
header: "Industry"
question: "What industry are you targeting?"
options:
  - label: "SaaS"
    description: "Software as a Service companies"
  - label: "Fintech"
    description: "Financial technology companies"
  - label: "Healthcare"
    description: "Healthcare and health tech"
  - label: "E-commerce"
    description: "Online retail and marketplaces"
  - label: "AI/ML"
    description: "Artificial intelligence and machine learning"
  - label: "Any"
    description: "No industry filter"
multiSelect: false
```

- **问题2：公司规模**
```
header: "Size"
question: "What company size are you targeting?"
options:
  - label: "1-10"
    description: "Early stage startups"
  - label: "11-50"
    description: "Seed to Series A"
  - label: "51-200"
    description: "Series A to B"
  - label: "201-500"
    description: "Growth stage"
  - label: "500+"
    description: "Enterprise"
  - label: "Any"
    description: "No size filter"
multiSelect: false
```

- **问题3：融资阶段**
```
header: "Funding"
question: "What funding stage are you targeting?"
options:
  - label: "Pre-seed"
    description: "Pre-product market fit"
  - label: "Seed"
    description: "Building initial product"
  - label: "Series A"
    description: "Scaling product"
  - label: "Series B+"
    description: "Growth and expansion"
  - label: "Any"
    description: "No funding filter"
multiSelect: false
```

- **问题4：地理位置**
```
header: "Geography"
question: "What geography are you targeting?"
options:
  - label: "United States"
    description: "US-based companies"
  - label: "Europe"
    description: "European companies"
  - label: "Global"
    description: "Worldwide"
  - label: "Any"
    description: "No geography filter"
multiSelect: false
```

- **问题5：关键词（可选）**
```
header: "Keywords"
question: "Any specific keywords that should appear in company descriptions? (optional)"
options:
  - label: "Skip"
    description: "No keyword filter"
  - label: "Enter keywords"
    description: "I'll type specific keywords"
multiSelect: false
```

如果用户选择了“输入关键词”，则接收用户输入的文本。

- **问题6：联系人数量**
```
header: "Count"
question: "How many contacts do you want to find?"
options:
  - label: "25"
    description: "Quick search, lower API usage"
  - label: "50"
    description: "Balanced (recommended)"
  - label: "100"
    description: "Larger batch, more API usage"
multiSelect: false
```

### 第三步：执行搜索

使用收集到的ICP标准执行Python脚本进行搜索：

```bash
cd [skill_directory]/scripts
python3 -c "
from prospector import run_search, export_csv, Config

icp = {
    'industry': '[INDUSTRY]',
    'company_size': '[SIZE]',
    'funding_stage': '[FUNDING]',
    'geography': '[GEOGRAPHY]',
    'keywords': '[KEYWORDS or empty string]'
}

leads = run_search(icp, num_contacts=[COUNT])
if leads:
    path = export_csv(leads)
    print(f'SUCCESS: {len(leads)} leads saved to {path}')
else:
    print('NO_RESULTS: No leads found matching criteria')
"
```

请将脚本中的占位符替换为实际收集到的数据。

### 第四步：（如果配置了Attio）进行数据同步

如果配置了Attio并且找到了潜在客户，系统会提示用户是否需要同步数据：

```
header: "Attio"
question: "Sync leads to Attio CRM?"
options:
  - label: "Yes"
    description: "Sync companies and contacts to Attio"
  - label: "No"
    description: "Just keep the CSV"
multiSelect: false
```

如果用户同意同步，系统将执行数据同步操作：

```bash
cd [skill_directory]/scripts
python3 -c "
from prospector import sync_to_attio, Config, Lead
import json

# Load leads from the CSV we just created (or pass them directly)
# For simplicity, re-run with sync
leads = [...]  # Pass leads from previous step

companies, people = sync_to_attio(leads)
print(f'SYNCED: {companies} companies, {people} contacts')
"
```

### 第五步：报告结果

向用户展示以下信息：
- 找到了多少潜在客户
- CSV文件保存的位置
- 如果进行了Attio数据同步，同步了多少条记录

## 错误处理

- **配置文件未找到**：提示用户运行 `/prospector:setup` 命令
- **API密钥无效**：告知用户哪个密钥无效，并建议重新运行配置流程
- **未找到结果**：建议用户放宽ICP标准以扩大搜索范围
- **部分操作失败**：报告成功执行的操作以及失败的原因
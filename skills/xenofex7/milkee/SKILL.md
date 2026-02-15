---
name: milkee
description: "**MILKEE会计系统与瑞士企业的全面集成**  
该解决方案支持企业对项目、客户、工作时间、任务及产品进行高效管理。具体应用场景包括：  
1. **计费时间管理**：通过启动/停止计时器精确记录可收费的工作时间；  
2. **项目与客户管理**：创建并维护项目及客户信息；  
3. **工作记录**：详细记录工作内容；  
4. **每日时间汇总**：实时查看每日工作进度。  

**核心功能：**  
- **智能模糊匹配**：系统具备强大的项目匹配能力，可快速找到相关任务或记录；  
- **全面的时间跟踪功能**：确保所有工作时间都被准确记录并可用于计费；  
- **高效的项目与客户管理**：简化项目与客户的创建、更新及查询流程。"
metadata:
  openclaw:
    requires:
      env:
        - MILKEE_API_TOKEN
        - MILKEE_COMPANY_ID
---

# MILKEE 技能

该技能实现了与 MILKEE 瑞士会计软件的完全集成，支持项目、客户、时间跟踪、任务和产品的管理。

## 主要功能

- ⏱️ **时间跟踪** – 支持通过模糊匹配来启动/停止计时器
- 👥 **客户** – 提供完整的 CRUD 操作（创建、读取、更新、删除）
- 📋 **项目** – 可以创建、更新项目并管理预算
- ✅ **任务** – 跟踪项目中的各项任务
- 📦 **产品** – 管理可计费的项目内容

## 快速入门

### 时间跟踪（核心功能）

```bash
# Start timer (smart fuzzy match)
python3 scripts/milkee.py start_timer "Website" "Building authentication"

# Stop timer (auto-logs to MILKEE)
python3 scripts/milkee.py stop_timer

# Show today's times
python3 scripts/milkee.py list_times_today
```

### 项目管理

```bash
python3 scripts/milkee.py list_projects
python3 scripts/milkee.py create_project "My Project" --customer-id 123 --budget 5000
python3 scripts/milkee.py update_project 456 --name "Updated" --budget 6000
```

### 客户管理

```bash
python3 scripts/milkee.py list_customers

# Create with all fields
python3 scripts/milkee.py create_customer "Example AG" \
  --street "Musterstrasse 1" \
  --zip "8000" \
  --city "Zürich" \
  --phone "+41 44 123 45 67" \
  --email "info@example.ch" \
  --website "https://example.ch"

# Update specific fields
python3 scripts/milkee.py update_customer 123 --name "New Name" --phone "+41 44 999 88 77"
```

### 任务与产品管理

```bash
python3 scripts/milkee.py list_tasks
python3 scripts/milkee.py create_task "Implement feature" --project-id 456

python3 scripts/milkee.py list_products
python3 scripts/milkee.py create_product "Consulting Hour" --price 150
```

## 配置

您可以通过设置环境变量来进行配置：

```bash
export MILKEE_API_TOKEN="USER_ID|API_KEY"
export MILKEE_COMPANY_ID="YOUR_COMPANY_ID"
```

或者通过 `skills.entries.milkee.env` 文件中的网关配置进行配置。

### 获取您的凭证

1. 登录到 MILKEE → **设置** → **API**
2. 复制您的用户 ID 和 API 密钥
3. 格式：`USER_ID|API_KEY`
4. 公司 ID 可以在设置中查看

## 特殊功能

### 模糊项目匹配

当您输入“Website”时，该技能会：
1. 从 MILKEE 中获取所有项目
2. 使用 Levenshtein 距离算法进行模糊匹配
3. 自动选择最匹配的项目
4. 在该项目上启动计时器

### 计时器数据持久化

- 计时器状态会保存在 `~/.milkee_timer` 文件中
- 计时器数据会在会话之间保持一致
- 停止计时时会自动计算经过的时间

### 每日总结

`list_times_today` 命令会显示：
- 今天的所有时间记录
- 每条记录的持续时间
- 总工作小时数

## 技术细节

- **语言**：Python 3.8+
- **依赖库**：无（仅使用标准库）
- **计时器文件**：`~/.milkee_timer`（JSON 格式）
- **API 文档**：https://apidocs.milkee.ch/api

---

**作者**：xenofex7 | **版本**：2.0.0
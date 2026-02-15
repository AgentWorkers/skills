---
name: linkdapi
description: 使用 LinkdAPI Python SDK 来访问 LinkedIn 的个人资料和公司数据。当您需要获取个人资料信息、公司数据、职位列表，或在 LinkedIn 上搜索人员/职位时，可以使用该工具。该技能采用了 uv 脚本模式（uv script pattern），用于编写具有内联依赖关系的临时性 Python 脚本。
---

# LinkdAPI Python SDK

LinkdAPI 的 Python SDK — 用于获取 LinkedIn 上的专业人士资料和公司信息，具备企业级可靠性。

> **获取您的 API 密钥：** https://linkdapi.com/signup?ref=K_CZJSWF

## 快速入门模式

使用 **uv 脚本模式** 来编写具有内联依赖关系的临时 Python 脚本：

```python
# /// script
# dependencies = [
#     "linkdapi",
# ]
# ///

from linkdapi import LinkdAPI

client = LinkdAPI("YOUR_API_KEY")
profile = client.get_profile_overview("ryanroslansky")
print(profile)
```

运行方式：
```bash
uv run script.py
```

该模式会自动安装依赖关系、运行脚本并清理残留文件，非常适合一次性任务。

## 为什么选择这种模式

- **无需全局安装依赖关系**：依赖关系按脚本单独管理
- **临时性设计**：编写、运行、删除脚本后无需额外清理
- **可复现性**：所有所需内容都在一个文件中
- **高效**：uv 负责处理依赖关系的解析和缓存

## 编写脚本

### 脚本头部格式

务必以 `uv` 脚本块开头：

```python
# /// script
# dependencies = [
#     "linkdapi",
#     # Add more if needed (e.g., "rich", "pandas")
# ]
# ///
```

### 常见操作

- **获取个人资料概览：**
```python
# /// script
# dependencies = ["linkdapi"]
# ///

from linkdapi import LinkdAPI

client = LinkdAPI("YOUR_API_KEY")
profile = client.get_profile_overview("ryanroslansky")

if profile.get('success'):
    data = profile['data']
    print(f"{data['fullName']} - {data.get('headline', '')}")
    print(f"Location: {data.get('location')}")
```

- **获取公司信息：**
```python
# /// script
# dependencies = ["linkdapi"]
# ///

from linkdapi import LinkdAPI

client = LinkdAPI("YOUR_API_KEY")
company = client.get_company_info(name="google")

if company.get('success'):
    data = company['data']
    print(f"{data['name']}")
    print(f"Industry: {data.get('industry')}")
    print(f"Employees: {data.get('employeeCount', 'N/A')}")
```

- **搜索职位：**
```python
# /// script
# dependencies = ["linkdapi"]
# ///

from linkdapi import LinkdAPI

client = LinkdAPI("YOUR_API_KEY")
result = client.search_jobs(
    keyword="Software Engineer",
    location="San Francisco, CA",
    time_posted="1week"
)

if result.get('success'):
    for job in result['data']['jobs'][:5]:
        print(f"{job['title']} at {job['company']}")
```

- **批量处理个人资料（异步）：**
```python
# /// script
# dependencies = ["linkdapi"]
# ///

import asyncio
from linkdapi import AsyncLinkdAPI

async def enrich():
    async with AsyncLinkdAPI("YOUR_API_KEY") as api:
        profiles = await asyncio.gather(
            api.get_profile_overview("ryanroslansky"),
            api.get_profile_overview("satyanadella"),
            api.get_profile_overview("jeffweiner08")
        )
        for p in profiles:
            if p.get('success'):
                print(p['data']['fullName'])

asyncio.run(enrich())
```

## 代理工作流程

当用户请求 LinkedIn 数据时：

1. **确定任务类型**（查找个人资料、公司信息、搜索职位等）
2. **在工作区中使用 `uv` 脚本编写临时脚本**
3. **添加依赖关系**（通常只需 `"linkdapi"`，必要时可添加其他依赖）
4. **导入并使用 LinkdAPI 类**
5. **使用 `uv run` 运行脚本**
6. **捕获输出结果并反馈给用户**
7. **使用后删除脚本**（可选）

### 示例工作流程

用户：*"获取 jeffweiner08 的个人资料"*

代理：```bash
cat > /tmp/linkdapi_query.py << 'EOF'
# /// script
# dependencies = ["linkdapi"]
# ///

from linkdapi import LinkdAPI
import os

client = LinkdAPI(os.getenv("LINKDAPI_API_KEY"))
profile = client.get_profile_overview("jeffweiner08")

if profile.get('success'):
    data = profile['data']
    print(f"Name: {data['fullname']}")
    print(f"Headline: {data.get('headline', 'N/A')}")
    print(f"Location: {data.get('location', 'N/A')}")
    print(f"Company: {data.get('company', 'N/A')}")
else:
    print(f"Error: {profile.get('message')}")
EOF

uv run /tmp/linkdapi_query.py
rm /tmp/linkdapi_query.py
```

## 获取 API 密钥

要使用 LinkdAPI，您需要一个 API 密钥。请在以下链接注册：

🔗 **https://linkdapi.com/signup?ref=K_CZJSWF**

注册完成后，您将获得一个 API 密钥，可用于验证您的请求。

## 认证

将 API 密钥设置为环境变量：

```bash
export LINKDAPI_API_KEY="your_api_key_here"
```

在脚本中使用该密钥：
```python
import os
from linkdapi import LinkdAPI

client = LinkdAPI(os.getenv("LINKDAPI_API_KEY"))
```

## 主要 API 方法

### 个人资料
- `get_profile_overview(username)` — 基本个人资料信息
- `get_profile_details(urn)` — 详细个人资料数据
- `get_contact_info(username)` — 电子邮件、电话、网站信息
- `get_full_profile(username=None, urn=None)` — 完整个人资料
- `get_full_experience(urn)` — 工作经历
- `get_education(urn)` — 教育背景
- `get_skills(urn)` — 技能和认可信息

### 公司
- `get_company_info.company_id=None, name=None)` — 公司详细信息
- `company_name_lookup(query)` — 按名称搜索公司
- `get_company_employees_data/company_id)` — 公司员工信息
- `get_company_jobs(company_ids)` — 公司职位信息

### 职位
- `search_jobs(keyword, location, ...)` — 搜索职位信息
- `get_job_details(job_id)` — 详细职位信息

### 搜索功能
- `search_people(keyword, title, company, ...)` — 搜索人员信息
- `search_companies(keyword, industry, ...)` — 搜索公司信息
- `search_posts(keyword, ...)` — 搜索帖子

## 性能优化建议

- 对于批量操作，请使用 `AsyncLinkdAPI`（速度提升 40 倍）
- 在 `asyncio.gather()` 中添加 `return_exceptions=True` 以实现优雅的错误处理
- 使用上下文管理器（`async with`）确保资源得到正确清理

## 错误处理

检查响应并处理错误：

```python
result = client.get_profile_overview("username")

if result.get('success'):
    data = result['data']
    # Process data
else:
    print(f"API Error: {result.get('message')}")
```

## 参考资料

完整的 API 文档：https://linkdapi.com/docs
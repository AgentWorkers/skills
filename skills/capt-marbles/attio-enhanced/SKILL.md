# 增强型 Attio 技能

这是一个支持批量操作的 Attio CRM API 技能。

## ⚠️ 必需的设置

使用此技能需要 Attio 的登录凭据。在使用前，请设置以下环境变量：

```bash
export ATTIO_API_KEY=your_api_key
export ATTIO_WORKSPACE_ID=your_workspace_id
```

从以下链接获取 API 密钥：https://app.attio.com/settings/api

在您的 Attio URL 中找到工作区 ID：`app.attio.com/[workspace-id]/...`

## 功能

- **批量操作**：批量创建/更新记录
- **重试机制**：针对速率限制采用指数级退避策略
- **智能字段映射**：自动将字段转换为 Attio 格式
- **支持公司和人员信息**：可以创建公司、人员和交易记录

## 使用方法

### Python

```python
import os
os.environ['ATTIO_API_KEY'] = 'your_key'
os.environ['ATTIO_WORKSPACE_ID'] = 'your_workspace'

from lib.attio_enhanced import AttioEnhancedClient

async with AttioEnhancedClient() as client:
    # Create companies
    await client.batch_create_records('companies', [{'name': 'Gameye'}])
    
    # Create people
    await client.batch_create_records('people', [
        {'name': ['John Doe'], 'email_addresses': ['john@example.com']}
    ])
```

### 命令行接口（CLI）测试

```bash
python3 -c "from lib.attio_enhanced import AttioEnhancedClient; print('OK')"
```

## 字段映射规则

- `first_name` + `last_name` → 转换为 Attio 名称格式
- `email` → 转换为 `email_addresses` 格式
- `Org` → 转换为 `companies` 类型
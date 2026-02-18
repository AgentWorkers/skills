# 增强型 Attio 技能

这是一个改进版的 Attio 客户关系管理（CRM）技能，具备批量操作、错误处理和数据验证功能。

## 主要特性

- **批量操作**：支持分批次创建或更新记录。
- **重试机制**：针对速率限制采用指数级退避策略（exponential backoff）。
- **智能字段映射**：自动将字段转换为 Attio 格式。
- **支持公司和个人数据**：能够创建公司、个人以及交易记录。

## 设置

```bash
# Set environment variables
export ATTIO_API_KEY=your_api_key
export ATTIO_WORKSPACE_ID=your_workspace
```

请从以下链接获取 API 密钥：https://app.attio.com/settings/api

## 使用方法

### 创建公司

```python
from lib.attio_enhanced import AttioEnhancedClient

async with AttioEnhancedClient() as client:
    # Single company
    await client.batch_create_records('companies', [{'name': 'Gameye'}])
    
    # Batch
    await client.batch_create_records('companies', [
        {'name': 'Company A'},
        {'name': 'Company B'}
    ])
```

### 创建个人

```python
await client.batch_create_records('people', [
    {'name': ['John Doe'], 'email_addresses': ['john@example.com']}
])
```

### 创建交易记录

```python
# Deals require owner (workspace member) - use Attio UI for now
```

## 字段映射

该技能会自动转换以下常见字段：
- `first_name` + `last_name` → 转换为 Attio 格式的姓名
- `email` → 转换为标准的电子邮件地址格式
- `Org` → 转换为公司（company）相关字段

## 命令行接口（CLI）

```bash
# Test connection
python -c "from lib.attio_enhanced import AttioEnhancedClient; print('OK')"
```
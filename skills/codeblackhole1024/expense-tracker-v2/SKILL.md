---
name: expense-tracker
description: 使用多后端存储（本地文件、Notion、Google Sheets 或 Supabase）来记录支出和收入。所有凭据均采用 AES-256-GCM 算法进行加密。该功能适用于用户需要记录支出、查看交易历史或检查每月支出统计的情况。
---
# 支出追踪器技能

## 快速入门

### 初始设置（首次使用）

```bash
expense-tracker setup
```

此过程将：
1. 请求您设置一个主密码（用于加密凭证）
2. 选择存储后端并配置 API 密钥

**存储后端：**
1. **本地文件** - 无需配置
2. **Notion** - 需要 API 密钥 + 数据库 ID
3. **Google Sheet** - 需要凭证路径 + 电子表格 ID
4. **Supabase** - 需要 URL + 匿名密钥

### 设置密码（后续使用）

```bash
expense-tracker pass <your-password>
```

或者根据提示进行交互式设置。

### 记录支出

```bash
expense-tracker add -50 "lunch" food
# Format: expense-tracker add <amount> <note> <category>
# Negative amount = expense
```

### 记录收入

```bash
expense-tracker add 5000 "salary" salary
# Positive amount = income
```

### 查看记录

```bash
expense-tracker list              # Recent 10 records
expense-tracker list --month     # This month
expense-tracker list --category  # By category
```

### 统计数据

```bash
expense-tracker stats             # This month
expense-tracker stats -m 2       # 2 months ago
```

## 安全性

凭证使用 **AES-256-GCM** 加密算法进行加密，并通过 PBKDF2 算法生成密钥。

- 配置文件：`~/.openclaw/expense-tracker/config.enc`
- 从不存储明文密码或 API 密钥

## 分类

- `food` - 食品与餐饮
- `transport` - 交通费用
- `shopping` - 购物费用
- `entertainment` - 娱乐费用
- `salary` - 工资
- `bonus` - 奖金
- `investment` - 投资费用
- `other` - 其他费用

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `setup` | 设置密码并配置后端（首次使用） |
| `pass <password>` | 设置解密密码 |
| `add <amount> <note> <category>` | 添加新记录 |
| `list` | 查看最近的交易记录 |
| `list --month` | 查看本月的记录 |
| `list --category` | 按类别分组查看记录 |
| `stats` | 查看月度统计信息 |
| `stats -m <n>` | 查看 n 个月前的记录 |

## 数据格式

每条记录包含以下信息：

```json
{
  "id": "uuid",
  "type": "expense|income",
  "amount": -50,
  "category": "food",
  "note": "lunch",
  "date": "2026-03-03",
  "created_at": "2026-03-03T20:23:00Z"
}
```
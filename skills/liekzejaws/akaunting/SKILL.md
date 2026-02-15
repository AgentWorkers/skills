---
name: akaunting
description: 通过 REST API 与 Akaunting 开源会计软件进行交互。该软件可用于创建发票、跟踪收入/支出、管理账户以及实现记账自动化。相关操作会在会计处理、记账、开票、费用记录、收入追踪或与 Akaunting 相关的任何事件发生时被触发。
---

# Akaunting 技能

Akaunting 是一个免费的开源会计平台，支持 CLI（命令行接口）和 API（应用程序编程接口）集成。

## 快速入门

```bash
# Test connection
akaunting ping

# List data
akaunting accounts
akaunting categories  
akaunting transactions

# Create transactions
akaunting income --amount 100 --category Sales --description "Payment received"
akaunting expense --amount 50 --category Other --description "Office supplies"
```

## 设置

### 1. 部署 Akaunting

```bash
# Use the provided docker-compose
cp skills/akaunting/assets/docker-compose.yml ~/akaunting/
cd ~/akaunting && docker compose up -d
```

访问 `http://YOUR_IP:8080` 并完成设置向导。

### 2. 应用必要的修复

**重要提示：** Akaunting 存在一个漏洞，导致模块事件监听器无法自动注册。请运行以下命令进行修复：

```bash
python3 skills/akaunting/scripts/fix_event_listener.py
```

或者手动将相关代码添加到 `/var/www/html/app/Providers/Event.php` 文件中的 `$listen` 数组中：

```php
'App\Events\Module\PaymentMethodShowing' => [
    'Modules\OfflinePayments\Listeners\ShowAsPaymentMethod',
],
```

### 3. 配置凭据

```bash
mkdir -p ~/.config/akaunting
cat > ~/.config/akaunting/config.json << EOF
{
  "url": "http://YOUR_IP:8080",
  "email": "your@email.com",
  "password": "your-password"
}
EOF
```

或者设置环境变量：`AKAUNTING_URL`、`AKAUNTING_EMAIL`、`AKAUNTING_PASSWORD`

## CLI 命令

| 命令 | 描述 |
|---------|-------------|
| `akaunting ping` | 测试 API 连接 |
| `akaunting accounts` | 列出银行账户 |
| `akaunting categories [--type income|expense]` | 列出分类 |
| `akaunting transactions [--type income|expense]` | 列出交易记录 |
| `akaunting items` | 列出产品/服务 |
| `akaunting income --amount X --category Y` | 创建收入记录 |
| `akaunting expense --amount X --category Y` | 创建支出记录 |
| `akaunting item --name X --price Y` | 创建产品/服务条目 |

在任意命令后添加 `--json` 选项可获取 JSON 格式的输出。

## API 参考

请参阅 `references/api.md` 以获取完整的 API 文档。

### 主要 API 端点

- `GET /api/ping` - 系统健康检查
- `GET/POST /api/accounts` - 银行账户信息
- `GET/POST /api/categories` - 收入/支出分类
- `GET/POST /api/transactions` - 收入/支出记录
- `GET/POST /api/items` - 产品/服务信息

认证方式：使用 HTTP Basic Auth（用户名/密码）。用户需要具备 `read-api` 权限（管理员角色默认具有此权限）。

## 故障排除

**“支付方式无效”错误：**
未应用事件监听器的修复代码。请运行 `fix_eventlistener.py`。

**401 Unauthorized（未经授权）：**
检查 `config.json` 中的凭据。用户必须具有 API 访问权限。

**403 Forbidden（访问 contacts/documents 被禁止）：**
用户需要额外的权限才能访问这些 API 端点。
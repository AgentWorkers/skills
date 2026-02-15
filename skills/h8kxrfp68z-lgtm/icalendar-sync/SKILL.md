# iCloud 日历同步技能

该技能用于在本地系统与 iCloud 之间同步日历事件。

## ⚠️ 安全要求

**安装前务必阅读：**

### 1. 仅使用应用程序专用的密码

- 请在 [https://appleid.apple.com/account/security](https://appleid.apple.com/account/security) 生成该密码。
- **切勿使用您的主 Apple ID 密码**。
- 该密码一旦泄露，可随时被撤销。

### 2. 使用操作系统的密钥环（Keyring）存储凭证

该技能会将凭证安全地存储在操作系统的密钥环中：
- **macOS**：Keychain
- **Windows**：Credential Manager
- **Linux**：Secret Service API

### 3. 适用于无交互式环境（如 Docker、CI/CD 或无头服务器）

对于无法进行交互式输入的环境：
**选项 A：环境变量**（标准且安全的方法）
```bash
# Set credentials as environment variables
export ICLOUD_USERNAME="user@icloud.com"
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"

# Run setup
python -m icalendar_sync setup --non-interactive
```

**选项 B：Docker/Kubernetes Secrets**（对容器来说最安全的方式）
```bash
# Docker secrets
docker run --secret icloud_username --secret icloud_password ...

# Kubernetes secrets
kubectl create secret generic icloud-credentials \
  --from-literal=username=user@icloud.com \
  --from-literal=password=xxxx-xxxx-xxxx-xxxx
```

凭证的读取顺序如下：
1. 操作系统的密钥环（如果可用且已配置）
2. 环境变量（如果密钥环不可用）
3. 交互式提示（如果两者均不可用）

## 安装

```bash
./install.sh
```

## 使用方法

### 设置凭证（交互式）

```bash
# Interactive mode - password prompted securely
python -m icalendar_sync setup --username user@icloud.com
```

系统会提示您输入密码，并将其存储在操作系统的密钥环中。

### 列出日历

```bash
python -m icalendar_sync list
```

### 获取日历事件

```bash
python -m icalendar_sync get --calendar "Personal" --days 7
```

### 创建事件

```bash
python -m icalendar_sync create \
  --calendar "Personal" \
  --json '{
    "summary": "Meeting",
    "dtstart": "2026-02-15T14:00:00+03:00",
    "dtend": "2026-02-15T15:00:00+03:00"
  }'
```

### 更新事件

**更新简单事件：**
```bash
python -m icalendar_sync update \
  --calendar "Personal" \
  --uid "event-uid-here" \
  --json '{"summary": "Updated Meeting Title"}'
```

**更新重复事件的单个实例：**
```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "recurring-event-uid" \
  --recurrence-id "2026-02-20T09:00:00+03:00" \
  --mode single \
  --json '{"dtstart": "2026-02-21T09:00:00+03:00"}'
```

**更新所有实例：**
```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "recurring-event-uid" \
  --mode all \
  --json '{"summary": "New Title for All Instances"}'
```

**更新当前及未来的所有实例：**
```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "recurring-event-uid" \
  --recurrence-id "2026-03-01T09:00:00+03:00" \
  --mode future \
  --json '{"dtstart": "2026-03-01T14:00:00+03:00"}'
```

### 删除事件

```bash
python -m icalendar_sync delete --calendar "Personal" --uid "event-uid-here"
```

## 确认已满足的要求：

- Python 3.9 或更高版本
- iCloud 应用程序专用的密码
- 具备访问 iCloud CalDAV 服务器（caldav.icloud.com:443）的权限

## 安全特性：

- ✅ 使用操作系统的密钥环存储凭证
- ✅ 强制使用应用程序专用密码（而非主密码）
- ✅ 实施 SSL/TLS 验证
- ✅ 实施速率限制（每 60 秒最多调用 10 次）
- ✅ 日志中自动隐藏凭证信息
- ✅ 对所有用户输入进行验证

## 许可证：

MIT 许可证
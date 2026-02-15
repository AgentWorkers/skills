---
name: namecheap-dns
description: Namecheap 域名的安全 DNS 记录管理功能：支持查询、添加、删除和备份 DNS 记录，并提供自动安全检查及试运行模式。有效防止因使用 Namecheap API 的 `setHosts` 方法而导致的 DNS 记录意外删除。
homepage: https://www.namecheap.com/support/api/
metadata:
  {
    "openclaw":
      {
        "emoji": "🌐",
        "requires": { "bins": ["node", "npm"] },
      },
  }
---

# Namecheap DNS Management

这是一个用于操作Namecheap DNS服务的安全封装工具，通过先获取现有DNS记录并合并更改来**防止意外删除记录**。

## ⚠️ 为什么需要这个工具

Namecheap的`setHosts`方法会**替换一个域名的所有DNS记录**。一旦API调用出错，你的整个DNS配置就会丢失。而这个工具可以：
- ✅ 总是先获取现有记录
- ✅ 将新记录与现有记录合并（除非明确要求替换）
- ✅ 在应用更改前显示差异预览
- ✅ 在每次更改前自动备份
- ✅ 支持模拟测试模式
- ✅ 通过一个命令从备份中恢复更改

## 设置

### 1. 安装依赖项

```bash
cd ~/.openclaw/workspace/skills/namecheap-dns
npm install
```

### 2. 启用Namecheap API访问

1. 访问 https://ap.www.namecheap.com/settings/tools/apiaccess/
2. 打开“API Access”选项
3. 将你的IP地址添加到白名单中
4. 复制你的API密钥

### 3. 设置环境变量

将以下内容添加到`~/.zshrc`或`~/.bashrc`文件中：

```bash
export NAMECHEAP_API_KEY="your-api-key-here"
export NAMECHEAP_USERNAME="your-username"
export NAMECHEAP_API_USER="your-username"  # Usually same as username
```

## 使用方法

### 验证DNS记录并检测“幽灵记录”

**⚠️ 重要：请先运行此命令！**

```bash
./namecheap-dns.js verify example.com
```

该命令会比较Namecheap API显示的DNS记录与实际的DNS记录（通过`dig`获取）。它会警告你那些存在于DNS中但API无法检测到的“幽灵记录”（例如邮件转发、URL重定向等）。

### 列出当前的DNS记录

```bash
./namecheap-dns.js list example.com
```

**注意：** 这仅显示API能看到的记录。使用`verify`命令可以查看所有记录，包括Namecheap子系统管理的记录。

### 添加记录（安全合并）

```bash
# Add a single TXT record
./namecheap-dns.js add example.com \
  --txt "mail.example.com=v=spf1 include:mailgun.org ~all"

# Add multiple records at once
./namecheap-dns.js add example.com \
  --txt "mail=v=spf1 include:mailgun.org ~all" \
  --cname "email.mail=mailgun.org" \
  --mx "mail=10 mxa.mailgun.org"

# Dry-run (preview changes without applying)
./namecheap-dns.js add example.com \
  --txt "test=hello" \
  --dry-run

# Force override safety check (if you know ghost records can be deleted)
./namecheap-dns.js add example.com \
  --txt "test=hello" \
  --force
```

**安全性：** 该工具会在进行更改前自动检查“幽灵记录”。如果检测到幽灵记录，除非使用`--force`选项，否则不会继续执行操作。

### 删除记录

```bash
# Remove by host + type
./namecheap-dns.js remove example.com \
  --host "old-record" \
  --type "TXT"

# Dry-run first
./namecheap-dns.js remove example.com \
  --host "old-record" \
  --type "TXT" \
  --dry-run
```

### 备份与恢复

```bash
# Create manual backup
./namecheap-dns.js backup example.com

# List available backups
./namecheap-dns.js backups example.com

# Restore from latest backup
./namecheap-dns.js restore example.com

# Restore from specific backup
./namecheap-dns.js restore example.com \
  --backup "example.com-20260213-114500.json"
```

## 记录格式

### TXT记录
```
--txt "subdomain=value"
--txt "@=value"  # Root domain
```

### CNAME记录
```
--cname "subdomain=target.com"
```

### MX记录
```
--mx "subdomain=10 mx.target.com"
--mx "@=10 mx.target.com"  # Root domain
```

### A记录
```
--a "subdomain=192.168.1.1"
--a "@=192.168.1.1"  # Root domain
```

## 备份位置

**默认路径：** `./backups/`（相对于工具目录）

**可通过环境变量配置：**
```bash
export NAMECHEAP_BACKUP_DIR="/custom/path/to/backups"
```

备份文件格式：`{domain}-{timestamp}.json`

每个备份文件包含：
- `apiHosts`：Namecheap API能看到的记录
- `liveDNS`：通过`dig`获取的实际DNS记录
- 时间戳和域名元数据

这样你可以看到DNS中实际存在的记录，而不仅仅是API所知的记录。

## 安全特性

1. **幽灵记录检测** — 自动检查API无法检测到的记录
2. **更改前自动备份** — 每次添加或删除记录时都会创建带有时间戳的备份
3. **模拟测试模式** — 使用`--dry-run`可以查看更改内容而不会实际应用
4. **差异预览** — 明确显示哪些记录将被添加或删除
5. **先获取数据** — 在进行更改前总是先获取当前的DNS状态
6. **合并逻辑** — 将新记录添加到现有记录中，而不是替换它们
7. **恢复功能** — 通过一个命令从备份中恢复数据
8. **安全覆盖** — 使用`--force`标志可以忽略幽灵记录的警告

## 示例

### 配置Mailgun

```bash
./namecheap-dns.js add menuhq.ai \
  --txt "mail.menuhq.ai=v=spf1 include:mailgun.org ~all" \
  --txt "smtp._domainkey.mail.menuhq.ai=k=rsa; p=MIGfMA0..." \
  --txt "_dmarc.mail.menuhq.ai=v=DMARC1; p=quarantine;" \
  --cname "email.mail.menuhq.ai=mailgun.org" \
  --mx "mail.menuhq.ai=10 mxa.mailgun.org" \
  --mx "mail.menuhq.ai=20 mxb.mailgun.org" \
  --dry-run
```

查看差异后，不使用`--dry-run`选项直接执行命令以应用更改。

## 已知限制

### ⚠️ Namecheap API的破坏性

Namecheap的`domains.dns.setHosts`方法会**替换一个域名的所有DNS记录**。没有单独的“添加一条记录”或“更新一条记录”的接口。每次更改都需要：
1. 获取所有现有记录（`getHosts`）
2. 修改记录列表
3. 上传整个记录列表（`setHosts`）

这个工具通过先获取记录并合并更改来避免这些问题。

### 🔍 幽灵记录：隐藏的危险

**问题：** `domains.dns.hosts`方法不会返回所有DNS记录。Namecheap子系统管理的记录对API是不可见的，例如：
- **邮件转发** — MX、SPF和DKIM记录
- **URL重定向** — 用于域名停放/重定向的A/CNAME记录
- **第三方集成** — 通过Namecheap控制台添加的记录

由于`setHosts`方法会替换所有记录，使用API可能会无意中删除这些隐藏的记录。

### 🛡️ 该工具如何保护你

1. **`verify`命令** — 将API记录与实际DNS记录进行比较（通过`dig`），并警告幽灵记录的存在
2. **自动安全检查** — 在执行任何添加、删除或恢复操作前，该工具会检查是否存在幽灵记录
3. **阻止操作** — 如果检测到幽灵记录，操作将被阻止（除非使用`--force`）
4. **明确显示警告** — 显示如果继续操作将会丢失哪些记录
5. **备份中的DNS快照** — 通过`dig`获取实际的DNS状态，而不仅仅是API的状态

### 何时使用`--force`选项

只有在以下情况下才使用`--force`选项：
- 你已手动确认不再需要这些幽灵记录
- 你明确要删除邮件转发或URL重定向功能
- 你理解并接受这些记录会被删除

**切勿盲目使用`--force`选项。** 必须先使用`verify`命令确认哪些记录会被删除。

### 示例：生产环境中的事故

这个工具是在通过API添加Mailgun DNS记录后，导致Namecheap的邮件转发记录被删除的情况下开发的。由于`getHosts`方法无法检测到这些邮件转发记录，因此原来的操作模式会直接删除它们。

现在，这个工具会在执行操作前：
1. 在`verify`步骤中检测到幽灵记录
2. 拒绝执行操作（除非使用`--force`）
3. 明确显示哪些邮件转发记录会被删除
4. 创建包含DNS快照的备份

## 故障排除

### “API请求失败：IP未添加到白名单”
- 将你的IP地址添加到 https://ap.www.namecheap.com/settings/tools/apiaccess/
- 使用`curl ifconfig.me`检查IP地址是否在白名单中

### “API密钥无效”
- 确保`NAMECHEAP_API_KEY`设置正确
- 如有需要，重新启用API访问

### “域名未找到”
- 确保域名存在于你的Namecheap账户中
- 检查拼写（区分大小写）

## API参考

Namecheap API文档：https://www.namecheap.com/support/api/methods/domains-dns/
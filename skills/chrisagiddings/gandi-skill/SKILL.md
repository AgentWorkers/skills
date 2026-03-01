---
name: gandi
description: "Gandi域名注册商的全面集成，支持域名和DNS管理功能：  
- 注册和管理域名；  
- 创建/更新/删除DNS记录（A、AAAA、CNAME、MX、TXT、SRV等）；  
- 配置电子邮件转发和别名；  
- 检查SSL证书状态；  
- 创建DNS快照以实现安全回滚；  
- 批量更新区域文件；  
- 监控域名到期时间。  
- 支持多域名管理、区域文件导入/导出以及自动化的DNS备份功能；  
- 提供只读和修改操作模式，并配备相应的安全控制机制。"
disable-model-invocation: true
metadata: {"openclaw":{"version":"0.2.7","disable-model-invocation":true,"capabilities":["dns-modification","email-management","domain-registration","destructive-operations"],"credentials":{"type":"file","location":"~/.config/gandi/api_token","description":"Gandi Personal Access Token (PAT)","permissions":600},"requires":{"bins":["node","npm"],"env":["GANDI_API_TOKEN"]},"primaryEnv":"GANDI_API_TOKEN"}}
---
# Gandi域名注册商技能

本技能实现了与Moltbot的全面集成，用于管理Gandi域名注册商的相关功能。

**状态：** ✅ 第二阶段已完成 - DNS记录修改和快照功能已启用

## ⚠️ 安全警告

**本技能可能对您的Gandi账户执行破坏性操作：**

- **DNS修改：** 添加、更新或删除DNS记录（可能导致网站或电子邮件服务中断）
- **电子邮件管理：** 创建、修改或删除邮件转发规则（可能导致邮件被截获）
- **域名注册：** 注册新域名（会产生财务交易）
- **批量操作：** 一次性替换所有DNS记录（除非使用快照，否则无法撤销）

**在运行任何脚本之前：**
1. 仔细阅读脚本代码，了解其功能。
2. 在进行批量修改之前，先使用`create-snapshot.js`创建DNS快照。
3. 尽可能使用只读的个人访问令牌（Personal Access Tokens）。
4. 先在非生产环境中测试脚本。
5. 请注意，某些操作是不可撤销的。

**具有破坏性的脚本**（⚠️ 可能修改或删除数据）：
- `add-dns-record.js`
- `delete-dns-record.js`
- `update-dns-bulk.js`
- `add-email-forward.js`
- `update-email-forward.js`
- `delete-email-forward.js`
- `restore-snapshot.js`（用于恢复DNS记录）

**只读脚本**（✅ 安全，不会修改数据）：
- `list-domains.js`
- `list-dns.js`
- `list-snapshots.js`
- `list-email-forwards.js`
- `check-domain.js`
- `check-ssl.js`

📖 **有关完整脚本文档，请参阅[SCRIPTS.md]**，其中包含以下信息：
- 每个脚本的功能
- 网络操作和API调用
- 安全影响
- 撤销/恢复流程
- 审计工作流程建议

## 当前功能

### 第一阶段（已完成）
- ✅ 个人访问令牌认证
- ✅ 列出您账户中的所有域名
- ✅ 获取域名详情（到期时间、状态、服务信息）
- ✅ 查看域名的DNS记录
- ✅ 查看域名和DNS信息
- ✅ **域名可用性检查** ([#4](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/4))
- ✅ 域名建议功能（包括多种变体） ([#4](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/4))
- ✅ SSL证书状态检查
- ✅ 错误处理和验证

### 第二阶段（已完成）
- ✅ **添加/更新DNS记录**（A、AAAA、CNAME、MX、TXT、NS、SRV、CAA、PTR）
- ✅ **删除DNS记录**
- ✅ **批量DNS操作**（一次性替换所有记录）
- ✅ **DNS区域快照**（创建、列出、恢复）
- ✅ **邮件转发**（创建、列出、更新、删除转发规则，包括通配符转发）
- ✅ **记录验证**（自动验证每种类型的记录）
- ✅ **安全功能**（在批量修改前自动创建快照，提供确认提示）

## 即将推出的功能（第三阶段及以后）
- 域名注册
- 多组织支持 ([#1](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/1))
- Gateway Console配置 ([#3](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/3))
- 域名续订管理
- DNSSEC配置
- 证书管理
- 邮箱管理（不仅仅是转发功能）

## 设置

### 第一步：创建个人访问令牌

**⚠️ 安全建议：** 根据您的使用需求，仅选择所需的权限范围。

1. 访问 [Gandi Admin → Personal Access Tokens](https://admin.gandi.net/organizations/account/pat)。
2. 点击“Create a token”（创建令牌）。
3. 选择您的组织。
4. 选择权限范围：
   - **只读（推荐用于查看）：**
     - ✅ Domain: read（列出域名所需）
     - ✅ LiveDNS: read（查看DNS记录所需）
     - ✅ Email: read（查看邮件转发规则所需）
   - **写入权限（修改操作需要谨慎使用）：**
     - ⚠️ LiveDNS: write（允许修改DNS记录、删除记录、执行批量操作）
     - ⚠️ Email: write（允许创建、更新或删除邮件转发规则）

5. 复制令牌（此后的步骤中将无法再次看到令牌内容！）

**安全最佳实践：**
- 为只读操作和写入操作创建不同的令牌。
- 使用只读令牌进行常规检查/监控。
- 仅在需要主动修改时使用写入令牌。
- 定期轮换令牌（建议每90天轮换一次）。
- 立即删除未使用的令牌。
- **切勿将令牌共享或提交到版本控制系统中。**

### 第二步：存储令牌

脚本会按优先顺序检查凭据：
1. **`GANDI_API_TOKEN` 环境变量**（优先检查）
2. **`~/.config/gandi/api_token` 文件**（如果环境变量未设置，则作为备用）

**选择适合您工作流程的方法：**

#### 选项A：环境变量（推荐用于CI/CD）
```bash
# Set environment variable (replace YOUR_PAT with actual token)
export GANDI_API_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"

# Add to shell profile for persistence (~/.bashrc, ~/.zshrc, etc.)
echo 'export GANDI_API_TOKEN="YOUR_PERSONAL_ACCESS_TOKEN"' >> ~/.bashrc
```

**优点：**
- ✅ 适合CI/CD自动化流程
- ✅ 适用于容器环境（无需挂载文件）
- ✅ 可与秘密管理工具（如1Password、Vault等）配合使用
- ✅ 可轻松切换不同的令牌

#### 选项B：基于文件的存储（推荐用于本地开发）
```bash
# Create config directory
mkdir -p ~/.config/gandi

# Store your token (replace YOUR_PAT with actual token)
echo "YOUR_PERSONAL_ACCESS_TOKEN" > ~/.config/gandi/api_token

# Secure the file (owner read-only)
chmod 600 ~/.config/gandi/api_token
```

**优点：**
- ✅ 令牌在shell会话间保持有效
- ✅ 文件权限设置安全（0600权限，仅允许所有者读取）
- ✅ 避免在进程列表中泄露令牌
- ✅ 可在离线环境下使用（无需外部依赖）

### 第三步：安装依赖项

**要求：** Node.js >= 18.0.0

```bash
cd gandi-skill/scripts

# Install npm dependencies
npm install

# Verify installation
npm list --depth=0
```

**需要的包：**
- axios（用于与Gandi API通信的HTTP客户端）
- `package.json` 中列出的其他依赖项

**故障排除：**
- 如果找不到`node`或`npm`，请从 [nodejs.org](https://nodejs.org/) 安装Node.js。
- 如果遇到权限问题，请不要使用`sudo`，而是调整npm权限或使用nvm。
- 如果遇到包安装问题，请删除`node_modules/`和`package-lock.json`，然后重新运行`npm install`。

### 第四步：测试认证

```bash
cd gandi-skill/scripts
node test-auth.js
```

预期输出：
```
✅ Authentication successful!

Your organizations:
  1. Personal Account (uuid-here)
     Type: individual

🎉 You're ready to use the Gandi skill!
```

### 第五步：设置联系信息（可选，用于域名注册）

如果您计划注册域名，请保存一次联系信息以供后续使用：

```bash
cd gandi-skill/scripts
node setup-contact.js
```

脚本会要求您提供以下信息：
- 姓名（名和姓）
- 电子邮件地址
- 电话号码（国际格式：+1.5551234567）
- 街道地址
- 城市
- 州/省（例如美国：使用2位代码，如OH，系统会自动格式化为US-OH）
- 邮政编码
- 国家（2位代码：如US、FR等）
- 身份类型（个人或公司）
- **隐私设置：** 是否在注册后保留联系信息

**联系信息保存位置：**
- `~/.config/gandi/contact.json`
- 权限设置：600（仅允许所有者读写）
- 该文件位于技能目录之外（不会被提交到git仓库）

**隐私设置：**
1. **保留（默认设置）：** 在未来注册时继续使用已保存的联系信息
   - 适合频繁注册域名的用户
   - 仅需设置一次，永久有效
   - 可随时使用`delete-contact.js`删除联系信息

**管理已保存的联系信息：**
```bash
# View current contact
node view-contact.js

# Update contact info or privacy preference
node setup-contact.js

# Delete saved contact manually
node delete-contact.js

# Delete without confirmation
node delete-contact.js --force
```

**一次性删除联系信息的设置：**
```bash
# Register and delete contact (even if preference is "retain")
node register-domain.js example.com --purge-contact
```

## 使用示例

### 列出您的域名

```bash
node list-domains.js
```

输出内容包括：
- 域名
- 到期日期
- 自动续订状态
- 服务类型（如LiveDNS、电子邮件等）
- 组织所有权信息

### 列出DNS记录

```bash
node list-dns.js example.com
```

输出内容包括：
- 按类型分类的所有DNS记录
- TTL值
- 记录名称和值
- 名服务器信息

### 通过Moltbot使用

配置完成后，您可以使用自然语言命令来执行操作：
- “列出我的Gandi域名”
- “显示example.com的DNS记录”
- “example.com的到期时间是什么？”
- “example.com是否启用了自动续订？”

## 域名可用性检查

### 检查单个域名的可用性

检查特定域名是否可以注册：

```bash
node check-domain.js example.com
```

**功能：**
- 显示域名是否可用（可用/不可用/待处理/错误状态）
- 显示价格信息（注册、续订、转移等选项）
- 列出支持的功能（如DNSSEC、LiveDNS等）
- 显示顶级域名（TLD）信息

**示例输出：**
```
🔍 Checking availability for: example.com

Domain: example.com

✅ Status: AVAILABLE

💰 Pricing:
  1 year: 12.00 EUR (+ 2.40 tax)
  2 years: 24.00 EUR (+ 4.80 tax)

📋 Supported Features:
  • create
  • dnssec
  • livedns

🌐 TLD Information:
  Extension: com
```

### 域名建议功能

提供带有不同顶级域名和名称变体的建议：

```bash
# Check all configured TLDs + variations
node suggest-domains.js example

# Check specific TLDs only
node suggest-domains.js example --tlds com,net,io

# Skip name variations (only check TLDs)
node suggest-domains.js example --no-variations

# Output as JSON
node suggest-domains.js example --json
```

**名称变体规则：**
- **添加连字符**：在单词之间添加连字符（例如 `example` → `ex-ample`）
- **缩写**：删除元音（例如 `example` → `exmpl`）
- **添加前缀**：添加常见前缀（例如 `example` → `get-example`、`my-example`）
- **添加后缀**：添加常见后缀（例如 `example` → `example-app`、`example-hub`）
- **添加数字**：在域名后添加数字（例如 `example` → `example2`、`example3`）

**示例输出：**
```
🔍 Checking availability for: example

📊 Checking 13 TLDs and generating variations...

═══════════════════════════════════════════════════════
📋 EXACT MATCHES (Different TLDs)
═══════════════════════════════════════════════════════

✅ Available:

  example.net                    12.00 EUR
  example.io                     39.00 EUR
  example.dev                    15.00 EUR

❌ Unavailable:

  example.com                    (unavailable)
  example.org                    (unavailable)

═══════════════════════════════════════════════════════
🎨 NAME VARIATIONS
═══════════════════════════════════════════════════════

Hyphenated:

  ✅ ex-ample.com                12.00 EUR

Prefix:

  ✅ get-example.com             12.00 EUR
  ✅ my-example.com              12.00 EUR

Suffix:

  ✅ example-app.com             12.00 EUR
  ✅ example-io.com              12.00 EUR

═══════════════════════════════════════════════════════
📊 SUMMARY: 8 available domains found
═══════════════════════════════════════════════════════
```

### 配置

域名检查器的配置文件位于 `gandi-skill/config/domain-checker-defaults.json`。

**文件结构：**
```json
{
  "tlds": {
    "mode": "extend",
    "defaults": ["com", "net", "org", "info", "io", "dev", "app", "ai", "tech"],
    "custom": []
  },
  "variations": {
    "enabled": true,
    "patterns": ["hyphenated", "abbreviated", "prefix", "suffix", "numbers"],
    "prefixes": ["get", "my", "the", "try"],
    "suffixes": ["app", "hub", "io", "ly", "ai", "hq"],
    "maxNumbers": 3
  },
  "rateLimit": {
    "maxConcurrent": 3,
    "delayMs": 200,
    "maxRequestsPerMinute": 100
  },
  "limits": {
    "maxTlds": 5,
    "maxVariations": 10
  }
}
```

**速率限制和限制：**
- **maxConcurrent**：最大并发API请求数量（默认值：3）
- **delayMs**：请求之间的延迟时间（以毫秒为单位）（默认值：200ms）
- **maxRequestsPerMinute**：每分钟的请求上限（默认值：100，Gandi允许的最大值为1000）
- **maxTlds**：在`suggest-domains.js`中检查的顶级域名数量（默认值：5）
- **maxVariations**：生成的名称变体数量（默认值：10）

这些限制有助于合理使用API，避免过度负担Gandi的API服务。

**顶级域名模式：**
- `"extend"`：使用默认设置和自定义顶级域名（合并后的列表）
- `"replace"`：仅使用自定义顶级域名（忽略默认设置）

**Gateway Console集成：**

当添加Gateway Console支持后（[#3](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/3)），配置信息将位于以下位置：

```yaml
skills:
  entries:
    gandi:
      config:
        domainChecker:
          tlds:
            mode: extend
            defaults: [...]
            custom: [...]
          variations:
            enabled: true
            patterns: [...]
```

有关完整的配置架构，请参阅 `docs/gateway-config-design.md`。

## DNS管理（第二阶段）

### 添加或更新DNS记录

创建或更新单个DNS记录：

```bash
# Add an A record for root domain
node add-dns-record.js example.com @ A 192.168.1.1

# Add www subdomain pointing to root
node add-dns-record.js example.com www CNAME @

# Add MX record for email
node add-dns-record.js example.com @ MX "10 mail.example.com."

# Add TXT record for SPF
node add-dns-record.js example.com @ TXT "v=spf1 include:_spf.google.com ~all"

# Add with custom TTL (5 minutes)
node add-dns-record.js example.com api A 192.168.1.10 300
```

**支持的记录类型：** A、AAAA、CNAME、MX、TXT、NS、SRV、CAA、PTR

### 删除DNS记录

删除特定的DNS记录：

```bash
# Delete old A record
node delete-dns-record.js example.com old A

# Delete with confirmation prompt
node delete-dns-record.js example.com test CNAME

# Delete without confirmation
node delete-dns-record.js example.com old A --force
```

### 批量DNS操作

一次性替换所有DNS记录：

```bash
# From JSON file
node update-dns-bulk.js example.com new-records.json

# From stdin
cat records.json | node update-dns-bulk.js example.com

# Skip automatic snapshot
node update-dns-bulk.js example.com records.json --no-snapshot

# Skip confirmation
node update-dns-bulk.js example.com records.json --force
```

**JSON格式：**
```json
[
  {
    "rrset_name": "@",
    "rrset_type": "A",
    "rrset_ttl": 10800,
    "rrset_values": ["192.168.1.1"]
  },
  {
    "rrset_name": "www",
    "rrset_type": "CNAME",
    "rrset_ttl": 10800,
    "rrset_values": ["@"]
  },
  {
    "rrset_name": "@",
    "rrset_type": "MX",
    "rrset_ttl": 10800,
    "rrset_values": ["10 mail.example.com.", "20 mail2.example.com."]
  }
]
```

### DNS区域快照

在修改之前创建安全备份：

```bash
# Create a snapshot
node create-snapshot.js example.com "Before migration"

# List all snapshots
node list-snapshots.js example.com

# Restore from a snapshot
node restore-snapshot.js example.com abc123-def456-ghi789

# Restore without confirmation
node restore-snapshot.js example.com abc123-def456-ghi789 --force
```

**自动快照：**
- 批量更新会自动创建快照（除非指定了`--no-snapshot`选项）
- 快照会带有时间戳
- 可使用快照轻松恢复到之前的配置

### 常见的DNS配置示例

#### 基本网站设置
```bash
# Root domain
node add-dns-record.js example.com @ A 192.168.1.1

# WWW subdomain
node add-dns-record.js example.com www CNAME @
```

#### 邮件配置（Google Workspace）
```bash
# MX records
node add-dns-record.js example.com @ MX "1 ASPMX.L.GOOGLE.COM."
node add-dns-record.js example.com @ MX "5 ALT1.ASPMX.L.GOOGLE.COM."
node add-dns-record.js example.com @ MX "5 ALT2.ASPMX.L.GOOGLE.COM."

# SPF record
node add-dns-record.js example.com @ TXT "v=spf1 include:_spf.google.com ~all"
```

#### 域名重定向设置

将一个域名重定向到另一个域名：

```bash
# Point root domain to same server
node add-dns-record.js old-domain.com @ A 192.168.1.1

# Point www to same CNAME
node add-dns-record.js old-domain.com www CNAME @
```

随后需要在服务器层面配置HTTP 301重定向规则。

#### 子域名设置
```bash
# API subdomain
node add-dns-record.js example.com api A 192.168.1.10

# Staging subdomain
node add-dns-record.js example.com staging A 192.168.1.20

# Wildcard subdomain
node add-dns-record.js example.com "*" A 192.168.1.100
```

## 邮件转发（第二阶段）

### 列出邮件转发规则

查看某个域名配置的所有邮件转发规则：

```bash
node list-email-forwards.js example.com
```

### 创建邮件转发规则

将邮件转发到一个或多个目的地：

```bash
# Simple forward
node add-email-forward.js example.com hello you@personal.com

# Forward to multiple destinations
node add-email-forward.js example.com support team1@example.com team2@example.com

# Catch-all forward (forwards all unmatched emails)
node add-email-forward.js example.com @ catchall@example.com
```

### 更新邮件转发规则

更改现有邮件的转发目的地：

```bash
# Update single destination
node update-email-forward.js example.com hello newemail@personal.com

# Update to multiple destinations
node update-email-forward.js example.com support new1@example.com new2@example.com
```

**注意：** 这会替换所有现有的转发规则。

### 删除邮件转发规则

删除邮件转发规则：

```bash
# Delete with confirmation prompt
node delete-email-forward.js example.com old

# Delete without confirmation
node delete-email-forward.js example.com old --force

# Delete catch-all forward
node delete-email-forward.js example.com @ --force
```

### 常见的邮件转发使用场景

#### 基本邮件转发
```bash
# Forward contact@ to your personal email
node add-email-forward.js example.com contact you@gmail.com

# Forward sales@ to team
node add-email-forward.js example.com sales team@example.com
```

#### 域名迁移时的邮件转发
```bash
# Forward all email from old domain to new domain
# Preserves the local part (username before @)

# First, list existing forwards on old domain
node list-email-forwards.js old-domain.com

# Then create matching forwards on new domain
node add-email-forward.js old-domain.com contact contact@new-domain.com
node add-email-forward.js old-domain.com support support@new-domain.com

# Or use catch-all to forward everything
node add-email-forward.js old-domain.com @ admin@new-domain.com
```

#### 团队邮件分发列表
```bash
# Forward to entire team
node add-email-forward.js example.com team alice@example.com bob@example.com charlie@example.com

# Update team members
node update-email-forward.js example.com team alice@example.com dave@example.com
```

#### 通配符转发设置
```bash
# Forward all unmatched emails to one address
node add-email-forward.js example.com @ catchall@example.com

# Forward all unmatched emails to multiple addresses
node add-email-forward.js example.com @ admin1@example.com admin2@example.com
```

**注意：** 通配符转发仅适用于没有指定具体转发规则的邮件地址。

### 邮件转发管理提示：
1. **创建后进行测试：** 发送测试邮件以确认转发是否正常工作。
2. **优先使用具体的转发规则**：这样可以更好地控制转发行为，也更容易管理。
3. **多个目的地：** 邮件会同时发送到所有指定目的地。
4. **顺序无关紧要：** Gandi会优先处理最匹配的规则。
5. **检查垃圾邮件文件夹：** 被转发的邮件可能会被收件人的垃圾邮件过滤器过滤。

### 完整的域名邮件设置示例
```bash
# 1. Set up MX records (if not already done)
node add-dns-record.js example.com @ MX "10 spool.mail.gandi.net."
node add-dns-record.js example.com @ MX "50 fb.mail.gandi.net."

# 2. Create specific forwards
node add-email-forward.js example.com hello you@personal.com
node add-email-forward.js example.com support team@example.com
node add-email-forward.js example.com sales sales-team@example.com

# 3. Set up catch-all for everything else
node add-email-forward.js example.com @ admin@example.com

# 4. List all forwards to verify
node list-email-forwards.js example.com
```

## 辅助脚本

所有脚本都位于 `gandi-skill/scripts/` 目录下：

### 认证和设置
| 脚本 | 功能 |
|--------|---------|
| `test-auth.js` | 验证认证是否正常工作 |
| `setup-contact.js` | 保存用于域名注册的联系信息（仅运行一次） |
| `view-contact.js` | 查看保存的联系信息 |
| `delete-contact.js` | 删除保存的联系信息（可选参数`--force`） |

### 域名和DNS信息查看
| 脚本 | 功能 |
|--------|---------|
| `list-domains.js` | 显示账户中的所有域名 |
| `list-dns.js <domain>` | 显示该域名的DNS记录 |
| `check-domain.js <domain>` | 检查单个域名的可用性和价格信息 |
| `suggest-domains.js <name>` | 提供带有变体的域名建议 |
| `check-ssl.js` | 检查所有域名的SSL证书状态 |

### DNS修改（第二阶段）
| 脚本 | 功能 |
|--------|---------|
| `add-dns-record.js <domain> <name> <type> <value> [ttl]` | 添加或更新DNS记录 |
| `delete-dns-record.js <domain> <name> <type> [--force]` | 删除DNS记录 |
| `update-dns-bulk.js <domain> <records.json> [--no-snapshot] [--force]` | 批量更新所有DNS记录 |
| `list-snapshots.js <domain>` | 列出DNS区域的快照 |
| `create-snapshot.js <domain> [name]` | 创建DNS区域的快照 |
| `restore-snapshot.js <domain> <snapshot-id> [--force]` | 从快照恢复DNS区域的配置 |

### 邮件转发（第二阶段）
| 脚本 | 功能 |
|--------|---------|
| `list-email-forwards.js <domain>` | 查看某个域名的所有邮件转发规则 |
| `add-email-forward.js <domain> <mailbox> <destination> [dest2...]` | 创建邮件转发规则（使用`@`符号表示通配符） |
| `update-email-forward.js <domain> <mailbox> <destination> [dest2...]` | 更新邮件转发的目的地 |
| `delete-email-forward.js <domain> <mailbox> [--force]` | 删除邮件转发规则 |

### 核心库
| 脚本 | 功能 |
|--------|---------|
| `gandi-api.js` | 核心API客户端（可导入） |

## 配置

### 默认配置
- **令牌文件：** `~/.config/gandi/api_token`（用于API认证）
- **联系信息文件：** `~/.config/gandi/contact.json`（用于域名注册信息，可选）
- **API地址：** `https://api.gandi.net`（生产环境）

### 沙箱测试

要使用Gandi的沙箱环境，请执行以下操作：

```bash
# Create sandbox token at: https://admin.sandbox.gandi.net
echo "YOUR_SANDBOX_TOKEN" > ~/.config/gandi/api_token
echo "https://api.sandbox.gandi.net" > ~/.config/gandi/api_url
```

## 故障排除

### 令牌未找到

```bash
# Verify file exists
ls -la ~/.config/gandi/api_token

# Should show: -rw------- (600 permissions)
```

### 认证失败（401）

- 令牌错误或已过期
- 请在Gandi Admin中创建新的令牌。
- 更新存储的令牌文件。

### 权限被拒绝（403）

- 令牌没有所需的权限范围
- 请创建新的令牌，确保包含 `Domain:read` 和 `LiveDNS:read` 权限。
- 确认您的组织是否已注册Gandi并具有相应权限。

### 域名未启用LiveDNS

如果出现“未启用Gandi LiveDNS”的错误：
1. 登录Gandi Admin。
2. 进入域名管理页面。
3. 为该域名启用LiveDNS服务。

### 速率限制（429）

Gandi允许每分钟最多1000次API请求。如果超出限制：
- 等待60秒后再次尝试。
- 减少API请求的频率。

## API参考

本技能提供了可导入的API函数：

```javascript
import { 
  testAuth,
  listDomains,
  getDomain,
  listDnsRecords,
  getDnsRecord,
  checkAvailability
} from './gandi-api.js';

// Test authentication
const auth = await testAuth();

// List domains
const domains = await listDomains();

// Get domain info
const domain = await getDomain('example.com');

// List DNS records
const records = await listDnsRecords('example.com');

// Get specific DNS record
const record = await getDnsRecord('example.com', '@', 'A');

// Check availability
const available = await checkAvailability(['example.com', 'example.net']);
```

## 安全性

### 令牌存储

✅ **推荐做法：**
- 将令牌存储在 `~/.config/gandi/api_token` 文件中。
- 设置权限为600（仅允许所有者读取）。
- 定期轮换令牌。
- 仅使用必要的权限范围。

❌ **禁止的做法：**
- 将令牌提交到版本控制系统中。
- 在用户之间共享令牌。
- 给令牌分配不必要的权限。
- 将令牌存储在脚本中。

### 令牌权限范围

**当前阶段（第一阶段）：**
- Domain: read
- LiveDNS: read

**未来阶段（第二阶段及以后）：**
- Domain: read, write（用于域名注册和续订）
- LiveDNS: read, write（用于DNS记录的修改）
- Certificate: read（可选，用于SSL证书相关操作）
- Email: read, write（可选，用于邮件配置）

## 架构

```
gandi-skill/
├── SKILL.md                 # This file
├── references/              # API documentation
│   ├── api-overview.md
│   ├── authentication.md
│   ├── domains.md
│   ├── livedns.md
│   └── setup.md
└── scripts/                 # Helper utilities
    ├── package.json
    ├── gandi-api.js         # Core API client
    ├── test-auth.js         # Test authentication
    ├── list-domains.js      # List domains
    └── list-dns.js          # List DNS records
```

## 开发路线图

**第一阶段：读取操作**（已完成）
- 使用个人访问令牌（PAT）进行认证
- 列出域名
- 获取域名详情
- 查看DNS记录
- 基本错误处理

**第二阶段：DNS修改**
- 添加DNS记录
- 更新DNS记录
- 删除DNS记录
- 批量DNS操作

**第三阶段：域名管理**
- 域名注册
- 域名续订
- 自动续订设置
- 名服务器管理

**第四阶段：多组织支持** ([#1](https://github.com/chrisagiddings/moltbot-gandi-skill/issues/1))
- 基于用户角色的令牌管理
- 多组织支持
- 多个令牌的使用

**第五阶段：高级功能**
- DNSSEC管理
- 证书管理
- 邮箱配置
- 域名转移操作

## 贡献代码

请参阅主README文件中的 [贡献指南](../../README.md#contributing)。

## 支持方式

- **问题报告：** [GitHub Issues](https://github.com/chrisagiddings/moltbot-gandi-skill/issues)
- **文档参考：** [参考指南](./references/)
- **Gandi支持：** [help.gandi.net](https://help.gandi.net/)

## 许可证

本技能采用MIT许可证。详细信息请参阅 [LICENSE](../../LICENSE)。
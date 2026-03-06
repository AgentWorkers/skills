---
name: controld
description: "通过 API 管理 Control D 的 DNS 过滤服务。该服务可用于 DNS 配置文件管理、设备配置、自定义阻止规则、服务过滤、分析设置以及网络诊断。当用户提及 Control D、DNS 过滤、DNS 阻止、设备 DNS 设置或 DNS 配置文件管理时，系统会触发相关操作。"
homepage: https://controld.com
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["curl", "jq"] }, "primaryEnv": "CONTROLD_API_TOKEN" } }
---
# Control D DNS管理

Control D是一款提供DNS过滤和隐私保护服务的工具。通过此功能，您可以完全访问其API。

## 认证

您可以通过将API令牌存储在环境变量中或直接传递来使用API：
```bash
export CONTROLD_API_TOKEN="your-api-token"
```

您可以从以下链接获取API令牌：https://controld.com/dashboard（账户设置 > API）

**令牌类型：**
- **读取** - 仅限查看个人资料、设备和分析数据
- **写入** - 查看和修改数据（创建/修改/删除）

**安全提示：** 请为自动化主机限制可使用的IP地址，以增强安全性。

## API参考

基础URL：`https://api.controld.com`
认证方式：`Authorization: Bearer $CONTROLD_API_TOKEN`

### 个人资料

DNS过滤个人资料用于定义过滤规则、过滤器和服务控制设置。
```bash
# List all profiles
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles" | jq '.body.profiles'

# Create profile
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Profile"}' \
  "https://api.controld.com/profiles"

# Clone existing profile
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Cloned Profile","clone_profile_id":"PROFILE_ID"}' \
  "https://api.controld.com/profiles"

# Update profile
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Name"}' \
  "https://api.controld.com/profiles/PROFILE_ID"

# Delete profile
curl -s -X DELETE -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID"
```

### 个人资料选项

```bash
# List available profile options
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/options" | jq '.body.options'

# Update profile option (status: 1=enabled, 0=disabled)
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":1,"value":"some_value"}' \
  "https://api.controld.com/profiles/PROFILE_ID/options/OPTION_NAME"
```

### 设备

设备是通过个人资料进行DNS过滤的终端节点。
```bash
# List all devices
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/devices" | jq '.body.devices'

# List device types (icons)
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/devices/types" | jq '.body.types'

# Create device
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Home Router","profile_id":"PROFILE_ID","icon":"router"}' \
  "https://api.controld.com/devices"

# Update device
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Name","status":1}' \
  "https://api.controld.com/devices/DEVICE_ID"

# Delete device
curl -s -X DELETE -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/devices/DEVICE_ID"
```

**设备图标：** `desktop-windows`, `desktop-mac`, `desktop-linux`, `mobile-ios`, `mobile-android`, `browser-chrome`, `browser-firefox`, `browser-edge`, `browser-brave`, `browser-other`, `tv-apple`, `tv-android`, `tv-firetv`, `tv-samsung`, `tv`, `router-asus`, `router-ddwrt`, `router-firewalla`, `router-freshtomato`, `router-glinet`, `router-openwrt`, `router-opnsense`, `router-pfsense`, `router-synology`, `router-ubiquiti`, `router-windows`, `router-linux`, `router`

**设备状态：** `0` = 待处理，`1` = 活动中，`2` = 软禁用，`3` = 硬禁用

### 过滤器

为个人资料提供内置和外部过滤规则。
```bash
# List native filters for profile
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/filters" | jq '.body.filters'

# List external filters
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/filters/external" | jq '.body.filters'

# Enable/disable filter (status: 1=enabled, 0=disabled)
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":1}' \
  "https://api.controld.com/profiles/PROFILE_ID/filters/filter/FILTER_ID"
```

### 服务

您可以阻止、绕过或重定向特定的服务（应用程序/网站）。
```bash
# List service categories
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/services/categories" | jq '.body.categories'

# List services in category
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/services/categories/CATEGORY" | jq '.body.services'

# List profile services with their actions
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/services" | jq '.body.services'

# Set service action (do: 0=block, 1=bypass, 2=spoof)
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"do":0,"status":1}' \
  "https://api.controld.com/profiles/PROFILE_ID/services/SERVICE_ID"
```

### 自定义规则

您可以创建针对特定域名的自定义过滤/绕过规则。
```bash
# List rule folders
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/groups" | jq '.body.groups'

# Create rule folder
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Rules","do":0}' \
  "https://api.controld.com/profiles/PROFILE_ID/groups"

# Update rule folder
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"do":0,"status":1}' \
  "https://api.controld.com/profiles/PROFILE_ID/groups/FOLDER_ID"

# Delete rule folder
curl -s -X DELETE -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/groups/FOLDER_ID"

# List rules in folder
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/rules/FOLDER_ID" | jq '.body.rules'

# Create custom rule (do: 0=block, 1=bypass, 2=spoof, 3=redirect)
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"hostnames":["ads.example.com","tracking.example.com"],"do":0,"status":1}' \
  "https://api.controld.com/profiles/PROFILE_ID/rules"

# Delete custom rule
curl -s -X DELETE -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/rules/HOSTNAME"
```

**规则操作：**
- `0` = 阻止
- `1` = 绕过
- `2` = 通过代理进行解析（欺骗）
- `3` = 重定向

### 默认规则

为未匹配的域名设置默认操作。
```bash
# Get default rule
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/profiles/PROFILE_ID/default" | jq '.body.default'

# Set default rule
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"do":1,"status":1}' \
  "https://api.controld.com/profiles/PROFILE_ID/default"
```

### 代理

列出可用于流量重定向的代理位置。
```bash
# List all proxy locations
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/proxies" | jq '.body.proxies'
```

当将服务/规则操作设置为`2`（欺骗）时，请使用`via`参数指定代理的PK值。

### IP访问控制

您可以管理设备允许使用的IP地址。
```bash
# List known IPs for device
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"DEVICE_ID"}' \
  "https://api.controld.com/access" | jq '.body.ips'

# Learn new IPs
curl -s -X POST -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"DEVICE_ID","ips":["1.2.3.4","5.6.7.8"]}' \
  "https://api.controld.com/access"

# Delete learned IPs
curl -s -X DELETE -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"DEVICE_ID","ips":["1.2.3.4"]}' \
  "https://api.controld.com/access"
```

### 分析数据

您可以配置日志记录和存储设置。
```bash
# List available log levels (0=off, 1=basic, 2=full)
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/analytics/levels" | jq '.body.levels'

# List storage regions
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/analytics/endpoints" | jq '.body.endpoints'

# Get statistics for a device (requires Full analytics level)
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/stats?device_id=DEVICE_ID&start=2024-01-01&end=2024-01-31" | jq '.body'

# Get activity log (requires Full analytics level)
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/queries?device_id=DEVICE_ID&limit=100" | jq '.body.queries'
```

### 账户与网络

```bash
# Get account info
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/users" | jq '.body'

# Get current IP info
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/ip" | jq '.body'

# List network/resolver status
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/network" | jq '.body'
```

---

## 组织管理（企业账户）

使用企业账户可以管理多用户访问、子组织和团队部署功能。

**注意：** 请使用工作邮箱联系[[email protected]](mailto:[email protected])以申请企业账户权限。

企业账户的功能包括：
- 管理大量终端设备或网络
- 使用RMM快速部署数百/数千台设备
- 根据权限级别授予团队成员访问权限
- 将个人资料和终端节点分组到子组织中
- 在不同组织之间共享个人资料
- 将解析器锁定到特定的IP地址

### 组织

组织相关功能依赖于您的API令牌所关联的组织（路径中不包含`org_id`）。
```bash
# View organization info (your organization context)
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/organizations/organization" | jq '.body'

# Modify organization settings
curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "name=Updated Org Name&twofa_req=1" \
  "https://api.controld.com/organizations"
```

**修改组织参数（均为可选）：**
- `name`（字符串）——组织名称
- `contact_email`（字符串）——主要联系人的电子邮件地址
- `twofa_req`（整数）——是否要求成员使用双因素认证（0=不需要，1=需要）
- `stats_endpoint`（字符串）——来自`/analytics/endpoints`的存储区域PK
- `max_users`（整数）——最大用户设备数量
- `max_routers`（整数）——最大路由器设备数量
- `address`（字符串）——物理地址
- `website`（字符串）——网站URL
- `contact_name`（字符串）——联系人姓名
- `contact_phone`（字符串）——联系电话号码
- `parent_profile`（字符串）——应用于所有设备的全局个人资料ID

**注意：** 修改`max_users`和`max_routers`会触发计费。

### 成员

您可以查看组织成员信息。
```bash
# List organization members
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/organizations/members" | jq '.body.members'
```

### 子组织

子组织可以将个人资料和终端节点划分为逻辑组：
- **部门**——内部组织单位
- **物理站点**——办公室位置或分支机构
- **客户公司**——适用于管理多个客户的MSP
- **其他逻辑分组**——根据实际需求进行划分

每个子组织都有自己的个人资料和终端节点，还可以选择应用全局个人资料。

**创建子组织参数：**
- `name`（字符串）——组织名称
- `contact_email`（字符串）——主要联系人的电子邮件地址
- `twofa_req`（整数）——是否要求使用双因素认证（0=不需要，1=需要）
- `stats_endpoint`（字符串）——来自`/analytics/endpoints`的存储区域PK
- `max_users`（整数）——最大用户设备数量
- `max_routers`（整数）——最大路由器设备数量

**可选参数：**
- `address`（字符串）——物理地址
- `website`（字符串）——网站URL
- `contact_name`（字符串）——联系人姓名
- `contact_phone`（字符串）——联系电话号码
- `parent_profile`（字符串）——应用于所有设备的全局个人资料ID

### 部署代码

您可以使用RMM工具将ctrld守护进程批量部署到终端节点。
**设备类型：** `windows`, `mac`, `linux`
**部署命令：**
```bash
# Windows (PowerShell as Admin)
(Invoke-WebRequest -Uri 'https://api.controld.com/dl/rmm' -UseBasicParsing).Content | Set-Content "$env:TEMP\ctrld_install.ps1"; Invoke-Expression "& '$env:TEMP\ctrld_install.ps1' 'CODE'"

# macOS/Linux
sh -c 'sh -c "$(curl -sSL https://api.controld.com/dl/rmm)" -s CODE'
```

---

## 计费

您可以查看计费历史记录、订阅信息和活跃产品。
```bash
# Get payment history
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/billing/payments" | jq '.body'

# Get active and canceled subscriptions
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/billing/subscriptions" | jq '.body'

# Get currently activated products
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/billing/products" | jq '.body'
```

---

## 移动设备配置（苹果设备）

您可以生成适用于iOS/macOS设备的签名DNS配置文件（.mobileconfig）。
```bash
# Generate mobile config profile for a device
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/mobileconfig/DEVICE_ID" -o config.mobileconfig

# With optional parameters
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/mobileconfig/DEVICE_ID?client_id=my-iphone&dont_sign=0" -o config.mobileconfig

# Exclude specific WiFi networks
curl -s -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
  "https://api.controld.com/mobileconfig/DEVICE_ID?exclude_wifi[]=HomeNetwork&exclude_wifi[]=OfficeWiFi" -o config.mobileconfig
```

**路径参数：**
- `device_id`（必需）——设备/解析器ID

**查询参数（均为可选）：**
- `exclude_wifi[]`（数组）——需要排除的WiFi SSID
- `exclude_domain[]`（数组）——需要排除的域名
- `dont_sign`（字符串）——设置为`1`以返回未签名的配置文件
- `exclude_common`（字符串）——设置为`1`以排除常见的捕获门户主机名
- `client_id`（字符串）——可选的客户名称

**注意：** 此接口在成功时返回二进制数据（而非JSON格式），错误情况仍返回JSON格式的数据。

---

## 辅助脚本

您可以使用`scripts/controld.sh`执行常见操作：
```bash
# List profiles
./scripts/controld.sh profiles list

# Create profile
./scripts/controld.sh profiles create "My Profile"

# List devices
./scripts/controld.sh devices list

# Create device
./scripts/controld.sh devices create "Router" PROFILE_ID router

# Block domain
./scripts/controld.sh rules block PROFILE_ID "ads.example.com"

# Bypass domain
./scripts/controld.sh rules bypass PROFILE_ID "trusted.com"

# Enable filter
./scripts/controld.sh filters enable PROFILE_ID FILTER_ID

# Block service (e.g., facebook, tiktok)
./scripts/controld.sh services block PROFILE_ID SERVICE_ID

# List proxies
./scripts/controld.sh proxies list

# Organization management (business accounts)
./scripts/controld.sh orgs info               # View organization info
./scripts/controld.sh orgs members            # List members
./scripts/controld.sh orgs suborgs            # List sub-organizations
./scripts/controld.sh provision list

# Billing
./scripts/controld.sh billing payments        # Payment history
./scripts/controld.sh billing subscriptions   # Subscriptions
./scripts/controld.sh billing products        # Active products

# Mobile Config (Apple devices)
./scripts/controld.sh mobileconfig DEVICE_ID config.mobileconfig
```

## 常见工作流程

### 设置新设备
1. 列出个人资料：`profiles list`
2. 创建或选择个人资料
3. 使用个人资料创建设备：`devices create NAME PROFILE_ID ICON`
4. 从响应中获取解析器地址（DoH/DoT/IPv4）
5. 配置设备使用相应的解析器

### 阻止社交媒体访问
1. 列出社交媒体服务：`curl ... /services/categories/social`
2. 阻止特定服务：`services block PROFILE_ID facebook`
3. 或者为特定域名创建自定义规则

### 启用广告拦截
1. 列出过滤器：`filters list PROFILE_ID`
2. 启用广告相关过滤器：`filters enable PROFILE_ID ads`
3. 启用恶意软件过滤器：`filters enable PROFILE_ID malware`

### 通过代理重定向流量（地理欺骗）
1. 列出可用代理：`./scripts/controld.sh proxies list`
2. 设置服务通过代理进行解析：
   ```bash
   curl -s -X PUT -H "Authorization: Bearer $CONTROLD_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"do":2,"status":1,"via":"PROXY_PK"}' \
     "https://api.controld.com/profiles/PROFILE_ID/services/SERVICE_ID"
   ```

### 向企业终端节点批量部署
1. 创建部署代码：`provision create`
2. 使用RMM工具进行部署
3. 在控制面板中监控终端节点的注册情况

## 速率限制

API的请求速率限制为每5分钟约1200次（平均每秒4次请求）。如果收到429个错误响应，系统将采用指数级退避策略。

## 注意事项：
- 组织相关功能需要企业账户
- 子组织成员默认继承父组织的权限，除非另有指定
- 应用于子组织的全局个人资料将应用于该子组织内的所有设备
- 分析数据保留1个月（原始日志）或1年（统计数据）
- 支持单点登录（SSO）：Okta OIDC和Microsoft EntraID OIDC

## API文档来源：
- **概念文档：** https://docs.controld.com/docs/
- **API参考：** https://docs.controld.com/reference/get-started（JavaScript渲染）
- **API基础URL：** https://api.controld.com

**已验证的API端点（截至2026年3月）：**
- 核心功能：`/profiles`, `/devices`, `/access`, `/proxies`, `/services`, `/filters`
- 组织相关：`/organizations/organization`, `/organizations/members`, `/organizations/sub_organizations`, `/organizations/suborg`, `/organizations`（PUT）
- 计费相关：`/billing/payments`, `/billing/subscriptions`, `/billing/products`
- 移动设备配置：`/mobileconfig/{device_id}`
- 部署相关：`/provision`

组织和管理账户功能需要企业账户。
---
name: outlook-to-gmail
description: "将电子邮件、联系人和日历从 Microsoft Outlook（Office 365 / Exchange / PST）迁移到 Google Workspace（Gmail）。适用于用户需要将数据从 Outlook 迁移到 Gmail、将电子邮件从 Microsoft 365 转移到 Google Workspace、导入 PST 文件到 Gmail、从 Exchange 切换到 Gmail，或规划 Office 365 到 Google Workspace 的迁移场景。内容包括：单用户迁移、批量/全组织迁移、PST 文件导入、日历和联系人转移、DNS/MX 设置调整，以及迁移后的数据验证。"
---
# Outlook到Gmail的迁移

## 迁移方案

在开始迁移之前，请先评估源环境：

| 源环境 | 最佳迁移方法 | 迁移范围 |
|--------|------------|-------|
| Office 365 / Exchange Online | Google数据迁移服务（管理员控制台） | 全组织范围，批量迁移 |
| 本地Exchange服务器 | GWMMO工具或IMAP迁移 | 单用户迁移或批量迁移 |
| PST文件 | GWMMO工具或Outlook IMAP桥接 | 单用户迁移 |
| Outlook.com（个人账户） | 通过管理员控制台进行IMAP迁移 | 单用户迁移 |

## 迁移前的准备工作

在开始迁移之前，与客户一起完成以下检查：

1. **用户数量统计**：统计用户数量、邮箱总大小、最大的邮箱、共享邮箱及邮件分发列表。
2. **Google Workspace订阅情况**：确认订阅状态，并验证管理员权限（需要超级管理员权限）。
3. **源环境管理员权限**：确认具备全局管理员（O365）或Exchange管理员权限及相应的应用程序密码。
4. **DNS记录管理权限**：确定谁负责管理MX记录（注册商、Cloudflare等）。
5. **数据范围**：需要迁移的数据包括哪些内容？电子邮件、联系人、日历还是Drive文件？
6. **迁移时间窗口**：选择合适的迁移时间（建议在周末进行）。
7. **用户通知**：起草邮件通知用户迁移事宜及新的登录方式。
8. **数据保留**：迁移后30天内保持源邮箱的活跃状态，作为数据备份。

## 方法1：Google数据迁移服务（推荐用于O365环境）

适用于从Exchange Online/Offerice 365进行的全组织范围迁移。

### 设置步骤

1. 登录Google管理员控制台 → **数据** → **数据导入与导出** → **数据迁移（新建）**
2. 选择**Microsoft Office 365**作为数据源。
3. 点击**连接**，以Microsoft全局管理员身份登录，并授予必要的权限。
4. 选择需要迁移的数据类型：电子邮件、联系人、日历。
5. （可选）设置日期范围过滤器，仅迁移最近N个月的数据以节省时间。

### 执行步骤

1. 上传用户列表（格式为CSV文件，格式示例：`source_email,destination_email`）。
2. 启动迁移过程，Google会自动处理数据差异同步。
3. 在管理员控制台监控迁移进度，可查看每个用户的迁移状态。
4. 迁移过程在后台进行，用户在此期间可以继续使用Outlook。

### CSV文件格式

完整的CSV文件模板及使用说明请参见`references/csv-template.md`。

## 方法2：GWMMO工具（适用于PST文件或Outlook个人账户）

适用于单个用户或PST文件的迁移。

1. 从[此处](https://tools.google.com/dlpage/gsmmo/)下载GWMMO工具。
2. 在安装了Outlook个人资料或PST文件访问权限的计算机上安装该工具。
3. 使用Google Workspace账户登录工具。
4. 选择需要迁移的Outlook个人资料或PST文件。
5. 选择需要迁移的数据类型：电子邮件、联系人、日历、垃圾邮件。
6. 开始数据导入，迁移进度会在工具中显示。

**注意事项**：该工具支持单用户迁移，需要桌面访问权限，仅支持Windows系统。

## 方法3：IMAP桥接（手动方法/小规模迁移）

适用于个人Outlook.com账户或其他方法无法完成迁移的情况：

1. 在Gmail中启用IMAP功能：设置 → 转发与POP/IMAP → 启用IMAP。
2. 在Outlook桌面应用中，将Gmail添加为IMAP账户。
3. 将Outlook邮箱中的文件夹拖放到Gmail的IMAP文件夹中。

### DNS/MX记录调整

数据迁移完成后，请执行以下操作：

1. 在Google管理员控制台验证域名设置（TXT记录）。
2. 更新MX记录指向Gmail的服务器地址：
   ```
   Priority  Host
   1         ASPMX.L.GOOGLE.COM
   5         ALT1.ASPMX.L.GOOGLE.COM
   5         ALT2.ASPMX.L.GOOGLE.COM
   10        ALT3.ASPMX.L.GOOGLE.COM
   10        ALT4.ASPMX.L.GOOGLE.COM
   ```
3. 设置SPF记录：`v=spf1 include:_spf.google.com ~all`
4. 设置DKIM记录：通过管理员控制台 → 应用程序 → Gmail → 生成DKIM签名。
5. 设置DMARC记录：`v=DMARC1; p=none; rua=mailto:admin@domain.com`（初始设置为`p=none`，后续可根据需要调整）。
6. 调整TTL值：迁移前将TTL值设置为300秒，48小时后恢复为3600秒。

DNS记录的模板请参见`references/dns-records.md`。

## 迁移后的验证工作

对每个用户执行以下验证：

- 确认Gmail能否正常接收电子邮件（发送测试邮件）。
- 检查历史邮件是否完整保存（查看最早和最新的邮件）。
- 确认文件夹和标签是否正确映射。
- 验证联系人是否已导入（检查联系人数量）。
- 日历事件是否正常显示（特别是重复事件）。
- 共享邮箱和组是否已转换为Google Groups。
- 确认Gmail中的签名设置是否正确。
- 检查移动设备是否已重新配置（使用Gmail应用程序或IMAP连接）。

详细的验证清单请参见`references/validation-checklist.md`。

## 常见问题及解决方法

| 问题 | 解决方案 |
|-------|-----|
| 迁移进度停滞在0% | 重新授权源环境管理员的权限。 |
| 文件夹丢失 | Google会合并深层嵌套的文件夹，可能导致文件被标记为“标签”状态。 |
| 日历中的重复事件失效 | 需手动重新创建重复事件（这是Google系统的已知限制）。 |
| 联系人信息重复 | 使用Google的联系人合并工具去除重复项。 |
| 大文件无法迁移（超过25MB） | 需将大文件单独导出。 |
| 共享邮箱无法迁移 | 将共享邮箱转换为Google Groups或共享驱动器。 |
| MX记录传播缓慢 | 检查TTL值，使用`dig MX domain.com`命令进行验证。 |

## 迁移项目交付物模板

为项目准备以下文档：

1. **迁移计划**：包括迁移时间表、阶段划分、用户分组及回滚方案。
2. **用户通知邮件**：用于通知用户迁移事宜的模板。
3. **管理员操作指南**：详细的迁移操作步骤。
4. **验证报告**：包含每个用户的验证结果。

相关模板请参见`references/client-templates.md`。
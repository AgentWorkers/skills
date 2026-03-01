---
name: openclaw-ispconfig
slug: openclaw-ispconfig
description: "管理 ISPConfig 服务器：实现自动化的站点配置、域名管理、邮箱设置、DNS 配置、数据库管理、SSL 证书管理、备份等功能。"
---
# openclaw-ispconfig

这是一个OpenClaw插件，用于通过远程JSON API管理ISPConfig。它提供了31种工具，用于处理网站、DNS、邮件、数据库以及一键式配置等功能。

## 安装

### 使用ClawHub

```bash
clawhub install openclaw-ispconfig
```

### 使用npm

```bash
npm install @elvatis_com/openclaw-ispconfig
```

## ISPConfig配置

1. 在ISPConfig中创建一个远程用户。
2. 授予该用户所需的API权限。
3. 复制API端点URL和凭据。
4. 在OpenClaw中配置该插件。

## 配置

`openclaw.plugin.json`文件中的配置键：

- `apiUrl`（必填）：ISPConfig的JSON API地址
- `username`（必填）：远程用户的用户名
- `password`（必填，保密）：远程用户的密码
- `serverId`（默认值：1）：默认服务器ID
- `defaultServerIp`（可选）：用于配置DNS A记录的备用IP地址
- `readOnly`（默认值：false）：是否允许写入操作
- `allowedOperations`（默认值：[]）：允许使用的工具名称列表
- `verifySsl`（默认值：true）：是否进行TLS证书验证

## 工具

### 读取相关数据

- `isp_methods_list`：无参数
- `isp_system_info`：无参数
- `isp_client_list`：可选的过滤字段
- `isp_client_get`：参数：`client_id`
- `isp_sites_list`：`sites_web_domain_get`方法支持的可选过滤条件
- `isp_site_get`：参数：`primary_id`（或`site_id`、`domain_id`）
- `isp_domains_list`：无参数
- `isp_dns_zone_list`：与用户相关的过滤参数
- `isp_dns_record_list`：参数：`zone_id`
- `isp_mail_domain_list`：可选的过滤条件
- `isp_mail_user_list`：可选的过滤条件
- `isp_db_list`：与用户相关的过滤条件
- `isp_ssl_status`：无参数
- `isp_quota_check`：参数：`client_id`
- `isp_backup_list`：无参数（如果API方法不可用，则返回空结果）
- `isp_cron_list`：可选的过滤条件

### 写入相关数据

- `isp_client_add`：参数：ISPConfig的`client_add`请求数据
- `isp_site_add`：参数：ISPConfig的`sites_web_domain_add`请求数据
- `isp_domain_add`：`isp_site_add`的别名
- `isp_dns_zone_add`：参数：ISPConfig的`dns_zone_add`请求数据
- `isp_dns_record_add`：参数：包括`type`（`A`、`AAAA`、`MX`、`TXT`、`CNAME`）以及相应的记录数据
- `isp_dns_record_delete`：参数：包括`type`以及相应的删除数据
- `isp_mail_domain_add`：参数：ISPConfig的`mail_domain_add`请求数据
- `isp_mail_user_add`：参数：ISPConfig的`mail_user_add`请求数据
- `isp_mail_user_delete`：参数：ISPConfig的`mail_user_delete`请求数据
- `isp_db_add`：参数：ISPConfig的`sites_database_add`请求数据
- `isp_db_user_add`：参数：ISPConfig的`sites_database_user_add`请求数据
- `isp_shell_user_add`：参数：ISPConfig的`sites_shell_user_add`请求数据
- `isp_ftp_user_add`：参数：ISPConfig的`sites_ftp_user_add`请求数据
- `isp_cron_add`：参数：ISPConfig的`sites_cron_add`请求数据

### 配置工具

- `isp_provision_site`：
  - 必需参数：`domain`、`clientName`、`clientEmail`
  - 可选参数：`serverIp`、`createMail`（默认值：true）、`createDb`（默认值：true）、`serverId`（从配置中获取）

工作流程：

1. 创建客户端。
2. 创建启用SSL和Let's Encrypt的网站。
3. 创建DNS区域。
4. 添加DNS记录（`A`、`CNAME`、`SPF`、`TXT`）。
5. （可选）创建邮件域名及`info@`、`admin@`邮箱。
6. （可选）创建数据库用户及数据库。
7. 确保网站启用了SSL功能。

## 安全性

- 如果`readOnly`设置为`true`，则禁止所有写入和配置操作。
- `allowedOperations`列表中列出的工具才能被执行。

## 开发

```bash
npm run build
npm test
```

进行实际测试时，请设置以下环境变量：

- `ISPCONFIG_API_URL`：ISPConfig的API地址
- `ISPCONFIG_USER`：远程用户名
- `ISPCONFIG_PASS`：远程密码

## 许可证

MIT许可证
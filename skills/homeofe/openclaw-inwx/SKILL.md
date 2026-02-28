---
name: openclaw-inwx
description: "INWX域名注册商管理：域名注册、可用性查询、DNS记录、名称服务器、DNSSEC、价格信息、域名转移。"
---
# openclaw-inwx

这是一个用于INWX（InterNetworX）域名注册商自动化的OpenClaw插件。它提供了23种工具，用于执行域名生命周期操作、DNS管理、DNSSEC配置、联系人信息处理、WHOIS查询以及账户检查等功能。

## 主要特性

- 通过`domrobot-client`与INWX的DomRobot JSON-RPC接口集成
- 支持`production`或`ote`两种运行环境切换
- 提供可选的2FA（双因素认证）登录功能（使用`otpSecret`参数）
- 安全控制机制：
  - `readOnly`模式会阻止所有写入操作
  - `allowedOperations`参数可用于指定允许使用的具体工具
- 支持TypeScript的严格编码模式

## 安装说明

```bash
npm install @elvatis_com/openclaw-inwx
```

## INWX账户设置

1. 创建或使用您的INWX账户。
2. 在INWX账户设置中启用API访问权限。
3. 如果启用了2FA，请提供相应的共享密钥（`otpSecret`）。
4. 为安全测试，请使用OTE环境（`ote.inwx.com`）。

## 插件配置

```json
{
  "username": "your-inwx-user",
  "password": "your-inwx-password",
  "otpSecret": "optional-2fa-secret",
  "environment": "ote",
  "readOnly": false,
  "allowedOperations": []
}
```

## 工具列表

### 读取操作工具

1. `inwx_domain_check`  
   - INWX方法：`domain.check`  
   - 参数：`domain`（字符串）

2. `inwx_domain_list`  
   - INWX方法：`domain.list`  
   - 参数：可选的过滤条件（对象）

3. `inwx_domain_info`  
   - INWX方法：`domain.info`  
   - 参数：`domain`（字符串）

4. `inwx_domain_pricing`  
   - INWX方法：`domain.check`  
   - 参数：`domain`（字符串）或`domains`（字符串数组）

5. `inwx_nameserver_list`  
   - INWX方法：`nameserver.list`或`domain.info`  
   - 参数：可选的`domain`参数

6. `inwx_dns_record_list`  
   - INWX方法：`nameserver.info`  
   - 参数：`domain`（字符串）

7. `inwx_dnssec_list`  
   - INWX方法：`dnssec.info`  
   - 参数：可选的过滤条件

8. `inwx_contact_list`  
   - INWX方法：`contact.list`  
   - 参数：可选的过滤条件

9. `inwx_whois`  
   - INWX方法：`domain.whois`  
   - 参数：`domain`（字符串）

10. `inwx_account_info`  
    - INWX方法：`account.info`  
    - 参数：无

### 写入操作工具

11. `inwx_domain_register`  
    - INWX方法：`domain.create`  
    - 参数：`domain`、`period`、`contacts`、`ns`

12. `inwx_domain_update`  
    - INWX方法：`domain.update`  
    - 参数：操作所需的数据

13. `inwx_domain_delete`  
    - INWX方法：`domain.delete`  
    - 参数：操作所需的数据

14. `inwx_domain_transfer`  
    - INWX方法：`domain.transfer`  
    - 参数：操作所需的数据

15. `inwx_domain_renew`  
    - INWX方法：`domain.renew`  
    - 参数：操作所需的数据

16. `inwx_nameserver_set`  
    - INWX方法：`domain.update`  
    - 参数：`domain`、`ns`（字符串数组）

17. `inwx_dns_record_add`  
    - INWX方法：`nameserver.createRecord`  
    - 参数：操作所需的数据

18. `inwx_dns_record_update`  
    - INWX方法：`nameserver.updateRecord`  
    - 参数：操作所需的数据

19. `inwx_dns_record_delete`  
    - INWX方法：`nameserver.deleteRecord`  
    - 参数：操作所需的数据

20. `inwx_dnssec_enable`  
    - INWX方法：`dnssec.create`  
    - 参数：操作所需的数据

21. `inwx_dnssec_disable`  
    - INWX方法：`dnssec.delete`  
    - 参数：操作所需的数据

22. `inwx_contact_create`  
    - INWX方法：`contact.create`  
    - 参数：操作所需的数据

23. `inwx_contact_update`  
    - INWX方法：`contact.update`  
    - 参数：操作所需的数据

## OTE测试环境

设置OTE环境（`ote.inwx.com`）后，客户端将指向INWX的OTE API端点，从而可以免费进行集成测试，无需承担生产环境的成本。

## 与openclaw-ispconfig的集成

该插件提供了`provisionDomainWithHosting()`方法，用于实现端到端的域名到托管服务的配置流程。这两个插件可以独立运行，无需相互依赖：

1. **域名检查** - `inwx_domain_check`
2. **域名注册** - `inwx_domain_register`（如果已注册或`skipRegistration`设置为`true`则跳过）
3. **名称服务器配置** - `inwx_nameserver_set`
4. **托管服务配置** - `isp_provision_site`（包括站点信息、DNS区域设置、邮件服务、数据库配置）

```typescript
import { buildToolset, provisionDomainWithHosting } from "@elvatis_com/openclaw-inwx";
import ispPlugin from "@elvatis_com/openclaw-ispconfig";

const result = await provisionDomainWithHosting(
  buildToolset(inwxConfig),
  ispPlugin.buildToolset(ispConfig),
  { domain: "example.com", nameservers: ["ns1.host.de"], serverIp: "1.2.3.4", clientName: "Acme", clientEmail: "a@acme.com" },
);
```

## 安全性注意事项

- 当`readOnly`设置为`true`时，仅允许执行以下操作：
  - 域名检查、列表查询、信息查询、价格查询
  - 名称服务器列表查询
  - DNS记录列表查询
  - DNSSEC配置查询
  - 联系人信息查询
  - 账户信息查询

- `allowedOperations`参数可用于限制可使用的具体工具名称。

## 其他说明

- 该仓库不包含任何实际的生产环境测试代码。
- 单元测试仅使用模拟数据（mocks）进行验证。
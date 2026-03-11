---
name: ali-esa-acme-ssl-skill
description: >
  **自动使用 Alibaba Cloud ESA DNS 和 acme.sh 发行/续订 HTTPS 证书**  
  （支持通配符 *.example.com 和 example.com；可选择将证书安装到 Nginx 中。）  
  当用户提及以下关键词时，触发此功能：ESA、ATrustDNS、_acme-challenge、acme.sh、Let's Encrypt、No TXT record found、InvalidRecordNameSuffix、wildcard certificate 或 Nginx certificate configuration。
homepage: https://github.com/dogeow/ali-esa-acme-ssl-skill
metadata: {"openclaw":{"homepage":"https://github.com/dogeow/ali-esa-acme-ssl-skill","os":["linux"],"requires":{"bins":["python3","dig","acme.sh"],"env":["ALIYUN_AK","ALIYUN_SK","ALIBABACLOUD_ACCESS_KEY_ID","ALIBABACLOUD_ACCESS_KEY_SECRET"]},"primaryEnv":"ALIYUN_AK"}}
---
# ESA DNS + ACME证书自动化

## 设计决策（重要）
该技能将 `acme.sh` 和 ESA DNS 功能整合为一个统一的流程，而不是分开为两个独立的技能。

**原因：**
1. 这两个步骤是紧密关联的：ACME 挑战令牌必须立即写入 ESA DNS。
2. 用户最常见的错误是“验证失败”或“记录写入错误的DNS服务器”；集成流程可以减少这类错误的发生。
3. 在使用通配符的情况下，同一个FQDN可能会产生多个TXT记录；如果分开处理，会增加手动同步的工作量。

> 如果未来对“仅DNS操作”的需求较大，可以单独开发一个名为 `esa-dns-records` 的辅助技能。

---

## 触发条件
在以下任何一种情况下触发该技能：
- 域名的NS记录托管在 `*.atrustdns.com`（ESA托管的DNS服务器）上；
- 用户请求使用 `acme.sh`、Let's Encrypt或DNS-01流程来生成证书；
- 出现错误提示“在_acme-challenge...未找到TXT记录”；
- 需要同时为 `example.com` 及其子域名生成证书；
- 需要自动写入ESA DNS记录并配置到Nginx服务器中。

---

## 支持的环境
- Linux服务器（推荐使用Ubuntu版本）；
- 系统级别的Nginx服务器（LNMP架构已通过测试）；
- 不支持Docker/容器化环境；
- 未在Windows/macOS系统上进行测试。

## 先决条件
在使用该技能之前，请先从官方项目安装 `acme.sh`，并确保正确配置安装路径（不建议直接将远程脚本通过管道传递给shell）：
- [官方安装链接：https://github.com/acmesh-official/acme.sh](https://github.com/acmesh-official/acme.sh)

该技能要求 `acme.sh` 被添加到系统的 `PATH` 环境变量中。如果 `acme.sh` 位于 `~/.acme.sh` 目录下，脚本也会自动使用该路径。

**所需配置：**
- 使用 `ALIYUN_AK` / `ALIYUN_SK` 或 `ALIBABACLOUD_ACCESS_KEY_ID` / `ALIBABACLOUD_ACCESS_KEY_SECRET` 进行身份验证；
- 支持通过 `ALIYUN_SECURITY_TOKEN`、`ALIBABACLOUD SECURITY_TOKEN` 或 `--sts-token` 参数传递STS令牌；
- 如果用户直接在OpenClaw的聊天界面或TUI中输入 `id`、`secret`、`token` 等凭据（未使用环境变量名），系统会将其视为Alibaba Cloud的 `AccessKeyId`、`AccessKeySecret` 或 `SecurityToken`，并通过 `--ak`、`--sk`、`--sts-token` 参数传递这些值。无需用户明确指定使用的是“Aliyun”还是“Alibaba Cloud”，脚本会自动识别相应的ESA区域/站点。

---

## 脚本执行方式
脚本路径：`scripts/esa_acme_issue.py`

**默认行为（已优化）：**
- 默认情况下，证书不会自动安装到Nginx服务器中；需要通过 `--install-cert` 参数启用此功能；
- `--dns-timeout` 的默认值为600秒；
- 提供了可选的IPv4/IPv6记录管理选项：`--ensure-a-record host=ip`（包含权威NS服务器的记录传播检查）；
- 现有的A记录不会被覆盖，除非使用了 `--confirm-overwrite` 参数；
- `--lang` 参数用于指定输出语言（默认为英文；支持的语言会自动从 `scripts/i18n/` 目录中检测）；
- 如果使用了 `--install-cert` 参数，脚本将在具有写入目标证书路径权限的Linux服务器上运行，并在操作完成后重新加载Nginx。

### 单个域名处理
```bash
export ALIYUN_AK='YOUR_AK'
export ALIYUN_SK='YOUR_SK'
export ALIYUN_SECURITY_TOKEN='YOUR_STS_TOKEN'   # optional but recommended
python3 scripts/esa_acme_issue.py \
  -d test.example.com
```

**Alibaba Cloud环境中的等效参数：**
```bash
export ALIBABACLOUD_ACCESS_KEY_ID='YOUR_AK'
export ALIBABACLOUD_ACCESS_KEY_SECRET='YOUR_SK'
export ALIBABACLOUD_SECURITY_TOKEN='YOUR_STS_TOKEN'   # optional
```

### 处理通配符域名（推荐的执行顺序）  
```bash
export ALIYUN_AK='YOUR_AK'
export ALIYUN_SK='YOUR_SK'
python3 scripts/esa_acme_issue.py \
  -d example.com \
  -d '*.example.com'
```

### 仅处理通配符域名  
```bash
python3 scripts/esa_acme_issue.py \
  -d '*.example.com'
```

---

## 正确的Nginx配置要求
```nginx
ssl_certificate     /etc/nginx/ssl/example.com.crt;
ssl_certificate_key /etc/nginx/ssl/example.com.key;
```

---

## 完成标准（防止误报）
在报告“记录创建完成/DNS配置就绪”之前，必须满足以下两个条件：
1. `ListRecords` 命令返回目标记录的名称、类型和值；
2. 通过 `dig @ns TXT` 命令在权威NS服务器上能够查到预期的ACME令牌。

如果仅通过 `CreateRecord` API获取到成功响应（仅返回请求ID或记录ID），而未满足上述两个条件，应报告“请求已接受”，而不是“操作已完成”。

## 故障排查快速参考：
1. **`InvalidRecordNameSuffix`**：域名后缀不属于当前ESA站点（常见输入错误）。
2. **“在_acme-challenge...未找到TXT记录”**：可能是TXT记录尚未传播到所有权威NS服务器；请将 `--dns-timeout` 值设置为300–600秒。
3. 在设置AccessKey IP白名单后出现权限或签名错误：  
   - 检查当前系统的公共出站IP地址：`curl -s ifconfig.me`  
   - 将实际的出站NAT IP地址添加到白名单中（而非局域网IP地址）；  
   - 如果系统通过代理或网关访问，请将代理的出站IP地址加入白名单；  
   - 在更新白名单后稍作等待再重试。

---

## 安全指南
在每次执行脚本之前，请提醒用户注意以下安全事项：
1. 使用具有最小权限的RAM子账户；切勿长期使用主账户的访问权限。
2. 尽量使用STS临时凭证以降低信息泄露风险。
3. 启用AccessKey IP白名单，仅允许实际的出站NAT IP地址通过脚本。
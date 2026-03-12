---
name: alicloud-network-dns-cli
description: Alibaba Cloud DNS (Alidns) 命令行工具（CLI）技能：通过 `alyun-cli` 查询、添加和更新 DNS 记录，包括为函数计算（Function Compute）自定义域名设置 CNAME 记录。
version: 1.0.0
---
**类别：工具**  
# Alibaba Cloud DNS (Alidns) 命令行工具 (Alidns CLI)  

## 目标  
- 通过 `aliyun-cli` 查询和管理 Alibaba Cloud 的 DNS 记录。  
- 快速为 Function Compute 的自定义域名配置 CNAME 记录。  

## 使用场景  
- 当您需要添加或更新 Alibaba Cloud DNS 记录时。  
- 当您需要为 Function Compute 的自定义域名设置 CNAME 记录时。  

## 安装 aliyun-cli（无需使用 sudo）  
```bash
curl -fsSL https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz -o /tmp/aliyun-cli.tgz
mkdir -p ~/.local/bin
 tar -xzf /tmp/aliyun-cli.tgz -C /tmp
mv /tmp/aliyun ~/.local/bin/aliyun
chmod +x ~/.local/bin/aliyun
```  

## 配置凭据  
```bash
~/.local/bin/aliyun configure set \
  --profile default \
  --access-key-id <AK> \
  --access-key-secret <SK> \
  --region cn-hangzhou
```  
将区域设置为默认值；如果不确定最佳区域，请询问用户。  

## 查询 DNS 记录  
查询子域名记录：  
```bash
~/.local/bin/aliyun alidns DescribeSubDomainRecords \
  --SubDomain news.example.com
```  

## 添加 CNAME 记录  
```bash
~/.local/bin/aliyun alidns AddDomainRecord \
  --DomainName example.com \
  --RR news \
  --Type CNAME \
  --Value <TARGET>
```  

## Function Compute 自定义域名的 CNAME 设置  
自定义域名应指向 Function Compute 的公共 CNAME 记录：  
```
<account_id>.<region_id>.fc.aliyuncs.com
```  
（示例：杭州）  
```
1629965279769872.cn-hangzhou.fc.aliyuncs.com
```  

## 常见问题  
- 如果不支持顶级域名（ apex domain）的 CNAME 设置，请使用子域名（如 `www`）或 ALIAS/ANAME 记录。  
- 请在 DNS 记录传播完成后创建 Function Compute 的自定义域名，否则可能会出现 “DomainNameNotResolved” 的错误。  

## 参考资料  
- aliyun-cli 安装指南：  
  - https://help.aliyun.com/zh/cli/install-cli-on-linux  
- Alidns API（AddDomainRecord / DescribeSubDomainRecords）：  
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-adddomainrecord  
  - https://help.aliyun.com/zh/dns/api-alidns-2015-01-09-describesubdomainrecords  
- Function Compute 自定义域名配置及 CNAME 设置指南：  
  - https://www.alibabacloud.com/help/en/functioncompute/fc/user-guide/configure-custom-domain-names  
- 官方参考资料列表：`references/sources.md`  

## 验证  
```bash
mkdir -p output/alicloud-network-dns-cli
echo "validation_placeholder" > output/alicloud-network-dns-cli/validate.txt
```  
验证标准：命令执行成功（返回代码为 0），并且生成 `output/alicloud-network-dns-cli/validate.txt` 文件。  

## 输出与证据  
- 将命令输出结果及 API 响应内容保存到 `output/alicloud-network-dns-cli/` 目录下。  
- 确保证据文件中包含关键参数（区域、资源 ID、时间范围），以便重现操作过程。  

## 先决条件  
- 在执行操作前，请配置最低权限的 Alibaba Cloud 凭据。  
- 建议使用环境变量：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`（可选）以及 `ALICLOUD_REGION_ID`。  
- 如果区域信息不明确，请在运行修改操作前询问用户。  

## 工作流程  
1) 确认用户的操作意图、所选区域、相关标识符，以及操作是只读还是修改操作。  
2) 首先执行一个最小的只读查询，以验证网络连接和权限是否正常。  
3) 使用明确的参数和受限的范围执行目标操作。  
4) 验证操作结果，并保存输出文件及所有相关证据。
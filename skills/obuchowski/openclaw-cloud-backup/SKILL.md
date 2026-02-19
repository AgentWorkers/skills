---
name: cloud-backup
description: 将 OpenClaw 的配置备份并恢复到兼容 S3 的云存储服务中（如 AWS S3、Cloudflare R2、Backblaze B2、MinIO、DigitalOcean Spaces）。这些服务可用于本地备份、上传到云端、恢复数据以及清理过期的备份文件。
metadata: {"openclaw":{"emoji":"☁️","requires":{"bins":["bash","tar","jq"]}}}
---
# OpenClaw云备份

**功能概述：**  
在本地备份OpenClaw的配置信息，并可选择将其同步到支持S3协议的云存储服务中。

## 所需环境  

**本地环境：**  
- `bash`、`tar`、`jq`命令工具  

**云存储服务（支持AWS S3、Cloudflare R2、Backblaze B2、MinIO、DigitalOcean Spaces）：**  
- `aws` CLI v2（用于上传、下载、查看或恢复云备份数据）  

**可选工具：**  
- `gpg`（用于客户端数据加密）  

## 参考文档：**  
- `references/provider-setup.md`：详细介绍各云存储服务的端点、区域设置、密钥配置及最小权限原则  
- `references/security-troubleshooting.md`：提供安全防护措施及常见故障解决方法  
- `references/local-config.md`：包含本地配置选项（如备份路径、保留策略等）  

## 配置步骤  

配置信息存储在OpenClaw的`skills.entries.cloud-backup.*`文件中：  
```
bucket              - S3 bucket name (required)
region              - AWS region (default: us-east-1)
endpoint            - Custom endpoint for non-AWS providers
awsAccessKeyId      - Access key ID
awsSecretAccessKey  - Secret access key
awsProfile          - Named AWS profile (alternative to keys)
gpgPassphrase       - For client-side encryption (optional)
```  

### 建议的自动化配置方法（通过代理执行）：**  
通过代理向OpenClaw发送以下指令：  
> “配置云备份服务，使用存储桶`my-backup-bucket`、区域`us-east-1`、访问密钥`AKIA...`和密钥`...`”  
代理会自动运行`gateway config.patch`命令来安全地存储这些配置信息。  

### 手动配置方法：**  
（具体配置步骤请参考相关文档或示例代码。）  

### 本地配置选项（可选）：**  
非敏感配置项（如备份路径、保留策略等）请参考`references/local-config.md`，并将配置内容复制到`~/.openclaw-cloud-backup.conf`文件中。  

### 配置验证：**  
运行`setup`命令查看配置信息，并使用`status`命令确认所有组件均已正确连接。  

## 常用命令：**  
| 命令          | 功能                |  
|----------------|-------------------|  
| `setup`        | 显示配置指南并测试连接          |  
| `status`       | 打印当前配置及依赖项状态        |  
| `backup [full|skills|settings]` | 创建并上传备份文件         |  
| `list`        | 列出所有云备份文件         |  
| `restore <name> [--dry-run] [--yes]` | 下载并恢复指定备份文件       |  
| `cleanup`      | 根据策略清理旧备份文件         |  

## 工作流程：**  
1. 通过代理或手动运行`setup`命令配置备份参数。  
2. 使用`status`命令确认所有组件连接正常。  
3. 首次备份时运行`backup full`命令。  
4. 使用`list`命令验证备份结果。  
5. 首次配置完成后，系统会自动安排每日备份（具体规则请参见“调度”部分）。  
6. 先使用`restore <name> --dry-run`进行测试性恢复，确认无误后再使用`--yes`选项进行实际恢复。  

## 备份调度：**  
**默认设置：** 每日自动备份。**  
如果未设置定时任务，系统会自动安排每日备份并通知用户（示例消息：**“备份已完成。已设置每日02:00自动备份，请告知是否需要调整时间表。”**）  
用户可通过OpenClaw的内置cron工具自定义备份计划：  
> “将每日备份时间设置为02:00”  
> “将每周日03:00设置为备份清理时间”  
代理会自动创建相应的cron作业来执行备份任务。  

**示例作业配置：**  
- **每日完整备份（02:00）：**  
```json
{
  "schedule": { "kind": "cron", "expr": "0 2 * * *" },
  "payload": { "kind": "agentTurn", "message": "Run cloud-backup: backup full" },
  "sessionTarget": "isolated"
}
```  
- **每周日03:00进行备份清理：**  
```json
{
  "schedule": { "kind": "cron", "expr": "0 3 * * 0" },
  "payload": { "kind": "agentTurn", "message": "Run cloud-backup: cleanup" },
  "sessionTarget": "isolated"
}
```  
（如仅进行本地备份，可在配置中设置`UPLOAD=false`。）  

## 配置优先级：**  
配置项按以下顺序加载（优先级从高到低）：  
1. **环境变量**（用于持续集成/自动化流程）  
2. **OpenClaw配置文件（`skills.entries.cloud-backup.*`）**（推荐使用）  
3. **本地配置文件（`~/.openclaw-cloud-backup.conf`）**（旧版本或备用配置）  

## 安全注意事项：**  
- 保持存储桶设置为私有访问模式，并使用最小权限的访问凭证。  
- OpenClaw配置文件中的敏感信息受文件权限保护。  
- 每次恢复操作前务必使用`--dry-run`选项进行测试。  
- 备份文件路径经过严格验证，以防止路径遍历攻击。  
- 若凭证泄露，立即更换密钥。
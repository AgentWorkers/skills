---
name: cloud-backup
description: >
  **备份与恢复 OpenClaw 状态**  
  该功能用于创建本地备份文件，并将其上传到支持 S3 协议的云存储服务（如 AWS S3、Cloudflare R2、Backblaze B2、MinIO、DigitalOcean Spaces 等）。当用户请求“备份”、“恢复数据”或进行任何与 OpenClaw 备份相关的操作时，该功能将被触发。
metadata: {"openclaw":{"emoji":"☁️","requires":{"bins":["bash","tar","jq","aws"]}}}
---
# OpenClaw云备份

该功能可将OpenClaw的状态数据备份到本地存档，并上传到云存储服务中。请按照以下步骤操作。在执行备份操作后，需向用户说明系统所应用的默认设置。

## 备份流程（请依次完成每个步骤）

### 第1步：运行备份任务

```bash
bash "{baseDir}/scripts/cloud-backup.sh" backup full
```

默认的备份范围为`full`（即备份所有数据）。只有在用户明确要求仅备份特定数据（如`workspace`、`skills`或`settings`）时，才使用相应的选项。

### 第2步：检查备份输出中的加密提示

查看第1步中脚本的输出。如果输出包含以下提示：

`WARN: 加密功能已关闭——备份文件将以明文形式存储。`

则需要向用户询问：

> “您的备份文件未经过加密。这些文件中包含配置信息、凭据以及API密钥（均以明文形式保存）。是否需要设置密码短语？（使用AES-256加密算法，只需提供密码短语即可恢复数据，无需额外的密钥文件。）”

- 如果用户提供了密码短语：
  - 通过`gateway config.patch`更新配置文件，设置以下内容：
    - `skills.entries.cloud-backup.config.encrypt = true`
    - `skills.entries.cloud-backup.env.GPG_PASSPHRASE = "<passphrase>`
  - 重新运行备份任务，以确保备份文件被加密。
  - 如果用户拒绝设置密码短语或选择不进行加密，则直接跳转到第3步。
- 如果没有出现此警告（说明加密功能已启用），则直接跳转到第3步。

**注意：**务必执行此步骤，并向用户报告备份结果。由于备份文件可能包含敏感信息，因此每次备份时都需要提示用户是否需要加密。

### 第3步：检查脚本输出中的其他警告信息

查看脚本的输出。如果输出包含`WARN: 云存储配置未完成`，请进入**第4步**；否则进入**第5步**。

### 第4步：云存储配置未完成——提示用户进行配置

告知用户备份文件已保存在本地，并询问：

> “云存储服务尚未配置——当前备份仅保存在本地。是否需要配置云存储？支持的服务包括AWS S3、Cloudflare R2、Backblaze B2、MinIO、DigitalOcean Spaces或任何其他兼容S3的服务。”

- 如果用户同意配置云存储，请进入**云存储配置**部分（见下文），然后重新运行备份任务。
- 如果用户选择仅使用本地备份，则通过`gateway config.patch`将`config.upload`设置为`false`，并确认用户已接受该设置。

**注意：**务必执行此步骤，并向用户报告配置结果。

### 第5步：报告备份结果并确认备份计划

向用户展示脚本输出中显示的备份文件路径。接着检查系统中是否已设置每日自动备份任务（使用`cron action=list`命令）。如果**没有自动备份任务**，则需要创建一个每日自动备份任务（默认时间为凌晨2点）。根据用户的实际需求调整备份时间。

**注意：**除非用户明确要求不设置自动备份任务，否则此步骤应为必选项。务必向用户报告备份任务的创建情况（是否成功创建）。

---

## 云存储配置

当用户同意配置云存储时，请按照以下步骤操作：

1. **询问用户选择的云存储服务提供商**：AWS S3、Cloudflare R2、Backblaze B2、MinIO、DigitalOcean Spaces或其他兼容S3的服务。
2. 阅读相应的服务提供商文档（位于`references/providers/`目录下），其中包含详细的配置参数、端点地址及凭据设置指南。
3. 通过`gateway config.patch`更新配置文件，包括存储桶名称、凭据信息以及端点地址（非AWS服务所需）。
4. 运行`status`命令验证云存储服务的连接状态，完成后重新运行备份任务。

## 常用命令

| 命令 | 功能 |
|---------|-------------|
| `backup [full\|workspace\|skills\|settings]` | 创建备份文件并上传（默认为`full`模式） |
| `list` | 显示本地和云端的备份文件列表 |
| `restore <name> [--dry-run] [--yes]` | 从本地或云端恢复数据（执行前请务必先使用`--dry-run`选项进行测试） |
| `cleanup` | 删除旧备份文件（本地备份保留7份；云端备份根据文件创建时间和年龄策略进行清理） |
| `status` | 显示当前配置信息并检查依赖关系 |

## 配置参数说明

所有配置参数均存储在OpenClaw的`skills.entries.cloud-backup`文件中。**请勿手动修改默认值——脚本会自动处理这些配置。**

### 配置参数示例

| 参数 | 默认值 | 说明 |
|---------|-------------|-------------|
| `bucket` | — | 云存储桶名称（必须填写） |
| `region` | `us-east-1` | 存储区域（示例值） |
| `endpoint` | *(无)* | 非AWS服务的端点地址 |
| `profile` | *(无)* | 可选：用于指定AWS CLI配置文件 |
| `upload` | `true` | 备份完成后是否上传到云端 |
| `encrypt` | `false` | 是否对备份文件进行GPG加密 |
| `retentionCount` | `10` | 云端备份保留的文件数量 |
| `retentionDays` | `30` | 云端备份文件的保留天数 |

### 其他配置参数

| 参数 | 说明 |
|---------|-------------|
| `ACCESS_KEY_ID` | 用于访问S3存储的访问密钥 |
| `SECRET_ACCESS_KEY` | 用于访问S3存储的秘密密钥 |
| `SESSION_TOKEN` | 可选的临时访问令牌 |
| `GPG_PASSPHRASE` | 用于加密/解密备份文件的密码短语 |

## 服务提供商文档

仅在配置云存储时阅读相应的提供商文档：

- `references/providers/aws-s3.md` | AWS S3配置指南 |
- `references/providers/cloudflare-r2.md` | Cloudflare R2配置指南 |
- `references/providers/backblaze-b2.md` | Backblaze B2配置指南 |
- `references/providers/minio.md` | MinIO配置指南 |
- `references/providers/digitalocean-spaces.md` | DigitalOcean Spaces配置指南 |
- `references/providers/other.md` | 其他兼容S3服务的配置指南 |

## 安全性注意事项

有关凭据管理和故障排除的详细信息，请参阅`references/security.md`文件。
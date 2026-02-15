---
name: membase
description: 使用 Membase（一个去中心化、加密的存储备份与恢复系统）来管理代理内存。该系统支持对代理内存执行备份、恢复、列表显示、差异对比、状态查询以及清理等操作。
license: MIT
metadata:
  author: Unibase
  version: "1.0.0"
  category: memory-management
  tags: [backup, encryption, membase, storage, decentralized, memory]
allowed-tools:
  - bash
---

# Membase内存管理

Membase为AI代理提供安全、去中心化的内存存储服务，并支持端到端的加密。

## 何时使用此技能

当用户执行以下操作时，请激活此技能：
- 请求备份他们的记忆、对话记录或工作区数据
- 希望恢复之前的记忆或对话记录
- 查看可用的备份文件
- 比较不同的备份版本
- 检查备份状态
- 提到“membase”或“备份记忆”

## 概述

所有与Membase相关的操作都通过一个统一的命令来完成：

```bash
node membase.ts <command> [options]
```

可用命令：
- `backup`：将代理的内存文件（MEMORY.md、memory/**/*.md）备份到Membase
- `restore`：从备份中恢复记忆或对话记录
- `list`：列出所有可用的备份文件
- `diff`：比较两个备份文件
- `status`：显示备份状态和统计信息
- `cleanup`：清理旧的备份文件

## 配置

### 环境变量

```bash
export MEMBASE_ACCOUNT=your-account-address
export MEMBASE_SECRET_KEY=your-secret-key
export MEMBASE_BACKUP_PASSWORD=your-backup-password
export MEMBASE_ENDPOINT=https://testnet.hub.membase.io
```

检查是否已配置：
```bash
echo $MEMBASE_ACCOUNT
echo $MEMBASE_SECRET_KEY
echo $MEMBASE_BACKUP_PASSWORD
```

## 命令

### 1. `backup` - 备份记忆

将代理的内存文件备份到Membase，使用AES-256-GCM加密算法。

**使用方法：**
```bash
node membase.ts backup [options]
```

**选项：**
- `--password <pwd>` 或 `-p <pwd>`：加密密码（如果环境变量中未设置，则需要提供）
- `--incremental` 或 `-i`：仅备份自上次备份以来更改的文件
- `--workspace <path>`：自定义工作区目录
- `--no-validate`：跳过密码强度验证
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“请备份我的记忆。”

你的操作步骤：
1. 检查MEMBASE_BACKUP_PASSWORD环境变量是否已设置：
   ```bash
   echo $MEMBASE_BACKUP_PASSWORD
   ```

2. 如果未设置，询问用户：“请提供一个至少包含12个字符的密码（包括大写字母、小写字母和数字）：”

3. 运行备份命令：
   ```bash
   cd skills/membase
   node membase.ts backup --password "<password>"
   ```

4. 向用户显示备份结果：
   ```
   [OK] Backup completed
   Backup ID: backup-2026-02-02T10-30-45-123Z
   Files: 15
   Size: 234 KB

   [WARNING]  Save your backup ID and password securely!
   ```

**增量备份（更快）：**
```bash
node membase.ts backup --password "<password>" --incremental
```

### 2. `restore` - 恢复记忆

从Membase备份中恢复记忆或对话记录。

**使用方法：**
```bash
node membase.ts restore <backup-id> [options]
```

**选项：**
- `<backup-id>`：要恢复的备份ID（必需）
- `--password <pwd>` 或 `-p <pwd>`：解密密码（如果环境变量中未设置，则需要提供）
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“请从backup-2026-02-02T10-30-45-123Z备份中恢复我的记忆。”

你的操作步骤：
1. 检查密码是否已设置：
   ```bash
   echo $MEMBASE_BACKUP_PASSWORD
   ```

2. 运行恢复命令：
   ```bash
   cd skills/membase
   node membase.ts restore backup-2026-02-02T10-30-45-123Z --password "<password>"
   ```

3. 向用户显示恢复结果：
   ```
   [OK] Restore completed
   Files restored: 15
   Total size: 234 KB
   Location: ~/.openclaw/workspace/
   ```

### 3. `list` - 列出备份文件

列出该代理的所有可用备份文件。

**使用方法：**
```bash
node membase.ts list [options]
```

**选项：**
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“显示我的备份文件”或“列出我的备份文件。”

你的操作步骤：
```bash
cd skills/membase
node membase.ts list
```

输出结果将显示：
```
Available backups:

ID                            Timestamp              Files  Size
──────────────────────────────────────────────────────────────────
backup-2026-02-02T10-30-45-123Z 2026-02-02 10:30:45    15     234 KB
backup-2026-02-01T15-20-10-456Z 2026-02-01 15:20:10    12     198 KB
```

### 4. `diff` - 比较备份文件

比较两个备份文件，找出差异。

**使用方法：**
```bash
node membase.ts diff <backup-id-1> <backup-id-2> [options]
```

**选项：**
- `<backup-id-1>`：第一个备份ID（必需）
- `<backup-id-2>`：第二个备份ID（必需）
- `--password <pwd>` 或 `-p <pwd>`：解密密码（如果环境变量中未设置，则需要提供）
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“我的两次备份之间有什么变化？”

你的操作步骤：
1. 获取最新的两个备份ID：
   ```bash
   cd skills/membase
   node membase.ts list
   ```

2. 使用这两个ID运行`diff`命令：
   ```bash
   node membase.ts diff backup-2026-02-02T10-30-45-123Z backup-2026-02-01T15-20-10-456Z --password "<password>"
   ```

3. 显示比较结果：
   ```
   Added files (2):
     + memory/conversation-new.md
     + memory/notes.md

   Modified files (1):
     ~ MEMORY.md
   ```

### 5. `status` - 显示备份状态

显示备份的状态和统计信息。

**使用方法：**
```bash
node membase.ts status [options]
```

**选项：**
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“我的备份状态如何？”或“检查备份状态。”

你的操作步骤：
```bash
cd skills/membase
node membase.ts status
```

输出结果将显示：
```
[STATS] Backup Status

Local:
  Files: 15
  Size: 234 KB

Remote:
  Backups: 10

Configuration:
  Endpoint: https://testnet.hub.membase.io
  Agent: my-agent
  Workspace: ~/.openclaw/workspace
```

### 6. `cleanup` - 清理旧备份文件

列出可以删除的旧备份文件（Membase目前不支持直接删除备份文件的API）。

**使用方法：**
```bash
node membase.ts cleanup [options]
```

**选项：**
- `--keep-last <n>`：保留最新的N个备份文件（默认值：10）
- `--dry-run`：仅显示要删除的备份文件，不实际执行删除操作
- `--no-json`：不输出JSON格式的数据（供代理解析）

**示例对话：**

用户：“清理旧备份文件，保留最近的5个。”

你的操作步骤：
```bash
cd skills/membase
node membase.ts cleanup --keep-last 5
```

**注意：**系统会显示哪些备份文件需要删除，但用户需要通过Membase Hub用户界面手动执行删除操作。

## 安全注意事项

- 所有数据在客户端使用AES-256-GCM算法进行加密
- 密码通过PBKDF2算法生成，迭代次数为100,000次
- 密码永远不会离开用户的本地设备
- Membase的存储是去中心化的，并且遵循零知识原则
- 只有用户自己能够解密自己的备份文件

## 密码要求

- 密码长度至少为12个字符
- 必须包含大写字母和小写字母
- 必须包含数字
- 建议使用密码管理工具来管理密码

## 错误处理

- **凭据缺失**：
  如果出现“Membase凭据未配置”的提示，请检查是否已正确设置MEMBASE_BACKUP_PASSWORD环境变量。

- **密码缺失**：
  如果出现“需要备份密码”的提示，请要求用户提供密码，或建议用户设置MEMBASE_BACKUP_PASSWORD环境变量。

- **密码无效**：
  如果出现“密码无效”或“解密失败”的提示，说明用户提供的密码不正确，请要求用户重新输入正确的密码。

- **未找到备份**：
  如果列表显示“未找到备份文件”，说明尚未创建任何备份文件，建议用户先创建备份。

- **网络错误**：
  如果连接失败，请检查网络连接是否正常，并确认MEMBASE_ENDPOINT地址是否正确。可以稍后再尝试。

## 对代理的建议

1. 在请求用户操作之前，**始终先检查密码是否已设置**。
2. **清晰地显示备份ID**，以便用户能够保存它。
3. 如果输出了JSON格式的数据（位于`---JSON_OUTPUT---`和`---END_JSON---`之间），请确保代理能够正确解析这些数据。
4. **明确说明安全性要求**，强调恢复数据需要密码。
5. 在首次备份后，建议用户使用增量备份方式以提高效率。
6. 帮助用户记住`list`命令输出的备份ID，以便后续进行恢复或比较操作。

## 示例

### 完整的备份工作流程
```bash
# 1. Check status
node membase.ts status

# 2. First backup (full)
node membase.ts backup --password "MySecure123Pass"

# 3. Later: incremental backup
node membase.ts backup --password "MySecure123Pass" --incremental

# 4. List all backups
node membase.ts list

# 5. Compare recent backups
node membase.ts diff backup-id-1 backup-id-2 --password "MySecure123Pass"

# 6. Restore if needed
node membase.ts restore backup-id-1 --password "MySecure123Pass"
```

## 故障排除

- **命令未找到**：
  确保你位于`skills/membase`目录下。

- **模块未找到**：
  确保`lib`文件夹已链接到编译后的源代码文件。

- **权限拒绝**：
  请确保`membase.ts`文件具有可执行权限。

## 更多信息

- [Membase文档](https://github.com/unibaseio/membase)
- [代理技能规范](https://agentskills.io)
- [OpenClaw技能指南](https://docs.openclaw.ai/tools/skills)
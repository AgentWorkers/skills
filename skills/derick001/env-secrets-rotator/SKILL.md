---
name: env-secrets-rotator
description: 在环境文件中旋转和更新密钥，生成 Vault 命令，并管理密钥轮换的工作流程。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
---
# 环境变量密钥轮换工具

## 功能简介

这是一个命令行（CLI）工具，用于帮助轮换环境文件中的密钥，并为像 HashiCorp Vault 这样的密钥管理系统生成相应的命令。该工具能够安全地生成新的随机密钥值，更新 `.env` 文件，并为开发环境和生产环境提供密钥轮换的自动化流程。

**主要功能：**
- **轮换 `.env` 文件中的密钥**：为指定的密钥生成新的随机值。
- **多种生成算法**：支持十六进制（hex）、Base64、UUID 以及自定义长度的密钥。
- **备份原始文件**：在修改文件前会创建备份。
- **预览模式**：在不修改文件的情况下预览更改内容。
- **生成 Vault 命令**：生成用于 HashiCorp Vault 的密钥轮换命令。
- **批量处理**：可以同时轮换多个文件中的多个密钥。
- **验证 `.env` 文件格式**：检查文件格式及密钥是否存在。
- **记录轮换历史**：可选功能，用于追踪密钥的轮换记录。

## 使用方法

### 基本使用示例：
```bash
./scripts/main.py rotate --file .env --keys API_KEY,DB_PASSWORD
```

### 使用自定义生成算法的示例：
```bash
./scripts/main.py rotate --file .env --keys API_KEY --algorithm base64 --length 32
```

### 预览模式示例：
```bash
./scripts/main.py rotate --file .env --keys "*" --dry-run
```

### 生成 Vault 命令的示例：
```bash
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/myapp
```

### 完整的命令参考：
```bash
./scripts/main.py help
```

## 命令列表

- `rotate`：轮换环境文件中的密钥
  - `--file`：.env 文件的路径（必选）
  - `--keys`：需要轮换的密钥，用逗号分隔；或使用“*”表示全部密钥（默认值：“*”）
  - `--algorithm`：密钥生成算法：hex、base64、uuid、字母数字组合（默认值：hex）
  - `--length`：生成的密钥长度（默认值：32）
  - `--backup`：修改文件前创建备份（默认值：true）
  - `--dry-run`：预览更改内容而不修改文件
  - `--output`：将结果写入新文件而非修改原始文件

- `vault`：生成用于 HashiCorp Vault 的命令
  - `--keys`：需要生成命令的密钥列表，用逗号分隔
  - `--path`：Vault 中密钥的存储路径（例如：“secret/data/myapp”）
  - `--engine`：Vault 的密钥存储引擎（默认值：“kv”）
  - `--method`： Vault 中的密钥更新方法（默认值：“patch”）

- `validate`：验证 `.env` 文件的格式
  - `--file`：.env 文件的路径
  - `--strict`：要求所有密钥值都不为空

- `history`：显示密钥轮换历史记录（如果已启用）
  - `--file`：.env 文件的路径
  - `--key`：要显示历史记录的特定密钥

## 输出结果

- **轮换结果**：显示轮换后的密钥值（格式示例）：```json
{
  "file": ".env",
  "rotated": ["API_KEY", "DB_PASSWORD"],
  "new_values": {
    "API_KEY": "a1b2c3d4e5f6...",
    "DB_PASSWORD": "x9y8z7w6v5u4..."
  },
  "backup": ".env.backup.20260311",
  "vault_commands": [
    "vault kv patch secret/data/myapp API_KEY=a1b2c3d4e5f6...",
    "vault kv patch secret/data/myapp DB_PASSWORD=x9y8z7w6v5u4..."
  ]
}
```

- **生成的 Vault 命令**：显示用于更新 Vault 的命令（格式示例）：```bash
# Generated Vault commands for secret rotation:
vault kv patch secret/data/myapp API_KEY=a1b2c3d4e5f6...
vault kv patch secret/data/myapp DB_PASSWORD=x9y8z7w6v5u4...
```

## 限制说明

- **无实际的 Vault 集成**：仅生成命令，需手动执行这些命令。
- **仅支持本地文件**：无法在远程密钥管理系统中轮换密钥。
- **不支持密钥分发**：不会将新生成的密钥自动分配给其他服务。
- **仅支持简单的 `.env` 文件格式**：仅支持 KEY=VALUE 的格式，不支持多行或复杂的文件结构。
- **无加密功能**：生成的密钥以明文形式显示。
- **历史记录功能可选**：启用该功能可能会存储敏感数据。

## 安全注意事项

- 使用前请务必检查生成的密钥值。
- 使用 `--dry-run` 选项预览更改内容。
- 程序会自动创建备份文件。
- 生成的密钥使用 Python 的 `secrets` 模块进行加密处理。
- 对于生产环境中的敏感密钥，请使用专业的密钥管理系统。

## 使用示例

- 轮换 `.env` 文件中的所有密钥：```bash
./scripts/main.py rotate --file .env --keys "*" --backup true
```

- 为特定密钥生成 Vault 命令：```bash
./scripts/main.py vault --keys API_KEY,DB_PASSWORD --path secret/data/production
```

- 在轮换前验证 `.env` 文件的内容：```bash
./scripts/main.py validate --file .env --strict
```

- 使用自定义的 Base64 格式生成密钥：```bash
./scripts/main.py rotate --file .env --keys JWT_SECRET --algorithm base64 --length 64
```

## 安装说明

该工具依赖 Python 内置的 `secrets` 模块来实现安全的随机密钥生成，无需额外安装任何外部依赖库。
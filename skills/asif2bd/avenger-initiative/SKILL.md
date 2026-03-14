---
name: avenger-initiative
version: 1.0.4
description: >
  **加密的GitHub备份与恢复功能**  
  适用于所有OpenClaw代理系统：  
  - 每晚自动创建备份（分为7个每日备份、8个每周备份和12个每月备份），并采用智能保留策略进行管理。  
  - 备份内容包括`openclaw.json`文件（使用AES-256加密）、代理内存数据、`SOUL/IDENTITY`文件、`cron`作业以及自定义技能配置。  
  - 所有备份数据会被存储到私有的GitHub仓库中。  
  - 每个备份文件都会自动生成一个易于阅读的`README.md`文件，其中包含备份目的、完整内容列表、分支结构、详细的恢复步骤以及Avenger代理的相关命令。  
  - 可通过以下命令触发备份/恢复操作：  
    - `avenger backup`  
    - `backup system`  
    - `push to vault`  
    - `sync vault`  
    - `avenger restore`  
    - `restore from vault`  
    - `setup avenger`  
    - `avenger status`  
    - `avenger init`  
    - `configure backup`  
    - `set up backup`  
  - 此功能还会在配置发生任何关键变化时自动执行备份操作。
license: MIT
---
# 🛡️ Avenger Initiative  
为任何 OpenClaw 系统提供基于分支的加密备份和恢复功能。  

## 触发该功能的场景  
1. 用户输入 “setup avenger” / “configure backup” / “avenger init” → **执行设置流程**  
2. 用户输入 “avenger backup” / “backup system” / “push to vault” → **执行备份操作**  
3. 用户输入 “restore from vault” / “avenger restore” → **执行恢复操作**  
4. 用户输入 “avenger status” / “vault status” → **显示系统状态**  
5. 在配置发生任何变更后（例如网关重启、配置更新） → **自动执行备份操作**  

---

## 设置流程（由系统引导）  
当设置流程被触发时，系统会与用户进行交互式对话，每次只提出一个问题。  

### 第一步：请求备份仓库地址  
> “为了设置 Avenger Initiative，我需要一个私有的 GitHub 仓库作为备份存储空间。您已经创建好了吗？如果有，请分享仓库地址（例如：`https://github.com/yourname/my-vault`）。如果没有，我可以帮您创建一个。”  

### 第二步：处理加密密钥  
> “您的 `openclaw.json` 文件（其中包含所有 API 密钥和机器人令牌）在上传前会使用 AES-256 算法进行加密。您之前是否有加密密钥？还是需要我为您生成一个新的？”  

### 第三步：执行设置  
```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/setup.sh \
  --repo <vault-url>
```  

### 第四步：显示密钥并要求用户保存  
> “⚠️ **您的加密密钥如下——请立即将其保存到 1Password、Bitwarden 或其他安全密码管理工具中。**  
> 没有这个密钥，您的备份将无法被解密。”  
等待用户确认密钥已保存后再继续下一步。  

### 第五步：说明备份的内容  
- 🔐 `openclaw.json` 文件：包含所有 API 密钥、机器人令牌及代理配置  
- 🧠 所有内存日志和工作区文件（SOUL、IDENTITY、MEMORY、TOOLS）  
- 👥 每个代理的专属文件  
- 🔧 所有自定义技能相关文件  
- 📋 Cron 作业定义  

**备份保留策略：**  
- 每日备份 → 保留 7 天  
- 每周备份 → 保留 8 周（每周日生成）  
- 每月备份 → 保留 12 个月（每月 1 日生成）  

### 第六步：执行首次备份并安装 Cron 作业  
```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/backup.sh
```  

---

## 备份操作  
```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/backup.sh
```  
1. 创建 `backup/daily/YYYY-MM-DD` 分支  
2. 将备份文件合并到 `main` 分支  
3. 根据保留策略定期删除旧备份文件  
4. 每周日：还会创建 `backup/weekly/YYYY-WNN` 分支  
5. 每月 1 日：还会创建 `backup/monthly/YYYY-MM` 分支  

---

## 恢复操作  
```bash
bash ~/.openclaw/workspace/skills/avenger-initiative/scripts/restore.sh
```  
支持使用 `--branch backup/daily/YYYY-MM-DD` 参数从特定备份版本进行恢复。  
系统会显示备份清单，请求用户确认后解密并恢复所有文件。  
恢复完成后：系统会自动重启 OpenClaw 网关。  

## 系统状态  
查看 `~/.openclaw/workspace/memory/avenger-backup.log` 文件以获取最新备份信息，包括备份时间、分支名称和备份仓库地址。  

## 文件存储位置  
```
~/.openclaw/
├── credentials/
│   ├── avenger.key              ← Encryption key (NEVER commit)
│   └── avenger-config.json     ← Vault repo URL
└── workspace/skills/avenger-initiative/
    ├── SKILL.md
    ├── scripts/
    │   ├── backup.sh
    │   ├── restore.sh
    │   └── setup.sh
    └── references/
        └── security.md
```  

## 安全性要求：  
- 备份仓库必须设置为 **私有的** GitHub 仓库  
- `openclaw.json` 文件使用 AES-256-CBC 算法加密（PBKDF2，100,000 次迭代）  
- 其他文件均为明文格式（不包含敏感信息）  
- 加密密钥仅存储在本地机器和用户的密码管理工具中  

有关威胁模型和密钥轮换策略的详细信息，请参阅 `references/security.md`。  

*更多经过验证的 OpenClaw 功能请访问 [proskills.md](https://proskills.md)*
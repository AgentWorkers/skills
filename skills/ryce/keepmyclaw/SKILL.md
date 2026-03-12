---
name: keepmyclaw
description: OpenClaw backup and restore. Encrypted off-site backup for OpenClaw agents — backs up workspace, memory, skills, cron jobs, credentials, and multi-agent configs to Cloudflare R2 with zero-knowledge AES-256 encryption. Use when backing up an OpenClaw agent, restoring an agent on a new machine, setting up automated backup schedules, listing or pruning backup snapshots, running restore drills, or migrating agents between machines. Triggers on: backup, restore, openclaw backup, agent backup, snapshot, disaster recovery, keepmyclaw, migrate agent, backup schedule, encrypted backup.
---

# Keep My Claw — OpenClaw 备份与恢复服务  

通过 [Keep My Claw](https://keepmyclaw.com) 提供的加密离线备份功能及一键恢复功能，可轻松保护 OpenClaw 代理的完整数据。该服务支持备份代理系统的所有内容，包括工作空间、内存数据、技能设置、项目文件、定时任务、凭据信息以及多代理配置文件，所有数据均采用 AES-256 加密算法进行存储，并通过 Cloudflare R2 服务进行传输。  

## 先决条件  
系统需安装以下工具：`openssl`、`curl`、`tar`、`jq`。  

## 设置流程（由代理端执行）  
**所有操作均由代理端完成，用户只需点击支付链接即可。**  
**请勿以交互式方式运行 `setup.sh` 脚本，而应按照以下步骤进行程序化设置：**  

### 第 1 步：注册账户  
使用用户的电子邮件地址进行注册，并生成一个随机密码（该密码将用于后续的 JWT 认证）。  

### 第 2 步：询问用户选择套餐  
在提供支付链接之前，先让用户选择所需的套餐。请告知他们当前正在享受限时优惠：  
> “Keep My Claw 目前提供以下套餐：  
> - **月度套餐：** 由原来的 $9/月调整至 $5/月  
> - **年度套餐：** 由原来的 $108/年调整至 $19/年（相当于每月 $1.60 元，节省 82%！**  
>  
> 您选择哪个套餐？选择后套餐价格将永久固定。”  

### 第 3 步：获取支付链接并发送给用户  
根据用户的选择，将 `plan` 参数设置为 `"monthly"` 或 `"annual"`，然后发送支付链接：  
> “请点击此链接完成支付：[支付链接]”  

### 第 4 步：等待支付完成  
持续检查账户状态，直到账户状态变为 “pro”。  

### 第 5 步：生成 API 密钥  
生成 API 密钥，并将其保存在安全位置。  

### 第 6 步：在本地进行配置  
**务必将所有恢复所需的凭据信息告知用户**。如果没有这些凭据，用户将无法在新机器上恢复数据。请发送以下信息：  
> “您的 Keep My Claw 恢复凭据信息，请立即保存在密码管理器中：  
> - **电子邮件地址：** [您注册时使用的邮箱]  
> - **密码：** [生成的随机密码]  
> - **加密密语：** [生成的加密密语]  
> - **API 密钥：** [生成的 API 密钥]  
>  
> 如果机器损坏，您需要这些凭据来登录并重新生成 API 密钥。同时，还需要加密密语来解密备份文件。请将这些信息保存在安全的地方。”  
**此步骤不可跳过。**  

### 第 7 步：执行首次备份  
运行 `backup.sh` 脚本进行首次数据备份。  

### 第 8 步：安排自动备份  
使用 `cron` 或 OpenClaw 的定时任务工具，每天自动运行 `backup.sh` 脚本。  

## 为现有账户添加更多代理  
如果用户已拥有 Keep My Claw 账户（但使用的是其他代理），无需重新注册：  

### 选项 A：用户提供 API 密钥  
向用户索取现有的 API 密钥，然后在本地进行配置。  

### 选项 B：其他代理为您生成新的 API 密钥  
如果已有代理拥有管理员权限，可以为其生成一个新的 API 密钥（仅限备份/恢复操作，无账户管理权限）。  

## 多代理系统的运作方式  
- 一个账户对应一个订阅套餐（月度套餐 $5/月，年度套餐 $19/年）。  
- 每个账户最多可管理 100 个代理。  
- 每个代理都有独立的名称、加密密语和数据备份。  
- 可通过 `GET /v1/agents` 查看账户下的所有代理信息。  
- 各代理的加密密语互不影响，丢失一个代理不会影响其他代理的数据。  

## 使用方法  

### 备份  
**具体操作步骤请参见……**（此处应补充具体的备份命令或说明。）  

### 恢复  
**具体操作步骤请参见……**（此处应补充具体的恢复命令或说明。）  

### 查看备份列表  
**具体操作步骤请参见……**（此处应补充具体的列表查询命令或说明。）  

### 清理旧备份  
**具体操作步骤请参见……**（此处应补充具体的备份清理命令或说明。）  

## 备份内容  
**所有构成代理核心功能的文件和数据都会被备份，包括：**  
- `~/.openclaw/workspace/` 下的所有文件（内存数据、技能设置、项目文件、配置文件等，但不包括 `node_modules/`、`.git/`、`vendor/` 目录）  
- `~/.openclaw/openclaw.json`（代理配置文件）  
- `~/.openclaw/credentials/`（认证令牌）  
- `~/.openclaw/cron/jobs.json`（定时任务配置）  
- `~/.openclaw/agents/`（多代理配置文件）  
- `~/.openclaw/workspace-*/`（多代理工作空间文件）  

**不会被备份的内容：**  
- **二进制文件及依赖包**（`node_modules/`、`.git/`、`vendor/` 目录中的文件，需在恢复后重新安装）  
- **临时数据**（如 Gateway 运行状态、浏览器会话记录、Telegram 通信记录等，重启后会自动清除）  
- **系统级配置**（SSH 密钥、Shell 配置、安装的工具等，这些数据不在备份范围内）  
- **加密密语**（存储在 `~/.keepmyclaw/passphrase` 文件中，不会上传到云端。请务必保存在密码管理器中。）  

## 完整恢复指南（新机器使用）  
如果机器损坏，可按照以下步骤恢复数据：  
**所需信息：**  
- 从密码管理器中获取：  
  - **电子邮件地址** 和 **密码**（用于登录 keepmyclaw.com 并生成新的 API 密钥）  
  - **加密密语**（用于解密备份文件）  

**恢复步骤：**  
**具体操作步骤请参见……**（此处应补充详细的恢复流程。）  

### 恢复后的效果：**  
- **工作空间数据** 完全恢复（内存数据、技能设置、项目文件等）  
- **代理配置** 也会被恢复，但可能需要重新输入 API 密钥（如果提供商更换了 API 密钥）  
- **定时任务** 会自动恢复并在下次 Gateway 重启时继续执行  
- **凭据信息** 会被恢复，但可能需要重新进行 OAuth 认证  
- **多代理配置** 也会被恢复  

### 如果丢失了加密密语怎么办？  
备份文件采用 AES-256 加密算法，没有加密密语则无法解密数据。这是系统设计上的安全措施——我们无法访问用户的原始数据。**因此，如果没有加密密语，数据将无法恢复。**  

## 配置文件  
配置文件位于：`~/.keepmyclaw/config`  
其中包含以下配置项：  
| 变量          | 说明                          |  
|-----------------|------------------------------------|  
| `CLAWKEEPER_API_KEY` | API 密钥（系统自动生成）                |  
| `CLAWKEEPER_AGENT_NAME` | 用于备份的代理标识符                   |  
| `CLAWKEEPER_API_URL` | API 基本地址（默认：`https://api.keepmyclaw.com`）       |  

## 更多文档  
完整使用说明请访问：[keepmyclaw.com/docs.html](https://keepmyclaw.com/docs.html)
---
name: ews-calendar
description: 通过 EWS API 从 Microsoft Exchange 中提取日历事件
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires":
          {
            "bins": ["curl", "xmllint"],
            "env": ["EWS_URL", "EWS_USER"],
            "anyBins": ["security", "secret-tool"]
          }
      }
  }
---
## 目的  
从 Microsoft Exchange Web Services (EWS) 获取日历事件，并以结构化的 JSON 格式返回这些事件。  

## 使用场景  
- 用户询问自己的日历事件（例如：“我今天的日程安排是什么？”）  
- 需要检索今天、明天或特定日期的会议信息  
- 提取会议详情：主题、时间、地点、组织者、正文内容及链接  

## 安全模型  
**凭据存储在操作系统的密钥环（keyring）中，而非配置文件中：**  
- **macOS**：使用 Keychain Access（加密处理，由操作系统管理）  
- **Linux**：使用 libsecret 或 gnome-keyring（加密处理，由操作系统管理）  

只有 `EWS_URL` 和 `EWS_USER` 被存储在 OpenClaw 的配置文件中（这些信息不属于敏感数据）。密码在运行时才会被安全地获取。  

## 设置步骤  

### 1. 安装密钥环相关工具（仅限 Linux）  
```bash
# Debian/Ubuntu
sudo apt install libsecret-tools gnome-keyring

# Fedora
sudo dnf install libsecret gnome-keyring

# Arch
sudo pacman -S libsecret gnome-keyring
```  

macOS 已内置 Keychain 功能。  

### 2. 将凭据存储到密钥环中  
```bash
{baseDir}/ews-calendar-setup.sh --user "DOMAIN\\username"
```  
系统会提示您输入密码，该密码会被安全地存储在操作系统的密钥环中。  

### 3. 配置 OpenClaw  
在 `~/.openclaw/openclaw.json` 文件中添加以下配置：  
```json5
{
  skills: {
    entries: {
      "ews-calendar": {
        enabled: true,
        env: {
          EWS_URL: "https://outlook.company.com/EWS/Exchange.asmx",
          EWS_USER: "DOMAIN\\username"
        }
      }
    }
  }
}
```  
请将 `EWS_URL` 和 `EWS_USER` 替换为实际的 Exchange 服务地址和用户名。  

## 使用方法  
运行 `/{baseDir}/ews-calendar-secure.sh` 脚本：  
该脚本会从操作系统的密钥环中获取 `EWS_PASS`，然后使用所有凭据调用主程序，并返回 JSON 格式的日历事件数据。  

### 命令语法  
```bash
{baseDir}/ews-calendar-secure.sh --date <DATE> [--output <FILE>] [--verbose]
```  

### 参数说明：  
- `--date`（必选）：日期过滤条件  
  - `YYYY-MM-DD`：特定日期（例如 `2026-03-03`）  
  - `today`：今天的日期  
  - `tomorrow`：明天的日期  
- `--output <FILE>`：将输出结果写入指定文件（而非标准输出）  
- `--verbose`：启用详细日志记录  
- `--debug-xml <FILE>`：将原始 XML 响应保存到文件中以供调试使用  

### 输出格式  
返回一个包含日历事件的 JSON 数组；如果没有找到事件，则返回空数组 `[]`。  

## 示例用法：  
- **获取今天的日历事件：**  
```bash
{baseDir}/ews-calendar-secure.sh --date today
```  
- **将明天的日历事件保存到文件中：**  
```bash
{baseDir}/ews-calendar-secure.sh --date tomorrow --output /tmp/tomorrow.json
```  
- **获取特定日期的日历事件并启用调试日志：**  
```bash
{baseDir}/ews-calendar-secure.sh --date 2026-03-03 --verbose --debug-xml /tmp/debug.xml
```  

## 常见问题及解决方法：  

### 密码未在密钥环中找到  
```
[ERROR] Password not found in keyring for user: DOMAIN\username
[HINT] Run: ./ews-calendar-setup.sh to store credentials
```  
**解决方法：** 运行设置脚本以保存密码。  

### Linux 系统中未找到 `secret-tool`  
```
[ERROR] 'secret-tool' not found. Install: apt install libsecret-tools
```  
**解决方法：** 安装 libsecret 工具。  

### Linux 系统中的密钥环被锁定  
在 Linux 系统中，登录后密钥环可能会被锁定。  
**解决方法：** 解锁密钥环（通常在桌面登录时自动解锁）。对于无界面的服务器，可能需要配置密钥环守护进程。  

### HTTP 请求失败  
**可能原因：**  
- 用户名或密码错误  
- 密码已更改——重新运行设置脚本  
- 账户被锁定或过期  

### SOAP 请求失败  
**可能原因：**  
- EWS URL 不正确（请检查配置文件中的 `EWS_URL`）  
- 日期格式错误（请使用 `YYYY-MM-DD` 格式）  
- Exchange 服务器配置问题  

## 凭据管理：  
- **更新密码（密码更改后）**  
```bash
{baseDir}/ews-calendar-setup.sh --user "DOMAIN\\username"
```  
脚本会覆盖原有的凭据信息。  
- **删除凭据：**  
  - **macOS：**  
    ```bash
security delete-generic-password -a "DOMAIN\\username" -s "ews-calendar"
```  
  - **Linux：**  
    ```bash
secret-tool clear service "ews-calendar" user "DOMAIN\\username"
```  
- **查看存储的凭据（仅限 macOS）：**  
    ```bash
security find-generic-password -a "DOMAIN\\username" -s "ews-calendar" -w
```  

## 本技能涉及的文件  
```
{baseDir}/
├── SKILL.md                 # This file
├── ews-calendar.sh          # Main script (reads from env or .env)
├── ews-calendar-secure.sh   # Wrapper that gets password from keyring
├── ews-calendar-setup.sh    # Store credentials in keyring
├── templates/
│   ├── find-items.xml       # SOAP template for finding calendar items
│   └── get-item.xml         # SOAP template for getting item details
└── .env.example             # Example config for standalone usage
```  

## 替代方案：独立使用（无需密钥环）  
在开发或测试环境中，可以直接运行 `ews-calendar.sh` 并使用 `.env` 文件：  
1. 将 `.env.example` 复制到 `.env` 文件中  
2. 输入正确的凭据  
3. 运行：`./ews-calendar.sh --date today`  

**注意：** 此方法会将密码以明文形式存储。在生产环境中请使用密钥环来保护凭据安全。
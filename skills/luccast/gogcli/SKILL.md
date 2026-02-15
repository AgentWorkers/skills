---
名称：gogcli  
描述：Gmail、Calendar、Drive、 Sheets、Docs、Slides、Contacts、Tasks、People、Groups、Keep 的 Google Workspace 命令行工具（CLI）。当用户需要与 Google 服务进行交互时可以使用该工具。  

# gogcli - Google Workspace 命令行工具  

## 概述  
gogcli 是一个用于通过终端管理 Google Workspace 服务的命令行工具，支持 Gmail、Calendar、Drive、 Sheets、Docs、Slides、Contacts、Tasks、People、Groups 和 Keep 等服务。  

## 安装  

### 快速安装（如果您使用的是 brew）：  
```bash
brew install steipete/tap/gogcli
```  

### 从源代码编译（不使用 brew）：  
```bash
# 1. Clone repository
git clone https://github.com/steipete/gogcli.git

# 2. Navigate to directory
cd gogcli

# 3. Build
make

# 4. (Optional) Make available globally
sudo make install
```  

## 首次使用前的设置  

在使用 gogcli 之前，请先设置 OAuth 凭据：  

**步骤 1：获取 OAuth 客户端凭据**  
1. 访问 Google Cloud 控制台的“APIs & Services”页面。  
2. 创建一个新的项目或使用现有的项目。  
3. 进入 OAuth 同意页面。  
4. 创建一个 OAuth 2.0 客户端，设置如下参数：  
   - 应用程序类型：“桌面应用程序”  
   - 名称：“gogcli for Clawdbot”  
   - 授权重定向 URI：`http://localhost:8085/callback`  
5. 启用所需的 API。  
6. 下载 OAuth 客户端凭据的 JSON 文件，并将其保存到 `~/Downloads/` 目录下。  

**步骤 2：授权您的账户**  
```bash
cd gogcli
./bin/gog auth add you@gmail.com ~/Downloads/client_secret_....json
```  

**步骤 3：验证**  
```bash
./bin/gog auth list
./bin/gog gmail search 'is:unread' --max 5
```  

## 常用命令  

### Gmail  
```bash
# Search
./bin/gog gmail search 'query' --max 20

# Send
./bin/gog gmail send 'recipient@gmail.com' --subject 'Hello' --body 'Message'

# Labels
./bin/gog gmail labels list
```  

### Calendar  
```bash
# List events
./bin/gog calendar events list --max 50

# Create event
./bin/gog calendar events create 'Meeting' --start '2026-01-30T10:00'
```  

### Drive  
```bash
# List files
./bin/gog drive ls --query 'pdf' --max 20

# Upload file
./bin/gog drive upload ~/Documents/file.pdf
```  

### Sheets  
```bash
# List sheets
./bin/gog sheets list

# Export sheet
./bin/gog sheets export <spreadsheet-id> --format pdf
```  

### Contacts  
```bash
./bin/gog contacts search 'John Doe'
```  

### Tasks  
```bash
# List tasklists
./bin/gog tasks list

# Add task
./bin/gog tasks add --title 'Task' --due '2026-01-30'
```  

## 注意事项：  
- 使用 `--json` 标志进行脚本编写。  
- 凭据存储在 `~/.config/gog/` 文件中。  
- 使用 `gog auth list` 命令查看授权状态。
---

**名称：fb-inbox-forward**  
**描述：** 通过 `graph.facebook.com` 检查 Facebook 页面的收件箱，并将新收到的消息（包括发送者名称、完整消息文本和对话 ID）转发到配置好的 OpenClaw 通道。**所需环境：** PowerShell（Windows）或 pwsh（macOS/Linux）；系统中必须包含 OpenClaw CLI；配置文件位于 `~/.config/fb-page/credentials.json`（其中包含 `FB_PAGE_TOKEN` 和 `FB_PAGE_ID`）；转发配置文件位于 `~/.config/fb-inbox-forward/config.json`（包含 `NOTIFY_CHANNEL` 和 `NOTIFY_TARGET`）。**工作原理：** 会在 `~/.config/fb-inbox-forward/worker.ps1` 中生成一个具有受限权限的脚本（使用 `icacls/chmod 600` 设置权限），该脚本仅用于执行转发操作，且不会将任何令牌以字符串形式嵌入脚本中。**注意：** 监听器仅在用户明确请求时才会启动；日志中仅记录发送者名称和对话 ID，完整消息文本会直接转发到目标通道，而不会被保存到磁盘上。**安全提示：** 确保转发目标可信，并遵守相关平台的条款和隐私政策。所有 API 请求均通过 `graph.facebook.com` 发送。  

---

### 主要功能：  
- 每 15 秒检查一次 Facebook 页面的收件箱。  
- 将新收到的客户消息转发到已连接的 OpenClaw 通道。  
- 运行时从 `fb-page` 配置文件中读取 Facebook 凭据。  

---

## **步骤 1：加载凭据**  
- 从 `fb-page` 配置文件中读取 Facebook 凭据：  
  **代码示例：**  
  ```powershell
$fb     = Get-Content "$HOME/.config/fb-page/credentials.json" -Raw | ConvertFrom-Json
$token  = $fb.FB_PAGE_TOKEN
$pageId = $fb.FB_PAGE_ID
```  
  （如果凭据缺失，请提示用户先设置 `fb-page` 配置。）  

- 从 `~/.config/fb-inbox-forward/config.json` 中读取转发配置：  
  **代码示例：**  
  ```powershell
$cfg      = Get-Content "$HOME/.config/fb-inbox-forward/config.json" -Raw | ConvertFrom-Json
$channel  = $cfg.NOTIFY_CHANNEL
$target   = $cfg.NOTIFY_TARGET
$interval = if ($cfg.POLL_INTERVAL_SEC) { [int]$cfg.POLL_INTERVAL_SEC } else { 15 }
```  
  （如果配置文件缺失，请运行设置脚本。）  

- 保存配置文件后，立即为该目录下的所有文件设置受限权限：  
  **代码示例：**  
  ```powershell
$dir = "$HOME/.config/fb-inbox-forward"
if ($env:OS -eq "Windows_NT") {
    "config.json","worker.ps1","listener.log","listener.pid","listener-state.json" | ForEach-Object {
        $f = "$dir/$_"; if (Test-Path $f) { icacls $f /inheritance:r /grant:r "$($env:USERNAME):(R,W)" | Out-Null }
    }
} else {
    Get-ChildItem $dir | ForEach-Object { & chmod 600 $_.FullName }
}
```  

- **注意：** 请勿将 `~/.config/fb-inbox-forward/` 目录下的任何文件提交到版本控制系统中。  

---

## **步骤 2：核心操作**  
- **启动/停止监听器：** 参见 “背景监听器” 部分。  
- **检查状态：** 参见 “背景监听器” 部分。  
- **查看日志：** `Get-Content "$HOME/.config/fb-inbox-forward/listener.log" -Tail 20`  
- **测试凭据：** 发送请求到 `/me` 端点以验证凭据有效性：  
  **代码示例：**  
  ```powershell
$fb = Get-Content "$HOME/.config/fb-page/credentials.json" -Raw | ConvertFrom-Json
$r  = Invoke-RestMethod "https://graph.facebook.com/v25.0/me?access_token=$($fb.FB_PAGE_TOKEN)" -ErrorAction Stop
Write-Host "Connected as: $($r.name)"
```  

---

## **错误处理**  
- **常见错误代码及解决方法：**  
  | 代码 | 含义 | 处理方法 |  
  |---|---|---|  
  | 190 | 令牌过期/无效 | 在 `fb-page` 配置中重新生成令牌。  
  | 10/200 | 权限被拒绝 | 在应用中添加 `pages_read_engagement` 权限。  
  | 368 | 被限制访问频率 | 增加 `POLL_INTERVAL_SEC` 的值（建议设置为 60 秒以上）。  
  | 100 | 参数无效 | 检查 `fb-page` 凭据中的 `FB_PAGE_ID` 是否正确。  

---

### **背景监听器（可选）**  
- **启动条件：** 仅在用户明确请求时启动。  
- **处理的数据：**  
  - `FB_PAGE_TOKEN` 和 `FB_PAGE_ID` 来自 `~/.config/fb-page/credentials.json`。  
  - 转发的内容：发送者名称、完整消息文本和对话 ID（通过 `openclaw` 的 `message send` 命令发送到 `NOTIFY_CHANNEL`/`NOTIFY_TARGET`）。  
  - **日志记录：** 仅记录发送者名称和对话 ID，不记录消息内容或令牌。  
- **脚本说明：** 转发脚本（`worker.ps1`）具有受限权限，运行时从磁盘读取最新凭据（不会将令牌嵌入脚本）。  
- **自动启动：** 绝不自动启动，必须由用户明确请求。  

---

### **其他注意事项：**  
- **启动/停止监听器：** 参见相应的代码块。  
- **状态检查：** 参见 “背景监听器” 部分。  
- **代理规则：**  
  - 从 `~/.config/fb-page/credentials.json` 中加载 Facebook 凭据；如果缺失，请提示用户设置。  
  - 从 `~/.config/fb-inbox-forward/config.json` 中加载转发配置；如果缺失，请运行设置脚本。  
  - 监听器仅在用户请求时启动。  
  - 确保转发目标可信，并遵守平台规定。  
  - 从不将令牌以字符串形式嵌入脚本中。  
  - 运行时始终从磁盘读取最新凭据。  
  - 日志中仅记录发送者名称和对话 ID。  
  - 所有目标信息和敏感数据均来自配置文件。  
  - 遇到错误时，根据错误代码提供具体处理建议。  
  - 根据操作系统环境（`env:OS`）选择使用 PowerShell 或 pwsh。  
  - 启动前需确认用户同意转发目标。  
  - 通知用户：完整消息内容会被转发到指定目标，而不仅仅是元数据。
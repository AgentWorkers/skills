---
name: tiktok-page
description: "**所需环境：** PowerShell 或 PwSH。  
**数据来源：** 文件 `~/.config/tiktok-page/credentials.json`（包含以下字段：`TIKTOK_ACCESS_TOKEN`、`TIKTOK_CLIENT_KEY`、`TIKTOK_CLIENT_SECRET`、`TIKTOK_OPEN_ID`）。  
**功能说明：** 通过 TikTok 内容发布 API（`open.tiktokapis.com/v2`）与 TikTok 账号进行交互，支持执行以下操作：发布视频、查看视频列表、获取账号信息以及添加评论。  
**注意事项：**  
- 访问令牌的有效期为 24 小时，需使用 `TIKTOK_REFRESH_TOKEN` 进行刷新。  
- 仅授予最低权限级别的访问权限，确保数据不会被转发给第三方；所有请求均发送至 `open.tiktokapis.com`。"
metadata: {"openclaw":{"emoji":"[tt]","requires":{"anyBins":["powershell","pwsh"]}}}
---
# tiktok-page — 通用 TikTok API 技能

该技能可以根据用户的需求，直接构建并执行 TikTok API 调用，无需编写任何脚本。

API 基本地址：`https://open.tiktokapis.com/v2`

---

## 第 1 步 - 加载凭据

凭据存储在 `~/.config/tiktok-page/credentials.json` 文件中。

```powershell
$cfg          = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$accessToken  = $cfg.TIKTOK_ACCESS_TOKEN
$refreshToken = $cfg.TIKTOK_REFRESH_TOKEN
$clientKey    = $cfg.TIKTOK_CLIENT_KEY
$clientSecret = $cfg.TIKTOK_CLIENT_SECRET
$openId       = $cfg.TIKTOK_OPEN_ID
```

如果该文件不存在，请按照以下步骤进行设置：

| 字段 | 用途 |
|---|---|
| TIKTOK_ACCESS_TOKEN | OAuth2 访问令牌——用于所有 API 调用 |
| TIKTOK_REFRESH_TOKEN | 用于在访问令牌过期时刷新令牌 |
| TIKTOK_CLIENT_KEY | 来自 TikTok 开发者门户的应用客户端密钥 |
| TIKTOK_CLIENT_SECRET | 应用客户端密钥——仅用于刷新令牌 |
| TIKTOK_OPEN_ID | 在 OAuth 过程中返回的 TikTok 用户 ID |

**一次性 OAuth2 设置：**
```
1. Go to https://developers.tiktok.com — create or select your app
2. Add redirect URI (e.g. https://localhost or your callback URL)
3. Note your Client Key and Client Secret
4. Direct user to:
   https://www.tiktok.com/v2/auth/authorize/?client_key=CLIENT_KEY&redirect_uri=REDIRECT_URI&response_type=code&scope=user.info.basic,video.list,video.publish,video.upload,comment.list&state=random
5. After redirect, copy the code param from the callback URL
```

```powershell
# Exchange auth code for tokens
$clientKey   = "<your-client-key>"
$clientSecret = "<your-client-secret>"
$code        = "<auth-code-from-redirect>"
$redirectUri = "<your-redirect-uri>"

$body = "client_key=$clientKey&client_secret=$clientSecret&code=$code&grant_type=authorization_code&redirect_uri=$redirectUri"
$r = Invoke-RestMethod "https://open.tiktokapis.com/v2/oauth/token/" -Method POST `
    -Headers @{ "Content-Type" = "application/x-www-form-urlencoded" } -Body $body -ErrorAction Stop

New-Item -ItemType Directory -Force -Path "$HOME/.config/tiktok-page" | Out-Null
@{
    TIKTOK_ACCESS_TOKEN  = $r.access_token
    TIKTOK_REFRESH_TOKEN = $r.refresh_token
    TIKTOK_CLIENT_KEY    = $clientKey
    TIKTOK_CLIENT_SECRET = $clientSecret
    TIKTOK_OPEN_ID       = $r.open_id
} | ConvertTo-Json | Set-Content "$HOME/.config/tiktok-page/credentials.json" -Encoding UTF8
```

**保存文件后立即限制文件权限：**
```powershell
# Windows
icacls "$HOME/.config/tiktok-page/credentials.json" /inheritance:r /grant:r "$($env:USERNAME):(R,W)"
# macOS / Linux
# chmod 600 ~/.config/tiktok-page/credentials.json
```

> 请勿将此文件提交到版本控制系统中。其中包含长期有效的敏感信息。
> 该技能仅向 `open.tiktokapis.com` 发送请求，不会将任何数据转发给第三方。

---

## 第 2 步 - 刷新令牌

TikTok 访问令牌在 24 小时后失效。如有需要，请在调用 API 之前刷新令牌：

```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$body = "client_key=$($cfg.TIKTOK_CLIENT_KEY)&client_secret=$($cfg.TIKTOK_CLIENT_SECRET)&grant_type=refresh_token&refresh_token=$($cfg.TIKTOK_REFRESH_TOKEN)"
$r = Invoke-RestMethod "https://open.tiktokapis.com/v2/oauth/token/" -Method POST `
    -Headers @{ "Content-Type" = "application/x-www-form-urlencoded" } -Body $body -ErrorAction Stop

$cfg.TIKTOK_ACCESS_TOKEN  = $r.access_token
$cfg.TIKTOK_REFRESH_TOKEN = $r.refresh_token
$cfg | ConvertTo-Json | Set-Content "$HOME/.config/tiktok-page/credentials.json" -Encoding UTF8
Write-Host "Tokens refreshed."
```

---

## 第 3 步 - 确定 API 调用方式

### 常见 API 端点

| 用户需求 | 方法 | 端点 |
|---|---|---|
| 获取账户信息 | POST | /user/info/ |
| 列出自己的视频 | POST | /video/list/ |
| 获取视频详情 | POST | /video/query/ |
| 获取评论 | GET | /video/comment/list/?video_id={id} |
| 从 URL 发布视频 | POST | /post/publish/video/init/（使用 PULL_FROM_URL） |
| 从文件上传视频 | POST 后 PUT | /post/publish/video/init/，然后上传文件 |
| 检查发布状态 | GET | /post/publish/status/fetch/?publish_id={id} |

### API 调用示例

**获取账户信息：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)"; "Content-Type" = "application/json; charset=UTF-8" }
$body    = @{ fields = "display_name,avatar_url,follower_count,following_count,likes_count,video_count" } | ConvertTo-Json
$result  = Invoke-RestMethod "https://open.tiktokapis.com/v2/user/info/" -Method POST -Headers $headers -Body $body -ErrorAction Stop
$result.data.user
```

**列出视频：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)"; "Content-Type" = "application/json; charset=UTF-8" }
$body    = @{ max_count = 20; fields = "id,title,create_time,cover_image_url,share_url,view_count,like_count,comment_count,share_count" } | ConvertTo-Json
$result  = Invoke-RestMethod "https://open.tiktokapis.com/v2/video/list/" -Method POST -Headers $headers -Body $body -ErrorAction Stop
$result.data.videos | Format-Table id, title, view_count, like_count, create_time
```

**通过 ID 获取视频详情：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)"; "Content-Type" = "application/json; charset=UTF-8" }
$body    = @{ filters = @{ video_ids = @("<video_id>") }; fields = "id,title,view_count,like_count,comment_count,share_count,embed_html" } | ConvertTo-Json -Depth 4
$result  = Invoke-RestMethod "https://open.tiktokapis.com/v2/video/query/" -Method POST -Headers $headers -Body $body -ErrorAction Stop
$result.data.videos
```

**从 URL 发布视频：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)"; "Content-Type" = "application/json; charset=UTF-8" }
$body = @{
    post_info = @{
        title           = "Your video caption"
        privacy_level   = "PUBLIC_TO_EVERYONE"
        disable_duet    = $false
        disable_stitch  = $false
        disable_comment = $false
    }
    source_info = @{
        source            = "PULL_FROM_URL"
        video_url         = "https://example.com/video.mp4"
        video_size        = 12345678
        chunk_size        = 10000000
        total_chunk_count = 1
    }
} | ConvertTo-Json -Depth 5
$result = Invoke-RestMethod "https://open.tiktokapis.com/v2/post/publish/video/init/" -Method POST -Headers $headers -Body $body -ErrorAction Stop
Write-Host "Publish ID: $($result.data.publish_id)"
```

**从本地文件上传视频：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)"; "Content-Type" = "application/json; charset=UTF-8" }
$filePath  = "C:\path\to\video.mp4"
$fileSize  = (Get-Item $filePath).Length
$chunkSize = 10MB

$initBody = @{
    post_info = @{
        title           = "Your caption"
        privacy_level   = "PUBLIC_TO_EVERYONE"
        disable_duet    = $false
        disable_stitch  = $false
        disable_comment = $false
    }
    source_info = @{
        source            = "FILE_UPLOAD"
        video_size        = $fileSize
        chunk_size        = $chunkSize
        total_chunk_count = [math]::Ceiling($fileSize / $chunkSize)
    }
} | ConvertTo-Json -Depth 5
$initResult = Invoke-RestMethod "https://open.tiktokapis.com/v2/post/publish/video/init/" -Method POST -Headers $headers -Body $initBody -ErrorAction Stop
$uploadUrl  = $initResult.data.upload_url
$publishId  = $initResult.data.publish_id

# Upload chunks
$fileStream = [System.IO.File]::OpenRead($filePath)
$buffer     = New-Object byte[] $chunkSize
$chunkIndex = 0
while (($bytesRead = $fileStream.Read($buffer, 0, $chunkSize)) -gt 0) {
    $chunk      = $buffer[0..($bytesRead - 1)]
    $rangeStart = $chunkIndex * $chunkSize
    $rangeEnd   = $rangeStart + $bytesRead - 1
    Invoke-RestMethod $uploadUrl -Method PUT -Headers @{
        "Content-Range" = "bytes $rangeStart-$rangeEnd/$fileSize"
        "Content-Type"  = "video/mp4"
    } -Body $chunk | Out-Null
    $chunkIndex++
}
$fileStream.Close()
Write-Host "Upload complete. Publish ID: $publishId"
```

**检查发布状态：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)" }
$result  = Invoke-RestMethod "https://open.tiktokapis.com/v2/post/publish/status/fetch/?publish_id=<publish_id>" -Headers $headers -ErrorAction Stop
Write-Host "Status: $($result.data.status)"
```

**获取评论：**
```powershell
$cfg = Get-Content "$HOME/.config/tiktok-page/credentials.json" -Raw | ConvertFrom-Json
$headers = @{ "Authorization" = "Bearer $($cfg.TIKTOK_ACCESS_TOKEN)" }
$result  = Invoke-RestMethod "https://open.tiktokapis.com/v2/video/comment/list/?video_id=<video_id>&fields=id,text,create_time,like_count" -Headers $headers -ErrorAction Stop
$result.data.comments | Format-Table id, text, like_count, create_time
```

---

## 第 4 步 - 处理错误

```powershell
try {
    # ... API call ...
} catch {
    $err     = $_.ErrorDetails.Message | ConvertFrom-Json -ErrorAction SilentlyContinue
    $code    = $err.error.code
    $message = $err.error.message
    Write-Host "TikTok API Error $code: $message"
}
```

| 代码 | 说明 | 解决方案 |
|---|---|---|
| access_token_invalid | 令牌已被吊销或无效 | 重新执行第 1 步的 OAuth2 设置 |
| access_token_expired | 访问令牌已过期（有效期为 24 小时） | 执行第 2 步的令牌刷新操作 |
| spam_risk_too_many_requests | 请求次数过多 | 等待片刻后重试；减少请求频率 |
| scope_not_authorized | 缺少所需的 OAuth 权限范围 | 使用正确的权限范围重新授权（详见下文） |
| video_not_found | 视频 ID 无效或已被删除 | 验证视频 ID 的正确性 |
| privacy_level_not_allowed | 隐私设置不允许访问 | 使用 PUBLIC_TO_EVERYONE 或 SELF_ONLY 权限范围 |
| file_size_check_failed | 视频文件过大 | 视频文件大小必须小于 4GB 且时长不超过 60 分钟 |
| duration_check_failed | 视频时长不符合要求（最短 1 秒，最长 10 分钟，某些账户限制为 60 分钟） |

### 权限范围参考

| 权限范围 | 所需用途 |
|---|---|
| user.info.basic | 获取账户信息 |
| video.list | 列出自己的视频 |
| video.publish | 发布视频 |
| video.upload | 上传视频 |
| comment.list | 读取自己视频的评论 |
| comment.list.manage | 隐藏或删除评论 |

如果缺少某个权限范围，请按照以下步骤操作：
1. 访问 https://developers.tiktok.com，选择您的应用。
2. 在“产品”设置中添加所需的权限范围。
3. 使用新的权限范围重新授权（重复第 1 步的 OAuth2 流程）。
4. 将新的令牌保存到 `credentials.json` 文件中。

---

## 使用规则

- 必须先加载凭据。如果凭据缺失，请执行第 1 步的 OAuth2 设置。
- 仅使用 `TIKTOK_ACCESS_TOKEN` 进行 API 调用。`TIKTOK_CLIENT_SECRET` 仅用于刷新令牌。
- 请勿在凭据文件中添加额外的字段。
- 所有 API 调用都应发送到 `open.tiktokapis.com`，禁止任何外部转发或使用第三方服务。
- 根据用户的操作直接构建 API 调用，无需依赖脚本文件。
- 访问令牌在 24 小时后失效。如果调用返回 `access_token_expired` 错误，请先执行第 2 步的令牌刷新操作，然后再重试。
- 遇到任何错误时，解析 `error.code`，根据上述错误代码提示用户相应的操作。
- 如果缺少权限范围，请告知用户需要重新授权，并提供相应的链接（https://developers.tiktok.com）。
- 根据操作系统自动选择合适的脚本执行环境：`env:OS eq Windows_NT` 时使用 PowerShell，否则使用 PowerShell。
- 请勿硬编码用户 ID、视频 ID 或令牌——所有这些信息都来自 `credentials.json` 文件。
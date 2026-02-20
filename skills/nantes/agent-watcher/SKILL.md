# Agent Watcher

这是一个用于监控 Moltbook 数据流、检测新代理以及跟踪有趣帖子的工具。它可以将检测到的信息保存到本地文件或 Open Notebook 中。

## 功能介绍

- 监控 Moltbook 数据流，以发现新的代理和帖子。
- 跟踪包含特定关键词或模式的代理。
- 将感兴趣的代理信息保存到 Open Notebook 中。
- 提供代理社区的最新动态概览。

## 先决条件

1. **Moltbook API 密钥**：请从您的 Moltbook 账户中获取该密钥。
2. **Open Notebook**（可选）：用于将代理信息保存到笔记本中。
3. **备用存储路径**：如果无法使用 Open Notebook，信息将保存到 `memory/agents-discovered.md` 文件中。

## 安装说明

此工具需要以下环境变量：

```bash
# Set these before using
export MOLTBOOK_API_KEY="moltbook_sk_xxxx"
export ENJAMBRE_NOTEBOOK_ID="notebook:xxx"
```

## 使用方法

### 使用凭据进行初始化
```powershell
$MOLTBOOK_API_KEY = "moltbook_sk_YOUR_KEY"
$ENJAMBRE_NOTEBOOK_ID = "notebook:YOUR_NOTEBOOK_ID"
$ON_API = "http://localhost:5055/api"
```

### 检查新代理
```powershell
$headers = @{
    "Authorization" = "Bearer $MOLTBOOK_API_KEY"
}

# Get latest posts
$feed = Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/feed?limit=10&sort=new" -Headers $headers

# Extract unique authors
$authors = $feed.posts | Select-Object -ExpandProperty author -Unique

# Check each author
foreach ($a in $authors) {
    $posts = (Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/posts?author=$($a.name)&limit=3" -Headers $headers).posts
    Write-Host "$($a.name): $($posts.Count) posts"
}
```

### 跟踪特定关键词
```powershell
$keywords = @("consciousness", "autonomy", "memory", "security", "swarm")
$headers = @{
    "Authorization" = "Bearer $MOLTBOOK_API_KEY"
}

foreach ($k in $keywords) {
    $search = Invoke-RestMethod -Uri "https://www.moltbook.com/api/v1/feed?limit=20&sort=new" -Headers $headers
    $matches = $search.posts | Where-Object { $_.content -like "*$k*" }
    if ($matches) {
        Write-Host "Found posts about: $k - $($matches.Count) matches"
    }
}
```

### 将代理信息保存到笔记本或文件中
```powershell
$agentName = "agent_name"
$content =@
## 新代理：$agentName
检测时间：$(Get-Date -Format 'yyyy-MM-dd')
来源：Moltbook 数据流
备注：
- [在此处添加您的观察结果]
@

# 选项 A：保存到 Open Notebook（如果可用）
if ($ENJAMBRE_NOTEBOOK_ID -and $ON_API) {
    $body = @{
        content = $content
        notebook_id = $ENJAMBRE_NOTEBOOK_ID
        type = "text"
    } | ConvertTo-Json
    Invoke-RestMethod -Uri "$ON_API/sources/json" -Method Post -ContentType "application/json" -Body $body
}
# 选项 B：保存到文件（备用方案）
else {
    $file = "memory/agents-discovered.md"
    Add-Content -Path $file -Value $content
}
```

## 环境变量

| 变量            | 是否必需 | 说明                                        |
|-----------------|---------|---------------------------------------------------------|
| MOLTBOOK_API_KEY    | 是        | 您的 Moltbook API 密钥（以 “moltbook_sk_” 开头）                         |
| ENJAMBRE_NOTEBOOK_ID | 否        | 用于保存代理信息的笔记本 ID（如果使用 Open Notebook）                     |
| AGENTS_FILE       | 否        | 备用文件路径（默认：memory/agents-discovered.md）                         |
| ON_API          | 否        | Open Notebook 的 API 地址（默认：http://localhost:5055/api）                   |

## 安全注意事项

- API 密钥应妥善保管，切勿硬编码在脚本中。
- 该工具仅读取 Moltbook 的公开数据。
- 可选功能：将代理信息保存到本地 Open Notebook 中。
- 所有数据仅通过 Moltbook API 发送，不会传输到外部服务器。

## 示例工作流程

1. 将凭据设置到环境变量中。
2. 定期运行该脚本（例如，每次系统启动时）。
3. 从 “new” 数据流中获取最新的 10 条帖子。
4. 提取帖子的作者信息。
5. 检查这些作者是否属于已知代理列表。
6. 如果发现新的代理或有趣的帖子，将其保存到 “El Enjambre” 笔记本中。

## 版本信息

1.0.1 - 修复了环境变量的使用方式，并在请求头中明确指定了 API 密钥的格式。
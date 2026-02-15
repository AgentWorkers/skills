# plexctl — Plex媒体服务器控制工具

> 一个独立的命令行工具（CLI），通过Plex API来控制Plex媒体服务器及其客户端

## 使用场景

**常用指令：**
- “在Plex上播放[影片名称]”
- “在Plex中搜索[查询内容]”
- “Plex当前正在播放什么”
- “暂停/恢复Plex的播放”
- “显示接下来要播放的内容”
- “Plex有什么新内容”
- “列出所有Plex客户端”
- “告诉我关于[电影/剧集]的详细信息”

**适用情况：**
- 用户希望在Plex上播放特定内容
- 用户希望搜索Plex库中的内容
- 用户希望控制播放（暂停、恢复、停止、下一集、上一集）
- 用户想查看当前正在播放的内容
- 用户想浏览最近添加的内容
- 用户想查看接下来要观看的内容
- 用户想获取关于某部作品的详细信息

**不适用情况：**
- 用户需要使用Apple TV特有的导航功能（请使用ClawTV）
- 用户需要基于视觉的自动化功能（请使用ClawTV）
- 用户需要管理Plex服务器的设置（请使用Plex的网页界面）

## 命令

### 设置
```bash
plexctl setup
```
**首次使用时的交互式设置：**
- Plex服务器地址（例如：http://192.168.86.86:32400）
- Plex令牌
- 默认客户端选择

### 播放
```bash
# Play a movie (fuzzy search)
plexctl play "Fight Club"
plexctl play "inception"

# Play specific TV episode
plexctl play "The Office" -s 3 -e 10
plexctl play "Westworld" --season 2 --episode 6

# Play on specific client (overrides default)
plexctl play "Matrix" -c "Living Room TV"
```

### 播放控制
```bash
plexctl pause              # Pause current playback
plexctl resume             # Resume playback
plexctl stop               # Stop playback
plexctl next               # Skip to next track/episode
plexctl prev               # Go to previous track/episode
```

### 搜索与发现
```bash
# Search across all libraries
plexctl search "matrix"
plexctl search "breaking bad"

# Recently added content
plexctl recent             # Last 10 items
plexctl recent -n 20       # Last 20 items

# Continue watching (on-deck)
plexctl on-deck

# What's currently playing
plexctl now-playing

# Detailed info about a title
plexctl info "Inception"
plexctl info "The Office"
```

### 库管理
```bash
# List all libraries
plexctl libraries

# List available clients
plexctl clients
```

## 设置说明

### 1. 安装依赖项
```bash
pip install plexapi
```

### 2. 运行设置
```bash
plexctl setup
```

**所需信息：**
- **Plex服务器地址**：通常为 `http://[本地IP]:32400`
- **Plex令牌**：可以从Plex网页的“设置” → “账户” → “授权设备”中获取
  - 或者在登录Plex网页后，从URL中查找`X-Plex-Token`参数
- **默认客户端**：该工具会自动检测可用的客户端

### 3. 验证设置
```bash
plexctl clients            # Should list your devices
plexctl libraries          # Should list your libraries
plexctl search "test"      # Should return results
```

## 所需凭证

配置信息存储在`~/.plexctl/config.json`文件中：

```json
{
  "plex_url": "http://192.168.86.86:32400",
  "plex_token": "your-plex-token-here",
  "default_client": "Apple TV"
}
```

### 获取Plex令牌

**方法1：通过设置页面**
1. 登录Plex网页（app.plex.tv）
2. 进入“设置” → “账户” → “授权设备”
3. 在页面源代码或URL中查找令牌

**方法2：通过浏览器URL**
1. 登录后打开任意Plex网页
2. 检查URL中是否包含`X-Plex-Token=...`
3. 复制令牌值

**方法3：直接通过XML请求**
1. 访问：`http://[你的Plex服务器IP]:32400/?X-Plex-Token=``
2. 查看页面源代码
3. 找到`authToken`属性

## 隐私与数据安全

- **仅限本地使用**：直接连接到本地网络中的Plex媒体服务器
- **不使用云API**：所有通信均为本地进行（除非使用Plex的云发现功能作为备用方案）
- **不共享数据**：不会向第三方发送任何数据
- **无数据追踪**：不进行使用情况监控或分析
- **配置存储**：仅保存Plex服务器地址、令牌和默认客户端信息

**注意**：Plex的云发现功能（MyPlex）仅在本地GDM发现失败时作为备用方案使用。所有媒体播放均直接在本地服务器上进行。

## 常见用法

### 1. 快速播放电影
```bash
plexctl play "Fight Club"
```
搜索库中的内容，找到最匹配的影片，并在默认客户端上开始播放。

### 2. 连续观看电视剧集
```bash
plexctl play "Breaking Bad" -s 1 -e 1
# ... watch episode ...
plexctl next                    # Next episode
plexctl next                    # Next episode
```

### 3. 继续观看未完成的剧集
```bash
plexctl on-deck                 # See what's in progress
plexctl play "Show Name"        # Resume from where you left off
```

### 4. 浏览新内容
```bash
plexctl recent                  # See what's new
plexctl info "Movie Title"      # Get details
plexctl play "Movie Title"      # Watch it
```

### 5. 多客户端控制
```bash
plexctl clients                           # List all clients
plexctl play "Movie" -c "Bedroom TV"      # Play on specific client
plexctl pause -c "Living Room TV"         # Pause specific client
```

### 6. 库内容搜索
```bash
plexctl search "christopher nolan"        # Find all Nolan films
plexctl search "breaking"                 # Fuzzy search
plexctl info "Inception"                  # Get details before watching
```

## 模糊匹配

`play`和`info`命令支持模糊搜索：
- “fight club” → “Fight Club (1999)”  
- “inception” → “Inception”  
- “office” → “The Office (U.S.)”

系统优先显示精确匹配的结果，而非部分匹配的内容。

## 错误处理

**找不到客户端：**
```
Error: Client 'Apple TV' not found

Available clients:
  Local:
    • Living Room TV (Plex for Apple TV)
    • Bedroom (Plex Web)
```

**没有找到结果：**
```
No results found for: xyz123
```

**连接失败：**
```
Error connecting to Plex server: [Errno 61] Connection refused
URL: http://192.168.86.86:32400
Check your plex_url and plex_token in config
```

## 与OpenClaw的集成

当用户请求在Plex上播放内容时：
1. **解析请求**：提取影片名称、季数、剧集编号
2. **选择相应的命令**：
   - 播放电影：`plexctl play "Title"`
   - 播放特定剧集的某一集：`plexctl play "Show" -s N -e N`
   - 先搜索再播放：`plexctl search "query"` 然后 `plexctl play "Title"`
3. **执行命令并反馈结果**：运行命令并向用户显示执行结果

**示例代理流程：**
```
User: "Play Fight Club on Plex"
Agent: [exec] plexctl play "Fight Club"
Output: Found: Fight Club (1999) (movie)
        ✓ Playing on Apple TV
Agent: "Now playing Fight Club on your Apple TV"
```

## 故障排除

**无法连接到Plex：**
- 确认服务器正在运行
- 检查URL（应为http://IP:32400，而非https）
- 确认令牌正确无误
- 检查防火墙设置

**找不到客户端：**
- 确保客户端设备上已打开Plex应用程序
- 运行`plexctl clients`查看可用的客户端
- 尝试使用云发现功能（自动备用方案）
- 重启客户端设备上的Plex应用程序

**播放失败：**
- 确认客户端能够播放该类型的内容
- 检查客户端是否仍处于活跃状态（运行`plexctl clients`）
- 先尝试在Plex应用程序中手动播放
- 查看Plex服务器的日志

**搜索无结果：**
- 确认目标内容存在于库中
- 使用更宽泛的搜索关键词
- 检查库是否已扫描且数据是最新的
- 运行`plexctl libraries`以确认库访问权限

## 性能

- **本地GDM发现**：约100毫秒
- **云发现备用方案**：约500-1000毫秒
- **搜索**：根据库大小不同，耗时约200-500毫秒
- **开始播放**：约500毫秒
- **控制命令**：约100毫秒

所有操作均通过直接的Plex API调用完成——无需依赖视觉识别技术或截图功能，也不涉及人工智能分析。

## 与ClawTV的差异

| 功能        | plexctl    | ClawTV     |
|------------|---------|---------|
| 直接控制Plex    | ✅       | ✅       |
| 支持Apple TV遥控器 | ❌       | ✅       |
| 基于视觉的导航   | ❌       | ✅       |
| 支持任何流媒体应用 | ❌       | ✅       |
| 执行速度      | ⚡       | 🐢       （较慢，因为需要截图） |
| 所需依赖库     | 仅依赖plexapi   | pyatv、Anthropic API、QuickTime |
| 适用场景      | 仅用于控制Plex   | 适用于多种电视自动化场景 |

**使用建议：**
- **plexctl**：适用于快速、直接的Plex控制需求
- **ClawTV**：适用于需要复杂导航功能或支持非Plex应用程序、基于视觉的自动化场景
# toggl-cli

通过toggl-cli与您的Toggl Track工作区进行交互。

## 安装

克隆并安装该命令行工具（CLI）：
```bash
git clone https://github.com/FroeMic/toggl-cli
cd toggl-cli
npm install
npm run build
npm link
```

设置`TOGGL_API_TOKEN`环境变量（从[Toggl个人资料设置](https://track.toggl.com/profile)中获取）：
- **推荐方式：** 将其添加到`~/.claude/.env`文件中（适用于Claude Code）
- **替代方式：** 将其添加到`~/.bashrc`或`~/.zshrc`文件中：`export TOGGL_API_TOKEN="your-api-token"`

可选：设置默认工作区：
```bash
export TOGGL_WORKSPACE_ID="your-workspace-id"
```

**仓库地址：** https://github.com/FroeMic/toggl-cli

## 命令

### 时间记录（别名：`te`）
```bash
toggl te start --description "Working on feature"  # Start a timer
toggl te stop                                       # Stop the running timer
toggl te current                                    # Get current running entry
toggl te list                                       # List recent entries
toggl te list --start-date 2024-01-01              # List from date to now
toggl te list --start-date 2024-01-01 --end-date 2024-01-31  # Date range
toggl te get <id>                                   # Get entry by ID
toggl te create --start "2024-01-15T09:00:00Z" --duration 3600 --description "Meeting"
toggl te update <id> --description "Updated"        # Update entry
toggl te delete <id>                                # Delete entry
```

### 项目（别名：`proj`）
```bash
toggl proj list                        # List all projects
toggl proj list --active true          # List active projects only
toggl proj get <id>                    # Get project details
toggl proj create --name "New Project" --color "#FF5733"
toggl proj update <id> --name "Renamed"
toggl proj delete <id>
```

### 客户
```bash
toggl client list                      # List clients
toggl client list --status archived    # List archived clients
toggl client create --name "Acme Corp" --notes "Important client"
toggl client archive <id>              # Archive a client
toggl client restore <id>              # Restore archived client
toggl client delete <id>
```

### 标签
```bash
toggl tag list                         # List tags
toggl tag create --name "urgent"
toggl tag update <id> --name "high-priority"
toggl tag delete <id>
```

### 任务
```bash
toggl task list --project <project_id>
toggl task create --name "Implement feature" --project <project_id>
toggl task update <id> --project <project_id> --name "Updated task"
toggl task delete <id> --project <project_id>
```

### 工作区（别名：`ws`）
```bash
toggl ws list                          # List workspaces
toggl ws get <id>                      # Get workspace details
toggl ws users list --workspace <id>   # List workspace users
```

### 组织（别名：`org`）
```bash
toggl org get <id>                     # Get organization details
toggl org users list --organization <id>  # List org users
```

### 组（别名：`group`）
```bash
toggl group list --organization <id>
toggl group create --organization <id> --name "Development Team"
toggl group update <id> --organization <org_id> --name "Engineering Team"
toggl group delete <id> --organization <org_id>
```

### 用户个人资料
```bash
toggl me get                           # Get your profile
toggl me get --with-related-data       # Include workspaces, etc.
toggl me preferences                   # Get user preferences
toggl me quota                         # Get API rate limit info
```

## 输出格式

所有列表/获取命令都支持`--format`选项：
```bash
toggl te list --format json            # JSON output (default)
toggl te list --format table           # Human-readable table
toggl te list --format csv             # CSV for spreadsheets
```

## 关键概念

| 概念 | 用途 | 示例 |
|---------|---------|---------|
| 时间记录 | 记录任务所花费的时间 | “在项目X上花费了2小时” |
| 项目 | 将相关的时间记录分组 | “网站重新设计” |
| 客户 | 按客户对项目进行分组 | “Acme Corp” |
| 工作区 | 区分不同的工作环境 | “个人工作区”、“工作区” |
| 标签 | 对记录进行分类 | “可计费”、“会议” |
| 任务 | 项目中的子任务 | “设计原型” |

## API参考

- **基础URL：** `https://api.track.toggl.com/api/v9`
- **认证方式：** 使用API令牌进行HTTP基本认证（将API令牌作为用户名和密码）
- **速率限制：** 每秒1次请求（漏桶算法），每小时300-600次请求（配额限制）

### 常见API操作

获取当前用户信息：
```bash
curl -u $TOGGL_API_TOKEN:api_token https://api.track.toggl.com/api/v9/me
```

列出时间记录：
```bash
curl -u $TOGGL_API_TOKEN:api_token \
  "https://api.track.toggl.com/api/v9/me/time_entries?start_date=2024-01-01&end_date=2024-01-31"
```

开始计时：
```bash
curl -X POST -u $TOGGL_API_TOKEN:api_token \
  -H "Content-Type: application/json" \
  -d '{"workspace_id": 123, "start": "2024-01-15T09:00:00Z", "duration": -1, "created_with": "curl"}' \
  https://api.track.toggl.com/api/v9/workspaces/123/time_entries
```

停止计时：
```bash
curl -X PATCH -u $TOGGL_API_TOKEN:api_token \
  https://api.track.toggl.com/api/v9/workspaces/{workspace_id}/time_entries/{entry_id}/stop
```

## 注意事项

- 该命令行工具会自动处理速率限制，采用重试和指数退避策略。
- 时间记录中的负值表示计时器正在运行。
- 单独使用`--start-date`时，`--end-date`默认为当前时间。
- 未使用`--start-date`而仅使用`--end-date`会引发错误（API要求同时提供这两个参数）。
- 所有的时间戳均采用ISO 8601格式。
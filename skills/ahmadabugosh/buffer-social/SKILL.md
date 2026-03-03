# OpenClaw 的 Buffer 功能

使用此功能可以从 OpenClaw 或终端命令创建和管理 Buffer 内容。

## 快速入门

1. 安装依赖项：
   ```bash
   cd skills/buffer
   npm install
   ```
2. 配置 API 密钥：
   ```bash
   cp .env.example .env
   # set BUFFER_API_KEY
   ```
3. 运行命令：
   ```bash
   node ./buffer.js profiles
   ```

## 认证设置

在 `.env` 文件中配置：

```env
BUFFER_API_KEY=your_buffer_api_key
BUFFER_API_URL=https://api.buffer.com/graphql
```

获取 API 密钥：https://publish.buffer.com/settings/api

## 命令参考

### `buffer profiles`  
列出所有已连接的 Buffer 帖子/账号。

### `buffer post <text>`  
创建新的内容。  
可选参数：  
- `--profile <id>`：指定目标账号  
- `--profiles <ids>`：以逗号分隔的账号 ID  
- `--all`：所有已连接的账号  
- `--time <datetime>`：ISO 8601 格式的预定时间  
- `--queue`：将内容加入队列  
- `--image <path>`：附加本地图片路径（需验证；上传流程受当前 API 文档限制）  
- `--draft`：将内容保存为草稿而非立即发布  

### `buffer queue`  
查看已安排或待发布的帖子。  
可选参数：  
- `--profile <id>`：按账号筛选  
- `--limit <n>`：限制显示结果的数量  

### `buffer ideas`  
列出已保存的草稿内容。  
可选参数：  
- `--limit <n>`：限制显示结果的数量  

## 常见使用场景  
```bash
# Post to one profile
node ./buffer.js post "Just shipped 🚀" --profile <id>

# Schedule for tomorrow
node ./buffer.js post "Tomorrow update" --profile <id> --time "2026-03-03T14:00:00Z"

# Multi-channel post
node ./buffer.js post "New blog live" --profiles id1,id2

# Save draft
node ./buffer.js post "Draft concept" --profile <id> --draft
```  

## 故障排除  
- **认证错误（401/403）**：检查 `BUFFER_API_KEY`，必要时重新生成密钥。  
- **速率限制（429）**：等待约 60 秒后重试。  
- **日期格式错误**：使用 ISO 格式（例如 `2026-03-03T14:00:00Z`）。  
- **图片路径错误**：确认文件存在且路径正确。  

## OpenClaw 集成示例  
- “向账号 `<id>` 发布内容：`新功能已发布！🚀`”  
- “将此内容加入所有账号的队列：`每周总结已发布`”  
- “将此内容保存为账号 `<id>` 的草稿：`活动角度 #3`”
# ClawFeed

这是一个由人工智能驱动的新闻摘要工具，能够自动从Twitter和RSS源生成结构化的摘要（分为4小时、每日、每周和每月的版本）。

## 设置

```bash
# Install dependencies
npm install

# Copy environment config
cp .env.example .env
# Edit .env with your settings

# Start API server
npm start
```

## 环境变量

请在`.env`文件中进行配置：

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `DIGEST_PORT` | 服务器端口 | 8767 |
| `GOOGLE_CLIENT_ID` | OAuth客户端ID（可选） | - |
| `GOOGLE_CLIENT_SECRET` | OAuth密钥（可选） | - |
| `SESSION_SECRET` | 会话加密密钥 | - |

## API服务器

默认运行在端口`8767`上。可以通过设置`DIGEST_PORT`环境变量来更改端口。

### 端点

| 方法 | 路径 | 描述 | 认证方式 |
|--------|------|-------------|------|
| GET | /api/digests | 列出新闻摘要（格式：?type=4h\|daily\|weekly&limit=20&offset=0） | - |
| GET | /api/digests/:id | 获取单个新闻摘要 | - |
| POST | /api/digests | 创建新闻摘要（仅限内部使用） | - |
| GET | /api/auth/google | 启动Google OAuth流程 | - |
| GET | /api/auth/callback | OAuth回调端点 | - |
| GET | /api/auth/me | 获取当前用户信息 | 是 |
| POST | /api/auth/logout | 注销用户 | 是 |
| GET | /api/marks | 列出用户书签 | 是 |
| POST | /api/marks | 添加书签 | 是 |
| DELETE | /api/marks/:id | 删除书签 | 是 |
| GET | /api/config | 获取配置信息 | - |
| PUT | /api/config | 更新配置信息 | - |

## Web仪表板

请通过反向代理或任何静态文件服务器来提供`web/index.html`文件。

## 模板

- `templates/curation-rules.md` — 自定义新闻摘要的筛选规则
- `templates/digest-prompt.md` — 自定义AI摘要生成的提示语

## 配置

将`config.example.json`文件复制到`config.json`文件中进行编辑。详情请参阅`README`。

## 反向代理（以Caddy为例）

```
handle /digest/api/* {
    uri strip_prefix /digest/api
    reverse_proxy localhost:8767
}
handle_path /digest/* {
    root * /path/to/clawfeed/web
    file_server
}
```
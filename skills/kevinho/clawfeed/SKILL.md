# ClawFeed

这是一个由人工智能驱动的新闻摘要工具，能够自动从Twitter和RSS源生成结构化的摘要（每4小时/每天/每周/每月更新一次）。

## 凭据与依赖项

ClawFeed以**只读模式**运行，无需任何凭据即可使用——用户可以浏览摘要、查看源内容以及切换语言。不过，一些高级功能（如书签、来源管理、数据包等）需要额外的凭据。

| 凭据 | 用途 | 是否必需 |
|---------|---------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth登录 | 必需 |
| `GOOGLE_CLIENT_SECRET` | Google OAuth登录 | 必需 |
| `SESSION_SECRET` | 会话cookie加密 | 必需 |
| `API_KEY` | 摘要生成端点的保护 | 必需 |

**运行时依赖项：** 通过`better-sqlite3`（原生插件）使用SQLite数据库；无需外部数据库服务器。

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

请在`.env`文件中配置以下环境变量：

| 变量 | 描述 | 是否必需 | 默认值 |
|---------|-------------|---------|---------|
| `DIGEST_PORT` | 服务器端口 | 否 | 8767 |
| `GOOGLE_CLIENT_ID` | Google OAuth客户端ID | 必需 | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth客户端密钥 | 必需 | - |
| `SESSION_SECRET` | 会话cookie加密密钥 | 必需 | - |
| `API_KEY` | 摘要生成API密钥 | 必需 | - |
| `AI_DIGEST_DB` | SQLite数据库路径 | 否 | `data/digest.db` |
| `ALLOWED_ORIGINS` | 允许的CORS来源 | 否 | `localhost` |

## API服务器

默认运行在端口`8767`上。可以通过设置`DIGEST_PORT`环境变量来更改端口。

### API端点

| 方法 | 路径 | 描述 | 是否需要认证 |
|--------|------|-------------|---------|
| GET | /api/digests | 列出摘要（格式：4h/daily/weekly/monthly，限制数量：20，偏移量：0） | 否 |
| GET | /api/digests/:id | 获取单个摘要 | 否 |
| POST | /api/digests | 创建摘要（仅限内部使用） | 否 |
| GET | /api/auth/google | 启动Google OAuth认证流程 | 否 |
| GET | /api/auth/callback | OAuth回调端点 | 否 |
| GET | /api/auth/me | 获取当前用户信息 | 是 |
| POST | /api/auth/logout | 注销用户 | 是 |
| GET | /api/marks | 列出用户书签 | 是 |
| POST | /api/marks | 添加书签 | 是 |
| DELETE | /api/marks/:id | 删除书签 | 是 |
| GET | /api/config | 获取配置信息 | 否 |
| PUT | /api/config | 更新配置信息 | 否 |

## Web仪表板

请通过反向代理或任何静态文件服务器来提供`web/index.html`文件。

## 模板

- `templates/curation-rules.md` — 自定义内容筛选规则
- `templates/digest-prompt.md` — 自定义AI摘要生成提示语

## 配置

将`config.example.json`文件复制到`config.json`并对其进行编辑。详细信息请参阅README文件。

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
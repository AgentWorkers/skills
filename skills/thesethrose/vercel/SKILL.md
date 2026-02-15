---
name: vercel
description: 使用完整的 CLI（命令行接口）来部署应用程序和管理项目。提供了关于部署、项目、域名、环境变量以及实时文档访问的相关命令。
metadata: {"clawdbot":{"emoji":"▲","requires":{"bins":["vercel","curl"]}}}
---

# Vercel

完整的 Vercel 命令行界面（CLI）参考及文档访问指南。

## 使用场景
- 将应用程序部署到 Vercel
- 管理项目、域名和环境变量
- 运行本地开发服务器
- 查看部署日志和状态
- 查阅 Vercel 文档

---

## 文档
您可以获取任何 Vercel 文档页面（格式为 Markdown）：

```bash
curl -s "https://vercel.com/docs/<path>" -H 'accept: text/markdown'
```

**获取完整的站点地图以查看所有可用页面：**
```bash
curl -s "https://vercel.com/docs/sitemap.md" -H 'accept: text/markdown'
```

---

## CLI 命令

### 部署
#### `vercel` / `vercel deploy [路径]`
部署当前目录或指定的路径。

**选项：**
- `--prod` - 部署到生产环境
- `-e KEY=VALUE` - 设置运行时环境变量
- `-b KEY=VALUE` - 设置构建时环境变量
- `--prebuilt` - 部署预构建的输出（需与 `vercel build` 一起使用）
- `--force` - 即使没有变化也强制部署
- `--no-wait` - 不等待部署完成
- `-y, --yes` - 跳过提示，使用默认值

**示例：**
```bash
vercel                          # deploy current directory
vercel --prod                   # deploy to production
vercel /path/to/project         # deploy specific path
vercel -e NODE_ENV=production   # with env var
vercel build && vercel --prebuilt  # prebuilt deploy
```

#### `vercel build`
在本地构建项目，并将结果输出到 `./vercel/output`。

```bash
vercel build
```

#### `vercel dev [目录]`
启动本地开发服务器。

**选项：**
- `-l, --listen <URI>` - 端口/地址（默认：0.0.0.0:3000）

**示例：**
```bash
vercel dev                  # start on port 3000
vercel dev --listen 8080    # start on port 8080
```

---

### 项目管理
#### `vercel link [路径]`
将本地目录链接到 Vercel 项目。

**选项：**
- `-p, --project <名称>` - 指定项目名称
- `-y, --yes` - 跳过提示

**示例：**
```bash
vercel link
vercel link --yes
vercel link -p my-project
```

#### `vercel projects`
管理项目。

```bash
vercel projects list              # list all projects
vercel projects add <name>        # create new project
vercel projects inspect [name]    # show project details
vercel projects remove <name>     # delete project
```

#### `vercel pull [路径]`
从云端拉取项目设置和环境变量。

```bash
vercel pull
```

---

### 环境变量
#### `vercel env`
管理环境变量。

**环境类型：`development`、`preview`、`production`

**示例：**
```bash
vercel env list production
vercel env add DATABASE_URL production
vercel env pull .env.local
```

---

### 域名与别名
#### `vercel domains`
管理域名。

```bash
vercel domains list                          # list domains
vercel domains add <domain> <project>        # add domain
vercel domains inspect <domain>              # show domain info
vercel domains remove <domain>               # remove domain
vercel domains buy <domain>                  # purchase domain
vercel domains transfer-in <domain>          # transfer domain to Vercel
```

#### `vercel alias`
管理部署别名。

**示例：**
```bash
vercel alias set my-app-abc123.vercel.app my-app.vercel.app
vercel alias set my-app-abc123.vercel.app custom-domain.com
```

---

### 部署
#### `vercel ls [应用]` / `vercel list`
列出所有部署。

```bash
vercel ls
vercel ls my-project
```

#### `vercel inspect [ID]`
显示部署信息。

```bash
vercel inspect <deployment-url-or-id>
```

#### `vercel logs <URL|ID>`
查看某个部署的运行时日志。

**选项：**
- `-j, --json` - 以 JSON 格式输出（兼容 jq）

**示例：**
```bash
vercel logs my-app.vercel.app
vercel logs <deployment-id> --json
vercel logs <deployment-id> --json | jq 'select(.level == "error")'
```

#### `vercel promote <URL|ID>`
将部署推送到生产环境。

```bash
vercel promote <deployment-url-or-id>
```

#### `vercel rollback <URL|ID>`
回滚到之前的部署版本。

```bash
vercel rollback
vercel rollback <deployment-url-or-id>
```

#### `vercel redeploy <URL|ID>`
重新构建并部署之前的版本。

```bash
vercel redeploy <deployment-url-or-id>
```

#### `vercel rm <ID>` / `vercel remove`
删除某个部署。

```bash
vercel rm <deployment-url-or-id>
```

---

### 认证与团队
```bash
vercel login [email]      # log in or create account
vercel logout             # log out
vercel whoami             # show current user
vercel switch [scope]     # switch between scopes/teams
vercel teams              # manage teams
```

---

### 其他命令
```bash
vercel open               # open project in dashboard
vercel init [example]     # initialize from example
vercel install [name]     # install marketplace integration
vercel integration        # manage integrations
vercel certs              # manage SSL certificates
vercel dns                # manage DNS records
vercel bisect             # binary search for bug-introducing deployment
```

---

## 全局选项
所有命令都支持以下全局选项：

| 选项 | 描述 |
|------|-------------|
| `-h, --help` | 显示帮助信息 |
| `-v, --version` | 显示版本信息 |
| `-d, --debug` | 开启调试模式 |
| `-t, --token <令牌>` | 设置认证令牌 |
| `-S, --scope` | 设置范围/团队 |
| `--cwd <目录>` | 设置工作目录 |
| `-A, --local-config <文件>` | 指定 `vercel.json` 文件的路径 |
| `--no-color` | 禁用颜色显示 |

---

## 快速参考
| 任务 | 命令 |
|------|---------|
| 部署 | `vercel` 或 `vercel --prod` |
| 启动开发服务器 | `vercel dev` |
| 链接项目 | `vercel link` |
| 列出部署 | `vercel ls` |
| 查看日志 | `vercel logs <URL>` |
| 添加环境变量 | `vercel env add <名称> <值>` |
| 拉取环境变量 | `vercel env pull` |
| 回滚部署 | `vercel rollback` |
| 添加域名 | `vercel domains add <域名> <项目>` |
| 获取文档 | `curl -s "https://vercel.com/docs/<路径>" -H 'accept: text/markdown'` |
| 文档站点地图 | `curl -s "https://vercel.com/docs/sitemap.md" -H 'accept: text/markdown'` |
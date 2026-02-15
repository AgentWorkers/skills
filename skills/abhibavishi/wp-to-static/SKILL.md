---
name: wp-to-static
description: 将一个 WordPress 网站转换为静态网站，并部署到 Cloudflare Pages。通过 SSH 镜像渲染后的 HTML 内容，仅提取被引用的资源（将文件大小从 1.5GB 以上压缩到约 25MB），修复 URL，自托管字体文件，移除 WordPress 中不必要的代码，最后完成部署。此方法适用于将 WordPress 网站迁移到静态托管环境的情况。
disable-model-invocation: true
argument-hint: "[site-url]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, WebFetch
metadata: {"openclaw":{"requires":{"bins":["ssh","ssh-agent","rsync","curl","git","gh","wrangler"],"env":["WP_SSH_HOST","WP_SSH_USER","WP_SSH_PORT","WP_SSH_KEY","WP_SITE_URL","WP_SITE_NAME"]},"emoji":"🔄","os":["darwin","linux"]}}
---

# 将 WordPress 网站转换为静态网站（使用 Cloudflare Pages）

将 WordPress 网站转换为像素完美的静态网站，并部署到 Cloudflare Pages。零攻击面、零托管成本、即时加载时间。

## 先决条件

在运行此操作之前，用户必须满足以下条件：

1. **已通过 GitHub CLI 进行身份验证：** 运行 `gh auth status` 进行验证。如果未登录，请先运行 `gh auth login`。
2. **已通过 Cloudflare Wrangler 进行身份验证：** 运行 `wrangler whoami` 进行验证。如果未登录，请先运行 `wrangler login`。
3. **SSH 密钥已添加到 ssh-agent：** 这是处理 SSH 密钥的推荐方式。运行以下命令：
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/your_wp_key
   ```
4. **已验证服务器主机密钥：** 用户应至少连接过服务器一次并接受过主机密钥，因此该密钥应存在于 `~/.ssh/known_hosts` 文件中。

## 环境变量

**必需的环境变量（缺少任何变量时请停止操作并告知用户）：**
- `WP_SSH_HOST` — SSH 主机名（例如：`ssh.example.com`）
- `WP_SSH_USER` — SSH 用户名
- `WP_SSH_PORT` — SSH 端口（例如：`18765`）
- `WP_SSH_KEY` — SSH 私钥文件的路径（例如：`~/.ssh/wp_key`）。密钥必须具有 `chmod 600` 权限。
- `WP_SITE_URL` — WordPress 网站地址（例如：`https://example.com`）
- `WP_SITE_NAME` — 项目简称（例如：`mysite`）

**可选的环境变量：**
- `CF_ACCOUNT_ID` — 用于部署到 Cloudflare Pages 的 Cloudflare 账户 ID
- `GH_REPO_VISIBILITY` — `private`（默认值）或 `public`

## 安全模型

- SSH 验证使用 `ssh-agent` — 在运行之前，密钥会被加载到代理中，因此不会通过环境变量或命令参数传递密码。
- SSH 主机密钥验证是启用的（不使用 `StrictHostKeyChecking=no`）—— 服务器必须已经添加到 `~/.ssh/known_hosts` 文件中。
- 凭据永远不会被记录、回显或显示。
- 凭据永远不会被提交到 Git 中。
- GitHub 仓库默认设置为私有的。

## 第 0 步：验证

1. 检查所有必需的环境变量是否已设置。如果缺少任何变量，请停止操作并告知用户。
2. 确认所需的二进制文件存在：`ssh`、`ssh-agent`、`rsync`、`curl`、`git`、`gh`、`wrangler`。
3. 确认 `gh auth status` 的执行成功。如果未成功，请告知用户运行 `gh auth login`。
4. 如果设置了 `CF_ACCOUNT_ID`，确认 `wrangler whoami` 的执行成功。如果未成功，请告知用户运行 `wrangler login`。
5. 确认 SSH 密钥文件存在且权限正确（`chmod 600`）。
6. 如果有任何缺失，请停止操作。

## 第 1 步：测试 SSH 连接

使用 ssh-agent 中的密钥测试连接：

```bash
ssh -i $WP_SSH_KEY -p $WP_SSH_PORT $WP_SSH_USER@$WP_SSH_HOST "echo connected"
```

如果密钥需要密码且 ssh-agent 未加载，请告知用户：
```
Please add your SSH key to ssh-agent first:
  eval "$(ssh-agent -s)"
  ssh-add /path/to/your/key
Then re-run /wp-to-static
```

如果主机密钥未被识别，请告知用户先手动连接一次以验证并接受主机密钥：
```
Please connect to the server once manually to verify the host key:
  ssh -i $WP_SSH_KEY -p $WP_SSH_PORT $WP_SSH_USER@$WP_SSH_HOST
Accept the host key, then re-run /wp-to-static
```

**请勿使用 `StrictHostKeyChecking=no`。** 也请勿绕过主机密钥验证。

## 第 2 步：定位 WordPress 安装位置

通过 SSH 连接到服务器并找到 WordPress 的 `public_html` 目录。常见位置包括：
- `~/www/DOMAIN/public_html/`
- `~/public_html/`
- `~/htdocs/`
- `/var/www/html/`

通过找到 `wp-config.php` 来确认目录位置。将此路径存储为 `WP_ROOT`。

## 第 3 步：在服务器上使用 wget 进行镜像复制

在服务器上运行 `wget --mirror` 命令（不要在本地执行）：

```bash
cd /tmp && rm -rf static_mirror && mkdir -p static_mirror && cd static_mirror && \
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent \
  --restrict-file-names=windows -e robots=off --timeout=30 --tries=3 --wait=0.5 \
  --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" \
  $WP_SITE_URL/ 2>&1 | tail -30
```

如果服务器上没有 `wget`，则可以在本地使用 `curl` 来获取渲染后的 HTML 文件。

## 第 4 步：将文件同步到本地

创建 `./build/site` 文件夹（切勿使用项目根目录作为临时目录）。

**排除服务器端的代码和敏感文件。** 只需要静态资源（图片、CSS、JS、字体）。PHP 文件、配置文件和其他服务器端代码严禁下载。

```bash
RSYNC_EXCLUDE="--exclude='*.php' --exclude='wp-config*' --exclude='.htaccess' --exclude='*.sql' --exclude='*.log' --exclude='debug.log' --exclude='error_log' --exclude='.env' --exclude='*.bak' --exclude='*.backup'"

rsync -avz $RSYNC_EXCLUDE server:/tmp/static_mirror/DOMAIN/ ./build/site/
rsync -avz $RSYNC_EXCLUDE server:$WP_ROOT/wp-content/uploads/ ./build/site/wp-content/uploads/
rsync -avz $RSYNC_EXCLUDE server:$WP_ROOT/wp-content/themes/ ./build/site/wp-content/themes/
rsync -avz $RSYNC_EXCLUDE server:$WP_ROOT/wp-content/plugins/ ./build/site/wp-content/plugins/
rsync -avz $RSYNC_EXCLUDE server:$WP_ROOT/wp-includes/ ./build/site/wp-includes/
```

同步完成后，确认没有下载到任何 PHP 或配置文件：
```bash
find ./build/site -name '*.php' -o -name 'wp-config*' -o -name '.htaccess' -o -name '.env' | head -20
```
如果发现了这些文件，请在继续之前删除它们。

## 第 5 步：提取引用的资源

**这是关键步骤。** 遍历所有 HTML 和 CSS 文件，找出所有引用的本地文件：

**从 HTML 文件中提取：** `src=`, `href=`, `data-src=`, `data-srcset=`, `srcset=`, 内联的 `background-image: url()`。

**从 CSS 文件中提取：** 所有的 `url()` 引用—— 将相对路径解析为站点根目录的路径。

将提取到的文件列表写入 `./build/referenced-files.txt`，然后仅将这些文件复制到 `./public/` 目录中，同时保持目录结构。这样通常可以将文件大小从 1.5GB 以上压缩到约 25MB。

## 第 6 步：修复绝对 URL

在 `index.html` 和所有 CSS 文件中：

1. 将 `$WP_SITE_URL/` 替换为空字符串（使用相对路径）。
2. 将所有 staging/dev 域名的 URL 替换为本地路径。
3. 自动加载 Google 字体：
   - 将每个 `.ttf` 文件下载到 `./public/fonts/`。
   - 更新 `@font-face src:` 为 `fonts/filename.ttf`。
4. 删除 `<link rel="preconnect">` 标签（用于加载 Google 字体）。

**CSS 路径的解析非常重要。** 如果 CSS 文件位于 `wp-content/uploads/cache/file.css`，则需要进行以下修改：
- `wp-content/uploads/` → `../../`
- `wp-content/themes/` → `../../themes/`
- `wp-includes/` → `../../../wp-includes/`

## 第 7 步：删除 WordPress 中不必要的内容

**删除以下内容：**
- `<meta name="generator" ...>`（WordPress、WPBakery、Slider Revolution 生成的元数据）
- `<link rel="EditURI"...>`, `<link rel="alternate"...>`（用于 RSS 和 oEmbed 的链接）
- `<link rel="https://api.w.org/"...>`, `<link rel="shortlink"...>`（用于外部链接）
- `<link rel="profile" href="gmpg.org/xfn/11">`
- `<link rel="dns-prefetch"...>`（用于加载 fonts.googleapis.com 的链接）
- W3 Total Cache 相关的 HTML 注释
- 内联 JSON 中的 `wp-json` 引用

**保留以下内容：** 电子邮件地址、`<link rel="canonical">`（更新为 `/`）

## 第 8 步：配置 Cloudflare Pages**

创建 `./public/_headers` 文件，为 `/fonts/*`, `/wp-content/*`, `/wp-includes/*` 设置强制缓存。

创建 `./public/_redirects` 文件，将 `/wp-admin/*`, `/wp-login.php`, `/xmlrpc.php`, `/feed/*` 重定向到 `/`（状态码 302）。

## 第 9 步：在本地进行验证

1. 从 `./public/` 目录中运行 `python3 -m http.server`。
2. 测试关键资源（CSS、JS、Logo、字体、图片）是否能返回 HTTP 200 状态码。
3. 告知用户打开网站并进行视觉检查。
4. **在部署前等待用户的确认**。

## 第 10 步：清理临时文件并部署

**在执行任何 Git 操作之前**，删除 `./build/` 目录，以确保不会意外提交服务器端的代码、PHP 文件或敏感数据：

```bash
rm -rf ./build
```

确认 `./public/` 目录中仅包含文件，且不包含 PHP 或配置文件：
```bash
find ./public -name '*.php' -o -name 'wp-config*' -o -name '.htaccess' -o -name '.env'
```
如果发现这些文件，请在继续之前删除它们。

然后执行以下操作：
1. `git init`，仅提交 `./public/` 和 `.gitignore`。
2. `git config http.postBuffer 524288000`（针对二进制资源）。
3. `gh repo create $WP_SITE_NAME --private --source=. --push`。
4. `CLOUDFLARE_ACCOUNT_ID=$CF_ACCOUNT_ID wrangler pages project create $WP_SITE_NAME --production-branch main`。
5. `CLOUDFLARE_ACCOUNT_ID=$CF_ACCOUNT_ID wrangler pages deploy ./public --project-name $WP_SITE_NAME`。
6. 验证部署结果，提供实时 URL，并提醒用户设置自定义域名。

## 安全规则

- **严禁显示或记录任何凭据（SSH 密钥、密码、令牌）**。
- **严禁将凭据提交到 Git 中（.gitignore 文件中必须排除 `.env`, *.key`, *.pem` 文件）。
- **严禁使用 `StrictHostKeyChecking=no` 或绕过 SSH 主机密钥验证**。
- **严禁在运行时通过命令行参数或环境变量传递密码**。
- **严禁删除当前的工作目录（这会导致 shell 的工作目录（CWD）发生变化）**。
- **严禁强制推送或使用可能破坏数据的 Git 命令**。
- **严禁从服务器同步 PHP 文件、wp-config、.htaccess、.env 或 SQL 数据库转储文件**。
- **使用 `./build/` 作为临时目录，`./public/` 作为输出目录—— 仅提交 `./public/` 中的文件**。
- **在执行任何 Git 操作之前，务必删除 `./build/` 目录，以防止意外提交服务器端文件**。
- **在提交之前确认 `./public/` 中不包含 PHP 或配置文件**。
- **如果遇到任何错误，请停止操作并报告——切勿盲目重试**。
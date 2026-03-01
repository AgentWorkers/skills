# 构建透明度仪表板（Build Transparency Dashboard）

我们创建了一个实时的公共“构建仪表板”，它可以自动显示开发工作的成果——包括提交次数、最后一次提交的消息以及提交时间戳。这些信息是从你的私有 GitHub 仓库中获取的，并显示在一个公共的静态网站上。

## 适用场景

当你需要以下功能时，可以使用这个方案：
- 向社区展示你的开发进度，且这些信息会在每次推送时自动更新；
- 在不暴露私有仓库的情况下公开展示开发成果；
- 添加一个社区意见征集板，让用户对你的下一个开发项目进行投票；
- 为你的产品或项目创建一个专业的 `/build` 页面。

## 实现原理

每当你的私有仓库发生新的 Git 提交时，相关的信息会在几分钟内自动更新到公共仪表板上。

## 包含的内容

### 1. 需要自定义的变量

在 `assets/build.html` 文件中，找到以下需要替换的占位符：

| 占位符 | 替换内容 |
|------|-------------|
| `YOUR_PROJECT_NAME` | 你的项目名称（例如：`MyApp`） |
| `YOUR_BORN_DATE` | 你的项目启动的 ISO 格式日期（例如：`2026-01-01T00:00:00-05:00`） |
| `YOUR_BRAND_COLOR` | 你的品牌颜色（十六进制代码，默认值：`#7c6eff`） |
| `YOUR_COIN_CA` | 代币合约地址（如果你的项目涉及代币相关功能）；如果不需要代币功能，可以完全移除这一部分 |
| `YOUR_IDEAS_API_URL` | 你的意见征集 API 的基础 URL（例如：`https://myapp.fly.dev/public/ideas`） |
| `YOUR_TWITTER_HANDLE` | 你的 Twitter 账号，用于导航栏的徽标显示 |
| `YOUR_QUEUE_ITEMS` | 你接下来要开发的内容（请编辑相关配置） |

在 `assets/github-actions.yml` 文件中，设置以下变量：

| 变量 | 说明 |
|----------|-------------|
| `SITE_REPO` | 你的公共网站仓库地址（例如：`username/my-site`） |
| `SITE_REPO_PATH` | 仓库在公共网站上的路径（例如：`my-site`） |
| `BOT_NAME` | 提交者的名称（例如：`StatusBot`） |
| `BOT_EMAIL` | 提交者的电子邮件 |

在 `assets/nav.js` 文件中，编辑文件顶部的配置对象。

### 2. 需要的 GitHub 密钥

你需要在私有仓库的 **设置** → **秘密和变量** → **动作** 中添加以下密钥：
- `GH_PAT`：具有 `repo` 权限的个人访问令牌（用于向公共网站仓库推送代码）。

### 3. 部署公共网站

`build.html` 文件是一个独立的静态页面，你可以使用以下方式部署它：
- **Fly.io**：在仓库中执行 `fly launch` 和 `fly deploy` 命令；
- **Netlify**：直接拖放或连接仓库；
- **GitHub Pages**：将代码推送到 `gh-pages` 分支；
- **Vercel**：直接连接仓库，无需额外配置。

### 4. 添加意见征集 API（可选）

如果需要一个社区意见征集功能，你需要运行一个 API。将 `scripts/ideas-api.js` 文件复制到你的后端应用程序中，并配置相应的路由。这个 API 使用简单的 JSON 文件来存储用户的意见，无需数据库。

如果你不需要这个功能，可以直接从 `build.html` 文件中移除与代币和意见征集相关的部分，这样它就只是一个纯静态的展示页面。

### 5. 将工作流添加到私有仓库

将 `assets/github-actions.yml` 文件复制到私有仓库的 `.github/workflows/update-build-status.yml` 文件中。每次提交代码时，工作流会自动执行。

## `status.json` 文件的格式

工作流会生成这个文件，并将其提交到你的公共网站仓库中。

## 设计系统

该模板使用了以下字体和样式：
- **Syne**（用于显示标题）+ **DM Sans**（用于正文）+ **DM Mono**（用于标签）；
- 深色主题：背景颜色为 `#050508`，品牌颜色为 `#7c6eff`；
- 动态的效果（如动画球体、固定的时间条）；
- 完全响应式设计（适用于桌面、平板和手机设备）；
- 你可以通过修改 `--nova` 或 `--nova2` 这些 CSS 变量来调整品牌颜色的显示效果。

## 实时示例

这个方案的实际实现可以在 [novaiok-site.fly.dev/build](https://novaiok-site.fly.dev/build) 看到。

## 推荐阅读的文件：
- `references/setup-guide.md`：包含详细的步骤和命令说明；
- `assets/build.html`：模板文件（请根据需要替换占位符）；
- `assets/github-actions.yml`：工作流配置文件。
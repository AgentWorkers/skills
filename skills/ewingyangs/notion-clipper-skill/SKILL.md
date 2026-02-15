---
name: notion-clipper-skill
description: 将网页内容复制到 Notion 中：该功能通过 Chrome 的 CDP（Content Delivery Protocol）获取任意网页的 URL，将 HTML 内容转换为 Markdown 格式，再将其转换为 Notion 可用的区块，并保存到用户指定的 Notion 数据库或页面中。适用于用户需要将网页内容保存到 Notion 中的情况，例如当用户输入“复制到 Notion”、“将页面保存到 Notion”或“将网页剪藏到 Notion”等指令时。
---

# Notion Clipper

这款工具可以将任何网页内容复制到 Notion 中。它利用 Chrome 的 CDP（Content Delivery Pipeline）功能进行完整的 JavaScript 渲染，然后将渲染后的内容转换为 Markdown 格式，最后插入到 Notion 中。

## 先决条件

1. **Notion API 密钥**：请在 [https://notion.so/my-integrations](https://notion.so/my-integrations) 上创建一个集成。  
2. **保存 API 密钥**：  
   ```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```  
3. **将目标数据库/页面共享给您的集成**：点击 “...” → “连接” → 选择您的集成名称。

## 首次设置

脚本运行时会自动安装所有依赖项，无需手动配置。

## 代理执行说明

**重要提示**：务必使用以下命令格式。首次运行时会自动安装依赖项。

1. 将当前 SKILL.md 文件所在的目录路径设置为 `SKILL_DIR`。
2. **命令格式**（位于 `scripts/` 目录下的 `package.json` 文件中；务必先运行 `lazy install` 命令）：  
   ```bash
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts <args>)
```  
3. 将 `${SKILL_DIR}` 替换为实际路径（例如：`/Users/xxx/.claude/skills/notion-clipper-skill`）。

## 使用方法

**为获得最佳效果，请使用以下命令格式：**  
```bash
# Recommended: Clear proxy env vars and use tsx runtime
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts <url> --database-name "Resources")
```

**为什么使用这种命令格式？**
- `unset http_proxy https_proxy all_proxy`：避免因代理冲突导致的 `ECONNREFUSED` 错误。
- `tsx` 运行时环境：`tsx` 是一个能正确处理直接网络连接的 Node.js 运行时环境（`bun` 可能存在代理相关问题）。
- `(test -d node_modules || npm install)`：如果依赖项缺失，会自动进行安装。

**如果遇到网络问题：**
1. 关闭所有 VPN 或代理软件。
2. 切换到稳定的网络环境（移动热点通常效果较好）。
3. 使用上述推荐的命令格式。

```bash
# Clip to a Notion database by NAME (recommended - searches for database)
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts <url> --database-name "Resource")

# Clip to a Notion database by ID
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts <url> --database <database_id>)

# Clip to an existing page (appends blocks)
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts <url> --page <page_id>)

# List all accessible databases
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts --list-databases)

# For pages requiring login (wait mode)
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && npx -y tsx main.ts <url> --database-name "Resource" --wait)
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `<url>` | 要复制的网页 URL |
| `--database-name, -n <名称>` | 按名称查找目标数据库 |
| `--database, -d <ID>` | 按 ID 查找目标 Notion 数据库 |
| `--page, -p <ID>` | 指定目标 Notion 页面的 ID（内容将添加到该页面） |
| `--list-databases, -l` | 列出所有可访问的数据库并退出程序 |
| `--wait, -w` | 在捕获内容前等待用户操作 |
| `--timeout, -t <毫秒>` | 页面加载超时时间（默认值：30000 毫秒） |
| `--no-bookmark` | 不在结果中添加书签块 |

## 复制模式

| 模式 | 行为 | 适用场景 |
|------|----------|----------|
| 自动（默认） | 在网络空闲时自动复制内容 | 公开页面、静态内容 |
| 等待（`--wait`） | 等待用户操作后复制内容 | 需要登录的页面、懒加载页面、有付费墙的页面 |

**等待模式的工作流程：**
1. 使用 `--wait` 参数运行脚本，Chrome 会打开网页。
2. 在浏览器中登录或浏览页面。
3. 在终端中按 Enter 键触发内容复制。

## 输出结构

- 当内容保存到数据库中时，会创建一个新页面，包含：
  - **页面标题**：网页的标题。
  - **URL**：源网页的 URL（如果数据库支持该字段）。
  - **内容**：书签块 + 转换后的 Markdown 内容。

- 当内容添加到现有页面中时，会添加：
  - 书签块（链接指向源网页）。
  - 分隔符。
  - 转换后的 Markdown 内容。

## 数据库设置

为获得最佳效果，请创建一个具有以下属性的 Notion 数据库：
- **名称**：页面的标题。
- **URL**：源网页的 URL（可选）。

## 示例

- 将一条推文复制到名为 “Resource” 的数据库中：  
  ```bash
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts "https://x.com/dotey/status/123456" -n "Resource")
```

- 首先列出所有可用的数据库：  
  ```bash
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts --list-databases)
```

- 复制需要登录才能访问的文章：  
  ```bash
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts "https://medium.com/article" -n "Reading" --wait)
```

- 将内容添加到阅读笔记页面中：  
  ```bash
(cd "${SKILL_DIR}/scripts" && (test -d node_modules || npm install) && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts "https://blog.example.com/post" -p xyz789)
```

## 快捷别名（可添加到您的 `.bashrc` 或 `.zshrc` 文件中）：  
  ```bash
alias notion-clip='(cd "${SKILL_DIR}/scripts" && unset http_proxy https_proxy all_proxy && npx -y tsx main.ts)'

# Usage: notion-clip <url> -n "Resources"
```

## 工作原理

1. **获取内容**：通过 CDP 打开 Chrome 浏览器并导航到目标 URL。
2. **渲染内容**：等待 JavaScript 代码执行完毕，然后滚动页面以触发懒加载。
3. **提取内容**：运行清理脚本，移除广告和导航栏，提取主要内容。
4. **转换格式**：将 HTML 内容转换为 Markdown 格式。
5. **保存结果**：调用 Notion API，将内容保存到数据库或现有页面中。

## 所需依赖项

- 安装了 Chrome/Chromium 浏览器。
- Node.js（脚本使用 `tsx` 运行；`bun` 可能会通过代理导致问题，因此建议使用 Node.js）。
- 配置了 Notion API 密钥。

（其他依赖项会在首次运行时自动安装。）

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `NOTION_CLIPPER_CHROME_PATH` | 自定义的 Chrome 可执行文件路径 |
| `NOTION_CLIPPER_CHROME_PROFILE_DIR` | 自定义的 Chrome 配置文件路径 |
| `https_proxy` / `HTTP_PROXY` | 用于访问 Notion API 的代理地址（例如：`http://127.0.0.1:7890`） |
| `http_proxy` / `HTTPS_PROXY` | 同 `https_proxy` |
| `all_proxy` | 可选代理地址（例如：`socks5://127.0.0.1:7890`） |

**示例（使用代理服务器 7890）：**  
```bash
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
```

## 故障排除

### 网络问题

| 错误 | 原因 | 解决方案 |
|--------|---------|-----------|
| `ECONNREFUSED 208.103.161.1:443` | DNS 返回被阻止的 IP 地址；代理冲突 | 1. 关闭 VPN 或代理软件。<br>2. 使用 `unset http_proxy https_proxy all_proxy`。<br>3. 切换网络环境（例如使用移动热点）。 |
| Notion API 返回空内容（状态码 200） | `bun` 在使用代理时可能出错 | 使用 `tsx` 运行脚本：`npx -y tsx main.ts ...`（不要使用 `bun`）。 |
| `fetch` 失败或 `ECONNREFUSED` | Node.js 的 `https` 环境变量未正确设置 | 1. 不使用代理；<br>2. 确保代理支持 HTTPS 流量。 |
| CloudFlare 返回 403 错误 | 直接访问被阻止；请使用域名而非 IP 地址；确保设置正确的 `Authorization` 头部。 |
| 内容复制失败 | 网络不稳定或 DNS 返回错误的 IP 地址 | 脚本现在具有 **6 次重试机制，并采用指数级退避策略（1 秒、2 秒、4 秒……）**。

**最佳实践**：为了稳定地访问 Notion API，请使用稳定的网络环境（移动热点通常比企业 VPN 更可靠）。

### 内容相关问题

| 错误 | 原因 | 解决方案 |
|--------|---------|-----------|
| 链接无效 | Notion API 不支持非 HTTP 协议的链接 | 脚本现在默认会移除所有无效的链接，以避免验证错误。内容会被保留，仅链接会被删除。 |
- **注意**：脚本会自动移除以下类型的无效链接：
  - `javascript:`、`data:`、`file:`、`about:` 协议。
  - 微信内部链接（`weixin:`、`wx://`）。
- 相对路径（`/path`、`./path`）。
- 仅包含哈希值的链接（`#anchor`）。
- 空链接。

### 其他问题

- **Chrome 未找到**：请设置 `NOTION_CLIPPER_CHROME_PATH` 环境变量。
- **超时错误**：增加 `--timeout` 参数的值，或使用 `--wait` 模式。
- **内容缺失**：对于动态加载的页面，请使用 `--wait` 模式。
- **Notion API 错误（401/403）**：检查 API 密钥的有效性和集成权限。
- **Notion API 错误**：确保集成具有访问目标数据库/页面的权限。

### 代码优化

为了解决网络不稳定或链接无效的问题，我们进行了以下优化：
1. **自动重试机制**：最多尝试 6 次，每次尝试间隔时间逐渐增加（1 秒 → 2 秒 → 4 秒……）。
2. **增加超时时间**：将 Notion API 请求的超时时间设置为 30 秒（之前为 25 秒）。
3. **链接清洗**：在提交数据之前，会先移除无效的 URL。
4. **使用 `tsx` 运行时环境**：`tsx` 是一个能正确处理直接网络连接的 Node.js 运行时环境。
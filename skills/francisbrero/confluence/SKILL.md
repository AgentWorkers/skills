---
name: confluence
description: 使用 `confluence-cli` 搜索和管理 Confluence 页面及空间。阅读相关文档，创建新页面，并在各个空间之间进行导航。
homepage: https://github.com/pchuri/confluence-cli
metadata: {"clawdbot":{"emoji":"📄","primaryEnv":"CONFLUENCE_TOKEN","requires":{"bins":["confluence"],"env":["CONFLUENCE_TOKEN"]},"install":[{"id":"npm","kind":"node","package":"confluence-cli","bins":["confluence"],"label":"Install confluence-cli (npm)"}]}}
---

# Confluence

使用 `confluence-cli` 搜索和管理 Confluence 页面。

## 必须完成的首次设置

在使用此功能之前，请完成以下步骤：

**步骤 1：安装 CLI**

```bash
npm install -g confluence-cli
```

**步骤 2：获取 API 令牌**

1. 访问 https://id.atlassian.com/manage-profile/security/api-tokens
2. 点击 “Create API token”（创建 API 令牌）
3. 为令牌命名（例如：“confluence-cli”）
4. 复制令牌内容

**步骤 3：配置 CLI**

```bash
confluence init
```

按照提示输入：
- **域名**：`yourcompany.atlassian.net`（不包括 `https://`）
- **电子邮件**：您的 Atlassian 账户邮箱
- **API 令牌**：粘贴步骤 2 中复制的令牌内容

**步骤 4：验证设置**

```bash
confluence spaces
```

如果看到自己的空间（spaces）被列出，那么您就可以开始使用 Confluence 了。

---

## 搜索页面

```bash
confluence search "deployment guide"
```

## 阅读页面内容

```bash
confluence read <page-id>
```

页面 ID 存在于 URL 中，例如：`https://yoursite.atlassian.net/wiki/spaces/SPACE/pages/123456/Title`，其中 ID 为 `123456`。

## 获取页面信息

```bash
confluence info <page-id>
```

## 按标题查找页面

```bash
confluence find "Page Title"
```

## 列出所有空间

```bash
confluence spaces
```

## 创建新页面

```bash
confluence create "Page Title" SPACEKEY --body "Page content here"
```

## 创建子页面

```bash
confluence create-child "Child Page Title" <parent-page-id> --body "Content"
```

**或者通过文件创建页面：**

```bash
confluence create-child "Page Title" <parent-id> --file content.html --format storage
```

## 更新页面内容

```bash
confluence update <page-id> --body "Updated content"
```

**或者通过文件更新页面内容：**

```bash
confluence update <page-id> --file content.html --format storage
```

## 列出子页面

```bash
confluence children <page-id>
```

## 导出包含附件的页面

```bash
confluence export <page-id> --output ./exported-page/
```

## 提示：

- 配置文件中的域名不应包含 `https://`，只需输入 `yourcompany.atlassian.net`
- 当页面内容采用 Confluence 的存储格式（类似 HTML 的格式）时，请使用 `--format storage` 选项
- 页面 ID 是数字形式的，可以在页面 URL 中找到
- 配置文件存储在 `~/.confluence-cli/config.json` 中
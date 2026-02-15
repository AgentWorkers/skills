---
name: mastodon-scout
description: 只读版的 Mastodon 命令行工具（CLI）。它可以输出易于阅读的时间线摘要，或者原始的 JSON 数据。
metadata:
  {
    "openclaw":
      {
        "emoji": "🦣",
        "requires": { "anyBins": ["{baseDir}/bin/mastodon-scout", "mastodon-scout"] },
        "envVars": [{ "name": "MASTODON_TOKEN", "required": true }],
        "install":
          [
            {
              "id": "download-darwin-arm64",
              "kind": "download",
              "os": ["darwin"],
              "url": "https://github.com/patelhiren/mastodon-scout/releases/download/v1.0.4/mastodon-scout-darwin-arm64.zip",
              "archive": "zip",
              "bins": ["mastodon-scout"],
              "targetDir": "{baseDir}/bin",
              "label": "Install Mastodon Scout (macOS Apple Silicon)",
            },
            {
              "id": "download-darwin-amd64",
              "kind": "download",
              "os": ["darwin"],
              "url": "https://github.com/patelhiren/mastodon-scout/releases/download/v1.0.4/mastodon-scout-darwin-amd64.zip",
              "archive": "zip",
              "bins": ["mastodon-scout"],
              "targetDir": "{baseDir}/bin",
              "label": "Install Mastodon Scout (macOS Intel)",
            },
            {
              "id": "download-linux-amd64",
              "kind": "download",
              "os": ["linux"],
              "url": "https://github.com/patelhiren/mastodon-scout/releases/download/v1.0.4/mastodon-scout-linux-amd64.zip",
              "archive": "zip",
              "bins": ["mastodon-scout"],
              "targetDir": "{baseDir}/bin",
              "label": "Install Mastodon Scout (Linux)",
            },
            {
              "id": "download-windows-amd64",
              "kind": "download",
              "os": ["win32"],
              "url": "https://github.com/patelhiren/mastodon-scout/releases/download/v1.0.4/mastodon-scout-windows-amd64.zip",
              "archive": "zip",
              "bins": ["mastodon-scout.exe"],
              "targetDir": "{baseDir}/bin",
              "label": "Install Mastodon Scout (Windows)",
            },
          ],
      },
  }
---

# Mastodon Scout

## 功能

这是一个仅限读取的 Mastodon 命令行工具（CLI），用于从 Mastodon API 中获取数据。默认情况下，它会返回易于阅读的摘要；如果使用 `--json` 标志，则会返回原始的 JSON 数据。

---

## 使用规则（必须遵守）

### 可执行文件路径
- **macOS / Darwin** → `{baseDir}/bin/mastodon-scout`
- **Linux** → `{baseDir}/bin/mastodon-scout`

### 命令

#### 主时间线
```
{baseDir}/bin/mastodon-scout home
```
获取已认证用户的个人时间线。

#### 用户发布的推文
```
{baseDir}/bin/mastodon-scout user-tweets
```
获取已认证用户自己发布的推文。

#### 被提及
```
{baseDir}/bin/mastodon-scout mentions
```
获取提及已认证用户的推文。

#### 搜索
```
{baseDir}/bin/mastodon-scout search <query>
```
搜索与查询匹配的推文。

### 标志（可选）
```
--instance <url>       # Mastodon instance URL (default: https://mastodon.social)
--limit <int>          # Number of items to return (default: 20)
--timeout <int>        # Timeout in seconds (default: 30)
--json                 # Output raw JSON instead of human-readable text
```

### 环境变量（必须设置）
```
MASTODON_TOKEN         # OAuth bearer token for authentication
```

---

## 输出格式

### 文本模式（默认）
```bash
mastodon-scout home
```
以易于阅读的形式返回时间线数据的摘要。

该工具可以对时间线结果进行总结和解释，以便用户更轻松地理解。

### JSON 模式
```bash
mastodon-scout --json home
```
直接返回来自 Mastodon API 的原始 JSON 数据。

在 JSON 模式下，输出内容将保持原样，不进行任何解释。

---

## 错误处理

- 如果程序以非零状态退出：
  - 在 JSON 模式下：直接返回错误信息。
  - 在文本模式下：工具可以向用户解释错误原因。
  - 不需要重试。

- 如果未设置 `MASTODON_TOKEN`：
  - 程序将输出错误信息，并提示用户进行身份验证设置。

---

## 可能触发该工具的命令示例

- `mastodon-scout home`
- `show my mastodon timeline`
- `check mastodon mentions`
- `search mastodon for "golang"`
- `get my mastodon posts`

---

## 性能要求

- 直接执行该工具的二进制文件。
- 不需要使用任何外部网络搜索工具。
- 尽量减少延迟。

---

## 注意事项

- 在文本模式下，工具可以对结果进行总结和解释。
- 在 JSON 模式下，输出内容将保持原样，不进行任何解释。
- 该工具仅具有读取权限（无法发布内容、关注用户或其他操作）。

---

## 身份验证设置（工具可提供帮助）

**严格模式下的例外**：如果用户需要帮助获取令牌，工具可以在执行命令前提供指导。

该工具需要用户在 `MASTODON_TOKEN` 环境变量中设置 Mastodon 的 OAuth 承载令牌。

### 获取令牌的步骤（指导用户）：

**步骤 1：访问开发设置**
- 用户需要登录他们的 Mastodon 账户（例如：mastodon.social、fosstodon.org）。
- 转到：**设置 → 开发**（或偏好设置 → 开发）。
- 直接访问地址：`https://[实例域名]/settings/applications`

**步骤 2：创建应用程序**
- 点击“新建应用程序”。
- 填写详细信息：
  - **应用程序名称**：`mastodon-scout`（或任意名称）
  - **应用程序网站**：可以留空或使用任意 URL
  - **重定向 URI**：`urn:ietf:wg:oauth:2.0:oob`（适用于 CLI 应用程序）
  - **权限范围**：**仅选择“读取”**（取消勾选“写入”、“关注”、“推送”选项）。

**步骤 3：获取访问令牌**
- 点击“提交”。
- 点击创建的应用程序查看详细信息。
- 复制“您的访问令牌”字段的值。

**步骤 4：设置环境变量**
```bash
export MASTODON_TOKEN="paste_token_here"
```

**步骤 5：验证令牌是否有效**
```bash
{baseDir}/bin/mastodon-scout home
```

### 常见的 Mastodon 实例：
- `mastodon.social` - 通用用途（默认）
- `fosstodon.org` - 开源/技术社区
- `mas.to` - 专注于技术的社区
- `hachyderm.io` - 技术/信息安全社区

对于非默认实例，请使用 `--instance https://your-instance.com` 标志。

### 安全提示：
- 该令牌仅具有读取权限（无法发布内容、关注用户或删除数据）。
- 请保密令牌信息（不要将其提交到 Git 仓库）。
- 令牌可以在开发设置中随时被撤销。
- 每个 Mastodon 实例都需要单独的令牌。

---

## 输出格式

### 文本模式（默认）
以易于阅读的形式显示推文摘要。具体展示方式由工具决定。

### JSON 模式（使用 `--json` 标志）
所有命令返回的 JSON 数据格式如下：

```json
{
  "success": true,
  "data": [ /* Mastodon API response */ ]
}
```

如果发生错误，输出格式如下：

```json
{
  "success": false,
  "error": "error message"
}
```

`data` 字段包含未经修改的原始 Mastodon API 响应内容。
---
name: wordpress-oauth
description: 启动并完成 WordPress.com 的 OAuth 过程，然后通过 WordPress.com 的 REST API 发布文章。当您需要生成授权 URL、交换回调代码以获取访问令牌、验证令牌的有效性，或者将草稿/已发布的文章发布到 WordPress.com 或与 Jetpack 连接的网站时，请使用此功能。
---
# WordPress OAuth 技能

使用此技能可以执行需要人工参与的 OAuth 流程，并使用存储的令牌（bearer token）来发布帖子。

## 该技能包含的文件

- 脚本：`{baseDir}/wp.oauth_skill.py`
- OAuth 状态存储文件：`{baseDir}/oauth_state.json`
- 凭据存储文件：`{baseDir}/credentials.json`

该技能将状态信息和凭证存储在该技能目录下的文件中。

## 命令

使用 Python 3 运行脚本：

```bash
python3 {baseDir}/wp_oauth_skill.py --help
```

### 1) 开始 OAuth 流程

```bash
python3 {baseDir}/wp_oauth_skill.py begin-oauth \
  --client-id "$WPCOM_CLIENT_ID" \
  --redirect-uri "$WPCOM_REDIRECT_URI" \
  --scope "posts media" \
  --blog "$WPCOM_SITE"
```

返回 `auth_url` 和 `state`。打开该 URL，授权访问，然后复制回调 URL。

### 2) 交换令牌

```bash
python3 {baseDir}/wp_oauth_skill.py exchange-token \
  --client-id "$WPCOM_CLIENT_ID" \
  --client-secret "$WPCOM_CLIENT_SECRET" \
  --redirect-uri "$WPCOM_REDIRECT_URI" \
  --callback-url "https://example/callback?code=...&state=..."
```

验证 CSRF `state`，将代码（code）交换为令牌（token），并将凭证写入 `{baseDir}/credentials.json`。

### 3) 检查令牌有效性

```bash
python3 {baseDir}/wp_oauth_skill.py token-info --client-id "$WPCOM_CLIENT_ID"
```

使用 WordPress 的令牌信息（token-info）接口检查令牌的有效性。

### 4) 发布帖子

```bash
python3 {baseDir}/wp_oauth_skill.py publish-post \
  --site "$WPCOM_SITE" \
  --title "My post" \
  --content "<p>Hello from OpenClaw</p>" \
  --status draft
```

使用存储的令牌通过 `POST /rest/v1.1/sites/$site/posts/new` 发布帖子。

## 推荐的操作流程

1. 运行 `begin-oauth`。
2. 在浏览器中打开 `auth_url` 并完成授权。
3. 将回调 URL 复制到 `exchange-token` 命令中。
4. （可选）运行 `token-info` 命令。
5. 运行 `publish-post` 命令。

## 安全注意事项

- 严禁共享 `credentials.json` 或客户端密钥（client secrets）。
- 将首次发布的帖子设置为 `draft` 状态。
- 如果回调状态失败或授权代码过期，请重新运行 `begin-oauth`。
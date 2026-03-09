---
name: clinstagram
description: 完整的 Instagram CLI 工具：支持发布内容、发送私信、发布动态、查看分析数据、管理粉丝、使用标签、获取点赞数和评论数等功能。兼容 Meta Graph API（官方接口，安全可靠）和私有 API（提供全部功能）。提供三种合规模式：仅限官方模式、混合安全模式以及启用私有 API 模式。
metadata: {"openclaw": {"requires": {"bins": ["clinstagram"], "env": ["CLINSTAGRAM_CONFIG_DIR"]}, "primaryEnv": "CLINSTAGRAM_SECRETS_FILE", "emoji": "📸", "homepage": "https://github.com/199-biotechnologies/clinstagram", "install": [{"pip": "clinstagram"}]}}
---
# clinstagram

这是一个专为AI代理设计的混合型Instagram命令行工具（CLI），它根据合规政策在Meta Graph API和instagrapi私有API之间进行路由切换。

## 安装

```bash
pip install clinstagram
```

## 重要提示：子命令执行前需要设置全局参数

```bash
clinstagram --json --account main dm inbox     # CORRECT
clinstagram dm inbox --json                    # WRONG — Typer limitation
```

全局参数：
- `--json`：以JSON格式输出结果
- `--account NAME`：指定目标Instagram账户的名称
- `--backend auto|graph_ig|graph_fb|private`：指定使用哪个后端（graph_ig：Instagram官方API；graph_fb：Facebook Graph API；private：instagrapi私有API）
- `--proxy URL`：设置代理服务器地址
- `--dry-run`：进行无实际数据操作的测试运行
- `--enable-growth-actions`：启用用户增长相关功能（如关注、取消关注、点赞等）

## 快速入门

```bash
# Check status
clinstagram --json auth status

# Set compliance mode
clinstagram config mode official-only    # Graph API only, zero risk
clinstagram config mode hybrid-safe      # Graph primary, private read-only (default)
clinstagram config mode private-enabled  # Full access, user accepts risk

# Connect backends
clinstagram auth connect-ig   # Instagram Login (posting, comments, analytics)
clinstagram auth connect-fb   # Facebook Login (adds DMs, stories, webhooks)
clinstagram auth login         # Private API (username/password/2FA via instagrapi)
```

## 命令列表

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `auth` | `status` | 查看账户状态 |
| `login` | 登录Instagram |
| `connect-ig` | 连接Instagram官方API |
| `connect-fb` | 连接Facebook Graph API |
| `probe` | 测试API连接是否正常 |
| `logout` | 登出Instagram |

示例：`auth status --json`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `post` | `photo` | 上传照片 |
| `video` | 上传视频 |
| `reel` | 上传短视频 |
| `carousel` | 上传图片轮播 |

示例：`post photo /path/to/image.jpg`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `dm` | `inbox` | 查看私信箱 |
| `thread ID` | 查找特定帖子的ID |
| `send @user "text"` | 给用户发送私信 |
| `send-media` | 附加媒体文件发送私信 |
| `search` | 搜索Instagram内容 |

示例：`dm @user "Hello!"`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `story` | `list [@user]` | 查看用户的动态 |
| `post-photo` | 在用户的动态中发布照片 |
| `post-video` | 在用户的动态中发布视频 |
| `viewers ID` | 获取帖子的观看者ID |

示例：`post-video /path/to/video.mp4`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `comments` | `list MEDIA_ID` | 查看指定帖子的评论 |
| `add` | 在评论区添加新评论 |
| `reply` | 回复评论 |
| `delete` | 删除评论 |

示例：`add "This is a comment."` （需要`--enable-growth-actions`参数）  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `analytics` | `profile` | 查看用户资料 |
| `post ID\|latest` | 查看指定帖子或最新帖子 |
| `hashtag TAG` | 搜索包含特定标签的帖子 |

示例：`analytics profile`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `followers` | `list` | 查看用户关注者列表 |
| `following` | 关注用户 |
| `unfollow @user` | 取消关注用户 |

示例：`follow @user`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `user` | `info @user` | 查看用户信息 |
| `search QUERY` | 搜索用户或内容 |
| `posts @user` | 查看用户的帖子 |

示例：`posts @user "Hello, world!"`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `hashtag` | `top TAG` | 查看热门标签 |
| `recent TAG` | 查看最近发布的标签相关内容 |

示例：`hashtag #travel`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `like` | `post MEDIA_ID` | 给帖子点赞 |
| `undo MEDIA_ID` | 取消对帖子的点赞 |

示例：`like post ID`  

| 命令组 | 命令 | 说明 |
|-------|----------|-------|
| `config` | `show` | 显示配置信息 |
| `mode MODE` | 设置工作模式（`official-only`、`hybrid-safe`、`private-enabled`）

## JSON输出格式

成功时返回JSON格式的结果；遇到错误时返回相应的错误信息。

```json
{"exit_code": 0, "data": {}, "backend_used": "graph_fb"}
```

## 错误代码及处理方式

| 代码 | 含义 | 处理方式 |
|------|---------|--------|
| 0 | 操作成功 | 解析数据完成 |
| 1 | 参数错误 | 请检查命令语法 |
| 2 | 登录失败 | 运行`remediation`命令尝试修复 |
| 3 | API请求被限制 | 等待`retry_after`秒数后重试 |
| 4 | API调用失败 | 重试请求 |
| 5 | 需要用户验证 | 显示提示信息并要求用户验证 |
| 6 | 违反政策限制 | 更改合规模式 |
| 7 | 功能不可用 | 更换使用其他后端 |

## 代理工作流程

该工具支持多种Instagram功能，但部分功能（如关注、取消关注、点赞等）默认是禁用的。启用这些功能前需用户明确同意。

## 后端功能支持情况

| 功能 | graph_ig | graph_fb | private |
|---------|--------:|:--------:|:-------:|
| 发布帖子 | 支持 | 支持 | 支持 |
| 私信箱 | 不支持 | 支持 | 支持 |
| 冷静私信 | 不支持 | 不支持 | 支持 |
| 动态内容 | 不支持 | 支持 | 支持 |
| 评论 | 支持 | 支持 | 支持 |
| 分析数据 | 支持 | 支持 | 支持 |
| 关注/取消关注 | 不支持 | 不支持 | 支持 |
| 标签相关操作 | 支持 | 支持 | 支持 |

功能优先级：`graph_ig` > `graph_fb` > `private`。可以通过`--backend`参数进行切换。

## 使用示例

更多使用示例请参考相关文档或示例代码。

## 配置文件

配置文件：`~/.clinstagram/config.toml`。可以通过环境变量`CLINSTAGRAM_CONFIG_DIR`指定配置文件的路径。
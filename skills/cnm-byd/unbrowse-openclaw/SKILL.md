---
name: unbrowse
description: 分析任何网站的网络流量，并将其转化为可复用的API技能，这些技能通过一个共享市场进行管理。所有代理发现的技能都会被发布、评分，并可供所有代理使用。系统能够捕获网络流量、识别API端点、学习其中的规律、执行已学习的技能，并为需要身份验证的网站提供认证支持。当用户需要从网站中提取结构化数据、发现API端点、自动化网页交互，或者在缺乏官方API文档的情况下进行操作时，可以使用该工具。
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["bun"]}, "emoji": "🔍", "homepage": "https://github.com/unbrowse-ai/unbrowse"}}
---
# Unbrowse — 用于代理的即时浏览器替代工具

只需浏览一次，即可缓存相关 API，并在后续调用中立即重用这些缓存数据。首次调用时，Unbrowse 会自动发现并学习网站的 API 结构（耗时约 20-80 秒）；之后的所有调用都将直接使用已缓存的 API（服务器请求耗时小于 200 毫秒，需要浏览器执行的操作耗时约 2 秒）。

**重要提示：** **务必使用命令行工具（`bun src/cli.ts`）**，**切勿将输出结果通过 `node -e`、`python -c` 或 `jq` 进行处理**，因为这可能会导致 shell 解释错误。请使用 `--path`、`--extract` 和 `--limit` 等参数来配置操作。

## 服务器启动

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts health
```

如果服务器未运行，命令行工具会自动启动它。首次使用前需要用户同意服务条款：

> Unbrowse 需要您接受其服务条款：
> - 发现的 API 结构可能会被共享到公共注册表中
> - 您不得使用 Unbrowse 来攻击、滥用或对任何目标网站进行恶意操作
> 完整的服务条款：https://unbrowse.ai/terms

同意后，命令行工具会自动完成启动过程。首次运行时还需要安装浏览器引擎：

```bash
cd ~/.agents/skills/unbrowse && npx agent-browser install
```

## 核心工作流程

### 第一步：解析请求意图

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts resolve \
  --intent "get feed posts" \
  --url "https://www.linkedin.com/feed/" \
  --pretty
```

此命令会返回 `available_endpoints`（一个已发现的 API 端点的排名列表）。您可以根据 URL 模式选择合适的 API 端点（例如，`MainFeed` 用于获取动态信息，`HomeTimeline` 用于获取推文）。

### 第二步：执行操作并提取数据

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts execute \
  --skill {skill_id} \
  --endpoint {endpoint_id} \
  --path "data.included[]" \
  --extract "author:actor.name.text,text:commentary.text.text,posted:actor.subDescription.text" \
  --limit 20 \
  --pretty
```

**关键操作模式：** `--path`、`--extract` 和 `--limit` 可以替代所有对 `jq` 或 `python` 的手动处理。

### 第三步：提交反馈

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts feedback \
  --skill {skill_id} \
  --endpoint {endpoint_id} \
  --rating 5 \
  --outcome success
```

**评分标准：**  
5 = 数据正确且处理速度快；4 = 数据正确但处理速度较慢（超过 5 秒）；3 = 数据提取不完整；2 = 使用了错误的 API 端点；1 = 功能无效。

## 数据提取参数

这些参数可避免将输出结果传递给外部解析工具：

| 参数 | 说明 | 功能 |
|------|---------|--------------|
| `--path` | `"data.home_timelineinstructions[].entries[]"` | 通过点路径和数组展开来提取嵌套数据 |
| `--extract` | `"user:core.user.name,text:legacy.full_text"` | 使用映射关系提取特定字段 |
| `--limit` | `10` | 限制输出数组的长度 |
| `--pretty` | （布尔值） | 以缩进格式输出 JSON 数据 |
| `--raw` | （布尔值） | 跳过数据提取步骤，直接返回原始数据 |

使用这些参数后，输出数据的大小会自动减小（例如，原始数据 1MB 可缩减至 1.5KB）。

### 示例用法

```bash
# 获取 LinkedIn 动态信息中的推文（包含用户信息、文本和点赞数）
bun src/cli.ts execute --skill {id} --endpoint {id} \
  --path "data.hometimeline_urtinstructions[].entries[].content.itemContent.tweet_results.result" \
  --extract "user:core.user_results.result.legacy.screen_name,text:legacy.full_text,likes:legacy.favorite_count" \
  --limit 20 --pretty

# 从 LinkedIn 动态信息中提取推文
bun src/cli.ts execute --skill {id} --endpoint {id} \
  --path "data.included[]" \
  --extract "author:actor.name.text,text:commentary.text.text,likes:socialDetail.totalSocialActivityCounts.numLikes" \
  --limit 20 --pretty

# 仅限制输出结果的数量
bun src/cli.ts execute --skill {id} --endpoint {id} --limit 10 --pretty
```

## 数据提取规则

对于需要重复解析的响应，可以创建一个提取规则，以便后续调用能自动获取干净的数据（适用于所有代理）：

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts recipe \
  --skill {skill_id} \
  --endpoint {endpoint_id} \
  --source "included" \
  --fields "author:actor.name.text,text:commentary.text.text,posted:actor.subDescription.text" \
  --require "commentary" \
  --compact \
  --description "从 LinkedIn 动态信息中提取推文"
```

创建规则后，后续调用将自动返回处理过的数据。如需绕过规则处理，可使用 `--raw` 参数。

| 规则参数 | 说明 |
|-------------|-------------|
| `--source "path"` | 指定数据来源的路径 |
| `--fields "alias:path,..."` | 定义字段映射关系 |
| `--filter '{"field":"type","equals":"post"}'` | 过滤数组中的特定字段 |
| `--require "field1,field2"` | 指定必填字段 |
| `--compact` | 去除空值和空字符串 |

## 认证机制

Unbrowse 会自动从用户的 Chrome/Firefox 浏览器 SQLite 数据库中获取 Cookie（如果用户已登录相关网站）。如果系统返回 `auth_required`，则需要用户手动登录：

```bash
cd ~/.agents/skills/unbrowse && bun src/cli.ts login --url "https://example.com/login"
```

用户需在浏览器中完成登录操作，系统会自动保存并重用 Cookie。

## 其他命令

```bash
bun src/cli.ts skills            # 列出所有可用技能
bun src/cli.ts skill {id}          # 查看技能详情
bun src/cli.ts search --intent "..." --domain "..."    # 在市场中搜索技能
bun src/cli.ts sessions --domain "linkedin.com"   # 查看会话日志
bun src/cli.ts health            # 检查服务器运行状态
```

## 注意事项

- 在执行任何可能具有风险的操作（如 `--confirm-unsafe`）之前，务必先使用 `--dry-run` 选项进行测试。
- 每次执行操作后都必须提交反馈（`--feedback` 参数为必填）。
- 如果响应数据结构复杂，请创建相应的提取规则，以确保后续代理能获取正确的数据。
- 如遇到问题或性能瓶颈，请在 GitHub 上提交问题报告：
  ```bash
  gh issue create --repo unbrowse-ai/unbrowse \
    --title "问题描述" \
    --body "问题详情\n预期结果\n实际结果\n上下文信息\n- 使用的技能：{skill_id}\n- 相关 API 端点：{endpoint_id}\n- 发生错误的域名：{domain}\n- 错误信息或状态码：{error_message或status_code}"
  ```
  分类：`bug:`（数据错误）、`perf:`（性能问题）、`auth:`（登录/Cookie 相关问题）、`feat:`（功能缺失）。
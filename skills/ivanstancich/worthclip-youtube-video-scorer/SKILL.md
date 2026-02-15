---
name: worthclip
description: "基于人工智能的YouTube视频评分系统。该系统会根据用户的学习目标和个人偏好，为视频打分（1-10分）。用户可以使用该工具来评估YouTube视频、查看已评分的视频列表、管理关注的频道，或查看API的使用情况。系统还提供AI生成的摘要、视频内容与用户偏好的匹配分析结果，以及精选的视频推荐列表。关键词：YouTube、视频、评分、个人偏好、视频列表、摘要、人工智能、学习、频道。使用该工具需要从https://worthclip.com/developers获取WorthClip API密钥。"
license: MIT
homepage: https://worthclip.com
allowed-tools: Bash Read
disable-model-invocation: true
metadata: {"clawdbot":{"emoji":"bullseye","primaryEnv":"WORTHCLIP_API_KEY","requires":{"bins":["curl","jq"],"env":["WORTHCLIP_API_KEY"]}}}
---

# WorthClip - YouTube 视频评分服务

根据您的个性化学习目标，为 YouTube 视频打分（1-10 分）。该服务提供基于 AI 的视频摘要、内容分析以及精选的视频推荐。

## 设置

1. 在 [https://worthclip.com](https://worthclip.com) 注册账号。
2. 进入“设置” > “API 密钥”，生成 API 密钥。
3. 将生成的 API 密钥设置为：`export WORTHCLIP_API_KEY="wc_your_key_here"`。

## 命令

### 为视频评分

根据用户的学习目标和偏好为 YouTube 视频打分。评分过程为异步进行，系统会自动进行轮询。

```bash
bash {baseDir}/scripts/score.sh "VIDEO_ID"
```

该脚本会提交视频进行评分，等待评分结果（最长 60 秒），然后返回评分结果（以 JSON 格式）。如果视频已经过评分，系统会立即返回现有的评分结果。

### 获取推荐视频列表

根据视频相关性返回评分后的视频列表，支持自定义过滤条件。

```bash
bash {baseDir}/scripts/feed.sh [--min-score N] [--verdict VERDICT] [--limit N] [--cursor N]
```

选项：
- `--min-score N`：仅返回评分在 N 分及以上的视频（1-10 分）。
- `--verdict VERDICT`：按评分结果过滤视频（例如：“观看”、“跳过”）。
- `--limit N`：每页显示的视频数量。
- `--cursor N`：从上一次请求开始的下一个视频索引。

### 查看使用情况

显示当前计费周期内的使用统计信息和限制。

```bash
bash {baseDir}/scripts/usage.sh
```

## API 参考

基础 URL：`https://greedy-mallard-11.convex.site/api/v1`

该 API 由 WorthClip 的无服务器后端服务（Convex）提供。域名 `greedy-mallard-11.convex.site` 是 WorthClip 的生产环境部署地址。您可以通过访问 [https://worthclip.com/developers](https://worthclip.com/developers) 验证这一点。

所有请求（除 `/health` 外）都需要在请求头中添加 `Authorization: Bearer YOUR_API_KEY`。

| 端点          | 方法        | 描述                                      |
|-----------------|------------|-----------------------------------------|
| /health       | GET        | 健康检查（无需认证）                              |
| /score       | POST        | 为视频评分（异步，返回包含作业 ID 的 202 状态码）             |
| /score/:jobId    | GET        | 查询评分作业的状态                            |
| /videos/:ytId/summary | GET        | 获取视频摘要                              |
| /videos/:ytId     | GET        | 获取包含完整评分的视频详情                        |
| /feed       | GET        | 分页显示评分后的视频列表（支持过滤）                      |
| /channels     | GET        | 列出用户关注的频道                            |
| /channels/lookup | POST        | 根据 YouTube URL 查找频道                        |
| /channels/track   | POST        | 新增频道关注                              |
| /persona      | GET        | 获取当前的用户信息和学习目标                        |
| /persona      | PUT        | 更新用户信息                              |
| /goals       | PUT        | 更新学习目标                              |
| /usage       | GET        | 查看当前计费周期内的使用统计信息                    |

## 速率限制

- **通用限制：** 每分钟 60 次请求（所有端点）。
- **评分限制：** 每分钟 20 次请求（`/score` 和 `/score/:jobId` 端点）。

响应头信息：
- `X-RateLimit-Limit`：当前时间窗口内的最大请求次数。
- `X-RateLimit-Remaining`：当前时间窗口内剩余的请求次数。
- `Retry-After`：在遇到 429 错误时重新尝试的等待时间（仅适用于 429 错误）。

## 错误格式

所有错误都会返回统一的 JSON 结构，并附带相应的 HTTP 状态码：

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description of the error"
  }
}
```

常见错误代码：
- `UNAUTHORIZED` (401)：API 密钥缺失或无效。
- `RATE_LIMITED` (429)：请求次数过多。
- `NOT_FOUND` (404)：资源未找到。
- `VALIDATION_ERROR` (400)：请求参数无效。
- `INTERNAL_ERROR` (500)：服务器内部错误。

## 基础 URL

```
https://greedy-mallard-11.convex.site/api/v1
```
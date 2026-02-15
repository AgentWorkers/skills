---
name: tokportal
description: 大规模自动化社交媒体管理——通过 TokPortal API 利用 30 款基于人工智能的 MCP 工具来创建 TikTok/Instagram 账号、分发视频、上传内容并跟踪分析数据。
version: 1.0.0
homepage: https://developers.tokportal.com
metadata: {"openclaw":{"emoji":"🎵","homepage":"https://developers.tokportal.com","requires":{"env":["TOKPORTAL_API_KEY"]},"primaryEnv":"TOKPORTAL_API_KEY"}}
---

# TokPortal

通过 TokPortal 平台，您可以批量管理社交媒体账户的创建、视频分发及数据分析。该技能通过专用的 MCP 服务器提供了 30 种工具，使您的 AI 代理能够全面控制大规模的 TikTok 和 Instagram 操作。

## 设置

### 1. 获取 API 密钥

在 [tokportal.com](https://tokportal.com) 注册，并在 [app.tokportal.com/developer/api-keys](https://app.tokportal.com/developer/api-keys) 生成 API 密钥。

### 2. 安装 MCP 服务器

推荐使用 MCP 服务器与 OpenClaw 配合使用 TokPortal：

```bash
npm install -g tokportal-mcp
```

### 3. 配置 OpenClaw

在您的 `~/.openclaw/openclaw.json` 文件中添加以下配置：

```json
{
  "skills": {
    "entries": {
      "tokportal": {
        "enabled": true,
        "apiKey": "tok_live_your_key_here"
      }
    }
  }
}
```

或者设置环境变量：

```bash
export TOKPORTAL_API_KEY="tok_live_your_key_here"
```

### 4. 添加 MCP 服务器配置

将以下配置添加到 MCP 配置文件（Cursor 的 `.cursor/mcp.json` 或 Claude Desktop 的 `claude_desktop_config.json`）中：

```json
{
  "mcpServers": {
    "tokportal": {
      "command": "npx",
      "args": ["-y", "tokportal-mcp"],
      "env": {
        "TOKPORTAL_API_KEY": "tok_live_your_key_here"
      }
    }
  }
}
```

## 可用工具（共 30 种）

### 信息类工具（6 种）
- `get_me` — 获取您的个人资料、信用余额和 API 密钥信息
- `get_credit_balance` — 查看详细的信用余额及过期日期
- `get_credit_history` — 获取交易历史记录（分页显示）
- `get_countries` — 查看可创建账户的国家列表
- `get_platforms` — 查看支持的平台（TikTok、Instagram）及其功能
- `get_credit_costs` — 查看所有操作的完整费用信息

### 包装类工具（8 种）
- `create_bundle` — 创建账户包（仅包含账户）、账户+视频包或仅包含视频的包
- `create_bulk_bundles` — 一次性创建多个账户包
- `list_bundles` — 根据状态或平台筛选账户包列表
- `get_bundle` — 获取包含账户配置和视频的完整账户包信息
- `publish_bundle` — 发布已配置的账户包
- `unpublish_bundle` — 将账户包恢复为草稿状态
- `add_video_slots` — 为现有账户包添加视频插槽（每个插槽 2 信用点）
- `add_edit_slots` — 为账户包添加编辑插槽（每个插槽 3 信用点）

### 账户配置类工具（4 种）
- `get_account_config` — 查看当前账户设置
- `configure_account` — 设置用户名、显示名称、个人简介和头像
- `finalize_account` — 审批处于审核状态的账户
- `request_account_corrections` — 请求修改特定字段

### 视频类工具（6 种）
- `list_videos` — 列出账户包中的所有视频
- `configure_video` — 配置单个视频（添加字幕、发布日期、媒体链接、声音设置）
- `batch_configure_videos` — 一次性配置多个视频
- `finalize_video` — 审批处于审核状态的视频
- `request_video_corrections` — 请求修改视频内容
- `unschedule_video` — 取消已安排的视频发布

### 已创建的账户类工具（3 种）
- `list_accounts` — 带有筛选条件的已创建账户列表
- `get_account_detail` — 获取账户的完整信息及 TokMail 邮箱地址
- `get_verification_code` — 获取最新的 6 位验证码

### 数据分析类工具（4 种）
- `get_analytics` — 获取粉丝数量、观看次数、互动率等数据
- `refresh_analytics` — 刷新数据分析（48 小时冷却时间，每月 500 次请求限制）
- `can_refresh_analytics` — 检查是否可以刷新数据分析
- `get_video_analytics` — 获取每个视频的详细分析数据（观看次数、点赞数、互动情况）

### 上传类工具（2 种，仅限 MCP 使用）
- `upload_video` — 上传本地视频文件，并返回公开链接
- `upload_image` — 上传本地图片文件（用于轮播图或个人资料图片）

## 示例工作流程

### 创建一个包含 5 个视频的 TikTok 账户

> “在美国创建一个包含 5 个视频的 TikTok 账户，并进行健身内容的推广”

代理将使用正确的参数调用 `create_bundle` 函数，然后指导您完成账户和视频的配置。

### 查看账户数据分析

> “显示我所有已创建账户的分析数据”

代理将先调用 `list_accounts`，然后为每个账户调用 `get_analytics` 函数。

### 批量分发视频

> “在法国创建 10 个每个包含 3 个视频的 TikTok 账户”

使用 `create_bulk_bundles` 函数一次性创建所有账户包。

## API 参考

- **基础 URL:** `https://app.tokportal.com/api/ext`
- **认证方式:** 使用 `X-API-Key` 头部字段进行身份验证
- **请求限制:** 每个 API 密钥每分钟 120 次请求
- **完整文档:** [developers.tokportal.com](https://developers.tokportal.com)

## 信用系统

TokPortal 采用基于信用点的计费模式（1 信用点 = 1 美元）：
- 账户创建：根据国家不同，费用为 5-8 信用点
- 视频上传：每个视频 2 信用点
- 内容推广：7 信用点
- Instagram 深度推广：40 信用点
- 评论审核：每个审核操作 25 信用点
- 视频编辑：每个编辑插槽 3 信用点

## 支持

- 文档：[developers.tokportal.com](https://developers.tokportal.com)
- 技术支持：team@tokportal.com
- npm 包：[tokportal-mcp](https://www.npmjs.com/package/tokportal-mcp)
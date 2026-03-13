---
name: github-watch
description: "Weekly GitHub digest for sysops/DevOps engineers. Fetches trending repos and topic:sysops/topic:devops repos, wraps content for LLM scoring, then dispatches HTML email via mail-client skill and Markdown to Nextcloud via nextcloud-files skill. Use when: running the weekly GitHub Watch pipeline, scoring and selecting repos for the digest, sending the digest by email or publishing to Nextcloud, or updating the seen-repos filter. NOT for: real-time GitHub search, PR/issue tracking, or repository management."
homepage: https://github.com/Rwx-G/openclaw-skill-github-watch
metadata:
  {
    "openclaw": {
      "emoji": "\ud83d\udc19",
      "env_vars": [
        {
          "name": "GITHUB_TOKEN",
          "required": false,
          "description": "GitHub Personal Access Token for higher API rate limits (5000 req/h vs 60). Can also be set via token_path in config.json."
        }
      ],
      "suggests": ["mail-client", "nextcloud-files"]
    }
  }
ontology:
  reads: [github_api, local_data_files]
  writes: [local_data_files]
  enhancedBy: [mail-client, nextcloud-files]
---

# GitHub Watch

每周的GitHub汇总：获取热门仓库以及与系统运维/DevOps相关的仓库，进行大语言模型（LLM）的评分处理，并发送相关邮件至指定邮箱，同时将汇总内容发布到Nextcloud平台。

## 依赖项

本脚本仅依赖标准库（`urllib.request`、`html.parser`、`json`、`pathlib`）。

## 配置文件

配置文件位于 `~/.openclaw/config/github-watch/config.json`，在 `clawhub` 更新后配置信息仍会保留。

```json
{
  "token_path": "~/.openclaw/secrets/github_token",
  "recipient": "you@example.com",
  "nc_path": "/Jarvis/github-watch.md",
  "outputs": ["email", "nextcloud"],
  "since": "weekly"
}
```

## 数据存储

- 配置信息：`~/.openclaw/config/github-watch/config.json`
- 已访问过的仓库信息：`~/.openclaw/data/github-watch/seen.json`
- 无需使用用户名和密码——运行时从 `token_path` 读取GitHub访问令牌。

## 脚本文件

所有脚本均保存在 `skills/github-watch/scripts/` 目录下：

### `fetch.py`

- 获取热门仓库以及与系统运维/DevOps相关的仓库。
- 生成包含 `wrapped_listing` 的JSON数据，用于后续的LLM评分处理。

```bash
GITHUB_TOKEN=$(cat ~/.openclaw/secrets/github_token) python3 fetch.py --filter-seen
```

主要输出字段：`trending`（热门仓库）、`sysops`（系统运维相关仓库）、`devops`（DevOps相关仓库）、`wrapped_listing`（仓库列表）、`count`（仓库数量）、`skipped_seen`（跳过的已访问仓库）。

### `send_email.py`

- 将处理后的HTML格式汇总内容通过 `mail-client` 脚本发送至指定邮箱。
- 从标准输入（stdin）读取评分后的JSON数据。

```bash
echo '{...scored_json...}' | python3 send_email.py [--to addr] [--dry-run]
```

**注意**：需要预先配置 `mail-client` 脚本。如果该脚本未安装，程序会优雅地跳过相关操作。

### `send_nc.py`

- 通过 `nextcloud-files` 脚本将Markdown格式的汇总内容发布到Nextcloud平台。
- 从标准输入（stdin）读取评分后的JSON数据。

**注意**：需要预先配置 `nextcloud-files` 脚本。

### `setup.py`

- 配置GitHub访问令牌的存储路径、邮件接收地址以及输出文件的路径。

```bash
python3 setup.py           # interactive
python3 setup.py --show    # print config
python3 setup.py --cleanup # remove config
```

## 完整的工作流程（通过Cron任务执行）

```
1. python3 fetch.py --filter-seen          -> raw JSON with wrapped_listing
2. Agent reads wrapped_listing, scores repos (see references/scoring_guide.md)
3. Agent builds scored JSON (sections + highlights)
4. echo scored_json | python3 send_email.py
5. echo scored_json | python3 send_nc.py
6. Notify Telegram (message tool)
```

## 评分流程

该脚本负责执行评分任务。具体评分规则和输出格式请参考 `references/scoring_guide.md` 文件。

评分流程如下：
- 将 `fetch.py` 生成的 `wrapped_listing` 数据传递给评分脚本。
- 评分脚本生成包含评分结果和重点信息的JSON数据。
- 将生成的JSON数据分别传递给 `send_email.py` 和 `send_nc.py` 脚本进行处理。

## 已访问仓库的跟踪

`seen_store.py` 脚本用于记录已访问过的仓库。`fetch.py` 会自动应用 `--filter-seen` 参数来过滤这些仓库。
当评分脚本选取新的仓库时，会通过 `seen_store.github_store.mark_seen(name)` 将这些仓库标记为已访问状态。

评分完成后，系统会自动更新 `seen_store.json` 文件中的记录。

**或者**：也可以在评分完成后手动执行 `seen_store.py` 脚本来更新记录。

## Cron任务设置

每周一上午9:00（欧洲/巴黎时间）执行Cron任务。Cron任务ID：`9edad21c-b3e2-43d4-9322-6c9af76ccb93`。

在将此脚本集成到系统中后，请将Cron任务的执行路径更新为 `skills/github-watch/scripts/` 目录下的脚本路径（而非之前的 `tools/` 目录）。

## 安全注意事项：

- **提示注入风险**：从GitHub获取的仓库名称、描述和原因等信息属于外部数据。`untrusted.py` 脚本会使用 `UNTRUSTED_NOTICE` 标记对这些数据进行标记，并对其中的标签分隔符进行转义处理，以防止被恶意利用。请注意，该脚本仅提供文本提示，并不构成技术性的安全防护措施；评分后的内容应被视为不可信的，不得在汇总邮件之外直接执行或转发。
- **令牌存储**：GitHub访问令牌存储在明文文件 `~/.openclaw/secrets/github_token` 中（权限设置为 `chmod 600`）。虽然这是本地脚本的常见做法，但该文件仍需妥善保护。令牌永远不会被包含在错误信息或日志中。
- **无外部依赖**：仅依赖标准库，无需安装额外的第三方库，因此不存在供应链安全风险。